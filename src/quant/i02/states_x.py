"""Representation ``X_t`` — I01 causal form with I02 σ policy (PREREG-v0.3 §13).

Inherited: ``M=252``, ``W_X=20``, inclusive causal μ/σ window.
I02 amendment: **no** ``ε_σ``. If ``σ̂_t = 0``, ``X_t`` is undefined.
If ``σ̂_t > 0``, divide exactly by ``σ̂_t``.
"""

from __future__ import annotations

import numpy as np

from quant.i02.params import I02Params
from quant.i02.types import SkipReason


class XUndefinedError(ValueError):
    """Raised when ``X_t`` cannot be formed under the I02 contract."""

    def __init__(self, message: str, reason: SkipReason) -> None:
        super().__init__(message)
        self.reason = reason


def first_valid_x_index(params: I02Params) -> int:
    """Smallest ``t`` at which an ``X`` window *could* be formed (``t >= M``)."""

    return params.M


def causal_mu_sigma(
    returns: np.ndarray, t: int, params: I02Params
) -> tuple[float, float]:
    """Sample mean and sample std (``ddof=1``) on ``[t-M+1, t]`` inclusive."""

    start = t - params.M + 1
    if start < 1 or t >= len(returns):
        raise XUndefinedError(
            f"standardization window at t={t} incomplete",
            SkipReason.INSUFFICIENT_X_HISTORY,
        )
    window = np.asarray(returns[start : t + 1], dtype=np.float64)
    if window.shape[0] != params.M or np.isnan(window).any():
        raise XUndefinedError(
            f"standardization window at t={t} invalid",
            SkipReason.INSUFFICIENT_X_HISTORY,
        )
    mu = float(np.mean(window))
    sigma = float(np.std(window, ddof=1))
    return mu, sigma


def state_vector_x(returns: np.ndarray, t: int, params: I02Params) -> np.ndarray:
    """Build ``X_t ∈ R^{W_X}`` from ``O_{<= t}`` only.

    Raises:
        XUndefinedError: incomplete history or ``σ̂_t = 0`` (no epsilon).
    """

    mu, sigma = causal_mu_sigma(returns, t, params)
    if sigma == 0.0:
        raise XUndefinedError(
            f"X undefined at t={t}: sigma_hat = 0",
            SkipReason.X_SIGMA_ZERO,
        )
    x_start = t - params.W_X + 1
    window = np.asarray(returns[x_start : t + 1], dtype=np.float64)
    if window.shape[0] != params.W_X or np.isnan(window).any():
        raise XUndefinedError(
            f"X state window at t={t} invalid",
            SkipReason.INSUFFICIENT_X_HISTORY,
        )
    return (window - mu) / sigma


def x_is_defined(returns: np.ndarray, t: int, params: I02Params) -> bool:
    """Whether ``X_t`` is defined (complete window and ``σ̂_t > 0``)."""

    try:
        state_vector_x(returns, t, params)
        return True
    except XUndefinedError:
        return False


def all_state_vectors_x(returns: np.ndarray, params: I02Params) -> np.ndarray:
    """Stack ``X_t``; NaN rows where undefined (including ``σ̂=0``)."""

    n = returns.shape[0]
    X = np.full((n, params.W_X), np.nan, dtype=np.float64)
    start = first_valid_x_index(params)
    for t in range(start, n):
        try:
            X[t] = state_vector_x(returns, t, params)
        except XUndefinedError:
            pass
    return X
