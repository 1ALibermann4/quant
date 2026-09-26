"""PERF-01 Phase 1A — exact E-MND/locality kernel equivalence (non-market)."""

from __future__ import annotations

import math

import numpy as np
import pytest

from quant.i03.blocks import TemporalBlock, build_blocks
from quant.i03.emnd import admissible_pool, compute_emnd_all, compute_emnd_block
from quant.i03.fixture_hat import generate_hat_returns
from quant.i03.g0 import build_states_x
from quant.i03.iaaft import iaaft
from quant.i03.locality import locality_for_block
from quant.i03.n3 import generate_n3_battery
from quant.i03.n4 import generate_n4_battery, n4_surrogate_returns, build_n4_scale_path
from quant.i03.params import DEFAULT_CONFIG
from quant.i03.pipeline import _emnd_on_returns, run_structural_analysis
from tests.i03.oracles_perf01 import (
    ref_admissible_pool,
    ref_compute_emnd_all,
    ref_compute_emnd_block,
    ref_locality_for_block,
)


def _float_bits_equal(a: float, b: float) -> bool:
    if math.isnan(a) and math.isnan(b):
        return True
    if math.isinf(a) and math.isinf(b):
        return math.copysign(1.0, a) == math.copysign(1.0, b)
    return a == b


def _emnd_equal(a, b) -> bool:
    if (
        a.period != b.period
        or a.n_queries != b.n_queries
        or a.n_skipped_undefined_x != b.n_skipped_undefined_x
        or a.n_skipped_insufficient_pool != b.n_skipped_insufficient_pool
    ):
        return False
    if set(a.theta_by_k) != set(b.theta_by_k):
        return False
    return all(_float_bits_equal(a.theta_by_k[k], b.theta_by_k[k]) for k in a.theta_by_k)


def _loc_equal(a, b) -> bool:
    return (
        a.period == b.period
        and a.hard_degenerate == b.hard_degenerate
        and a.n_queries_used == b.n_queries_used
        and _float_bits_equal(a.Lambda, b.Lambda)
        and _float_bits_equal(a.Gamma, b.Gamma)
    )


