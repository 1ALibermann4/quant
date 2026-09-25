"""Frozen I02 scientific parameters (preregistration §0).

Scientific constants are frozen here as the runtime source of truth.
Do not expose them as CLI tuning knobs. Do not retune after results
(DR-007 D-4 / I02 change-control class C).

``X`` standardization length ``M`` and sigma floor ``x_sigma_epsilon``
are **inherited from the I01 geometric form of** ``X`` (standardized
log-returns), not listed in the I02 prereg §0 table. See
:data:`quant.i02.contract_gaps.X_STANDARDIZATION_INHERITANCE_NOTE`.
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
        M: Causal standardization window for ``X`` (I01 inheritance).
        x_sigma_epsilon: Floor on σ̂ in ``X`` standardization (I01 form).
    """

    W_X: int = 20
    W_RV: int = 20
    h: int = 10
    k: int = 50
    M_Z: tuple[int, ...] = (3, 12, 21)
    stride: int = 1
    b_star: int = 40
    b_sensitivity: tuple[int, ...] = (20, 40, 80)
    # I01 geometric X inheritance (not in I02 prereg §0 table):
    M: int = 252
    x_sigma_epsilon: float = 1.0e-8

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
        if self.W_X % 2 != 0:
            raise ValueError("W_X must be even for S2 early/late 10+10 split")
        if self.M < self.W_X:
            raise ValueError("M must be >= W_X")


DEFAULT_PARAMS = I02Params()
