"""Unit tests for I02 L1 mathematical primitives (synthetic only)."""

from __future__ import annotations

import numpy as np
import pytest

from quant.i02.bootstrap import frozen_block_lengths, moving_block_bootstrap
from quant.i02.contract_gaps import ImplementationContractGap
from quant.i02.crps import crps_empirical
from quant.i02.distances import distance_s2_d2, distance_s3_blocked
from quant.i02.estimand import relative_incremental_value, score_difference
from quant.i02.features import (
    dynamics_D,
    mean_abs_amplitude,
    realized_rms_volatility,
    shape_Q,
)
from quant.i02.neighbors import select_neighbors
from quant.i02.params import DEFAULT_PARAMS
from quant.i02.pool import admissible_pool
from quant.i02.regime import std_pop, z_at
from quant.i02.spearman import spearman_grid, spearman_rho
from quant.i02.target import future_realized_rms
from quant.i02.types import SkipReason


def test_params_frozen_values():
    p = DEFAULT_PARAMS
    assert p.W_X == 20 and p.W_RV == 20
    assert p.h == 10 and p.k == 50 and p.stride == 1
    assert p.M_Z == (3, 12, 21)
    assert p.b_star == 40 and p.b_sensitivity == (20, 40, 80)


def test_rv_rms_not_sample_std(synthetic_returns):
    t = 300
    w = 20
    rv = realized_rms_volatility(synthetic_returns, t, w)
    window = synthetic_returns[t - w + 1 : t + 1]
    expected = float(np.sqrt(np.mean(window * window)))
    assert rv == pytest.approx(expected)
    # Distinct from ddof=1 std
    assert rv != pytest.approx(float(np.std(window, ddof=1)))


def test_target_v_indexing(synthetic_returns):
    p = DEFAULT_PARAMS
    t = 300
    v = future_realized_rms(synthetic_returns, t, p)
    fut = synthetic_returns[t + 1 : t + 1 + p.h]
    assert v == pytest.approx(float(np.sqrt(np.mean(fut * fut))))


def test_hard_availability_in_pool(synthetic_returns):
    p = DEFAULT_PARAMS
    t = 500
    pool = admissible_pool(synthetic_returns, t, p)
    assert pool.size >= p.k
    assert np.all(pool < t)
    assert np.all(pool + p.h <= t)


def test_tie_break_distance_then_s():
    library = np.array([10, 5, 8, 3], dtype=np.intp)
    distances = np.array([1.0, 1.0, 0.5, 0.5], dtype=np.float64)
    nbrs, dists = select_neighbors(library, distances, k=2)
    # distances 0.5 at s=3 and s=8 → older s=3 first
    assert list(nbrs) == [3, 8]
    assert list(dists) == [0.5, 0.5]


def test_duplicate_atoms_preserved_in_crps():
    atoms = np.array([1.0, 1.0, 2.0])
    y = 1.0
    # Explicit multiplicity: two atoms at 1.0
    c = crps_empirical(atoms, y)
    atoms_dedup_wrong = np.array([1.0, 2.0])
    c_wrong = crps_empirical(atoms_dedup_wrong, y)
    assert c != pytest.approx(c_wrong)


def test_crps_identity_single_atom():
    assert crps_empirical(np.array([3.0]), 3.0) == pytest.approx(0.0)
    assert crps_empirical(np.array([3.0]), 4.0) == pytest.approx(1.0)


def test_r_zero_denominator():
    r, reason = relative_incremental_value(0.0, 0.1)
    assert r is None
    assert reason == SkipReason.CRPS_COMPARATOR_ZERO
    r2, reason2 = relative_incremental_value(0.5, 0.1)
    assert reason2 is None
    assert r2 == pytest.approx(score_difference(0.5, 0.1) / 0.5)


def test_rv_zero_q_undefined():
    r = np.full(40, np.nan, dtype=np.float64)
    r[1:] = 0.0
    with pytest.raises(ValueError, match="RV_t is zero"):
        shape_Q(r, 30, DEFAULT_PARAMS)


def test_z_indexing_m_levels(synthetic_returns):
    p = DEFAULT_PARAMS
    t = 400
    m = 3
    z, reason = z_at(synthetic_returns, t, m, p)
    assert reason is None
    assert z is not None
    # m-1 increments: std_pop of length 2
    assert isinstance(z, float)


def test_std_pop_ddof0():
    x = np.array([1.0, 2.0, 3.0])
    assert std_pop(x) == pytest.approx(float(np.std(x, ddof=0)))
    assert std_pop(x) != pytest.approx(float(np.std(x, ddof=1)))


def test_s2_d2_metric():
    assert distance_s2_d2(0.0, 0.0, 3.0, 4.0) == pytest.approx(5.0)


def test_s3_distance_is_contract_gap():
    with pytest.raises(ImplementationContractGap):
        distance_s3_blocked()


def test_bootstrap_is_contract_gap():
    b_star, sens = frozen_block_lengths()
    assert b_star == 40 and sens == (20, 40, 80)
    with pytest.raises(ImplementationContractGap):
        moving_block_bootstrap()


def test_spearman_monotone():
    x = np.arange(10, dtype=np.float64)
    y = 2 * x + 1
    assert spearman_rho(x, y) == pytest.approx(1.0)
    grid = spearman_grid({3: x, 12: x}, {"S1": y, "S2": -y})
    assert grid[("S1", 3)] == pytest.approx(1.0)
    assert grid[("S2", 12)] == pytest.approx(-1.0)


def test_dynamics_d_scale_invariant():
    rng = np.random.default_rng(1)
    r = np.full(50, np.nan)
    r[1:] = rng.normal(0, 0.02, 49)
    d1 = dynamics_D(r, 40, DEFAULT_PARAMS)
    d2 = dynamics_D(r * 3.0, 40, DEFAULT_PARAMS)
    assert d1 == pytest.approx(d2)


def test_ma_le_rv(synthetic_returns):
    t = 300
    ma = mean_abs_amplitude(synthetic_returns, t, 20)
    rv = realized_rms_volatility(synthetic_returns, t, 20)
    assert ma <= rv + 1e-12
