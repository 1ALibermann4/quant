# I03 — C1–C10 freeze record (DESIGN finalization)

> **STATUS :** C1–C10 FROZEN — **HD-N4-SCALE = SCALE-W**  
> **Authority class :** RESEARCH / PROTOCOL  
> **Baseline design :** `15ab106` · [I03-DESIGN-v0.1.md](I03-DESIGN-v0.1.md)  
> **D1–D8 :** [I03-D1-D8-FREEZE.md](I03-D1-D8-FREEZE.md) — **not reopened**  
> **HD-N4-SCALE :** [I03-HD-N4-SCALE-FREEZE.md](I03-HD-N4-SCALE-FREEZE.md) — \(W_\sigma=20\)  
> **Preregistration :** [I03-PREREG-v0.1.md](I03-PREREG-v0.1.md)

```text
I03 STATUS = DESIGN + PREREG DRAFT COMPLETE
HD-N4-SCALE = SCALE-W (W_sigma = 20)
NO MARKET DATA USED TO CHOOSE SCALE
NO EXPERIMENT RUN
NO IMPLEMENTATION IN THIS FREEZE
NO SCI / PRED / ECON CLAIM
```

---

## 0. Rejected tautology (motivates C1 refinement)

**MATHEMATICAL FACT.** Under fixed-\(k\) nearest neighbors, if the admissible
pool satisfies \(\lvert A_t\rvert \ge k\), the set \(N_k^\tau(t)\) **always**
contains exactly \(k\) indices. Therefore any “recurrence rate” defined as

\[
\frac{1}{\lvert\mathcal{T}\rvert}
\sum_{t\in\mathcal{T}}
\mathbf{1}\{\lvert N_k^\tau(t)\rvert = k\}
\]

is identically 1 whenever queries are restricted to sufficient pools. That
statistic measures **pool adequacy**, not revisit structure. It cannot differ
meaningfully between observed G0 and surrogates that preserve the same
calendar and skip rules.

**Consequence.** The DESIGN lean “E-RR as kNN membership rate” is **rejected**
as primary. Primary estimand uses **distances to τ-separated neighbors**
(magnitude of locality), which vary under nulls that destroy state sequencing.

---

## HD-C1 — Primary estimand (FROZEN): E-MND — mean τ-separated k-NN distance

### Objects

| Symbol | Definition |
|--------|------------|
| \(r_t\) | Log-return at trading time index \(t\) (known under causal G0) |
| \(X_t\in\mathbb{R}^{W_X}\) | G0 state: causally standardized return window, \(W_X=20\), \(M=252\) |
| \(d_0(x,y)=\|x-y\|_2\) | Frozen Euclidean geometry |
| \(\tau\) | \(\tau = W_X = 20\) (D4) |
| \(\mathcal{K}\) | \(\{10,25,50\}\) (HD-C2) |
| Block \(B_p\) | Contiguous time block from HD-C5, \(p=1,\ldots,P\) |

### Query states

Within each block \(B_p\), the **query set** \(\mathcal{T}_p\) is the set of
indices \(t\in B_p\) such that:

1. \(X_t\) is defined under G0 (including skip if \(\hat\sigma_t=0\));
2. the admissible pool \(A_t^{(p)}\) (below) satisfies \(\lvert A_t^{(p)}\rvert \ge k_{\max}\)
   with \(k_{\max}=50\) (so the same queries are comparable across all \(k\in\mathcal{K}\));
3. no future returns enter \(X_t\) or the estimand.

### Admissible historical states (within-block, τ-exclusion)

\[
A_t^{(p)}
=
\bigl\{
s\in B_p
:\ 
\lvert t-s\rvert \ge \tau,\ 
X_s\text{ defined}
\bigr\}.
\]

**Only same-block** indices enter \(A_t^{(p)}\). Cross-period stability is
enforced by requiring the structural property **in each block**, not by
pooling neighbors across blocks (avoids leakage of “one long episode” into
every query).

### Neighborhood / local distances

Order admissible distances:

\[
d_{(1)}^\tau(t;p)
\le
d_{(2)}^\tau(t;p)
\le
\cdots
\le
d_{(\lvert A_t^{(p)}\rvert)}^\tau(t;p)
\]

