"""Finite-surrogate left-tail inference (I03-PREREG-v0.1 §11)."""

from __future__ import annotations

import numpy as np


def left_tail_p(observed: float, surrogates: np.ndarray) -> float:
    """``p = (1 + #{Θ* <= Θ}) / (B+1)`` — lower Θ = stronger recurrence."""

    s = np.asarray(surrogates, dtype=np.float64)
    B = s.size
    if B < 1:
        raise ValueError("need at least one surrogate")
    count = int(np.sum(s <= observed))
    return (1 + count) / (B + 1)


def survives(p_hat: float, alpha: float) -> bool:
    """Survive iff ``p_hat <= alpha`` (equality survives)."""

    return bool(p_hat <= alpha)
