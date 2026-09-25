# I03-PRE — Intrinsic Recurrence / Stability Decision Dossier v0.1

> **STATUS :** PRE-FRAMING — **HISTORICAL** (D1–D8 human-frozen; I03 = DESIGN)  
> **Authority class :** RESEARCH (mathematical / scientific design)  
> **Parent decision :** Geometry Program Review v0.1 @ `547fc57` — **FRAME A**  
> **Protocol :** QDP v0.1 · DR-007  
> **Freeze record :** [I03-D1-D8-FREEZE.md](../I03/I03-D1-D8-FREEZE.md)  
> **Design :** [I03-DESIGN-v0.1.md](../I03/I03-DESIGN-v0.1.md)  
>
> ```text
> I03-PRE = HISTORICAL
> D1–D8 = HUMAN-FROZEN (see I03 freeze record)
> I03 STATUS = DESIGN (not executable prereg; not executed)
> NO MARKET DATA USED IN THIS PRE-FRAMING
> ```

**Label convention**

| Tag | Meaning |
|-----|---------|
| **PROJECT FACT** | Repository evidence (I01/I02/geometry review) |
| **MATHEMATICAL FACT** | Logical / geometric necessity under G0 definitions |
| **LITERATURE PRACTICE** | Established methodology outside the project |
| **INTERPRETATION** | Reasoning connecting the above; not a freeze |
| **HUMAN DECISION REQUIRED** | Choice that must be made by humans before I03 opens |

---

## 1. Executive summary

**PROJECT FACT.** Frame A was selected: ask whether current classical geometry
**G0** has intrinsic structure *before* replacing representation or metric.

**INTERPRETATION.** I01/I02 evaluated the full chain \(X \to \mathrm{L2} \to
N_k \to\) future criteria. They did **not** establish independently that local
neighborhoods under \(d_0\) are meaningfully recurrent or stable. A structural
I03 (if opened) would answer a SCI-level *geometry* question without PRED.

**This dossier does not freeze I03.** It exposes competing definitions of
recurrence and stability, the temporal-overlap trap, null-model doctrine,
identifiability limits, and **eight human decisions (D1–D8)** that should be
taken in one pass before any preregistration.

**Two traps treated as first-class (mandate):**

1. **Temporal overlap.** With \(W_X=20\), \(X_t\) and \(X_{t+1}\) share 19
   underlying returns. Without temporal exclusion, “nearest neighbors” can
   rediscover window construction.
2. **Null model.** Financial series exhibit volatility persistence,
   autocorrelation, heavy tails, and nonstationarity. “Recurrence exists” is
   scientifically empty unless compared to nulls that preserve specified
   nuisance structure and destroy the state-space structure under test.

**Cursor stance.** Where methodology strongly favors an option, it is marked
`RECOMMENDED ON METHODOLOGICAL GROUNDS`. **No option is frozen.**

---

## 2. Status / evidence boundary

### 2.1 In scope

- `research/I01/`, `research/I02/`, `research/geometry/`
- External literature for recurrence, Theiler windows, surrogates, distance
  concentration — definitional only

### 2.2 Out of scope (hard)

Market-data download/execution; SPY analysis; I01/I02 recomputation; any
\(Y\), \(V\), \(H_{\mathrm{raw}}\), CRPS, \(D\), \(R\), PnL; alternative
geometry/metric/representation; TDA / p-adic; parameter optimization;
threshold selection from data; `research/I03/`; preregistration; SCI/PRED/ECON
promotion; implementation.

### 2.3 Parent references

| Item | Location |
|------|----------|
| Geometry review | [GEOMETRY-PROGRAM-REVIEW-v0.1.md](../geometry/GEOMETRY-PROGRAM-REVIEW-v0.1.md) @ `547fc57` |
| Human frame | **A** — intrinsic structure of current G0 first |
| Candidate question retained | Stable local recurrence of \(X\) independent of futures |

---

## 3. Fixed G0 object

**PROJECT FACT / MATHEMATICAL FACT.** For this pre-framing, the object is
**held fixed** (not declared optimal):

\[
X_t
=
\bigl(\tilde r_{t-W_X+1},\ldots,\tilde r_t\bigr)
\in\mathbb{R}^{W_X},
\quad
W_X=20,\quad M=252,
\]

with causal inclusive standardization as in the I01/I02 representation
contract (I02: skip if \(\hat\sigma_t=0\); I01 historically used
\(\varepsilon=10^{-8}\)).

\[
d_0(X_t,X_s)=\|X_t-X_s\|_2.
\]

**Forbidden in I03-PRE / any G0 structural I03 under Frame A:**

Mahalanobis, Wasserstein, learned metrics, TDA, p-adic, alternative \(X\),
changes to \(W_X\), \(M\), normalization, or L2.

**INTERPRETATION.** Fixing G0 answers: *does this object have structure?*
It cannot answer whether another geometry would.

---

## 4. Meaning of recurrence — competing concepts

Do **not** begin with a statistic. Concepts first.

