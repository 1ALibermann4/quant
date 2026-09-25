# Geometry Program Review v0.1

> **STATUS :** RESEARCH ARCHITECTURE REVIEW (post-I02 / pre-I03)  
> **Authority class :** RESEARCH — diagnostic only  
> **Protocol :** QDP v0.1 · DR-007 · DR-008  
> **Not :** I03 · experiment · metric selection · PRED / ECON / SCI claim  
>
> ```text
> NO NEW MARKET DATA
> NO NEW EXPERIMENT
> NO I03 OPENED
> NO METRIC SELECTED
> NO RETUNING
> NO PRED / ECON / SCI CLAIM
> ```

**Purpose.** Determine what I01/I02 established about the project’s classical
“market geometry” pipeline; decompose the assumption stack; map where evidence
constrains the research space; identify legitimate mathematical research
families; and propose a small number of discriminating scientific questions
that could *justify* a future I03 — without converting a negative I02 into
post-hoc metric shopping.

**Label convention (mandatory).** Every substantive claim is tagged:

| Tag | Meaning |
|-----|---------|
| **PROJECT FACT** | Stated in repository evidence (I01/I02 docs, artifacts, commits) |
| **EXTERNAL LITERATURE** | External theory / empirical literature; not demonstrated by I01/I02 |
| **INTERPRETATION** | Reasoned reading of project evidence; not a new empirical result |
| **OPEN QUESTION** | Unresolved; not settled by current evidence |

---

## 1. Executive scientific summary

**PROJECT FACT.** I01 (exploratory, CLOSE) observed that Euclidean \(k\)-NN
neighborhoods on a causally standardized recent-return window \(X_t\) produce
more homogeneous future return paths than a naive baseline B0 on the SPY /
yfinance sandbox, largely via volatility amplitude (`H_vol`), with near-absent
shape contribution (`H_shape`). Against a past-volatility control `rv_W`, any
residual advantage was highly concentrated in stress / tail episodes (notably
2008, 2009, 2020). The original broad I01 hypothesis was **not recommended for
confirmation**.

**PROJECT FACT.** I02 (exploratory, CLOSED — EXPL-ABSENT) preregistered a
*different* question: monotone Spearman association between
volatility-regime instability \(Z\) and comparator-relative CRPS incremental
value \(R\) of rich \(X\) vs adversarial summaries \(S\). E01 found **0/12**
detectable cells (MS-1 null), S3_Q / S3_phi agreement, K1–K8 not triggered,
robustness across \(b\in\{20,40,80\}\), and secondary mean \(D<0\) against all
four comparator branches. **No SCI claim.**

**INTERPRETATION.** Together, I01+I02 constrain *claims about average /
monotone predictive increment of the classical \(X+\mathrm{L2}+k\mathrm{NN}\)
chain* on this sandbox. They do **not** identify which layer of the stack
(representation, normalization, metric, locality, recurrence, future
dependence, controls, conditionality) is the failing component. They also do
**not** establish that an alternative geometry would restore predictive
value.

**INTERPRETATION.** The program’s next decision should therefore prefer
*discriminating structural questions* over method shopping. Current evidence
does **not** uniquely select among: testing intrinsic structure of the
*current* geometry before changing it (frame A); isolating representation
(B); isolating metric/geometry (C); or stopping the geometric-neighborhood
branch (D).

---

## 2. Scope and evidence boundary

### 2.1 In scope

- Repository evidence under `research/I01/` and `research/I02/`
- External scholarly literature for §§7–8 only
- Conceptual decomposition and decision support for humans

### 2.2 Out of scope (hard)

Market-data download; E02; I03 opening; backtests; recomputation of I01/I02;
parameter tuning; metric selection; “best geometry”; trading strategies;
PRED / ECON / SCI promotion; implementation changes.

### 2.3 Lineage check vs mandate

| Mandate item | Repository state | Status |
|--------------|------------------|--------|
| I02 E01 evidence `33d063d` | Present (`research(I02): record exploratory E01 results`) | **Match** |
| I02 E01 pin `2b00657` | Present (`docs(I02): correct E01 evidence commit pin`) | **Match** |
| Postmortem `f581416` | Present (`research(I02): review negative E01 result`) | **Match** |
| Closure document | Present: [I02-CLOSURE.md](../I02/I02-CLOSURE.md) @ `68f7f56`; pin `c4ac436` | **Present** (mandate: “if now present”) |

**PROJECT FACT — discrepancy note.** The mandate listed E01 / pin / postmortem
hashes and treated closure as optional. Closure and pin commits
(`68f7f56`, `c4ac436`) exist *after* the mandate’s listed hashes; they do not
contradict E01 evidence. This review treats closure as authoritative for
disposition.

### 2.4 Primary project sources

- I01: [I01-exploratory-synthesis.md](../I01/I01-exploratory-synthesis.md),
  [hypothesis.md](../I01/hypothesis.md), E01–E04 run reports
- I02: [I02-preregistration.md](../I02/I02-preregistration.md) (v0.3),
  [I02-L2-CONTRACT-TEST.md](../I02/I02-L2-CONTRACT-TEST.md),
  [I02-HAT.md](../I02/I02-HAT.md), [I02-E01.md](../I02/I02-E01.md),
  `e01/run1/`, [I02-E01-POSTMORTEM.md](../I02/I02-E01-POSTMORTEM.md),
  [I02-CLOSURE.md](../I02/I02-CLOSURE.md)

---

## 3. Current classical baseline

