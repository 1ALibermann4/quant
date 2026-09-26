# I03 — Formal scientific closure

> **INVESTIGATION :** I03 — Classical Geometric Recurrence (intrinsic recurrence of G0)  
> **STATUS :** **CLOSED**  
> **EVIDENCE LEVEL :** EXPLORATORY / UNQUALIFIED (DR-007 / DR-008)  
> **FINAL STRUCTURAL VERDICT :** INCONCLUSIVE (`NEG_E`)  
> **EXPLORATORY CLASSIFICATION :** **EXPL-INCONCLUSIVE**  
> **Authority class :** RESEARCH · QDP v0.1  
> **Preregistration :** [I03-PREREG-v0.1.md](I03-PREREG-v0.1.md) @ `0ff457a` — **unchanged through closure**  
> **Canonical E01 observation :** [e01/run2/I03-E01-RUN2.md](e01/run2/I03-E01-RUN2.md) @ `b4ea158`  
> **Execution HEAD (RUN2) :** `1dfdae6`

```text
I03 = CLOSED
FINAL STRUCTURAL = INCONCLUSIVE (NEG_E)
EXPLORATORY = EXPL-INCONCLUSIVE
NOT SCI-PASS · NOT SCI-FAIL
NO SCI PROMOTION · NO PRED PROMOTION · NO ECON PROMOTION
E02 = NOT AUTHORIZED / NOT EXECUTED
G0 = BASELINE / REFERENCE GEOMETRY — NOT PROMOTED
N3 = INVALID UNDER I03 RUN2 CONTRACT
NO NEW EXPERIMENT · NO N3 REPAIR · NO NEXT INVESTIGATION STARTED
```

---

## 1. Executive closure

I03 asked whether **current classical geometry G0** exhibits **nontrivial local
temporal recurrence** that is **coherent** across preregistered neighborhood
scales and time blocks, relative to frozen nulls N4 and N3, **without**
future-return information.

A single complete exploratory observation — **E01 RUN2** on the authorized
UNQUALIFIED SPY canonical input — was executed after a long engineering
qualification chain. Under the **frozen** decision table:

| Predicate | RUN2 |
|-----------|------|
| \(V\) | TRUE |
| \(E\) | FALSE |
| \(C_4\) | FALSE |
| \(C_3\) | FALSE |
| \(F_4\) | FALSE |

Therefore **PASS** and **FAIL** are both unavailable. The only legitimate
structural label is **INCONCLUSIVE** (`NEG_E`). Mapped for E01 reporting:
**EXPL-INCONCLUSIVE**.

This closes the investigation. It does **not** authorize E02, confirmation,
or promotion.

---

## 2. Original scientific question

Faithful restatement of [I03-PREREG-v0.1 §1](I03-PREREG-v0.1.md):

> Under fixed causal G0 and mandatory temporal exclusion \(|t-s|\ge\tau\) with
> \(\tau=W_X\), does the market-state trajectory exhibit nontrivial local
> temporal recurrence—measured by mean τ-separated \(k\)-NN distance
> (E-MND)—that is coherent across neighborhood scales \(\mathcal{K}\) and
> across \(P=3\) deterministic time blocks, beyond a preregistered
> volatility-preserving null N4 (\(W_\sigma=20\)) and under an adversarial
> IAAFT null N3, without using future-return information?

**Object:** STRUCTURE / RECURRENCE under G0.  
**Not in scope:** prediction, profitability, economic exploitability
(prereg §1.1 / D8).

---

## 3. Frozen design (G0, estimand, nulls, inference)

### 3.1 G0 (unchanged after results)

| Object | Contract |
|--------|----------|
| State | \(X_t\) = causally standardized return window |
| \(W_X\) | 20 |
| Metric | Euclidean \(L_2\) |
| Temporal exclusion | \(\|t-s\|\ge\tau\), \(\tau=W_X=20\) |
| \(M\) | 252 (causal normalization window) |
| \(\mathcal{K}\) | \(\{10,25,50\}\) — report all; **no** best-\(k\) |
| \(P\) | 3 contiguous blocks |
| Primary estimand | \(\Theta_k(p)\) = mean \(k\)-th admissible-neighbor distance (E-MND) |
| Locality diagnostics | \(\Lambda\), \(\Gamma\) (validity prerequisite; non-promotional) |

