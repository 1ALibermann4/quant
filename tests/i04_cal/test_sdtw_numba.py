"""Numerical equivalence: Soft-DTW Numba vs reference."""

from __future__ import annotations

import time

import numpy as np
import pytest

from quant.i04_cal.sdtw import _HAS_NUMBA, clear_sdtw_self_cache, soft_dtw, soft_dtw_ref


pytestmark = pytest.mark.skipif(not _HAS_NUMBA, reason="numba not installed")


@pytest.mark.parametrize("W", [20, 40, 60])
@pytest.mark.parametrize("gamma", [0.1, 1.0, 10.0])
def test_sdtw_numba_matches_ref(W: int, gamma: float) -> None:
    rng = np.random.default_rng(42 + W)
    x = rng.normal(size=W)
    y = rng.normal(size=W)
    clear_sdtw_self_cache()
    a = soft_dtw_ref(x, y, gamma)
    b = soft_dtw(x, y, gamma, backend="numba")
    # Float64 contract: allow tiny ULPs from math lib ordering; require close
    assert np.isfinite(a) and np.isfinite(b)
    assert abs(a - b) <= max(1e-12, 1e-12 * abs(a))


def test_sdtw_numba_speedup_meaningful() -> None:
    rng = np.random.default_rng(7)
    W = 60
    pairs = [(rng.normal(size=W), rng.normal(size=W)) for _ in range(40)]
    # Warmup JIT
    soft_dtw(pairs[0][0], pairs[0][1], 1.0, backend="numba")
    t0 = time.perf_counter()
    for x, y in pairs:
        soft_dtw_ref(x, y, 1.0)
    t_ref = time.perf_counter() - t0
    t0 = time.perf_counter()
    for x, y in pairs:
        soft_dtw(x, y, 1.0, backend="numba")
    t_jit = time.perf_counter() - t0
    # Require at least 5x on this microbench (conservative)
    assert t_jit < t_ref / 5.0, f"ref={t_ref:.4f}s jit={t_jit:.4f}s"