### 4.1 Relation among R1–R4

| Pair | Relation |
|------|----------|
| R1 vs R3 | **Complementary / overlapping.** R1 emphasizes *who* is near whom across time; R3 emphasizes *returns of the trajectory* to previously visited regions. Operationally often coupled. |
| R1 vs R2 | **Nested if strengthened.** R2 requires more than isolated nearest matches (composition/geometry of neighborhoods). R1 can hold while R2 fails. |
| R2 vs R4 | **Related but different.** R2 is local about a state; R4 is recoverability of local relations across temporal segments (cross-period). |
| R3 vs R4 | **Complementary.** R3 is dynamical revisit; R4 is structural transport across epochs. |
| All four | **Not equivalent.** Choosing one is a scientific claim choice (**HUMAN DECISION REQUIRED** — D1). |

### 4.2 R1 — Nearest-neighbor recurrence

| Aspect | Content |
|--------|---------|
| **Object** | For query \(t\), ranked set \(N_k^{\mathrm{excl}}(t)=\{s: |t-s|\ge\tau,\ \mathrm{rank}_{d_0}\le k\}\) (exclusion \(\tau\) separate — §7). |
| **Meaning** | Historically separated times repeatedly land near the same states under \(d_0\). |
| **Assumptions** | \(d_0\) meaningful; pool dense enough; exclusion adequate. |
| **Sample density** | High — sparse regions yield unstable “neighbors.” |
| **Temporal dependence** | Extreme without \(\tau\); still high with short \(\tau\). |
| **Vol scaling** | Causal std mitigates raw scale; residual vol-shape coupling remains. |
| **Dimensionality** | High — concentration can flatten ranks (§6). |
| **DoF** | \(k\), \(\tau\), pool definition, aggregation over \(t\). |
| **PASS** | Separated revisits under \(d_0\) exceed null. |
| **FAIL** | No excess NN recurrence beyond null / trivial overlap. |

### 4.3 R2 — Neighborhood recurrence

| Aspect | Content |
|--------|---------|
| **Object** | Properties of full local sets (overlap of neighbor sets for nearby queries; local pairwise geometry; composition). |
| **Meaning** | Local *clouds*, not lone nearest matches, are reproducible. |
| **Assumptions** | Locality is multi-point; \(k\) or radius enters. |
| **Sample density** | High. |
| **Temporal dependence** | High; correlated queries inflate overlap. |
| **Vol scaling** | Neighborhoods may collapse to “same vol level.” |
| **Dimensionality** | High. |
| **DoF** | How “composition/geometry” is scored; \(k\)/radius. |
| **PASS** | Local clouds cohere beyond null. |
| **FAIL** | Only accidental isolated matches (R1 weak or null-only). |

### 4.4 R3 — Temporal recurrence

| Aspect | Content |
|--------|---------|
| **Object** | Recurrence times / rates: first return of \(X_t\) into a ball / neighbor relation after lag \(\ge\tau\). |
| **Meaning** | Trajectory re-enters previously visited regions after separation. |
| **Assumptions** | State space + metric define “region”; stationarity optional but affects interpretation. |
| **Sample density** | Affects return-time tails. |
| **Temporal dependence** | Intrinsic to the claim; must separate trivial short-lag returns. |
| **Vol scaling** | Vol clustering induces short returns to high-vol regions. |
| **Dimensionality** | Ball volumes explode with dimension. |
| **DoF** | Ball radius vs \(k\)-NN dual; return-time functional. |
| **PASS** | Return structure atypical under null. |
| **FAIL** | Returns match nuisance-driven surrogates. |

### 4.5 R4 — Structural recurrence

| Aspect | Content |
|--------|---------|
| **Object** | Map of local relations estimated on segment \(A\), evaluated on segment \(B\) (cross-period neighborhood preservation). |
| **Meaning** | Local geometry is *transportable* across time, not episode-bound. |
| **Assumptions** | Segments comparable; no future in split rule. |
| **Sample density** | Both segments need adequate density. |
| **Temporal dependence** | Split choice interacts with nonstationarity. |
| **Vol scaling** | Shared vol regimes across periods can fake transport. |
| **Dimensionality** | Same concentration issues. |
| **DoF** | Split doctrine; what “preservation” means. |
| **PASS** | Local structure recoverable out of period beyond null. |
| **FAIL** | Structure collapses across periods (E5-compatible). |

**HUMAN DECISION REQUIRED — D1** (primary recurrence meaning). See §15.

---

## 5. Meaning of stability — competing concepts

### 5.1 S1 — Perturbation stability

| Aspect | Content |
|--------|---------|
| **Property** | Small admissible past-only perturbations of \(X_t\) do not radically change \(N(t)\). |
| **Tests** | Metric + locality (+ representation sensitivity). |
| **Advantages** | Direct probe of “meaningful locality.” |
| **Weaknesses** | Requires a perturbation law (noise model) — major DoF (**F12**). |
| **Requires** | Magnitude / direction family; must be preregistered, not data-fit. |

### 5.2 S2 — Temporal stability

