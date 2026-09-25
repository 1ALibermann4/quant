# I02 — Preregistration & readiness contract

> **STATUS :** PREREGISTRATION IN FORCE — **I02 = OPEN**
> **Authority class :** RESEARCH / PROTOCOL (normative for I02)
> **Protocol :** QDP v0.1
> **Design readiness :** R2 — DESIGN CLOSED @ `260988b` (pin `32b60c4`)
> **Prereg ID :** **I02-PREREG-v0.3** (S3-A human decision + executable contract)
> **Prereg readiness :** **P2** at open ; L1 gaps **closed** (§13–§15 / S3-A)
> **I02 :** **OPEN**
> **Scientific run :** NOT AUTHORIZED until HAT PASS
> **Opened at :** `4f6be2a` — **before any I02 implementation**
> **L1 implementation :** `8d05905` ; **L1 patch :** *(this commit)*
>
> **Parent design history :** [I02-hypothesis-draft.md](I02-hypothesis-draft.md)
> **Governance :** DR-007, DR-008, C02 v1.1, closure gates, MS-1…MS-4

This file is the **executable scientific contract**. It does **not**
redesign I02. Rationale and adversarial history live in the draft.
Cross-references only.

```text
I02 = OPEN
CORE DESIGN = FROZEN (R2)
L1 CONTRACT-GAP AMENDMENTS = §13–§16 (pre-experimental)
NO PARAMETER SEARCH FROM DATA
NO MARKET DATA IN THIS DOCUMENT
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
| \(X\) form | I01 causal standardized log-returns ; **\(M=252\)** inherited (§13) |
| \(X\) degenerate \(\hat\sigma_t=0\) | **undefined / skip** — **no** \(\varepsilon_\sigma\) (§13) |
| Target | \(V_{t,10}=\sqrt{\frac1{10}\sum_{j=1}^{10}r_{t+j}^{2}}\) |
| Forecast | \(\widehat{\mathbb{P}}_t^{R}=\frac1{50}\sum_{i=1}^{50}\delta_{V_{s_i,10}}\) |
| Pool | common \(A_t\) for \(X,S_1,S_2,S_3\) |
| Hard availability | \(s+10\le t\) |
| Ties | \((\mathrm{distance}\uparrow,\,s\uparrow)\), \(\lvert N\rvert=50\) |
| Weights | uniform \(1/50\) |
| Early history | skip if \(\lvert A_t\rvert<50\) |
| Representations | \(X\), \(S_1\), \(S_2\), \(S_3\) (as accepted in draft) |
| S3 kNN metric | **S3-A ACCEPTED** (§14) — co-equal ``S3_Q`` / ``S3_phi`` ; no primary |
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
| Inference | non-circular **moving block bootstrap** on paired valid series (§15) |
| Primary \(b\) | \(b^\star=40\) |
| Robustness \(b\) | \(\{20,40,80\}\) — report **all** ; **no best-\(p\)** |
| Bootstrap \(B\) | \(9999\) replicates (§15) |
| Bootstrap seed | \(42\) (§15) |
| Detectability | CI-dual at \(\alpha=0.05\) (§15) — **not** a separate null-world test |
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

**Statistical detectability** (preregistered meaning, §15):

For a cell \((S,m)\), detectability at block length \(b\) means the
two-sided **percentile CI** for Spearman \(\rho^{(S,m)}\) at level
\(\alpha=0.05\), constructed by the frozen non-circular moving block
bootstrap on the paired valid series, **does not contain** \(0\).

This is **CI-dual** inference under stationarity/mixing assumptions
for the paired process. It is **not** a separate null-world procedure
that destroys association while preserving marginal dependence.
See §15.4 for the explicit distinction.

Detectability is **necessary** for counting a cell as a detected
association, **not sufficient** for PASS.

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
| **A. OPEN I02** (investigation authorization) | Design R2 ; this preregistration in force ; **explicit human OPEN I02** ; **not** blocked on DR-003 / DR-005 / C02 qualification. **Status : DONE.** |
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

**Classification at preregistration authorship :**

\[
\boxed{\texttt{P2}}
\]

**Rationale (at authorship) :** scientific contract complete ; C02
correctly **not** required for OPEN ; HAT specified but not built
⇒ not P3.

**Human decision (subsequent) :** **I02 = OPEN** — see §12.
Lifecycle after OPEN :

```text
I02 OPEN
  → IMPLEMENTATION
  → TESTS / HAT
  → EXPLORATORY EXECUTION
  → evaluation under this contract
