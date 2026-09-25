"""I02 mathematical core — historical (investigation CLOSED — EXPL-ABSENT).

Authority: ``research/I02/I02-preregistration.md`` (I02-PREREG-v0.3, historical).
Closure: ``research/I02/I02-CLOSURE.md``.
Design history: ``research/I02/I02-hypothesis-draft.md``.

This package must not import market-data vendors into the mathematical core.
Replay / maintenance only — does not reopen I02. I03 is not opened.
"""

from quant.i02.bootstrap import MBBResult, mbb_spearman_ci, mbb_spearman_robustness
from quant.i02.params import DEFAULT_PARAMS, I02Params
from quant.i02.pipeline import QueryResult, evaluate_query, evaluate_series
from quant.i02.types import SkipReason

__all__ = [
    "DEFAULT_PARAMS",
    "I02Params",
    "MBBResult",
    "QueryResult",
    "SkipReason",
    "evaluate_query",
    "evaluate_series",
    "mbb_spearman_ci",
    "mbb_spearman_robustness",
]