| Aspect | Content |
|--------|---------|
| **Property** | Local structure persists across separated segments. |
| **Tests** | Recurrence + nonstationarity (aligns with R4). |
| **Advantages** | Blocks episode-dominated “structure.” |
| **Weaknesses** | Split DoF (**F11**); power loss. |
| **Requires** | Temporal split doctrine (causally defined). |

### 5.3 S3 — Sampling stability

| Aspect | Content |
|--------|---------|
| **Property** | Not critically dependent on individual points / one realization. |
| **Tests** | Finite-sample robustness. |
| **Advantages** | Guards against single-point leverage. |
| **Weaknesses** | Resampling rule DoF; interaction with dependence. |
| **Requires** | Block bootstrap / leave-block-out style rule compatible with time series. |

### 5.4 S4 — Neighborhood-scale stability

| Aspect | Content |
|--------|---------|
| **Property** | Conclusions not artifacts of one cardinality \(k\). |
| **Tests** | Locality definition. |
| **Advantages** | Prevents \(k{=}50\) inheritance fallacy. |
| **Weaknesses** | Multiple \(k\) ⇒ multiple-testing / fishing unless preregistered grid + MS-style reading. |
| **Requires** | Scale set or primary scale + robustness — **HUMAN DECISION REQUIRED (D3)**. |

### 5.5 S5 — Rank / topological local stability

| Aspect | Content |
|--------|---------|
| **Property** | Relative local orderings preserved when exact distances shift. |
| **Tests** | Ordinal locality (weaker than metric equality). |
| **Advantages** | Less sensitive to global rescale; interpretable. |
| **Weaknesses** | May miss magnitude-critical geometry; still \(k\)/τ dependent. |
| **Requires** | Rank functional definition. |

### 5.6 Role of \(k=50\)

**PROJECT FACT.** \(k=50\) is frozen in I01/I02 *prediction* designs.

**MATHEMATICAL FACT.** Nothing in the definition of “recurrence” or “stability”
*forces* a unique neighborhood cardinality.

**INTERPRETATION — three doctrines (D3):**

| Option | Doctrine |
|--------|----------|
| **D3-A** | Inherit \(k=50\) as G0 contract for primary structural claim |
| **D3-B** | Primary claim is scale-robust (preregistered small set of \(k\); no best-\(k\)) |
| **D3-C** | Primary claim is radius- / rank-based and **does not** use \(k\) as the defining object; \(k\) only diagnostic |

`RECOMMENDED ON METHODOLOGICAL GROUNDS`: **D3-B or D3-C** over D3-A, because
structural claims should not silently inherit a PRED hyperparameter. D3-A
remains defensible if the scientific question is explicitly “structure of the
*same* neighborhoods I01/I02 used.”

**HUMAN DECISION REQUIRED — D2** (primary stability), **D3** (\(k\) role).

---

## 6. Dimensionality / distance concentration

**MATHEMATICAL FACT.** In high-dimensional Euclidean space, under broad
conditions, pairwise distances concentrate: the relative contrast
\((d_{\max}-d_{\min})/d_{\min}\) can vanish as dimension grows, degrading
nearest-neighbor discrimination (classical curse-of-dimensionality / distance
concentration literature).

**PROJECT FACT.** Here \(W_X=20\) — moderate, not ultra-high, but not trivial.
Coordinates are dependent (overlapping construction + standardization), so
*effective* dimension may be \(\ll 20\).

**INTERPRETATION — could false neighbors arise?** Yes: weak contrast + finite
samples can yield unstable “nearest” sets even without meaningful locality.

**INTERPRETATION — could true recurrence look weak?** Yes: concentration +
sparse sampling can flatten recurrence rates relative to intuition.

### Role recommendation (not frozen)

| Role | Candidate | Consequence |
|------|-----------|-------------|
| **Prerequisite diagnostic** | Distance contrast / local effective dimension (past-only) | If degenerate, structural PASS/FAIL may be **INCONCLUSIVE** by design |
| **Primary evidence** | Usually **no** — concentration alone is not “recurrence” | Avoid substituting a diagnostic for the claim |
| **Secondary diagnostic** | Yes | Helps interpret FAIL vs “geometry blind” |
| **Irrelevant** | No | Ignoring concentration risks miscategorizing F4/F5 |

`RECOMMENDED ON METHODOLOGICAL GROUNDS`: treat concentration / local-dimension
style checks as **prerequisite or secondary diagnostics**, not as the primary
estimand (**HUMAN DECISION REQUIRED — D6**).

---

## 7. Temporal-overlap problem (mandatory)

### 7.1 Mathematical contamination

**MATHEMATICAL FACT.** Let \(W=W_X=20\). The raw-return supports of \(X_t\) and
\(X_s\) are \([t-W+1,t]\) and \([s-W+1,s]\). These intervals overlap iff

\[
|t-s| < W.
\]

