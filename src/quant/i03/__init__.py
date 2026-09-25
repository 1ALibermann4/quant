"""I03 — Intrinsic temporal recurrence of G0 (prereg I03-PREREG-v0.1).

Structural analysis only. No market download in this package's tests.
"""

from quant.i03.params import DEFAULT_CONFIG, I03Config
from quant.i03.verdict import VerdictLabel, decide_verdict

__all__ = [
    "DEFAULT_CONFIG",
    "I03Config",
    "VerdictLabel",
    "decide_verdict",
]
