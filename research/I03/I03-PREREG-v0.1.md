# I03 — Preregistration v0.1

> **STATUS :** **DRAFT COMPLETE** — executable *specification*; **NOT implemented**; **NOT executed**  
> **Authority class :** RESEARCH / PROTOCOL  
> **Protocol :** QDP v0.1 · DR-007 · DR-008 (exploratory data class)  
> **Investigation :** I03 — Intrinsic temporal recurrence of classical geometry G0  
> **Parents :**  
> [I03-D1-D8-FREEZE.md](I03-D1-D8-FREEZE.md) ·  
> [I03-C1-C10-FREEZE.md](I03-C1-C10-FREEZE.md) ·  
> [I03-HD-N4-SCALE-FREEZE.md](I03-HD-N4-SCALE-FREEZE.md) ·  
> [I03-DESIGN-v0.1.md](I03-DESIGN-v0.1.md) (historical discussion only)
>
> ```text
> I03-PREREG-v0.1 = DRAFT COMPLETE
> NOT IMPLEMENTATION-READY UNTIL CODE MATCHES THIS TEXT
> NO MARKET DATA USED TO WRITE THIS DOCUMENT
> NO EXPERIMENT RUN
> NO SCI / PRED / ECON CLAIM FROM PREREG ALONE
> W_sigma = 20
> ```

**Static freedom audit :** §24 — **PASS** (no unresolved execution-affecting
scientific choice found after HD-N4-SCALE).

---

## 0. Frozen constants (normative)

| Symbol | Value |
|--------|-------|
| \(W_X\) | 20 |
| \(M\) | 252 |
| \(W_\sigma\) | 20 |
| \(W_{RV}\) | 20 (identity \(W_\sigma:=W_{RV}:=W_X\)) |
| \(\tau\) | \(W_X=20\) |
| \(\mathcal{K}\) | \(\{10,25,50\}\) |
| \(k_{\max}\) | 50 |
| \(P\) | 3 |
| \(B_{\mathrm{N4}}\) | 999 |
| \(B_{\mathrm{N3}}\) | 999 |
| \(\alpha\) | 0.05 |
| Master seed | 42 |
| \(n_{\min}\) | 250 |
| \(m_{\mathrm{rand}}\) | 50 |
| IAAFT \(I_{\max}\) | 100 |
| IAAFT \(\varepsilon_{\mathrm{IAAFT}}\) | \(10^{-8}\) |
| IAAFT nonconvergence gate | \(>0.05\cdot B_{\mathrm{N3}}\) flagged → INCONCLUSIVE |

---

## 1. Scientific question

Under fixed causal G0 and mandatory temporal exclusion \(|t-s|\ge\tau\) with
\(\tau=W_X\), does the market-state trajectory exhibit nontrivial local
temporal recurrence—measured by mean τ-separated \(k\)-NN distance
(E-MND)—that is coherent across neighborhood scales \(\mathcal{K}\) and
across \(P=3\) deterministic time blocks, beyond a preregistered
volatility-preserving null N4 (\(W_\sigma=20\)) and under an adversarial
IAAFT null N3, without using future-return information?

### 1.1 Claim boundary (D8)

An I03 **PASS** supports **only** a structural claim about current G0.
PASS does **not** imply: predictive value; future-return information;
trading value; economic exploitability; superiority of L2 over alternative
geometries. Governance permission to *later ask* a PRED question is **not**
part of the I03 scientific claim.

---

## 2. Data class and analysis calendar

### 2.1 Exploratory path (this prereg)

