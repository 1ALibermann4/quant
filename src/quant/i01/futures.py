"""Future vectors ``Y_t = (r_{t+1}, …, r_{t+h})`` (DEC-04)."""

from __future__ import annotations

import numpy as np

from quant.i01.params import I01Params


def future_vector(returns: np.ndarray, t: int, params: I01Params) -> np.ndarray:
    """Return the length-``h`` future starting strictly at ``t+1``.

    Raises:
        ValueError: If ``Y_t`` is incomplete.
    """

    end = t + params.h
    if t < 0 or end >= len(returns):
        raise ValueError(f"Y_t incomplete at t={t}")
    y = returns[t + 1 : end + 1]
    if y.shape[0] != params.h or np.isnan(y).any():
        raise ValueError(f"Y_t contains NaN or wrong length at t={t}")
    return y.copy()


def all_future_vectors(returns: np.ndarray, params: I01Params) -> np.ndarray:
    """Stack ``Y_t``; rows without a complete future are NaN."""

    n = returns.shape[0]
    Y = np.full((n, params.h), np.nan, dtype=np.float64)
    last = n - 1 - params.h
    for t in range(0, last + 1):
        if t >= 1:
            Y[t] = future_vector(returns, t, params)
    return Y