In particular, \(X_t\) and \(X_{t+1}\) share \(W-1=19\) underlying returns.
Even after causal standardization, the *coordinate vectors* remain nearly
identical for small lags: nearest-neighbor relations at lag \(1,\ldots,W-1\)
are largely **construction artifacts**, not independent revisits of state space.

**MATHEMATICAL FACT (stronger dependence channel).** Standardization uses a
window of length \(M=252\). Even when return windows are disjoint
(\(|t-s|\ge W\)), \(\hat\mu_t,\hat\sigma_t\) and \(\hat\mu_s,\hat\sigma_s\) still
share most of their estimation sample whenever \(|t-s|<M\). This does **not**
force identical \(X\), but induces **serial dependence of the standardized
coordinates** beyond pure return-window overlap.

### 7.2 What exclusion prevents

| Exclusion | Prevents | Does not prevent |
|-----------|----------|------------------|
| \(\tau \ge W_X\) (i.e. \(|t-s|\ge W_X\)) | Shared return coordinates / trivial sliding-window matches | Shared standardization (\(M\)); vol clustering; true short-memory dynamics |
| \(\tau \ge M\) | Shared standardization windows as well | Economic regime persistence longer than \(M\); marginal/vol null structure |
| \(\tau > M\) (extra) | Some additional short-lag dynamical dependence | Requires independent justification (ACF, space-time separation) — **DoF** |

### 7.3 Doctrine options (**HUMAN DECISION REQUIRED — D4**)

| Option | Rule | Forced? |
|--------|------|---------|
| **D4-A** | Minimum overlap exclusion only: \(\tau_{\min}=W_X\) (no neighbor with \(|t-s|<W_X\)) | **Mathematically forced** as lower bound against F1 |
| **D4-B** | Standardization-aware: \(\tau_{\min}=M=252\) | Not forced by return overlap; justified if shared \(\mu/\sigma\) is deemed trivial contamination |
| **D4-C** | D4-A primary + preregistered robustness at a second larger \(\tau\) (e.g. literature Theiler-style), **without** data-chosen \(\tau\) | Extra \(\tau\) values need non-data justification |

`RECOMMENDED ON METHODOLOGICAL GROUNDS`:

1. **Adopt D4-A as hard invariant** (non-negotiable against F1).
2. Treat D4-B vs “D4-A + optional robustness \(\tau\)” as the real human choice.
3. **Do not** pick numerical \(\tau>W_X\) from market ACF in this pre-framing
   (would be data-dependent DoF). If extra exclusion is desired, justify by
   *contract* (e.g. \(\tau=M\)) or by a preregistered rule that does not peek
   at the analysis sample’s recurrence scores.

**LITERATURE PRACTICE.** Theiler windows in recurrence / correlation-dimension
work exclude temporally correlated neighbors around the line of identity
(Theiler 1986; standard RQA practice). Choice often uses ACF decay or
space-time separation plots — informative, but **data-adaptive \(\tau\) is a
researcher DoF** that must be controlled if used.

---

## 8. Candidate null models (central)

A “recurrence” finding is meaningless without a null that preserves nuisance
properties capable of faking recurrence.

### 8.1 Family table

| ID | Sketch | Destroys | Preserves | Controls | Fails to control | Too weak? | Too strong? | Fitted params? | Extra DoF |
|----|--------|----------|-----------|----------|------------------|-----------|-------------|----------------|-----------|
| **N0** | IID / global permutation of returns (or of \(X\) if mis-applied) | Almost all temporal structure | Marginal distribution (if permuting returns) | Pure marginal shape | Vol clustering, AC, nonstationarity | **Yes** for finance | Rarely | Minimal | Low |
| **N1** | Distribution-preserving temporal shuffle of returns | Time order / path structure | Exact marginal of shuffled object | Marginal-driven fake geometry | Dependence, vol persistence | Often **yes** | Can be strong vs “any time structure” | Minimal | Low–med |
| **N2** | Block shuffle / moving-block surrogate | Long-range / cross-block state structure | Short-block dependence | Short-memory artifacts | Choice of block length; nonstationarity across blocks | Depends on block | Long blocks preserve too much “state” | Block length | **High** (block) |
| **N3** | Linear surrogates (phase-randomization / FT; IAAFT) | Nonlinear state recurrence beyond linear AC/spectrum | Spectrum (FT); spectrum+marginal (IAAFT) | Linear correlation / spectral nuisance | Heteroskedasticity; regime switching | Can be weak if vol rules | Can reject “interesting” linear structure if claim is broader | Spectrum est. | Med |
| **N4** | Volatility-preserving / heteroskedastic surrogate (e.g. shuffle standardized residuals under a frozen vol skeleton; GARCH residual shuffle — *conceptual*) | Residual state path beyond vol | Vol clustering / magnitude path (as specified) | **F2** vol-level recurrence | Misspecified vol model; residual dependence | If vol model wrong | If vol skeleton retains state labels | Vol model | **High** |
| **N5** | Geometry-specific synthetic: preserve chosen marginals / norms of \(X\) but destroy temporal embedding structure | Temporal arrangement of states | Selected \(X\)-marginal geometry | Finite-sample density + marginal cloud shape (**F3/F4**) | Dynamics that create true revisits | If too little preserved | If “preserve local geometry” destroys the estimand | Construction recipe | High |