| Field | Contract |
|-------|----------|
| Class | `EXPLORATORY` / `UNQUALIFIED` (DR-007 / DR-008) |
| Continuity object | Same G0 sandbox lineage as I02-E01: **SPY**, **daily**, log-returns from adjusted close |
| Source family | yfinance-class download as in DR-008 / I02-E01; **pin library version in the run artifact** at execution time (do not silently change mid-run) |
| Returns | \(r_t=\ln(P_t/P_{t-1})\); \(P_t\) adjusted close known at \(t\) |
| Calendar | Maximal available contiguous daily history under the pinned source at run start; record \([t_{\mathrm{start}},t_{\mathrm{end}}]\), \(T\), and content hash in the artifact |
| Confirmatory | **Out of scope** for this prereg; requires separate C02 path |

No date range may be shortened post hoc to improve recurrence scores.

---

## 3. G0 representation (fixed)

### 3.1 Causal normalization of \(X\) (window \(M=252\))

For each \(t\) with at least \(M\) prior returns in
\(\{r_{t-M+1},\ldots,r_t\}\):

\[
\hat\mu_t^{(X)}
=
\frac1M\sum_{u=t-M+1}^{t} r_u,
\quad
\hat\sigma_t^{(X)}
=
\sqrt{
\frac1{M-1}
\sum_{u=t-M+1}^{t}
\bigl(r_u-\hat\mu_t^{(X)}\bigr)^2
}.
\]

- If \(\hat\sigma_t^{(X)}>0\):
  \(\tilde r_u=(r_u-\hat\mu_t^{(X)})/\hat\sigma_t^{(X)}\) for
  \(u\in\{t-W_X+1,\ldots,t\}\).
- If \(\hat\sigma_t^{(X)}=0\) or undefined (insufficient history):
  \(X_t\) **undefined** (skip). **No** \(\varepsilon_\sigma\).

\[
X_t=(\tilde r_{t-W_X+1},\ldots,\tilde r_t)\in\mathbb{R}^{W_X}.
\]

\[
d_0(x,y)=\|x-y\|_2.
\]

Normalization uses **global** causal history (may extend before a block
boundary). Neighbor pools are **within-block** only (§6).

---

## 4. Temporal exclusion

\[
\tau = W_X = 20.
\]

Admissible pairs require \(|t-s|\ge\tau\). This is the hard anti-overlap floor
for return windows composing \(X\). No ACF-mined enlargement.

---

## 5. Blocks (cross-period)

Order the analysis index set as increasing trading times
\(\{t_0,\ldots,t_{T-1}\}\) on which returns exist (calendar §2).

\[
L=\lfloor T/P\rfloor,\quad P=3,\quad R=T\bmod P.
\]

\[
\begin{aligned}
B_1&=\{t_0,\ldots,t_{L-1}\},\\
B_2&=\{t_L,\ldots,t_{2L-1}\},\\
B_3&=\{t_{2L},\ldots,t_{3L-1+R}\}.
\end{aligned}
\]

Remainder length \(R\) is **appended to \(B_3\)** only. No crisis labels.
No boundaries defined by 2008 / 2009 / 2020.

---

## 6. Primary estimand E-MND

### 6.1 Admissible pool (within block)

\[
A_t^{(p)}
=
\{s\in B_p:\ |t-s|\ge\tau,\ X_s\text{ defined}\}.
\]

### 6.2 Query set

\[
\mathcal{T}_p
=
\{t\in B_p:\ X_t\text{ defined},\ \lvert A_t^{(p)}\rvert\ge k_{\max}\}.
\]

If \(\lvert\mathcal{T}_p\rvert < n_{\min}\) for any \(p\) → predicate \(E\)
fails → verdict **INCONCLUSIVE** (§19).

### 6.3 Distances

Let \(d_{(j)}^\tau(t;p)\) be the \(j\)-th smallest \(d_0(X_t,X_s)\) over
\(s\in A_t^{(p)}\). Ties: sort by \((\mathrm{distance}\uparrow,\,s\uparrow)\)
with \(s\) the integer time index.

\[
\delta_k(t;p):=d_{(k)}^\tau(t;p),\quad k\in\mathcal{K}.
\]

### 6.4 Cell estimand

