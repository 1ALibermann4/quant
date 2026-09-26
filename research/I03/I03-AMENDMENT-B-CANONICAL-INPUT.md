# I03 — Amendment B: Canonical Numerical Input (transport)

> **Status :** DOCUMENTED — implementation available; **real SPY artifact NOT produced**  
> **Class :** NON-SCIENTIFIC IMPLEMENTATION AMENDMENT  
> **Prereg :** [I03-PREREG-v0.1.md](I03-PREREG-v0.1.md) @ `0ff457a` — **unchanged**  
> **E01 auth :** [I03-E01.md](I03-E01.md) — EXPLORATORY / UNQUALIFIED  
> **Does NOT authorize E01 observation**

```text
AMENDMENT B — EXECUTION / TRANSPORT ONLY
NO PREREG SCIENTIFIC CHANGE
NO E01 EXECUTION IN THIS MILESTONE
NO MARKET SCIENTIFIC RESULT
```

---

## 1. Motivation

Codex Cloud receives the frozen DR-008 SPY CSV/meta **bit-identically**, but
cannot construct the full pandas/A–D environment (proxy blocks package install).

Cloud **does** have NumPy 2.5.3 and can execute I03 E–I
(`run_structural_analysis`) once given a bit-identical `returns` vector.

Canonical Windows A–D (CPython 3.12.10 / MSC / NumPy 2.5.3 / pandas 3.0.6)
is the only environment proven to produce the authorized return payload SHA.

---

## 2. Boundary

```text
LOCAL (Windows MSC):
  authorized CSV+meta
    → load_cache_by_stem (exact stem)
    → log_returns
    → fail-closed identity gates
    → returns.npy + manifest.json

TRANSFER:
  bit-identical artifact directory (FILE HASH + FLOAT64 PAYLOAD HASH)

CLOUD:
  load_canonical_artifact(..., require_authorized_spy=True)
    → run_structural_analysis(returns, DEFAULT_CONFIG)   # UNCHANGED
```

Layers A–D = input preparation.  
Layers E–I = frozen science (untouched).

---

## 3. Scientific invariance

Unchanged: \(X_t\), \(W_X\), \(M\), \(\tau\), \(K\), \(P\), E-MND, locality,
N4/\(W_\sigma\), N3/IAAFT, \(B\), seeds, convergence, finite-p, coherence,
PASS/FAIL/INCONCLUSIVE.

Classification vs frozen prereg: **B** (non-scientific implementation
amendment). Prereg text is **not** rewritten.

---

## 4. Artifact contract (`I03-CANONICAL-INPUT-v1`)

| File | Role |
|------|------|
| `returns.npy` | float64 little-endian, C-contiguous, shape `(8470,)`, `r[0]=NaN` |
| `manifest.json` | provenance + dual hashes |

**FLOAT64 PAYLOAD HASH** = SHA-256 of float64 LE C-order bytes  
→ must equal `bde9a3045659bcb6ffdde99c52d7b088662456ed5d42737662f7c8384091c02e`

**FILE HASH** = SHA-256 of the on-disk `.npy` container (includes NumPy header)

Also recorded: source CSV/meta raw FILE hashes, price payload SHA, sessions,
acquisition UTC, producer environment, EXPLORATORY / UNQUALIFIED.

Fail-closed on any mismatch.

---

## 5. Operator commands

Produce (local Windows only; **do not run until authorized**):

```powershell
$env:PYTHONPATH = "src"
py -3.12 -m quant.i03 --mode produce-canonical `
  --cache-dir data/exploratory `
  --out-dir data/exploratory/canonical_i03_spy_v1
```

Consume (Cloud / any NumPy host; **E01 not authorized in this milestone**):

```text
python -m quant.i03 --mode e01 \
  --canonical-dir data/exploratory/canonical_i03_spy_v1 \
  --out-dir research/I03/e01/run1
```

Existing CSV E01 path remains:

```text
python -m quant.i03 --mode e01 --cache-dir data/exploratory --out-dir ...
```

`--cache-dir` and `--canonical-dir` are mutually exclusive.

---

## 6. Code

| Module | Role |
|--------|------|
| `src/quant/i03/canonical_input.py` | producer / consumer / gates |
| `src/quant/exploratory/adapter.py` | `load_cache_by_stem` (exact stem) |
| `src/quant/i03/e01.py` | optional canonical intake |
| `src/quant/i03/runtime.py` | `--mode produce-canonical`, `--canonical-dir` |
| `tests/i03/test_canonical_input.py` | adversarial + synthetic equivalence |

`run_structural_analysis` is **not** modified.

---

## 7. Cloud qualification (external evidence)

Independently established before this amendment:

- Cloud NumPy 2.5.3;
- I03 E–I imports OK;
- 57/57 L1/L2 PASS;
- HAT B=999 SEMANTIC_IDENTICAL (excluding `implementation_id`).

---

## 8. Stop rule

```text
STOP after implementation + synthetic validation.
Await explicit authorization before:
  - producing the real SPY canonical artifact;
  - running I03-E01 (CSV or canonical).
```