### 8.2 Weak vs strong

- **Too weak (F8):** N0/N1 alone — almost any financial series will “reject”
  them; PASS becomes cheap and scientifically thin.
- **Too strong (F9):** A null that preserves nearly the same local \(X\)-path
  structure one claims to test — FAIL becomes almost automatic; claim vacuous.

### 8.3 Hierarchy vs single null

**INTERPRETATION.** A **hierarchy** is scientifically preferable to one
arbitrary null:

```text
N0/N1  (sanity: beats pure marginal?)
   ->
N3     (beats linear spectral structure?)
   ->
N4     (beats volatility persistence?)
   ->
optional N2/N5 as robustness
```

Reading rule (conceptual, MS-analogue):

| Pattern | Interpretation |
|---------|----------------|
| Fails to beat N0/N1 | Strong FAIL — not even above marginal |
| Beats N0/N1, fails N3/N4 | Structure compatible with linear/vol nuisance — **not** G0-state claim |
| Beats N4 (and weaker) | Strongest support for intrinsic state recurrence beyond vol |
| Disagreement across nulls | **INCONCLUSIVE** unless preregistered primacy order |

`RECOMMENDED ON METHODOLOGICAL GROUNDS`: **hierarchical null doctrine** with a
**predeclared primary null** (likely N4 *or* N3 — human choice) and weaker
nulls as necessary diagnostics — **not** “pick the null that passes.”

**Do not freeze N\* here.** **HUMAN DECISION REQUIRED — D5.**

---

## 9. Causal / no-future information boundary

**Hard invariant.** Structural evidence must not depend on:

\(Y_t\), \(V_{t,h}\), \(\mathcal{H}_{\mathrm{raw/vol/shape}}\) *future*
homogeneity, CRPS, \(D\), \(R\), PnL, trading signals.

### 9.1 Legitimate information at analysis time \(u\)

**INTERPRETATION (proposed boundary):**

| Allowed | Forbidden |
|---------|-----------|
| Prices/returns with index \(\le u\) when forming \(X_u\) | Any return with index \(>u\) in estimands |
| Distances \(d_0(X_a,X_b)\) for admissible pairs with \(a,b\le T_{\mathrm{anal}}\) | Using future segments to choose \(\tau\), \(k\), splits, or null params |
| Past-only perturbations of coordinates known at \(t\) | Perturbations defined using future residuals |
| Null generation using only information allowed by the null’s past-only recipe | Fitting a global model on the full sample then claiming causal neighborhoods without freeze discipline |
| Predeclared calendar splits using time indices only | Splits chosen to isolate 2008/2009/2020 after seeing scores |

### 9.2 Leakage channels to block in design

| Channel | Risk | Prevention layer |
|---------|------|------------------|
| Global standardization fitted on full sample | **F13** | Keep causal \(M\)-window contract; forbid full-sample z-scoring |
| Null model fit on full path including “future” relative to query | Leakage | Fit-forward or global-but-symmetric null with preregistered justification |
| Segment selection by outcome | Contamination | Time-only splits |
| Diagnostic using I01 residual years as targets | Post-hoc | Forbidden as primary; known contamination from geometry review §10 |

---

## 10. Candidate evidence families

Only after §§4–9. **Not** mandatory metrics; **no** calculation.

| Family | Operationalizes | Needs null? | Major DoF | Interpretability | Circularity risk | Clear P/F/I? |
|--------|-----------------|-------------|-----------|------------------|------------------|--------------|
| Neighbor-set overlap (Jaccard etc. on \(N(t)\)) | R1/R2 + S3/S5 | Yes | \(k,\tau\) | High | Low if past-only | Yes if null hierarchy set |
| Rank stability under perturbation | S1 + S5 | Yes (vs null perturbations) | Perturbation law | Medium | High if law tuned | Yes if law frozen |
| Recurrence rate / ε-ball rate | R3 | Yes | ε or adaptive ε | Medium | High if ε data-mined | Yes if ε doctrine fixed |
| Recurrence-time distribution | R3 | Yes | Censoring, τ | Medium | Med | Often I if heavy tails |
| Cross-period neighborhood preservation | R4 + S2 | Yes | Split | High for nonstationarity | Med | Yes |
| Local distance contrast | Dimensionality diagnostic | Optional | Window | Diagnostic | Low | Supports I more than P/F |
| Perturbation sensitivity curves | S1 | Yes | Magnitude grid | Medium | High (F12) | Yes if grid preregistered |
| Local-dimension diagnostics | Density / F4–F5 | Optional | Method | Low–med | Low | Better as diagnostic |

**INTERPRETATION.** A minimal discriminating design typically pairs:

- one **recurrence** family (R1/R3-style) under **τ ≥ W_X**,
- one **stability** family (S2 and/or S1),
- a **null hierarchy** with declared primary null,
- concentration as **diagnostic**.

