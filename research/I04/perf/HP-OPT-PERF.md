# I04-CAL HP-OPT — Performance Report (L4)

**Date**: 2026-10-12  
**Host**: ASUS i5-1035G1 / 8 logical / ~12 GiB  

## Before → After (Soft-DTW kernel)

| Metric | Baseline (ref) | Numba | Gain |
|--------|----------------|-------|------|
| W=20 pair | 0.834 ms | 0.024 ms | ~35× |
| W=40 pair | 2.60 ms | 0.077 ms | ~34× |
| W=60 pair | 5.69 ms | 0.189 ms | ~30× |
| Numeric | — | max‖Δ‖ ≤ 3e-11 | PASS |

## End-to-end cell (S0a, b=0, W=20, 1 worker)

| Family | elapsed_s | Notes |
|--------|-----------|-------|
| G1 | **1.16** | Was hours-class historically; now seconds |
| G0 | 10.3 | Vector KNN path; now slower than G1 W20 |
| G3 | 11.6 | Similar to G0 |
| G2 / G5 / G4 | deferred | Core strides 8/4 pairwise still dominate under load |

Smoke (packed tree, G1 gamma=10 W=20): **9.2 s** cold including import/JIT.

## Recommended CPU config (ASUS)

- `workers = logical_cpus - 1` → **7** on this host (avoid oversubscription; OMP=1)
- Soft-DTW backend: `auto` (Numba when installed)
- Cache: ON
- GPU: **OFF** (see HP-OPT-GPU.md)

## Projection (honest)

Assumptions: Numba on; cache on; 7 workers; G2/G5 still heavy.

| Scope | Estimate |
|-------|----------|
| Remaining cells | 12 027 (69 already in CANONICAL-02) |
| G1 share (2592 cells) | no longer the wall-clock monster at W=20 |
| Dominant remaining | **G2 + G5** pairwise under strides 8/4 |
| Ambitious 3 h full remaining | **Not guaranteed** without G2/G5 acceleration |
| 16 h bi-machine window | **Best available throughput**; maximize valid cells, not a PASS criterion |

Refine OptiPlex projection after first-boot microbench (`reports/hardware.json` + capacity knobs on split).

## Retained vs rejected

| Optimization | Verdict |
|--------------|---------|
| Numba Soft-DTW | **RETAINED** |
| Self-term + distance cache (PERF-02) | **RETAINED** |
| ProcessPool workers | **RETAINED** |
| GPU Intel UHD | **REJECTED** |
| Scientific stride / oracle / universe changes | **FORBIDDEN** |
