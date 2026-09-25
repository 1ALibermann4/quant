# I03 — Design v0.1 (Intrinsic Recurrence of G0)

> **STATUS :** **DESIGN** — not executable preregistration  
> **Authority class :** RESEARCH  
> **Protocol :** QDP v0.1 · DR-007  
> **D1–D8 :** [I03-D1-D8-FREEZE.md](I03-D1-D8-FREEZE.md) — **HUMAN-FROZEN**  
> **Pre-framing :** [I03-pre decision dossier](../I03-pre/I03-INTRINSIC-RECURRENCE-DECISION-v0.1.md)  
>
> ```text
> I03 STATUS = DESIGN
> NO MARKET DATA USED
> NO EXPERIMENT RUN
> NO FUTURE TARGET
> NO NUMERICAL GATE MINED
> NO SCI / PRED / ECON CLAIM
> NO BEST-k
> NO POST-HOC PERIODS
> ```

**Label convention:** PROJECT FACT · MATHEMATICAL FACT · LITERATURE PRACTICE ·
INTERPRETATION · HUMAN DECISION REQUIRED · RECOMMENDED ON METHODOLOGICAL GROUNDS.

---

## 0. Frozen inputs (do not reopen)

| Item | Value |
|------|-------|
| G0 | \(W_X=20\), \(M=252\), causal std, \(d_0=\|\cdot\|_2\) |
| D1 | R3 temporal recurrence (primary) |
| D2 | S2 temporal stability (primary) |
| D3 | Multi-scale \(\mathcal{K}\); no inherit \(k=50\) as truth; no best-\(k\) |
| D4 | \(\tau\ge W_X=20\); not \(\tau\ge M\); no ACF mining |
| D5 | Primary null **N4**; adversarial **N3**; recipes open (C3/C4) |
| D6 | Concentration = validity diagnostic; degenerate → INCONCLUSIVE |
| D7 | Cross-period in primary PASS; no 2008/2009/2020-constructed periods |
| D8 | PASS = structure only |

**Accepted DESIGN question**

Under fixed causal G0 and mandatory temporal exclusion \(|t-s|\ge W_X\), does
the market-state trajectory exhibit nontrivial local temporal recurrence that
is stable across time and neighborhood scales, beyond a preregistered
volatility-preserving null and under an adversarial linear/spectral-preserving
null, without using future-return information?

---

## 1. Design goals for v0.1

Resolve remaining contracts **C1–C10** to the point where humans can freeze
them in one pass. Propose options, consequences, DoF, methodological lean —
**without** inspecting market data and **without** writing an executable
prereg until humans freeze remaining choices.

---

## C1 — Operational estimand for R3 temporal recurrence

### Scientific target (frozen concept)

After mandatory separation \(|t-s|\ge\tau\) with \(\tau=W_X\), the trajectory
re-enters previously visited **local regions** of G0 state space.

### What “local region” means — options

| Option | Definition of local region around past state \(X_s\) | Recurrence event at \(t>s+\tau-1\) (sketch) |
|--------|------------------------------------------------------|-----------------------------------------------|
| **C1-A** | \(k\)-NN ball dual: membership in \(N_k^{\tau}(s)\) or \(t\in N_k^{\tau}\) of historical states | Count / rate of τ-separated revisits into \(k\)-neighborhoods |
| **C1-B** | ε-ball \(\{x:d_0(x,X_s)<\varepsilon\}\) | Classical recurrence rate / return times (Eckmann–Ruelle / RQA-style) |
| **C1-C** | Hybrid: primary recurrence rate via ε **linked** to empirical distance quantiles **frozen without outcome fishing** (e.g. contractual quantile rule on past-only distances under τ) | Bridges radius and density |

### Estimand candidates (given a region doctrine)

| ID | Estimand sketch | Pros | Cons / DoF |
|----|-----------------|------|------------|
| **E-RR** | Recurrence rate: fraction of admissible pairs \((t,s)\) with \(d_0(X_t,X_s)<\varepsilon\) (or kNN-membership) and \(|t-s|\ge\tau\) | Standard; null-comparable | ε or \(k\) DoF |
| **E-MRT** | Mean / distributional summary of recurrence times (first return ≥τ into region of \(X_t\)) | Dynamical semantics strong | Censoring; heavy tails; harder gates |
| **E-COND** | Conditional revisit rate given “occupied” regions (density-normalized) | Partly mitigates empty-space artifacts | Extra normalization DoF |