where \(d_{(j)}^\tau(t;p)\) is the \(j\)-th smallest \(d_0(X_t,X_s)\) over
\(s\in A_t^{(p)}\). Ties broken deterministically by \((\mathrm{distance}\uparrow,\,s\uparrow)\)
as in I02 spirit (implementation contract later).

For \(k\in\mathcal{K}\):

\[
\delta_k(t;p)
:=
d_{(k)}^\tau(t;p).
\]

**Interpretation.** \(\delta_k(t;p)\) is the radius needed to capture \(k\)
τ-separated same-block revisits. Smaller ⇒ tighter local recurrence at scale
\(k\).

### Primary cell estimand

\[
\Theta_k^{(p)}
:=
\frac{1}{\lvert\mathcal{T}_p\rvert}
\sum_{t\in\mathcal{T}_p}
\delta_k(t;p).
\]

**Direction.** Lower \(\Theta_k^{(p)}\) = stronger temporal recurrence at scale
\(k\) in block \(p\).

### Null comparison (excess / null-relative)

For null family \(\nu\in\{\mathrm{N4},\mathrm{N3}\}\) and surrogate replicate
\(b=1,\ldots,B_\nu\), recompute the entire pipeline on surrogate returns →
\(X^{\ast(b)}}\) → \(\Theta_k^{(p),\ast(b),\nu}\).

**Cell survival vs \(\nu\)** (one-sided, stronger recurrence):

\[
\hat p_{k,p}^{(\nu)}
=
\frac{
1 + \#\{b:\ \Theta_k^{(p),\ast(b),\nu} \le \Theta_k^{(p)}\}
}{B_\nu + 1}.
\]

Survive \(\nu\) at \((k,p)\) iff \(\hat p_{k,p}^{(\nu)} \le \alpha\)
(observed tightness is extreme in the lower tail of the null).

*(Equivalently: observed \(\Theta\) smaller than the empirical \(\alpha\)-quantile
of surrogate \(\Theta\).)*

### Why this is non-tautological under fixed-\(k\) kNN

1. Fixed \(k\) always yields \(\lvert N_k\rvert=k\) when \(\lvert A_t\rvert\ge k\);
   that **cardinality** is discarded as a statistic.
2. The **radius** \(\delta_k\) is a continuous functional of the configuration
   of τ-separated states; it changes when temporal ordering of innovations is
   destroyed while marginal/vol/spectral nuisances are preserved by N4/N3.
3. Under a null that preserves calendar and pool sizes but destroys state
   sequencing, \(\mathbb{E}^*[\Theta_k^{(p)}]\) need not equal the observed
   \(\Theta_k^{(p)}\). A significant left-tail gap is empirical content, not an
   identity.

### Explicitly rejected primaries

| Rejected | Reason |
|----------|--------|
| \(\mathbf{1}\{\lvert N_k\rvert=k\}\) rate | Tautology under sufficient pools |
| Any future \(Y\), \(V\), CRPS, \(D\), \(R\) | Violates no-future invariant |
| Best-\(k\) selection on \(\Theta\) | Violates D3 / HD-C2 |

**Label:** E-MND (mean neighbor distance), replacing tautological E-RR.

---

## HD-C2 — Multi-scale \(\mathcal{K}\) (FROZEN)

\[
\mathcal{K} = \{10, 25, 50\}.
\]

| \(k\) | Role |
|-------|------|
| 10 | Finer locality |
| 25 | Intermediate |
| 50 | Continuity with historical G0 PRED neighborhoods (not structural “truth”) |

### Rules (frozen)

- Report **all** \(k\in\mathcal{K}\).
- **No** best-\(k\); **no** optimization over \(k\).
- Scale-localized effect **must not** silently become global PASS.

### Semantics (frozen, a priori)

Let \(S_\nu(k,p)\in\{0,1\}\) be the indicator that cell \((k,p)\) **survives**
null \(\nu\) under HD-C1/C7.

For a fixed null \(\nu\) and block \(p\), define the scale pattern
\(v_p^{(\nu)} = \bigl(S_\nu(10,p), S_\nu(25,p), S_\nu(50,p)\bigr)\).