Sources: PREREG §3–§6, §10; C1–C10; HD-N4-SCALE (\(W_\sigma=20\)).

### 3.2 N4 — volatility-preserving null

- \(\hat\sigma_t\): causal sample stdev, \(W_\sigma=20\), denominator \(19\), inclusive \(r_t\)
- \(z_t=r_t/\hat\sigma_t\); shuffle \(z\) on defined set; \(r^\ast_t=\hat\sigma_t\,z^\ast_t\)
- \(B=999\); seed \(=42+b\)

### 3.3 N3 — adversarial linear/spectral null (IAAFT)

- IAAFT on returns; rebuild \(X^\ast\); recompute E-MND
- \(B=999\); seed \(=10000+b\)
- \(I_{\max}=100\); \(\varepsilon=10^{-8}\)
- **Frozen validity (BEFORE RUN2):** if non-convergence fraction \(>0.05\) →
  **N3 INVALID** → contributes to \(\neg E\) → **INCONCLUSIVE**
  (PREREG §0 table, §9, §13)

### 3.4 Inference and truth table (PREREG §11–§14)

- \(\alpha=0.05\)
- \(p=(1+\#\{\Theta^\ast\le\Theta\})/(B+1)\)
- Cell survival \(S_\nu(k,p)\) at \(\alpha\)
- **Coherent\((p,\nu)\):** \(S_\nu(k,p)=1\) for **all** \(k\in\mathcal{K}\)
- \(C_\nu\): coherent for **all** periods \(p\in\{1,2,3\}\)
- \(F_4\): \(S_{\mathrm{N4}}(k,p)=0\) for **all** \(k\) and **all** \(p\)

| Symbol | Meaning (prereg) |
|--------|------------------|
| \(V\) | Locality validity (§10.2) — not hard-degenerate; required positive distances |
| \(E\) | \(|\mathcal{T}_p|\ge n_{\min}\) ∀p; **N4 not INVALID; N3 not INVALID** |
| \(C_4\) | Global N4 coherence \(C_{\mathrm{N4}}\) |
| \(C_3\) | Global N3 coherence \(C_{\mathrm{N3}}\) |
| \(F_4\) | Uniform N4 non-survival |

| Condition | Verdict |
|-----------|---------|
| \(\neg V\) or \(\neg E\) | **INCONCLUSIVE** |
| \(V\land E\land C_4\land C_3\) | **PASS** |
| \(V\land E\land F_4\) | **FAIL** |
| other \(V\land E\) combinations | **INCONCLUSIVE** (incl. ND-2) |

PASS is stringent. **NOT PASS ≠ automatic FAIL.**

---

## 4. Evidence chain (audit)

```text
I03-PRE (91d6c9d)
  → D1–D8 / DESIGN (15ab106)
  → C1–C10 freeze (c6a26a3)
  → HD-N4-SCALE (W_σ=20)
  → PREREG v0.1 (0ff457a)
  → Implementation contract → L1 (fb23c06 / 570246c)
  → L2-PASS (684c933 / 0dda827 @ f6684ed lineage)
  → HAT synthetic PASS (f61eefe / 32583aa)
  → E01 authorization freeze (0a50a2f) — EXPLORATORY / UNQUALIFIED
  → Amendment B canonical input (4e7bec1 / ab9fa82)
  → M1 materialize SPY artifact (8a19b47 / 055b6be)
  → M2 Cloud transport FAIL (CRLF FILE hash) → M2R LF fix (6dc8adb)
  → Cloud runtime qualification (external; NumPy/L1–L2/HAT documented)
  → Cloud E01 RUN1: ABORTED — RESOURCE CONSTRAINT (dfa3bd9 reported; no science)
  → PERF-01 Phase 0 (c304d7b) → 1A (109faaa / 651e9ee) → 1B (f7bcb67 / 0592ee8)
    → 1C (3b73be0 / bb5d1ee) → Final HAT (38ce793) → CLI wiring (4300eb9 / 1dfdae6)
  → E01 RUN2 COMPLETE (b4ea158) — EXPL-INCONCLUSIVE
  → THIS CLOSURE
```

Failed / aborted operational milestones are **retained** (M2 CRLF fail-closed;
Cloud RUN1 abort). They are not scientific results.

---

## 5. RUN1 operational abort

| Item | Record |
|------|--------|
| Status | `I03-E01 CLOUD RUN1: ABORTED — RESOURCE CONSTRAINT` |
| Evidence (reported) | `dfa3bd9…` (cited in PERF-01 Phase 0) |
| Wall | ~4312 s (~71.9 min) |
| Last progress | N4 E-MND **950/999** |
| Scientific verdict | **NONE** |
| Exploratory label | **NONE** |
| Partial Θ / p interpretation | **FORBIDDEN** |

RUN1 motivated **PERF-01 engineering** only. It did **not** change
preregistration, parameters, nulls, or geometry.

---

## 6. PERF-01 engineering qualification

**Purpose:** make the **frozen** experiment executable without changing
scientific semantics.

| Phase | Role | Status |
|-------|------|--------|
| 0 | Profile / parallelization design | PROCEED |
| 1A | Exact E-MND/locality kernel optimization | PASS |
| 1B | Deterministic ProcessPool (`workers`) | PASS |
| 1C | Deterministic checkpoint / resume | PASS |
| Final local HAT | Stack qualification interrupt/resume BITWISE | PASS (`38ce793`) |
| CLI wiring | Forward `--workers` / checkpoint / `--resume` to E01 | PASS (`4300eb9`/`1dfdae6`) |

```text
PERF-01 changed EXECUTION MECHANICS, not I03 SCIENTIFIC SEMANTICS.
```

---

## 7. RUN2 execution integrity

| Item | Value |
|------|--------|
| Execution HEAD | `1dfdae6` |
| Result commit | `b4ea158` |
| Environment | Windows 11 · Python 3.12.10 · NumPy 2.5.3 · i5-1035G1 · workers=4 · BLAS=1 |
| Wall | **7218.3 s (~2.01 h)** |
| Interrupt/resume | **none** |
| Completeness | N4 **999/999** · N3 **999/999** · checkpoint **COMPLETE** · seeds PASS |
| Canonical input | payload `bde9a304…` · npy `4aee1aae…` · manifest transport `9d285f24…` |
| Input class | EXPLORATORY / UNQUALIFIED |

Full record: [e01/run2/I03-E01-RUN2.md](e01/run2/I03-E01-RUN2.md).

---

## 8. Locality (MEASURED)

\(V=\mathbf{TRUE}\).

| Period | Λ | Γ | hard_degenerate |
|--------|---|---|-----------------|
| 1 | 0.5137 | 0.3008 | false |
| 2 | 0.4969 | 0.2922 | false |
| 3 | 0.4759 | 0.2914 | false |

**Allowed:** G0 did **not** fail the preregistered locality validity prerequisite
on this exploratory dataset.  
**Forbidden:** “G0 is validated”; “market states form useful predictive clusters.”

---

## 9. N4 results (MEASURED — full 9-cell)

Observed finite \(p\)-values (α=0.05 survival in parentheses):

| Period \ \(k\) | 10 | 25 | 50 |
|----------------|----|----|-----|
| 1 | 0.666 (F) | 0.822 (F) | 0.877 (F) |
| 2 | 0.119 (F) | 0.281 (F) | 0.424 (F) |
| 3 | **0.029 (T)** | 0.064 (F) | 0.115 (F) |

N4 meta: valid; \(Z_{\mathrm{frac}}\approx 0.9976\); \(B=999\).

**Only one of nine cells** crosses α: **P3 / \(k=10\) / \(p=0.029\)**.

Under frozen coherence, this **isolated** cell:

- MUST NOT be selected post hoc as evidence of structural recurrence;
- is **not** a “discovery”;
- is **not** discarded — it is an observed cell that does **not** satisfy
  \(C_4\) (requires survival for **all** \(k\) in **all** periods).

Hence \(C_4=\mathbf{FALSE}\). Also \(F_4=\mathbf{FALSE}\) (not uniform
non-survival across all cells).

---

## 10. N3 validity failure (MEASURED)

| Metric | Value |
|--------|--------|
| Converged | **0 / 999** |
| Non-converged | **999 / 999** |
| Fraction | **1.0** |
| Threshold | \(>0.05\) (preregistered **before** RUN2) |
| Status | **N3 = INVALID** (`N3_IAAFT_NONCONV_FRAC`) |

**Scientifically relevant statement:**  
N3 **failed its preregistered validity requirement**.

Artifact N3 \(p=1.0\) / \(S=\mathrm{false}\) on all cells are **not**
interpretable as “spectral null explains the data,” nor as rejection or
confirmation of recurrence. They are associated with an **invalid** null
execution under the frozen contract.

```text
DO NOT: "N3 rejected recurrence"
DO NOT: "N3 confirmed the null"
DO NOT: repair / retune / replace N3 in this closure
```

---

## 11. Frozen decision logic → final verdict

| Predicate | Value | Consequence |
|-----------|-------|-------------|
| \(V\) | TRUE | Locality gate passed |
| \(E\) | **FALSE** | N3 INVALID (among other \(E\) conjuncts) |
| \(C_4\) | FALSE | No global N4 coherence |
| \(C_3\) | FALSE | N3 not a valid coherent null outcome |
| \(F_4\) | FALSE | Not uniform N4 non-survival |

- PASS \(= V\land E\land C_4\land C_3\) → **not met** (\(E\) false; also \(C_4,C_3\) false)
- FAIL \(= V\land E\land F_4\) → **not met** (\(E\) false)
- Therefore **INCONCLUSIVE** by first row of the truth table: \(\neg E\)

Reason code: **`NEG_E`**.

Exploratory mapping (DR-007 / E01 contract):  
**INCONCLUSIVE → EXPL-INCONCLUSIVE**.

This is the **only** legitimate classification under the frozen rule given
RUN2 evidence. It is **not** SCI-FAIL, **not** evidence of absence, and
**not** a soft PASS.

---

## 12. What I03 establishes

### A. Engineering

The frozen experiment is executable reproducibly with:

- Amendment B canonical numerical input;
- deterministic multiprocessing (`workers`);
- deterministic checkpoint / resume;
- bitwise-qualified mechanics (PERF-01 + Final HAT);
- CLI forwarding for E01 operational flags.

### B. Geometry / locality

On this exploratory SPY path, G0 **satisfies** the frozen locality validity
prerequisite (\(V=\mathrm{TRUE}\)).

### C. N4

The N4 comparison **does not** exhibit the required **coherent** recurrence
pattern across all preregistered periods and neighborhood scales
(\(C_4=\mathrm{FALSE}\)). One isolated cell (P3/\(k=10\)) is recorded without
promotion.

### D. N3

The preregistered adversarial N3 (IAAFT) is **INVALID** on RUN2:
**0/999** converged under frozen \(I_{\max}/\varepsilon\).

### E. Overall

I03 **cannot** establish structural **PASS** or structural **FAIL** under
its frozen decision rule. Final label: **INCONCLUSIVE / EXPL-INCONCLUSIVE**.

---

## 13. What I03 does not establish

I03 does **not** establish:

- that G0 is universally invalid;
- that Euclidean geometry cannot model markets;
- that markets lack recurrent structure;
- that P3/\(k=10\) is a robust phenomenon;
- that N4 “fully explains” G0;
- that N3 confirms or rejects recurrence;
- predictive power; economic exploitability; profitability;
- SCI-level evidence; PRED promotion; ECON promotion.

Additionally: the dataset remains **UNQUALIFIED** exploratory; confirmatory
scientific promotion is **impossible** regardless of exploratory outcome
(DR-007).

---

## 14. Relationship to I01 and I02

| Investigation | Object | Exploratory outcome |
|---------------|--------|---------------------|
| **I01** | Apparent future homogeneity under G0 | Original broad hypothesis **not recommended for confirmation**; regime-conditional phenomenon identified (not SCI-FAIL) |
| **I02** | Incremental predictive value of multivariate state vs volatility controls | **EXPL-ABSENT** (CLOSED) |
| **I03** | Upstream **structural recurrence** of G0 itself | **EXPL-INCONCLUSIVE** (CLOSED) |

Progression of the research question (synthesis only — **not** a joint
statistical claim):

```text
future homogeneity (I01)
  → incremental prediction (I02)
  → structural recurrence (I03)
```

Do **not** combine I01+I02+I03 into a stronger claim than each supports.

---

## 15. Status of G0 after I03

**Do not** declare G0 scientifically falsified.  
**Do not** declare G0 validated.

```text
G0 remains a valid BASELINE / REFERENCE GEOMETRY.

I03 did not provide the preregistered coherent evidence required to promote
the hypothesis that G0 contains stable local temporal recurrence beyond the
tested controls.

G0 = BASELINE / REFERENCE GEOMETRY — NOT PROMOTED STRUCTURAL MODEL
```

---

## 16. Status of N3

```text
N3 / IAAFT as preregistered in I03:
INVALID FOR I03 RUN2
```

This does **not** automatically prove IAAFT is fundamentally unusable in
all settings. Cause diagnosis and replacement nulls are **out of scope**
here (see Open Questions).

---

## 17. Open questions (questions only — not answers)

1. Why did IAAFT fail to converge for **999/999** RUN2 surrogates under frozen
   \(I_{\max}=100\), \(\varepsilon=10^{-8}\)?
2. Is that failure specific to the frozen N3 implementation/criterion, to
   dataset characteristics (SPY length / spectral properties), or to
   algorithmic configuration?
3. Would another **independently preregistered** adversarial null be more
   appropriate for a **new** investigation?
4. Is recurrence under G0 regime-dependent rather than globally stable across
   the three frozen blocks?
5. Is \(L_2\) on raw causally standardized return windows the appropriate
   topology?
6. Would a different representation/metric expose more stable structure?

These are **not** a roadmap and **not** an authorization to start I04 / E02 /
N5.

---

## 18. Governance closure block

```text
INVESTIGATION: I03 — Classical Geometric Recurrence
STATUS: CLOSED
EVIDENCE LEVEL: EXPLORATORY / UNQUALIFIED
FINAL STRUCTURAL VERDICT: INCONCLUSIVE (NEG_E)
EXPLORATORY CLASSIFICATION: EXPL-INCONCLUSIVE
SCI: NO PROMOTION
PRED: NO PROMOTION
ECON: NO PROMOTION
E02: NOT AUTHORIZED / NOT EXECUTED
G0: BASELINE / NOT PROMOTED
N3: INVALID UNDER I03 RUN2 CONTRACT
```

No active I03 experiment remains open after this document.

---

## 19. Audit trail / key commits

| Milestone | Commit / pointer |
|-----------|------------------|
| I03-PRE framing | `91d6c9d` |
| Design open | `15ab106` |
| C1–C10 freeze | `c6a26a3` |
| Prereg v0.1 | `0ff457a` |
| L1 implementation | `fb23c06` / `570246c` |
| L2 PASS | `684c933` / `0dda827` |
| HAT PASS | `f61eefe` / `32583aa` |
| E01 authorization | `0a50a2f` |
| Amendment B | `4e7bec1` / `ab9fa82` |
| M1 canonical SPY | `8a19b47` / `055b6be` |
| M2R transport LF fix | `6dc8adb` |
| Cloud RUN1 abort | `dfa3bd9` (reported in PERF-01 Phase 0; no science) |
| PERF-01 Phase 0 | `c304d7b` |
| PERF-01 Phase 1A | `109faaa` / `651e9ee` |
| PERF-01 Phase 1B | `f7bcb67` / `0592ee8` |
| PERF-01 Phase 1C | `3b73be0` / `bb5d1ee` |
| Final local HAT | `38ce793` |
| CLI wiring | `4300eb9` / `1dfdae6` |
| E01 RUN2 result | `b4ea158` |
| This closure | *(this commit)* |

---

## 20. Documentation consistency / tests

- Production code: **unchanged** in this closure task.
- Post-RUN2 regressions already recorded at result commit: `tests/i03` →
  **114 passed** (`b4ea158` evidence chain).
- Closure task: documentation / registry updates only.

---

## Document control

| Field | Value |
|-------|-------|
| Type | Scientific / governance closure |
| Supersedes status | `E01 AUTHORIZED / NOT YET OBSERVED` (README historical) |
| Next investigation | **Human decision required** — not opened here |
