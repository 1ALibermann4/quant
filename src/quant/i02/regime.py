"""Volatility-regime instability ``Z_t^{(m)}`` (prereg §0 / Gate 3).

    L_t = log(RV_t)
    ΔL_u = L_u - L_{u-1}
    Z_t^{(m)} = Std_pop(ΔL_{t-m+2}, …, ΔL_t)

Uses ``m`` L-levels and ``m-1`` increments. Population std (ddof=0).
``Z`` must never filter ``A_t`` or neighbor selection.
"""

from __future__ import annotations

import numpy as np

from quant.i02.features import first_valid_rv_index, log_rv
from quant.i02.params import I02Params
from quant.i02.types import SkipReason


def std_pop(x: np.ndarray) -> float:
    """Population standard deviation (denominator ``n``, ddof=0)."""

    x = np.asarray(x, dtype=np.float64).reshape(-1)
    if x.size == 0:
        raise ValueError("Std_pop on empty array")
    return float(np.std(x, ddof=0))


def first_valid_z_index(m: int, params: I02Params) -> int:
    """Earliest ``t`` with ``m`` constructible positive-RV L-levels ending at ``t``.

    Needs L at ``t-m+1, …, t`` ⇒ first RV index ``t-m+1 >= first_valid_rv``.
    """

    return first_valid_rv_index(params) + (m - 1)


def z_at(
    returns: np.ndarray, t: int, m: int, params: I02Params
) -> tuple[float | None, SkipReason | None]:
    """Compute ``Z_t^{(m)}`` or a skip reason.

    Indexing check: levels ``L_{t-m+1},…,L_t`` (``m`` values);
    increments ``ΔL_{t-m+2},…,ΔL_t`` (``m-1`` values).
    """

    if m < 2:
        raise ValueError("m must be >= 2 for at least one ΔL")
    first_l = t - m + 1
    if first_l < first_valid_rv_index(params) or t >= len(returns):
        return None, SkipReason.INSUFFICIENT_Z_HISTORY
    levels: list[float] = []
    for u in range(first_l, t + 1):
        try:
            levels.append(log_rv(returns, u, params))
        except ValueError:
            return None, SkipReason.RV_ZERO
    if len(levels) != m:
        return None, SkipReason.INSUFFICIENT_Z_HISTORY
    deltas = np.diff(np.asarray(levels, dtype=np.float64))
    if deltas.shape[0] != m - 1:
        return None, SkipReason.INSUFFICIENT_Z_HISTORY
    return std_pop(deltas), None


def z_vector(
    returns: np.ndarray, t: int, params: I02Params
) -> tuple[dict[int, float | None], list[SkipReason]]:
    """Canonical ``Z_t = (Z^{(3)}, Z^{(12)}, Z^{(21)})`` with per-scale skips."""

    out: dict[int, float | None] = {}
    reasons: list[SkipReason] = []
    for m in params.M_Z:
        val, reason = z_at(returns, t, m, params)
        out[m] = val
        if reason is not None:
            reasons.append(reason)
    return out, reasons
