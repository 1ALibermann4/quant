"""Independent numerical oracles for I03 L2 (derived from prereg text only).

Production code must NOT import this module for expected values in unit tests
that compare against itself — L2 tests import these oracles.
"""

from __future__ import annotations

import numpy as np


def oracle_causal_mu_sigma(returns: np.ndarray, t: int, M: int = 252) -> tuple[float, float] | None:
    """Prereg §3 sample mean/stdev on ``[t-M+1, t]``; index 0 unused."""

    start = t - M + 1
    if start < 1 or t >= len(returns):
        return None
    w = np.asarray(returns[start : t + 1], dtype=np.float64)
    if w.shape[0] != M or np.isnan(w).any():
        return None
    mu = float(np.mean(w))
    sigma = float(np.std(w, ddof=1))
    return mu, sigma


def oracle_X(returns: np.ndarray, t: int, M: int = 252, W_X: int = 20) -> np.ndarray | None:
    """Independent G0 ``X_t`` from prereg §3 (no ε; σ=0 → None)."""

    ms = oracle_causal_mu_sigma(returns, t, M=M)
    if ms is None:
        return None
    mu, sigma = ms
    if sigma == 0.0:
        return None
    x_start = t - W_X + 1
    if x_start < 1:
        return None
    w = np.asarray(returns[x_start : t + 1], dtype=np.float64)
    if w.shape[0] != W_X or np.isnan(w).any():
        return None
    return (w - mu) / sigma


def oracle_n4_sigma(returns: np.ndarray, t: int, W_sigma: int = 20) -> float | None:
    """Prereg §8.1 sample stdev, denom W-1, inclusive of r_t."""

    start = t - W_sigma + 1
    if start < 1 or t >= len(returns):
        return None
    w = np.asarray(returns[start : t + 1], dtype=np.float64)
    if w.shape[0] != W_sigma or np.isnan(w).any():
        return None
    return float(np.std(w, ddof=1))


def oracle_kth_distance(
    query: np.ndarray, pool_states: dict[int, np.ndarray], k: int
) -> float:
    """k-th distance with ties (dist↑, s↑). ``pool_states`` maps s → vector."""

    pairs = []
    for s, vec in pool_states.items():
        d = float(np.linalg.norm(query - vec))
        pairs.append((d, int(s)))
    pairs.sort(key=lambda x: (x[0], x[1]))
    return pairs[k - 1][0]


def oracle_left_tail_p(observed: float, surrogates: list[float] | np.ndarray) -> float:
    """``p = (1 + #{Θ* <= Θ}) / (B+1)``."""

    s = np.asarray(surrogates, dtype=np.float64)
    B = s.size
    return (1 + int(np.sum(s <= observed))) / (B + 1)


def oracle_max_count_survive_alpha(B: int, alpha: float) -> int:
    """Largest ``c = #{Θ* <= Θ}`` with ``(1+c)/(B+1) <= alpha``."""

    # (1+c)/(B+1) <= alpha  ⇒  c <= alpha*(B+1) - 1
    return int(np.floor(alpha * (B + 1) - 1))


def oracle_n3_invalid(n_nonconverged: int, B: int, frac: float = 0.05) -> bool:
    """True iff battery INVALID under prereg ``>#frac`` nonconverged."""

    return (n_nonconverged / B) > frac


def oracle_decide_verdict(
    V: bool, E: bool, C4: bool, C3: bool, F4: bool
) -> tuple[str, str | None]:
    """Independent encoding of prereg §14 → (label, nd_code)."""

    if not V:
        return "INCONCLUSIVE", None
    if not E:
        return "INCONCLUSIVE", None
    if C4 and C3:
        return "PASS", "ND-1"
    if F4:
        return "FAIL", "ND-4"
    if C4 and not C3:
        return "INCONCLUSIVE", "ND-2"
    if C3 and not C4:
        return "INCONCLUSIVE", "ND-3"
    return "INCONCLUSIVE", "ND-5"


def oracle_blocks(T: int, P: int = 3) -> list[tuple[int, int]]:
    """Return list of (start, end) inclusive per prereg §5."""

    L = T // P
    R = T % P
    return [
        (0, L - 1),
        (L, 2 * L - 1),
        (2 * L, 3 * L + R - 1),
    ]
