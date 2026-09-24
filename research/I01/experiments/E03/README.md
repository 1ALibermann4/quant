# I01-E03 — Volatility Mechanism Diagnostic

> **Status :** EXPLORATORY / UNQUALIFIED / NOT SCIENTIFICALLY PROMOTABLE
> **Parent :** I01-E02 (revue : poursuivre l'investigation, pas confirmer)
> **Parameters :** frozen (`W=20`, `k=50`, `h=10`, L2, B0)

Does L2 add future-vol structure beyond past-volatility persistence?

The past-vol k-NN (match on `rv_W` inside the same `L_t`) is a **diagnostic
control**, not a new B0 and not a replacement for B0.

```text
python -m quant.exploratory.e03 --from-cache
```

Uses the E01 UNQUALIFIED cache. No confirmatory inference. No retuning.