Exact bundle waits on D1–D8.

---

## 11. Adversarial failure modes

| ID | Mechanism | Consequence | Prevention | Layer |
|----|-----------|-------------|------------|-------|
| **F1** | Overlapping windows → trivial near neighbors | Fake R1/R3 | Hard \(\tau\ge W_X\) | Design |
| **F2** | Vol level clustering → “same state” | Fake geometry = vol | N4 primary or co-primary; vol diagnostics | Design + diagnostics |
| **F3** | Heavy-tailed marginals shape clouds | Fake density structure | N1/N5 | Design |
| **F4** | Finite-sample density accidents | Unstable neighbors | S3; density diagnostics | Diagnostics |
| **F5** | Distance concentration | Ranks meaningless | Prerequisite contrast checks → INCONCLUSIVE if degenerate | Diagnostics + interpretation |
| **F6** | Nonstationarity read as recurrence | Misleading PASS | R4/S2; segment reports | Design + interpretation |
| **F7** | One episode dominates | Non-transportable “structure” | Cross-period; forbid post-hoc crisis targeting | Design |
| **F8** | Null too weak (N0 only) | Cheap PASS | Hierarchy; primary ≥ N3/N4 | Design |
| **F9** | Null too strong | Forced FAIL | Declare what null may destroy; don’t preserve estimand | Design |
| **F10** | Single \(k\) artifact | Non-robust claim | D3-B/C | Design |
| **F11** | Split fishing | False S2 | Preregister split rule | Design |
| **F12** | Post-hoc perturbation size | False S1 | Freeze perturbation family | Design |
| **F13** | Global normalization | Leakage / non-causal \(X\) | Causal \(M\) only | Implementation |
| **F14** | Multi-definition fishing | False discovery | Single primary claim + limited robustness; no best-star | Design + interpretation |

---

## 12. Discriminating power / identifiability

Competing explanations:

| ID | Claim |
|----|-------|
| **E1** | \(X\) has recurrent structure and L2 captures it |
| **E2** | \(X\) has structure but L2 does not represent it reliably |
| **E3** | \(X\) itself lacks stable recurrent state structure |
| **E4** | Apparent recurrence is trivial (overlap / vol / marginal) |
| **E5** | Structure exists but is strongly nonstationary |

### What fixed G0 **can** identify

| Outcome pattern (conceptual) | Favors |
|------------------------------|--------|
| Excess recurrence/stability vs primary null including vol, with τ≥W_X, cross-period OK | **E1** (on this object) |
| Beats weak nulls only; fails N4 | **E4** (vol/marginal) more than E1 |
| Strong within-period, fails cross-period | **E5** |
| Degenerate distance contrast / unstable ranks even locally | E2 *or* E3 — **not separated** |
| No excess vs well-posed null hierarchy | Not-E1 for G0; compatible with E3 or E2 |

### What fixed G0 **cannot** identify

**MATHEMATICAL / LOGICAL LIMIT.**

- An experiment that **only** studies \(X+d_0\) **cannot fully separate E2 from E3**.
  Distinguishing “bad metric on good \(X\)” from “bad \(X\)” requires either an
  alternative metric (GM — out of scope for Frame A primary) or an alternative
  representation (GR), or an auxiliary structural criterion independent of \(d_0\).
- FAIL under G0 does **not** imply “markets have no geometry.”
- PASS under G0 does **not** imply PRED value (I01/I02 already constrain PRED).

---

## 13. PASS / FAIL / INCONCLUSIVE semantics

Refine before any numerical gates.

### PASS (structural)

Evidence supports **nontrivial intrinsic recurrence and/or stability of current
G0** beyond the **preregistered** nuisance/null class, under the preregistered
primary meanings of recurrence/stability, with hard temporal exclusion
\(\tau\ge W_X\), **without** use of future returns.

PASS authorizes a **structural SCI-path claim about G0 localities** only to the
extent D8 allows — **not** PRED, not ECON, not “geometry in general.”

### FAIL

Under the preregistered test, current G0 does **not** demonstrate the required
structural property (e.g. no excess vs primary null; or primary stability fails).

FAIL means: **this \(X+\mathrm{L2}\) baseline lacks evidenced intrinsic
recurrence/stability as defined** — not “geometry is impossible.”

### INCONCLUSIVE

Includes at least:

- defensible primary definitions disagree under preregistered dual read;
- null hierarchy yields incompatible conclusions without a primacy rule;
- insufficient effective sample / pool after exclusion;
- distance-concentration / degeneracy diagnostics trip;
- design cannot discriminate the explanations the claim asserted;
- implementation/contract defects (then INVALID until fixed — separate from
  scientific INCONCLUSIVE).

**No numerical thresholds here.**

---

## 14. Outcome decision tree

