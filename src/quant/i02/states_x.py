"""Representation ``X_t`` — I01 causal standardized log-return window.

Reuses I01 standardization mathematics (``M``, σ floor) as the
inherited geometric form of ``X``; see contract note in
:mod:`quant.i02.contract_gaps`.
"""

from __future__ import annotations

import numpy as np

from quant.i01.params import I01Params
from quant.i01.standardization import standardize_window
from quant.i02.params import I02Params


def _as_i01_params(params: I02Params) -> I01Params:
    return I01Params(
        W=params.W_X,
        M=params.M,
        epsilon=params.x_sigma_epsilon,
        h=params.h,
        k=params.k,
    )


def first_valid_x_index(params: I02Params) -> int:
    """Smallest ``t`` at which ``X_t`` is defined (``t >= M``)."""

    return params.M


def state_vector_x(returns: np.ndarray, t: int, params: I02Params) -> np.ndarray:
    """Build ``X_t ∈ R^{W_X}`` from ``O_{<= t}`` only."""

    return standardize_window(returns, t, _as_i01_params(params))


def all_state_vectors_x(returns: np.ndarray, params: I02Params) -> np.ndarray:
    """Stack ``X_t``; rows before first valid index are NaN."""

    n = returns.shape[0]
    X = np.full((n, params.W_X), np.nan, dtype=np.float64)
    start = first_valid_x_index(params)
    for t in range(start, n):
        X[t] = state_vector_x(returns, t, params)
    return X
