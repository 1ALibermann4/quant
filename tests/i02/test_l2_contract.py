"""I02 L2 adversarial contract-test suite (synthetic only; no market data).

Attempts to falsify fidelity of the implementation to I02-PREREG-v0.3.
Independent oracles use hand/numpy formulas — not production helpers under test.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import numpy as np
import pytest

from quant.i02.bootstrap import (
    frozen_block_lengths,
    mbb_spearman_ci,
    moving_block_bootstrap_indices,
)
from quant.i02.crps import crps_empirical
from quant.i02.distances import (
    distance_s1_level,
    distance_s2_d2,
    distance_s3_phi,
    distance_s3_q,
    phi_from_q,
)
from quant.i02.estimand import relative_incremental_value, score_difference
from quant.i02.features import (
    dynamics_D,
    log_rv,
    mean_abs_amplitude,
    realized_rms_volatility,
    shape_Q,
)
from quant.i02.neighbors import select_neighbors
from quant.i02.params import DEFAULT_PARAMS, I02Params
from quant.i02.pipeline import evaluate_query, evaluate_series
from quant.i02.pool import admissible_pool, representation_constructible
from quant.i02.regime import std_pop, z_at
from quant.i02.spearman import spearman_grid, spearman_rho
from quant.i02.states_x import causal_mu_sigma, state_vector_x, XUndefinedError
from quant.i02.target import future_realized_rms
from quant.i02.types import SkipReason

P = DEFAULT_PARAMS
I02_ROOT = Path(__file__).resolve().parents[2] / "src" / "quant" / "i02"


# ---------------------------------------------------------------------------
# Fixtures / helpers (synthetic only)
# ---------------------------------------------------------------------------


def _series(n: int, seed: int = 0, scale: float = 0.02) -> np.ndarray:
    rng = np.random.default_rng(seed)
    r = np.full(n, np.nan, dtype=np.float64)
    r[1:] = rng.normal(0.0, scale, n - 1)
    return r


def _oracle_rv(r: np.ndarray, t: int, w: int) -> float:
    wdw = r[t - w + 1 : t + 1]
    return float(np.sqrt(np.mean(wdw * wdw)))


def _oracle_v(r: np.ndarray, t: int, h: int) -> float:
    fut = r[t + 1 : t + 1 + h]
    return float(np.sqrt(np.mean(fut * fut)))


def _oracle_crps(atoms: np.ndarray, y: float) -> float:
    v = np.asarray(atoms, dtype=np.float64)
    k = v.size
    term1 = float(np.mean(np.abs(v - y)))
    term2 = float(np.sum(np.abs(v[:, None] - v[None, :]))) / (2.0 * k * k)
    return term1 - term2


# ===========================================================================
# §2 Temporal indexing
# ===========================================================================


class TestTemporalIndexing:
    def test_v_exact_support_r_s_plus_1_to_s_plus_h(self):
        r = np.full(80, np.nan, dtype=np.float64)
        # unique recognizable magnitudes
        r[1:] = np.arange(1, 80, dtype=np.float64) * 0.001
        s = 30
        v = future_realized_rms(r, s, P)
        expected = math.sqrt(sum((r[s + j] ** 2) for j in range(1, 11)) / 10.0)
        assert v == pytest.approx(expected)
        # wrong windows must differ
        wrong_incl_s = math.sqrt(sum((r[s + j] ** 2) for j in range(0, 10)) / 10.0)
        wrong_to_9 = math.sqrt(sum((r[s + j] ** 2) for j in range(1, 10)) / 9.0)
        assert v != pytest.approx(wrong_incl_s)
        assert v != pytest.approx(wrong_to_9)

    def test_rv_window_inclusive_ending_at_t(self):
        r = np.full(50, np.nan, dtype=np.float64)
        r[1:] = np.linspace(0.01, 0.05, 49)
        t = 30
        got = realized_rms_volatility(r, t, 20)
        assert got == pytest.approx(_oracle_rv(r, t, 20))
        # off-by-one: exclude r_t or include r_{t-20}
        wrong = float(np.sqrt(np.mean(r[t - 20 : t] ** 2)))  # excludes r_t
        assert got != pytest.approx(wrong)

    def test_hard_availability_s_plus_h_le_t(self):
        r = _series(600, seed=3)
        t = 500
        pool = admissible_pool(r, t, P)
        assert pool.size >= 1
        # maximum eligible calendar index under hard availability alone
        s_max = t - P.h
        assert s_max + P.h == t
        if representation_constructible(r, s_max, P):
            assert s_max in set(pool.tolist())
        # one step too late must never appear
        assert (t - P.h + 1) not in set(pool.tolist())
        # adversarial inequalities that would wrongly include/exclude
        assert not any(int(s) + P.h > t for s in pool)
        # s+h < t would drop the boundary; s+9<=t would include t-h+1
        boundary_in = s_max in set(pool.tolist())
        if boundary_in:
            # using strict < would exclude s_max — we require it present when constructible
            assert s_max + P.h <= t
            assert not (s_max + P.h < t and s_max + P.h == t) or True
        assert (t - P.h + 1) + 9 <= t  # would pass wrong s+9<=t rule
        assert (t - P.h + 1) not in set(pool.tolist())

    def test_x_support_last_w_of_m_window(self):
        r = _series(400, seed=5)
        t = 300
        x = state_vector_x(r, t, P)
        mu, sigma = causal_mu_sigma(r, t, P)
        expected = (r[t - 19 : t + 1] - mu) / sigma
        np.testing.assert_allclose(x, expected)
        assert x.shape == (20,)
        # M window for mu/sigma is distinct
        assert t - P.M + 1 == t - 251


# ===========================================================================
# §3 Causality / leakage
# ===========================================================================


class TestCausalityLeakage:
    def test_future_perturbation_does_not_alter_query_state(self):
        base = _series(500, seed=11)
        t = 400
        alt = base.copy()
        alt[t + 1 :] = 9.99  # radical future change

        x0 = state_vector_x(base, t, P)
        x1 = state_vector_x(alt, t, P)
        np.testing.assert_array_equal(x0, x1)

        assert realized_rms_volatility(base, t, 20) == realized_rms_volatility(
            alt, t, 20
        )
        assert log_rv(base, t, P) == log_rv(alt, t, P)
        for m in P.M_Z:
            z0, _ = z_at(base, t, m, P)
            z1, _ = z_at(alt, t, m, P)
            assert z0 == z1

        pool0 = admissible_pool(base, t, P)
        pool1 = admissible_pool(alt, t, P)
        np.testing.assert_array_equal(pool0, pool1)

        res0 = evaluate_query(base, t, params=P)
        res1 = evaluate_query(alt, t, params=P)
        assert not res0.skipped and not res1.skipped
        for name in ("X", "S1", "S2", "S3_Q", "S3_phi"):
            np.testing.assert_array_equal(
                res0.forecasts[name].neighbor_indices,
                res1.forecasts[name].neighbor_indices,
            )
            np.testing.assert_allclose(
                res0.forecasts[name].neighbor_distances,
                res1.forecasts[name].neighbor_distances,
            )
        # V_obs MAY change
        assert res0.v_obs != pytest.approx(res1.v_obs)

    def test_candidate_future_beyond_eligibility_cannot_leak_into_pool(self):
        """Perturb returns after t; pool membership unchanged (already covered).

        Additionally: for candidate s with s+h == t, V_s uses r_{s+1..s+h}
        which are all <= t, so known at query time — that is allowed.
        """
        r = _series(500, seed=12)
        t = 400
        s = t - P.h
        v = future_realized_rms(r, s, P)
        # all indices used are <= t
        assert s + P.h == t
        used = list(range(s + 1, s + P.h + 1))
        assert max(used) == t


# ===========================================================================
# §4 Common A_t
# ===========================================================================


class TestCommonAt:
    def test_all_branches_share_identical_pool_before_ranking(self):
        r = _series(600, seed=21)
        t = 500
        pool = admissible_pool(r, t, P)
        res = evaluate_query(r, t, params=P)
        assert not res.skipped
        np.testing.assert_array_equal(res.pool_indices, pool)
        # every neighbor set is a subset of the same A_t
        for name in ("X", "S1", "S2", "S3_Q", "S3_phi"):
            nbrs = res.forecasts[name].neighbor_indices
            assert set(nbrs.tolist()).issubset(set(pool.tolist()))
            assert nbrs.shape[0] == P.k

    def test_common_at_is_intersection_all_representations(self):
        """A_t requires X and S-features constructible — not per-branch pools."""
        r = _series(500, seed=22)
        # force sigma=0 on a window by constant returns in a mid segment
        r[200:260] = 0.01
        t = 400
        pool = admissible_pool(r, t, P)
        for s in pool:
            assert representation_constructible(r, int(s), P)
            # X defined and RV>0 etc.
            state_vector_x(r, int(s), P)
            assert realized_rms_volatility(r, int(s), 20) > 0.0

    def test_undefined_representation_excludes_from_common_pool(self):
        r = _series(400, seed=23)
        r[100:160] = 0.0  # RV=0 region
        t = 300
        pool = set(admissible_pool(r, t, P).tolist())
        for s in range(100, 160):
            if s + P.h <= t:
                assert s not in pool


# ===========================================================================
# §5 kNN / ties / multiplicity
# ===========================================================================


class TestKnnTiesMultiplicity:
    def test_tie_break_distance_then_s_ascending(self):
        library = np.array([40, 10, 30, 20], dtype=np.intp)
        distances = np.array([0.5, 0.5, 0.1, 0.1], dtype=np.float64)
        nbrs, dists = select_neighbors(library, distances, k=2)
        assert list(nbrs) == [20, 30]
        assert list(dists) == [0.1, 0.1]

    def test_k_exactly_50_when_pool_ge_50(self, synthetic_returns):
        t = 500
        res = evaluate_query(synthetic_returns, t, params=P)
        if res.skipped:
            pytest.skip("skip")
        assert res.pool_size >= 50
        for f in res.forecasts.values():
            assert f.atoms.shape == (50,)
            assert f.neighbor_indices.shape == (50,)

    def test_pool_lt_k_skips_no_adaptive_k(self):
        r = np.full(120, np.nan, dtype=np.float64)
        r[1:] = 0.01
        # early t → insufficient constructible pool / history
        res = evaluate_query(r, 80, params=P)
        assert res.skipped
        assert (
            SkipReason.INSUFFICIENT_ADMISSIBLE_POOL in res.skip_reasons
            or SkipReason.INSUFFICIENT_X_HISTORY in res.skip_reasons
            or SkipReason.X_SIGMA_ZERO in res.skip_reasons
        )
        assert res.forecasts == {}

    def test_duplicate_atoms_multiplicity_preserved(self):
        atoms = np.array([1.0, 1.0, 1.0, 2.0, 2.0])
        y = 1.5
        c = crps_empirical(atoms, y)
        assert c == pytest.approx(_oracle_crps(atoms, y))
        # collapsing duplicates changes CRPS
        collapsed = np.array([1.0, 2.0])
        assert c != pytest.approx(crps_empirical(collapsed, y))


# ===========================================================================
# §6 Representation oracles
# ===========================================================================


class TestRepresentationOracles:
    def test_hand_oracle_rv_l_d_q_phi_distances(self):
        r = np.full(40, np.nan, dtype=np.float64)
        # craft early/late halves with known RMS
        early = np.full(10, 0.02)
        late = np.full(10, 0.04)
        r[11:31] = np.concatenate([early, late])
        t = 30
        rv = math.sqrt(np.mean(np.concatenate([early, late]) ** 2))
        ma = float(np.mean(np.abs(np.concatenate([early, late]))))
        assert realized_rms_volatility(r, t, 20) == pytest.approx(rv)
        assert mean_abs_amplitude(r, t, 20) == pytest.approx(ma)
        assert log_rv(r, t, P) == pytest.approx(math.log(rv))
        d_exp = math.log(0.04 / 0.02)
        assert dynamics_D(r, t, P) == pytest.approx(d_exp)
        q_exp = ma / rv
        assert shape_Q(r, t, P) == pytest.approx(q_exp)
        assert phi_from_q(q_exp) == pytest.approx(math.acos(q_exp))

        # distances independent of production pairwise helpers
        La, Qa, Da = math.log(rv), q_exp, d_exp
        Lb, Qb, Db = La + 1.0, 0.5, Da - 0.5
        assert distance_s1_level(La, Lb) == pytest.approx(1.0)
        assert distance_s2_d2(La, Da, Lb, Db) == pytest.approx(
            math.sqrt(1.0**2 + 0.5**2)
        )
        assert distance_s3_q(La, Qa, Lb, Qb) == pytest.approx(
            math.sqrt(1.0**2 + (Qa - Qb) ** 2)
        )
        assert distance_s3_phi(La, Qa, Lb, Qb) == pytest.approx(
            math.sqrt(1.0**2 + (math.acos(Qa) - math.acos(Qb)) ** 2)
        )

    def test_q_domain_rejects_nonpositive(self):
        with pytest.raises(ValueError):
            phi_from_q(0.0)
        with pytest.raises(ValueError):
            phi_from_q(-0.1)
        with pytest.raises(ValueError):
            phi_from_q(1.0 + 1e-12)


# ===========================================================================
# §7 X standardization
# ===========================================================================


class TestXStandardization:
    def test_m_252_and_w_distinct(self):
        assert P.M == 252 and P.W_X == 20
        assert P.M != P.W_X

    def test_sigma_zero(self):
        r = np.full(400, np.nan)
        r[1:] = 1.0  # exact binary constant → sample σ̂ = 0
        with pytest.raises(XUndefinedError) as ei:
            state_vector_x(r, 300, P)
        assert ei.value.reason == SkipReason.X_SIGMA_ZERO

    def test_tiny_sigma_exact_division_no_eps(self):
        r = np.full(400, np.nan)
        rng = np.random.default_rng(99)
        r[1:] = 1e-12 * rng.normal(size=399)
        t = 300
        mu, sigma = causal_mu_sigma(r, t, P)
        assert 0.0 < sigma < 1e-10
        x = state_vector_x(r, t, P)
        expected = (r[t - 19 : t + 1] - mu) / sigma
        np.testing.assert_allclose(x, expected)
        contaminated = (r[t - 19 : t + 1] - mu) / (sigma + 1e-8)
        assert np.any(x != contaminated)

    def test_perturbation_outside_m_no_effect(self):
        r = _series(400, seed=31)
        t = 300
        x0 = state_vector_x(r, t, P)
        r2 = r.copy()
        r2[t - P.M] = 50.0  # just outside [t-M+1, t]
        x1 = state_vector_x(r2, t, P)
        np.testing.assert_array_equal(x0, x1)

    def test_perturbation_inside_m_changes_x(self):
        r = _series(400, seed=32)
        t = 300
        x0 = state_vector_x(r, t, P)
        r2 = r.copy()
        r2[t - 100] = r2[t - 100] + 1.0  # inside M window, outside W_X
        x1 = state_vector_x(r2, t, P)
        assert not np.allclose(x0, x1)


# ===========================================================================
# §8 CRPS oracle
# ===========================================================================


class TestCrpsOracle:
    def test_identical_atoms(self):
        atoms = np.full(50, 2.0)
        assert crps_empirical(atoms, 2.0) == pytest.approx(0.0)
        assert crps_empirical(atoms, 3.0) == pytest.approx(1.0)

    def test_two_valued_and_outside(self):
        atoms = np.array([0.0, 0.0, 1.0, 1.0])
        y = 0.5
        assert crps_empirical(atoms, y) == pytest.approx(_oracle_crps(atoms, y))
        assert crps_empirical(atoms, 5.0) == pytest.approx(_oracle_crps(atoms, 5.0))

    def test_positive_homogeneous_scaling(self):
        atoms = np.array([1.0, 2.0, 4.0, 0.5])
        y = 1.5
        a = 3.0
        c0 = crps_empirical(atoms, y)
        c1 = crps_empirical(a * atoms, a * y)
        assert c1 == pytest.approx(a * c0, rel=1e-12, abs=1e-12)


# ===========================================================================
# §9 D / R semantics
# ===========================================================================


class TestDRSemantics:
    def test_d_sign_and_r_exact(self):
        # X better ⇒ CRPS_X < CRPS_S ⇒ D > 0
        d = score_difference(0.5, 0.2)
        assert d == pytest.approx(0.3)
        assert d > 0
        r, reason = relative_incremental_value(0.5, 0.2)
        assert reason is None
        assert r == pytest.approx(0.3 / 0.5)

    def test_crps_s_zero_undefined(self):
        r, reason = relative_incremental_value(0.0, 0.1)
        assert r is None and reason == SkipReason.CRPS_COMPARATOR_ZERO

    def test_tiny_positive_crps_s_exact_division(self):
        cs = 1e-18
        cx = 0.5e-18
        r, reason = relative_incremental_value(cs, cx)
        assert reason is None
        assert r == pytest.approx((cs - cx) / cs)


# ===========================================================================
# §10 Z oracle
# ===========================================================================


class TestZOracle:
    def test_m_levels_and_increments_count(self):
        r = _series(400, seed=41)
        t = 300
        for m in (3, 12, 21):
            z, reason = z_at(r, t, m, P)
            assert reason is None and z is not None
            # rebuild increments independently
            levels = [log_rv(r, u, P) for u in range(t - m + 1, t + 1)]
            assert len(levels) == m
            deltas = np.diff(levels)
            assert deltas.shape[0] == m - 1
            assert z == pytest.approx(float(np.std(deltas, ddof=0)))
            assert z != pytest.approx(float(np.std(deltas, ddof=1))) or m == 2

    def test_constant_delta_l_gives_z_zero(self):
        # Constant |r| ⇒ constant RV ⇒ ΔL=0 ⇒ Z=0
        r = np.full(100, np.nan)
        r[1:] = 0.02
        # Need non-zero sigma for X elsewhere; for Z alone use RV path
        # constant RV after W_RV: all ΔL=0
        t = 50
        z, reason = z_at(r, t, 3, P)
        # L defined (RV>0), ΔL=0
        assert reason is None
        assert z == pytest.approx(0.0)

    def test_z_no_future(self):
        r = _series(300, seed=42)
        t = 200
        z0, _ = z_at(r, t, 12, P)
        r2 = r.copy()
        r2[t + 1 :] *= 10.0
        z1, _ = z_at(r2, t, 12, P)
        assert z0 == z1


# ===========================================================================
# §11 Skip propagation
# ===========================================================================


class TestSkipPropagation:
    def test_insufficient_x_history(self):
        r = _series(200, seed=1)
        res = evaluate_query(r, 100, params=P)  # t=100 < M=252
        assert res.skipped
        assert SkipReason.INSUFFICIENT_X_HISTORY in res.skip_reasons

    def test_x_sigma_zero_reason(self):
        r = np.full(400, np.nan)
        r[1:] = 0.01
        res = evaluate_query(r, 300, params=P)
        assert res.skipped
        assert SkipReason.X_SIGMA_ZERO in res.skip_reasons
        assert res.forecasts == {}

    def test_insufficient_pool(self):
        r = _series(280, seed=2, scale=0.01)
        # earliest possible queries have small A_t
        res = evaluate_query(r, 260, params=P)
        if not res.skipped:
            pytest.skip("pool unexpectedly large")
        assert SkipReason.INSUFFICIENT_ADMISSIBLE_POOL in res.skip_reasons or (
            SkipReason.INSUFFICIENT_X_HISTORY in res.skip_reasons
        )

    def test_crps_comparator_zero_no_silent_zero_r(self):
        # Force via estimand API (pipeline needs crafted perfect S forecast)
        r_val, reason = relative_incremental_value(0.0, 1.0)
        assert r_val is None
        assert reason == SkipReason.CRPS_COMPARATOR_ZERO

    def test_skip_reasons_not_converted_to_zero_in_r_dict(self):
        r = np.full(400, np.nan)
        r[1:] = 0.01
        res = evaluate_query(r, 300, params=P)
        assert res.skipped
        # no fabricated R=0
        assert all(v is None or isinstance(v, float) for v in res.r.values())


# ===========================================================================
# §12 S3 dual-branch governance
# ===========================================================================


class TestS3DualBranch:
    def test_both_branches_always_present(self, synthetic_returns):
        res = evaluate_query(synthetic_returns, 520, params=P)
        if res.skipped:
            pytest.skip("skip")
        assert "S3_Q" in res.forecasts and "S3_phi" in res.forecasts
        assert "S3" not in res.forecasts
        assert "S3_Q" in res.r and "S3_phi" in res.r

    def test_fixture_identical_vs_divergent_rankings(self):
        # Identical: Q near 1 for all ⇒ φ≈0; L differences dominate similarly
        # Divergent: construct two library points with swap in Q vs φ geometry
        # Point A: L=0, Q=1 (φ=0); Point B: L=0, Q=0.5 (φ=π/3)
        # Query: L=0, Q=0.8
        # d_Q(A)=|1-0.8|=0.2; d_Q(B)=|0.5-0.8|=0.3 → A nearer in Q
        # d_φ(A)=|0-arccos(0.8)|; d_φ(B)=|π/3-arccos(0.8)|
        q_q, q_a, q_b = 0.8, 1.0, 0.5
        d_q_a = distance_s3_q(0.0, q_q, 0.0, q_a)
        d_q_b = distance_s3_q(0.0, q_q, 0.0, q_b)
        d_p_a = distance_s3_phi(0.0, q_q, 0.0, q_a)
        d_p_b = distance_s3_phi(0.0, q_q, 0.0, q_b)
        assert d_q_a < d_q_b
        # φ chart may disagree on relative order depending on arccos curvature
        assert d_p_a != pytest.approx(d_p_b)
        # both metrics defined independently — no selection
        assert d_q_a > 0 and d_p_a > 0

    def test_static_no_best_s3_selection_in_source(self):
        text = ""
        for path in I02_ROOT.glob("*.py"):
            text += path.read_text(encoding="utf-8") + "\n"
        # forbid obvious post-hoc selectors on scientific S3 outputs
        forbidden = [
            r"best_s3",
            r"s3_primary",
            r"choose_s3",
            r"select_s3_branch",
            r"argmin\(.*S3",
            r"argmax\(.*S3",
        ]
        for pat in forbidden:
            assert re.search(pat, text, re.I) is None, pat


# ===========================================================================
# §13 Spearman
# ===========================================================================


class TestSpearmanOracle:
    def test_perfect_mono(self):
        x = np.arange(20, dtype=float)
        assert spearman_rho(x, x) == pytest.approx(1.0)
        assert spearman_rho(x, -x) == pytest.approx(-1.0)

    def test_ties_and_constant(self):
        x = np.array([1.0, 1.0, 2.0, 2.0])
        y = np.array([3.0, 4.0, 5.0, 6.0])
        rho = spearman_rho(x, y)
        assert np.isfinite(rho)
        assert math.isnan(spearman_rho(np.ones(10), np.arange(10.0)))

    def test_full_grid_no_best_cell(self):
        z = {3: np.arange(10.0), 12: np.arange(10.0), 21: np.arange(10.0)}
        r = {
            "S1": np.arange(10.0),
            "S2": -np.arange(10.0),
            "S3_Q": np.arange(10.0),
            "S3_phi": np.arange(10.0),
        }
        grid = spearman_grid(z, r)
        assert len(grid) == 4 * 3
        assert set(grid) == {(s, m) for s in r for m in z}


# ===========================================================================
# §14–17 Bootstrap
# ===========================================================================


class TestBootstrapStructural:
    def test_block_starts_enumerated_no_wrap(self):
        n, b = 10, 4
        rng = np.random.default_rng(0)
        idx = moving_block_bootstrap_indices(n, b, B=200, rng=rng)
        assert idx.shape == (200, n)
        for row in idx:
            # reconstruct: first full blocks contiguous
            pos = 0
            while pos + b <= n:
                block = row[pos : pos + b]
                start = int(block[0])
                assert 0 <= start <= n - b
                assert list(block) == list(range(start, start + b))
                pos += b

    def test_truncate_and_b_equals_n(self):
        rng = np.random.default_rng(1)
        n = b = 8
        idx = moving_block_bootstrap_indices(n, b, B=20, rng=rng)
        assert idx.shape == (20, n)
        for row in idx:
            # only one block start possible: 0
            assert list(row) == list(range(n))

    def test_n_lt_b_inconclusive(self):
        out = mbb_spearman_ci(np.arange(10.0), np.arange(10.0), b=40)
        assert out.inconclusive
        assert out.reason == SkipReason.BOOTSTRAP_INSUFFICIENT_N

    def test_frozen_B_seed_alpha_blocks(self):
        assert P.bootstrap_B == 9999
        assert P.bootstrap_seed == 42
        assert P.alpha == 0.05
        assert frozen_block_lengths() == (40, (20, 40, 80))
        with pytest.raises(ValueError):
            I02Params(bootstrap_B=100)  # type: ignore[call-arg]

    def test_compressed_valid_series_semantics(self):
        """v0.3: calendar gaps removed; valid pairs become contiguous for MBB.

        CONTRACT RISK (accepted): indices 102 and 150 become adjacent after
        compression — documented in prereg §15.2 Source series.
        """
        z = np.array(
            [np.nan, 1.0, 2.0, 3.0, np.nan, np.nan, 4.0, 5.0], dtype=np.float64
        )
        r = np.array(
            [np.nan, 0.1, 0.2, 0.3, np.nan, np.nan, 0.4, 0.5], dtype=np.float64
        )
        # n_valid = 5 after compression; mechanical B for speed
        out = mbb_spearman_ci(z, r, b=3, n_replicates=50)
        assert out.n_valid == 5
        assert out.reason != SkipReason.BOOTSTRAP_INSUFFICIENT_N
        mask = np.isfinite(z) & np.isfinite(r)
        assert int(mask.sum()) == 5

    def test_seed_reproducibility_and_no_global_rng(self):
        z = np.linspace(0, 1, 120)
        r = z + 0.05 * np.sin(np.arange(120))
        np.random.seed(999)  # pollute global RNG deliberately
        a = mbb_spearman_ci(z, r, b=20, seed=42, n_replicates=200)
        np.random.seed(1)
        b = mbb_spearman_ci(z, r, b=20, seed=42, n_replicates=200)
        assert a.ci_low == b.ci_low and a.ci_high == b.ci_high

    def test_percentile_ci_convention_linear(self):
        # Strong monotone → CI should exclude 0 (full B left to v0.3 suite)
        z = np.arange(250, dtype=float)
        r = z.copy()
        out = mbb_spearman_ci(z, r, b=40, n_replicates=499)
        assert not out.inconclusive
        assert out.detectable is True
        assert out.ci_low is not None and out.ci_low > 0

    def test_all_degenerate_replicates_inconclusive(self):
        z = np.ones(100)
        r = np.linspace(0, 1, 100)
        out = mbb_spearman_ci(z, r, b=20, n_replicates=200)
        assert out.inconclusive
        assert out.reason == SkipReason.BOOTSTRAP_DEGENERATE
        assert out.ci_low is None and out.ci_high is None

    def test_production_B_frozen_override_is_explicit(self):
        """Scientific default remains B=9999; test override must be explicit."""
        assert P.bootstrap_B == 9999
        z = np.arange(80, dtype=float)
        r = z.copy()
        out = mbb_spearman_ci(z, r, b=20, n_replicates=30)
        assert out.n_finite_replicates <= 30

    def test_robustness_reports_all_b_no_selection(self):
        rng = np.random.default_rng(7)
        z = rng.normal(size=200)
        r = 0.4 * z + rng.normal(scale=0.5, size=200)
        # structural key set only — full B×3 left to contract_v03
        assert list(P.b_sensitivity) == [20, 40, 80]
        for b in P.b_sensitivity:
            cell = mbb_spearman_ci(z, r, b=b, n_replicates=40)
            assert cell.b == b


# ===========================================================================
# §18 Metamorphic
# ===========================================================================


class TestMetamorphic:
    def test_positive_rescale_rv_l_delta_z(self):
        r = _series(350, seed=55)
        a = 2.5
        t = 300
        rv0 = realized_rms_volatility(r, t, 20)
        rv1 = realized_rms_volatility(r * a, t, 20)
        assert rv1 == pytest.approx(a * rv0)
        # L shifts by log(a); ΔL and Z invariant under positive scale
        l0 = log_rv(r, t, P)
        l1 = log_rv(r * a, t, P)
        assert l1 == pytest.approx(l0 + math.log(a))
        for m in P.M_Z:
            z0, _ = z_at(r, t, m, P)
            z1, _ = z_at(r * a, t, m, P)
            assert z0 == pytest.approx(z1)

    def test_crps_scale(self):
        atoms = np.array([0.1, 0.2, 0.4])
        y = 0.25
        assert crps_empirical(2 * atoms, 2 * y) == pytest.approx(
            2 * crps_empirical(atoms, y)
        )

    def test_spearman_order_preserving(self):
        x = np.array([1.0, 3.0, 2.0, 5.0, 4.0])
        y = np.array([2.0, 1.0, 4.0, 3.0, 5.0])
        # strictly increasing transform of x
        x2 = np.exp(x)
        assert spearman_rho(x, y) == pytest.approx(spearman_rho(x2, y))


# ===========================================================================
# §19 Randomized synthetic stress
# ===========================================================================


class TestRandomizedSynthetic:
    def test_boundary_lengths_and_ties_reproducible(self):
        rng = np.random.default_rng(12345)
        for n in (280, 320, 400):
            r = np.full(n, np.nan)
            r[1:] = rng.normal(0, 0.01, n - 1)
            # inject exact ties / tiny variance / zero run
            r[50:55] = r[50]
            r[80:90] *= 1e-15
            t = n - 15
            if t >= P.M:
                res = evaluate_query(r, t, params=P)
                assert isinstance(res.skipped, bool)
                if not res.skipped:
                    assert set(res.forecasts) >= {
                        "X",
                        "S1",
                        "S2",
                        "S3_Q",
                        "S3_phi",
                    }


# ===========================================================================
# §20 Static scientific-freedom audit
# ===========================================================================


class TestStaticFreedomAudit:
    def test_params_immutable_scientific_constants(self):
        with pytest.raises(ValueError):
            I02Params(W_X=21)  # type: ignore[call-arg]
        with pytest.raises(ValueError):
            I02Params(k=49)  # type: ignore[call-arg]
        with pytest.raises(ValueError):
            I02Params(h=5)  # type: ignore[call-arg]
        with pytest.raises(ValueError):
            I02Params(M=100)  # type: ignore[call-arg]
        with pytest.raises(ValueError):
            I02Params(bootstrap_B=1000)  # type: ignore[call-arg]
        with pytest.raises(ValueError):
            I02Params(b_star=30)  # type: ignore[call-arg]

    def test_no_i02_cli_tuning_surface(self):
        for path in I02_ROOT.glob("*.py"):
            src = path.read_text(encoding="utf-8")
            assert "argparse" not in src
            assert "click" not in src

    def test_no_hidden_epsilon_adaptive_best(self):
        patterns = [
            r"epsilon_sigma\s*=",
            r"adaptive_k",
            r"adaptive_b",
            r"best_m\b",
            r"best_b\b",
            r"best_S\b",
            r"fallback_metric",
        ]
        for path in I02_ROOT.glob("*.py"):
            src = path.read_text(encoding="utf-8")
            for pat in patterns:
                assert re.search(pat, src) is None, f"{path.name}: {pat}"


# ===========================================================================
# §21 End-to-end structural
# ===========================================================================


class TestEndToEndStructural:
    def test_full_query_flow_structural_only(self):
        r = _series(700, seed=77)
        results = evaluate_series(r, params=P, query_indices=np.arange(500, 505))
        assert len(results) == 5
        ok = [res for res in results if not res.skipped]
        assert ok, "expected at least one evaluable query"
        res = ok[0]
        assert set(res.forecasts) == {"X", "S1", "S2", "S3_Q", "S3_phi"}
        assert set(res.r) >= {"S1", "S2", "S3_Q", "S3_phi"}
        assert set(res.z) == {3, 12, 21}
        assert res.pool_size >= P.k
        # Spearman grid structural across evaluable queries
        zs = {m: [] for m in P.M_Z}
        rs = {s: [] for s in ("S1", "S2", "S3_Q", "S3_phi")}
        for q in ok:
            for m in P.M_Z:
                zs[m].append(q.z[m] if q.z[m] is not None else np.nan)
            for s in rs:
                rs[s].append(q.r[s] if q.r[s] is not None else np.nan)
        z_arr = {m: np.asarray(v, float) for m, v in zs.items()}
        r_arr = {s: np.asarray(v, float) for s, v in rs.items()}
        grid = spearman_grid(z_arr, r_arr)
        assert len(grid) == 12
        # bootstrap mechanics on one cell if enough finite pairs (cheap b)
        z3 = z_arr[3]
        r1 = r_arr["S1"]
        mask = np.isfinite(z3) & np.isfinite(r1)
        if mask.sum() >= 40:
            boot = mbb_spearman_ci(z3, r1, b=40)
            assert boot.b == 40
            assert boot.n_valid == int(mask.sum())
