# I04-CAL — Synthetic Structural Calibration Specification v0.2

> **Status :** FROZEN FOR IMPLEMENTATION  
> **Class :** SYNTHETIC / STRUCTURAL / PRE-MARKET  
> **Parent program :** Quant geometry research (post-I03)  
> **Baseline Git HEAD at freeze start :** `725b8f366a1c1026dbe2160bccbd9367c424de4c`  
> **Authority :** Mandat Cursor I04-CAL v0.2 (human-authorized execution)

```text
NO FUTURE MARKET TARGET
NO SYNTHETIC WINNER / BEST-W / BEST-SEED / BEST-HYPERPARAMETER
NO MARKET DATA
NO PRED / ECON
CAL-6 IS NOT A RANKING SCORE
G0 = BASELINE / REFERENCE — NOT PROMOTED / NOT FALSIFIED
G6 = HOLD (causal comparability unresolved)
Koopman/HMM = OUT OF CORE
```

---

## 1. Purpose

Qualify a **synthetic structural measurement bench** before any I04 market
screening:

```text
GENERATOR DEFINES TRUTH → GATES ATTEMPT TO RECOVER/CHARACTERIZE IT
```

I04-CAL does **not** select a best geometry and does **not** test predictive
homogeneity.

---

## 2. Absolute invariants (INV-01 … INV-12)

As stated in the authorizing mandat. Implementation MUST fail closed if
violated.

---

## 3. Seeds and replications

| Parameter | Value |
|-----------|--------|
| \(B_{\mathrm{world}}\) | **32** |
| Index | \(b=0,\ldots,31\) |
| Primary seed | \(\mathrm{seed}(S_i,b)=100000\cdot i + b\) |

World index map (fixed):

| World | \(i\) |
|-------|------|
| S0a | 0 |
| S0b | 1 |
| S1 | 2 |
| S2 | 3 |
| S3 | 4 |
| S4 | 5 |
| S5 | 6 |
| S6 | 7 |
| S7 | 8 |

Variants (no collision with primary):

| Variant | seed |
|---------|------|
| S0a | \(100000\cdot 0 + b\) |
| S0b | \(100000\cdot 1 + b\) |
| S1 | \(100000\cdot 2 + b\) |
| S2 | \(100000\cdot 3 + b\) |
| S3 | \(100000\cdot 4 + b\) |
| S4 | \(100000\cdot 5 + b\) |
| S5 | \(100000\cdot 6 + b\) |
| S6 | \(100000\cdot 7 + b\) |
| S7 | \(100000\cdot 8 + b\) |
| S7 logistic secondary | \(100000\cdot 80 + b\) |
| Projection/aux RNG (geometry) | \(100000\cdot 900 + g_{\mathrm{id}}\) (independent of \(b\)) |

Seeds MUST NOT depend on worker count, OS, or scheduling order.

---

## 4. Series length and windows

| Parameter | Value |
|-----------|--------|
| Post burn-in \(N\) | **8192** (where applicable) |
| \(W\) | \(\{20,40,60\}\) — all reported; **no best-\(W\)** |
| Query stride (preregistered) | **16** |
| Candidate stride (preregistered) | **16** |
| G1-only query/candidate stride | **32** (O(W²) Soft-DTW) |
| Temporal embargo for neighbors | \(\lvert t-s\rvert \ge W\) |
| \(k\) for neighborhood gates | **\(\{5,10,20\}\)** (all reported; no best-\(k\)) |

Query/candidate strides are **execution/estimation** contracts frozen **before**
CAL results. They are **not** optimized on CAL-6.

---

## 5. Worlds (summary)

Full definitions live in code modules under `quant.i04_cal.worlds` and MUST
match this freeze.

| World | Truth summary |
|-------|----------------|
| S0a | IID \(N(0,1)\) — no structural recurrence |
| S0b | IID \(t_5/\sqrt{5/3}\) — no structural recurrence |
| S1 | SV \(\phi=0.98\), \(\sigma_h=0.15\), burn-in 2000 — volatility-dominated |
| S2 | 3 frozen sinusoidal prototypes + warps \(\alpha\in\{0.65,1,1.55\}\) — class \(j\) |
| S3 | Regimes Gaussian / \(t_5\) / skew-normal(shape=5); \(L\sim U\{120..300\}\) |
| S4 | Same multiset, orderings O1/O2/O3; oracle on interior windows only |
| S5 | AR(1) \(\phi\in\{-0.6,0,0.6\}\); continuous; \(L\sim U\{150..350\}\) |
| S6 | Latent manifold + univariate observation; observability prerequisite |
| S7 | Lorenz \(\sigma=10,\rho=28,\beta=8/3\), RK4 \(dt=0.01\); noise levels frozen |

---

## 6. Geometry hyperparameter grids (preregistered BEFORE CAL)

