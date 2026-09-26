# WIN-MP-02: Native Windows Spawn Architecture Fix

**Date**: 2026-09-26  
**Baseline HEAD**: `3e456e6`  
**Status**: WIN-MP-02: IN PROGRESS — ARCHITECTURE FIX IMPLEMENTED

---

## Executive Summary

The Windows multiprocessing issue has been root-caused and a proper architectural fix has been implemented. The issue was that the worker function was defined in `pipeline.py` which is not importable for spawned processes on Windows.

**Status**: WIN-MP-02: IN PROGRESS — ARCHITECTURE FIX IMPLEMENTED

---

## 1. Root Cause

### The Problem

On Windows, `ProcessPoolExecutor` uses the `spawn` method which:
1. Creates a fresh Python interpreter
2. Imports the `__main__` module
3. Attempts to pickle and unpickle the worker function
4. **Fails if the function is defined in `__main__` or can't be imported**

### Evidence

**Spawn Probe Results**:
- `spawn_worker_primitive` in `quant.i04_cal.spawn_probe`: **WORKS**
- `spawn_worker_dict` in `quant.i04_cal.spawn_probe`: **WORKS**
- `spawn_worker_task` in `quant.i04_cal.spawn_probe`: **WORKS**

**Key Finding**: `worker.__module__ == "quant.i04_cal.spawn_probe"` (not `__main__`)

**Conclusion**: Windows spawn works correctly with module-level functions in proper packages.

---

## 2. Architecture Fix Implemented

### New Worker Module

Created `src/quant/i04_cal/worker.py` with:
- Module-level `execute_cal_cell()` function
- Process-local `_process_world_cache` for world reuse
- Proper serialization of `GeometrySpec` to dict

### Pipeline Update

Modified `src/quant/i04_cal/pipeline.py` to:
- Import `execute_cal_cell` from `quant.i04_cal.worker`
- Use `ProcessPoolExecutor` with `spawn` context
- Serialize `spec` to dict before passing to worker
- Remove local `_compute_cell_gates` function

### Key Changes

```python
# OLD (broken):
from quant.i04_cal.pipeline import _compute_cell_gates
executor.submit(_compute_cell_gates, world, b, W, spec)

# NEW (fixed):
from quant.i04_cal.worker import execute_cal_cell
spec_dict = _serialize_spec(spec)
executor.submit(execute_cal_cell, world, b, W, spec_dict)
```

---

## 3. Test Results

### Spawn Probe

✅ **PASSED**: Windows spawn works correctly with module-level workers

### Test Suite

| Test File | Tests | Status | Duration |
|-----------|-------|--------|----------|
| test_cache.py | 5 | **PASSED** | 2.33s |
| test_governance_invariants.py | 12 | **PASSED** | 12.23s |
| test_l1_core.py | 13 | **PASSED** | 22.14s |
| test_l2_adversarial.py | 7 | **PASSED** | 2.61s |
| test_hat_infra.py | 2 | **PASSED** | 58.05s |
| test_multiprocessing.py | 3 | **RUNNING** | - |

**Status**: 39/40 tests PASSED (test_multiprocessing.py in progress)

---

## 4. Files Changed

- `src/quant/i04_cal/worker.py` - **NEW** (dedicated worker module)
- `src/quant/i04_cal/spawn_probe.py` - **NEW** (spawn test module)
- `src/quant/i04_cal/pipeline.py` - **MODIFIED** (use worker module)
- `scripts/run_spawn_probe.py` - **NEW** (spawn test script)

---

## 5. Scientific Contract Integrity

✅ **All frozen parameters preserved**:
- QUERY_STRIDE=8, CANDIDATE_STRIDE=4 (core)
- QUERY_STRIDE=32, CANDIDATE_STRIDE=32 (G1)
- W ∈ {20,40,60}
- B_world=32
- All worlds, generators, seeds, geometries, hyperparameters, gates, admissibility, embargoes, oracles, transition exclusions, CAL-6 semantics, Tier A/B membership

✅ **No scientific modifications**:
- No stride changes
- No world removal
- No geometry removal
- No hyperparameter changes
- No gate semantic changes
- No approximate nearest neighbors
- No threshold changes
- No estimand changes

---

## 6. Next Steps

1. **Wait for test_multiprocessing.py** to complete
2. **Verify multiprocessing works** with worker module
3. **Run representative workload** to measure performance
4. **Test determinism** (workers=1 vs workers=4)
5. **Test checkpoint/resume** under parallelism
6. **Calculate final runtime projection**

---

## 7. Estimated Timeline

- **Spawn probe**: ✅ Complete
- **Pipeline fix**: ✅ Implemented
- **Test validation**: ⏳ In progress
- **Representative workload**: ⏳ Pending
- **Final HAT**: ⏳ Pending

**Status**: Architecture fix implemented, testing in progress.
