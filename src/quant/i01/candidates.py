"""Admissible library ``L_t`` (DEC-02) and evaluation set."""

from __future__ import annotations

import numpy as np

from quant.i01.params import I01Params


def first_evaluation_index(params: I01Params) -> int:
    """Smallest ``t`` with ``|L_t| >= L_min`` and ``X_t`` valid.

    ``|L_t| = t - M - tau`` when the embargo binds harder than ``s+h <= t``.
    """

    return params.M + params.tau + params.L_min


def last_evaluation_index(n_sessions: int, params: I01Params) -> int:
    """Largest ``t`` with complete ``Y_t``."""

    return n_sessions - 1 - params.h


def evaluation_indices(n_sessions: int, params: I01Params) -> np.ndarray:
    """Session ranks in ``T_eval``."""

    first = first_evaluation_index(params)
    last = last_evaluation_index(n_sessions, params)
    if last < first:
        return np.empty(0, dtype=np.intp)
    return np.arange(first, last + 1, dtype=np.intp)


def admissible_candidates(t: int, n_sessions: int, params: I01Params) -> np.ndarray:
    """Return ranks ``s`` in ``L_t``.

    Invariants (all enforced):

    * ``s < t``
    * ``|s - t| > tau`` (embargo)
    * ``s + h <= t``  (``candidate.future_end <= query.information_cutoff``)
    * ``X_s`` valid (``s >= M``)
    * ``Y_s`` complete (``s + h <= n_sessions - 1``)
    """

    if t < 0 or t >= n_sessions:
        raise ValueError(f"query rank t={t} out of range")
    s = np.arange(params.M, t, dtype=np.intp)
    future_end = s + params.h
    mask = (
        (s < t)
        & ((t - s) > params.tau)
        & (future_end <= t)
        & (future_end <= n_sessions - 1)
    )
    return s[mask]
