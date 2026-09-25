"""Spearman association grid (prereg §1–§2) — two-sided, non-causal.

Computes the full ``S × m`` matrix without selecting best S/m.
No Pearson alternative.
"""

from __future__ import annotations

import numpy as np


def _rankdata(x: np.ndarray) -> np.ndarray:
    """Average ranks for ties (1..n style)."""

    x = np.asarray(x, dtype=np.float64)
    n = x.shape[0]
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(n, dtype=np.float64)
    sorted_x = x[order]
    i = 0
    while i < n:
        j = i
        while j + 1 < n and sorted_x[j + 1] == sorted_x[i]:
            j += 1
        # average rank (1-based)
        avg = 0.5 * ((i + 1) + (j + 1))
        ranks[order[i : j + 1]] = avg
        i = j + 1
    return ranks


def spearman_rho(x: np.ndarray, y: np.ndarray) -> float:
    """Pearson correlation of average ranks (Spearman ρ).

    Requires finite paired observations; ``n >= 2``.
    """

    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    if x.shape != y.shape:
        raise ValueError("x and y shape mismatch")
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    n = x.shape[0]
    if n < 2:
        return float("nan")
    rx = _rankdata(x)
    ry = _rankdata(y)
    # Constant ranks ⇒ undefined correlation
    if np.allclose(rx, rx[0]) or np.allclose(ry, ry[0]):
        return float("nan")
    c = np.corrcoef(rx, ry)[0, 1]
    return float(c)


def spearman_grid(
    z_by_m: dict[int, np.ndarray],
    r_by_s: dict[str, np.ndarray],
) -> dict[tuple[str, int], float]:
    """Full grid ``ρ̂^(S,m)`` for all provided series (aligned length).

    Does not drop columns to a best cell. Caller must pass only the
    paired valid mask already applied (or NaNs for invalid pairs).
    """

    out: dict[tuple[str, int], float] = {}
    for s_name, r_series in r_by_s.items():
        for m, z_series in z_by_m.items():
            out[(s_name, m)] = spearman_rho(z_series, r_series)
    return out