```text
I03 PASS (if opened; structural)
    ->
    G0 earned a limited structural claim (scope = D8)
    ->
    future work MAY ask whether that structure carries PRED value
       (new investigation; not automatic; I01/I02 contamination applies)
    ->
    does NOT unlock metric shopping
    ->
    does NOT unlock ECON

I03 FAIL
    ->
    do NOT conclude "markets have no geometry"
    ->
    current X+L2 structural baseline unsupported under the frozen claim
    ->
    human may consider later GR (representation) and/or GM (metric)
       as *new* questions — not silent retunes of I03
    ->
    or pause geometric-neighborhood branch (program decision)

I03 INCONCLUSIVE
    ->
    name the blocking issue (null conflict / degeneracy / split / power / ...)
    ->
    redesign decision dossier or stop — do NOT mine thresholds
```

No automatic next experiment.

---

## 15. Human decisions required (D1–D8)

Compact decision table. Cursor marks methodological leanings; **humans choose**.

### D1 — Primary scientific meaning of recurrence

| Option | Content | Math consequence | Advantage | Risk | DoF |
|--------|---------|------------------|-----------|------|-----|
| **D1-A** | Primary = **R1** (NN recurrence with τ) | Claim about separated nearest matches | Closest to G0 kNN practice | May pass via isolated matches without cloud structure | \(k\) |
| **D1-B** | Primary = **R3** (temporal return structure) | Claim about return times/rates | Dynamical clarity | Radius/\(k\) dual; vol-driven returns | ε or \(k\) |
| **D1-C** | Primary = **R2** (neighborhood composition) | Stronger than R1 | Blocks lone-match artifacts | Harder to operationalize cleanly | Composition score |
| **D1-D** *(combo)* | Primary R1 or R3, with R4 as **required co-claim** | Must transport across periods | Blocks F6/F7 | Power; split DoF | Split |

`RECOMMENDED ON METHODOLOGICAL GROUNDS`: **D1-A or D1-B**, with **R4 as either
primary co-claim or mandatory robustness** (see D7) — avoid R2-only as first
I03 unless composition scoring is frozen tightly.

### D2 — Primary meaning of stability

| Option | Content | Consequence | Advantage | Risk | DoF |
|--------|---------|-------------|-----------|------|-----|
| **D2-A** | **S2** temporal stability primary | Aligns with transport | Blocks episode PASS | Split doctrine | High if split free |
| **D2-B** | **S1** perturbation primary | Probes locality sharpness | Direct “meaningful neighborhood” | Perturbation law (F12) | High |
| **D2-C** | **S5** rank stability primary | Ordinal robustness | Less scale-sensitive | May be weak | Med |
| **D2-D** | Bundle S2 + (S1 or S5) | Stricter PASS | Strong scientific content | More INCONCLUSIVE risk | Higher |

`RECOMMENDED ON METHODOLOGICAL GROUNDS`: **D2-A** as primary for Frame A
“intrinsic structure,” with S1/S5 secondary — unless humans prioritize locality
mechanics (then D2-B).

### D3 — Role of \(k\) / neighborhood scale

| Option | Content | Consequence | Advantage | Risk | DoF |
|--------|---------|-------------|-----------|------|-----|
| **D3-A** | Fix \(k=50\) inherited | Tests *same* neighborhoods as I01/I02 | Continuity with G0 PRED object | F10; PRED hyperparameter leakage into structure | Low |
| **D3-B** | Preregistered small \(k\)-set; MS-style; no best-\(k\) | Scale-robust claim | Blocks F10 | Multiplicity | Med |
| **D3-C** | Primary not \(k\)-defined (rate/radius/rank); \(k\) diagnostic only | Cleaner structural object | Avoids inheriting PRED \(k\) | Radius DoF instead | Med |

`RECOMMENDED ON METHODOLOGICAL GROUNDS`: **D3-B** if D1 uses neighborhoods;
**D3-C** if D1-B with radius doctrine. Prefer **not** D3-A unless the explicit
question is “structure of the I01/I02 \(k{=}50\) object.”

### D4 — Temporal exclusion doctrine

| Option | Content | Consequence | Advantage | Risk | DoF |
|--------|---------|-------------|-----------|------|-----|
| **D4-A** | Hard \(\tau\ge W_X=20\) only | Removes return-window overlap | Mathematically forced floor | Leaves shared \(M\)-std dependence | Low |
| **D4-B** | Hard \(\tau\ge M=252\) | Also removes shared std windows | Stronger anti-trivial dependence | Heavy power loss; may over-exclude true short revisits | Low (contractual) |
| **D4-C** | D4-A hard + one preregistered larger contractual \(\tau\) (not ACF-mined) | Robustness without data fishing | Balanced | Which second \(\tau\)? | Med |

`RECOMMENDED ON METHODOLOGICAL GROUNDS`: **D4-A as invariant**; choose **D4-B or
D4-C** for the scientific exclusion doctrine beyond overlap. **Do not**
data-mine \(\tau\).

### D5 — Null-model doctrine