### Coupling to D3

**MATHEMATICAL FACT.** If local regions are \(k\)-NN-defined (C1-A), then
multi-scale \(\mathcal{K}\) **is** the scale set of the primary estimand.
If ε-balls (C1-B), multi-scale may mean a set \(\mathcal{E}\) of radii (or
quantile levels), and \(\mathcal{K}\) becomes secondary/diagnostic — but D3
froze a **neighborhood-scale** set \(\mathcal{K}\), which linguistically
favors kNN-type regions unless humans redefine “neighborhood scale” as ε-scale.

**INTERPRETATION.** D3’s wording (“neighborhood-scale set \(\mathcal{K}\)”)
aligns most cleanly with **C1-A** (or C1-C with \(k\in\mathcal{K}\)).

| Decision | Options | Lean |
|----------|---------|------|
| Region + primary estimand | C1-A + E-RR · C1-B + E-RR · C1-A + E-MRT | **RECOMMENDED: C1-A + E-RR** (rate of τ-separated kNN-revisits), with E-MRT as optional secondary (C10) |

**HUMAN DECISION REQUIRED — HD-C1:** choose C1-A / C1-B / C1-C and primary
functional (E-RR vs E-MRT).

**Numerical thresholds / ε absolute values:** not frozen; if C1-B/C chosen,
quantile rule must be contractual and past-only (**no** outcome mining).

---

## C2 — Multi-scale neighborhood doctrine \(\mathcal{K}\)

### Frozen rules (D3)

- Small preregistered set \(\mathcal{K}\)
- No best-\(k\)
- No result-driven scale choice
- Scale disagreement explicitly interpreted
- Scale-local structure ≠ silent global PASS

### Candidate sets (illustrative — **not mined**)

| Option | \(\mathcal{K}\) | Rationale | Risk |
|--------|-----------------|-----------|------|
| **C2-A** | \(\{10,25,50\}\) | Spans local→I01/I02-historical scale without sanctifying 50 alone | Still includes 50 — continuity vs PRED object |
| **C2-B** | \(\{5,15,40\}\) | Avoids 50 entirely; stresses finer scales | Weaker continuity with I01/I02 neighborhoods |
| **C2-C** | \(\{8,20,50\}\) | Near-\(W_X\) mid scale + poles | Midpoint story may be over-interpreted |

### Aggregation / disagreement semantics (must preregister)

| Option | Global PASS requires | Disagreement handling |
|--------|----------------------|------------------------|
| **C2-Agg-1** | Excess recurrence vs primary null at **all** \(k\in\mathcal{K}\) **and** cross-period (strict) | Any scale fail → not PASS (FAIL or INCONCLUSIVE per gate doc) |
| **C2-Agg-2** | Excess at **≥2** scales including both a “small” and “large” member (define partition of \(\mathcal{K}\)) | Single-scale-only → not global PASS; report MS-LOCAL |
| **C2-Agg-3** | Primary scale designated *a priori* + others robustness only | Conflicts with “no silent single-scale PASS” unless primary is declared and non-selected from data |

**RECOMMENDED ON METHODOLOGICAL GROUNDS:** **C2-A** or **C2-B** for the set;
**C2-Agg-1** or **C2-Agg-2** for reading (prefer **C2-Agg-2** if power
concern dominates; **C2-Agg-1** if claim strength dominates). Avoid C2-Agg-3
unless humans explicitly want a declared primary \(k\).

**HUMAN DECISION REQUIRED — HD-C2:** choose \(\mathcal{K}\) and aggregation
rule. **Do not** pick by running data.

---

## C3 — Exact N4 volatility-preserving surrogate

### Scientific role (frozen)

Destroy temporal **state-path** structure in \(X\) beyond what is implied by
volatility clustering / heteroskedastic magnitude, while preserving a declared
vol nuisance — the main competitor after I01.

### Recipe options (conceptual algorithms)

