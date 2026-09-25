# I02 — Preregistration & readiness contract

> **STATUS :** PREREGISTRATION COMPLETE (document) — **not** I02 OPEN
> **Authority class :** RESEARCH / PROTOCOL (normative for I02 if opened)
> **Protocol :** QDP v0.1
> **Design readiness :** R2 — DESIGN CLOSED @ `260988b` (pin `32b60c4`)
> **Prereg readiness :** **P2** — may be opened by explicit human decision
> **I02 :** NOT OPENED
> **NO EXPERIMENT AUTHORIZED** until OPEN + implementation HAT PASS
>
> **Parent design history :** [I02-hypothesis-draft.md](I02-hypothesis-draft.md)
> **Governance :** DR-007, DR-008, C02 v1.1, closure gates, MS-1…MS-4

This file is the **executable scientific contract**. It does **not**
redesign I02. Rationale and adversarial history live in the draft.
Cross-references only.

```text
CORE DESIGN = FROZEN
NO PARAMETER SEARCH
NO DATA ANALYSIS IN THIS DOCUMENT
```

---

## 0. Frozen design (normative)

| Object | Value |
|--------|-------|
| \(W_X\) | 20 |
| \(W_{RV}\) | 20 |
| \(\mathcal{M}_Z\) | \(\{3,12,21\}\) — **no primary scale** |
| \(h\) | 10 |
| \(k\) | 50 |
| stride | 1 |
| Target | \(V_{t,10}=\sqrt{\frac1{10}\sum_{j=1}^{10}r_{t+j}^{2}}\) |
| Forecast | \(\widehat{\mathbb{P}}_t^{R}=\frac1{50}\sum_{i=1}^{50}\delta_{V_{s_i,10}}\) |
| Pool | common \(A_t\) for \(X,S_1,S_2,S_3\) |
| Hard availability | \(s+10\le t\) |
| Ties | \((\mathrm{distance}\uparrow,\,s\uparrow)\), \(\lvert N\rvert=50\) |
| Weights | uniform \(1/50\) |
| Early history | skip if \(\lvert A_t\rvert<50\) |
| Representations | \(X\), \(S_1\), \(S_2\), \(S_3\) (as accepted in draft) |
| Score | CRPS (lower better) |
| Primary estimand | \(R_t^{(S)}=\dfrac{\operatorname{CRPS}_S(t)-\operatorname{CRPS}_X(t)}{\operatorname{CRPS}_S(t)}\) |
| Secondary | \(D_t^{(S)}=\operatorname{CRPS}_S(t)-\operatorname{CRPS}_X(t)\) — diagnostic only |
| \(\operatorname{CRPS}_S=0\) | structural **skip** (no \(\varepsilon\)) |
| State | \(L_t=\log(RV_t)\), \(\Delta L_u=L_u-L_{u-1}\) |
| | \(Z_t^{(m)}=\mathrm{Std}_{\mathrm{pop}}(\Delta L_{t-m+2},\ldots,\Delta L_t)\), \(m\in\{3,12,21\}\) |
| Canonical state | \(\mathbf{Z}_t=(Z_t^{(3)},Z_t^{(12)},Z_t^{(21)})\) |
| \(RV=0\) | structural **skip** for affected \(Z^{(m)}\) / analyses |
| \(Z\) role | query indexing / analysis only — **never** filters \(A_t\), neighbors, \(k\), weights, target, forecast |
| Association | Spearman ; **two-sided** ; **non-causal** |
| Inference | moving / block bootstrap |
| Primary \(b\) | \(b^\star=40\) |
| Robustness \(b\) | \(\{20,40,80\}\) — report **all** ; **no best-\(p\)** |
| Scales | report **all** \(m\) ; **no best-scale** |

Duplicate forecast atoms: multiplicity preserved.
Design sources: draft §14I–§14M.

---

## 1. Exact preregistered hypothesis

### 1.1 Scientific claim

