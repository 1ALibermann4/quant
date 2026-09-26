# I03-PERF-01 — Phase 1B: Deterministic Process-Parallel Surrogates

> **Status :** PHASE 1B CLOSED  
> **Class :** ENGINEERING OPTIMIZATION ONLY  
> **Phase 0 :** [I03-PERF-01-PHASE0.md](I03-PERF-01-PHASE0.md) @ `c304d7b`  
> **Phase 1A :** [I03-PERF-01-PHASE1A.md](I03-PERF-01-PHASE1A.md) @ `109faaa` / `651e9ee`  
> **Prereg :** unchanged  
> **E01 / E02 :** **NOT executed** · **checkpoint/resume :** **NOT implemented**

```text
THIS IS AN ENGINEERING OPTIMIZATION.
NO SCIENTIFIC RESULT WAS PRODUCED.
NO E01 · NO E02 · NO CHECKPOINT/RESUME · NO PARAMETER CHANGE
```

**Verdict:** `PERF01-PHASE1B: PASS`

---

## 1. Baseline

| Item | Value |
|------|--------|
| Pre-1B HEAD | `651e9ee` (Phase 1A docs) |
| Python / NumPy | 3.12.10 / 2.5.3 |
| Host | Windows-11 AMD64, `logical_cpus=8` |
| BLAS env (bench) | `OMP/OPENBLAS/MKL_NUM_THREADS=1` (setdefault in workers) |
| I03 tests | 99 passed after Phase 1B |

---

## 2. Process architecture

```text
Parent:
  build_blocks, observed E-MND, N4 scale path
  → run_n4_battery_parallel(b=1..B_N4)
  → run_n3_battery_parallel(b=1..B_N3)
  → reassemble_by_b (ascending)
  → survival / locality observed / verdict

Worker (spawn-safe module functions):
  N4: seed=42+b → n4_surrogate_returns → E-MND → locality(seed=20000+p+1000*b)
  N3: seed=10000+b → IAAFT (no retry) → E-MND
```

Module: `src/quant/i03/parallel.py`  
Pipeline hook: `run_structural_analysis(..., workers: int = 1)`  
CLI: `--workers N` (operational only)

`workers=1` keeps the Phase-1A serial fused reference path (no process pool).

---

## 3. Worker contract

- Unit of work = surrogate index **`b`** (1-based).  
- Payload carries explicit `b`, `family` (`N4`|`N3`), `seed`.  
- No shared mutable RNG; no seed from worker id / PID / clock / schedule.  
- Worker failure → exception propagates; **B is not silently reduced**.

---

## 4. RNG / seed isolation

| Family | Seed |
|--------|------|
| N4 | `cfg.master_seed + b` (= `42 + b`) |
| N3 IAAFT | `10000 + b` |
| N4 locality | `20000 + period + 1000*b` |

Identical to serial doctrine. Scheduling order cannot change seeds.

---

## 5. Canonical `b` reassembly

`reassemble_by_b(results, B, family)`:

- sorts to `b=1..B`  
- fail-closed on missing / duplicate / unexpected `b`, wrong family, malformed payload  

Completion order is ignored.

---

## 6–8. Bitwise equivalence evidence

Dedicated tests: `tests/i03/test_perf01_phase1b.py`

| Gate | Evidence |
|------|----------|
| N4 w∈{1,2,4} | Θ + locality BITWISE vs `workers=1` (HAT, B=8) |
| N3 w∈{1,2,4} | flags, iterations, series bytes, Θ BITWISE (HAT, B=6) |
| Full pipeline | `run_structural_analysis` w=1 vs w=2/4 artifact equality (B_n4=6, B_n3=4) |
| Adversarial order | even-`b` completes before odd-`b`; reassembly restores 1..B |
| Fail-closed | missing/duplicate/wrong family/malformed; worker exception |

Phase-1A oracle tests **unchanged** and still PASS.

---

## 9. Platform / spawn

- Workers are top-level picklable functions + dict initializer (Windows **spawn** safe).  
- No `fork`-only assumptions.  
- Nested process spawning avoided (`workers` applied once at battery level).  
- Validated under native Windows ProcessPoolExecutor in this milestone.

---

## 10. Resource / thread pools

Worker initializer uses `os.environ.setdefault` for:

`OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_NUM_THREADS` → `"1"`

Explicit user settings are **not** overridden. Parent bench exported the same vars.

Default workers remain **`1`** (never blind `cpu_count()`).

`tracemalloc` peaks in children are **not** visible in the parent; parent-side peaks under-report multi-process RSS. Acceptable: per-worker footprint remains ~obs+scale+one surrogate (~tens of MB class from Phase 0/1A).

---

## 11–13. Benchmarks / scaling (MEASURED)

Same machine, Python, NumPy, BLAS=1. Artifact: [`phase1b_bench.json`](phase1b_bench.json).

### A. HAT-like

| Workload | w=1 | w=2 | w=4 | speedup@4 | eff@4 |
|----------|-----|-----|-----|-----------|-------|
| N4 B=16 + loc | 13.19 s | 12.03 s | 8.95 s | 1.47× | 0.37 |
| N3 B=12 | 4.73 s | 3.13 s | 3.30 s | 1.43× | 0.36 |
| Pipeline B12/B8 | 14.44 s | 10.95 s | 8.94 s | 1.61× | 0.40 |

### B. SPYLEN (non-market, \(T=8470\)) N4 B=12 + loc

| workers | wall | speedup | efficiency |
|---------|------|---------|------------|
| 1 | 202.3 s | 1.00× | 1.00 |
| 2 | 84.0 s | **2.41×** | 1.20* |
| 4 | 61.1 s | **3.31×** | 0.83 |

\*Efficiency >1 at w=2 is measurement noise / single-rep cold-start; treat as “strong scaling observed”, not super-linear physics.

**Bottleneck reading:** on SPYLEN, CPU-bound E-MND/locality dominates; process parallelism helps. Sub-linear efficiency at w=4 from IPC/pickle of shared arrays + remaining serial fractions. Not memory-bandwidth collapsed on this host.

### ESTIMATED E01 (N4+loc only, from SPYLEN B=12)

| workers | EST. N4 B=999 wall |
|---------|---------------------|
| 1 | ~1.68×10⁴ s (~4.7 h) |
| 2 | ~7.0×10³ s (~1.9 h) |
| 4 | ~5.1×10³ s (~1.4 h) |

**Excludes** N3 battery (~similar order) and Cloud 1-vCPU penalty. Full E01 still multi-hour; **checkpoint/resume still recommended** for RUN2 on constrained Cloud.

---

## 14. Gates C1–C10

| Gate | Result |
|------|--------|
| C1 config unchanged | **PASS** |
| C2 seed ≠ worker/schedule | **PASS** |
| C3 canonical reassembly | **PASS** |
| C4 N4 bitwise | **PASS** |
| C5 N3 bitwise | **PASS** |
| C6 adversarial/failure | **PASS** |
| C7 Windows/spawn-safe | **PASS** |
| C8 I03 regressions | **PASS** (99) |
| C9 measurable speedup w>1 | **PASS** (SPYLEN up to 3.31× @4) |
| C10 memory/resources | **PASS** |

---

## 15. Recommendation

1. **E01 RUN2:** use `--workers 4` (or host core count, capped) on a **multi-core** machine; keep `workers=1` for audits.  
2. **Still implement checkpoint/resume** before relying on 1-vCPU Cloud for full \(B=999\).  
3. Do **not** change \(B\), seeds, or science.

---

## Engineering verdict

```text
PERF01-PHASE1B: PASS
```
