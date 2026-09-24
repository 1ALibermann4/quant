"""State vectors ``X_t ∈ R^W``."""

from __future__ import annotations

import numpy as np

from quant.i01.params import I01Params
from quant.i01.standardization import standardize_window


def first_valid_state_index(params: I01Params) -> int:
    """Smallest session rank ``t`` at which ``X_t`` is defined (``t >= M``)."""

    return params.M


def state_vector(returns: np.ndarray, t: int, params: I01Params) -> np.ndarray:
    """Build ``X_t`` from ``O_{<= t}`` only."""

    return standardize_window(returns, t, params)


def all_state_vectors(returns: np.ndarray, params: I01Params) -> np.ndarray:
    """Stack ``X_t`` for every valid ``t``; rows before the first valid state are NaN."""

    n = returns.shape[0]
    X = np.full((n, params.W), np.nan, dtype=np.float64)
    start = first_valid_state_index(params)
    for t in range(start, n):
        X[t] = state_vector(returns, t, params)
    return X