**H1-I02 (preregistered, two-sided).**  
Under the frozen design above, the comparator-relative proper-score
incremental predictive value of the multivariate past window \(X\)
relative to each pre-registered simple summary
\(S\in\{S_1,S_2,S_3\}\),

\[
R_t^{(S)}
=
1-\frac{\operatorname{CRPS}_X(t)}{\operatorname{CRPS}_S(t)}
\quad(\operatorname{CRPS}_S(t)>0),
\]

exhibits a **systematic monotone association** with volatility-regime
instability \(Z_t^{(m)}\) for \(m\in\{3,12,21\}\), in the sense of a
non-null population Spearman association on the stride-1 query
schedule (non-skipped dates).

**State-dependent incremental predictive value** means: variation of
\(R_t^{(S)}\) that is systematically related to \(Z_t^{(m)}\), not
merely a non-zero unconditional mean of \(R\) or \(D\).

### 1.2 Null / absence target

**H0-I02.**  
No such systematic monotone associations exist, under the joint
evidence-unit and MS-1…MS-4 interpretation of §2–§4 (including the
case where apparent associations are fragile, concentrated, or
adversarially explained).

### 1.3 Directionality

**Two-sided.** No ex-ante signed prediction is authorized.
E04 must **not** supply direction.

### 1.4 Non-claims

H1-I02 is **not**: Shannon information gain; causality; economic
value; a trading rule; a Market-State Engine; a SCI verdict on I01;
an unconditional claim that \(\mathbb{E}[R]>0\).

---

## 2. Unit of evidence — \(S\times m\)

### 2.1 Full result structure

Primary reported object (per data class / run version):

\[
\hat\rho^{(S,m)}
=
\operatorname{Spearman}\bigl(Z_t^{(m)},\,R_t^{(S)}\bigr)
\]

for all pairs

\[
(S,m)\in\{S_1,S_2,S_3\}\times\{3,12,21\}
\]

with dependence-aware uncertainty under **primary** \(b^\star=40\),
and the **same** grid repeated for diagnostic \(b\in\{20,80\}\)
(full \(\{20,40,80\}\) always shown).

Secondary diagnostics (not primary evidence): \(D_t^{(S)}\);
concentration / effective support; skip rates
(\(\operatorname{CRPS}_S=0\), \(RV=0\), \(\lvert A_t\rvert<50\)).

### 2.2 Forbidden selection

**Prohibited:**

- selecting the best \(S\) ;
- selecting the best \(m\) ;
- selecting the best \(b\) ;
- minimum-\(p\) hunting across the grid ;
- declaring success from **one isolated cell**.

### 2.3 Multiscale taxonomy (MS-1…MS-4)

Applied to the \(m\)-dimension **for each fixed \(S\)**, then
summarized across \(S\):

| Code | Meaning | Protocol consequence |
|------|---------|----------------------|
| **MS-1** | Same qualitative conclusion on **all** \(m\in\mathcal{M}_Z\) | strongest cross-scale support for that \(S\) |
| **MS-2** | Effect localized on a **subset** of scales | allowed pattern ; **≠** promoting that subset to PRIMARY ; ≠ retune |
| **MS-3** | **Opposite** conclusions across scales | ensemble **INCONCLUSIVE** for that \(S\) (no opportunistic vote) |
| **MS-4** | Insufficient / unstable information | do not “rescue” via one scale |

### 2.4 Cross-adversary interpretation

| Pattern | Reading |
|---------|---------|
| Association pattern coherent vs \(S_1,S_2,S_3\) | supports “beyond simple summaries” broadly |
| Only vs \(S_1\), absent vs \(S_2/S_3\) | at most “beyond level (\(RV\))” — **not** full H1 vs richer \(S\) |
| Present vs richer \(S\), absent vs \(S_1\) | atypical ; treat as **INCONCLUSIVE** pending adversary audit |
| Explained by kill criteria (§5) | FAIL or INVALID per kill |

---

## 3. PASS / FAIL / INCONCLUSIVE

### 3.1 Two verdict layers (DR-007)