| Term | Definition |
|------|------------|
| **Coherent (block \(p\), null \(\nu\))** | \(S_\nu(k,p)=1\) for **all** \(k\in\mathcal{K}\) |
| **Scale-localized (block \(p\), null \(\nu\))** | At least one \(S_\nu(k,p)=1\) and at least one \(S_\nu(k',p)=0\) |
| **Contradictory (block \(p\), null \(\nu\))** | Reserved for logically inconsistent pipelines (e.g. implementation defects). Ordinary mixed survival is **scale-localized**, not “contradictory.” |
| **Multi-scale coherent globally (null \(\nu\))** | **Every** block \(p=1,\ldots,P\) is coherent under \(\nu\) |

**Global PASS eligibility** requires multi-scale coherence under **both** N4 and
N3 (with HD-C8/C9), not mere scale-localized survival in any cell.

**Scale-localized** ⇒ cannot support PASS; maps to FAIL or INCONCLUSIVE per
truth table (HD-C8), never silent PASS.

---

## HD-C3 — Primary null N4-A (ALGORITHM FROZEN; scale window = FINAL HD)

### Purpose

Preserve nuisance **volatility / local scale** structure motivated by I01;
destroy temporal sequencing of standardized innovations that induces
nontrivial τ-separated state recurrence under G0.

### Existing G0 scale contracts (no data inspection)

| Contract | Value | Role in project |
|----------|-------|-----------------|
| Standardization window | \(M=252\) | Causal \(\mu/\sigma\) inside \(X_t\) |
| Vol window | \(W_{RV}=20\) (= \(W_X\)) | I02 / I01 `rv_W` family |

Both are **methodologically defensible** as N4 scale estimators. Neither is
mathematically forced as *the* vol nuisance skeleton for N4.

### HD-N4-SCALE — RESOLVED as SCALE-W

See [I03-HD-N4-SCALE-FREEZE.md](I03-HD-N4-SCALE-FREEZE.md).
\(W_\sigma=20\). Formula in [I03-PREREG-v0.1.md](I03-PREREG-v0.1.md) §8.

### Algorithm N4-A (complete; scale frozen)


**Inputs:** return path \(\{r_t\}\); scale rule \(\hat\sigma_t\) from HD-N4-SCALE;
seeds; \(B_{\mathrm{N4}}\).

For each surrogate \(b=1,\ldots,B_{\mathrm{N4}}\):

1. **Decomposition.** For every \(t\) with \(\hat\sigma_t\) defined and
   \(\hat\sigma_t > 0\):
   \[
   z_t = r_t / \hat\sigma_t.
   \]
   If \(\hat\sigma_t=0\) or undefined: mark \(t\) as **non-residual** (no \(z_t\)).

2. **Preserve.** The series \(\{\hat\sigma_t\}\) (and the set of times where it
   is defined) is **held fixed**.

3. **Destroy.** Let \(\mathcal{Z}=\{t: z_t\text{ defined}\}\). Draw a uniform
   random permutation \(\pi^{(b)}\) of \(\mathcal{Z}\) (seed stream \(b\)):
   \[
   z_t^{\ast(b)} = z_{\pi^{(b)}(t)}\quad(t\in\mathcal{Z}).
   \]
   (i.i.d. shuffle of residuals — **not** block-shuffle, unless humans later
   authorize a robustness diagnostic.)

4. **Reconstruct returns.**
   \[
   r_t^{\ast(b)} =
   \begin{cases}
   \hat\sigma_t\cdot z_t^{\ast(b)} & t\in\mathcal{Z},\\
   r_t & t\notin\mathcal{Z}\ \text{(deterministic copy; rare)}.
   \end{cases}
   \]

5. **Rebuild G0.** Compute \(X_t^{\ast(b)}\) from \(\{r^{\ast(b)}\}\) with
   **identical** causal \(W_X,M\), skip-on-zero-\(\sigma\) contract as observed G0.

6. **Estimands.** Recompute \(\Theta_k^{(p),\ast(b),\mathrm{N4}}\) on the same
   calendar blocks / query rules.

### Preservation / destruction summary

| Exactly preserved | Approximately preserved | Intentionally destroyed |
|-------------------|-------------------------|-------------------------|
| \(\{\hat\sigma_t\}\) path under frozen scale rule | Unconditional scale occupancy / vol clustering implied by that path | Temporal order of standardized residuals \(\{z_t\}\) |
| Calendar, block cuts, τ, \(\mathcal{K}\), query eligibility rules | Marginal magnitude of returns *conditional on* \(\hat\sigma\) | State-sequence recurrence beyond the vol skeleton |
| G0 reconstruction map | — | Phase relationship between innovation order and \(X\)-geometry |

### Boundary / degeneracy

| Condition | Action |
|-----------|--------|
| \(\lvert\mathcal{Z}\rvert\) too small vs \(n_{\min}\) (HD constants) | N4 **INVALID** → I03 **INCONCLUSIVE** (surrogate degeneracy) |
| \(\hat\sigma_t\) constant for almost all \(t\) | Flag; N4 collapses toward marginal shuffle → **INCONCLUSIVE** |
| Permutation seed collision / non-reproducible RNG | Implementation INVALID until fixed |

### Seeds & count

See Final constants table: \(B_{\mathrm{N4}}=999\); master seed doctrine.

---

## HD-C4 — Adversarial null N3 = IAAFT (FROZEN)

### Contract

1. Apply **IAAFT** to the scalar return series \(\{r_t\}\) over the full analysis
   calendar used for I03 (same indices as observed).
2. From each surrogate return path \(\{r^{\ast(b)}\}\), **fully rebuild** causal
   \(X^{\ast(b)}\) under G0.
3. Recompute \(\Theta_k^{(p)}\) identically.

### What IAAFT preserves / destroys (accurate claims)

**LITERATURE PRACTICE** (Schreiber & Schmitz 1996, 2000):

| Claim level | Content |
|-------------|---------|
| **Approximately preserves** | Power spectrum (linear autocorrelation structure); amplitude histogram / marginal distribution of \(r_t\) |
| **Does not exactly preserve** | Finite-sample spectrum and marginal simultaneously (iterative compromise); higher-order / nonlinear temporal structure |
| **Intentionally destroys** | Nonlinear phase relationships beyond linear spectral + marginal constraints; hence much state-recurrence not implied by spectrum+marginal |

**Do not claim exact preservation** of spectrum or marginal.

### Algorithmic parameters (frozen conventions)

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Max iterations | \(I_{\max}=100\) | Common IAAFT convention; computational |
| Convergence | Stop early if max relative change of sorted amplitudes and of power spectrum bins below \(\varepsilon_{\mathrm{IAAFT}}=10^{-8}\) | Convention-based numerical tolerance — **not** market-tuned |
| Initialization | Start from random shuffle of \(\{r_t\}\) (seeded) then iterate rank-spectrum steps | Standard IAAFT |
| Failure | If not converged at \(I_{\max}\): **accept last iterate** and flag `IAAFT_NONCONVERGED` in artifact; if flag rate \(>5\%\) of surrogates → **INCONCLUSIVE** (surrogate degeneracy) | Policy |

### Seeds & count

\(B_{\mathrm{N3}}=999\); independent seed stream from N4 (Final constants).

---

## HD-C5 — Cross-period doctrine (FROZEN construction; \(P=3\))

### Frozen construction

- **Contiguous equal-length temporal blocks** in calendar index order.
- **Deterministic**; no crisis/event labels; **no** boundaries defined by
  2008 / 2009 / 2020 or other known favorable episodes.
- Within-block admissible pools only (HD-C1).

### Choice of \(P\)

**Constraints (methodological, no empirical scoring):**

| Constraint | Implication |
|------------|-------------|
| \(k_{\max}=50\), \(\tau=20\) | Each block needs enough indices so many \(t\) have \(\lvert A_t^{(p)}\rvert\ge 50\) |
| Cross-period claim | \(P=2\) is minimal against “one episode”; weak generalization |
| Surrogate inference per block | Too large \(P\) → short blocks, unstable \(\Theta\), frequent INCONCLUSIVE |
| Conjunction PASS (all blocks coherent) | Large \(P\) makes PASS extremely stringent |

**Candidates:** \(P\in\{2,3,4\}\).

**RECOMMENDED AND FROZEN:** \(P=3\) — dominant balance between rejecting
single-episode PASS and preserving per-block effective sample / stable
surrogate tests. \(P=2\) too weak for D7 spirit; \(P=4\) acceptable but
materially harsher without methodological necessity a priori.

### Remainder observations

Let analysis index set be \(\{t_0,\ldots,t_{T-1}\}\) in increasing order
(\(T\) length).

\[
L = \lfloor T / P\rfloor,
\quad
R = T \bmod P.
\]

Blocks (deterministic):

\[
\begin{aligned}
B_1 &= \{t_0,\ldots,t_{L-1}\},\\
B_2 &= \{t_L,\ldots,t_{2L-1}\},\\
B_3 &= \{t_{2L},\ldots,t_{3L-1}\},
\end{aligned}
\]

with the **remainder** \(\{t_{3L},\ldots,t_{T-1}\}\) (length \(R<P\))
**appended to the last block** \(B_P\) (here \(B_3\)). No remainder is dropped;
no remainder forms a crisis-sized custom block.

If after construction any block fails \(n_{\min}\) (Final constants) →
**INCONCLUSIVE** (insufficient effective sample), not FAIL.

---

## HD-C6 — Locality validity (FROZEN): C6-D with inference/hard gates

### Quantities (past-only, within block, τ-respecting)

For \(t\in\mathcal{T}_p\):

\[
\delta_1(t;p) = d_{(1)}^\tau(t;p).
\]

Draw \(m=50\) indices uniformly from \(A_t^{(p)}\) without replacement (seeded
diagnostic RNG); let \(\bar d_{\mathrm{rand}}(t;p)\) be their mean \(d_0\) to
\(X_t\). If \(\lvert A_t^{(p)}\rvert < m\), use all admissible states.

**Diagnostic 1 — NN/random ratio**

\[
\lambda(t;p) = \frac{\delta_1(t;p)}{\bar d_{\mathrm{rand}}(t;p)},
\quad
\Lambda_p = \mathrm{median}_{t\in\mathcal{T}_p}\lambda(t;p).
\]

**Diagnostic 2 — distance contrast at \(k_{\max}\)**

\[
\gamma(t;p)
=
\frac{d_{(k_{\max})}^\tau(t;p) - d_{(1)}^\tau(t;p)}{d_{(1)}^\tau(t;p)},
\quad
\Gamma_p = \mathrm{median}_{t\in\mathcal{T}_p}\gamma(t;p).
\]

### Why both

| Diagnostic | Guards |
|------------|--------|
| \(\Lambda_p\) | NN no closer than random admissible states (vacuous locality) |
| \(\Gamma_p\) | Near-equal distances among first \(k_{\max}\) neighbors (rank/distance concentration) |

### Degeneracy → INCONCLUSIVE (not FAIL)

**Hard (mathematically forced interpretation):**

- If \(\Lambda_p \ge 1\) for any block \(p\) → **locality degenerate** in that
  block → global verdict **INCONCLUSIVE** (cannot interpret G0 neighborhoods).

**Inference-based contrast gate (no mined constant):**

Compare observed \(\Gamma_p\) to the distribution of \(\Gamma_p^{\ast}\) under
**N4** surrogates (validity uses primary nuisance null’s geometry, not a free
threshold). Declare contrast-degenerate in block \(p\) if observed \(\Gamma_p\)
is **not larger** than the median of \(\{\Gamma_p^{\ast(b),\mathrm{N4}}\}\)
*and* absolute level satisfies \(\Gamma_p = 0\) within numerical tol
\(10^{-15}\) **OR** more simply:

**Frozen contrast rule:** block \(p\) is contrast-degenerate iff

\[
\Gamma_p \le \mathrm{median}_b \Gamma_p^{\ast(b),\mathrm{N4}}
\quad\text{and}\quad
\Lambda_p \ge \mathrm{median}_b \Lambda_p^{\ast(b),\mathrm{N4}}.
\]

Meaning: observed data shows **no more** NN-vs-random separation **and** **no
more** neighbor-distance contrast than the vol-preserving null’s typical
geometry — locality adds nothing interpretable beyond N4 nuisance geometry →
**INCONCLUSIVE**.

*(If hard \(\Lambda_p\ge 1\) already tripped, stop.)*

Validity diagnostics are **not** recurrence estimands and **cannot** create PASS.

---

## HD-C7 — Inference (FROZEN)

### Batteries

| Null | Ensemble size | Role |
|------|---------------|------|
| N4 | \(B_{\mathrm{N4}}=999\) | Primary |
| N3 | \(B_{\mathrm{N3}}=999\) | Adversarial |

Independent seed streams (Final constants). \(\alpha=0.05\).

### Test

Per cell \((k,p,\nu)\): left-tail Monte Carlo p-value \(\hat p_{k,p}^{(\nu)}\)
as in HD-C1 (smaller \(\Theta\) = stronger recurrence).

### Multiplicity doctrine — **conjunction / coherence**, not generic FWER maze

The scientific claim is inherently a **conjunction**:

\[
\text{coherent survival on all }k\in\mathcal{K}
\text{ and all }p\in\{1,\ldots,P\}
\text{ under N4 and under N3}.
\]

Therefore:

- **No** Bonferroni/Holm across \(\mathcal{K}\times P\times\{\mathrm{N4},\mathrm{N3}\}\).
- Cellwise tests at level \(\alpha\) feed **coherence predicates** (HD-C2).
- This is stricter than “any cell wins” and matches the claim; it avoids a
  large generic multiple-testing framework.

---

## HD-C8 — Verdict gates + truth table (FROZEN)

### Principles

- **PASS is stringent** (asymmetric).
- **NOT PASS ≠ automatic FAIL.**
- FAIL only when a **valid** experiment affirmatively shows absence of the
  required property under the frozen primary reading.
- INCONCLUSIVE for validity/sample/surrogate/discrimination failures and for
  specified disagreement patterns (HD-C9).

### Predicates

| Symbol | Meaning |
|--------|---------|
| \(V\) | Locality validity OK on **all** blocks (HD-C6) |
| \(E\) | Effective sample OK: \(\lvert\mathcal{T}_p\rvert \ge n_{\min}\) ∀p; N4/N3 not INVALID |
| \(C_4\) | Multi-scale coherent globally under **N4** (all \(k\), all \(p\)) |
| \(C_3\) | Multi-scale coherent globally under **N3** |
| \(L_4\) | Scale-localized under N4 in at least one block, and not \(C_4\) |
| \(L_3\) | Scale-localized under N3 in at least one block, and not \(C_3\) |
| \(F_4\) | Under N4: **no** cell survives in a reading that still has \(V\land E\) — specifically: for every block \(p\), \(S_{\mathrm{N4}}(k,p)=0\) for all \(k\) (uniform non-survival) |
| \(F_3\) | Analogous uniform non-survival under N3 |

### Exhaustive truth table (given \(V\land E\); else INCONCLUSIVE)

| \(C_4\) | \(C_3\) | \(F_4\) | Pattern notes | Verdict |
|-------|-------|-------|---------------|---------|
| 1 | 1 | 0/1 | ND-1 | **PASS** |
| 1 | 0 | 0 | N4 coherent; N3 not; not uniform N3 fail necessarily | **INCONCLUSIVE** (null disagreement / adversarial) |
| 0 | 1 | 0 | N3 coherent; N4 not | **INCONCLUSIVE** if not \(F_4\); else see below |
| 0 | 0 | 1 | Primary N4 uniformly fails | **FAIL** |
| 0 | 0 | 0 | Mixed/scale-localized / partial | **INCONCLUSIVE** |
| 1 | 0 | 1 | Impossible logically if \(C_4\Rightarrow\neg F_4\) | — |
| 0 | 1 | 1 | N4 uniform fail; N3 coherent | **FAIL** (primary null decides absence for broad claim) |

Additional:

| Condition | Verdict |
|-----------|---------|
| \(\neg V\) | **INCONCLUSIVE** |
| \(\neg E\) | **INCONCLUSIVE** |
| IAAFT nonconvergence rate \(>5\%\) | **INCONCLUSIVE** |
| Scale-localized only (\(L_4\) or \(L_3\)) without \(C_4\land C_3\) | **INCONCLUSIVE** (not PASS; not automatic FAIL) |
| Cross-period: some blocks coherent, others uniformly fail N4 | **INCONCLUSIVE** (blocks global claim; not silent FAIL unless \(F_4\) globally as defined) |

**PASS requires:** \(V\land E\land C_4\land C_3\) (and thus ND-1).

**FAIL requires:** \(V\land E\land F_4\) (affirmative primary-null rejection of
the structural property), including the case where N3 is coherent but N4
uniformly fails.

---

## HD-C9 — Null disagreement (FROZEN)

| Code | Pattern | Meaning | Verdict impact |
|------|---------|---------|----------------|
| **ND-1** | Survives N4 **and** N3 with multi-scale global coherence | Eligible for PASS | PASS iff other gates OK |
| **ND-2** | N4 coherent survival; N3 does not | Beyond vol plausible; linear/spectral nuisance not cleared | **INCONCLUSIVE** for broad I03 claim; record restricted interpretation |
| **ND-3** | N3 coherent; N4 does not | Spectral null cleared but **vol-primary** not | If \(F_4\): **FAIL**; else **INCONCLUSIVE** |
| **ND-4** | Neither coherent; if \(F_4\) | No residual recurrence beyond vol skeleton | **FAIL** |
| **ND-5** | Mixed scale/period patterns | Non-equivalent cell pattern | **INCONCLUSIVE** |

Default: genuine disagreement without uniform primary failure →
**INCONCLUSIVE**, not FAIL.

---

## HD-C10 — Secondary diagnostic whitelist (FROZEN)

Every item labeled **`DIAGNOSTIC — NON-PROMOTIONAL`**.

| Allowed | Purpose |
|---------|---------|
| HD-C6 \(\Lambda_p,\Gamma_p\) + surrogate references | Locality validity |
| N4: histogram of \(\hat\sigma\); count of zero-scale skips; shuffle seed audit | Surrogate generation audit |
| N3: IAAFT convergence flags; spectrum/marginal diagnostics vs target | Surrogate generation audit |
| Tables of \(S_\nu(k,p)\) and \(\Theta_k^{(p)}\) vs null quantiles | Explain preregistered verdict |
| Per-block \(\lvert\mathcal{T}_p\rvert\), skip rates | Effective-sample audit |

### Forbidden as quasi-primary

- Exploratory S1 perturbation batteries
- Exploratory S5 rank batteries as claim generators
- Crisis-stratified recurrence
- Any diagnostic that **rescues** a failed primary (\(F_4\) / not PASS → PASS)

---

## Final constants table

| Constant | Value | Status | Justification class | Sensitivity |
|----------|-------|--------|---------------------|-------------|
| \(\mathcal{K}\) | \(\{10,25,50\}\) | **FROZEN** | Human policy (HD-C2) | Finer/coarser locality grid |
| \(\tau\) | \(W_X=20\) | **FROZEN** | Mathematically forced floor (D4) | Overlap contamination if lowered |
| \(P\) | \(3\) | **FROZEN** | Methodological balance | \(P\uparrow\) ⇒ harder PASS |
| Remainder | Append to last block | **FROZEN** | Deterministic policy | Slight last-block length asymmetry |
| \(B_{\mathrm{N4}}\) | \(999\) | **FROZEN** | Convention (p-resolution \(0.001\)) | Larger ⇒ smoother tails, cost |
| \(B_{\mathrm{N3}}\) | \(999\) | **FROZEN** | Same | Same |
| \(\alpha\) | \(0.05\) | **FROZEN** | Convention | Stricter α ⇒ harder PASS |
| Master seed | `42` | **FROZEN** | Continuity with I02 seed culture | Changes surrogate draws |
| Seed streams | `N4: seed=42+b`, `N3: seed=10_000+b`, validity RNG `seed=20_000+p` | **FROZEN** | Computational reproducibility policy | — |
| \(n_{\min}\) | \(250\) queries per block | **FROZEN** | Policy: \(\ge 5\cdot k_{\max}\) | Lower ⇒ more PASS power / weaker stability |
| \(m\) random distances | \(50\) | **FROZEN** | Equals \(k_{\max}\); computational | Noise in \(\lambda\) |
| IAAFT \(I_{\max}\) | \(100\) | **FROZEN** | Convention | — |
| IAAFT \(\varepsilon\) | \(10^{-8}\) | **FROZEN** | Numerical convention | — |
| IAAFT fail rate gate | \(>5\%\) → INCONCLUSIVE | **FROZEN** | Policy | — |
| **N4 scale window** | \(W_\sigma=20\) (**SCALE-W**) | **FROZEN** | Derived nuisance-control horizon | See HD-N4-SCALE |

No constant above was selected from observed market recurrence results.

---

## HD-N4-SCALE — RESOLVED

**SCALE-W** frozen: \(W_\sigma := W_{RV} := W_X = 20\).  
Record: [I03-HD-N4-SCALE-FREEZE.md](I03-HD-N4-SCALE-FREEZE.md).

---

## Preregistration status

| Artifact | Status |
|----------|--------|
| `I03-PREREG-v0.1.md` | **DRAFT COMPLETE** (not implemented; not executed) |

---

## Document control

| Field | Value |
|-------|-------|
| ID | I03-C1-C10-FREEZE |
| Supersedes open options in | DESIGN v0.1 §§C1–C10 (historical discussion retained; freeze governs) |
| D1–D8 reopened? | **No** |