**PROJECT FACT.** In this project, “classical geometry” means the following
frozen pipeline (I01 objects inherited into I02 where noted), **not** a
generic academic phrase.

```text
returns r_t
    |
    v
X_t = recent standardized return window (W_X)
    |
    v
causal standardization (window M)
    |
    v
Euclidean L2 distance on X
    |
    v
historical k-nearest neighbors (admissible pool A_t)
    |
    v
empirical future distribution / homogeneity statistic
    |
    v
statistical / predictive evaluation (I01: H_*; I02: CRPS / R / Z)
```

### 3.1 Frozen components (as recorded)

| Component | I01 (hypothesis v0.2) | I02 (PREREG-v0.3 / closure) |
|-----------|----------------------|-----------------------------|
| \(W_X\) | 20 | 20 |
| \(W_{RV}\) | (control `rv_W` on same \(W\)) | 20 |
| \(M\) (causal mean/σ window) | 252 | 252 (inherited) |
| Standardization ε | \(\varepsilon=10^{-8}\) | **no** \(\varepsilon_\sigma\); \(\hat\sigma_t=0\) → undefined / skip |
| \(h\) | 10 | 10 |
| \(k\) | 50 | 50 |
| Metric on \(X\) | Euclidean L2 | Euclidean L2 |
| Ties | (I01 protocol) | \((\mathrm{distance}\uparrow,\,s\uparrow)\), \(\lvert N\rvert=50\) |
| Weights | uniform | uniform \(1/50\) |
| Admissibility | \(Y\) available; \(\lvert\mathcal{L}_t\rvert\ge L_{\min}=3k\) (I01) | common pool \(A_t\); hard \(s+10\le t\); skip if \(\lvert A_t\rvert<50\) |
| Target (I01) | future path \(Y_t^{(h)}\); homogeneity \(\mathcal{H}_{\mathrm{raw/vol/shape}}\) | — |
| Target (I02) | — | \(V_{t,10}=\sqrt{\frac1{10}\sum_{j=1}^{10} r_{t+j}^2}\) |
| Forecast (I02) | — | empirical atoms \(\frac1{50}\sum_i \delta_{V_{s_i,10}}\) |
| Score (I02) | — | CRPS (lower better) |
| Comparators | B0 (naive); diagnostic `rv_W` k-NN | \(S_1=[RV]\), \(S_2=[RV,D]\), \(S_3\) as S3_Q / S3_phi (S3-A) |
| State \(Z\) (I02) | — | \(Z_t^{(m)}=\mathrm{Std_{pop}}(\Delta L)\) on \(m\in\{3,12,21\}\); analysis only |
| Association (I02) | — | Spearman \(Z\leftrightarrow R\); MBB \(B=9999\), seed 42, \(b^\star=40\), robustness \(\{20,40,80\}\) |

**PROJECT FACT — do not reinterpret.** I02 did **not** re-test I01’s
\(\mathcal{H}_{\mathrm{raw}}\) vs B0 claim. I02 tested monotone organization of
*relative CRPS incremental value* by \(Z\). Secondary mean \(D\) is diagnostic
only under the preregistration.

### 3.2 What “classical geometry” asserts operationally

**INTERPRETATION.** Operationally, classical geometry here is:

1. **Representation:** a fixed-length window of causally standardized log-returns;
2. **Geometry:** Euclidean \(\mathbb{R}^{W}\) with L2;
3. **Neighborhood:** historical \(k\)-NN under hard availability;
4. **Scientific use:** either future-path homogeneity (I01) or distributional
   forecast of realized volatility via CRPS vs simple controls (I02).

---

## 4. Assumption stack

Do **not** treat the pipeline as one hypothesis. Layers below are analytical
separations; I01/I02 rarely isolated them.

| Layer | Assertion | I01 test | I02 test | Evidence status | Downstream dependence |
|-------|-----------|----------|----------|-----------------|------------------------|
| **A. State representation** | Finite recent-return window \(X_t\in\mathbb{R}^{W}\) is a meaningful market-state summary | Indirect (pipeline assumed) | Indirect (same \(X\) frozen) | Untested as object; used throughout | All geometry / PRED claims on \(X\) |
| **B. Normalization / invariance** | Causal \(\mu/\sigma\) (I01: +\(\varepsilon\); I02: skip if \(\sigma=0\)) removes nuisance scale while preserving relevant structure | Indirect | Indirect (ε policy changed) | Untested vs alternatives | Metric distances; vol-control comparisons |
| **C. Metric** | Euclidean L2 is a meaningful similarity on represented states | Direct *as the only metric used* — not vs alternatives | Same | L2-specific results exist; **not** “L2 is optimal” | Neighborhoods; local PRED |
| **D. Locality** | Near states under the metric form meaningful local neighborhoods | Indirect via \(k\)-NN effects | Indirect | Effects observed under L2 \(k\)-NN; locality not isolated from metric/representation | Recurrence sampling; forecast atoms |
| **E. Structural recurrence** | Comparable states recur often enough for historical neighborhoods to be meaningful | Indirect (pool sizes / years) | Indirect (59 skips `INSUFFICIENT_ADMISSIBLE_POOL`) | Partially compatible; not quantified as scientific estimand | Any historical-neighbor method |
| **F. Future homogeneity / dependence** | Geometrically similar pasts have systematically related futures | **Direct** (H_raw/vol/shape vs B0; vs `rv_W`) | Indirect via CRPS of \(V_{t,10}\) | I01: yes vs B0 (vol-dominated); residual vs `rv_W` episodic; I02: no average CRPS gain of \(X\) | PRED claims |
| **G. Predictive increment** | Rich \(X\) adds information beyond simpler controls | Direct vs `rv_W` (partial) | Direct vs \(S_1,S_2,S_3\) (mean \(D\); association \(R\)) | Weakened: residual vs `rv_W` episodic; I02 mean \(D<0\) all branches; no monotone \(Z\leftrightarrow R\) | Justification for rich \(X\) |
| **H. Conditional structure** | Residual advantage may depend on regime / state | Direct descriptive (E04 stress/tail) | Direct *for monotone \(Z\)* — **absent** | Weakened for *this* \(Z\) monotone claim; episodic form open | Any “stress geometry” narrative |
| **I. Economic exploitability** | Structure survives costs, risk, ops | Not tested | Not tested | Untested | ECON / promotion |