| Layer | When | Allowed labels |
|-------|------|----------------|
| **Investigation (exploratory)** | `EXPLORATORY` / `UNQUALIFIED` data | `EXPL-SUPPORT` / `EXPL-ABSENT` / `EXPL-INCONCLUSIVE` |
| **Scientific (confirmatory)** | `CONFIRMATORY` C02 path only | `SCI-PASS` / `SCI-FAIL` / `SCI-INCONCLUSIVE` |

Exploratory labels **never** equal SCI-PASS / SCI-FAIL.
Positive exploratory ≠ confirmatory validation.
Negative exploratory ≠ SCI-FAIL of I02.

### 3.2 Necessary ≠ sufficient

**Statistical detectability** (e.g. two-sided uncertainty at \(b^\star=40\)
incompatible with \(\rho=0\) for a cell) is **necessary** for counting
that cell as a detected association, **not sufficient** for PASS.

**Scientifically meaningful predictive structure** additionally
requires the joint rules below.

### 3.3 Confirmatory SCI rules (qualitative-binding; no lone \(p<0.05\))

Evaluate the full \(S\times m\) grid + \(\{20,40,80\}\) + diagnostics.

**SCI-PASS** only if **all** hold:

1. **Detectability:** for **each** of \(S_1,S_2,S_3\), at least one
   \(m\) shows two-sided detectability at \(b^\star=40\) **or** a
   pre-recognized MS-2 localization that is declared in the run
   report without discarding other \(m\) ;
2. **No MS-3** on any \(S\) that is used to claim support ;
3. **Cross-adversary:** pattern is **not** confined to \(S_1\) alone
   (full H1 requires non-null structure vs \(S_2\) and vs \(S_3\) as
   well, under MS taxonomy) ;
4. **Robustness:** qualitative conclusion at \(b^\star=40\) is **not
   reversed** by \(b\in\{20,80\}\) (discordance → not PASS; see
   INCONCLUSIVE) ;
5. **Non-fragility:** no kill criterion in §5 triggers FAIL/INVALID ;
6. **Support:** association not carried by a pathological skip /
   denominator regime or a tiny date subset (§5) ;
7. **No causal language** in the claim.

**SCI-FAIL** if:

- after a valid confirmatory execution, the grid shows **absence**
  of systematic \(Z\leftrightarrow R\) structure under the evidence
  unit (including coherent near-null across \(S\times m\)), **or**
- a kill criterion with consequence FAIL triggers,
- without requiring a single magic \(p\)-threshold as the sole rule.

**SCI-INCONCLUSIVE** if:

- MS-3 / MS-4 dominate ;
- \(b\)-sensitivity reverses the primary qualitative reading ;
- effective support / skips too severe to interpret ;
- implementation or availability integrity is doubtful but not
  proven false (else INVALID) ;
- design executed but information insufficient for PASS or FAIL.

### 3.4 Exploratory investigation rules

Mirror §3.3 with labels `EXPL-*` and **weaker promotional force**:

| Label | Meaning |
|-------|---------|
| `EXPL-SUPPORT` | pattern would meet SCI-PASS *structure* on UNQUALIFIED data — **only** answers “worth confirmatory follow-up?” |
| `EXPL-ABSENT` | pattern would meet SCI-FAIL *structure* |
| `EXPL-INCONCLUSIVE` | otherwise |

No DATA-PASS, SCI-PASS, SCI-FAIL, PRED, ECON, or promotion from
exploratory output (DR-007).

---

## 4. Kill criteria

