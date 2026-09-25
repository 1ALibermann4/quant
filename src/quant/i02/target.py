"""Future realized RMS volatility target ``V_{t,h}`` (prereg §0)."""

from __future__ import annotations

import numpy as np

from quant.i02.params import I02Params


def future_realized_rms(
    returns: np.ndarray, t: int, params: I02Params
) -> float:
    """``V_{t,h} = sqrt( (1/h) * sum_{j=1..h} r_{t+j}^2 )``.

    Uses only returns strictly after ``t``. Raises if the future
    window is incomplete or contains NaN.
    """

    h = params.h
    end = t + h
    if t < 0 or end >= len(returns):
        raise ValueError(f"V future window at t={t} incomplete")
    fut = np.asarray(returns[t + 1 : end + 1], dtype=np.float64)
    if fut.shape[0] != h or np.isnan(fut).any():
        raise ValueError(f"V future window at t={t} invalid")
    return float(np.sqrt(np.mean(fut * fut)))


def all_future_realized_rms(
    returns: np.ndarray, params: I02Params
) -> np.ndarray:
    """``V_{t,h}`` for all ``t`` with complete future; else NaN."""

    n = returns.shape[0]
    out = np.full(n, np.nan, dtype=np.float64)
    last = n - 1 - params.h
    for t in range(0, last + 1):
        try:
            out[t] = future_realized_rms(returns, t, params)
        except ValueError:
            out[t] = np.nan
    return out
