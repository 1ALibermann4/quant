"""Orchestrate the I01 geometry. Vendor-agnostic. No SCI verdict."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date

import numpy as np

from quant.i01.baseline import b0_mean_homogeneity
from quant.i01.candidates import admissible_candidates, evaluation_indices
from quant.i01.diagnostics import PerTDiagnostics
from quant.i01.futures import all_future_vectors
from quant.i01.homogeneity import batch_homogeneity, homogeneity_bundle
from quant.i01.neighbors import l2_neighbors, library_l2_distances
from quant.i01.observations import ObservationSeries
from quant.i01.params import DEFAULT_PARAMS, I01Params
from quant.i01.returns import log_returns
from quant.i01.states import all_state_vectors


@dataclass(frozen=True, slots=True)
class ExampleNeighborhood:
    """One evaluated date, kept for the exploratory report."""

    t: int
    session: date
    x_t: tuple[float, ...]
    neighbor_ranks: tuple[int, ...]
    neighbor_sessions: tuple[date, ...]
    distances: tuple[float, ...]
    geo: dict[str, float]
    b0: dict[str, float]


@dataclass(frozen=True, slots=True)
class GeometryResult:
    """Full-run geometry. Not a scientific gate result."""

    n_sessions: int
    first_session: date
    last_session: date
    n_eval: int
    eval_first_session: date | None
    eval_last_session: date | None
    mean_geo: dict[str, float]
    mean_b0: dict[str, float]
    mean_delta: dict[str, float]
    example: ExampleNeighborhood | None
    per_t_geo_raw: tuple[float, ...] = field(repr=False)
    per_t_b0_raw: tuple[float, ...] = field(repr=False)
    per_t_sessions: tuple[date, ...] = field(repr=False)
    diagnostics: PerTDiagnostics | None = field(default=None, repr=False)


def _mean_bundle(rows: list[dict[str, float]]) -> dict[str, float]:
    keys = ("H_raw", "H_vol", "H_shape")
    return {key: float(np.mean([row[key] for row in rows])) for key in keys}


def run_geometry(
    series: ObservationSeries,
    params: I01Params | None = None,
    *,
    example_rank: int | None = None,
    progress: Callable[[int, int], None] | None = None,
) -> GeometryResult:
    """Compute geometric neighborhoods, H metrics and B0 on ``T_eval``.

    Does **not** compute p-values, SCI gates, PRED or ECON.
    """

    params = params or DEFAULT_PARAMS
    returns = log_returns(series)
    states = all_state_vectors(returns, params)
    futures = all_future_vectors(returns, params)
    eval_idx = evaluation_indices(len(series), params)
    if eval_idx.size == 0:
        raise ValueError(
            "no evaluation dates: series is shorter than the I01 technical minimum"
        )

    rng = np.random.default_rng(params.B0_seed)
    geo_rows: list[dict[str, float]] = []
    b0_rows: list[dict[str, float]] = []
    example: ExampleNeighborhood | None = None
    target_example = example_rank if example_rank is not None else int(eval_idx[0])
    raw_geo: list[float] = []
    raw_b0: list[float] = []
    eval_sessions: list[date] = []
    eval_ranks: list[int] = []
    geo_vol: list[float] = []
    geo_shape: list[float] = []
    b0_vol: list[float] = []
    b0_shape: list[float] = []
    age_median: list[float] = []
    age_q10: list[float] = []
    age_q90: list[float] = []
    d_rank1: list[float] = []
    d_rank_k: list[float] = []
    d_lib_median: list[float] = []
    rank_distance_sum = np.zeros(params.k, dtype=np.float64)
    pooled_ages: list[float] = []

    for step, t in enumerate(eval_idx, start=1):
        query = int(t)
        library = admissible_candidates(query, len(series), params)
        if library.shape[0] < params.L_min:
            raise ValueError(f"|L_t|={library.shape[0]} < L_min at t={t}")
        lib_d = library_l2_distances(states[query], states, library)
        neighbors, distances = l2_neighbors(states[query], states, library, params.k)
        geo = homogeneity_bundle(futures[neighbors], params.epsilon)
        picks = np.stack(
            [rng.choice(library, size=params.k, replace=False) for _ in range(params.B0_R)]
        )
        batched = batch_homogeneity(futures[picks], params.epsilon)
        b0 = {key: float(values.mean()) for key, values in batched.items()}
        geo_rows.append(geo)
        b0_rows.append(b0)
        raw_geo.append(geo["H_raw"])
        raw_b0.append(b0["H_raw"])
        geo_vol.append(geo["H_vol"])
        geo_shape.append(geo["H_shape"])
        b0_vol.append(b0["H_vol"])
        b0_shape.append(b0["H_shape"])
        eval_sessions.append(series.sessions[query])
        eval_ranks.append(query)
        ages = (query - neighbors).astype(np.float64)
        pooled_ages.extend(float(a) for a in ages)
        age_median.append(float(np.median(ages)))
        age_q10.append(float(np.quantile(ages, 0.10)))
        age_q90.append(float(np.quantile(ages, 0.90)))
        d_rank1.append(float(distances[0]))
        d_rank_k.append(float(distances[-1]))
        d_lib_median.append(float(np.median(lib_d)))
        rank_distance_sum += distances

        if progress is not None:
            progress(step, int(eval_idx.size))
        if int(t) == target_example or (
            example is None and int(t) == int(eval_idx[0])
        ):
            example = ExampleNeighborhood(
                t=int(t),
                session=series.sessions[int(t)],
                x_t=tuple(float(x) for x in states[t]),
                neighbor_ranks=tuple(int(i) for i in neighbors),
                neighbor_sessions=tuple(series.sessions[int(i)] for i in neighbors),
                distances=tuple(float(d) for d in distances),
                geo=geo,
                b0=b0,
            )

    mean_geo = _mean_bundle(geo_rows)
    mean_b0 = _mean_bundle(b0_rows)
    mean_delta = {key: mean_b0[key] - mean_geo[key] for key in mean_geo}
    ages = np.asarray(pooled_ages, dtype=np.float64)
    n_eval = max(len(eval_ranks), 1)
    qs = (0.10, 0.25, 0.50, 0.75, 0.90)
    qnames = ("q10", "q25", "median", "q75", "q90")
    pooled = {name: float(np.quantile(ages, q)) for name, q in zip(qnames, qs, strict=True)}
    pooled["mean"] = float(np.mean(ages))
    share = {
        "gt_252": float(np.mean(ages > 252.0)),
        "gt_1260": float(np.mean(ages > 1260.0)),
        "gt_2520": float(np.mean(ages > 2520.0)),
    }
    diagnostics = PerTDiagnostics(
        ranks=tuple(eval_ranks),
        sessions=tuple(eval_sessions),
        geo_raw=tuple(raw_geo),
        geo_vol=tuple(geo_vol),
        geo_shape=tuple(geo_shape),
        b0_raw=tuple(raw_b0),
        b0_vol=tuple(b0_vol),
        b0_shape=tuple(b0_shape),
        age_median=tuple(age_median),
        age_q10=tuple(age_q10),
        age_q90=tuple(age_q90),
        d_rank1=tuple(d_rank1),
        d_rank_k=tuple(d_rank_k),
        d_lib_median=tuple(d_lib_median),
        mean_distance_by_rank=tuple(float(x) for x in (rank_distance_sum / n_eval)),
        pooled_age_quantiles=pooled,
        neighbor_age_share=share,
    )
    return GeometryResult(
        n_sessions=len(series),
        first_session=series.sessions[0],
        last_session=series.sessions[-1],
        n_eval=int(eval_idx.size),
        eval_first_session=eval_sessions[0],
        eval_last_session=eval_sessions[-1],
        mean_geo=mean_geo,
        mean_b0=mean_b0,
        mean_delta=mean_delta,
        example=example,
        per_t_geo_raw=tuple(raw_geo),
        per_t_b0_raw=tuple(raw_b0),
        per_t_sessions=tuple(eval_sessions),
        diagnostics=diagnostics,
    )


# Re-export for tests that want the unused symbol documented.
__all__ = ["ExampleNeighborhood", "GeometryResult", "run_geometry", "b0_mean_homogeneity"]