**INTERPRETATION — non-collapse rule.** Geometric structure ≠ predictive
structure ≠ economic exploitability. A negative on G/H does not by itself
falsify A–E as descriptive geometry; a positive on F vs B0 does not establish G
vs rich controls or I.

---

## 5. Evidence map — I01 + I02

### 5.1 I01 (preserved conclusions)

**PROJECT FACT** ([I01-exploratory-synthesis.md](../I01/I01-exploratory-synthesis.md)):

- L2 neighborhoods showed reduced future \(\mathcal{H}_{\mathrm{raw}}\) relative to B0
  (\(\Delta_{\mathrm{raw}}\approx -13.7\%\)); \(\mathcal{H}_{\mathrm{vol}}\approx -54\%\);
  \(\mathcal{H}_{\mathrm{shape}}\approx -0.21\%\).
- Effect is primarily volatility-/amplitude-related; shape contribution nearly absent.
- `rv_W` control explained part of the story (neighbors largely share past vol;
  control recovers much of \(\mathcal{H}_{\mathrm{vol}}\) vs B0) but not necessarily all
  of \(\mathcal{H}_{\mathrm{raw}}\) / residual \(\mathcal{H}_{\mathrm{vol}}\) patterning.
- Residual relative advantage vs `rv_W` was highly concentrated in stress/tail
  periods (2008, 2009, 2020; high descriptive tertiles of `rv_W` / \(\|X\|\));
  median residual often unfavorable.
- Verdict: *ORIGINAL HYPOTHESIS NOT RECOMMENDED FOR CONFIRMATION;
  REGIME-CONDITIONAL PHENOMENON IDENTIFIED* — exploratory, not SCI-FAIL
  (DR-007).

### 5.2 I02 (preserved conclusions)

**PROJECT FACT** ([I02-CLOSURE.md](../I02/I02-CLOSURE.md),
[I02-E01-POSTMORTEM.md](../I02/I02-E01-POSTMORTEM.md)):

- Preregistered question: monotone \(Z\leftrightarrow R\) (Spearman), not
  unconditional \(\mathbb{E}[R]>0\).
- E01: EXPLORATORY / UNQUALIFIED; **0/12** detectable cells; **MS-1**;
  S3_Q / S3_phi agree; robustness \(b\in\{20,40,80\}\); K1–K8 not triggered;
  8208 / 8149 / 59 queries.
- Secondary: mean \(D<0\) vs S1, S2, S3_Q, S3_phi (approx. \(-6.4\times 10^{-4}\)
  to \(-7.2\times 10^{-4}\)).
- Disposition: **CLOSED / EXPL-ABSENT**; **no SCI claim**.
- Explicit non-conclusions: “\(Z\) contains no information”; “\(X\) never helps”;
  SCI-FAIL of the scientific claim class.

### 5.3 Mandatory distinctions

| Question | Answer |
|----------|--------|
| Which layers were **weakened**? | **G** (average incremental CRPS of \(X\)); **H** for *monotone organization by this \(Z\)*; **F** as *unconditional / broad* predictive story (already cautioned by I01 E04). |
| Which **survived untested**? | **A, B, C-as-alternative, D-isolated, E-as-estimand, I**; also nonlinear / episodic dependence (postmortem H-B). |
| Results concerning **L2 specifically**? | All neighborhood constructions used L2; no alternative metric was run. L2 is implicated only as *the implemented metric*, not as an isolated factor. |
| Results concerning **\(X\) specifically**? | I02 mean \(D<0\) and null \(R\) vs *all* \(S\) speak to rich \(X\) under this pipeline; I01 shape near-zero speaks to *path-shape* content of futures under L2 neighbors, not to representation adequacy alone. |
| Results concerning the **entire \(X+\mathrm{L2}+k\mathrm{NN}\) chain**? | Essentially all predictive results. Failure localization to a single component is **not identifiable** from I01+I02 alone. |

**INTERPRETATION.** I02’s negative monotone-\(Z\) result is compatible with I01’s
episodic residual story (postmortem H-B). It is **not** a proof that geometry
is empty; it is evidence against the *preregistered organizing claim*.

---

## 6. Failure-localization matrix

Diagnostic only. Rows are candidate explanations; columns are compatibility /
identifiability. **No preferred row is selected.**

