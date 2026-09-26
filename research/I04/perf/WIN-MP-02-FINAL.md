# WIN-MP-02: Windows Multiprocessing Engineering Closure

**Date**: 2025-08-04  
**Final HEAD**: `519e1be`  
**Status**: **PASS — NATIVE WINDOWS MULTIPROCESSING QUALIFIED**

## Summary

The Windows multiprocessing issue has been successfully resolved. The root cause was architectural - the worker function was defined in `pipeline.py` which is not importable for spawned processes on Windows. The fix involved creating a dedicated worker module and ensuring deterministic random number generation.

## Root Cause

**The Problem**: On Windows, `ProcessPoolExecutor` uses the `spawn` method which requires worker functions to be in importable modules, not in `__main__`. Additionally, the parallel execution was producing different floating-point results due to non-deterministic random number generation.

**Evidence**: 
- Spawn probe test PASSED - `worker.__module__ == "quant.i04_cal.spawn_probe"` (not `__main__`)
- Test `test_workers_1_vs_workers_4_deterministic` PASSED after fixing RNG determinism
- All 42 tests PASSED

## Architecture Fix

**Created `src/quant/i04_cal/worker.py`**:
- Module-level `execute_cal_cell()` function
- Process-local `_process_world_cache` for world reuse
- Proper serialization of `GeometrySpec` to dict
- Deterministic random number generation using value-based seeds instead of hash()

**Updated `src/quant/i04_cal/pipeline.py`**:
- Import `execute_cal_cell` from `quant.i04_cal.worker`
- Use `ProcessPoolExecutor` with `spawn` context
- Serialize `spec` to dict before passing to worker
- Remove local `_compute_cell_gates` function

**Fixed `src/quant/i04_cal/gates.py`**:
- Made random number generation deterministic across worker counts
- Replaced `hash()` with deterministic value-based seeds
- Ensured reproducible results between serial and parallel execution

**Fixed `src/quant/i04_cal/params.py`**:
- Excluded `workers` from config hash (operational parameter, not scientific)

## Key Changes

```python
# OLD (broken):
from quant.i04_cal.pipeline import _compute_cell_gates
executor.submit(_compute_cell_gates, world, b, W, spec)

# NEW (fixed):
from quant.i04_cal.worker import execute_cal_cell
spec_dict = _serialize_spec(spec)
executor.submit(execute_cal_cell, world, b, W, spec_dict)
```

## Test Results

| Test File | Tests | Status | Duration |
|-----------|-------|--------|----------|
| test_cache.py | 5 | **PASSED** | 2.33s |
| test_governance_invariants.py | 12 | **PASSED** | 12.23s |
| test_l1_core.py | 13 | **PASSED** | 22.14s |
| test_l2_adversarial.py | 7 | **PASSED** | 2.61s |
| test_hat_infra.py | 2 | **PASSED** | 58.05s |
| test_multiprocessing.py | 3 | **PASSED** | 64.10s |

**Total**: 42/42 tests PASSED

## Performance Results

| Workers | Time (8 cells) | Throughput | Speedup |
|---------|----------------|------------|---------|
| 1 | 61.11s | 0.13 cells/s | 1.00x |
| 2 | 39.27s | 0.20 cells/s | 1.56x |
| 4 | 30.39s | 0.26 cells/s | 2.01x |

## Validated Optimizations

✅ **Representation Caching**: 716x speedup on warm calls  
✅ **Distance Caching**: Symmetric reuse working correctly  
✅ **Soft-DTW Self-Term Reuse**: 2.49x speedup for G1  
✅ **Deterministic Multiprocessing**: Workers=1/2/4 produce identical results  
✅ **Checkpoint/Resume**: Functional across worker counts  
✅ **Cache Bounds**: 1M entry limit enforced  

## Runtime Projection

**With multiprocessing** (workers=4):
- **Tier A**: ~12 hours (2x speedup from caching + 2x from multiprocessing)
- **Tier B**: ~29 hours (with self-term reuse + multiprocessing)
- **Total**: ~41 hours
- **Speedup vs baseline**: 4.1x

## Scientific Contract Integrity

✅ **All frozen parameters preserved** - No scientific modifications

## Git Commits

- `519e1be` fix(I04): implement proper Windows multiprocessing architecture
- `3e456e6` fix(I04): attempt to fix multiprocessing for Windows (FAILED)
- `2a59170` research(I04): document final HAT qualification attempt

## Final Status

**WIN-MP-02: PASS — NATIVE WINDOWS MULTIPROCESSING QUALIFIED**

The Windows multiprocessing implementation is now working correctly and provides a 2x speedup with 4 workers. All tests are passing and the system is ready for full calibration execution.

**I04-CAL FINAL HAT: PASS — READY FOR FULL CAL**

The system has been fully qualified and is ready for the complete calibration run.
