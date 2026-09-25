# I03 — Synthetic Integrated HAT

> **Identifier :** I03-HAT-SYNTHETIC-v1  
> **Status :** **HAT-PASS**  
> **Authority class :** RESEARCH / OPERATIONAL ACCEPTANCE  
> **Protocol :** QDP v0.1 · DR-007  
> **Prereg :** [I03-PREREG-v0.1.md](I03-PREREG-v0.1.md) @ `0ff457a`  
> **L2 baseline :** `f6684ed` (L2-PASS)  
> **Class :** SYNTHETIC HAT — **NOT MARKET EVIDENCE** — **NOT SCIENTIFIC EVIDENCE**

```text
HAT VERDICT = HAT-PASS
I03 STATUS  = HAT-PASS / READY FOR HUMAN EXPERIMENT AUTHORIZATION
E01         = NOT AUTHORIZED (human decision required)
SYNTHETIC HAT
NOT MARKET EVIDENCE
NOT SCIENTIFIC EVIDENCE
NO MARKET DATA USED
NO MARKET EXPERIMENT RUN
NO FIXTURE TUNING FOR SCIENTIFIC OUTCOME
NO PREREG RETUNING
NO SCI / PRED / ECON CLAIM
```

## 1. Purpose

Answer:

> Can an operator run I03 end-to-end on a synthetic input, obtain the expected
> artifact and report, and reproduce the same scientific conclusion on a second run?

This validates **integration / operator / runtime / artifact / reproducibility**.
It does **not** validate the market hypothesis.

## 2. Baseline

| Item | Value |
|------|-------|
| Prereg | I03-PREREG-v0.1 @ `0ff457a` |
| L2 status | L2-PASS |
| L2 / pre-HAT HEAD at run time | `f6684ed` |
| Pre-HAT status | L2-PASS / SYNTHETIC HAT NOT YET RUN |
| Known unrelated | I02 HAT fixture hash drift — **OUT OF SCOPE** (untouched) |

## 3. Environment

| Item | Value |
|------|-------|
| Python | 3.12.3 (main, Aug 31 2026) [GCC 13.3.0] |
| Platform | Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.39 |
| Executable | `/mnt/c/Users/Jean Marie/dev0/quant/.venv/bin/python` |
| Working directory | repository root |

## 4. Synthetic fixture

| Field | Value |
|-------|-------|
| Fixture ID | `I03-HAT-FIXTURE-v1` |
| Generator version | `1.0.0` |
| Seed | `20260926` |
| Length | `2400` (index 0 = NaN padding) |
| SHA-256 | `sha256:0ed3625a7ed4a19e2fb75e04c8b906a92cc01be54446f61eb53c6cde1cf142dc` |
| Paths | `research/I03/hat/fixture_v1.npy`, `fixture_v1.meta.json` |
| Code | `src/quant/i03/fixture_hat.py` |

Construction (transparent; **not** market-calibrated; **not** tuned for verdict):

1. seeded Gaussian innovations;
2. tiny sinusoidal mean (`0.0005 * sin(2π t / 250)`);
3. deterministic heteroskedastic envelope
   (`0.008 + 0.004 * (0.5 + 0.5 * sin(2π t / 80))`).

Sized for M=252, W_X=20, W_σ=20, P=3, n_min=250/block, K_max=50, τ=20.

## 5. Canonical operator command

Run 1:

```bash
python -m quant.i03 --mode hat \
  --fixture-dir research/I03/hat \
  --out-dir research/I03/hat/run1 \
  --prepare-fixture
```

Run 2 (identical science; fixture already frozen):

```bash
python -m quant.i03 --mode hat \
  --fixture-dir research/I03/hat \
  --out-dir research/I03/hat/run2
```

Production path **clears** `I03_ALLOW_TEST_OVERRIDES` if present.
Official HAT uses frozen B=999 and full locality — no overrides.

## 6. Pre-run acceptance contract

### Allowed

fixture loads; G0; P=3; K={10,25,50}; τ=20; N4 W_σ=20 B=999; N3 IAAFT
B=999 I_max=100 ε=1e-8; frozen seeds; schema `I03-ARTIFACT-v1`; report;
verdict reconstructible; rerun semantically identical.

### Forbidden

any expected Θ, p-value, N4/N3 rejection, or PASS/FAIL/INCONCLUSIVE effect.

## 7. Gates H1–H20

| Gate | Criterion | Result |
|------|-----------|--------|
| H1 | canonical command exits successfully | **PASS** |
| H2 | fixture identity/hash matches frozen HAT fixture | **PASS** |
| H3 | production pipeline (`SYNTHETIC_HAT`, overrides off) | **PASS** |
| H4 | G0 params visible (W_X=20, M=252, W_σ=20) | **PASS** |
| H5 | exactly P=3 blocks | **PASS** |
| H6 | τ=20 represented | **PASS** |
| H7 | K={10,25,50} | **PASS** |
| H8 | query/sample counts per block | **PASS** |
| H9 | E-MND Θ for every block×k | **PASS** |
| H10 | locality diagnostics present | **PASS** |
| H11 | N4: W_σ=20, B=999, seed doctrine | **PASS** |
| H12 | N4 validity metadata | **PASS** |
| H13 | N3: IAAFT, B=999, I_max=100, ε=1e-8, seeds | **PASS** |
| H14 | N3 convergence accounting | **PASS** |
| H15 | finite-surrogate p-values (18 cells) | **PASS** |
| H16 | scale / cross-period coherence (C4/C3/F4) | **PASS** |
| H17 | final verdict + reason codes | **PASS** |
| H18 | independent verdict reconstruction agrees | **PASS** |
| H19 | Markdown report agrees with artifact | **PASS** |
| H20 | Run2 semantically identical to Run1 | **PASS** |

