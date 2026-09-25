"""Frozen I02 scientific parameters (preregistration §0).

Scientific constants are frozen here as the runtime source of truth.
Do not expose them as CLI tuning knobs. Do not retune after results
(DR-007 D-4 / I02 change-control class C).

``X`` standardization length ``M`` is the inherited I01 geometric form
(I02-PREREG-v0.2 §13). ``x_sigma_epsilon`` remains in this dataclass
only until the L1 patch removes it; the scientific contract forbids
using ε for I02 ``X`` (degenerate ``σ̂=0`` ⇒ undefined / skip).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class I02Params:
    """Preregistered I02 constants.

    Attributes:
        W_X: Representation window for ``X`` (sessions).
        W_RV: Window for realized RMS volatility ``RV_t``.
        h: Forecast horizon (sessions).
        k: Neighbor count (common across representations).
        M_Z: Multiscale instability windows (no primary).
        stride: Query schedule stride.
        b_star: Primary block length for dependence-aware inference.
        b_sensitivity: Predetermined diagnostic block lengths.
        bootstrap_B: Frozen MBB replicate count (PREREG-v0.2 §15).
        bootstrap_seed: Frozen RNG seed (PREREG-v0.2 §15).
        alpha: Two-sided CI level (PREREG-v0.2 §15).
        M: Causal standardization window for ``X`` (I01 inheritance).
        x_sigma_epsilon: LEGACY L1 field — must not be used after §13
            patch (kept temporarily for import compatibility).
    """

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
    M: int = 252
    x_sigma_epsilon: float = 1.0e-8  # legacy — do not use post §13

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
        if self.M < self.W_X:
            raise ValueError("M must be >= W_X")


DEFAULT_PARAMS = I02Params()
