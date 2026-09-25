"""Query-level and series-level I02 evaluation pipeline (aligned PREREG-v0.3)."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from quant.i02.crps import crps_empirical
from quant.i02.distances import (
    build_L_D_Q_series,
    pairwise_s1,
    pairwise_s2,
    pairwise_s3_phi,
    pairwise_s3_q,
    pairwise_x,
)
from quant.i02.estimand import relative_incremental_value, score_difference
from quant.i02.features import realized_rms_volatility
from quant.i02.neighbors import select_neighbors
from quant.i02.params import DEFAULT_PARAMS, I02Params
from quant.i02.pool import admissible_pool, representation_constructible
from quant.i02.regime import z_vector
from quant.i02.states_x import (
    XUndefinedError,
    all_state_vectors_x,
    first_valid_x_index,
    state_vector_x,
)
from quant.i02.target import future_realized_rms
from quant.i02.types import SkipReason


@dataclass(slots=True)
class RepresentationForecast:
    """Empirical predictive atoms and scores for one representation / chart."""

    name: str
    neighbor_indices: np.ndarray
    neighbor_distances: np.ndarray
    atoms: np.ndarray
    crps: float


@dataclass(slots=True)
class QueryResult:
    """Typed deterministic result for one query ``t``."""

    t: int
    skipped: bool
    skip_reasons: list[SkipReason] = field(default_factory=list)
    pool_size: int = 0
    pool_indices: np.ndarray | None = None
    v_obs: float | None = None
    forecasts: dict[str, RepresentationForecast] = field(default_factory=dict)
    d: dict[str, float | None] = field(default_factory=dict)
    r: dict[str, float | None] = field(default_factory=dict)
    z: dict[int, float | None] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)


def _atoms_from_neighbors(
    neighbor_idx: np.ndarray,
    v_series: np.ndarray,
) -> np.ndarray:
    return np.asarray([v_series[int(s)] for s in neighbor_idx], dtype=np.float64)


def _attach_comparator(
    result: QueryResult,
    *,
    name: str,
    pool: np.ndarray,
    distances: np.ndarray,
    v_series: np.ndarray,
    v_obs: float,
    crps_x: float,
    params: I02Params,
) -> None:
    nbrs, dists = select_neighbors(pool, distances, params.k)
    atoms = _atoms_from_neighbors(nbrs, v_series)
    crps_s = crps_empirical(atoms, v_obs)
    result.forecasts[name] = RepresentationForecast(
        name=name,
        neighbor_indices=nbrs,
        neighbor_distances=dists,
        atoms=atoms,
        crps=crps_s,
    )
    result.d[name] = score_difference(crps_s, crps_x)
    r_val, reason = relative_incremental_value(crps_s, crps_x)
    result.r[name] = r_val
    if reason is not None:
        result.skip_reasons.append(reason)
        result.notes.append(f"R^({name}) undefined: CRPS_S == 0")


def evaluate_query(
    returns: np.ndarray,
    t: int,
    *,
    params: I02Params = DEFAULT_PARAMS,
    states_x: np.ndarray | None = None,
    L: np.ndarray | None = None,
    D: np.ndarray | None = None,
    Q: np.ndarray | None = None,
    v_series: np.ndarray | None = None,
    constructible: np.ndarray | None = None,
) -> QueryResult:
    """Evaluate one query under the frozen v0.3 contract.

    Comparators: ``S1``, ``S2``, ``S3_Q``, ``S3_phi`` (no primary; both S3
    charts always reported when the query is evaluable).
    """

    returns = np.asarray(returns, dtype=np.float64)
    n = returns.shape[0]
    result = QueryResult(t=t, skipped=False)

    if t < 0 or t >= n:
        result.skipped = True
        result.skip_reasons.append(SkipReason.QUERY_OUT_OF_RANGE)
        return result

    if t + params.h >= n:
        result.skipped = True
        result.skip_reasons.append(SkipReason.INSUFFICIENT_TARGET_HISTORY)
        return result

    if t < first_valid_x_index(params):
        result.skipped = True
        result.skip_reasons.append(SkipReason.INSUFFICIENT_X_HISTORY)
        return result

    try:
        state_vector_x(returns, t, params)
    except XUndefinedError as exc:
        result.skipped = True
        result.skip_reasons.append(exc.reason)
        return result

    if constructible is not None:
        query_ok = bool(constructible[t])
    else:
        query_ok = representation_constructible(returns, t, params)
    if not query_ok:
        try:
            rv = realized_rms_volatility(returns, t, params.W_RV)
            if rv == 0.0:
                result.skip_reasons.append(SkipReason.RV_ZERO)
        except ValueError:
            result.skip_reasons.append(SkipReason.INSUFFICIENT_RV_HISTORY)
        result.skipped = True
        if not result.skip_reasons:
            result.skip_reasons.append(SkipReason.INSUFFICIENT_RV_HISTORY)
        return result

    pool = admissible_pool(
        returns, t, params, constructible=constructible
    )
    result.pool_indices = pool
    result.pool_size = int(pool.shape[0])
    if result.pool_size < params.k:
        result.skipped = True
        result.skip_reasons.append(SkipReason.INSUFFICIENT_ADMISSIBLE_POOL)
        return result

    if states_x is None:
        states_x = all_state_vectors_x(returns, params)
    if L is None or D is None or Q is None:
        L, D, Q = build_L_D_Q_series(returns, params)
    if v_series is None:
        from quant.i02.target import all_future_realized_rms

        v_series = all_future_realized_rms(returns, params)

    try:
        v_obs = future_realized_rms(returns, t, params)
    except ValueError:
        result.skipped = True
        result.skip_reasons.append(SkipReason.INSUFFICIENT_TARGET_HISTORY)
        return result
    result.v_obs = v_obs

    # X
    dx = pairwise_x(states_x, pool, t)
    nx, dist_x = select_neighbors(pool, dx, params.k)
    atoms_x = _atoms_from_neighbors(nx, v_series)
    crps_x = crps_empirical(atoms_x, v_obs)
    result.forecasts["X"] = RepresentationForecast(
        name="X",
        neighbor_indices=nx,
        neighbor_distances=dist_x,
        atoms=atoms_x,
        crps=crps_x,
    )

    _attach_comparator(
        result,
        name="S1",
        pool=pool,
        distances=pairwise_s1(L, pool, t),
        v_series=v_series,
        v_obs=v_obs,
        crps_x=crps_x,
        params=params,
    )
    _attach_comparator(
        result,
        name="S2",
        pool=pool,
        distances=pairwise_s2(L, D, pool, t),
        v_series=v_series,
        v_obs=v_obs,
        crps_x=crps_x,
        params=params,
    )
    # S3-A: both charts, no selection
    _attach_comparator(
        result,
        name="S3_Q",
        pool=pool,
        distances=pairwise_s3_q(L, Q, pool, t),
        v_series=v_series,
        v_obs=v_obs,
        crps_x=crps_x,
        params=params,
    )
    _attach_comparator(
        result,
        name="S3_phi",
        pool=pool,
        distances=pairwise_s3_phi(L, Q, pool, t),
        v_series=v_series,
        v_obs=v_obs,
        crps_x=crps_x,
        params=params,
    )

    zmap, zreasons = z_vector(returns, t, params)
    result.z = zmap
    result.skip_reasons.extend(zreasons)
    return result


def evaluate_series(
    returns: np.ndarray,
    *,
    params: I02Params = DEFAULT_PARAMS,
    query_indices: np.ndarray | None = None,
) -> list[QueryResult]:
    """Evaluate a stride-1 (or provided) query schedule. No market data."""

    from quant.i02.pool import constructible_mask, query_schedule
    from quant.i02.target import all_future_realized_rms

    returns = np.asarray(returns, dtype=np.float64)
    if query_indices is None:
        query_indices = query_schedule(len(returns), params)
    states_x = all_state_vectors_x(returns, params)
    L, D, Q = build_L_D_Q_series(returns, params)
    v_series = all_future_realized_rms(returns, params)
    constructible = constructible_mask(
        returns, params, states_x=states_x, L=L, D=D, Q=Q
    )
    out: list[QueryResult] = []
    n_q = len(query_indices)
    for i, t in enumerate(query_indices):
        if i > 0 and i % 500 == 0:
            print(f"I02 evaluate_series: {i}/{n_q} queries", flush=True)
        out.append(
            evaluate_query(
                returns,
                int(t),
                params=params,
                states_x=states_x,
                L=L,
                D=D,
                Q=Q,
                v_series=v_series,
                constructible=constructible,
            )
        )
    return out