| Option | Content | Consequence | Advantage | Risk | DoF |
|--------|---------|-------------|-----------|------|-----|
| **D5-A** | Primary **N3** (linear/spectral); N0/N1 diagnostic | Classic surrogate logic | Standard lit | May miss vol-driven fake recurrence (F2) | Med |
| **D5-B** | Primary **N4** (vol-preserving); N0/N1/N3 diagnostic ladder | Directly attacks F2 | Matches I01 vol dominance lesson | Vol-model DoF (F9 if overbuilt) | **High** |
| **D5-C** | **Hierarchy with dual primaries** (must beat N3 *and* N4) | Strict PASS | Strong claim | More INCONCLUSIVE / F9 | High |
| **D5-D** | Primary N2 only | Dependence-aware shuffle | Simple | Block-length DoF; weak vs vol | High |

`RECOMMENDED ON METHODOLOGICAL GROUNDS`: **D5-B or D5-C**, given I01’s volatility
dominance. Avoid D5-A alone. Avoid N0-only. Specify vol surrogate class at
prereg time without fitting to maximize PASS.

### D6 — Distance-concentration diagnostics

| Option | Content | Consequence | Advantage | Risk | DoF |
|--------|---------|-------------|-----------|------|-----|
| **D6-A** | Prerequisite: degeneracy ⇒ INCONCLUSIVE | Protects interpretation | Blocks F5 mis-PASS/FAIL | Need degeneracy definition | Med |
| **D6-B** | Secondary diagnostic only | Soft warning | Flexible | Ignored in practice | Low |
| **D6-C** | Irrelevant / omit | Simpler | — | Blind to F4/F5 | — |

`RECOMMENDED ON METHODOLOGICAL GROUNDS`: **D6-A**.

### D7 — Cross-period stability in the primary claim?

| Option | Content | Consequence | Advantage | Risk | DoF |
|--------|---------|-------------|-----------|------|-----|
| **D7-A** | Yes — R4/S2 **inside** primary PASS | Transport required | Blocks F6/F7; stronger SCI | Power; split rule | Split |
| **D7-B** | No — cross-period **robustness only** | Easier PASS | Power | Episode-dominated PASS possible | Lower |
| **D7-C** | Separate co-equal estimands (recurrence ∧ stability reported; PASS needs both) | Transparent | Clear semantics | More INCONCLUSIVE | Med |

`RECOMMENDED ON METHODOLOGICAL GROUNDS`: **D7-A or D7-C** for a claim worth a
structural SCI path; **D7-B** only if humans accept weaker authorization under D8.

### D8 — What PASS authorizes scientifically

| Option | Authorization | Advantage | Risk |
|--------|---------------|-----------|------|
| **D8-A** | “G0 localities exhibit nontrivial recurrence/stability beyond preregistered nulls” — **structural only**; unlocks *permission to ask* PRED later | Tight | None if respected |
| **D8-B** | Same + “supports continued investment in G0 neighborhoods as scientific objects” | Program clarity | Soft mission creep |
| **D8-C** | Any language implying PRED, edge, or “geometry works for trading” | — | **Forbidden** — reject |

`RECOMMENDED ON METHODOLOGICAL GROUNDS`: **D8-A** (optionally + D8-B program
note). **Reject D8-C.**

---

## 16. Recommendation for I03 formulation

**Proposal for human approval — not an opened investigation.**

Contingent on humans accepting methodological leans (D4-A invariant; null
hierarchy with vol-aware primary; concentration as prerequisite; PASS ≠ PRED):

> Under hard temporal exclusion of overlapping return windows
> (\(\tau \ge W_X\)) and the existing causal G0 contract
> (\(W_X=20\), \(M=252\), Euclidean \(d_0\)), does the current representation
> \(X\) exhibit [D1-primary recurrence] with [D2-primary stability]
> beyond a preregistered [D5 null hierarchy], without using any future-return
> target?

**Illustrative filled form** *(only if humans pick the recommended leans —
still not frozen)*:

> Under \(\tau \ge W_X\), causal G0 fixed, does \(X\) exhibit separated
> nearest-neighbor / temporal recurrence that is temporally transportable
> across preregistered segments, beyond a volatility-preserving primary null
> (with weaker marginal/linear nulls as diagnostics), with distance-contrast
> degeneracy yielding INCONCLUSIVE rather than PASS/FAIL?

No thresholds, datasets, code, or gates.

---

## 17. References

See [references.md](references.md) for bibliographic detail.

**Internal:** geometry review `547fc57`; I01 synthesis; I02 closure (EXPL-ABSENT);
AGENTS.md / DR-007.

**External (definitional):** Theiler (1986) temporal exclusion; Theiler et al.
(1992) surrogate data; Schreiber–Schmitz IAAFT; Marwan et al. RQA; Kantz–
Schreiber nonlinear time-series; distance concentration / NN in high dimension
(e.g. Beyer et al.; Aggarwal et al.).

---

## Document control

| Field | Value |
|-------|-------|
| ID | I03-INTRINSIC-RECURRENCE-DECISION-v0.1 |
| Directory | `research/I03-pre/` only |
| Opens I03? | **No** |
| Freezes D1–D8? | **No** — human pass required |
