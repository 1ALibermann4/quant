"""I02 mathematical core — vendor-agnostic preregistered pipeline.

Authority: ``research/I02/I02-preregistration.md`` (I02-PREREG-v0.3).
Design history: ``research/I02/I02-hypothesis-draft.md``.

This package must not import market-data vendors or ``quant.exploratory``.
L1 implements the computational contract; HAT / exploratory runs are
separate milestones.

Contract gaps A/B/C closed (v0.3): M=252 no-ε X; S3-A dual charts;
non-circular MBB. See :mod:`quant.i02.contract_gaps`.

Operational entry point (HAT / future exploratory):

```text
python -m quant.i02 --input fixture.npz --output-dir out/
```
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