\[
\Theta_k^{(p)}
:=
\frac1{\lvert\mathcal{T}_p\rvert}
\sum_{t\in\mathcal{T}_p}
\delta_k(t;p).
\]

**Lower is stronger recurrence.** Tautological membership-rate statistics are
**forbidden** as primary.

### 6.5 Non-tautology (normative note)

Under \(\lvert A_t^{(p)}\rvert\ge k\), \(\lvert N_k\rvert=k\) always; that
cardinality is not an estimand. \(\delta_k\) is the continuous radius of the
\(k\)-ball and is the object compared to surrogates.

---

## 7. Multi-scale coherence

\(\mathcal{K}=\{10,25,50\}\). Report all \(k\). **No** best-\(k\).

Let \(S_\nu(k,p)=1\) iff cell \((k,p)\) survives null \(\nu\) (§17).

| Term | Definition |
|------|------------|
| Coherent\((p,\nu)\) | \(S_\nu(k,p)=1\) ∀ \(k\in\mathcal{K}\) |
| Scale-localized\((p,\nu)\) | \(\exists k: S_\nu(k,p)=1\) and \(\exists k': S_\nu(k',p)=0\) |
| \(C_\nu\) (global) | Coherent\((p,\nu)\) for **all** \(p\in\{1,2,3\}\) |

Scale-localized structure **never** implies PASS.

---

## 8. N4 primary null — exact contract (\(W_\sigma=20\))

### 8.1 Scale estimator \(\hat\sigma_t^{\mathrm{N4}}\)

**Authority:** C3 “analogous stdev” to G0 sample-stdev, window \(W_\sigma=20\)
([HD-N4-SCALE](I03-HD-N4-SCALE-FREEZE.md)).

**Not** I02’s undemeaned RMS \(RV_t=\sqrt{\frac1W\sum r^2}\). Same horizon,
different functional.

Warm-up: \(\hat\sigma_t^{\mathrm{N4}}\) is defined iff indices
\(t-W_\sigma+1,\ldots,t\) all exist in the return calendar.

\[
\bar r_t^{(\sigma)}
=
\frac1{W_\sigma}
\sum_{u=t-W_\sigma+1}^{t} r_u,
\]

\[
\hat\sigma_t^{\mathrm{N4}}
=
\sqrt{
\frac1{W_\sigma-1}
\sum_{u=t-W_\sigma+1}^{t}
\bigl(r_u-\bar r_t^{(\sigma)}\bigr)^2
}.
\]

- Inclusive of \(r_t\) (causal).
- Denominator \(W_\sigma-1=19\) (sample stdev; matches G0’s \(M-1\) convention).
- If undefined (warm-up): no residual at \(t\).
- If \(\hat\sigma_t^{\mathrm{N4}}=0\): no residual at \(t\) (non-residual).

### 8.2 Decomposition and permutation domain

\[
\mathcal{Z}
=
\{t:\ \hat\sigma_t^{\mathrm{N4}}\text{ defined and }>0\}.
\]

\[
z_t = r_t / \hat\sigma_t^{\mathrm{N4}},\quad t\in\mathcal{Z}.
\]

**Preserve exactly:** \(\{\hat\sigma_t^{\mathrm{N4}}\}\) on all \(t\) where
defined (including zeros).

**Destroy:** order of \(\{z_t:t\in\mathcal{Z}\}\) via uniform random
permutation \(\pi^{(b)}\) of \(\mathcal{Z}\).

### 8.3 Reconstruction

\[
r_t^{\ast(b)}
=
\begin{cases}
\hat\sigma_t^{\mathrm{N4}}\cdot z_{\pi^{(b)}(t)} & t\in\mathcal{Z},\\
r_t & t\notin\mathcal{Z}.
\end{cases}
\]

Rebuild \(X^{\ast(b)}\) from \(\{r^{\ast(b)}\}\) with **identical** §3 G0
map. Recompute blocks on the **same calendar indices** (block cuts are not
re-fit). Recompute \(\Theta_k^{(p),\ast(b),\mathrm{N4}}\).

