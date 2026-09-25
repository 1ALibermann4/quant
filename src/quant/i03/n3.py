"""N3 adversarial IAAFT battery (I03-PREREG-v0.1 §9)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from quant.i03.iaaft import iaaft
from quant.i03.params import I03Config


@dataclass(frozen=True, slots=True)
class N3BatteryMeta:
    """N3 battery accounting."""

    B_requested: int
    n_converged: int
    n_nonconverged: int
    valid: bool
    invalid_reason: str | None
    converged_flags: tuple[bool, ...]


def n3_nonconv_frac_invalid(n_nonconverged: int, B: int, frac_max: float = 0.05) -> bool:
    """Prereg §9.3: INVALID iff ``n_non/B > frac_max`` (strict greater-than)."""

    if B < 1:
        raise ValueError("B must be positive")
    return (n_nonconverged / B) > frac_max


def generate_n3_battery(
    returns: np.ndarray,
    cfg: I03Config,
    B: int | None = None,
) -> tuple[N3BatteryMeta, list[np.ndarray]]:
    """Generate N3 surrogates; do not replace non-converged runs.

    Seed for replicate ``b``: ``10000 + b`` (prereg §9.3).
    """

    n = cfg.B_N3 if B is None else int(B)
    if n < 1:
        raise ValueError("B must be positive")
    series_list: list[np.ndarray] = []
    flags: list[bool] = []
    for b in range(1, n + 1):
        res = iaaft(
            returns,
            seed=10_000 + b,
            I_max=cfg.iaaft_I_max,
            eps=cfg.iaaft_eps,
        )
        series_list.append(res.series)
        flags.append(res.converged)
    n_non = sum(1 for f in flags if not f)
    invalid = n3_nonconv_frac_invalid(n_non, n, cfg.iaaft_nonconv_frac)
    reason = "N3_IAAFT_NONCONV_FRAC" if invalid else None
    meta = N3BatteryMeta(
        B_requested=n,
        n_converged=n - n_non,
        n_nonconverged=n_non,
        valid=not invalid,
        invalid_reason=reason,
        converged_flags=tuple(flags),
    )
    return meta, series_list
