"""I02 mathematical core — vendor-agnostic preregistered pipeline.

Authority: ``research/I02/I02-preregistration.md`` (frozen contract).
Design history: ``research/I02/I02-hypothesis-draft.md``.

This package must not import market-data vendors or ``quant.exploratory``.
L1 implements the computational contract; HAT / exploratory runs are
separate milestones.

Known contract gaps (do not invent fixes here):

* S3 kNN distance / L+form aggregation still OPEN in the draft
  (§9.16 vs aggregation OPEN) — see :mod:`quant.i02.contract_gaps`.
* Moving/block bootstrap algorithm details (replicates, wrapping,
  CI construction) underspecified for a unique implementation —
  see :mod:`quant.i02.contract_gaps`.
"""

from quant.i02.params import DEFAULT_PARAMS, I02Params
from quant.i02.pipeline import QueryResult, evaluate_query, evaluate_series
from quant.i02.types import SkipReason

__all__ = [
    "DEFAULT_PARAMS",
    "I02Params",
    "QueryResult",
    "SkipReason",
    "evaluate_query",
    "evaluate_series",
]
