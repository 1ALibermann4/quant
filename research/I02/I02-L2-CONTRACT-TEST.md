# I02 — L2 Contract-Test Closure Report

> **STATUS :** L2 VERIFICATION EVIDENCE
> **Authority class :** RESEARCH / PROTOCOL (non-normative vs prereg)
> **Preregistration :** [I02-PREREG-v0.3](I02-preregistration.md) — **unchanged**
> **Baseline implementation :** `b5465b0`
> **Baseline pin :** `cc608fd`
> **L2 suite :** `tests/i02/test_l2_contract.py`
> **L2 closure commit :** `16cfee2`
> **Market data :** NONE
> **Experiment / HAT :** NOT STARTED

```text
OBJECTIVE: falsify fidelity of implementation to I02-PREREG-v0.3
CORE DESIGN UNCHANGED
PREREGISTRATION v0.3 UNCHANGED
NO POST-HOC CHOICE
```

---

## 1. Exit verdict

\[
\boxed{\texttt{L2-PASS}}
\]

Conditions met:

- Executable preregistration clauses traced (matrix §2)
- Adversarial contract tests pass (`tests/i02` **95/95**)
- Full repository regression green after one unrelated T2 generator fix
- No T3/T4 blocker remains
- Implementation remains aligned with v0.3

**L2-PASS ≠ HAT PASS.** HAT not started.

---

## 2. Traceability matrix

Statuses: **COVERED** / **PARTIAL** / **UNCOVERED** / **NON-EXECUTABLE**

| Clause | Prereg | Implementation | Test(s) | Status |
|--------|--------|----------------|---------|--------|
| \(W_X=20\) | §0 | `params.W_X` / `states_x` | `test_params_*`, L2 X | COVERED |
| \(M=252\) | §0, §13 | `params.M` / `causal_mu_sigma` | v0.3 + L2 X | COVERED |
| \(\hat\sigma=0\) ⇒ undefined | §0, §13 | `X_SIGMA_ZERO` | v0.3 + L2 X/skips | COVERED |
| \(W_{RV}=20\) | §0 | `params.W_RV` / `features` | primitives + L2 oracles | COVERED |
| \(h=10\) | §0 | `params.h` / `target` | primitives + L2 temporal | COVERED |
| \(\mathcal{M}_Z=\{3,12,21\}\) | §0 | `params.M_Z` / `regime` | L2 Z + e2e | COVERED |
| \(k=50\) | §0 | `params.k` / `neighbors` | L2 kNN | COVERED |
| stride=1 | §0 | `query_schedule` | pipeline | COVERED |
| Hard availability \(s+h\le t\) | §0 | `pool.admissible_pool` | L2 temporal | COVERED |
| Common \(A_t\) | §0 | `admissible_pool` + constructible ∩ | L2 common \(A_t\) | COVERED |
| \(X\) L2 distances | §0 | `pairwise_x` | pipeline / L2 | COVERED |
| \(S_1\) | §0 | `distance_s1` | L2 oracles | COVERED |
| \(S_2\) \(d_2\) | §0 | `distance_s2_d2` | L2 oracles | COVERED |
| \(S3_Q\) / \(S3_\phi\) | §14 | `distance_s3_*` / pipeline | L2 S3 + v0.3 | COVERED |
| Deterministic ties | §0 | `select_neighbors` lexsort | L2 kNN | COVERED |
| Empirical atoms \(1/k\sum\delta\) | §0 | forecast atoms | L2 multiplicity | COVERED |
| Duplicate multiplicity | §0 | CRPS + atoms | L2 + primitives | COVERED |
| CRPS | §0 | `crps_empirical` | L2 CRPS oracle | COVERED |
| \(D=\mathrm{CRPS}_S-\mathrm{CRPS}_X\) | §0 | `score_difference` | L2 D/R | COVERED |
| \(R=D/\mathrm{CRPS}_S\) | §0 | `relative_incremental_value` | L2 D/R | COVERED |
| Denominator-zero | §0 | `CRPS_COMPARATOR_ZERO` | L2 D/R + skips | COVERED |
| \(Z\) indexing \(m\), \(m-1\) | §0 | `z_at` | L2 Z | COVERED |
| \(Z\) causality | §0 | window ends at \(t\) | L2 Z / leakage | COVERED |
| Spearman grid | §1–§2 | `spearman_grid` | L2 Spearman | COVERED |
| Two-sided interpretation | §1.3 | association API (no signed gate) | L2 Spearman + docs | COVERED |
| MBB non-circular | §15 | `bootstrap.py` | L2 bootstrap + v0.3 | COVERED |
| \(b^\star=40\), \(\{20,40,80\}\) | §0, §15 | `params` / robustness | L2 + v0.3 | COVERED |
| \(B=9999\), seed=42 | §15 | frozen params | L2 freedom + v0.3 | COVERED |
| Percentile CI \(\alpha=0.05\) | §15 | `np.quantile` linear | L2 + v0.3 | COVERED |
| Degenerate replicates | §15 | drop + \(\lceil 0.8B\rceil\) | L2 + v0.3 | COVERED |
| \(n<b\) INCONCLUSIVE | §15 | `BOOTSTRAP_INSUFFICIENT_N` | L2 + v0.3 | COVERED |
| No-primary S3 | §14 | dual charts, no selector | L2 S3 audit | COVERED |
| No-best-\(m\) / no-best-\(b\) | §0, §15 | grid / robustness | L2 + static audit | COVERED |

