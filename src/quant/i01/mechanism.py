"""Exploratory volatility-mechanism diagnostics.

Does not change ``W``, ``k``, ``h``, L2 or B0. The past-volatility neighborhood
is a *diagnostic control*, not a confirmatory baseline and not a replacement
for B0 (DR-007 D-4).
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date

import numpy as np

from quant.i01.candidates import admissible_candidates, evaluation_indices
from quant.i01.futures import all_future_vectors
from quant.i01.homogeneity import batch_homogeneity, homogeneity_bundle
from quant.i01.neighbors import l2_neighbors
from quant.i01.observations import ObservationSeries
from quant.i01.params import DEFAULT_PARAMS, I01Params
from quant.i01.returns import log_returns
from quant.i01.standardization import causal_mu_sigma
from quant.i01.states import all_state_vectors


@dataclass(frozen=True, slots=True)
class PastFeatures:
    """Causal descriptors of the past window. Selection must not read ``Y``."""

    rv_w: np.ndarray
    sigma_m: np.ndarray
    x_norm: np.ndarray
    raw_amp: np.ndarray
    window_sum: np.ndarray


@dataclass(frozen=True, slots=True)
class MechanismResult:
    """L2 vs past-vol control vs B0. Not a SCI verdict."""

    n_sessions: int
    first_session: date
    last_session: date
    n_eval: int
    eval_first_session: date
    eval_last_session: date
    mean_geo: dict[str, float]
    mean_b0: dict[str, float]
    mean_volctrl: dict[str, float]
    mean_delta_b0_minus_geo: dict[str, float]
    mean_delta_b0_minus_volctrl: dict[str, float]
    mean_delta_volctrl_minus_geo: dict[str, float]
    past_vol_proximity: dict[str, float]
    associations: dict[str, float]
    frac_t_geo_vol_lt_ctrl: float
    frac_t_geo_vol_lt_b0: float
    frac_t_ctrl_vol_lt_b0: float
    note: str
    sessions: tuple[date, ...] = field(repr=False)
    per_t_h_vol_geo: tuple[float, ...] = field(repr=False)
    per_t_h_vol_ctrl: tuple[float, ...] = field(repr=False)
    per_t_h_vol_b0: tuple[float, ...] = field(repr=False)


def past_window_features(
    returns: np.ndarray,
    states: np.ndarray,
    params: I01Params,
) -> PastFeatures:
    """Vol / energy of the past window from ``O_<=t`` only."""

    n = returns.shape[0]
    rv_w = np.full(n, np.nan, dtype=np.float64)
    sigma_m = np.full(n, np.nan, dtype=np.float64)
    x_norm = np.full(n, np.nan, dtype=np.float64)
    raw_amp = np.full(n, np.nan, dtype=np.float64)
    window_sum = np.full(n, np.nan, dtype=np.float64)
    for t in range(params.M, n):
        window = returns[t - params.W + 1 : t + 1]
        rv_w[t] = float(np.std(window, ddof=1))
        raw_amp[t] = float(np.linalg.norm(window))
        window_sum[t] = float(np.sum(window))
        _mu, sigma = causal_mu_sigma(returns, t, params)
        sigma_m[t] = sigma
        x_norm[t] = float(np.linalg.norm(states[t]))
    return PastFeatures(
        rv_w=rv_w,
        sigma_m=sigma_m,
        x_norm=x_norm,
        raw_amp=raw_amp,
        window_sum=window_sum,
    )


@dataclass(frozen=True, slots=True)
class PairedHomogeneity:
    """Per-date L2 vs ``rv_W`` control. No B0 — E04 reads these series only."""

    ranks: tuple[int, ...]
    sessions: tuple[date, ...]
    h_raw_geo: np.ndarray
    h_vol_geo: np.ndarray
    h_raw_ctrl: np.ndarray
    h_vol_ctrl: np.ndarray
    rv_w: np.ndarray
    x_norm: np.ndarray
    window_sum: np.ndarray


def collect_paired_homogeneity(
    series: ObservationSeries,
    params: I01Params | None = None,
    *,
    progress: Callable[[int, int], None] | None = None,
) -> PairedHomogeneity:
    """Same ``L_t`` / L2 / ``rv_W`` neighbors as E03. Does not draw B0."""

    params = params or DEFAULT_PARAMS
    returns = log_returns(series)
    states = all_state_vectors(returns, params)
    futures = all_future_vectors(returns, params)
    features = past_window_features(returns, states, params)
    eval_idx = evaluation_indices(len(series), params)
    if eval_idx.size == 0:
        raise ValueError("no evaluation dates: series is shorter than the I01 technical minimum")

    ranks: list[int] = []
    sessions: list[date] = []
    h_raw_geo: list[float] = []
    h_vol_geo: list[float] = []
    h_raw_ctrl: list[float] = []
    h_vol_ctrl: list[float] = []
    rv_w: list[float] = []
    x_norm: list[float] = []
    window_sum: list[float] = []

    for step, t in enumerate(eval_idx, start=1):
        query = int(t)
        library = admissible_candidates(query, len(series), params)
        if library.shape[0] < params.L_min:
            raise ValueError(f"|L_t|={library.shape[0]} < L_min at t={t}")
        neighbors, _ = l2_neighbors(states[query], states, library, params.k)
        ctrl, _ = scalar_neighbors(float(features.rv_w[query]), features.rv_w, library, params.k)
        geo = homogeneity_bundle(futures[neighbors], params.epsilon)
        ctrl_h = homogeneity_bundle(futures[ctrl], params.epsilon)
        ranks.append(query)
        sessions.append(series.sessions[query])
        h_raw_geo.append(geo["H_raw"])
        h_vol_geo.append(geo["H_vol"])
        h_raw_ctrl.append(ctrl_h["H_raw"])
        h_vol_ctrl.append(ctrl_h["H_vol"])
        rv_w.append(float(features.rv_w[query]))
        x_norm.append(float(features.x_norm[query]))
        window_sum.append(float(features.window_sum[query]))
        if progress is not None:
            progress(step, int(eval_idx.size))

    return PairedHomogeneity(
        ranks=tuple(ranks),
        sessions=tuple(sessions),
        h_raw_geo=np.asarray(h_raw_geo, dtype=np.float64),
        h_vol_geo=np.asarray(h_vol_geo, dtype=np.float64),
        h_raw_ctrl=np.asarray(h_raw_ctrl, dtype=np.float64),
        h_vol_ctrl=np.asarray(h_vol_ctrl, dtype=np.float64),
        rv_w=np.asarray(rv_w, dtype=np.float64),
        x_norm=np.asarray(x_norm, dtype=np.float64),
        window_sum=np.asarray(window_sum, dtype=np.float64),
    )


def scalar_neighbors(
    query_value: float,
    values: np.ndarray,
    library: np.ndarray,
    k: int,
) -> tuple[np.ndarray, np.ndarray]:
    """``k`` library ranks closest in ``|v_s - v_t|``. Ties: oldest rank."""

    if library.shape[0] < k:
        raise ValueError(f"library size {library.shape[0]} < k={k}")
    distances = np.abs(values[library] - query_value)
    order = np.lexsort((library, distances))
    chosen = order[:k]
    return library[chosen], distances[chosen]


def _mean_bundle(rows: list[dict[str, float]]) -> dict[str, float]:
    keys = ("H_raw", "H_vol", "H_shape")
    return {key: float(np.mean([row[key] for row in rows])) for key in keys}


def _pearson(x: np.ndarray, y: np.ndarray) -> float:
    if x.size < 2 or float(np.std(x)) == 0.0 or float(np.std(y)) == 0.0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def run_vol_mechanism(
    series: ObservationSeries,
    params: I01Params | None = None,
    *,
    progress: Callable[[int, int], None] | None = None,
) -> MechanismResult:
    """Same ``L_t`` / L2 / B0 as I01. Adds a past-``rv_W`` diagnostic neighborhood."""

    params = params or DEFAULT_PARAMS
    returns = log_returns(series)
    states = all_state_vectors(returns, params)
    futures = all_future_vectors(returns, params)
    features = past_window_features(returns, states, params)
    y_amp = np.linalg.norm(futures, axis=1)
    eval_idx = evaluation_indices(len(series), params)
    if eval_idx.size == 0:
        raise ValueError("no evaluation dates: series is shorter than the I01 technical minimum")

    rng = np.random.default_rng(params.B0_seed)
    geo_rows: list[dict[str, float]] = []
    b0_rows: list[dict[str, float]] = []
    ctrl_rows: list[dict[str, float]] = []
    sessions: list[date] = []
    h_vol_geo: list[float] = []
    h_vol_ctrl: list[float] = []
    h_vol_b0: list[float] = []
    geo_rv_gap: list[float] = []
    ctrl_rv_gap: list[float] = []
    lib_rv_gap: list[float] = []
    assoc_rv: list[float] = []
    assoc_sigma: list[float] = []
    assoc_xnorm: list[float] = []
    assoc_y: list[float] = []

    for step, t in enumerate(eval_idx, start=1):
        query = int(t)
        library = admissible_candidates(query, len(series), params)
        if library.shape[0] < params.L_min:
            raise ValueError(f"|L_t|={library.shape[0]} < L_min at t={t}")

        neighbors, _distances = l2_neighbors(states[query], states, library, params.k)
        ctrl, _ctrl_d = scalar_neighbors(float(features.rv_w[query]), features.rv_w, library, params.k)

        geo = homogeneity_bundle(futures[neighbors], params.epsilon)
        ctrl_h = homogeneity_bundle(futures[ctrl], params.epsilon)
        picks = np.stack(
            [rng.choice(library, size=params.k, replace=False) for _ in range(params.B0_R)]
        )
        batched = batch_homogeneity(futures[picks], params.epsilon)
        b0 = {key: float(values.mean()) for key, values in batched.items()}

        geo_rows.append(geo)
        ctrl_rows.append(ctrl_h)
        b0_rows.append(b0)
        sessions.append(series.sessions[query])
        h_vol_geo.append(geo["H_vol"])
        h_vol_ctrl.append(ctrl_h["H_vol"])
        h_vol_b0.append(b0["H_vol"])

        q_rv = float(features.rv_w[query])
        geo_rv_gap.append(float(np.mean(np.abs(features.rv_w[neighbors] - q_rv))))
        ctrl_rv_gap.append(float(np.mean(np.abs(features.rv_w[ctrl] - q_rv))))
        lib_rv_gap.append(float(np.median(np.abs(features.rv_w[library] - q_rv))))
        assoc_rv.append(q_rv)
        assoc_sigma.append(float(features.sigma_m[query]))
        assoc_xnorm.append(float(features.x_norm[query]))
        assoc_y.append(float(y_amp[query]))

        if progress is not None:
            progress(step, int(eval_idx.size))

    mean_geo = _mean_bundle(geo_rows)
    mean_b0 = _mean_bundle(b0_rows)
    mean_volctrl = _mean_bundle(ctrl_rows)
    keys = ("H_raw", "H_vol", "H_shape")
    geo_v = np.asarray(h_vol_geo, dtype=np.float64)
    ctrl_v = np.asarray(h_vol_ctrl, dtype=np.float64)
    b0_v = np.asarray(h_vol_b0, dtype=np.float64)
    rv = np.asarray(assoc_rv, dtype=np.float64)
    sig = np.asarray(assoc_sigma, dtype=np.float64)
    xn = np.asarray(assoc_xnorm, dtype=np.float64)
    ya = np.asarray(assoc_y, dtype=np.float64)

    note = (
        "Exploratory diagnostic. The past-volatility neighborhood is not B0, "
        "not a SCI gate, and not a reason to retune W/k/h/L2/B0."
    )
    return MechanismResult(
        n_sessions=len(series),
        first_session=series.sessions[0],
        last_session=series.sessions[-1],
        n_eval=int(eval_idx.size),
        eval_first_session=sessions[0],
        eval_last_session=sessions[-1],
        mean_geo=mean_geo,
        mean_b0=mean_b0,
        mean_volctrl=mean_volctrl,
        mean_delta_b0_minus_geo={key: mean_b0[key] - mean_geo[key] for key in keys},
        mean_delta_b0_minus_volctrl={key: mean_b0[key] - mean_volctrl[key] for key in keys},
        mean_delta_volctrl_minus_geo={key: mean_volctrl[key] - mean_geo[key] for key in keys},
        past_vol_proximity={
            "mean_abs_drv_geo_neighbors": float(np.mean(geo_rv_gap)),
            "mean_abs_drv_volctrl_neighbors": float(np.mean(ctrl_rv_gap)),
            "mean_median_abs_drv_library": float(np.mean(lib_rv_gap)),
            "geo_over_library": float(
                np.mean(geo_rv_gap) / max(float(np.mean(lib_rv_gap)), 1e-15)
            ),
            "volctrl_over_library": float(
                np.mean(ctrl_rv_gap) / max(float(np.mean(lib_rv_gap)), 1e-15)
            ),
        },
        associations={
            "corr_rv_w_future_amp": _pearson(rv, ya),
            "corr_sigma_m_future_amp": _pearson(sig, ya),
            "corr_x_norm_future_amp": _pearson(xn, ya),
            "corr_rv_w_sigma_m": _pearson(rv, sig),
            "corr_x_norm_rv_w": _pearson(xn, rv),
        },
        frac_t_geo_vol_lt_ctrl=float(np.mean(geo_v < ctrl_v)),
        frac_t_geo_vol_lt_b0=float(np.mean(geo_v < b0_v)),
        frac_t_ctrl_vol_lt_b0=float(np.mean(ctrl_v < b0_v)),
        note=note,
        sessions=tuple(sessions),
        per_t_h_vol_geo=tuple(h_vol_geo),
        per_t_h_vol_ctrl=tuple(h_vol_ctrl),
        per_t_h_vol_b0=tuple(h_vol_b0),
    )


def yearly_h_vol(result: MechanismResult) -> list[dict[str, float | int]]:
    """Mean ``H_vol`` by calendar year of ``t`` — description only."""

    buckets: dict[int, list[int]] = defaultdict(list)
    for i, session in enumerate(result.sessions):
        buckets[session.year].append(i)
    geo = np.asarray(result.per_t_h_vol_geo, dtype=np.float64)
    ctrl = np.asarray(result.per_t_h_vol_ctrl, dtype=np.float64)
    b0 = np.asarray(result.per_t_h_vol_b0, dtype=np.float64)
    rows: list[dict[str, float | int]] = []
    for year in sorted(buckets):
        idx = np.asarray(buckets[year], dtype=np.intp)
        rows.append(
            {
                "year": year,
                "n": int(idx.size),
                "mean_h_vol_geo": float(np.mean(geo[idx])),
                "mean_h_vol_volctrl": float(np.mean(ctrl[idx])),
                "mean_h_vol_b0": float(np.mean(b0[idx])),
            }
        )
    return rows


def summarize_mechanism(result: MechanismResult) -> dict:
    """JSON-safe bundle. No class verdict, no gate."""

    return {
        "mean_H_geo": result.mean_geo,
        "mean_H_B0": result.mean_b0,
        "mean_H_volctrl": result.mean_volctrl,
        "mean_delta_B0_minus_geo": result.mean_delta_b0_minus_geo,
        "mean_delta_B0_minus_volctrl": result.mean_delta_b0_minus_volctrl,
        "mean_delta_volctrl_minus_geo": result.mean_delta_volctrl_minus_geo,
        "past_vol_proximity": result.past_vol_proximity,
        "associations": result.associations,
        "frac_t_geo_vol_lt_ctrl": result.frac_t_geo_vol_lt_ctrl,
        "frac_t_geo_vol_lt_b0": result.frac_t_geo_vol_lt_b0,
        "frac_t_ctrl_vol_lt_b0": result.frac_t_ctrl_vol_lt_b0,
        "yearly_h_vol": yearly_h_vol(result),
        "note": result.note,
    }
