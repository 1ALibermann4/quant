# I03-PERF-01 — Phase 0: Profiling and Parallelization Design

> **Status :** PHASE 0 CLOSED  
> **Class :** ENGINEERING ONLY — no SCI / PRED / ECON meaning  
> **Prereg :** [I03-PREREG-v0.1.md](../I03-PREREG-v0.1.md) @ `0ff457a` — **unchanged**  
> **E01 :** **NOT executed** in this milestone  
> **Evidence :** `phase0_bench.json`, `phase0_process_scaling.json`, `cprofile_hat_B10_B5.txt`

```text
NO I03-E01 EXECUTION
NO SPY run_structural_analysis
NO MARKET SCIENTIFIC RESULT
NO PREREG CHANGE
NO PARAMETER CHANGE
NO PARALLEL IMPLEMENTATION (Phase 0 design only)
```

**Engineering verdict (end of document):** `PERF01-PHASE0: PROCEED`

---

## 1. RUN1 resource context

| Item | Value |
|------|--------|
| Cloud RUN1 status | `I03-E01 CLOUD RUN1: ABORTED — RESOURCE CONSTRAINT` |
| Abort evidence commit (reported) | `dfa3bd9c489fa62a6ebc0cc5eb79b6572bf4c95e` |
| Logged wall window | **4312.440428 s** (~71.9 min) |
| Last progress line | **N4 E-MND 950/999** |
| Scientific verdict | **NONE** (abort; no exploratory label; no partial interpretation) |

**Implication.** RUN1 died inside the N4 E-MND surrogate loop, after N4 surrogate generation and before N3 IAAFT / N3 E-MND / N4 locality batteries. Wall time is therefore dominated by **per-surrogate E-MND** on SPY-length \(T=8470\), not by N4 residual permutation itself.

Local Phase-0 timing on a SPY-**length** synthetic series (non-market) measured
\(\approx 4.10\,\mathrm{s}\) per N4 E-MND. Cloud abort implies
\(4312.44 / 950 \approx 4.54\,\mathrm{s}\) per N4 E-MND — consistent order of magnitude
(Cloud slightly slower / noisier).

---

## 2. Execution call graph

```text
E01 / runtime
  └─ run_structural_analysis(returns, cfg)          [pipeline.py]
       ├─ build_blocks(T, cfg)                      [blocks.py]
       ├─ _emnd_on_returns(obs)                     [states + E-MND observed]
       │    ├─ build_states_x                       [g0 → i02.states_x]
       │    └─ compute_emnd_all → compute_emnd_block × P
       ├─ generate_n4_battery                       [n4.py]
       │    ├─ build_n4_scale_path (σ̂, z, Z)        # once, observed
       │    └─ for b=1..B_N4: n4_surrogate_returns  # seed = 42+b
       ├─ generate_n3_battery                       [n3.py]
       │    └─ for b=1..B_N3: iaaft(..., seed=10000+b)
       ├─ for b=1..B_N4: _emnd_on_returns(n4_sur[b])   # N4 E-MND  ★ HOT
       ├─ for b=1..B_N3: _emnd_on_returns(n3_sur[b])   # N3 E-MND  ★ HOT
       ├─ build_survival_grid                       [coherence / p-values]
       ├─ locality_for_block × P (observed)         [seed 20000+p]
       ├─ for b=1..B_N4: locality × P on n4_sur[b]  # N4 locality ★ HOT
       │         seeds 20000+p+1000*b
       └─ decide_verdict                            [verdict.py]
```

Frozen constants (must remain): \(W_X=M_\sigma=\tau=20\), \(M=252\),
\(K=\{10,25,50\}\), \(P=3\), \(n_{\min}=250\), \(B=999\), N4/N3 seed doctrines,
IAAFT \(I_{\max}=100\), \(\varepsilon=10^{-8}\), \(\alpha=0.05\).

---

## 3. Loop inventory

