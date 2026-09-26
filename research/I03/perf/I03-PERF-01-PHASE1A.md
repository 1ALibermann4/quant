# I03-PERF-01 — Phase 1A: Exact E-MND / Locality Kernel Optimization

> **Status :** PHASE 1A CLOSED  
> **Class :** ENGINEERING OPTIMIZATION ONLY  
> **Prereg :** [I03-PREREG-v0.1.md](../I03-PREREG-v0.1.md) — **unchanged**  
> **Phase 0 :** [I03-PERF-01-PHASE0.md](I03-PERF-01-PHASE0.md) @ `c304d7b`  
> **E01 / E02 :** **NOT executed**

```text
THIS IS AN ENGINEERING OPTIMIZATION.
NO SCIENTIFIC RESULT WAS PRODUCED.
NO E01 · NO E02 · NO MULTIPROCESSING · NO CHECKPOINT/RESUME
NO PARAMETER CHANGE · NO PREREG CHANGE
```

**Verdict:** `PERF01-PHASE1A: PASS`

---

## 1. Baseline (frozen before edits)

| Item | Value |
|------|--------|
| HEAD | `c304d7bbd589ece11d03d7ecf5516a2764619c76` |
| Python | 3.12.10 |
| NumPy | 2.5.3 |
| Platform | Windows-11 AMD64 (local) |
| I03 tests @ baseline | 78 passed |
| Entry points | `compute_emnd_block`, `locality_for_block`, `_emnd_on_returns`, `run_structural_analysis` |
| Fixtures | I03-HAT (`generate_hat_returns`); SPYLEN i.i.d. \(T=8470\) (timing only) |

Benchmark artifact: [`phase1a_bench.json`](phase1a_bench.json).

---

## 2. Hotspot targeted

From Phase 0 + inspection:

1. **`compute_emnd_block`** — Python loop over queries; per-query `admissible_pool` + distance/`lexsort`.  
2. **`locality_for_block`** — same pool/distance pattern; **double** `admissible_pool` (query list + body).  
3. **`all_state_vectors_x`** — exception-driven per-\(t\) construction inside every E-MND pass.  
4. **Pipeline duplicate** — N4 locality loop called `_emnd_on_returns` again (full G0+E-MND rebuild) after E-MND already computed the same states.

Not changed: N4/N3 generation, IAAFT, inference, seeds, \(B\), distances formula
`sqrt(sum(diff*diff))` + `lexsort((pool, dists))`.

---

## 3. Implementation changes

| Change | Location | Effect |
|--------|----------|--------|
| Shared `iter_block_query_pools` | `emnd.py` | One ascending enumeration of \((t,\mathrm{pool})\); precomputed member/defined views |
| Single-pass locality | `locality.py` | Reuses query/pool list; no second admissibility scan |
| Exception-free `all_state_vectors_x` | `i02/states_x.py` | Same `mean`/`std`/`(w-μ)/σ` arithmetic; no try/except control flow |
| Fuse N4 E-MND + locality | `pipeline.py` | One `_emnd_on_returns` per surrogate; locality uses those states |

Reference oracle (frozen pre-1A kernels): [`tests/i03/oracles_perf01.py`](../../tests/i03/oracles_perf01.py).

---

## 4. Scientific neutrality

- Admissible set: still \(\lvert t-s\rvert \ge \tau\) and \(X_s\) defined, ascending \(s\).  
- \(k\)-NN: still Euclidean \(L_2\), ties \((d\uparrow,s\uparrow)\) via `lexsort`.  
- \(\Theta_k\): still mean of the same \(d_{(k)}\) sequence.  
- \(\Lambda,\Gamma\): same formulas and RNG stream (`default_rng(seed)`).  
- States: same window bounds, `ddof=1`, no \(\varepsilon\), \(\sigma=0\Rightarrow\) undefined.  
- Pipeline fusion: locality inputs identical to a fresh `build_states_x` on the same surrogate (proven bitwise via tests).

No parameter, null, seed, or verdict-rule change.

---

## 5. Equivalence methodology

**Primary contract: BITWISE.**

For each block / seed / surrogate \(b\):

