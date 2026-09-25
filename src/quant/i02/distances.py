"""Distances for neighbor selection (I02-PREREG-v0.3).

S1: ``|ΔL|``.
S2: primary ``d_2 = sqrt((ΔL)^2 + (ΔD)^2)``.
S3-A (ACCEPTED): co-equal product metrics

    d_S3,Q   = sqrt((ΔL)^2 + (ΔQ)^2)
    d_S3,phi = sqrt((ΔL)^2 + (Δφ)^2),  φ = arccos(Q)

No primary between S3-Q and S3-phi. No λ / z-score / whitening.
"""

from __future__ import annotations

import numpy as np

from quant.i01.neighbors import pairwise_l2
from quant.i02.features import dynamics_D, log_rv, shape_Q


def distance_s1_level(L_a: float, L_b: float) -> float:
    """``|L_a - L_b|``."""

    return abs(L_a - L_b)


def distance_s2_d2(L_a: float, D_a: float, L_b: float, D_b: float) -> float:
    """Primary S2 metric ``d_2`` (§9.16.3)."""

    dL = L_a - L_b
    dD = D_a - D_b
    return float(np.sqrt(dL * dL + dD * dD))


def phi_from_q(q: float) -> float:
    """``φ = arccos(Q)`` with ``Q ∈ (0, 1]``."""

    q = float(q)
    if q <= 0.0 or q > 1.0 + 1e-15:
        raise ValueError(f"Q out of domain for arccos: {q}")
    # numerical clamp into [-1, 1] for floating noise at Q≈1
    q_c = min(1.0, max(0.0, q))
    return float(np.arccos(q_c))


def distance_s3_q(L_a: float, Q_a: float, L_b: float, Q_b: float) -> float:
    """S3-A product metric on ``(L, Q)``."""

    dL = L_a - L_b
    dQ = Q_a - Q_b
    return float(np.sqrt(dL * dL + dQ * dQ))


def distance_s3_phi(L_a: float, Q_a: float, L_b: float, Q_b: float) -> float:
    """S3-A product metric on ``(L, φ)`` with ``φ = arccos(Q)``."""

    dL = L_a - L_b
    dphi = phi_from_q(Q_a) - phi_from_q(Q_b)
    return float(np.sqrt(dL * dL + dphi * dphi))


def pairwise_s1(L: np.ndarray, library: np.ndarray, query_idx: int) -> np.ndarray:
    lq = float(L[query_idx])
    return np.asarray(
        [distance_s1_level(lq, float(L[s])) for s in library],
        dtype=np.float64,
    )


def pairwise_s2(
    L: np.ndarray, D: np.ndarray, library: np.ndarray, query_idx: int
) -> np.ndarray:
    lq, dq = float(L[query_idx]), float(D[query_idx])
    return np.asarray(
        [
            distance_s2_d2(lq, dq, float(L[s]), float(D[s]))
            for s in library
        ],
        dtype=np.float64,
    )


def pairwise_s3_q(
    L: np.ndarray, Q: np.ndarray, library: np.ndarray, query_idx: int
) -> np.ndarray:
    lq, qq = float(L[query_idx]), float(Q[query_idx])
    return np.asarray(
        [
            distance_s3_q(lq, qq, float(L[s]), float(Q[s]))
            for s in library
        ],
        dtype=np.float64,
    )


def pairwise_s3_phi(
    L: np.ndarray, Q: np.ndarray, library: np.ndarray, query_idx: int
) -> np.ndarray:
    lq, qq = float(L[query_idx]), float(Q[query_idx])
    return np.asarray(
        [
            distance_s3_phi(lq, qq, float(L[s]), float(Q[s]))
            for s in library
        ],
        dtype=np.float64,
    )


def pairwise_x(
    states: np.ndarray, library: np.ndarray, query_idx: int
) -> np.ndarray:
    return pairwise_l2(states[query_idx].reshape(1, -1), states[library])[0]


def build_L_D_Q_series(
    returns: np.ndarray, params
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Precompute ``L_t``, ``D_t``, ``Q_t``; NaN where undefined."""

    from quant.i02.features import first_valid_rv_index
    from quant.i02.params import I02Params

    assert isinstance(params, I02Params)
    n = len(returns)
    L = np.full(n, np.nan, dtype=np.float64)
    D = np.full(n, np.nan, dtype=np.float64)
    Q = np.full(n, np.nan, dtype=np.float64)
    for t in range(first_valid_rv_index(params), n):
        try:
            L[t] = log_rv(returns, t, params)
            D[t] = dynamics_D(returns, t, params)
            Q[t] = shape_Q(returns, t, params)
        except ValueError:
            pass
    return L, D, Q


def build_L_D_series(
    returns: np.ndarray, params
) -> tuple[np.ndarray, np.ndarray]:
    """Backward-compatible ``(L, D)`` only."""

    L, D, _Q = build_L_D_Q_series(returns, params)
    return L, D
