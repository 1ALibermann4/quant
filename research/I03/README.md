# I03 — Intrinsic recurrence of G0

> **STATUS :** **IMPLEMENTED / NOT VALIDATED** (L1 complete; L2 not started)  
> **Authority class :** RESEARCH  
> **Protocol :** QDP v0.1 · DR-007  
> **Frame :** Geometry review A @ `547fc57`  
> **Pre-framing (historical) :** [`research/I03-pre/`](../I03-pre/)  
> **D1–D8 freeze :** [I03-D1-D8-FREEZE.md](I03-D1-D8-FREEZE.md)  
> **C1–C10 freeze :** [I03-C1-C10-FREEZE.md](I03-C1-C10-FREEZE.md)  
> **HD-N4-SCALE :** [I03-HD-N4-SCALE-FREEZE.md](I03-HD-N4-SCALE-FREEZE.md) — \(W_\sigma=20\)  
> **Prereg :** [I03-PREREG-v0.1.md](I03-PREREG-v0.1.md)  
> **Implementation contract :** [I03-IMPLEMENTATION-CONTRACT-v0.1.md](I03-IMPLEMENTATION-CONTRACT-v0.1.md)  
> **L1 report :** [I03-L1-IMPLEMENTATION.md](I03-L1-IMPLEMENTATION.md)  
> **Code :** `src/quant/i03/`

```text
I03 STATUS = IMPLEMENTED / NOT VALIDATED
PREREG v0.1 = DRAFT COMPLETE
L1 = PASS (synthetic)
L2 = NOT STARTED
E01 = NOT AUTHORIZED
W_sigma = 20 (SCALE-W)
PRIMARY ESTIMAND = E-MND
NO MARKET DATA
NO EXPERIMENT
NO SCI / PRED / ECON CLAIM
```

## Lifecycle

```text
I03-PRE → D1–D8 → DESIGN → C1–C10 → PREREG
    → Implementation Contract → L1 (here)
    → L2 adversarial (next)
    → HAT → human E01 authorization
```

## Object

Structural test of **current classical geometry G0** — temporal recurrence
(R3) with cross-period stability (S2), multi-scale neighborhoods, vs N4
(primary) and N3 (adversarial), no future returns.

## Lifecycle (intended)

```text
I03-PRE (done) → D1–D8 freeze (done) → DESIGN v0.1 (this)
    → human freeze of remaining C* contracts
    → executable preregistration (later)
    → implementation / HAT / E01 (later)
```

Do **not** retune from I01/I02 predictive outcomes.
