"""E04 — descriptive anatomy of ``D_t``. No threshold search, no retuning.

``D_t = H^{rv}(t) - H^{L2}(t)`` (positive ⇒ L2 more homogeneous than the
past-vol control). Blocks and tertile cuts are **prefixed**, not optimized.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date

import numpy as np

from quant.i01.mechanism import PairedHomogeneity

# Prefixed before inspecting D_t. Do not search a cutoff that maximises D.
CHRONO_LABELS = ("early", "middle", "late")
CALENDAR_BLOCKS: tuple[tuple[int, int, str], ...] = (
    (1994, 1999, "1994-1999"),
    (2000, 2009, "2000-2009"),
    (2010, 2019, "2010-2019"),
    (2020, 2026, "2020-2026"),
)
STATE_LABELS = ("low", "mid", "high")
TOP_FRACTIONS = (0.01, 0.05)


def d_series(paired: PairedHomogeneity) -> dict[str, np.ndarray]:
    """Control minus L2 on each metric."""

    return {
        "vol": paired.h_vol_ctrl - paired.h_vol_geo,
        "raw": paired.h_raw_ctrl - paired.h_raw_geo,
    }


def _skewness(sample: np.ndarray) -> float:
    if sample.size < 3:
        return float("nan")
    centered = sample - float(np.mean(sample))
    scale = float(np.std(centered, ddof=0))
    if scale == 0.0:
        return float("nan")
    return float(np.mean(centered**3) / scale**3)


def distribution(sample: np.ndarray) -> dict[str, float]:
    """Mean, median, tails, skew — why a minority of wins can still lift the mean."""

    qs = (0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99)
    names = ("q01", "q05", "q10", "q25", "median", "q75", "q90", "q95", "q99")
    out = {name: float(np.quantile(sample, q)) for name, q in zip(names, qs, strict=True)}
    out["mean"] = float(np.mean(sample))
    out["min"] = float(np.min(sample))
    out["max"] = float(np.max(sample))
    out["skewness"] = _skewness(sample)
    out["frac_positive"] = float(np.mean(sample > 0.0))
    out["mean_minus_median"] = out["mean"] - out["median"]
    return out


def top_share_of_sum(sample: np.ndarray, fraction: float) -> float:
    """Share of ``sum(D)`` coming from the largest ``fraction`` of dates."""

    total = float(np.sum(sample))
    if total == 0.0:
        return float("nan")
    n = max(1, int(round(fraction * sample.size)))
    order = np.argsort(sample)[::-1]
    return float(np.sum(sample[order[:n]]) / total)


def concentration(sample: np.ndarray) -> dict[str, float]:
    out: dict[str, float] = {}
    for fraction in TOP_FRACTIONS:
        key = f"top_{int(fraction * 100):02d}pct_share_of_sum"
        out[key] = top_share_of_sum(sample, fraction)
    return out


def yearly_d(sessions: tuple[date, ...], sample: np.ndarray) -> list[dict[str, float | int]]:
    buckets: dict[int, list[int]] = defaultdict(list)
    for i, session in enumerate(sessions):
        buckets[session.year].append(i)
    total = float(np.sum(sample))
    rows: list[dict[str, float | int]] = []
    for year in sorted(buckets):
        idx = np.asarray(buckets[year], dtype=np.intp)
        chunk = sample[idx]
        rows.append(
            {
                "year": year,
                "n": int(idx.size),
                "mean_d": float(np.mean(chunk)),
                "median_d": float(np.median(chunk)),
                "frac_positive": float(np.mean(chunk > 0.0)),
                "share_of_sum": (
                    float("nan") if total == 0.0 else float(np.sum(chunk) / total)
                ),
            }
        )
    return rows


def _block_stats(sample: np.ndarray, idx: np.ndarray) -> dict[str, float | int]:
    chunk = sample[idx]
    return {
        "n": int(idx.size),
        "mean_d": float(np.mean(chunk)),
        "median_d": float(np.median(chunk)),
        "frac_positive": float(np.mean(chunk > 0.0)),
    }


def chrono_tertiles(sample: np.ndarray) -> dict[str, dict[str, float | int]]:
    """Equal-count chronological thirds of ``T_eval`` — prefixed, not optimized."""

    n = sample.size
    cuts = (0, n // 3, 2 * n // 3, n)
    return {
        label: _block_stats(sample, np.arange(cuts[i], cuts[i + 1], dtype=np.intp))
        for i, label in enumerate(CHRONO_LABELS)
        if cuts[i + 1] > cuts[i]
    }


def calendar_blocks(
    sessions: tuple[date, ...], sample: np.ndarray
) -> list[dict[str, float | int | str]]:
    """Prefixed calendar decades. Years outside the table are omitted, not reassigned."""

    rows: list[dict[str, float | int | str]] = []
    years = np.asarray([session.year for session in sessions], dtype=np.intp)
    for start, end, label in CALENDAR_BLOCKS:
        idx = np.nonzero((years >= start) & (years <= end))[0]
        if idx.size == 0:
            continue
        rows.append({"block": label, **_block_stats(sample, idx)})
    return rows


def equal_count_tertiles(values: np.ndarray) -> np.ndarray:
    """0/1/2 labels by rank thirds. Ties follow rank order — not a searched cutoff."""

    n = values.size
    order = np.argsort(values, kind="mergesort")
    labels = np.empty(n, dtype=np.intp)
    cuts = (0, n // 3, 2 * n // 3, n)
    for i in range(3):
        labels[order[cuts[i] : cuts[i + 1]]] = i
    return labels


def state_tertiles(
    values: np.ndarray, sample: np.ndarray
) -> dict[str, dict[str, float | int]]:
    labels = equal_count_tertiles(values)
    return {
        name: _block_stats(sample, np.nonzero(labels == i)[0])
        for i, name in enumerate(STATE_LABELS)
    }


def summarize_anatomy(paired: PairedHomogeneity) -> dict:
    """Four prefixed views. No SCI verdict, no maximised threshold."""

    deltas = d_series(paired)
    bundle: dict = {
        "note": (
            "Exploratory anatomy of D_t = H_ctrl - H_L2. Prefixed blocks only. "
            "Not a SCI gate, not a reason to retune W/k/h/L2/B0, not a regime classifier."
        ),
        "n_eval": int(paired.rv_w.size),
    }
    for key, sample in deltas.items():
        yearly = yearly_d(paired.sessions, sample)
        shares = [float(row["share_of_sum"]) for row in yearly]
        bundle[key] = {
            "distribution": distribution(sample),
            "concentration": {
                **concentration(sample),
                "max_year_share_of_sum": max(shares) if shares else float("nan"),
                "top_years_by_share": sorted(
                    yearly, key=lambda row: float(row["share_of_sum"]), reverse=True
                )[:5],
            },
            "yearly": yearly,
            "stability": {
                "chrono_tertiles": chrono_tertiles(sample),
                "calendar_blocks": calendar_blocks(paired.sessions, sample),
            },
            "state_tertiles_descriptive": {
                "rv_w": state_tertiles(paired.rv_w, sample),
                "x_norm": state_tertiles(paired.x_norm, sample),
                "window_sum": state_tertiles(paired.window_sum, sample),
            },
        }
    return bundle
