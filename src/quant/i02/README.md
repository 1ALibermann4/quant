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

## Contract gaps (intentional)

- **S3 kNN**: aggregation L+form / metric primary underspecified → `ImplementationContractGap`
- **Bootstrap inference**: algorithm not uniquely specified → `ImplementationContractGap`

See `quant.i02.contract_gaps`.