| ID | Trigger | Consequence |
|----|---------|-------------|
| **K1** | Incremental value of \(X\) reproduced by \(S_1/S_2/S_3\) in the sense that \(R\) association / advantage collapses once \(S\) matching is accounted for as designed | **FAIL** (H2-class) |
| **K2** | Apparent \(Z\leftrightarrow R\) (or \(R\)) support concentrated on very few dates / known crisis clusters such that removing them (predeclared diagnostic, not tuned) nullifies the claim | **FAIL** or **INCONCLUSIVE** if removal rule itself is unstable — default **FAIL** if concentration is the sole carrier |
| **K3** | State relation driven by pathological denominators / skip mass (\(\operatorname{CRPS}_S\approx 0\) neighborhood, extreme \(R\)) rather than forecast content | **INCONCLUSIVE** or **INVALID** if estimand corrupted |
| **K4** | Verdict depends on a single member of a robustness set (§9.16 metrics, or \(b\in\{20,40,80\}\), or single \(m\)) with others contradicting | **INCONCLUSIVE** (MS / robustness) — **not** PASS via best cell |
| **K5** | Leakage / hard-availability violation / \(Z\) entering neighbor selection | **INVALID** |
| **K6** | Hidden post-hoc scale, \(S\), or \(b\) selection | **INVALID** |
| **K7** | Implementation contradiction changing the mathematical contract of \(R\), CRPS, \(Z\), or \(A_t\) | **INVALID** until corrected under change control §8 ; confirmatory status void if already claimed |
| **K8** | Metric/representation artifact (e.g. only under one non-robust chart) under §9.16 doctrine | **INCONCLUSIVE** / non-resistance — no post-hoc metric rescue |

**No post-hoc rescue tuning.** A kill terminates redesign-as-rescue;
a new investigation / new prereg version is required for design
change (class C/D, §8).

---

## 5. Holdout / confirmatory governance (DR-007)

### 5.1 Classes

| Class | Role |
|-------|------|
| `EXPLORATORY` / `UNQUALIFIED` | pipeline, debug, preliminary investigation labels `EXPL-*` only |
| `CONFIRMATORY` | C02-qualified path ; SCI labels only |

No mixing (DR-007 D-3). No silent promotion of SPY/yfinance to
confirmatory (DR-008 / DR-003 L-13 unchanged).

### 5.2 What must be frozen before confirmatory results

Before **observing** confirmatory I02 results:

- this preregistration version (or a bumped version under §8) ;
- confirmatory dataset identity (C02 snapshot) ;
- **holdout / evaluation boundary** (calendar cut or equivalent)
  fixed **without** choosing a favorable historical period ;
- analysis code hash / protocol version ;
- seed policy for bootstrap resampling.

Exact confirmatory calendar cut is **not** required to **OPEN** I02
exploratory, but **is** required before confirmatory execution.

### 5.3 Temporal split principle

Prefer a **predeclared temporal** evaluation policy (or other
instrument / universe split) that does **not** cherry-pick
2008/2009/2020. Post-2022 is **not** a virgin holdout for this
hypothesis family (draft §12) if contaminated by exploratory I01/I02
work on the same series — document contamination status in the run
report.

### 5.4 Exploratory historical data

May be used for **implementation / debugging** and for `EXPL-*`
investigation **only** if labeled `UNQUALIFIED` / `EXPLORATORY`.
Seeing exploratory outcomes **must not** adapt the frozen design
before confirmatory (§8 class C/D).

### 5.5 Modifications after exploratory execution

| Change | Requirement |
|--------|-------------|
| Editorial / bugfix preserving math contract | §8 A/B |
| Any scientific design change | new prereg version **before** confirmatory |
| Adapting design to confirmatory outcomes | **forbidden** (class D) |

---

## 6. Data / C02 requirements

| Goal | Requirements |
|------|----------------|
| **A. OPEN I02** (investigation authorization) | Design R2 ; this preregistration in force ; **explicit human OPEN I02** ; **not** blocked on DR-003 / DR-005 / C02 qualification |
| **B. Exploratory execution** | OPEN I02 ; implementation HAT PASS (§7) ; `UNQUALIFIED` dataset with DR-007 labeling ; no paid acquisition under DR-007 D-6 ; no SCI / DATA-PASS / promotion claims |
| **C. Confirmatory execution / SCI promotion path** | OPEN I02 ; HAT PASS ; **C02** snapshot qualifying path ; **DR-003 D-1 ACCEPTED** ; **DR-005 ACCEPTED** ; holdout frozen (§5.2) ; confirmatory prereg version frozen ; then SCI verdicts (§3.3) |

