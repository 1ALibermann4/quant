# I02 implementation (historical — investigation CLOSED)

Runtime package: `src/quant/i02/`

> **I02 = CLOSED — EXPL-ABSENT**  
> Closure: [`research/I02/I02-CLOSURE.md`](../../research/I02/I02-CLOSURE.md)  
> Contract (historical): [`I02-PREREG-v0.3`](../../research/I02/I02-preregistration.md)

## Lifecycle status

| Stage | Status |
|-------|--------|
| Design | R2 CLOSED |
| L1 / C2 | aligned v0.3 |
| L2 | [PASS](../../research/I02/I02-L2-CONTRACT-TEST.md) |
| HAT | [PASS](../../research/I02/I02-HAT.md) (operational) |
| E01 | [EXPL-ABSENT](../../research/I02/I02-E01.md) |
| Postmortem | [read-only](../../research/I02/I02-E01-POSTMORTEM.md) |
| Investigation | **CLOSED** |

Not a software failure. Not SCI-PASS / SCI-FAIL.

Scientific artifacts are historical. Do not retune as “I02-E02”.
I03 is not opened.

## Entry points (maintenance / replay only)

```python
from quant.i02 import evaluate_query, evaluate_series, DEFAULT_PARAMS
```

```text
python -m quant.i02 --input fixture.npz --output-dir out/
python -m quant.i02.e01 --cache-dir data/exploratory --output-dir out/
```

No scientific knobs. Replay does not reopen the investigation.
