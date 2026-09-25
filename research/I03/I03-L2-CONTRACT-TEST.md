# I03 — L2 Adversarial Contract Test Report

> **STATUS :** **L2-PASS** / SYNTHETIC HAT NOT YET RUN  
> **Prereg :** [I03-PREREG-v0.1.md](I03-PREREG-v0.1.md) @ `0ff457a`  
> **L1 baseline :** `a617a50`  
> **Contract :** [I03-IMPLEMENTATION-CONTRACT-v0.1.md](I03-IMPLEMENTATION-CONTRACT-v0.1.md)  
> **Suite :** `tests/i03/test_l2_adversarial.py` + `tests/i03/oracles_l2.py`
>
> ```text
> I03 STATUS = L2-PASS / SYNTHETIC HAT NOT YET RUN
> NO MARKET DATA USED
> NO EXPERIMENT RUN
> NO PREREG RETUNING
> NO SCI / PRED / ECON CLAIM
> I02 HAT HASH DRIFT = OUT OF SCOPE (unchanged)
> ```

---

## 1. Baseline

| Item | Value |
|------|-------|
| Prereg | I03-PREREG-v0.1 @ `0ff457a` |
| L1 close | `a617a50` |
| Purpose | Falsify “implementation ≡ prereg” with independent oracles |

---

## 2. Traceability

**COVERED** for execution-affecting clauses exercised adversarially: G0, blocks,
τ, E-MND, N4 (σ + semantics + causality), N3 boundary, inference, coherence,
ND, verdict table, locality, \(n_{\min}\), artifact, reproducibility, freedoms.

---

## 3. Exact numerical boundaries (recorded)

### 3.1 Finite-surrogate \(p\le 0.05\) with \(B=999\)

\[
p=\frac{1+c}{B+1}=\frac{1+c}{1000}\le 0.05
\quad\Rightarrow\quad
c\le 49.
\]

| \(c=\#\{\Theta^*\le\Theta\}\) | \(p\) | Survive? |
|------------------------------|-------|----------|
| 49 | 0.050 | **yes** (`≤`) |
| 50 | 0.051 | **no** |

### 3.2 N3 nonconvergence `> 5%` with \(B=999\)

\[
\frac{n_{\mathrm{non}}}{999} > 0.05
\quad\Rightarrow\quad
n_{\mathrm{non}} \ge 50.
\]

| \(n_{\mathrm{non}}\) | fraction | Battery |
|----------------------|----------|---------|
| 49 | ≈0.04905 | **VALID** |
| 50 | ≈0.05005 | **INVALID** |

Helper: `n3_nonconv_frac_invalid` (strict `>`).

---

## 4. Static freedom audit

| Freedom | Status |
|---------|--------|
| `I03Config` frozen constants | Rejects retunes |
| CLI / env scientific knobs | None for science |
| `B_n4`/`B_n3`/`compute_locality_on_n4=False` | **Test-only**; now gated by `I03_ALLOW_TEST_OVERRIDES=1` (L2-I1/I2 harden) |
| Mutable alternate metrics/nulls | Not present |

---

## 5. Independent oracle results

| Domain | Result |
|--------|--------|
| G0 vs prereg oracle vs I02 | **Agree** |
| Future-suffix metamorphic | **PASS** |
| Blocks partition / remainder | **PASS** |
| τ ∈ {0,1,19,20,21} both directions | **PASS** (`≥20`) |
| E-MND k-th ≠ mean-kNN; non-tautology | **PASS** |
| N4 σ ≠ pop/RMS; envelope ≠ recompute | **PASS** (counterexample) |
| N4 causality of source σ/z | **PASS** (global shuffle distinct) |
| N3 5% boundary | **PASS** |
| p-value / left-tail / ties | **PASS** |
| Verdict table vs independent oracle | **PASS** (full boolean product) |
| Locality → INCONCLUSIVE not FAIL | **PASS** |
| Artifact reconstructs verdict | **PASS** |
| Semantic reproducibility | **PASS** |

---

## 6. Mutation-style catches

Suite fails plausible wrong contracts: `τ>20`, `ddof=0` σ, right-tail p,
`p<α` strict, majority-k PASS. N3 replacement-until-999 not implemented
(battery length = requested B).

---

## 7. Issues L2-I1…I8

| ID | Finding | Action |
|----|---------|--------|
| L2-I1 | Test overrides could leak into production calls | Gated by env `I03_ALLOW_TEST_OVERRIDES` |
| L2-I2 | N3 boundary not unit-tested as pure predicate | Added `n3_nonconv_frac_invalid` |
| L2-I8 | L2 report / README status | This document |
| I3–I7 | **None unresolved** | — |

**Prereg unchanged.**

---

## 8. Regression

| Scope | Result |
|-------|--------|
| `tests/i03` (L1+L2) | **57 passed** |
| I02 `test_hat_fixture_deterministic_hash` | **Known pre-existing FAIL** — **not modified** |
| New failures introduced by L2 | **None** |

---

## 9. Final L2 verdict

\[
\boxed{\texttt{L2-PASS}}
\]

Next: **HAT synthetic** — not market E01.