| Option | Generator (sketch) | Preserves | Destroys | Fitted qty | Causal risk | DoF |
|--------|-------------------|-----------|----------|------------|-------------|-----|
| **N4-A** | Estimate causal local scale \(\hat\sigma_t\) (e.g. from same \(M\) or \(W_{RV}\) contract); form \(z_t=r_t/\hat\sigma_t\); **permute** \(\{z_t\}\); rebuild \(r^\*\) and recompute causal \(X^\*\) | Vol skeleton \(\hat\sigma\) path (as defined) | Ordering of standardized shocks; most state sequencing | \(\hat\sigma\) definition | Use **causal** \(\hat\sigma_t\) only | σ-window, permute vs block-permute residuals |
| **N4-B** | Fit a **preregistered** univariate vol model (e.g. GARCH(1,1) class) on returns with frozen estimation rule; shuffle standardized residuals; simulate \(r^\*\) | Model-implied conditional vol | Residual sequence beyond model | Model params | Full-sample fit vs expanding fit | Model order, estimation window — **high** |
| **N4-C** | Preserve rolling realized-vol path; reshuffle return **signs** / ranks inside vol bins | Coarse vol regime occupancy | Fine path geometry | Binning | Bin edges contractual | Bin DoF — high |

### Degeneracy conditions (must declare)

- \(\hat\sigma_t=0\) / undefined → skip policy aligned with G0
- Residual sequence too short after exclusions
- Vol estimate identical constant → N4 collapses toward N1 (flag INCONCLUSIVE / INVALID null)

### Reproducibility requirements (design mandate)

- Seed schedule for surrogate ensemble
- Exact formula for \(\hat\sigma_t\) or model
- Whether surrogates rebuild \(X\) with **identical** causal \(M\) contract
- Number of surrogates \(B_N\) (numerical later)

**RECOMMENDED ON METHODOLOGICAL GROUNDS:** **N4-A** (causal local-scale +
shuffle standardized innovations) — fewer parametric DoF than GARCH-class
N4-B; clearer “preserve vol path, destroy state order” story; closer to G0’s
existing causal scale objects. Prefer **i.i.d. shuffle of \(z\)** as primary
N4; optional block-shuffle of \(z\) as robustness only if humans approve
(extra DoF).

**HUMAN DECISION REQUIRED — HD-C3:** N4-A / N4-B / N4-C (+ residual shuffle
i.i.d. vs block).

---

## C4 — Exact N3 linear/spectral-preserving surrogate

### Scientific role (frozen)

Adversarial null: apparent recurrence explained by **linear correlation /
spectral** structure rather than nonlinear state revisit.

### Recipe options

| Option | Generator | Preserves | Destroys | Notes |
|--------|-----------|-----------|----------|-------|
| **N3-A** | Fourier phase randomization (FT surrogates) | Power spectrum (linear AC structure for Gaussian) | Phase relations / nonlinear recurrence | Classic Theiler et al.; weak on marginals |
| **N3-B** | IAAFT (Schreiber–Schmitz) | Spectrum **and** amplitude marginal | Nonlinear temporal structure beyond that | Stronger / standard for nonlinear tests |
| **N3-C** | AAFT | Approx. spectrum + marginal | Similar, less exact than IAAFT | Usually dominated by N3-B |

**LITERATURE PRACTICE.** IAAFT is the usual upgrade when marginals matter.

**RECOMMENDED ON METHODOLOGICAL GROUNDS:** **N3-B (IAAFT)** on the **return**
series, then rebuild causal \(X^\*\) under G0 — so the null lives at the same
object level as N4. Apply the **same** \(\tau\) and estimand pipeline.

**Caveat (F9):** IAAFT can be “strong”; combined with N4 primacy, PASS is
demanding — acceptable if semantics (C9) are explicit.

**HUMAN DECISION REQUIRED — HD-C4:** N3-A vs N3-B (recommend B).

---

## C5 — Temporal / cross-period segmentation doctrine

### Frozen constraints (D7)

- Cross-period stability ∈ primary PASS
- One episode insufficient
- **Forbidden** to define periods around 2008, 2009, 2020, or other
  already-known favorable episodes
- Segmentation preregistered; time-index only

