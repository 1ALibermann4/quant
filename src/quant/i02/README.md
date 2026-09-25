# I02 implementation (L1)

Runtime package: `src/quant/i02/`

Authoritative contract: [`research/I02/I02-preregistration.md`](../../research/I02/I02-preregistration.md)

## Status

- **I02 = OPEN**
- L1: computational pipeline (this package)
- HAT: not claimed
- Exploratory run: not authorized until HAT PASS

## Entry points

```python
from quant.i02 import evaluate_query, evaluate_series, DEFAULT_PARAMS
```

Synthetic / caller-supplied log-return arrays only. No yfinance in this package.

## Contract gaps (L1 → PREREG-v0.2)

| Gap | Status |
|-----|--------|
| A — `M=252` / `ε_σ` | Contract closed (§13); **code still on I01 ε** — patch pending |
| B — S3 L+form | **HUMAN DECISION REQUIRED** (§14) |
| C — MBB inference | Contract closed (§15); **code not yet patched** |

Readiness after gap review: **C0**. See `quant.i02.contract_gaps` and
[`I02-preregistration.md`](../../research/I02/I02-preregistration.md) §13–§16.

Do not start L2/HAT until S3 is decided and implementation is patched.
