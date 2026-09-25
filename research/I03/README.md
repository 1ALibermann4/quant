# I03 — Intrinsic recurrence of G0

> **STATUS :** **HAT-PASS** / READY FOR HUMAN EXPERIMENT AUTHORIZATION  
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
> **L2 report :** [I03-L2-CONTRACT-TEST.md](I03-L2-CONTRACT-TEST.md)  
> **HAT report :** [I03-HAT.md](I03-HAT.md)  
> **Code :** `src/quant/i03/`

```text
I03 STATUS = HAT-PASS / READY FOR HUMAN EXPERIMENT AUTHORIZATION
PREREG v0.1 = DRAFT COMPLETE
L1 = PASS
L2 = PASS
HAT = PASS (synthetic integrated)
E01 = NOT AUTHORIZED
W_sigma = 20 (SCALE-W)
NO MARKET DATA
NO EXPERIMENT
NO SCI / PRED / ECON CLAIM
```

## Lifecycle

```text
I03-PRE → D1–D8 → DESIGN → C1–C10 → PREREG
    → Implementation Contract → L1 → L2 → HAT synthetic (here)
    → human E01 authorization (next; not granted)
```

## Object

Structural test of **current classical geometry G0** — temporal recurrence
(R3) with cross-period stability (S2), multi-scale neighborhoods, vs N4
(primary) and N3 (adversarial), no future returns.

## Operator (HAT)

```bash
python -m quant.i03 --mode hat \
  --fixture-dir research/I03/hat \
  --out-dir research/I03/hat/run1 \
  --prepare-fixture
```

Synthetic fixture only. See [I03-HAT.md](I03-HAT.md).

Do **not** retune from I01/I02 predictive outcomes.
