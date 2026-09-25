"""Incremental-value estimands ``D`` (secondary) and ``R`` (primary)."""

from __future__ import annotations

from quant.i02.types import SkipReason


def score_difference(crps_s: float, crps_x: float) -> float:
    """``D = CRPS_S - CRPS_X`` (secondary diagnostic)."""

    return float(crps_s) - float(crps_x)


def relative_incremental_value(
    crps_s: float, crps_x: float
) -> tuple[float | None, SkipReason | None]:
    """Primary estimand ``R = D / CRPS_S``.

    If ``CRPS_S == 0``, returns ``(None, CRPS_COMPARATOR_ZERO)``.
    No epsilon, sentinel, or silent zero.
    """

    cs = float(crps_s)
    if cs == 0.0:
        return None, SkipReason.CRPS_COMPARATOR_ZERO
    d = score_difference(cs, crps_x)
    return d / cs, None
