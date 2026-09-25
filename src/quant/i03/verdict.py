"""Pure verdict engine (I03-PREREG-v0.1 §12–§14).

No statistical computation here — only frozen truth-table logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class VerdictLabel(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass(frozen=True, slots=True)
class VerdictInput:
    """Completed evidence predicates for the truth table."""

    V: bool
    E: bool
    C4: bool  # multi-scale coherent globally under N4
    C3: bool  # under N3
    F4: bool  # uniform N4 non-survival


@dataclass(frozen=True, slots=True)
class VerdictResult:
    label: VerdictLabel
    nd_code: str | None
    reason: str


def decide_verdict(inp: VerdictInput) -> VerdictResult:
    """Encode prereg §14 literally."""

    if not inp.V:
        return VerdictResult(VerdictLabel.INCONCLUSIVE, None, "NEG_V")
    if not inp.E:
        return VerdictResult(VerdictLabel.INCONCLUSIVE, None, "NEG_E")

    if inp.C4 and inp.C3:
        return VerdictResult(VerdictLabel.PASS, "ND-1", "C4_AND_C3")

    if inp.F4:
        return VerdictResult(VerdictLabel.FAIL, "ND-4", "F4")

    if inp.C4 and not inp.C3:
        return VerdictResult(VerdictLabel.INCONCLUSIVE, "ND-2", "N4_OK_N3_FAIL")

    if inp.C3 and not inp.C4:
        # ND-3 without F4
        return VerdictResult(VerdictLabel.INCONCLUSIVE, "ND-3", "N3_OK_N4_NOT_F4")

    return VerdictResult(VerdictLabel.INCONCLUSIVE, "ND-5", "MIXED")
