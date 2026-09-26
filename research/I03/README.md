# I03 — Intrinsic recurrence of G0

> **STATUS :** **E01 AUTHORIZED / NOT YET OBSERVED**  
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
> **E01 :** [I03-E01.md](I03-E01.md) — EXPLORATORY / UNQUALIFIED  
> **Amendment B :** [I03-AMENDMENT-B-CANONICAL-INPUT.md](I03-AMENDMENT-B-CANONICAL-INPUT.md) — transport only  
> **M1 canonical SPY :** [I03-M1-CANONICAL-SPY.md](I03-M1-CANONICAL-SPY.md) — artifact at `data/exploratory/canonical_i03_spy_v1/`  
> **Code :** `src/quant/i03/`

```text
I03 STATUS = E01 AUTHORIZED / NOT YET OBSERVED
PREREG v0.1 = UNCHANGED
L1 = PASS
L2 = PASS
HAT = PASS (synthetic)
E01 = AUTHORIZED — EXPLORATORY / UNQUALIFIED (not yet run)
W_sigma = 20 (SCALE-W)
NO SCI / PRED / ECON CLAIM
```

## Lifecycle

```text
I03-PRE → D1–D8 → DESIGN → C1–C10 → PREREG
    → Implementation Contract → L1 → L2 → HAT synthetic
    → E01 exploratory/unqualified (authorized; not yet observed)
    → postmortem / human decision (later)
```

## Object

Structural test of **current classical geometry G0** — temporal recurrence
(R3) with cross-period stability (S2), multi-scale neighborhoods, vs N4
(primary) and N3 (adversarial), no future returns.

## Operator

HAT (synthetic):

```bash
python -m quant.i03 --mode hat \
  --fixture-dir research/I03/hat \
  --out-dir research/I03/hat/run1 \
  --prepare-fixture
```

E01 (exploratory SPY / DR-008 cache — Windows `py -3.12` for hash match):

```powershell
$env:PYTHONPATH = "src"
py -3.12 -m quant.i03 --mode e01 --cache-dir data/exploratory --out-dir research/I03/e01/run1
```

Amendment B (canonical returns artifact — produce on Windows; consume on Cloud):
see [I03-AMENDMENT-B-CANONICAL-INPUT.md](I03-AMENDMENT-B-CANONICAL-INPUT.md).
**Real SPY canonical artifact and E01 not authorized in the Amendment B milestone.**

See [I03-E01.md](I03-E01.md).

Do **not** retune from I01/I02 predictive outcomes.