| Loop | Location | Sequential dep.? | Independent across iter.? | RNG | Major work | Parallel candidate? |
|------|----------|------------------|---------------------------|-----|------------|---------------------|
| \(b=1..B\) N4 gen | `generate_n4_battery` | No | **Yes** (seed \(42+b\)) | per-\(b\) `default_rng` | permute \(z\) on \(Z\); Python `for` over \(Z\) | Yes (low value — cheap) |
| \(t\) in scale path | `build_n4_scale_path` | Yes (once) | N/A | none | rolling stdev | Serial / micro-opt only |
| \(b=1..B\) N4 E-MND | `pipeline` | No | **Yes** | none in E-MND | `build_states_x` + `compute_emnd_block`×P | **Primary** |
| \(t\) queries / block | `compute_emnd_block` | Yes within block | No (reduction order fixed) | none | distances + `lexsort` | Keep serial **within** \(b\) |
| \(k \in K\) | inside E-MND | Yes | trivial | none | index into sorted distances | No |
| \(b=1..B\) IAAFT | `generate_n3_battery` | No | **Yes** (seed \(10000+b\)) | per-\(b\) | rFFT/irFFT ≤100 iters | Yes (secondary; cheap vs E-MND) |
| IAAFT iteration | `iaaft` | Yes | No | owned by \(b\) | FFT + rank map | No (preserve convergence) |
| \(b=1..B\) N3 E-MND | `pipeline` | No | **Yes** | none | same as N4 E-MND | **Primary** |
| \(b=1..B\) N4 locality | `pipeline` | No | **Yes** (seed \(20000+p+1000b\)) | per call | similar distance work | **Primary** |
| \(t\) locality queries | `locality_for_block` | Yes within block | No | stream per seed | distances + `rng.choice` | Keep serial within \(b\) |

**Natural parallel unit**

```text
result_b = f(returns_obs | scale_obs | cfg, seed_b)
```

with strict reassembly in ascending \(b\).

---

## 4. Profiling evidence

### 4.1 Environment (local Phase 0)

- CPython 3.12.10 / Windows AMD64 / NumPy 2.5.3  
- `os.cpu_count() = 8`  
- Fixtures: **I03-HAT** (\(T=2400\)); **SPYLEN** = i.i.d. synthetic length **8470** (timing scale only; **not** SPY; **not** E01)

Artifacts: [`phase0_bench.json`](phase0_bench.json), [`cprofile_hat_B10_B5.txt`](cprofile_hat_B10_B5.txt), [`phase0_process_scaling.json`](phase0_process_scaling.json).

### 4.2 Microbench (mean wall seconds)

| Stage | HAT \(T=2400\) | SPYLEN \(T=8470\) |
|-------|----------------|-------------------|
| `build_states_x` | 0.076 | 0.226 |
| E-MND observed | 0.323 | **4.75** |
| N4 one surrogate | 0.001 | 0.005 |
| N4 one E-MND | **0.299** | **4.10** |
| IAAFT one | 0.020 | 0.065 |
| N3 one E-MND | 0.316 | **3.55** |
| Locality one block | 0.084 | (scaled in §7) |
| N4 gen+E-MND \(B=20\) | 6.02 | — |

### 4.3 cProfile (HAT, \(B_{N4}=10\), \(B_{N3}=5\), locality-on-N4 off)

Cumulative hotspots:

1. `compute_emnd_block` — dominant `tottime`  
2. `build_states_x` / `causal_mu_sigma` / `np.std`  
3. `admissible_pool`  
4. `locality_for_block` (when enabled)  
5. IAAFT / N4 generation — far smaller

---

## 5. Hotspot ranking

| Rank | Component | Role in RUN1 abort | Relative cost (SPYLEN ×999 est.) |
|------|-----------|--------------------|----------------------------------|
| 1 | **N4 E-MND battery** | Abort at 950/999 | ~4095 s (~68 min) |
| 2 | **N3 E-MND battery** | Not reached | ~3546 s |
| 3 | **N4 locality battery** | Not reached | ~3457 s (est.) |
| 4 | N3 IAAFT battery | Not reached | ~65 s |
| 5 | N4 surrogate generation | Completed before abort | ~5 s |
| 6 | Observed E-MND / states | Once | ~5 s |

**Conclusion.** Wall time is **not** limited by N4 permutation or IAAFT FFT count.
It is limited by **repeated full G0+E-MND (and locality) passes over \(B=999\)**
on long series. Parallelizing generation alone will not fix RUN1-class aborts.

---

## 6. RNG / state analysis

