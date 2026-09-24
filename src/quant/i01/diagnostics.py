"""Exploratory summaries of an I01 geometry run.

These functions describe *where* a Δ came from. They do not change ``W``,
``k``, ``h``, L2 or B0, and they do not emit a SCI verdict.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date

import numpy as np


@dataclass(frozen=True, slots=True)
class PerTDiagnostics:
    """Aligned per-evaluation-date series. Session ranks, not a calendar."""

    ranks: tuple[int, ...]
    sessions: tuple[date, ...]
    geo_raw: tuple[float, ...]
    geo_vol: tuple[float, ...]
    geo_shape: tuple[float, ...]
    b0_raw: tuple[float, ...]
    b0_vol: tuple[float, ...]
    b0_shape: tuple[float, ...]
    age_median: tuple[float, ...]
    age_q10: tuple[float, ...]
    age_q90: tuple[float, ...]
    d_rank1: tuple[float, ...]
    d_rank_k: tuple[float, ...]
    d_lib_median: tuple[float, ...]
    mean_distance_by_rank: tuple[float, ...]
    pooled_age_quantiles: dict[str, float]
    neighbor_age_share: dict[str, float]


def _arr(values: tuple[float, ...]) -> np.ndarray:
    return np.asarray(values, dtype=np.float64)


def _quantiles(sample: np.ndarray) -> dict[str, float]:
    qs = (0.10, 0.25, 0.50, 0.75, 0.90)
    names = ("q10", "q25", "median", "q75", "q90")
    out = {name: float(np.quantile(sample, q)) for name, q in zip(names, qs, strict=True)}
    out["mean"] = float(np.mean(sample))
    out["min"] = float(np.min(sample))
    out["max"] = float(np.max(sample))
    return out


def relative_reductions(geo: dict[str, float], b0: dict[str, float]) -> dict[str, float]:
    """``(H_B0 - H_geo) / H_B0`` per metric. Undefined if B0 is 0."""

    out: dict[str, float] = {}
    for key in ("H_raw", "H_vol", "H_shape"):
        denom = b0[key]
        out[key] = float("nan") if denom == 0.0 else (denom - geo[key]) / denom
    return out


def delta_series(per_t: PerTDiagnostics) -> dict[str, np.ndarray]:
    """``Δ = H_B0 - H_geo`` (positive ⇒ geo more homogeneous)."""

    return {
        "raw": _arr(per_t.b0_raw) - _arr(per_t.geo_raw),
        "vol": _arr(per_t.b0_vol) - _arr(per_t.geo_vol),
        "shape": _arr(per_t.b0_shape) - _arr(per_t.geo_shape),
    }


def temporal_by_year(per_t: PerTDiagnostics) -> list[dict[str, float | int]]:
    """Mean Δ and share of dates with Δ_raw > 0, grouped by calendar year of ``t``."""

    deltas = delta_series(per_t)
    buckets: dict[int, list[int]] = defaultdict(list)
    for i, session in enumerate(per_t.sessions):
        buckets[session.year].append(i)
    rows: list[dict[str, float | int]] = []
    total_raw = float(np.sum(deltas["raw"]))
    for year in sorted(buckets):
        idx = np.asarray(buckets[year], dtype=np.intp)
        raw = deltas["raw"][idx]
        vol = deltas["vol"][idx]
        shape = deltas["shape"][idx]
        rows.append(
            {
                "year": year,
                "n": int(idx.size),
                "mean_delta_raw": float(np.mean(raw)),
                "mean_delta_vol": float(np.mean(vol)),
                "mean_delta_shape": float(np.mean(shape)),
                "frac_delta_raw_positive": float(np.mean(raw > 0.0)),
                "share_of_sum_delta_raw": (
                    float("nan") if total_raw == 0.0 else float(np.sum(raw) / total_raw)
                ),
            }
        )
    return rows


def pearson(x: np.ndarray, y: np.ndarray) -> float:
    """Pearson correlation; NaN if a series is constant."""

    if x.size < 2 or float(np.std(x)) == 0.0 or float(np.std(y)) == 0.0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def descriptive_raw_association(per_t: PerTDiagnostics) -> dict[str, float]:
    """OLS ``Δ_raw ~ Δ_vol + Δ_shape`` — description only, not a gate."""

    d = delta_series(per_t)
    y = d["raw"]
    x = np.column_stack([np.ones(y.shape[0]), d["vol"], d["shape"]])
    beta, _, _, _ = np.linalg.lstsq(x, y, rcond=None)
    fitted = x @ beta
    ss_res = float(np.sum((y - fitted) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = float("nan") if ss_tot == 0.0 else 1.0 - ss_res / ss_tot
    return {
        "intercept": float(beta[0]),
        "coef_delta_vol": float(beta[1]),
        "coef_delta_shape": float(beta[2]),
        "r_squared": r2,
        "corr_raw_vol": pearson(d["raw"], d["vol"]),
        "corr_raw_shape": pearson(d["raw"], d["shape"]),
        "corr_vol_shape": pearson(d["vol"], d["shape"]),
        "frac_raw_positive": float(np.mean(d["raw"] > 0.0)),
        "frac_vol_positive": float(np.mean(d["vol"] > 0.0)),
        "frac_shape_positive": float(np.mean(d["shape"] > 0.0)),
    }


def tertile_age_medians(per_t: PerTDiagnostics) -> dict[str, float]:
    """Median-of-medians neighbor age on chronological tertiles of ``T_eval``."""

    ages = _arr(per_t.age_median)
    n = ages.size
    cuts = (0, n // 3, 2 * n // 3, n)
    labels = ("early", "middle", "late")
    return {
        label: float(np.median(ages[cuts[i] : cuts[i + 1]]))
        for i, label in enumerate(labels)
        if cuts[i + 1] > cuts[i]
    }


def distance_contrast(per_t: PerTDiagnostics) -> dict[str, float]:
    """How tight is the k-ball versus a typical library member."""

    d1 = _arr(per_t.d_rank1)
    dk = _arr(per_t.d_rank_k)
    lib = _arr(per_t.d_lib_median)
    by_rank = _arr(per_t.mean_distance_by_rank)
    return {
        "mean_rank1": float(np.mean(d1)),
        "mean_rank_k": float(np.mean(dk)),
        "mean_library_median": float(np.mean(lib)),
        "mean_rank_k_over_lib_median": float(np.mean(dk / np.maximum(lib, 1e-15))),
        "mean_rank1_over_lib_median": float(np.mean(d1 / np.maximum(lib, 1e-15))),
        "mean_distance_rank_1": float(by_rank[0]),
        "mean_distance_rank_mid": float(by_rank[len(by_rank) // 2]),
        "mean_distance_rank_k": float(by_rank[-1]),
    }


def summarize(per_t: PerTDiagnostics, geo_means: dict[str, float], b0_means: dict[str, float]) -> dict:
    """Bundle the four E02 diagnostics as JSON-safe observations."""

    d = delta_series(per_t)
    yearly = temporal_by_year(per_t)
    shares = [float(row["share_of_sum_delta_raw"]) for row in yearly]
    top = sorted(yearly, key=lambda row: float(row["share_of_sum_delta_raw"]), reverse=True)[:5]
    return {
        "relative_reduction_vs_b0": relative_reductions(geo_means, b0_means),
        "temporal": {
            "mean_delta": {
                "raw": float(np.mean(d["raw"])),
                "vol": float(np.mean(d["vol"])),
                "shape": float(np.mean(d["shape"])),
            },
            "by_year": yearly,
            "top_years_by_share_of_sum_delta_raw": top,
            "n_years": len(yearly),
            "frac_years_mean_raw_positive": float(
                np.mean([float(row["mean_delta_raw"]) > 0.0 for row in yearly])
            ),
            "max_year_share_of_sum_delta_raw": max(shares) if shares else float("nan"),
        },
        "neighbor_age": {
            "pooled_quantiles_session_ranks": per_t.pooled_age_quantiles,
            "share_of_neighbors": per_t.neighbor_age_share,
            "per_t_median_quantiles": _quantiles(_arr(per_t.age_median)),
            "tertile_median_of_median_age": tertile_age_medians(per_t),
        },
        "neighborhood_structure": {
            **distance_contrast(per_t),
            "mean_distance_by_rank": list(per_t.mean_distance_by_rank),
        },
        "raw_vol_shape": descriptive_raw_association(per_t),
        "note": (
            "Exploratory description of an unqualified run. Not SCI-PASS, "
            "not SCI-FAIL, not a reason to retune W/k/h/L2/B0."
        ),
    }