**Counts:** COVERED **35** · PARTIAL **0** · UNCOVERED **0** · NON-EXECUTABLE **0**
(among the mandated executable checklist)

---

## 3. Adversarial audits (summary)

### 3.1 Temporal / leakage

- \(V_{t,10}\) uses exactly \(r_{t+1},\ldots,r_{t+10}\).
- Hard availability is \(s+10\le t\) (boundary \(s=t-10\) eligible when constructible; \(s=t-9\) excluded).
- Future-only perturbation after query \(t\) does **not** alter \(X_t\), \(RV_t\), \(L_t\), \(Z_t\), \(A_t\), or neighbor identities/distances; **may** alter \(V_{t,10}\).

**Result:** PASS (no off-by-one / leakage T1 found).

### 3.2 Common \(A_t\)

**Contract reading (v0.3):** one shared pool for \(X,S_1,S_2,S_3\).

**Implementation:** `representation_constructible` requires \(X\) **and** S-features (RV/D/Q) defined — i.e. **intersection** of dates evaluable for all representations. Neighbor ranking is representation-specific; the candidate set is not.

**Result:** PASS — implementation and preregistration agree. Not representation-specific pools.

### 3.3 S3 dual-branch

Both `S3_Q` and `S3_phi` survive through neighbors → forecast → CRPS → D/R. Static audit found no `best_s3` / branch `argmin`/`argmax` selection. Geometry fixtures show Q vs φ distances can disagree without code choosing a winner.

**Result:** PASS.

### 3.4 Bootstrap / compressed time

v0.3 §15.2 **Source series**:

> time-ordered paired valid observations after structural skips removed (**compressed** valid series). Calendar gaps from skips are **not** re-inserted as missingness inside blocks.

**Consequence (explicit):** valid query indices `100,101,102,150,151` become five contiguous positions; block construction treats `102→150` as adjacent.

**Implementation:** `mbb_spearman_ci` masks to finite pairs then runs non-circular MBB on length \(n_{\mathrm{valid}}\) — matches v0.3.

**CONTRACT RISK (accepted, not redesigned):** compressed-time adjacency is a modeling consequence of the frozen algorithm. It is **not** a T3/T4 contradiction. Documented here so HAT/runners do not reinterpret MBB as calendar-aware blocks.

**Result:** PASS (semantics verified; risk recorded, not changed).

### 3.5 Static scientific-freedom audit

- `I02Params` freezes \(W_X,M,W_{RV},h,k,\mathcal{M}_Z,\mathrm{stride},b^\star,B,\mathrm{seed},\alpha\).
- No I02 argparse/click surface.
- No `epsilon_sigma=`, adaptive \(k\)/\(b\), best-\(m\)/\(b\)/\(S\) hooks in `src/quant/i02`.
- Test-only `n_replicates` override on MBB is **explicit**; default scientific path uses frozen `B=9999`.

**Result:** PASS.

**Note (numerical):** `phi_from_q` clamps \(Q\) into \([0,1]\) only after rejecting \(Q\notin(0,1+10^{-15}]\). This is floating hygiene for `arccos`, not scientific clipping of defined \(Q\).

**Note (σ̂):** exact binary constants (e.g. all `1.0`) yield \(\hat\sigma=0\); some decimal constants (e.g. `0.03`) can yield tiny float std noise under NumPy — contract uses exact `== 0.0` (no ε), consistent with no-epsilon policy.

---

## 4. Issues discovered (T1–T5)

| ID | Class | Description | Action |
|----|-------|-------------|--------|
| L2-01 | T2 | L1 unit tests did not cover end-to-end adversarial invariants (temporal, leakage, common \(A_t\), dual S3, compression) | Added `test_l2_contract.py` |
| L2-02 | T5 | README / package status still framed as pre-L2 in places | Updated via L2 report + README readiness pointer |
| L2-03 | T2 | C02 Hypothesis generator used unbounded `st.integers()`, colliding with QCJ-1 safe-int (unrelated to I02; revealed when full suite collected) | Constrained generator to \(\pm(2^{53}-1)\) |
| L2-04 | — | Compressed-time MBB adjacency | **CONTRACT RISK accepted** (v0.3); not a gap |

No **T1** implementation bugs requiring code correction against a unique contract reading.
No **T3** / **T4** blockers.

---

## 5. Fixes performed

1. **T2 (I02):** adversarial L2 test suite + traceability report.
2. **T2 (tooling):** optional explicit `n_replicates` on `mbb_spearman_ci` for mechanical tests without mutating frozen `bootstrap_B=9999`.
3. **T2 (foundations):** Hypothesis QCJ-1 integer bounds in `tests/contracts/test_c02_properties.py`.

No preregistration amendment. No design redesign.

---

## 6. Test counts

| Scope | Result |
|-------|--------|
| `tests/i02` | **95 passed** |
| Full repository (`pytest`) | **695 passed** |

---

## 7. Remaining gaps / blockers

- **None for L2 exit.**
- Next authorized milestone: **HAT protocol** (synthetic controlled harness), not market data, not experiment.

---

## 8. Confirmations

```text
CORE DESIGN UNCHANGED
PREREGISTRATION v0.3 UNCHANGED
NO MARKET DATA USED
NO EXPERIMENT RUN
HAT NOT STARTED
NO POST-HOC CHOICE
L2-PASS ≠ HAT PASS
```
