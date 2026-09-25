"""Frozen I03 scientific configuration (I03-PREREG-v0.1 §0).

Single canonical source of constants — do not duplicate magic numbers.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class I03Config:
    """Preregistered I03 constants.

    Indexing convention (inherited from I02 G0): ``returns[0]`` is unused
    padding; the first valid return lives at index ``1``.
    """

    W_X: int = 20
    M: int = 252
    W_sigma: int = 20
    tau: int = 20
    K: tuple[int, ...] = (10, 25, 50)
    k_max: int = 50
    P: int = 3
    B_N4: int = 999
    B_N3: int = 999
    alpha: float = 0.05
    master_seed: int = 42
    n_min: int = 250
    m_rand: int = 50
    iaaft_I_max: int = 100
    iaaft_eps: float = 1e-8
    iaaft_nonconv_frac: float = 0.05
    n4_z_frac_min: float = 0.95
    prereg_id: str = "I03-PREREG-v0.1"

    def __post_init__(self) -> None:
        if self.W_X != 20 or self.W_sigma != 20 or self.tau != 20:
            raise ValueError("I03 freezes W_X = W_sigma = tau = 20")
        if self.M != 252:
            raise ValueError("I03 freezes M = 252")
        if self.K != (10, 25, 50) or self.k_max != 50:
            raise ValueError("I03 freezes K = {10,25,50}, k_max = 50")
        if self.P != 3:
            raise ValueError("I03 freezes P = 3")
        if self.B_N4 != 999 or self.B_N3 != 999:
            raise ValueError("I03 freezes B_N4 = B_N3 = 999")
        if self.alpha != 0.05:
            raise ValueError("I03 freezes alpha = 0.05")
        if self.n_min != 250 or self.m_rand != 50:
            raise ValueError("I03 freezes n_min = 250, m_rand = 50")
        if self.W_sigma != self.W_X:
            raise ValueError("W_sigma must equal W_X under SCALE-W")


DEFAULT_CONFIG = I03Config()