### Options

| Option | Segmentation | Cross-period claim | Pros | Cons |
|--------|--------------|--------------------|------|------|
| **C5-A** | \(P\) contiguous equal-length blocks in time order (e.g. \(P=3\) or \(4\)) | Recurrence excess must hold in **each** block vs nulls fit/applied per doctrine | Simple; no calendar storytelling | Block edges arbitrary; unequal market eras lumped |
| **C5-B** | Calendar decades / fixed calendar partitions **chosen without crisis labels** (e.g. 1990–99, 2000–09, …) | Same per-partition excess | Interpretable | 2000–09 **contains** 2008 — allowed as calendar block, but must **not** be selected *because* of 2008; still contamination-adjacent |
| **C5-C** | Odd/even index split or 2-fold contiguous halves | Transport: structure on fold A predicts fold B neighbor/recurrence relations | Strong S2 | Coarse; dependence across folds |
| **C5-D** | Require dual: within-block recurrence **and** cross-block preservation score | Strongest stability | More INCONCLUSIVE risk; extra estimand |

**Contamination note.** Calendar blocks that *happen* to include crises are
not the same as **constructing** a “crisis period.” D7 forbids the latter.
C5-B remains legally calendar-based but is **psychologically** contaminated;
prefer C5-A or C5-C if humans want maximal distance from I01 episode memory.

**RECOMMENDED ON METHODOLOGICAL GROUNDS:** **C5-A** with small fixed \(P\)
(e.g. 3) declared pre-experiment, plus explicit rule: PASS needs excess
recurrence in **all** blocks (or all-but-one with preregistered INCONCLUSIVE
if exactly one fails — humans choose strictness). Avoid crisis-named periods.

**HUMAN DECISION REQUIRED — HD-C5:** C5-A/B/C/D, value of \(P\) or fold rule,
and whether “all blocks” vs “all-but-one” for PASS.

---

## C6 — Distance-concentration / locality validity diagnostic

### Frozen role (D6)

Prerequisite for interpreting G0 neighborhoods. Degeneracy → **INCONCLUSIVE**,
not automatic FAIL. Not the primary recurrence estimand.

### Diagnostic options

| Option | Quantity (past-only, τ-respecting) | Degeneracy intuition |
|--------|-------------------------------------|----------------------|
| **C6-A** | Relative NN contrast among admissible pairs: e.g. \((\bar d_{(k)}-\bar d_{(1)})/\bar d_{(1)}\) or first-vs-\(k\) ratio | Contrast ≈ 0 → ranks uninformative |
| **C6-B** | Ratio \(\mathbb{E}[d_{\mathrm{NN}}]/\mathbb{E}[d_{\mathrm{random}}]\) under τ | NN not closer than random → locality vacuous |
| **C6-C** | Hubness / skewness of in-degree in kNN graph | Pathological locality |
| **C6-D** | Bundle C6-A + C6-B (OR or AND degeneracy rule) | Safer coverage |

**RECOMMENDED ON METHODOLOGICAL GROUNDS:** **C6-D** with a **preregistered**
boolean degeneracy rule (numerical cutoffs later, not data-mined for PASS
optimization — use only contractual constants or literature defaults declared
blind). Apply **before** interpreting primary estimands; if triggered →
INCONCLUSIVE for the affected scale/segment (or globally — HD).

**HUMAN DECISION REQUIRED — HD-C6:** which diagnostic(s); per-scale vs global
INCONCLUSIVE scope; whether numerical cutoffs are deferred to a later freeze
pass (acceptable).

---

## C7 — Inference / uncertainty procedure

### Requirements

- Compare observed estimand(s) to surrogate ensembles under N4 and N3
- Respect time dependence (do not pretend i.i.d. queries without care)
- Multiplicity: scales \(\mathcal{K}\), segments, two nulls
- Reproducible seeds

### Options

| Option | Procedure | Pros | Cons |
|--------|-----------|------|------|
| **C7-A** | Percentile / rank test vs \(B_N\) surrogates per (scale × segment × null) | Standard surrogate testing | Multiplicity |
| **C7-B** | C7-A + preregistered Holm / Bonferroni across \(\mathcal{K}\times\) segments for primary null only | Controls FWER | Conservative |
| **C7-C** | Hierarchical: first N4 battery; N3 battery separately; combine via C9 | Matches dual-null doctrine | Needs C9 clarity |
| **C7-D** | Studentize using block bootstrap **on top of** surrogates | Extra dependence layer | Double complexity; possible over-conditioning |