| State | Class | Notes |
|-------|-------|-------|
| `cfg` / blocks geometry | Read-only shared | Safe to broadcast |
| Observed `returns`, N4 `scale` (\(\sigmâ,z,Z\)) | Read-only shared after construction | Safe |
| Per-\(b\) RNG | **Owned by \(b\)** | `default_rng(42+b)` / `(10000+b)` / locality seeds — **no shared Generator** |
| Surrogate arrays | Mutable local | Independent writes |
| E-MND / locality outputs | Pure functions of inputs + seed | No hidden globals observed |
| Progress `print` | Side effect | Must not gate science |

**Independence:** surrogate \(b\) executions are **independent**. No shared mutable RNG.
No cross-\(b\) reduction until survival / validity aggregation (order of aggregation
must remain deterministic: raise by ascending \(b\)).

**GIL:** E-MND / locality spend substantial time in **Python iteration**
(`compute_emnd_block` query loop, `admissible_pool`) plus NumPy ufuncs.
Measured **thread** pool on HAT \(B=8\) N4 gen+E-MND: **no speedup**
(1→2→4 workers: 2.36 / 2.42 / 3.02 s vs serial 2.67 s). Threads are
**inappropriate** as the primary strategy.

**Processes:** HAT \(B=8\) process pool: serial 2.26 s → 2 workers 1.89 s
(~1.19×) → 4 workers 1.56 s (~1.45×). Positive scaling with spawn overhead;
expect better amortization at \(B=999\).

---

## 7. Determinism contract (pre-implementation)

Future parallel execution **must** preserve frozen science. Equivalence gates:

### BITWISE_IDENTICAL (required when order-independent)

| Object | Rule |
|--------|------|
| N4 surrogate returns \(r^{*(b)}\) | Bit-identical to serial for each \(b\) (same seed, same algorithm) |
| N3 IAAFT series + `converged` + `iterations` | Bit-identical per \(b\) |
| Per-\(b\) \(\Theta_k(p)\) maps | Bit-identical if each \(b\) runs serial E-MND internally (preferred) |
| N4 scale path on observed | Unchanged (computed once) |
| Convergence / non-convergence flags | Exact |
| Validity flags (`n4.valid`, `n3.valid`, \(V\), \(E\)) | Exact |
| Survival / coherence booleans \(S\), \(C4\), \(C3\), \(F4\) | Exact |
| Finite \(p\)-values | Exact under identical \(\Theta\) inputs |
| Final structural verdict label / `nd_code` | Exact |

### NUMERICALLY_IDENTICAL (only if bitwise unjustified)

Prefer **never** relaxing. If a future vectorized reduction **within** one \(b\)
changed FP association order, document an explicit ULPs/abs tolerance **before**
implementation — **do not** weaken gates merely to pass a parallel harness.

**Reassembly:** workers may complete out of order; parent **sorts by \(b\)** before
building `theta_n4`, `theta_n3`, `loc_n4`, and all aggregations.

**Forbidden:** changing \(B\), seeds, batching that merges RNG streams, approximate
FFT, GPU numeric substitution, adaptive early stop, selective surrogate replacement.

---

## 8. Resource / scaling model

### 8.1 Serial estimate (local SPYLEN microbench → \(B=999\))

| Component | \(T_{\mathrm{serial}}\) est. |
|-----------|------------------------------|
| N4 E-MND | ~4095 s |
| N3 E-MND | ~3546 s |
| N4 locality | ~3457 s |
| N3 IAAFT | ~65 s |
| N4 gen + obs | ~10 s |
| **Total** | **\(\approx 1.1\times 10^4\,\mathrm{s} \approx 3.1\,\mathrm{h}\)** |

Cloud RUN1: ~71.9 min to 95% of **N4 E-MND only** → full Cloud serial would be
**many hours** (N4 E-MND remainder + full N3 + locality).

### 8.2 Ideal \(T(N)\) (embarrassing over \(b\), perfect scaling)

\[
T(N) \approx T_{\mathrm{fixed}} + T_{\mathrm{parallel}} / N
\]

with \(T_{\mathrm{parallel}} \approx\) N4/N3 E-MND + N4 locality (~11 000 s local est.),
\(T_{\mathrm{fixed}}\) small. Theoretical: \(N=2 \Rightarrow \sim 1.6\,\mathrm{h}\),
\(N=4 \Rightarrow \sim 0.8\,\mathrm{h}\) on a machine matching local SPYLEN rates.

Measured process scaling at small \(B\) is **sub-linear** (init overhead).
Expect closer to ideal only for large \(B\) and warm workers.

### 8.3 Thread vs process vs 1-vCPU Cloud

