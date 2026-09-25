"""Common admissible historical pool ``A_t`` (prereg §0 / draft §14J.2).

All of ``X, S1, S2, S3`` must select neighbors from the **same** ``A_t``.
``Z_t`` must not filter this pool.

I02 does **not** inherit I01's embargo ``tau`` or ``L_min`` — those are
absent from the I02 frozen contract. Only:

* ``s < t``
* ``s + h <= t`` (hard availability of ``V_{s,h}``)
* representations constructible at ``s`` for every ``R``
* ``V_{s,h}`` complete in-sample (``s + h <= n - 1``)

If ``|A_t| < k``, the query is skipped (no adaptive ``k``).
"""

from __future__ import annotations

import numpy as np

from quant.i02.features import first_valid_rv_index, realized_rms_volatility
from quant.i02.params import I02Params
from quant.i02.states_x import first_valid_x_index, x_is_defined


def first_constructible_index(params: I02Params) -> int:
    """Earliest session where X and RV-based features are constructible."""

    return max(first_valid_x_index(params), first_valid_rv_index(params))


def last_query_index(n_sessions: int, params: I02Params) -> int:
    """Largest ``t`` with complete ``V_{t,h}``."""

    return n_sessions - 1 - params.h


def representation_constructible(
    returns: np.ndarray, s: int, params: I02Params
) -> bool:
    """Whether ``X_s`` and S-features at ``s`` are constructible without ε hacks.

    Requires complete windows, ``σ̂_s > 0`` for ``X``, and ``RV_s > 0``,
    ``RV_early > 0``, ``RV_late > 0`` so that ``L``, ``D``, ``Q`` are defined.
    """

    if s < first_constructible_index(params):
        return False
    if not x_is_defined(returns, s, params):
        return False
    try:
        rv = realized_rms_volatility(returns, s, params.W_RV)
    except ValueError:
        return False
    if rv == 0.0:
        return False
    half = params.W_RV // 2
    start = s - params.W_RV + 1
    window = returns[start : s + 1]
    early = window[:half]
    late = window[half:]
    if float(np.sqrt(np.mean(early * early))) == 0.0:
        return False
    if float(np.sqrt(np.mean(late * late))) == 0.0:
        return False
    return True


def admissible_pool(
    returns: np.ndarray, t: int, params: I02Params
) -> np.ndarray:
    """Return ranks ``s ∈ A_t`` (sorted ascending).

    Causality: no ``s >= t``; no future beyond ``t`` enters neighbor
    targets (``s + h <= t``).
    """

    n = len(returns)
    if t < 0 or t >= n:
        raise ValueError(f"query t={t} out of range")
    start = first_constructible_index(params)
    if start >= t:
        return np.empty(0, dtype=np.intp)
    candidates = np.arange(start, t, dtype=np.intp)
    keep: list[int] = []
    for s in candidates:
        if int(s) + params.h > t:
            continue
        if int(s) + params.h > n - 1:
            continue
        if not representation_constructible(returns, int(s), params):
            continue
        keep.append(int(s))
    return np.asarray(keep, dtype=np.intp)


def query_schedule(n_sessions: int, params: I02Params) -> np.ndarray:
    """Stride-1 evaluation ranks with complete ``V_{t,h}`` and buildable state."""

    first = first_constructible_index(params)
    last = last_query_index(n_sessions, params)
    if last < first:
        return np.empty(0, dtype=np.intp)
    return np.arange(first, last + 1, params.stride, dtype=np.intp)
