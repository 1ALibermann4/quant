"""Volatility features for S1/S2/S3 and regime state (RMS RV, not I01 std).

Critical: I01 ``rv_w`` is sample std of returns. I02 ``RV_t`` is

    RV_t = sqrt( (1/W) * sum_{j=0..W-1} r_{t-j}^2 )

No epsilon, clipping, or smoothing.
"""

from __future__ import annotations

import numpy as np

from quant.i02.params import I02Params


def first_valid_rv_index(params: I02Params) -> int:
    """Smallest ``t`` with a complete RV window of valid returns.

    Log-returns use ``r[0] = nan`` (I01 convention); the first valid
    return is at index 1, so the first complete window of length ``W``
    ends at ``t = W``.
    """

    return params.W_RV


def realized_rms_volatility(
    returns: np.ndarray, t: int, w: int
) -> float:
    """Compute RMS volatility ending at ``t`` over ``w`` sessions.

    Window: ``r_{t-w+1}, …, r_t``. Raises if the window is incomplete
    or contains NaN. Returns 0.0 if all squared returns are zero (no ε).
    """

    start = t - w + 1
    if start < 1 or t >= len(returns):
        raise ValueError(f"RV window at t={t} incomplete")
    window = np.asarray(returns[start : t + 1], dtype=np.float64)
    if window.shape[0] != w or np.isnan(window).any():
        raise ValueError(f"RV window at t={t} has NaN or wrong length")
    return float(np.sqrt(np.mean(window * window)))


def mean_abs_amplitude(returns: np.ndarray, t: int, w: int) -> float:
    """``MA_t = (1/w) sum |r|`` on the same window as RV."""

    start = t - w + 1
    if start < 1 or t >= len(returns):
        raise ValueError(f"MA window at t={t} incomplete")
    window = np.asarray(returns[start : t + 1], dtype=np.float64)
    if window.shape[0] != w or np.isnan(window).any():
        raise ValueError(f"MA window at t={t} has NaN or wrong length")
    return float(np.mean(np.abs(window)))


def rv_early_late(
    returns: np.ndarray, t: int, w: int
) -> tuple[float, float]:
    """Early/late half-window RMS for ``W`` even (I02: 10+10).

    Ordered window ``r_{t-w+1},…,r_t``:
    early = first half (older); late = second half (includes ``r_t``).
    """

    if w % 2 != 0:
        raise ValueError("early/late split requires even W")
    half = w // 2
    start = t - w + 1
    if start < 1 or t >= len(returns):
        raise ValueError(f"early/late window at t={t} incomplete")
    window = np.asarray(returns[start : t + 1], dtype=np.float64)
    if window.shape[0] != w or np.isnan(window).any():
        raise ValueError(f"early/late window at t={t} invalid")
    early = window[:half]
    late = window[half:]
    rv_e = float(np.sqrt(np.mean(early * early)))
    rv_l = float(np.sqrt(np.mean(late * late)))
    return rv_e, rv_l


def dynamics_D(returns: np.ndarray, t: int, params: I02Params) -> float:
    """``D_t = log(RV_late / RV_early)``.

    Structurally undefined if ``RV_early == 0`` or ``RV_late == 0``
    (no epsilon). Raises ``ValueError`` in that case.
    """

    rv_e, rv_l = rv_early_late(returns, t, params.W_RV)
    if rv_e == 0.0 or rv_l == 0.0:
        raise ValueError("D undefined: RV_early or RV_late is zero")
    return float(np.log(rv_l / rv_e))


def shape_Q(returns: np.ndarray, t: int, params: I02Params) -> float:
    """``Q_t = MA_t / RV_t``. Undefined if ``RV_t == 0`` (no epsilon)."""

    rv = realized_rms_volatility(returns, t, params.W_RV)
    if rv == 0.0:
        raise ValueError("Q undefined: RV_t is zero")
    ma = mean_abs_amplitude(returns, t, params.W_RV)
    return float(ma / rv)


def log_rv(returns: np.ndarray, t: int, params: I02Params) -> float:
    """``L_t = log(RV_t)``. Undefined if ``RV_t == 0``."""

    rv = realized_rms_volatility(returns, t, params.W_RV)
    if rv == 0.0:
        raise ValueError("L undefined: RV_t is zero")
    return float(np.log(rv))


def all_rv(returns: np.ndarray, params: I02Params) -> np.ndarray:
    """Series of ``RV_t``; NaN where incomplete."""

    n = returns.shape[0]
    out = np.full(n, np.nan, dtype=np.float64)
    for t in range(first_valid_rv_index(params), n):
        out[t] = realized_rms_volatility(returns, t, params.W_RV)
    return out
