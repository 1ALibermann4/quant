# I02 implementation (L1 patch / PREREG-v0.3)

Runtime package: `src/quant/i02/`

Authoritative contract: [`research/I02/I02-preregistration.md`](../../research/I02/I02-preregistration.md) — **I02-PREREG-v0.3**

## Status

- **I02 = OPEN**
- L1: computational pipeline aligned with v0.3 (this package) — **C2**
- L2: contract-test closure — [`I02-L2-CONTRACT-TEST.md`](../../research/I02/I02-L2-CONTRACT-TEST.md)
- HAT: **PASS** — [`I02-HAT.md`](../../research/I02/I02-HAT.md) (synthetic operational; not scientific evidence)
- Exploratory run: not started (distinct from HAT)
- Readiness: **HAT-PASS** (authorized to prepare exploratory run under DR-007; not SCI)

## Entry points

```python
from quant.i02 import evaluate_query, evaluate_series, DEFAULT_PARAMS
from quant.i02 import mbb_spearman_ci, mbb_spearman_robustness
```

Synthetic / caller-supplied log-return arrays only. No yfinance in this package.

## Contract gaps (CLOSED)

| Gap | Status |
|-----|--------|
| A — `M=252` / `ε_σ` | **CLOSED** — M inherited; no ε; `σ̂=0` ⇒ X undefined |
| B — S3 L+form | **CLOSED** — S3-A ACCEPTED; co-equal `S3_Q` / `S3_phi`; no primary |
| C — MBB inference | **CLOSED** — non-circular MBB; B=9999; seed=42; CI-dual detectability |

See `quant.i02.contract_gaps` and prereg §13–§16.

Do not start HAT until L2 contract-test closure. No market data / no experiment.
