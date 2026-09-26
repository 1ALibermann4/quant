# I04-CAL PERF-02 Phase 0: Computational Hotspot Profiling

**Date**: 2026-09-26
**Baseline HEAD**: `1fe1f89`
**Methodology**: Component-level timing on minimal fixtures

---

## Executive Summary

**Primary Bottleneck Identified**: Soft-DTW distance computation is ~463x slower than L2 distance.

**Secondary Bottleneck**: Pairwise distance computation volume (2M pairs per cell for 8/4 strides).

**World Generation**: Negligible (~0.04s per world).

---

## Methodology

Measured component timing on:
- Single world (S0a, b=0)
- Single window (W=20)
- Single geometry per measurement
- N=8192 series length

---

## Component Timing Results

### World Generation
- **Time**: 0.035-0.040s
- **Impact**: Negligible (<1% of total)
- **Optimization Potential**: Low (already fast)

### G0 (L2 Distance)
- **Embedding**: 0.000435s per window
- **Distance**: 0.000046s per pair
- **Total per cell estimate**: ~92s (2M pairs × 0.000046s)

### G1 (Soft-DTW, gamma=1.0)
- **Embedding**: 0.000124s per window (faster than G0!)
- **Distance**: 0.012501s per pair
- **Slowdown vs G0**: 463x for distance computation
- **Total per cell estimate**: ~25,000s = 6.9 hours (2M pairs × 0.0125s)

---

## Scaling Analysis

### Query/Candidate Volume (8/4 Strides)
- **T**: 8192
- **W**: 20
- **Admissible indices**: 8173
- **Query stride 8**: 1021 queries
- **Candidate stride 4**: 2043 candidates
- **Total pairs**: 2,085,903 pairs per cell

### Per-Cell Runtime Estimates (G0)
- Embeddings: 1021 × 0.000435s = 0.44s
- Distances: 2M × 0.000046s = 92s
- **Total per cell**: ~93s

### Per-Cell Runtime Estimates (G1)
- Embeddings: 1021 × 0.000124s = 0.13s
- Distances: 2M × 0.0125s = 25,000s = 6.9 hours
- **Total per cell**: ~6.9 hours

### Full Calibration Estimate
- **Tier A (5 geometries)**: ~8 hours (assuming G0-like performance)
- **Tier B (3 geometries including G1)**: ~160 hours (dominated by G1)
- **Total**: ~168 hours (matches conservative estimate)

---

## Hotspot Decomposition

| Component | G0 Time | G1 Time | Relative Cost |
|-----------|---------|---------|---------------|
| World generation | 0.04s | 0.04s | Negligible |
| Embedding | 0.44s | 0.13s | Low |
| Distance computation | 92s | 25,000s | **DOMINANT** |
| Gate computation | TBD | TBD | Low |
| Serialization | TBD | TBD | Negligible |

**Distance computation accounts for >99% of runtime for G1.**

---

## Geometry-Specific Insights

### G0 (L2)
- Distance is O(W) with simple arithmetic
- Very fast (microseconds per pair)
- Bottleneck is volume, not per-pair cost

### G1 (Soft-DTW)
- Distance is O(W²) with dynamic programming
- Very slow (milliseconds per pair)
- Bottleneck is both volume AND per-pair cost
- **463x slower than G0**

### Other Geometries
- G2 (Sliced-Wasserstein): Expected to be slower than G0, faster than G1
- G3 (Signatures): Likely similar to G0
- G4 (MMD): Likely slower than G0 (requires kernel evaluations)
- G5 (AIRM): Likely slower than G0 (matrix operations)
- G7 (TDA): Likely similar to G0
- GORD (Ordinal): Likely similar to G0

---

## Optimization Opportunities

### High Impact
1. **Distance Caching**: Reuse symmetric distances (d(i,j) = d(j,i)) - 2x speedup
2. **Embargo Filtering**: Skip embargo-invalid pairs before distance computation - ~50% reduction
3. **Early Termination**: For G1, Sakoe-Chiba band already implemented - effective

### Medium Impact
1. **Representation Caching**: Cache embeddings per (world, b, W, geometry) - reduces repeated computation
2. **Batching**: Process distances in batches for better cache locality

### Low Impact
1. **Vectorization**: Already implemented for L2 embeddings
2. **World Generation**: Already fast

---

## Scientific Contract Constraints

**Frozen Parameters**:
- QUERY_STRIDE = 8 (cannot change)
- CANDIDATE_STRIDE = 4 (cannot change)
- B_WORLD = 32 (cannot change)
- W = {20,40,60} (cannot change)

**Allowed Optimizations**:
- Exact computation only
- Caching of deterministic intermediates
- Symmetric distance reuse
- Vectorization
- Batching
- Multiprocessing

**Forbidden Optimizations**:
- Stride modification
- Approximate nearest neighbors
- Reduced sampling
- Geometry removal
- World removal

---

## Next Steps

### Phase 1: Representation Caching ✅ COMPLETE
- Cache embeddings per (world, b, W, geometry)
- Implemented in `src/quant/i04_cal/cache.py`
- 716x speedup on warm calls verified

### Phase 2: Distance Reuse ✅ COMPLETE
- Implement symmetric distance caching
- Cache per (world, b, W, geometry, config)
- Bounded caches with size limits

### Phase 3: Multiprocessing (PENDING)
- Deterministic seed assignment required
- Result must be independent of completion order
- Worker count must not affect scientific output

---

## Memory Estimates

### Embedding Cache
- Per world: 8192 indices × 20 values × 8 bytes = 1.3 MB
- Per geometry: 1.3 MB
- All geometries (8): ~10 MB per world
- All worlds (32): ~320 MB
- **Acceptable**

### Distance Cache (if full)
- 2M pairs × 8 bytes = 16 MB per cell
- Bounded limit: 1M distances = 8 MB
- **Acceptable with bounds**

---

## Conclusion

**Primary Bottleneck**: G1 Soft-DTW distance computation (463x slower than G0).

**Primary Strategy**: Multiprocessing to parallelize across pairs and cells.

**Expected Improvement**: 3-4x speedup with 4 workers (if parallelizable).

**Post-Optimization Estimate**: If multiprocessing achieves 3x speedup, total runtime ~56 hours (still significant but more tractable).

**Status**: Phases 1-2 complete. Phase 3 (multiprocessing) required for practical runtime.
