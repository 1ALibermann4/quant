"""Frozen I01 v0.2 numerical parameters.

Values are copied from ``research/I01/configuration.yaml``. The YAML is the
research authority; this module is the runtime copy. Do not retune after seeing
results (DR-007 D-4).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class I01Params:
    """Pre-registered I01 geometry parameters.

    Attributes:
        W: State window length (sessions).
        M: Causal standardization window (sessions), inclusive of ``r_t``.
        epsilon: Floor added to σ̂ and to shape-normalization norms.
        h: Future horizon (sessions); ``Y_t`` is ``(r_{t+1}, …, r_{t+h})``.
        k: Neighborhood size.
        tau: Embargo half-width; candidates with ``|s-t| <= tau`` are excluded.
        L_min: Minimum admissible library size for an evaluation date.
        B0_R: Monte-Carlo repetitions of baseline B0.
        B0_seed: Frozen RNG seed for B0 (protocol §5).
    """

    W: int = 20
    M: int = 252
    epsilon: float = 1.0e-8
    h: int = 10
    k: int = 50
    tau: int = 20
    L_min: int = 150
    B0_R: int = 200
    B0_seed: int = 42

    def __post_init__(self) -> None:
        if self.W < 1 or self.M < 2 or self.h < 1 or self.k < 2:
            raise ValueError("W, M, h, k must be in range (W>=1, M>=2, h>=1, k>=2)")
        if self.M < self.W:
            raise ValueError("M must be >= W so X_t sits inside the μ/σ window")
        if self.tau < 0 or self.L_min < self.k:
            raise ValueError("tau >= 0 and L_min >= k are required")
        if self.B0_R < 1:
            raise ValueError("B0_R must be >= 1")


DEFAULT_PARAMS = I01Params()
