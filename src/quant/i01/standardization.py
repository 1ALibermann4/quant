"""Causal μ̂/σ̂ standardization inclusive of ``r_t`` (hypothesis §4.2)."""

from __future__ import annotations

import numpy as np

from quant.i01.params import I01Params


def causal_mu_sigma(returns: np.ndarray, t: int, params: I01Params) -> tuple[float, float]:
    """Sample mean and sample std of ``r_{t-M+1}, …, r_t`` (σ uses ``ddof=1``).

    Raises:
        ValueError: If ``t`` does not have a complete causal window.
    """

    start = t - params.M + 1
    if start < 1 or t >= len(returns):
        raise ValueError(f"standardization window at t={t} is incomplete")
    window = returns[start : t + 1]
    if window.shape[0] != params.M or np.isnan(window).any():
        raise ValueError(f"standardization window at t={t} contains NaN or wrong length")
    mu = float(np.mean(window))
    sigma = float(np.std(window, ddof=1))
    return mu, sigma


def standardize_window(
    returns: np.ndarray, t: int, params: I01Params
) -> np.ndarray:
    """Return ``(r̃_{t-W+1}, …, r̃_t)`` using μ̂_t, σ̂_t from ``[t-M+1, t]``.

    No return after ``t`` is read.
    """

    mu, sigma = causal_mu_sigma(returns, t, params)
    x_start = t - params.W + 1
    window = returns[x_start : t + 1]
    return (window - mu) / (sigma + params.epsilon)