Qualified confirmatory C02 data is **not** a prerequisite for
**I02 OPEN**. It **is** a prerequisite for confirmatory execution
and any SCI-PASS / promotion claim.

---

## 7. Implementation validation requirements (HAT)

**Define only — do not implement in this review.**

Before the **first scientific run** (exploratory or confirmatory),
the following must PASS as an implementation HAT / test battery:

1. Hard availability \(s+h\le t\) with \(h=10\)
2. Common \(A_t\) across \(X,S_1,S_2,S_3\)
3. \(k=50\) exact ; no adaptive \(k\)
4. Deterministic ties \((\mathrm{dist}\uparrow,s\uparrow)\)
5. Duplicate \(V\) atom multiplicity preserved
6. CRPS empirical identity / ensemble form
7. \(R\) denominator-zero → skip
8. \(Z_t^{(m)}\) indexing (\(m\) levels \(L\), \(m-1\) increments)
9. \(RV=0\) → skip / undefined \(L\) handling
10. Causal \(Z\) (\(\mathcal{F}_t\) only)
11. \(Z\) does not filter neighbors / \(A_t\)
12. stride \(=1\) schedule construction
13. Bootstrap blocks of lengths \(\{20,40,80\}\); primary reporting \(b^\star=40\)
14. Reproducibility : fixed seeds where RNG applies ; artifact hashes

Failure of any item ⇒ **no scientific run**.

---

## 8. Change control

| Class | Meaning | Action |
|-------|---------|--------|
| **A** | Editorial / documentation clarification | doc update ; no verdict invalidation |
| **B** | Implementation correction **preserving** mathematical contract | fix + HAT re-PASS ; prior EXPL/SCI **VOID** if contract was wrong in executed code |
| **C** | Scientific design change (any frozen §0 object, estimand, association, inference family, evidence rules) | **preregistration version bump** ; new OPEN decision if already opened ; prior confirmatory status **invalidated** |
| **D** | Post-result redesign / outcome-driven retune | **forbidden** as continuation ; requires **new investigation** (new ID or major version) and new confirmatory run after new prereg |

Silent researcher degrees of freedom are class C/D violations.

---

## 9. Final readiness

| Code | Status |
|------|--------|
| P0 | Preregistration incomplete |
| P1 | Complete but non-data blocker remains |
| **P2** | **Preregistration complete ; I02 MAY BE OPENED** (human decision) |
| P3 | Implementation may begin |

**Classification for this document :**

\[
\boxed{\texttt{P2}}
\]

**Rationale :** scientific contract is complete and does not redesign
the frozen core ; C02 is correctly **not** required for OPEN ;
implementation HAT is **specified but not built** ⇒ not P3.
Remaining step to open : **explicit human decision OPEN I02**.
After OPEN : implement protocol + HAT ⇒ then exploratory execution
may begin (still NOT confirmatory).

**Not P3 :** “documentation exists” ≠ authorization to run code
before OPEN + HAT PASS.

---

## 10. Blockers

| Blocker | Blocks |
|---------|--------|
| Human decision **OPEN I02** | opening |
| Implementation HAT not yet built / PASS | first scientific run |
| DR-003 D-1 / DR-005 not ACCEPTED | confirmatory acquisition / SCI path only |
| C02 confirmatory snapshot not qualified | confirmatory execution / SCI-PASS only |
| Confirmatory holdout boundary not yet fixed | confirmatory execution only |

**No blocking contradiction** found in the closed core design during
this review.

---

## 11. Confirmations

```text
CORE DESIGN UNCHANGED
NO DATA USED
NO EXPERIMENT RUN
I02 = NOT OPENED
READINESS = P2
```

---

## Document control

| Field | Value |
|-------|-------|
| Preregistration ID | I02-PREREG-v0.1 |
| Design freeze commit | `260988b` |
| Design freeze pin | `32b60c4` |
| Preregistration commit | `344b128` |
| Supersedes | *(none — first preregistration)* |
| Draft history | [I02-hypothesis-draft.md](I02-hypothesis-draft.md) |