```

Confirmatory path remains separately gated (§6).

**Not P3 at OPEN :** OPEN authorizes investigation lifecycle ;
scientific runs still require HAT PASS. Implementation code belongs
in **subsequent** commits after this OPEN record.

---

## 10. Blockers

| Blocker | Blocks | Status at OPEN |
|---------|--------|----------------|
| Human decision **OPEN I02** | opening | **CLEARED** |
| Implementation HAT not yet built / PASS | first scientific run | **active** |
| DR-003 D-1 / DR-005 not ACCEPTED | confirmatory path only | active |
| C02 confirmatory snapshot not qualified | confirmatory path only | active |
| Confirmatory holdout boundary not yet fixed | confirmatory path only | active |

**No blocking contradiction** in the closed core design.

---

## 11. Confirmations (at OPEN transition)

```text
I02 = OPEN
CORE DESIGN UNCHANGED
PREREGISTRATION UNCHANGED (lifecycle status only)
NO IMPLEMENTATION YET
NO DATA USED
NO EXPERIMENT RUN
```

---

## 12. OPEN record — human decision

**Decision :** `I02 = OPEN`

**Baseline at decision :** preregistration `344b128` / pin `58a3284` ;
design freeze `260988b` / `32b60c4`.

**Rationale accepted :**

- Core design = R2 — DESIGN CLOSED
- Preregistration readiness = P2
- Core design frozen ; hypothesis, evidence unit, verdicts,
  kill K1–K8, holdout, data/C02 split, HAT requirements,
  change control defined
- No data analysis ; no experiment performed

**OPEN does not mean :** implementation validated ; exploratory or
confirmatory evidence obtained ; SCI promotion ; C02 qualification
complete.

**Next authorized work :** close remaining L1 contract gaps (§13–§16) ;
patch implementation ; L2 contract tests ; then HAT ; then exploratory
execution under DR-007. Confirmatoire remains blocked per §6.

---

## 13. Gap A — \(X\) inheritance (\(M=252\), \(\varepsilon_\sigma\))

**Baseline L1 :** `8d05905` inherited I01 `M=252` and
\(\varepsilon_\sigma=10^{-8}\).

### 13.1 Trace of authority (I01)

Exact I01 definition ([hypothesis.md](../I01/hypothesis.md) §4.2 ;
[configuration.yaml](../I01/configuration.yaml) `state_X` ;
DEC-04) :

\[
\hat\mu_t=\frac1M\sum_{u=t-M+1}^{t}r_u,
\quad
\hat\sigma_t=\sqrt{\frac1{M-1}\sum_{u=t-M+1}^{t}(r_u-\hat\mu_t)^{2}}
\]

\[
\tilde r_u=\frac{r_u-\hat\mu_t}{\hat\sigma_t+\varepsilon},
\quad
X_t=(\tilde r_{t-W+1},\ldots,\tilde r_t),
\quad W=20,\; M=252,\; \varepsilon=10^{-8}.
\]

I02 accepted “\(X\) forme I01 / rendements standardisés” with
\(W_X=20\). That **does** entail the causal inclusive \(\mu/\sigma\)
window of length **\(M=252\)** (no conflict with \(W_X=20\) :
\(M\ge W\)).

### 13.2 Verdict — \(M=252\)

\[
\boxed{M=252\ \texttt{= INHERITED REPRESENTATION CONTRACT}}
\]

**Amendment class :** **A** (clarification of already frozen “forme
I01”) / recorded in §0.

### 13.3 Verdict — \(\varepsilon_\sigma\)

\(\varepsilon\) enters the **denominator for every window**, not only
\(\hat\sigma=0\). For \(\hat\sigma>0\) it is a small but nonzero
alteration of \(X\). For \(\hat\sigma=0\) (constant \(M\)-window) it
is a **regularization** that replaces an undefined standardization
by \((r-\mu)/\varepsilon\).

| Class | Fit |
|-------|-----|
| A — pure numerical guard, no effect on valid non-degenerate windows | **no** (affects all windows) |
| B — part of mathematical representation | yes under I01 ; **not** authorized by I02’s “no ε” doctrine for undefined objects |
| C — undocumented regularization (relative to I02) | **yes** if silently kept |

**Recommendation (accepted in this amendment) :**

- **Do not** inherit \(\varepsilon_\sigma\) into I02.
- If \(\hat\sigma_t>0\) : \(\tilde r_u=(r_u-\hat\mu_t)/\hat\sigma_t\).
- If \(\hat\sigma_t=0\) : \(X_t\) **undefined** → exclude \(t\) from
  queries and from \(A_t\) (reason `X_SIGMA_ZERO` / insufficient
  representation) — **no** ε, clip, or sentinel.

**Amendment class :** **B** (pre-experimental specification
amendment — degenerate-window policy).

### 13.4 Historical gap record

L1 noted inheritance of both \(M\) and \(\varepsilon\). This section
**keeps** that discovery and **closes** it asymmetrically as above.

---

## 14. Gap B — S3 metric / L+form aggregation

### 14.1 Preserved doctrine (unchanged)

\[
S_3=[RV,Q],\quad Q=MA/RV,\quad \phi=\arccos Q
\]

Shape charts (no primary) :

\[
d_Q=\lvert\Delta Q\rvert,
\quad
d_\phi=\lvert\Delta\phi\rvert
\]

Level : \(\delta_{\mathrm{level}}=\lvert\Delta L\rvert\) on \(RV>0\).

### 14.2 Human decision — S3-A `ACCEPTED` (pre-experimental)

**When :** after L1 gap review (`4778842`), **before** market data,
experiment, or HAT.

**Decision :**

\[
\boxed{\texttt{S3-A = ACCEPTED}}
\]

\[
d_{S3,Q}(a,b)
=
\sqrt{(L_a-L_b)^{2}+(Q_a-Q_b)^{2}}
\]

\[
d_{S3,\phi}(a,b)
=
\sqrt{(L_a-L_b)^{2}+(\phi_a-\phi_b)^{2}},
\quad
\phi=\arccos(Q)
\]

**Status labels :**

```text
S3 PRODUCT METRIC = L2
NO PRIMARY SHAPE CHART
```

**Rejected :** S3-C (shape-only) ; S3-B (L1 aggregation) **not retained**.

**Forbidden :** λ weights ; empirical rescaling ; z-scoring ; whitening ;
adaptive coordinate normalization ; post-hoc metric selection.

### 14.3 No-primary governance

Both branches **`S3_Q`** and **`S3_phi`** must be executed and reported.
They are two preregistered coordinate charts of the same S3 adversarial
concept. Material disagreement ⇒ apply metric-disagreement doctrine
⇒ **`INCONCLUSIVE`** where applicable. Never select the favorable branch.

Evidence unit : expand S3 into co-equal charts inside the
\(S\times m\) structure (report both ; no best-chart).

### 14.4 Amendment class

**B** (pre-experimental specification completing OPEN aggregation) with
evidence-unit expansion to named charts (documented, not post-hoc).

### 14.5 Historical gap

v0.2 left S3 as HUMAN DECISION. Closed here by human S3-A.

---

## 15. Gap C — Moving block bootstrap (executable algorithm)

### 15.1 Frozen already

\(b^\star=40\) ; robustness \(\{20,40,80\}\) ; stride 1 ; Spearman ;
two-sided ; no best-\(b\).

### 15.2 Algorithm (ACCEPTED in this amendment)

| Item | Specification |
|------|----------------|
| Type | **Non-circular moving block bootstrap** (overlapping blocks ; Künsch-style) within the accepted block-bootstrap family. **Not** circular MBB. **Not** stationary bootstrap. |
| Source series | For each fixed \((S,m)\): the **time-ordered** sequence of paired valid observations \((Z_{t}^{(m)}, R_{t}^{(S)})\) after structural skips removed (compressed valid series of length \(n\)). Calendar gaps from skips are **not** re-inserted as missingness inside blocks. |
| Block construction | A block start \(j\in\{0,1,\ldots,n-b\}\) yields \((Y_j,\ldots,Y_{j+b-1})\) contiguous in the valid series. |
| Edge handling | **No wrap**. Starts only in \(\{0,\ldots,n-b\}\). |
| Bootstrap sample length | Draw blocks with replacement ; concatenate until length \(\ge n\) ; **truncate** to \(n\). |
| Replicates \(B\) | **\(B=9999\)** fixed ex ante. |
| RNG | NumPy Generator ; **seed \(=42\)** for the primary reported run ; seed recorded in artifacts. No result-dependent seed. |
| Statistic | Spearman \(\rho\) on each replicate (average ranks ; NaN if undefined). |
| Inferential object | Two-sided **percentile CI** at \(\alpha=0.05\): \([\rho^*_{(\alpha/2)},\rho^*_{(1-\alpha/2)}]\) from the \(B\) replicate rhos (after dropping undefined replicates). |
| Detectability | CI at \(b^\star\) does **not** contain \(0\) (§3.2). |
| Degenerate replicates | If \(\rho^*\) undefined (e.g. constant ranks): **drop** that replicate from the percentile sample. If fewer than \(\lceil 0.8 B\rceil\) finite replicates remain: cell inference **`INCONCLUSIVE`**. |
| Insufficient \(n\) | If \(n < b\): cannot form a block → cell inference **`INCONCLUSIVE`** at that \(b\). |
| Robustness | Repeat **identical** algorithm for \(b\in\{20,40,80\}\) ; report all ; **never** select best \(p\)/CI. |

### 15.3 What this is / is not

```text
MBB percentile CI  =  sampling uncertainty for ρ̂
                      under dependence (stationarity/mixing assumptions)