REFERENCE (`oracles_perf01`) vs OPTIMIZED (production)

compare skip counts, \(n\) queries, every \(\Theta_k\), \(\Lambda\), \(\Gamma\), flags, and
(where tested) admissible pools.

No tolerance introduced. No FP reduction-order change required human review.

---

## 6. Adversarial cases

Covered in `tests/i03/test_perf01_phase1a.py`:

- HAT full-block E-MND + locality vs reference  
- \(\tau\) boundary inclusion/exclusion  
- Tied / duplicate distances  
- Insufficient pool / tiny block  
- \(\Lambda\) across seeds  
- Deterministic re-run  
- SPYLEN one-block sample  

Existing L1/L2 suite retained (88 I03 tests total after adding Phase 1A).

---

## 7. N4 / N3 integration equivalence

Small engineering batteries (\(B=3\)), non-market HAT:

- N4: surrogate bytes vs `n4_surrogate_returns`; \(\Theta\) + locality vs reference  
- N3: IAAFT series + convergence flags; \(\Theta\) + locality vs reference  
- Pipeline fused locality vs reference on observed states (\(B_{N4}=B_{N3}=2\))

Generation code paths untouched.

---

## 8. Benchmark methodology

- Warm-up + median of multiple `perf_counter` reps  
- Same machine / Python 3.12.10 / NumPy 2.5.3  
- REFERENCE = frozen oracles; OPTIMIZED = production  
- Additional **fusion** microbench: old pipeline shape (E-MND + rebuild + locality)
  vs Phase 1A fused (E-MND + locality) on HAT \(B=8\)

No multiprocessing benchmarked.

---

## 9–11. Results / speedup / memory

| Workload | \(T_{\mathrm{reference}}\) | \(T_{\mathrm{optimized}}\) | Speedup |
|----------|----------------------------|-----------------------------|---------|
| HAT E-MND (3 blocks) | 0.254 s | 0.236 s | **1.07×** |
| HAT locality (3 blocks) | 0.384 s | 0.352 s | **1.09×** |
| SPYLEN states+E-MND | 4.68 s | 4.40 s | **1.06×** |
| HAT N4 \(B=8\) E-MND+locality (unfused vs fused) | 9.77 s | 6.57 s | **1.49×** |

`tracemalloc` peak for one SPYLEN E-MND pass: **~66 MB** (no material regression vs Phase 0 ~70 MB model).

**Interpretation for E01:** kernel-only gains are **small**. The **pipeline fusion**
(~1.5× on the N4 E-MND+locality battery) is the material Phase 1A win. It
**does not** by itself bring Cloud \(B=999\) SPY E01 into a short window; Phase 0
still implies multi-hour serial work. Report objectively: **insufficient alone
to solve the E01 runtime abort**, but a correct prerequisite for Phase 1B.

---

## 12. Gates C1–C8

| Gate | Result |
|------|--------|
| C1 scientific config unchanged | **PASS** |
| C2 reference/optimized BITWISE | **PASS** |
| C3 adversarial equivalence | **PASS** |
| C4 N4 integration equivalence | **PASS** |
| C5 N3 integration equivalence | **PASS** |
| C6 I03 regression (`tests/i03`) | **PASS** (88) |
| C7 measurable serial improvement | **PASS** (1.06–1.49×) |
| C8 no material memory regression | **PASS** |

---

## 13. Limitations

- Distance kernel still \(O(Q\cdot L\cdot D)\) per block; no ANN / approx.  
- `all_state_vectors_x` still per-\(t\) Python loop (cumsum rejected: would break bitwise).  
- Threading still ineffective (Phase 0).  
- Phase 1A does **not** implement process pools or checkpoint/resume.

---

## 14. Recommendation for Phase 1B

```text
PROCEED TO PHASE 1B — process-parallel surrogate-b execution
with BITWISE reassembly contract from Phase 0 §7,
on top of this fused/optimized serial kernel.
```

Also keep Cloud CPU ≥4 and/or fail-closed checkpoint as operational companions;
1-vCPU Cloud remains insufficient even after 1A.

---

## Engineering verdict

```text
PERF01-PHASE1A: PASS
```