### 8.4 N4 degeneracy → invalidate \(E\) (→ INCONCLUSIVE)

| Condition | Action |
|-----------|--------|
| \(\lvert\mathcal{Z}\rvert / T < 0.95\) | N4 INVALID |
| \(\mathrm{Var}(\{\hat\sigma_t^{\mathrm{N4}}:t\in\mathcal{Z}\})=0\) | N4 INVALID |
| RNG/permutation not reproducible under §16 | Implementation INVALID |

### 8.5 Seeds

For replicate \(b=1,\ldots,B_{\mathrm{N4}}\): permutation RNG seed
`42 + b` (integers).

---

## 9. N3 adversarial null — IAAFT

### 9.1 Scope

Apply IAAFT to the full analysis return series \(\{r_{t_0},\ldots,r_{t_{T-1}}\}\).
Then rebuild \(X^\ast\) under §3 and recompute E-MND on the same blocks.

### 9.2 Preservation claims (accurate)

IAAFT **approximately** preserves the power spectrum and the amplitude
marginal of \(r\). It does **not** exactly preserve either in finite samples.
It destroys nonlinear temporal structure beyond those constraints.

### 9.3 Algorithm parameters

| Step | Rule |
|------|------|
| Init | Random shuffle of \(\{r_t\}\) with seed `10000 + b` |
| Iterate | Standard IAAFT: impose spectrum via FFT phase step; impose amplitude ranks |
| Stop | Relative max change of sorted amplitudes **and** of periodogram bins each \(<\varepsilon_{\mathrm{IAAFT}}\), or \(I_{\max}\) reached |
| Nonconvergence | Accept last iterate; set flag `IAAFT_NONCONVERGED=1` |
| Gate | If \(\#\{\text{flags}\}/B_{\mathrm{N3}} > 0.05\) → N3 INVALID → INCONCLUSIVE |

Periodogram bins: FFT of length \(T\) (real FFT packing as implemented must be
recorded in artifact; scientific contract = full-series discrete Fourier
power matching IAAFT standard).

---

## 10. Locality validity (C6-D)

### 10.1 Quantities

For each \(t\in\mathcal{T}_p\), initialize diagnostic RNG seed `20000 + p`
**once per block**, then process \(t\) in **increasing** order:

- \(\delta_1(t;p)=d_{(1)}^\tau(t;p)\).
- Sample \(m_{\mathrm{rand}}=50\) distinct indices from \(A_t^{(p)}\) without
  replacement using that RNG; if \(\lvert A_t^{(p)}\rvert<50\), use all.
- \(\bar d_{\mathrm{rand}}(t;p)=\) mean \(d_0(X_t,X_s)\) over the sample.
- \(\lambda(t;p)=\delta_1(t;p)/\bar d_{\mathrm{rand}}(t;p)\) (if denominator 0:
  treat as degenerate → fail \(V\)).

\[
\Lambda_p=\mathrm{median}_{t\in\mathcal{T}_p}\lambda(t;p).
\]

\[
\gamma(t;p)
=
\frac{d_{(k_{\max})}^\tau(t;p)-d_{(1)}^\tau(t;p)}{d_{(1)}^\tau(t;p)}
\quad(d_{(1)}>0;\ \text{else fail }V),
\]

\[
\Gamma_p=\mathrm{median}_{t\in\mathcal{T}_p}\gamma(t;p).
\]

Recompute \(\Lambda_p^{\ast(b),\mathrm{N4}}\), \(\Gamma_p^{\ast(b),\mathrm{N4}}\)
on each N4 surrogate with **fresh** diagnostic stream seed
`20000 + p + 1000\cdot b` (independent of observed stream).

### 10.2 Validity predicate \(V\)

\(V=0\) (INCONCLUSIVE path) if **any** block \(p\) satisfies:

1. **Hard:** \(\Lambda_p \ge 1\); or
2. **Inference:** \(\Gamma_p \le \mathrm{median}_b\Gamma_p^{\ast(b),\mathrm{N4}}\)
   **and** \(\Lambda_p \ge \mathrm{median}_b\Lambda_p^{\ast(b),\mathrm{N4}}\).

\(V\) cannot create PASS.

---

## 11. Inference

### 11.1 Cell p-value (left tail)

\[
\hat p_{k,p}^{(\nu)}
=
\frac{
1+\#\{b:\ \Theta_k^{(p),\ast(b),\nu}\le \Theta_k^{(p)}\}
}{B_\nu+1}.
\]

Survive: \(S_\nu(k,p)=1\) iff \(\hat p_{k,p}^{(\nu)} \le \alpha\).
Equality at \(\alpha\) **survives** (closed).

### 11.2 Multiplicity

**Conjunction / coherence only** (§7, §19). No Bonferroni/Holm across cells.

### 11.3 Batteries

Independent N4 and N3 ensembles; sizes in §0.

---

## 12. Null-disagreement semantics

| Code | Pattern | Verdict role |
|------|---------|--------------|
| ND-1 | \(C_{\mathrm{N4}}\land C_{\mathrm{N3}}\) | PASS-eligible |
| ND-2 | \(C_{\mathrm{N4}}\) and not \(C_{\mathrm{N3}}\) | **INCONCLUSIVE** (restricted interpretation recorded) |
| ND-3 | \(C_{\mathrm{N3}}\) and not \(C_{\mathrm{N4}}\) | **FAIL** if \(F_{\mathrm{N4}}\); else **INCONCLUSIVE** |
| ND-4 | \(F_{\mathrm{N4}}\) | **FAIL** |
| ND-5 | Mixed / scale-localized without \(C_{\mathrm{N4}}\land C_{\mathrm{N3}}\) | **INCONCLUSIVE** |

\(F_{\mathrm{N4}}:=1\) iff \(S_{\mathrm{N4}}(k,p)=0\) for all \(k\in\mathcal{K}\)
and all \(p\in\{1,2,3\}\) (uniform non-survival under primary null).

---

## 13. Predicates

| Symbol | Definition |
|--------|------------|
| \(V\) | §10.2 |
| \(E\) | \(\lvert\mathcal{T}_p\rvert\ge n_{\min}\) ∀p; N4 not INVALID; N3 not INVALID |
| \(C_4\) | \(C_{\mathrm{N4}}\) |
| \(C_3\) | \(C_{\mathrm{N3}}\) |
| \(F_4\) | \(F_{\mathrm{N4}}\) |

---

## 14. PASS / FAIL / INCONCLUSIVE truth table

| Condition | Verdict |
|-----------|---------|
| \(\neg V\) or \(\neg E\) | **INCONCLUSIVE** |
| \(V\land E\land C_4\land C_3\) | **PASS** |
| \(V\land E\land F_4\) | **FAIL** |
| \(V\land E\land C_4\land\neg C_3\) (ND-2) | **INCONCLUSIVE** |
| \(V\land E\land\neg C_4\land C_3\land\neg F_4\) | **INCONCLUSIVE** |
| \(V\land E\land\neg C_4\land\neg C_3\land\neg F_4\) | **INCONCLUSIVE** |

PASS is stringent. NOT PASS ≠ automatic FAIL.

---

## 15. Diagnostic whitelist

Every item labeled **`DIAGNOSTIC — NON-PROMOTIONAL`**.

Allowed: §10 locality tables; N4 \(\hat\sigma\) histogram / zero counts /
\(|\mathcal{Z}|/T\); N3 convergence flags; full \(S_\nu(k,p)\) and \(\Theta\)
vs null quantiles; \(\lvert\mathcal{T}_p\rvert\); skip tallies.

Forbidden: S1/S5 claim batteries; crisis strata; any rescue of primary FAIL /
non-PASS into PASS.

---

## 16. Reproducibility and artifacts

### 16.1 Required artifact fields

- Prereg ID `I03-PREREG-v0.1` + git commit of this file
- Data pin: ticker, source library+version, date range, \(T\), content hash
- Seeds used for every surrogate and validity stream
- All \(\Theta_k^{(p)}\), surrogate quantiles, \(\hat p\), \(S_\nu(k,p)\)
- \(\Lambda_p,\Gamma_p\) and N4 medians
- N4 INVALID / N3 INVALID flags
- Final verdict + predicate vector \((V,E,C_4,C_3,F_4)\)
- Software commit hash implementing this prereg

### 16.2 Prohibited post-hoc freedoms

No: best-\(k\); result-driven \(P\)/blocks; ACF-tuned \(\tau\); SCALE-M swap;
threshold mining; crisis period construction; dropping blocks; changing
\(B_\nu\)/α after seeing results; future targets; alternative metrics/representations;
promoting diagnostics to primary.

---

## 17. Kill / invalid (non-scientific software failures)

Implementation contradiction with this text → **INVALID** until fixed under
change control; not a scientific FAIL.

---

## 18. Non-claims

I03 does not claim PRED, ECON, SCI promotion beyond the structural verdict
labels under DR-007 exploratory class, nor “markets have geometry” in
general, nor that L2 is optimal.

---

## 19. Execution status

```text
IMPLEMENTATION = NOT STARTED BY THIS DOCUMENT
E01 = NOT RUN
HAT = NOT RUN
```

---

## 24. Static freedom audit

### 24.1 Phrase scan (this file + freeze parents as normative)

| Pattern | Occurrences in this prereg | Classification |
|---------|----------------------------|----------------|
| choose / tune / optimize / best | None as open scientific knobs | OK |
| appropriate / reasonable / optionally / may use | None leaving execution free | OK |
| for example / etc. | None in normative sections | OK |
| sensitivity / alternative | Only in non-normative parent history | OK |
| depending on results | None | OK |

### 24.2 Checklist audit

| Risk | Status |
|------|--------|
| Undefined distance statistic | **Closed** — E-MND §6 |
| Ambiguous query/pool indexing | **Closed** — §6.1–6.2 |
| τ off-by-one | **Closed** — \(\lvert t-s\rvert\ge 20\) |
| Block-boundary / remainder | **Closed** — §5 append to \(B_3\) |
| Insufficient-pool behavior | **Closed** — skip from \(\mathcal{T}_p\); \(n_{\min}\) |
| N4 sigma indexing | **Closed** — §8.1 inclusive causal \(W_\sigma\) |
| N4 permutation scope | **Closed** — \(\mathcal{Z}\) only |
| IAAFT convergence | **Closed** — §9.3 + gate |
| Surrogate seeds | **Closed** — §8.5, §9.3, §10.1 |
| Tail direction | **Closed** — left tail on \(\Theta\) |
| Equality-at-α | **Closed** — \(\le\alpha\) survives |
| Missing / zero scale | **Closed** — §3, §8 |
| Scale-localized verdict | **Closed** — §7, §14 |
| Period-localized / disagreement | **Closed** — §12–§14 |
| N4 vs \(RV_t\) RMS ambiguity | **Closed** — §8.1 explicit rejection of RMS identity |

### 24.3 Audit verdict

\[
\boxed{\texttt{STATIC FREEDOM AUDIT = PASS}}
\]

\[
\boxed{\texttt{I03-PREREG-v0.1 = DRAFT COMPLETE}}
\]

**Not** implementation-ready until code and HAT prove bit-level conformance.

---

## Document control

| Field | Value |
|-------|-------|
| ID | I03-PREREG-v0.1 |
| Opens E01? | **No** |
| Implements? | **No** |
