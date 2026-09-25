# I03 — L1 Implementation Report

> **STATUS :** L1 COMPLETE — **IMPLEMENTED / NOT VALIDATED**  
> **Prereg :** [I03-PREREG-v0.1.md](I03-PREREG-v0.1.md) @ `0ff457a`  
> **Contract :** [I03-IMPLEMENTATION-CONTRACT-v0.1.md](I03-IMPLEMENTATION-CONTRACT-v0.1.md)  
> **Package :** `src/quant/i03/`
>
> ```text
> I03 STATUS = IMPLEMENTED / NOT VALIDATED
> L2 ADVERSARIAL = NOT STARTED
> E01 = NOT AUTHORIZED
> NO MARKET DATA USED
> NO EXPERIMENT RUN
> NO PREREG RETUNING
> NO SCI / PRED / ECON CLAIM
> ```

---

## 1. Traceability coverage

All prereg execution clauses mapped in the implementation contract matrix
(G0, τ, blocks, E-MND, N4, N3, inference, locality, coherence, verdict,
artifact). No unmapped execution-affecting clause identified during L1.

---

## 2. Architecture

| Module | Role |
|--------|------|
| `params.py` | Single frozen `I03Config` |
| `g0.py` | G0 via I02 `states_x` (compatibility asserted) |
| `blocks.py` | P=3 + remainder→B3 |
| `emnd.py` | E-MND / τ pools / ties |
| `n4.py` | SCALE-W σ path + shuffle reconstruction |
| `iaaft.py` / `n3.py` | IAAFT battery + nonconvergence accounting |
| `locality.py` | C6-D validity diagnostics |
| `inference.py` | Finite-surrogate left-tail p |
| `coherence.py` | Survival grid / C4 / C3 / F4 |
| `verdict.py` | Pure truth table |
| `pipeline.py` | Structural runner + artifact dict |

Production entry: `run_structural_analysis(returns, cfg)` — **no download**.
Test-only `B_n4`/`B_n3` overrides exist on the runner; production must omit them.

---

## 3. G0 reuse

**Reused** `quant.i02.states_x` (causal M=252, W_X=20, ddof=1, no ε, σ=0→undefined,
index-0 padding). Classified **compatible** with I03-PREREG §3. Mismatch would be
**L1-I5 STOP**.

---

## 4. E-MND

`δ_k` = k-th τ-separated intra-block L2 distance; `Θ_k(p)` = mean over
`T_p` with `|A|≥k_max`. Ties `(dist↑, s↑)`. Vectorized distance sort for speed.

---

## 5. N4

`W_σ=20`, sample stdev denominator 19, inclusive of `r_t`, ≠ I02 RMS RV.

**Preserved by construction:** observed `{σ̂_t}` path.  
**Not claimed:** recomputed rolling stdev on `r*` equals that path.  
Documented in code docstring and artifact fields `preserves` /
`does_not_claim`.

Seeds: `42+b`. Validity: `|Z|/T < 0.95` or `var(σ̂_Z)=0` → INVALID.

---

## 6. N3

IAAFT on full series; seeds `10000+b`; `I_max=100`; `ε=1e-8`.
Non-converged surrogates **kept** (not replaced). Gate: >5% flags → INVALID.

---

## 7. Inference

`p=(1+#{Θ*≤Θ})/(B+1)`; survive iff `p≤α`; no Bonferroni.

---

## 8. Verdict

Pure `decide_verdict(VerdictInput)` encoding prereg §14. Diagnostics cannot
rescue FAIL.

---

## 9. Artifact schema

`I03-ARTIFACT-v1` via `artifact_dict` — config, blocks, Θ, locality, N4/N3
meta, survival, predicates, verdict, N4 preservation semantics.

---

## 10. L1 synthetic tests

Suite: `tests/i03/` — **20 passed** (synthetic only).

Covers: causality, τ boundary, blocks, k-th oracle/ties, σ denom 19,
N4 preserve/determinism, p=α, verdict PASS/FAIL/INCONCLUSIVE, N3 accounting,
pipeline determinism, config freeze.

---

## 11. Repository regression

| Suite | Result |
|-------|--------|
| `tests/i03` + `tests/i01` | **58 passed** |
| `tests/i02` (excl. HAT fixture hash) | **96 passed** |
| `tests/i02::test_hat_fixture_deterministic_hash` | **FAIL** — pinned SHA drift (`196f9…` → `9dba0…`); **pre-existing / unrelated to I03** (no I02 code changed). Track as env/numpy fixture pin issue, not L1-I03 blocker. |

---

## 12. Issues (L1-I1…I6)

| ID | Finding | Action |
|----|---------|--------|
| — | None scientific (I3/I4/I5) | — |
| L1-I1 | Initial E-MND Python loop too slow for T≈2400×surrogates | Fixed: vectorized distances |
| L1-I6 | N4 “recomputed σ on r*” clarification | Documented in contract + artifact |
| (ext) | I02 HAT fixture hash mismatch | Out of I03 scope; not introduced by this work |

---

## 13. Prereg changes

**None.**

---

## 14. Next milestone

**L2 adversarial contract test** (synthetic). Not market E01.
