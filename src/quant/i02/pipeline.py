"""Query-level and series-level I02 evaluation pipeline (L1).

Implements X / S1 / S2 paths fully. S3 neighbor path is blocked by
:data:`S3_KNN_AGGREGATION_GAP`. Bootstrap inference is blocked by
:data:`BOOTSTRAP_ALGORITHM_GAP`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from quant.i02.contract_gaps import (
    ImplementationContractGap,
    S3_KNN_AGGREGATION_GAP,
)
from quant.i02.crps import crps_empirical
from quant.i02.distances import build_L_D_series, pairwise_s1, pairwise_s2, pairwise_x
from quant.i02.estimand import relative_incremental_value, score_difference
from quant.i02.features import realized_rms_volatility
from quant.i02.neighbors import select_neighbors
from quant.i02.params import DEFAULT_PARAMS, I02Params
from quant.i02.pool import admissible_pool, representation_constructible
from quant.i02.regime import z_vector
from quant.i02.states_x import all_state_vectors_x, first_valid_x_index
from quant.i02.target import future_realized_rms
from quant.i02.types import SkipReason


@dataclass(slots=True)
class RepresentationForecast:
    """Empirical predictive atoms and scores for one representation."""

    name: str
    neighbor_indices: np.ndarray
    neighbor_distances: np.ndarray
    atoms: np.ndarray
    crps: float


@dataclass(slots=True)
class QueryResult:
    """Typed deterministic result for one query ``t`` (prereg L1 §10)."""

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
    """Preserve multiplicity: one atom per neighbor (no dedup)."""

    return np.asarray([v_series[int(s)] for s in neighbor_idx], dtype=np.float64)


def evaluate_query(
    returns: np.ndarray,
    t: int,
    *,
    params: I02Params = DEFAULT_PARAMS,
    states_x: np.ndarray | None = None,
    L: np.ndarray | None = None,
    D: np.ndarray | None = None,
    v_series: np.ndarray | None = None,
) -> QueryResult:
    """Evaluate one query date under the frozen contract.

    Scientific values are separated from skip provenance. S3 kNN is not
    invented: the result records ``S3_CONTRACT_GAP`` instead of a fake
    ``R^(S3)``.
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

    if not representation_constructible(returns, t, params):
        # Query itself must support L/D for S1/S2 distances.
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

    pool = admissible_pool(returns, t, params)
    result.pool_indices = pool
    result.pool_size = int(pool.shape[0])
    if result.pool_size < params.k:
        result.skipped = True
        result.skip_reasons.append(SkipReason.INSUFFICIENT_ADMISSIBLE_POOL)
        return result

    if states_x is None:
        states_x = all_state_vectors_x(returns, params)
    if L is None or D is None:
        L, D = build_L_D_series(returns, params)
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

    # --- X ---
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

    # --- S1 ---
    d1 = pairwise_s1(L, pool, t)
    n1, dist_1 = select_neighbors(pool, d1, params.k)
    atoms_1 = _atoms_from_neighbors(n1, v_series)
    crps_1 = crps_empirical(atoms_1, v_obs)
    result.forecasts["S1"] = RepresentationForecast(
        name="S1",
        neighbor_indices=n1,
        neighbor_distances=dist_1,
        atoms=atoms_1,
        crps=crps_1,
    )
    result.d["S1"] = score_difference(crps_1, crps_x)
    r1, reason1 = relative_incremental_value(crps_1, crps_x)
    result.r["S1"] = r1
    if reason1 is not None:
        result.skip_reasons.append(reason1)
        result.notes.append("R^(S1) undefined: CRPS_S1 == 0")

    # --- S2 (primary d_2) ---
    d2 = pairwise_s2(L, D, pool, t)
    n2, dist_2 = select_neighbors(pool, d2, params.k)
    atoms_2 = _atoms_from_neighbors(n2, v_series)
    crps_2 = crps_empirical(atoms_2, v_obs)
    result.forecasts["S2"] = RepresentationForecast(
        name="S2",
        neighbor_indices=n2,
        neighbor_distances=dist_2,
        atoms=atoms_2,
        crps=crps_2,
    )
    result.d["S2"] = score_difference(crps_2, crps_x)
    r2, reason2 = relative_incremental_value(crps_2, crps_x)
    result.r["S2"] = r2
    if reason2 is not None:
        result.skip_reasons.append(reason2)
        result.notes.append("R^(S2) undefined: CRPS_S2 == 0")

    # --- S3 blocked ---
    result.d["S3"] = None
    result.r["S3"] = None
    result.skip_reasons.append(SkipReason.S3_CONTRACT_GAP)
    result.notes.append(S3_KNN_AGGREGATION_GAP.strip().splitlines()[0])

    # --- Z (does not affect forecasts) ---
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
    """Evaluate a stride-1 (or provided) query schedule.

    Precomputes shared series for determinism and speed. Does not load
    market data. Does not run bootstrap inference.
    """

    from quant.i02.pool import query_schedule
    from quant.i02.target import all_future_realized_rms

    returns = np.asarray(returns, dtype=np.float64)
    if query_indices is None:
        query_indices = query_schedule(len(returns), params)
    states_x = all_state_vectors_x(returns, params)
    L, D = build_L_D_series(returns, params)
    v_series = all_future_realized_rms(returns, params)
    out: list[QueryResult] = []
    for t in query_indices:
        out.append(
            evaluate_query(
                returns,
                int(t),
                params=params,
                states_x=states_x,
                L=L,
                D=D,
                v_series=v_series,
            )
        )
    return out


def assert_s3_gap() -> None:
    """Helper for tests: S3 distance must raise the contract gap."""

    from quant.i02.distances import distance_s3_blocked

    try:
        distance_s3_blocked()
    except ImplementationContractGap:
        return
    raise AssertionError("expected ImplementationContractGap for S3")
