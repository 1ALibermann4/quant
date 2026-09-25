"""Contract-alignment tests for I02 L1 patch (PREREG-v0.3). No market data."""

from __future__ import annotations

import numpy as np
import pytest

from quant.i02.bootstrap import (
    frozen_block_lengths,
    mbb_spearman_ci,
    mbb_spearman_robustness,
    moving_block_bootstrap_indices,
)
from quant.i02.distances import (
    distance_s3_phi,
    distance_s3_q,
    phi_from_q,
)
from quant.i02.neighbors import select_neighbors
from quant.i02.params import DEFAULT_PARAMS
from quant.i02.pipeline import evaluate_query
from quant.i02.states_x import (
    XUndefinedError,
    causal_mu_sigma,
    first_valid_x_index,
    state_vector_x,
)
from quant.i02.types import SkipReason


def test_m_is_252():
    assert DEFAULT_PARAMS.M == 252
    assert first_valid_x_index(DEFAULT_PARAMS) == 252


def test_sigma_zero_x_undefined():
    r = np.full(300, np.nan, dtype=np.float64)
    r[1:] = 0.02  # constant after first → σ̂=0 on any full window of equals
    # Make M-window constant
    r[:] = np.nan
    r[1:] = 0.01
    with pytest.raises(XUndefinedError) as ei:
        state_vector_x(r, 260, DEFAULT_PARAMS)
    assert ei.value.reason == SkipReason.X_SIGMA_ZERO


def test_sigma_positive_exact_division_no_epsilon():
    rng = np.random.default_rng(7)
    r = np.full(400, np.nan, dtype=np.float64)
    r[1:] = rng.normal(0.0, 0.02, 399)
    t = 300
    mu, sigma = causal_mu_sigma(r, t, DEFAULT_PARAMS)
    assert sigma > 0.0
    x = state_vector_x(r, t, DEFAULT_PARAMS)
    w = DEFAULT_PARAMS.W_X
    window = r[t - w + 1 : t + 1]
    expected = (window - mu) / sigma
    np.testing.assert_allclose(x, expected)
    # Explicitly not the I01 (sigma+eps) form — must differ elementwise
    eps = 1e-8
    contaminated = (window - mu) / (sigma + eps)
    assert np.any(x != contaminated)


def test_s3_q_distance_exact():
    d = distance_s3_q(0.0, 0.0, 3.0, 4.0)
    assert d == pytest.approx(5.0)


def test_s3_phi_distance_exact():
    # Q=1 => phi=0; Q=0.5 => phi=arccos(0.5)=π/3
    d = distance_s3_phi(0.0, 1.0, 0.0, 0.5)
    assert d == pytest.approx(abs(0.0 - np.arccos(0.5)))
    assert phi_from_q(1.0) == pytest.approx(0.0)


def test_s3_ties_deterministic():
    library = np.array([10, 5, 8, 3], dtype=np.intp)
    # equal distances: older s first
    distances = np.array([1.0, 1.0, 0.5, 0.5], dtype=np.float64)
    nbrs, _ = select_neighbors(library, distances, k=2)
    assert list(nbrs) == [3, 8]


def test_pipeline_preserves_both_s3_branches(synthetic_returns):
    res = evaluate_query(synthetic_returns, 500, params=DEFAULT_PARAMS)
    if res.skipped:
        pytest.skip("skip at t=500")
    assert "S3_Q" in res.forecasts
    assert "S3_phi" in res.forecasts
    assert "S3_Q" in res.r and "S3_phi" in res.r
    # no single "S3" winner key
    assert "S3" not in res.forecasts


def test_mbb_noncircular_and_truncate():
    rng = np.random.default_rng(0)
    n, b, B = 100, 40, 5
    idx = moving_block_bootstrap_indices(n, b, B, rng)
    assert idx.shape == (B, n)
    assert idx.min() >= 0 and idx.max() < n
    # each full block of length b is contiguous; no wrap past n-1
    for row in idx:
        assert row.shape[0] == n
        pos = 0
        while pos + b <= n:
            block = row[pos : pos + b]
            assert list(block) == list(range(int(block[0]), int(block[0]) + b))
            assert int(block[-1]) < n
            pos += b
        # remainder is truncated prefix of a block (contiguous)
        rem = row[pos:]
        if rem.size:
            assert list(rem) == list(range(int(rem[0]), int(rem[0]) + rem.size))


def test_mbb_seed_reproducibility():
    z = np.linspace(0, 1, 200)
    r = z + 0.01 * np.sin(np.arange(200))
    a = mbb_spearman_ci(z, r, b=40, seed=42)
    b = mbb_spearman_ci(z, r, b=40, seed=42)
    assert a.ci_low == b.ci_low and a.ci_high == b.ci_high
    assert a.rho_hat == b.rho_hat
    assert a.n_finite_replicates == b.n_finite_replicates
    assert a.n_finite_replicates >= int(np.ceil(0.8 * DEFAULT_PARAMS.bootstrap_B))


def test_mbb_contract_B_and_blocks():
    assert DEFAULT_PARAMS.bootstrap_B == 9999
    assert DEFAULT_PARAMS.bootstrap_seed == 42
    assert frozen_block_lengths() == (40, (20, 40, 80))


def test_mbb_n_less_than_b_inconclusive():
    z = np.arange(10, dtype=float)
    r = z.copy()
    out = mbb_spearman_ci(z, r, b=40)
    assert out.inconclusive
    assert out.reason == SkipReason.BOOTSTRAP_INSUFFICIENT_N


def test_mbb_robustness_all_b():
    rng = np.random.default_rng(1)
    z = rng.normal(size=300)
    r = 0.3 * z + rng.normal(scale=0.5, size=300)
    grid = mbb_spearman_robustness(z, r)
    assert set(grid) == {20, 40, 80}
    for b, res in grid.items():
        assert res.b == b
        if not res.inconclusive:
            assert res.ci_low is not None and res.ci_high is not None
            assert res.detectable is not None


def test_percentile_ci_excludes_zero_when_strong():
    z = np.arange(400, dtype=float)
    r = z.copy()
    out = mbb_spearman_ci(z, r, b=40)
    assert not out.inconclusive
    assert out.detectable is True
    assert out.ci_low is not None and out.ci_low > 0


def test_query_sigma_zero_skip_reason():
    r = np.full(400, np.nan, dtype=np.float64)
    r[1:] = 0.01
    res = evaluate_query(r, 300, params=DEFAULT_PARAMS)
    assert res.skipped
    assert SkipReason.X_SIGMA_ZERO in res.skip_reasons


def test_degenerate_bootstrap_dropped_or_inconclusive():
    # Constant Z ⇒ Spearman undefined on point estimate and replicates
    z = np.ones(200, dtype=np.float64)
    r = np.linspace(0, 1, 200)
    out = mbb_spearman_ci(z, r, b=40)
    assert out.inconclusive
    assert out.reason == SkipReason.BOOTSTRAP_DEGENERATE
    assert out.n_finite_replicates < int(np.ceil(0.8 * DEFAULT_PARAMS.bootstrap_B))


def test_no_branch_selection_keys(synthetic_returns):
    res = evaluate_query(synthetic_returns, 500, params=DEFAULT_PARAMS)
    if res.skipped:
        pytest.skip("skip at t=500")
    # both charts present; no selector / winner field
    assert set(res.forecasts) >= {"S3_Q", "S3_phi"}
    assert not hasattr(res, "s3_primary")
    assert "S3" not in res.forecasts
