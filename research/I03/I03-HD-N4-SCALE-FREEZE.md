# I03 — HD-N4-SCALE freeze

> **STATUS :** HUMAN-FROZEN  
> **Decision :** **SCALE-W**  
> **Parent :** [I03-C1-C10-FREEZE.md](I03-C1-C10-FREEZE.md)

```text
W_sigma := W_RV := W_X = 20
SCALE-M = REJECTED FOR PRIMARY N4
NO MARKET RESULT USED
```

## Freeze

\[
W_\sigma := W_{RV} := W_X = 20.
\]

Classification: **derived nuisance-control horizon** (aligned with the
local scale of represented state \(X\)), **not** a fitted / optimized /
result-selected parameter.

## Rationale (human)

N4 attacks the I01 nuisance that apparent G0 recurrence may reflect local
volatility. The relevant horizon is the local vol scale of the state window
(\(W_{RV}=W_X=20\)), not the causal normalization window \(M=252\).

## Estimator formula authority

Follows C3 “analogous stdev” to G0’s sample-stdev contract, with window
\(W_\sigma\) replacing \(M\). **Not** identical to I02’s undemeaned RMS
\(RV_t\) (same window length, different functional). Full formula is in
[I03-PREREG-v0.1.md](I03-PREREG-v0.1.md) §N4.