| Mode | Local evidence | Cloud ~1 vCPU |
|------|----------------|---------------|
| Serial | Baseline | Matches abort economics |
| Threads | **No benefit** (GIL / Python loops) | No benefit |
| Processes \(N=2..4\) | Modest–good speedup on 8-core host | **No wall-time win** if only ~1 effective CPU; may **hurt** via contention |
| Checkpoint / resume | Operational only | Can finish multi-hour jobs without changing science |

**Explicit statement:** If Cloud effectively provides **~1 vCPU**, **parallelization
alone will not solve** Cloud wall-time / abort risk. Need a **larger CPU quota**,
**local multi-core** execution, and/or **fail-closed checkpoint/resume** that
replays exact \(b\) streams without adaptive stopping.

### 8.4 Memory

| Item | Estimate |
|------|----------|
| One returns vector \(T=8470\) | ~68 KB |
| 999 resident surrogates | ~68 MB |
| One states matrix \((T,20)\) | ~1.4 MB |
| Serial peak (current design) | **\(\sim 70\,\mathrm{MB}\)** + allocator churn — not the abort driver |
| Per process worker | ~obs + scale + one surrogate + states (~few MB) × workers |

Memory is **not** the primary constraint; **CPU-hours on E-MND** are.

---

## 9. Alternative execution options (not implemented)

| Option | Pros | Cons / science risk |
|--------|------|---------------------|
| Optimized serial | No determinism surface change if alg identical | Limited; E-MND asymptotic still \(O(B\cdot P\cdot Q\cdot L)\) |
| **Multiprocessing over \(b\)** | Matches independence; measured positive scaling | Needs reassembly contract; IPC overhead; useless on 1 vCPU |
| Threading | Low IPC | **Measured ineffective** |
| Vectorization within E-MND | Could cut serial constant | Must preserve distance/`lexsort` semantics → prefer exact identity |
| Chunked surrogate execution | Same as process chunks | OK if chunking ≠ RNG merge |
| **Checkpoint / resume** | Survives Cloud time limits | Allowed **only** as operational replay of exact \(b\); **no** selective replace / adaptive stop / partial science |
| Local multi-core hardware | Best practical path for full \(B=999\) | Operational, not Cloud-1vCPU |

---

## 10. Risks

1. **1-vCPU Cloud:** parallel Phase 1 insufficient alone.  
2. **FP relaxation pressure:** reject unless mathematically justified.  
3. **Hidden order dependence:** must keep intra-\(b\) E-MND serial.  
4. **Materialize-all-then-E-MND:** current pipeline allocates 999 arrays before
   E-MND — harmless for RAM; streaming per \(b\) is optional operational cleanup.  
5. **Progress logging:** Cloud abort line is engineering telemetry only — not a
   scientific checkpoint.  
6. **false “speedup” via \(B\) cut:** forbidden.

---

## 11. Recommendation for Phase 1

Implement **process-based parallel execution over surrogate index \(b\)** for:

1. N4 E-MND evaluation (and optionally N4 generation inside the worker),  
2. N3 IAAFT + N3 E-MND,  
3. N4 locality,

with **strict ascending-\(b\) reassembly** and a **BITWISE** equivalence harness on
the HAT / SPYLEN fixtures (never market E01 in the harness).

Additionally (still non-scientific):

- Document Cloud **CPU requirement** (≥4 effective cores recommended for
  practical wall time),  
- Design **optional fail-closed checkpoint/resume** of completed \(b\) results
  (exact replay; no adaptive stop),  
- Optional **serial micro-optimizations** that preserve bit-identical outputs
  (e.g. vectorize N4 \(Z\)-loop write; accelerate `states_x` without changing
  formulas).

Do **not** prioritize threading. Do **not** change \(B\), seeds, or nulls.

---

## Engineering verdict

```text
PERF01-PHASE0: PROCEED
```

Rationale: surrogate-\(b\) work is independent with per-\(b\) RNG ownership;
hotspots are E-MND/locality batteries; process parallelism is the appropriate
engine; a pre-declared bitwise determinism contract is feasible. Proceed to
Phase 1 **implementation of parallel execution + equivalence tests**, with the
explicit caveat that **1-vCPU Cloud needs more CPU and/or checkpoint/resume** —
parallelism alone is not a Cloud-1vCPU fix.

This verdict has **no** SCI / PRED / ECON meaning.
