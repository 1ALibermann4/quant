"""Pipeline integration tests on synthetic returns (no market data)."""

from __future__ import annotations

import numpy as np
import pytest

from quant.i02.pipeline import evaluate_query, evaluate_series
from quant.i02.params import DEFAULT_PARAMS
from quant.i02.pool import admissible_pool
from quant.i02.types import SkipReason


def test_evaluate_query_common_pool_and_k(synthetic_returns):
    p = DEFAULT_PARAMS
    t = 500
    res = evaluate_query(synthetic_returns, t, params=p)
    assert not res.skipped or SkipReason.INSUFFICIENT_ADMISSIBLE_POOL in res.skip_reasons
    if res.skipped:
        pytest.skip("synthetic draw produced small pool at t=500")
    assert res.pool_size >= p.k
    assert "X" in res.forecasts and "S1" in res.forecasts and "S2" in res.forecasts
    assert "S3_Q" in res.forecasts and "S3_phi" in res.forecasts
    for name in ("X", "S1", "S2", "S3_Q", "S3_phi"):
        f = res.forecasts[name]
        assert f.neighbor_indices.shape == (p.k,)
        assert f.atoms.shape == (p.k,)
    pool = admissible_pool(synthetic_returns, t, p)
    assert np.array_equal(pool, res.pool_indices)


def test_insufficient_pool_skips_without_adaptive_k():
    p = DEFAULT_PARAMS
    # Short series: cannot form |A|>=50
    r = np.full(100, np.nan, dtype=np.float64)
    r[1:] = 0.01
    res = evaluate_query(r, 80, params=p)
    assert res.skipped
    assert SkipReason.INSUFFICIENT_ADMISSIBLE_POOL in res.skip_reasons or (
        SkipReason.INSUFFICIENT_X_HISTORY in res.skip_reasons
    )


def test_series_stride_one(synthetic_returns):
    p = DEFAULT_PARAMS
    # Restrict to a few queries for speed
    idx = np.arange(400, 420, dtype=np.intp)
    results = evaluate_series(synthetic_returns, params=p, query_indices=idx)
    assert len(results) == len(idx)
    assert [r.t for r in results] == list(idx)


def test_z_not_filtering_neighbors(synthetic_returns):
    p = DEFAULT_PARAMS
    t = 520
    res = evaluate_query(synthetic_returns, t, params=p)
    if res.skipped:
        pytest.skip("skip at t")
    # Forecast neighbors selected from pool only — Z may be None on some m
    # but forecasts still present
    assert "X" in res.forecasts
    assert res.z.keys() == {3, 12, 21}