**RECOMMENDED ON METHODOLOGICAL GROUNDS:** **C7-C** implemented as **C7-A**
per cell, with **preregistered multiplicity policy** (lean **C7-B** light —
correct across \(\mathcal{K}\) within segment, then require segment rule from
C5). Avoid C7-D unless dependence diagnostics demand it.

**Numerical \(B_N\), α:** unfrozen (propose later without data mining; e.g.
conventional α=0.05 / \(B_N\ge 999\) as *candidates for human freeze*, not
evidence-based tuning).

**HUMAN DECISION REQUIRED — HD-C7:** C7-A/B/C structure; multiplicity scope;
whether α/\(B_N\) freeze now or in prereg v0.1.

---

## C8 — PASS / FAIL / INCONCLUSIVE gates (semantics + structure)

### Semantics (align D8)

| Verdict | Meaning |
|---------|---------|
| **PASS** | Nontrivial τ-separated temporal recurrence of G0, stable across preregistered scales and periods, beyond **N4**, and satisfying adversarial **N3** semantics (C9), with validity diagnostics OK — **structure only** |
| **FAIL** | Primary structural property not demonstrated (e.g. fails N4 under agreed reading) |
| **INCONCLUSIVE** | Validity degeneracy (C6); null/implementation defect; irreconcilable null disagreement under C9; insufficient effective sample; scale/segment pattern outside preregistered readable cases |

### Gate structure options (numerical cuts later)

| Option | PASS skeleton |
|--------|----------------|
| **C8-A** | Validity OK ∧ (excess vs N4 at required scales/segments) ∧ (C9 N3 condition) |
| **C8-B** | Same but N3 only diagnostic (conflicts with frozen “adversarial” role — **not recommended**) |
| **C8-C** | Two-tier: STRUCT-SUPPORT vs N4, ADV-SUPPORT vs N3; PASS = both | Matches dual-null spirit |

**RECOMMENDED:** **C8-C** combined with **C8-A** boolean — i.e. explicit
two-tier reporting, PASS only if both tiers clear under C9.

**HUMAN DECISION REQUIRED — HD-C8:** confirm C8-C; defer numerical percentiles
to prereg freeze.

---

## C9 — Null-disagreement semantics

### Frozen constraint

Do **not** choose N3 vs N4 from results. Survival of one ≠ automatic PASS.

### Options

| Code | Pattern | Preregistered reading |
|------|---------|------------------------|
| **ND-1** | Beats N4 and beats N3 | Eligible for PASS (if scales/segments/validity OK) |
| **ND-2** | Beats N4, fails N3 | **Not PASS.** Interpretation: structure beyond vol but compatible with linear/spectral nuisance → **FAIL** or **INCONCLUSIVE-ADV** (humans pick label) |
| **ND-3** | Fails N4, beats N3 | **Not PASS.** Vol nuisance not cleared → **FAIL** (primary null is N4) |
| **ND-4** | Fails both | **FAIL** |
| **ND-5** | Mixed across scales/segments | Apply C2/C5 aggregation first; if aggregation undefined → **INCONCLUSIVE** |

**RECOMMENDED ON METHODOLOGICAL GROUNDS:**

- PASS only on **ND-1** (+ C2/C5/C6/C8).
- **ND-3** and **ND-4** → FAIL.
- **ND-2** → **FAIL** if the scientific claim is “beyond vol *and* not merely
  linear spectral,” **or** **INCONCLUSIVE-ADV** if humans want a distinct
  label acknowledging “vol-cleared but spectrally compatible.”  
  Lean: **FAIL** for global PASS eligibility, with mandatory reporting that
  N4 was cleared — avoids soft PASS creep.

**HUMAN DECISION REQUIRED — HD-C9:** ND-2 label = FAIL vs INCONCLUSIVE-ADV.

---

## C10 — Secondary diagnostics (optional, non-primary)