| Candidate explanation | Compatible with I01? | Compatible with I02? | Directly tested? | Currently distinguishable? | Evidence required to distinguish |
|-----------------------|----------------------|----------------------|------------------|----------------------------|----------------------------------|
| Representation inadequate | Yes (shape weak; residual fragile) | Yes (mean \(D<0\)) | No (no alt \(X\)) | No | Alt representations with *same* metric/pool; structural tests without \(Y\) |
| Normalization inadequate | Possible | Possible (ε policy differs I01/I02) | No | No | Controlled normalization ablations; invariance diagnostics |
| Metric inadequate | Possible | Possible | No (L2 only) | No | Metric family changes *holding \(X\) fixed*; geometry-before-PRED |
| Local-neighborhood assumption inadequate | Possible | Possible | No | No | Vary locality notions; stability under perturbation |
| Recurrence insufficient | Partially (skips exist) | Partially (59 pool skips) | Not as estimand | No | Recurrence rates / revisit statistics independent of \(Y\) |
| No useful future dependence | Tensions with I01 vs B0 | Compatible with mean \(D<0\) | Partial | Partial | Separate B0-style vs control-style estimands; do not conflate |
| Controls already capture relevant information | Strongly suggested vs `rv_W` / \(S\) | Strongly (mean \(D<0\) all \(S\)) | Partial | Better than others for *average PRED increment* | Still does not isolate metric vs representation |
| Effect exists only conditionally | **Supported descriptively** (E04) | Compatible if non-monotone / episodic | Partial (descriptive I01; monotone \(Z\) failed I02) | Not for *which* condition | Preregistered conditionals **without** reusing 2008/2009/2020 labels post hoc |
| Apparent I01 residual is sampling/tail artifact | Open | Compatible | No conclusive test | No | Holdouts, fresh assets, synthetic nulls, confirmatory design |

**INTERPRETATION.** I01+I02 discriminate *somewhat* toward “average rich-\(X\)
increment is weak / negative under I02 controls” and “broad confirmation of
original I01 is unjustified,” but **do not** discriminate among representation
vs metric vs locality vs episodic structure.

---

## 7. State of the art (focused)

**EXTERNAL LITERATURE.** Summaries below are literature maps, **not** project
results. Relevance tags: DIRECTLY RELEVANT / POSSIBLY RELEVANT /
CURRENTLY UNJUSTIFIED relative to *this* classical baseline and evidence.

### 7.1 Evaluation template (applied per family)

For each retained family: mathematical object; geometry; invariances;
financial interpretation; scientific claim type in literature; evidence
quality; weaknesses; relation to baseline; testability before prediction;
project relevance.

### 7.2 Family briefs

#### A. Euclidean / classical state-space

1. **Object:** vectors of returns / indicators in \(\mathbb{R}^d\).  
2. **Geometry:** \(\|\cdot\|_2\) (or \(\ell_p\)).  
3. **Invariances:** none intrinsic beyond chosen normalization.  
4. **Finance:** “similar recent paths.”  
5. **Claims:** description, clustering, k-NN forecasting.  
6. **Evidence:** extensive historical empirical; mixed OOS.  
7. **Weaknesses:** scale domination, curse of dimensionality, nonstationarity.  
8. **vs baseline:** *is* the baseline (representation + metric).  
9. **Before \(Y\):** neighborhood stability / recurrence can be studied without futures.  
10. **Relevance:** **DIRECTLY RELEVANT** (G0).

#### B. Mahalanobis / covariance-aware geometry

1. **Object:** same vectors; metric \(d_\Sigma(x,y)=\sqrt{(x-y)^\top\Sigma^{-1}(x-y)}\).  
2. **Geometry:** ellipsoid induced by covariance.  
3. **Invariances:** linear whitening (up to \(\Sigma\)).  
4. **Finance:** decorrelate coordinates / account for co-movement.  
5. **Claims:** classification, anomaly, forecasting features.  
6. **Evidence:** classical multivariate stats; finance applications common.  
7. **Weaknesses:** \(\Sigma\) estimation error; regime dependence of \(\Sigma\).  
8. **vs baseline:** primarily **metric** (sometimes representation if \(\Sigma\) is the state).  
9. **Before \(Y\):** metric stability of \(\Sigma_t\) estimable from past only.  
10. **Relevance:** **POSSIBLY RELEVANT** (GM) — not justified as next experiment solely by I02.

#### C. Metric learning