| Geometry | Grid | Notes |
|----------|------|-------|
| G0 | none | standardized window + L2 |
| G1 Soft-DTW div | \(\gamma\in\{0.1,1.0,10.0\}\); Sakoe–Chiba band \(=\max(2,W/4)\) | Band is part of frozen G1 definition for CAL |
| G2 Sliced-W | \(d\in\{2,3\}\), \(L=32\) fixed dirs | directions from aux seed |
| G3 Signature | \(M\in\{2,3\}\), time-aug **on** | distance in truncated feature space |
| G4 MMD | RBF; bandwidth = median pairwise on **within-window** lags (causal) | estimator ≠ population |
| G5 AIRM | \(p\in\{2,3\}\), \(\lambda=10^{-3}\) | Cov+\(\lambda I\) |
| G6 Diffusion | **HOLD** | stubs/tests only; not CAL-qualified |
| G7 TDA | delay \(m=2\), \(\tau=1\); VR maxdim=1; bottleneck | viability audit; no post-hoc retune |
| G-ORD | \(D\in\{3,4\}\), \(\tau=1\) | permutation JS |

**G_VOL** = \(\log RV_t\) nuisance baseline — **not** an I04 candidate.

---

## 7. Gates

| Gate | Role |
|------|------|
| CAL-G1 Contrast | median kNN / median random-admissible |
| CAL-G2 Excess persistence | Jaccard persistence vs overlap-null (see §7.1) |
| CAL-G3 Historical recurrence | \(R_G(H)\) for \(H\in\{2W,5W,10W\}\) |
| CAL-G4 Perturbation stability | Spearman rank curve for \(c\in\{0.05,0.1,0.2\}\) |
| CAL-G5 Nuisance dominance | associations vs \(\lvert\Delta RV\rvert,\lvert\Delta\mathrm{mean}\rvert,\ldots\) + G_VOL |
| CAL-6 Oracle recovery | categorical / Spearman vs latent — **never** a ranking score |

### 7.1 CAL-G2 overlap-null (implementation choice — documented)

**Primary null (preregistered):** for each query \(t\), form null neighborhoods by
sampling \(k\) indices from the **same admissible set** as kNN (embargo +
in-bounds), independently for consecutive queries, **without** using geometry
ranks. This destroys geometry-induced neighborhood identity while preserving
admissibility/overlap opportunity induced by shared feasible sets.

**OPEN GOVERNANCE (non-blocking for CAL execution):** whether a stronger
overlap-null that also preserves latent continuity should replace this for
future market I04. CAL reports properties of the primary null; does not
promote alternatives post-hoc.

---

## 8. Observability (S6 / S7)

Diagnostic (not a scientific PASS threshold):

1. Build delay vectors of length \(W\) from univariate series.
2. On a fixed set of admissible pairs (deterministic subsample), compute
   Spearman(\(d_{\mathrm{delay}}\), \(d_Z\)) where \(d_{\mathrm{delay}}\) is L2 on delays.

| Diagnostic band | Oracle status |
|-----------------|---------------|
| Spearman \(\ge 0.25\) | ORACLE VALID (usable for CAL-6 reporting) |
| Spearman \(< 0.25\) | ORACLE INVALID → CAL-6 for that world **NOT INTERPRETABLE** / INCONCLUSIVE |

```text
OPEN GOVERNANCE DECISION:
Exact observability cutoff (0.25) is an engineering diagnostic frozen for
I04-CAL reporting consistency. Changing it for market I04 requires human
governance. It does NOT authorize geometry FAIL when oracle is INVALID.
```

---

## 9. Qualification criteria C1–C10

As in mandat §19. Bench status labels:

| Label | Meaning |
|-------|---------|
| CAL-PASS | Bench/protocol qualifies under C1–C10 |
| CAL-INCONCLUSIVE | Incomplete evidence / oracle invalid blocking interpretation |
| CAL-FAIL | Systematic false structure / broken measurement under contract |

CAL-PASS ≠ market hypothesis proven.

---

## 10. Status taxonomies

Worlds: VALID / INVALID / INCONCLUSIVE  
Oracles: VALID / INVALID / NOT_APPLICABLE  
Execution: COMPLETE / INCOMPLETE / FAILED_TECHNICAL  
Geometries: EXECUTABLE / DEGENERATE / PARAMETER_FRAGILE / HOLD / INVALID_UNDER_CONTRACT  

---

## 11. Hard stops / non-goals

No SPY download, no I01–I03 cache reuse for CAL science, no E01 market, no
PRED/ECON, no geometry winner, no G6 promotion, no Koopman/HMM core.

---

## Document control

| Field | Value |
|-------|--------|
| Spec id | I04-CAL-SPEC-v0.2 |
| Freeze rule | grids/worlds fixed before primary CAL observation |