Allowed only as **diagnostics**, not extra primary claims (D1/D2).

| Diagnostic | Maps to | Purpose | Risk if misused |
|------------|---------|---------|-----------------|
| R1 NN-overlap summaries | R1 | Operational sanity vs R3 rate | Quiet promotion to primary |
| Neighborhood composition (R2-lite) | R2 | See if revisits are lone matches | Same |
| S1 small perturbation of \(X_t\) | S1 | Locality sharpness | F12 if magnitude free |
| S5 rank stability | S5 | Ordinal robustness | Soft second primary |
| Vol-level stratified recurrence | F2 audit | Check residual vol channel under N4 | Post-hoc strata fishing |

**RECOMMENDED:** Include **minimal** set: (i) validity already in C6;
(ii) optional R1 rate alongside E-RR for interpretability; (iii) **forbid**
S1/S5 in v0.1 primary design unless humans reopen D2. Any stratification must
be preregistered and non-crisis-targeted.

**HUMAN DECISION REQUIRED — HD-C10:** accept minimal diagnostics vs add S1/S5
(requires explicit approval).

---

## 2. Contract summary table (C1–C10)

| ID | Topic | Frozen already? | Options on table | Methodological lean | Human ID |
|----|-------|-----------------|------------------|---------------------|----------|
| C1 | R3 estimand | Concept only | C1-A/B/C × E-RR/E-MRT | C1-A + E-RR | HD-C1 |
| C2 | \(\mathcal{K}\) + aggregation | Rules only | C2-A/B/C × Agg-1/2/3 | C2-A or B; Agg-2 (or 1) | HD-C2 |
| C3 | N4 recipe | Family only | N4-A/B/C | N4-A | HD-C3 |
| C4 | N3 recipe | Family only | N3-A/B/C | N3-B IAAFT | HD-C4 |
| C5 | Segmentation | Constraints only | C5-A/B/C/D | C5-A | HD-C5 |
| C6 | Concentration | Role only | C6-A/B/C/D | C6-D | HD-C6 |
| C7 | Inference | — | C7-A/B/C/D | C7-C (+ light B) | HD-C7 |
| C8 | Gates | Semantics sketch | C8-A/B/C | C8-C | HD-C8 |
| C9 | Null disagreement | Constraint | ND-2 label | PASS=ND-1 only; ND-2=FAIL lean | HD-C9 |
| C10 | Secondaries | D1/D2 limits | minimal vs +S1/S5 | minimal | HD-C10 |

---

## 3. Remaining researcher DoF after recommended leans

Even if all leans are accepted, still unfrozen until prereg numbers:

- Exact \(\mathcal{K}\) members if choosing between C2-A/B
- \(P\) for C5-A
- \(B_N\), α, percentile rule
- Exact \(\hat\sigma\) window inside N4-A (candidate: align \(W_{RV}=20\) or \(M=252\) — **human**)
- IAAFT iteration count / convergence tolerance
- Degeneracy numerical constants for C6
- Effective-sample minimum after τ

These must be frozen **pre-experiment** without outcome fishing.

---

## 4. Identifiability reminder (unchanged)

Fixed G0 tests **E1 vs E4/E5-style** stories under declared nulls. It does
**not** separate E2 (bad L2) from E3 (bad \(X\)). FAIL ≠ “no market geometry.”
PASS ≠ PRED (D8).

---

## 5. Path to executable preregistration

```text
Human freeze HD-C1 … HD-C10
    →
I03-PREREG-v0.1 (executable contract)
    →
implementation + L2/HAT
    →
E01 EXPLORATORY or CONFIRMATORY path per DR-007 (separate decision)
```

This DESIGN document is **not** that prereg.

---

## 6. References

See [references.md](references.md). Key method anchors: Theiler surrogates;
Schreiber–Schmitz IAAFT; Eckmann–Ruelle recurrence plots; Marwan RQA; Beyer /
Aggarwal distance concentration; I03-pre dossier; geometry review.

---

## Document control

| Field | Value |
|-------|-------|
| ID | I03-DESIGN-v0.1 |
| Status | DESIGN |
| Executable? | **No** |
| Alters D1–D8? | **No** |
