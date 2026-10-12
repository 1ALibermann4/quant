# I04-CAL HP-OPT — Profiling Report (L1)

**Date**: 2026-10-12  
**Branch**: `perf/I04-CAL-hp-opt`  
**Baseline code tip (scientific parent)**: `a268029440d757a3e283f80e1e33f09db5ab86a8`  
**Machine (ASUS)**: Intel i5-1035G1 (4C/8L), ~12 GiB RAM, Intel UHD Graphics  

## Identity checks

| Reference | Expected | Observed | Status |
|-----------|----------|----------|--------|
| config_hash | `70e996a1…ba1f5` | `70e996a15397c91e8db12edee6cadc4e96615fbdf0424811cb7f20eb396ba1f5` | MATCH |
| universe | 12096 | 12096 | MATCH |
| CANONICAL-02 completed | 69 | 69 | PRESERVED |
| seed contract | `I04-CAL-SEED-v1` | same | MATCH |

## Architecture (engine)

- Workers: `ProcessPoolExecutor` + Windows `spawn` (`worker.execute_cal_cell`)
- Checkpoints: atomic JSON per cell, fail-closed resume
- Cache: embeddings + symmetric distances (PERF-02)
- Soft-DTW: moved to `sdtw.py` with optional Numba JIT (`backend=auto`)

## Bottlenecks (ordered)

1. **G1 Soft-DTW pair loops** — dominant before HP-OPT (~hours/cell historically).
2. **Pairwise volume** on non-vector geometries (G1/G2/G4/G5).
3. **G2 sliced-Wasserstein** — secondary after Soft-DTW acceleration.
4. **Checkpoint/JSON serialization** — visible but secondary.
5. **Process spawn / import** — one-time overhead per worker.

## Soft-DTW microbench (80 pairs, gamma=1)

| W | t_ref (s) | t_numba (s) | speedup | max‖Δ‖ |
|---|-----------|-------------|---------|--------|
| 20 | 0.067 | 0.0019 | **~35×** | 0 |
| 40 | 0.208 | 0.0062 | **~34×** | ≤5e-16 |
| 60 | 0.455 | 0.0151 | **~30×** | ≤3e-11 |

Artifact: `research/I04/perf/HP-OPT-PROFILE.json`

## Component timing (qualitative)

| Phase | Share (G1) | Note |
|-------|------------|------|
| Prep / world gen | ≪1% | cached per (world,b) in worker |
| Representation | low | embedding cache |
| Distance Soft-DTW | **>95%** historically | Numba path |
| Metrics / gates | moderate | reuses NN cache |
| Serialization | low–moderate | large gate payloads |
| Checkpoint | low | atomic replace |

## Conclusion Phase A

G1 Soft-DTW is the primary lever. Numba preserves float64 contract within measured ULP/ε and is retained for Phase B.