1. **Object:** learned \(d_\theta(x,x')\).  
2. **Geometry:** parametric / neural metrics.  
3. **Invariances:** whatever training imposes.  
4. **Finance:** “task-optimal” similarity.  
5. **Claims:** mostly prediction / retrieval.  
6. **Evidence:** ML empirical; high snooping risk.  
7. **Weaknesses:** data snooping, nonstationarity, opacity.  
8. **vs baseline:** metric (± representation).  
9. **Before \(Y\):** weak unless supervised by non-\(Y\) structure (hard).  
10. **Relevance:** **CURRENTLY UNJUSTIFIED** as next step after negative I02 (researcher DoF explosion).

#### D. Delay-coordinate embedding / phase-space reconstruction

1. **Object:** \((x_t,x_{t-\tau},\ldots,x_{t-(m-1)\tau})\) (Takens-type).  
2. **Geometry:** ambient Euclidean or delay-space metric.  
3. **Invariances:** none automatic.  
4. **Finance:** reconstruct latent dynamical state from scalars.  
5. **Claims:** description, recurrence, sometimes prediction.  
6. **Evidence:** theory strong for deterministic systems; finance empirical mixed (noise, nonstationarity).  
7. **Weaknesses:** parameter \((m,\tau)\); stochastic markets ≠ clean attractors.  
8. **vs baseline:** **representation** (+ possibly GD).  
9. **Before \(Y\):** recurrence plots / correlation dimension style diagnostics possible.  
10. **Relevance:** **POSSIBLY RELEVANT** (GR / GD). Classic refs: Takens (1981); Sauer–Yorke–Casdagli (1991).

#### E. Recurrence analysis / RQA / recurrence networks

1. **Object:** recurrence matrix \(R_{i,j}=\mathbf{1}\{d(x_i,x_j)\le\varepsilon\}\).  
2. **Geometry:** thresholded similarity; network topology optional.  
3. **Invariances:** depend on \(d\) and normalization.  
4. **Finance:** temporal recurrence, regime transitions.  
5. **Claims:** description, regime detection; sometimes early-warning.  
6. **Evidence:** methodological + empirical finance RQA literature.  
7. **Weaknesses:** \(\varepsilon\)/threshold sensitivity; multiple testing.  
8. **vs baseline:** **neighborhood / topology of recurrence**, often keeping representation.  
9. **Before \(Y\):** **yes** — recurrence structure is intrinsically past-based.  
10. **Relevance:** **DIRECTLY RELEVANT** to geometry-before-prediction (conceptual). Marwan et al. RQA reviews.

#### F. Manifold learning

1. **Object:** low-dimensional manifold assumed in high-d observations.  
2. **Geometry:** geodesic / graph approximations (Isomap, LLE, etc.).  
3. **Invariances:** local isometries (approx.).  
4. **Finance:** “market states lie on a manifold.”  
5. **Claims:** visualization, clustering; weaker causal PRED evidence.  
6. **Evidence:** mostly descriptive / synthetic; finance OOS thin.  
7. **Weaknesses:** noise, nonstationarity, parameter sensitivity.  
8. **vs baseline:** representation / neighborhood geometry.  
9. **Before \(Y\):** partially (intrinsic dimension, embedding stability).  
10. **Relevance:** **POSSIBLY RELEVANT**; not auto-next.

#### G. Diffusion maps / diffusion geometry

1. **Object:** data graph; diffusion distance from random-walk semigroup.  
2. **Geometry:** spectral embedding of Markov operator (Coifman–Lafon).  
3. **Invariances:** approximately to sampling density (with normalization).  
4. **Finance:** multiscale geometry of state clouds.  
5. **Claims:** dimensionality reduction, clustering; limited trading claims in serious work.  
6. **Evidence:** strong applied-math theory; finance applications exist but thinner.  
7. **Weaknesses:** kernel scale; cost; nonstationarity.  
8. **vs baseline:** metric / neighborhood (affinity).  
9. **Before \(Y\):** yes for structural spectral stability.  
10. **Relevance:** **POSSIBLY RELEVANT** (GM / GD).

#### H. Riemannian geometry (SPD / covariance manifolds)

1. **Object:** SPD matrices (covariances, kernels) as points on a manifold.  
2. **Geometry:** affine-invariant, Log-Euclidean, Bures–Wasserstein, etc.  
3. **Invariances:** congruence / scale depending on metric.  
4. **Finance:** covariance dynamics as geometric trajectories; portfolio geometry.  
5. **Claims:** mostly description, portfolio/robust optimization, clustering — **not** “options = Riemannian trading” as a theorem of markets.  
6. **Evidence:** solid math (Pennec; Bhatia–Jain–Lim on Bures–Wasserstein); finance applications active.  
7. **Weaknesses:** estimation of SPD; choice of metric; interpretability.  
8. **vs baseline:** **representation** (state = covariance) and **metric**.  
9. **Before \(Y\):** geodesic stability of covariance paths testable without returns targets.  
10. **Relevance:** **POSSIBLY RELEVANT** if state is redefined as SPD; **CURRENTLY UNJUSTIFIED** as drop-in L2 replacement for return-window \(X\).

#### I. Optimal transport / Wasserstein geometry

1. **Object:** probability measures (return distributions, empirical clouds).  
2. **Geometry:** Wasserstein-\(p\) distances; barycenters; DRO balls.  
3. **Invariances:** none universal; ground metric choices matter.  
4. **Finance:** distributional discrepancy; robust portfolio (Wasserstein DRO); Gaussian case ↔ Bures.  
5. **Claims:** portfolio robustness, distributional forecasting metrics — stronger than crash-prediction lore.  
6. **Evidence:** strong math (Villani); growing finance DRO / robust risk literature (e.g. Blanchet et al.; mean-covariance Gelbrich/Wasserstein).  
7. **Weaknesses:** computational cost; ground metric; adapted vs classical OT for time series.  
8. **vs baseline:** can change **object** (distributions) and **metric**; may leave \(k\)-NN paradigm.  
9. **Before \(Y\):** distances between *past* empirical measures yes; predictive claims no.  
10. **Relevance:** **POSSIBLY RELEVANT** (GM); not selected.

#### J. Topological data analysis / persistent homology

1. **Object:** filtrations on point clouds → persistence diagrams / landscapes.  
2. **Geometry:** topological features across scales.  
3. **Invariances:** approximate isometry robustness (stability theorems).  
4. **Finance:** “shape” of multi-asset return clouds; proposed crash early warnings.  
5. **Claims:** description + **claimed** early-warning (e.g. Gidea–Katz 2017, arXiv:1703.04385).  
6. **Evidence:** historical empirical on known crises; limited prospective / holdout discipline in much of the crash-warning literature.  
7. **Weaknesses:** parameter choices; multiple testing; post-hoc crisis labeling; computational cost.  
8. **vs baseline:** **topology** (GT), often changing multi-series representation.  
9. **Before \(Y\):** persistence of past clouds yes; “predict crashes” requires futures / labels.  
10. **Relevance:** **POSSIBLY RELEVANT** as structural toolkit; **CURRENTLY UNJUSTIFIED** as automatic I03.

#### K. Information geometry

1. **Object:** parametric families as Riemannian manifolds (Fisher–Rao).  
2. **Geometry:** Fisher metric; α-connections (Amari).  
3. **Invariances:** reparameterization invariance of Fisher–Rao.  
4. **Finance:** geometry of statistical models (vol models, copulas).  
5. **Claims:** mostly theoretical / estimation; occasional empirics.  
6. **Evidence:** deep theory; finance applied layer thinner.  
7. **Weaknesses:** model misspecification; estimation.  
8. **vs baseline:** different object (model parameters), not a drop-in on \(X\).  
9. **Before \(Y\):** divergence geometry on fitted past models possible.  
10. **Relevance:** **POSSIBLY RELEVANT** only if program shifts to parametric model states.

#### L. Ultrametric / hierarchical geometry

1. **Object:** hierarchies / dendrograms; ultrametric \(d(x,z)\le\max\{d(x,y),d(y,z)\}\).  
2. **Geometry:** tree-like multi-scale similarity.  
3. **Invariances:** hierarchical coarse-graining.  
4. **Finance:** hierarchical risk, clustering of assets/times.  
5. **Claims:** portfolio hierarchy (e.g. Tumminello / hierarchical risk parity *related* practice); descriptive taxonomy.  
6. **Evidence:** empirical clustering literature; not a proof of market ultrametricity.  
7. **Weaknesses:** linkage choices; instability; overinterpretation.  
8. **vs baseline:** neighborhood / topology (GH).  
9. **Before \(Y\):** hierarchy stability testable.  
10. **Relevance:** **POSSIBLY RELEVANT** as **future R&D branch**, not active commitment.

#### M. p-adic approaches

1. **Object:** p-adic numbers / hierarchies as state spaces.  
2. **Geometry:** p-adic absolute values (ultrametric).  
3. **Invariances:** hierarchical.  
4. **Finance:** speculative analogies to hierarchical capital structures / tick hierarchies.  
5. **Claims:** mostly theoretical / exploratory essays; scarce rigorous predictive finance evidence.  
6. **Evidence:** niche; not established finance mainstream.  
7. **Weaknesses:** weak empirical base; mapping from market data underdetermined.  
8. **vs baseline:** deep representation+metric change.  
9. **Before \(Y\):** unclear without a faithful embedding.  
10. **Relevance:** **CURRENTLY UNJUSTIFIED**; remain **future R&D only** unless new evidence appears.

### 7.3 Cross-cutting literature finding

**EXTERNAL LITERATURE + INTERPRETATION.** Across families, serious work more
often supports *description, clustering, robust optimization, or regime
diagnostics* than *stable out-of-sample trading alpha from exotic geometry*.
Crash-prediction and “stable attractor” claims are especially fragile under
nonstationarity and researcher degrees of freedom.

---

## 8. Claim audit — geometric finance narrative

| Claim | Classification | Why (with sources) |
|-------|----------------|--------------------|
| “Covariance defines market geometry” | **VALID BUT CONTEXT-DEPENDENT** | Covariance induces well-studied geometries (Mahalanobis; SPD Riemannian; Bures–Wasserstein ≡ \(W_2\) on centered Gaussians — Bhatia–Jain–Lim; OT/Gaussian formulae). It defines *a* geometry of second moments, not *the* unique market geometry, and does not by itself imply predictive neighborhoods for return *paths*. |
| “Option trading is Riemannian geometry” | **WEAK / OVERSTATED** | Differential-geometric language appears in mathematical finance (e.g. information geometry of models; smile geometries in research), but equating live option trading with Riemannian geometry as an operational identity overstates; no project evidence; treat as metaphor / specialized theory, not established trading law. |
| “Market phase spaces contain stable attractors” | **WEAK / OVERSTATED** (finance empirics) | Takens-style reconstruction is **WELL-ESTABLISHED** mathematically for deterministic systems; applying “stable attractors” to noisy, nonstationary markets is **ACTIVE RESEARCH** at best and often overclaimed. I01/I02 did not test attractors. |
| “Persistent-homology holes predict crashes” | **ACTIVE RESEARCH** leaning **WEAK / OVERSTATED** for operational prediction | Gidea–Katz (arXiv:1703.04385) report persistence-landscape norms rising near known crises (2000, 2008) on multi-index clouds — historical descriptive / early-warning *proposal*, not a validated prospective trading system. High contamination risk if crises are pre-labeled. |
| “Ultrametric / p-adic geometry naturally describes markets” | **NOT SUPPORTED** as a general law; ultrametric hierarchies **VALID BUT CONTEXT-DEPENDENT** as clustering tools; p-adic finance **WEAK / OVERSTATED** | Hierarchical clustering is useful descriptive practice; “natural p-adic market” lacks strong primary empirical consensus. |

**Strictness note.** Claims of crash prediction, stable attractors, or superior
trading performance require prospective discipline far beyond I01/I02 and beyond
most promotional geometric-finance narratives.

---

## 9. Geometry before prediction

**OPEN QUESTION (program-level):** Can a market-state geometry be shown
nontrivial and stable *before* asking whether it predicts \(Y\)?

**INTERPRETATION — answer:** **Yes, in principle.** Classes of evidence that
could establish nontrivial / stable geometry **without future returns** include
(conceptual classes only — **not** authorized metrics or an experiment design):

1. **Neighborhood stability** — small past-only perturbations of \(X_t\) leave
   neighbor sets largely unchanged.
2. **Temporal recurrence** — states revisit ε-balls at rates unlike i.i.d. nulls
   constructed from past marginals / block-shuffles.
3. **Local dimensionality** — intrinsic dimension estimates stable across
   subperiods (past-only).
4. **Metric stability** — rankings of pairwise distances stable under
   estimation windows / sub-sampling.
5. **Topology persistence** — persistence summaries of past point clouds stable
   under reasonable filtrations (descriptive, not crash labels).
6. **Out-of-period neighborhood preservation** — neighbor relations estimated
   on period A predict neighbor relations on period B *without* using \(Y\).

**INTERPRETATION.** Such tests can falsify “pure noise cloud” stories and can
constrain A–E **without** reopening PRED shopping. They **cannot** by themselves
restore G/H/I. I01/I02’s predictive negatives make this sequencing scientifically
attractive: they reduce the temptation to change the metric solely to chase \(Y\).

**PROJECT FACT.** Neither I01 nor I02 preregistered a geometry-before-prediction
battery as primary estimand.

---

## 10. Contamination / researcher degrees of freedom

### 10.1 Already known (cannot be pristine discovery)

**PROJECT FACT / INTERPRETATION.** The following are **contaminated** as
surprise discoveries for future design:

| Known pattern | Source | Implication |
|---------------|--------|-------------|
| Episodes **2008, 2009, 2020** | I01 E04 | Cannot define “stress regime” post hoc as “those years” to recover the effect |
| Volatility dominance of L2 vs B0 | I01 E02–E03 | Any new metric that mostly re-encodes vol will look like a rediscovery |
| Weak **shape** result | I01 | “Path-shape geometry predicts path-shape futures” already strained under L2 |
| Stress/tail concentration of residual vs `rv_W` | I01 E04 | Conditional stories must be preregistered without fishing those episodes |
| I02 mean \(D<0\) vs all \(S\) | I02 E01 secondary | “Average rich-\(X\) CRPS gain” is not a clean positive prior |
| Failure of preregistered monotone \(Z\leftrightarrow R\) | I02 E01 | Cannot silently replace \(Z\) with another organizer fitted to the same run |

### 10.2 Implications for future confirmatory work

**INTERPRETATION.**

- Exploratory sandbox (SPY / yfinance / daily, DR-008) remains **UNQUALIFIED**;
  confirmatory path still requires C02 + DR-003 D-1 + DR-005 + holdout.
- Fresh assets, periods, holdouts, and synthetic nulls may eventually be
  required to separate genuine structure from episode memory — **not chosen
  here**.
- A future investigation that *defines* stress after seeing I01 E04 is
  methodologically invalid as confirmation of the I01 residual story.
- Metric shopping after EXPL-ABSENT maximizes false-positive risk; any GM/GT/GH
  move needs an independent structural claim, preferably testable without \(Y\).

---

## 11. Research branch map

Provisional names. Branches organized by **scientific change**, not fashion.
**p-adic / ultrametric** and **TDA** remain non-committed unless evidence
justifies activation.

```text
G0 — CLASSICAL BASELINE
     current X + causal standardization + L2 + historical k-NN
        |
        +-- GR  alternative representation (same or new metric)
        +-- GM  alternative metric / affinity (fixed X)
        +-- GD  dynamical geometry (delay/recurrence/diffusion dynamics)
        +-- GT  topology (persistence / qualitative shape of clouds)
        +-- GH  hierarchical / ultrametric (FUTURE R&D unless justified)
```

| Branch | Assumption replaced | Assumption retained | New claim introduced | Minimum evidence before PRED |
|--------|---------------------|---------------------|----------------------|------------------------------|
| **G0** | — | A–E as currently implemented | Classical neighborhoods carry structure | Already used for PRED; structural battery still missing |
| **GR** | A (±B) | C–E optional | New object encodes market state better | Past-only discriminability vs \(X\); invariance checks |
| **GM** | C (±D) | A,B (ideally) | New similarity better matches “same state” | Neighbor stability / recurrence vs L2 *without \(Y\)* |
| **GD** | A/D as static window | recurrence emphasis | Dynamics / revisit structure is the geometry | RQA-style or delay recurrence vs null, past-only |
| **GT** | topology of neighborhoods | cloud construction | Qualitative multi-scale shape is meaningful | Persistence stability across periods; **no** crisis fishing |
| **GH** | D as Euclidean balls | hierarchy | Ultrametric organization is intrinsic | Hierarchy stability; keep as R&D until then |

**INTERPRETATION.** After I02, jumping to GM or GT *because* mean \(D<0\) is
exactly the shopping failure mode this review exists to prevent.

---

## 12. Candidate I03 questions

**Maximum three.** Discriminating scientific questions — **not** methods.
No parameters, datasets, thresholds, metrics, procedures, or code.

### Candidate Q1 — Intrinsic recurrence of the current representation

- **Question:** Do neighborhoods defined by the current classical representation
  \(X\) exhibit nontrivial, temporally structured recurrence that is stable
  across subperiods, *independently of future outcomes*?
- **Layer targeted:** D, E (and secondarily A)
- **Why I01/I02 motivate it:** Predictive claims on the full chain are weakened;
  recurrence/locality were never primary estimands; geometry-before-prediction
  is the lowest-DoF way to avoid metric shopping.
- **Distinguishes:** “geometry is pure noise” vs “structure exists but does not
  yield average PRED increment under I02 controls.”
- **Future returns required?** **No**
- **Contamination risk:** Medium if recurrence thresholds are tuned to recover
  2008/2009/2020; low if preregistered without crisis labels
- **If PASS:** Justifies continued investment in G0 structural science; still
  no PRED/ECON claim
- **If FAIL:** Strongly supports frame D (stop or radical GR), not silent GM

### Candidate Q2 — Failure attribution: Euclidean neighborhood instability vs absent recurrence

- **Question:** Is the apparent failure of the classical baseline’s *predictive
  increment* more consistent with instability of Euclidean neighborhoods under
  past-only perturbations than with absence of recurrent state structure in \(X\)?
- **Layer targeted:** C/D vs E (localizes metric/locality vs recurrence)
- **Why I01/I02 motivate it:** I01/I02 cannot identify the failing component;
  this is a discriminating structural fork before changing representation or
  metric opportunistically.
- **Distinguishes:** GM-motivation (unstable L2 neighborhoods) vs “no revisits”
  (E failure) vs neither (points back to G/H/controls)
- **Future returns required?** **No** for the structural discrimination; PRED
  increment remains a separate claim
- **Contamination risk:** Medium (definition of “instability”); must not sneak
  \(Y\) into the criterion
- **If PASS (instability, recurrence present):** Motivates careful GM *or*
  normalization work with structural gates
- **If PASS (no recurrence):** Motivates GR / stop more than metric cosmetics
- **If FAIL to distinguish:** Remains non-identifiable — do not pick a glamorous
  family anyway

### Candidate Q3 — Residual episodic advantage without monotone \(Z\)

- **Question:** Does rich \(X\) exhibit *any* residual predictive advantage over
  the adversarial controls under *preregistered* episodic or state conditions
  that are **not** post-hoc encodings of 2008/2009/2020, despite I02’s absent
  average increment and absent monotone \(Z\leftrightarrow R\)?
- **Layer targeted:** G, H (and F)
- **Why I01/I02 motivate it:** I01 suggested episodic residual; I02 rejected
  broad monotone \(Z\) organization and showed mean \(D<0\); closure already
  flagged an undesigned candidate along these lines.
- **Distinguishes:** “controls fully dominate” vs “non-monotone / episodic
  residual remains” vs “I01 residual was artifact”
- **Future returns required?** **Yes** (PRED-layer by nature)
- **Contamination risk:** **High** — highest shopping/hazard branch; requires
  extreme precommitment and likely fresh holdout / asset discipline
- **If PASS:** Narrows to conditional PRED research; still not ECON; still not
  SCI without confirmatory path
- **If FAIL:** Further weakens G/H; strengthens case for A (structure-only) or D

**INTERPRETATION.** Q1–Q2 are structurally prior to metric fashion. Q3 is
scientifically motivated but contamination-heavy; it must not be used to reopen
I02 under a new label.

---

## 13. Decision frame

Possible human outcomes:

| Code | Outcome |
|------|---------|
| **A** | Investigate whether the **current** geometry has intrinsic structure before changing it |
| **B** | Isolate **representation** as the next research problem |
| **C** | Isolate **metric / geometry** as the next research problem |
| **D** | Stop the current geometric-neighborhood branch — evidence does not justify further investigation |
| **E** | Another outcome strongly justified by the review |

**INTERPRETATION — discrimination status.**

- Evidence **supports seriousness of A** as a low-contamination next step:
  A–E were never established independently of PRED; I02 weakened G/H without
  falsifying descriptive geometry.
- Evidence **weakens** naive continuation of broad PRED claims on G0, but does
  **not** by itself mandate D.
- Evidence **does not uniquely select B vs C**: mean \(D<0\) and I01’s
  vol/shape pattern are compatible with bad representation, bad metric,
  saturated controls, or episodic-only effects.
- Therefore: **A vs B vs C are not identified.** A human may still *choose* A
  as process discipline without claiming it is empirically forced.
- **D** would require an additional value judgment (opportunity cost /
  program priority), not a unique logical consequence of EXPL-ABSENT.
- **E** examples (not selected): pause geometry and pursue non-geometric vol
  modeling; or confirmatory infrastructure (C02) without new geometry science.

**This review does not select A/B/C/D/E.**

---

## 14. References

Primary bibliographic list: [references.md](references.md).

### Project evidence (internal)

1. `research/I01/I01-exploratory-synthesis.md`
2. `research/I01/hypothesis.md` (+ E01–E04 reports)
3. `research/I02/I02-preregistration.md` (I02-PREREG-v0.3)
4. `research/I02/I02-L2-CONTRACT-TEST.md`
5. `research/I02/I02-HAT.md` (+ `hat/run*`)
6. `research/I02/I02-E01.md` + `e01/run1/`
7. `research/I02/I02-E01-POSTMORTEM.md` @ `f581416`
8. `research/I02/I02-CLOSURE.md` @ `68f7f56` (pin `c4ac436`)
9. Commits: E01 `33d063d`, pin `2b00657`, postmortem `f581416`, closure
   `68f7f56` / `c4ac436`

### External (selected; see references.md for identifiers)

Takens (1981); Sauer–Yorke–Casdagli (1991); Marwan et al. (RQA); Coifman–Lafon
(diffusion maps); Pennec (SPD Riemannian); Bhatia–Jain–Lim (Bures–Wasserstein);
Villani (OT); Blanchet et al. / Wasserstein DRO portfolio literature;
Gidea–Katz (2017) TDA crashes (arXiv:1703.04385); Amari (information geometry).

---

## Document control

| Field | Value |
|-------|-------|
| ID | GEOMETRY-PROGRAM-REVIEW-v0.1 |
| Created for | Post-I02 / pre-I03 architecture decision |
| Alters I01/I02 historical docs? | **No** |
| Opens I03? | **No** |
| Selects metric? | **No** |
