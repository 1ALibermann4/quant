"""Empirical CRPS for equiponderated forecast atoms (prereg §0)."""

from __future__ import annotations

import numpy as np


def crps_empirical(atoms: np.ndarray, y: float) -> float:
    """Ensemble / energy form of CRPS for ``F = (1/k) sum δ_{V_i}``.

    .. math::

        \\mathrm{CRPS}(F,y)
        = \\frac1k \\sum_i |V_i - y|
        - \\frac1{2k^2} \\sum_i \\sum_j |V_i - V_j|

    Duplicate atoms are preserved (multiplicity). No KDE / smoothing.
    """

    v = np.asarray(atoms, dtype=np.float64).reshape(-1)
    k = v.shape[0]
    if k < 1:
        raise ValueError("CRPS requires at least one atom")
    y = float(y)
    term1 = float(np.mean(np.abs(v - y)))
    # Pairwise absolute differences
    dif = np.abs(v[:, None] - v[None, :])
    term2 = float(np.sum(dif)) / (2.0 * k * k)
    return term1 - term2
