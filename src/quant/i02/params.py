"""Frozen I02 scientific parameters (I02-PREREG-v0.3).

Scientific constants are frozen here as the runtime source of truth.
Do not expose them as CLI tuning knobs.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class I02Params:
    """Preregistered I02 constants."""

    W_X: int = 20
    W_RV: int = 20
    h: int = 10
    k: int = 50
    M_Z: tuple[int, ...] = (3, 12, 21)
    stride: int = 1
    b_star: int = 40
    b_sensitivity: tuple[int, ...] = (20, 40, 80)
    bootstrap_B: int = 9999
    bootstrap_seed: int = 42
    alpha: float = 0.05
    M: int = 252  # inherited I01 X form

    def __post_init__(self) -> None:
        if self.W_X < 1 or self.W_RV < 1 or self.h < 1 or self.k < 1:
            raise ValueError("W_X, W_RV, h, k must be >= 1")
        if self.W_X != 20 or self.W_RV != 20:
            raise ValueError("I02 freezes W_X = W_RV = 20")
        if self.h != 10 or self.k != 50 or self.stride != 1:
            raise ValueError("I02 freezes h=10, k=50, stride=1")
        if self.M_Z != (3, 12, 21):
            raise ValueError("I02 freezes M_Z = (3, 12, 21)")
        if self.b_star != 40 or self.b_sensitivity != (20, 40, 80):
            raise ValueError("I02 freezes b*=40 and sensitivity {20,40,80}")
        if self.bootstrap_B != 9999 or self.bootstrap_seed != 42:
            raise ValueError("I02 freezes B=9999 and seed=42")
        if self.alpha != 0.05:
            raise ValueError("I02 freezes alpha=0.05")
        if self.W_X % 2 != 0:
            raise ValueError("W_X must be even for S2 early/late 10+10 split")
        if self.M != 252:
            raise ValueError("I02 freezes M=252 (inherited X form)")
        if self.M < self.W_X:
            raise ValueError("M must be >= W_X")


DEFAULT_PARAMS = I02Params()
