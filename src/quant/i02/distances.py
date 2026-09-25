"""Distances for neighbor selection (draft §9.14 / §9.16).

S1: ``|ΔL|`` (multiplicative level).
S2: primary ``d_2 = sqrt((ΔL)^2 + (ΔD)^2)`` (§9.16.3).
S3: **not implemented** — see :data:`S3_KNN_AGGREGATION_GAP`.
X: L2 on standardized state vectors (I01 geometric form).
"""

from __future__ import annotations

import numpy as np

from quant.i01.neighbors import pairwise_l2
from quant.i02.contract_gaps import (
    ImplementationContractGap,
    S3_KNN_AGGREGATION_GAP,
)
from quant.i02.features import dynamics_D, log_rv


def distance_s1_level(L_a: float, L_b: float) -> float:
    """``|L_a - L_b|``."""

    return abs(L_a - L_b)


def distance_s2_d2(L_a: float, D_a: float, L_b: float, D_b: float) -> float:
    """Primary S2 metric ``d_2`` (§9.16.3)."""

    dL = L_a - L_b
    dD = D_a - D_b
    return float(np.sqrt(dL * dL + dD * dD))


def distance_s3_blocked(*_args, **_kwargs) -> float:
    """S3 kNN distance is a contract gap — do not invent aggregation."""

    raise ImplementationContractGap(S3_KNN_AGGREGATION_GAP)


def pairwise_s1(L: np.ndarray, library: np.ndarray, query_idx: int) -> np.ndarray:
    """Distances from query to each library index under S1."""

    lq = float(L[query_idx])
    return np.asarray(
        [distance_s1_level(lq, float(L[s])) for s in library],
        dtype=np.float64,
    )


def pairwise_s2(
    L: np.ndarray, D: np.ndarray, library: np.ndarray, query_idx: int
) -> np.ndarray:
    """Distances from query to library under primary ``d_2``."""

    lq, dq = float(L[query_idx]), float(D[query_idx])
    return np.asarray(
        [
            distance_s2_d2(lq, dq, float(L[s]), float(D[s]))
            for s in library
        ],
        dtype=np.float64,
    )


def pairwise_x(
    states: np.ndarray, library: np.ndarray, query_idx: int
) -> np.ndarray:
    """L2 distances in ``X``-space."""

    return pairwise_l2(states[query_idx].reshape(1, -1), states[library])[0]


def build_L_D_series(
    returns: np.ndarray, params
) -> tuple[np.ndarray, np.ndarray]:
    """Precompute ``L_t`` and ``D_t``; NaN where undefined."""

    from quant.i02.params import I02Params

    assert isinstance(params, I02Params)
    n = len(returns)
    L = np.full(n, np.nan, dtype=np.float64)
    D = np.full(n, np.nan, dtype=np.float64)
    from quant.i02.features import first_valid_rv_index

    for t in range(first_valid_rv_index(params), n):
        try:
            L[t] = log_rv(returns, t, params)
            D[t] = dynamics_D(returns, t, params)
        except ValueError:
            pass
    return L, D