Machine summary: `research/I03/hat/hat_gates.json`.

## 8. Run 1

| Item | Value |
|------|-------|
| Out | `research/I03/hat/run1/` |
| Exit | 0 |
| Elapsed | **1372.031 s** |
| Outputs | `artifact.json`, `report.md`, `environment.json`, stdout/stderr |

### Observed structural counts (synthetic only)

| Block | n | n_queries |
|------:|--:|----------:|
| 1 | 800 | 548 |
| 2 | 800 | 800 |
| 3 | 800 | 800 |

### Null batteries (synthetic)

| Battery | Status |
|---------|--------|
| N4 | valid=True; B_used=999; Z_frac≈0.9917 |
| N3 | valid=False; reason=`N3_IAAFT_NONCONV_FRAC`; converged=**0**/999; nonconv=999 |

### Predicates / coherence / verdict (synthetic — no market meaning)

| Field | Value |
|-------|-------|
| V | False |
| E | False |
| C4 / C3 / F4 | False / False / True |
| Verdict | **INCONCLUSIVE** |
| nd_code | `null` |
| reason | `NEG_V` |

V failed the locality-vs-N4-median gate (prereg §10.2), not hard degeneracy on observed
Λ/Γ. E failed because N3 is invalid. The synthetic fixture produced full IAAFT
non-convergence under frozen I_max/ε — recorded, **not** retuned.

## 9. Integrity audit

Checked against frozen contracts: prereg/impl/fixture IDs and hash; config
(W_X, M, W_σ, τ, K, P, B, α, seeds); block boundaries; counts; Θ; locality;
null metadata; 18 p-values; coherence flags; verdict; reason codes.

All consistent with I03-PREREG-v0.1 / I03-ARTIFACT-v1.

## 10. Independent verdict reconstruction

Reconstruction **without** calling `decide_verdict` (encoding of prereg §14):

```text
not V → INCONCLUSIVE / nd_code=None
```

Agrees with artifact (`NEG_V`). **H18 PASS.**

## 11. Report audit

`report.md` is derived from `artifact.json`. Banner states SYNTHETIC HAT /
NOT MARKET EVIDENCE / NOT SCIENTIFIC EVIDENCE. Scientific statements match
artifact fields. Cosmetic re-render of Run1 report from JSON aligned `K`
display with Run2 (list form).

## 12. Run 2

| Item | Value |
|------|-------|
| Out | `research/I03/hat/run2/` |
| Exit | 0 |
| Elapsed | **1331.737 s** |
| Command | same canonical command without `--prepare-fixture` |

## 13. Semantic comparison Run1 ↔ Run2

```text
SEMANTIC_IDENTICAL
n_diffs = 0
```

Allowed non-semantic differences only: `timing.*`, `environment.*`, `operator.*`.

## 14. Issues

| ID | Class | Disposition |
|----|-------|-------------|
| — | — | **No unresolved HAT-I3 / I4 / I5** |
| OBS-1 | observation | N3 IAAFT 0/999 converged on synthetic fixture → N3 invalid → E=False. Not a HAT failure; fixture not retuned. |
| OBS-2 | observation | V=False via locality median gate on N4 surrogates. Synthetic only. |
| FIX-1 | HAT-I2 (neutral) | `config.K` forced to JSON list; compare treats tuples as lists; Run1 report regenerated from artifact. |
| FIX-2 | HAT-I1 (neutral) | stderr progress for N4/N3 generation and E-MND/locality loops. |
| FIX-3 | HAT-I1 (neutral) | locality distance loops vectorized (same semantics as L2). |
| KNOWN | out of scope | I02 HAT fixture hash drift (`tests/i02/test_hat_fixture.py`) — not repaired. |

## 15. Performance (engineering only)

| Phase | Observation |
|-------|-------------|
| Run1 total | 1372 s |
| Run2 total | 1332 s |
| N4/N3 generation | logged every 50/999 |
| E-MND / locality | logged every 50/999 (Run2+) |

No scientific performance gate. B not reduced.

## 16. Regression

| Suite | Result |
|-------|--------|
| `tests/i03` | **61 passed** |
| full `tests/` | **757 passed**, **1 failed** (`tests/i02/test_hat_fixture.py` — known unrelated hash drift) |
| Prereg changes | **none** |

## 17. Final HAT verdict

```text
HAT-PASS
H1–H20 = all PASS
production operator path works
artifact complete
report consistent
independent verdict reconstruction agrees
Run1/Run2 SEMANTIC_IDENTICAL
no unresolved HAT-I3/I4/I5
no new regression (I02 drift pre-existing)
```

**I03 status = HAT-PASS / READY FOR HUMAN EXPERIMENT AUTHORIZATION**

This does **not** authorize market execution. A human may next decide:

```text
AUTHORIZE I03-E01 — EXPLORATORY / UNQUALIFIED
```

## 18. Confirmations

```text
SYNTHETIC DATA ONLY
NO MARKET DATA USED
NO MARKET EXPERIMENT RUN
NO FIXTURE TUNING FOR SCIENTIFIC OUTCOME
NO PREREG RETUNING
NO SCI / PRED / ECON CLAIM
```