MBB CI excluding 0  =  CI-dual “detectability” (preregistered)

NOT automatically   =  a null construction that breaks association
                      while preserving marginal serial dependence
```

No additional null-world zoo is introduced. If a future protocol
requires a stricter dependence-preserving null test, that is a
**new** preregistered procedure (change-control C), not a silent
reinterpretation of MBB.

### 15.4 Amendment of prior detectability wording

v0.1’s phrase “uncertainty incompatible with \(\rho=0\)” is hereby
**clarified** as the CI-dual rule above — not as an unspecified
\(p\)-value search.

**Amendment class :** **B** (pre-experimental specification
amendment completing Gate 6 / §14M).

### 15.5 Historical gap record

L1 correctly stopped (`IMPLEMENTATION CONTRACT GAP`). Closed here
for algorithm uniqueness ; CI vs null distinction retained
explicitly.

---

## 16. Cross-check, readiness, remaining decisions

### 16.1 Amendment classifications

| Gap | Object | Class | Status |
|-----|--------|-------|--------|
| A | \(M=252\) | **A** | **CLOSED** |
| A | \(\varepsilon_\sigma\) rejected ; \(\hat\sigma=0\) undefined | **B** | **CLOSED** |
| B | S3-A product metrics (human) | **B** | **CLOSED** (v0.3) |
| C | MBB algorithm + CI-dual detectability | **B** | **CLOSED** |

### 16.2 HUMAN DECISIONS REQUIRED

*(none remaining for L1 contract executability)*

### 16.3 Implementation impact

L1 patch must implement §13–§15 and S3-A. Then L2 contract-test
closure, then HAT.

### 16.4 Readiness (after human S3-A + successful L1 patch)

\[
\boxed{\texttt{C2 — CONTRACT + IMPLEMENTATION ALIGNED}}
\]

when tests for X / S3-A / MBB pass. HAT still **not** claimed.

```text
NO MARKET DATA USED
NO EXPERIMENT RUN
HAT NOT STARTED
NO POST-HOC CHOICE
S3-A BEFORE DATA / BEFORE EXPERIMENT / BEFORE HAT
```

---

## Document control

| Field | Value |
|-------|-------|
| Preregistration ID | **I02-PREREG-v0.3** |
| Previous | I02-PREREG-v0.2 @ `4778842` |
| Design freeze commit | `260988b` |
| Design freeze pin | `32b60c4` |
| OPEN commit | `4f6be2a` |
| L1 implementation | `8d05905` |
| Gap-closure (v0.2) | `4778842` |
| S3-A + L1 patch (v0.3) | `b5465b0` |
| Draft history | [I02-hypothesis-draft.md](I02-hypothesis-draft.md) |