def _synth_returns(n: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    r = np.full(n, np.nan, dtype=np.float64)
    r[1:] = rng.normal(0.0, 0.01, size=n - 1)
    return r


def test_hat_emnd_locality_bitwise_vs_reference() -> None:
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    states = build_states_x(r, cfg)
    defined = ~np.isnan(states[:, 0])
    blocks = build_blocks(len(r), cfg)
    for b in blocks:
        opt = compute_emnd_block(states, defined, b, cfg)
        ref = ref_compute_emnd_block(states, defined, b, cfg)
        assert _emnd_equal(opt, ref)
        lo = locality_for_block(states, defined, b, cfg, seed=20_000 + b.period)
        lr = ref_locality_for_block(states, defined, b, cfg, seed=20_000 + b.period)
        assert _loc_equal(lo, lr)


def test_admissible_pool_tau_boundaries() -> None:
    cfg = DEFAULT_CONFIG
    # Minimal contiguous block
    idx = np.arange(0, 80, dtype=np.intp)
    block = TemporalBlock(period=1, start=0, end=79, indices=idx)
    defined = np.zeros(80, dtype=bool)
    defined[5:] = True
    t = 40
    pool = admissible_pool(t, block, defined, cfg)
    pref = ref_admissible_pool(t, block, defined, cfg)
    assert np.array_equal(pool, pref)
    # tau boundary: |s-t| == tau must be included; == tau-1 excluded
    assert (t - cfg.tau) in set(int(x) for x in pool)
    assert (t - cfg.tau + 1) not in set(int(x) for x in pool) or not defined[t - cfg.tau + 1]
    assert np.all(np.abs(pool.astype(np.int64) - t) >= cfg.tau)


def test_tied_distances_kth_neighbor_stable() -> None:
    cfg = DEFAULT_CONFIG
    # Construct states where several pool members share an identical distance
    T = 400
    states = np.zeros((T, cfg.W_X), dtype=np.float64)
    defined = np.ones(T, dtype=bool)
    defined[0] = False
    # query at 200
    states[200] = 0.0
    for s in range(1, T):
        states[s] = float(s % 7)  # create duplicates
    block = TemporalBlock(
        period=1, start=0, end=T - 1, indices=np.arange(T, dtype=np.intp)
    )
    opt = compute_emnd_block(states, defined, block, cfg)
    ref = ref_compute_emnd_block(states, defined, block, cfg)
    assert _emnd_equal(opt, ref)


def test_insufficient_pool_and_min_block() -> None:
    cfg = DEFAULT_CONFIG
    # Block too small for k_max=50 after tau exclusion
    idx = np.arange(0, 30, dtype=np.intp)
    block = TemporalBlock(period=1, start=0, end=29, indices=idx)
    states = np.ones((30, cfg.W_X), dtype=np.float64)
    defined = np.ones(30, dtype=bool)
    opt = compute_emnd_block(states, defined, block, cfg)
    ref = ref_compute_emnd_block(states, defined, block, cfg)
    assert _emnd_equal(opt, ref)
    assert opt.n_queries == 0


def test_lambda_around_one_locality() -> None:
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    states = build_states_x(r, cfg)
    defined = ~np.isnan(states[:, 0])
    blocks = build_blocks(len(r), cfg)
    for seed in (20_001, 20_002, 20_003):
        lo = locality_for_block(states, defined, blocks[0], cfg, seed=seed)
        lr = ref_locality_for_block(states, defined, blocks[0], cfg, seed=seed)
        assert _loc_equal(lo, lr)


def test_deterministic_repeated_execution() -> None:
    cfg = DEFAULT_CONFIG
    r = _synth_returns(900, seed=99)
    states = build_states_x(r, cfg)
    defined = ~np.isnan(states[:, 0])
    blocks = build_blocks(len(r), cfg)
    a1 = compute_emnd_all(states, defined, blocks, cfg)
    a2 = compute_emnd_all(states, defined, blocks, cfg)
    assert all(_emnd_equal(x, y) for x, y in zip(a1, a2))
    l1 = locality_for_block(states, defined, blocks[1], cfg, seed=20002)
    l2 = locality_for_block(states, defined, blocks[1], cfg, seed=20002)
    assert _loc_equal(l1, l2)


def test_n4_integration_small_battery_equivalence() -> None:
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    scale, sur = generate_n4_battery(r, cfg, B=3)
    blocks = build_blocks(len(r), cfg)
    for b_idx, rs in enumerate(sur, start=1):
        # Surrogate identity vs direct generator
        direct = n4_surrogate_returns(r, scale, b_idx, cfg)
        assert np.array_equal(rs, direct, equal_nan=True)
        st, df, em = _emnd_on_returns(rs, blocks, cfg)
        emr = ref_compute_emnd_all(st, df, blocks, cfg)
        assert all(_emnd_equal(a, b) for a, b in zip(em, emr))
        for blk in blocks:
            lo = locality_for_block(
                st, df, blk, cfg, seed=20_000 + blk.period + 1000 * b_idx
            )
            lr = ref_locality_for_block(
                st, df, blk, cfg, seed=20_000 + blk.period + 1000 * b_idx
            )
            assert _loc_equal(lo, lr)


def test_n3_integration_small_battery_equivalence() -> None:
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    meta, sur = generate_n3_battery(r, cfg, B=3)
    blocks = build_blocks(len(r), cfg)
    for b_idx, rs in enumerate(sur, start=1):
        ia = iaaft(r, seed=10_000 + b_idx, I_max=cfg.iaaft_I_max, eps=cfg.iaaft_eps)
        assert np.array_equal(rs, ia.series, equal_nan=True)
        assert meta.converged_flags[b_idx - 1] == ia.converged
        st, df, em = _emnd_on_returns(rs, blocks, cfg)
        emr = ref_compute_emnd_all(st, df, blocks, cfg)
        assert all(_emnd_equal(a, b) for a, b in zip(em, emr))
        for blk in blocks:
            lo = locality_for_block(st, df, blk, cfg, seed=20_000 + blk.period)
            lr = ref_locality_for_block(st, df, blk, cfg, seed=20_000 + blk.period)
            assert _loc_equal(lo, lr)


def test_pipeline_fused_locality_matches_reference_kernels(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("I03_ALLOW_TEST_OVERRIDES", "1")
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    result = run_structural_analysis(
        r, cfg, B_n4=2, B_n3=2, compute_locality_on_n4=True
    )
    # Recompute observed locality via reference
    states = build_states_x(r, cfg)
    defined = ~np.isnan(states[:, 0])
    for obs, blk in zip(result.locality_obs, result.blocks):
        ref = ref_locality_for_block(
            states, defined, blk, cfg, seed=20_000 + blk.period
        )
        assert _loc_equal(obs, ref)
    assert result.B_n4_used == 2
    assert result.B_n3_used == 2


def test_spylen_emnd_bitwise_sample() -> None:
    """SPY-length synthetic timing fixture — correctness sample, not market."""

    cfg = DEFAULT_CONFIG
    r = _synth_returns(8470, seed=0)
    states = build_states_x(r, cfg)
    defined = ~np.isnan(states[:, 0])
    blocks = build_blocks(len(r), cfg)
    # One block only for runtime in CI
    b = blocks[0]
    assert _emnd_equal(
        compute_emnd_block(states, defined, b, cfg),
        ref_compute_emnd_block(states, defined, b, cfg),
    )
