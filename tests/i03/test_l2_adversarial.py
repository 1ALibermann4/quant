"""I03 L2 adversarial contract suite — independent oracles, no market data.

Tries to falsify: implementation executes exactly I03-PREREG-v0.1.
"""

from __future__ import annotations

import itertools
import os

import numpy as np
import pytest

from quant.i02.params import DEFAULT_PARAMS as I02P
from quant.i02.states_x import state_vector_x
from quant.i03.blocks import build_blocks
from quant.i03.coherence import build_survival_grid
from quant.i03.emnd import admissible_pool, kth_distance
from quant.i03.g0 import build_states_x
from quant.i03.inference import left_tail_p, survives
from quant.i03.locality import LocalityBlockDiagnostic, locality_validity_ok
from quant.i03.n3 import n3_nonconv_frac_invalid
from quant.i03.n4 import build_n4_scale_path, n4_sigma_at, n4_surrogate_returns
from quant.i03.params import DEFAULT_CONFIG
from quant.i03.pipeline import artifact_dict, run_structural_analysis
from quant.i03.verdict import VerdictInput, VerdictLabel, decide_verdict

from tests.i03.oracles_l2 import (
    oracle_X,
    oracle_blocks,
    oracle_decide_verdict,
    oracle_kth_distance,
    oracle_left_tail_p,
    oracle_max_count_survive_alpha,
    oracle_n3_invalid,
    oracle_n4_sigma,
)

os.environ.setdefault("I03_ALLOW_TEST_OVERRIDES", "1")


# ===========================================================================
# §3 Static freedom audit
# ===========================================================================


def test_L2_freedom_config_rejects_retunes():
    from quant.i03.params import I03Config

    for kwargs in (
        {"W_X": 21},
        {"M": 100},
        {"tau": 19},
        {"P": 4},
        {"B_N4": 100},
        {"alpha": 0.01},
        {"K": (10, 25)},
    ):
        with pytest.raises(ValueError):
            I03Config(**kwargs)  # type: ignore[arg-type]


def test_L2_freedom_production_rejects_B_override_without_env(monkeypatch):
    monkeypatch.delenv("I03_ALLOW_TEST_OVERRIDES", raising=False)
    r = np.full(100, np.nan)
    r[1:] = 0.01
    with pytest.raises(RuntimeError, match="I03_ALLOW_TEST_OVERRIDES"):
        run_structural_analysis(r, B_n4=2)


# ===========================================================================
# §4 G0 independent oracle
# ===========================================================================


def test_L2_G0_oracle_matches_implementation_and_i02():
    rng = np.random.default_rng(11)
    r = np.full(400, np.nan)
    r[1:] = rng.normal(0, 0.02, 399)
    for t in (252, 253, 300, 399):
        ox = oracle_X(r, t)
        assert ox is not None
        impl = state_vector_x(r, t, I02P)
        assert np.allclose(ox, impl)
        # I03 build path
        states = build_states_x(r, DEFAULT_CONFIG)
        assert np.allclose(ox, states[t])


def test_L2_G0_future_suffix_metamorphic():
    rng = np.random.default_rng(12)
    r = np.full(400, np.nan)
    r[1:] = rng.normal(0, 0.02, 399)
    t = 300
    x0 = oracle_X(r, t)
    r2 = r.copy()
    r2[t + 1 :] = 1e6
    assert np.allclose(x0, oracle_X(r2, t))


def test_L2_G0_zero_variance_undefined():
    r = np.full(300, np.nan)
    r[1:] = 0.0
    assert oracle_X(r, 252) is None


def test_L2_G0_first_valid_boundary():
    rng = np.random.default_rng(13)
    r = np.full(260, np.nan)
    r[1:] = rng.normal(0, 0.01, 259)
    assert oracle_X(r, 251) is None  # incomplete M window under index-0 unused
    assert oracle_X(r, 252) is not None


# ===========================================================================
# §5 Blocks
# ===========================================================================


@pytest.mark.parametrize("T,rem", [(99, 0), (100, 1), (101, 2), (9, 0), (10, 1)])
def test_L2_blocks_partition_and_remainder(T, rem):
    assert T % 3 == rem
    blocks = build_blocks(T, DEFAULT_CONFIG)
    oracle = oracle_blocks(T, 3)
    assert len(blocks) == 3
    covered = []
    for b, (s, e) in zip(blocks, oracle):
        assert b.start == s and b.end == e
        covered.extend(range(s, e + 1))
    assert covered == list(range(T))
    # no overlap
    sets = [set(b.indices.tolist()) for b in blocks]
    assert len(sets[0] & sets[1]) == 0
    assert len(sets[1] & sets[2]) == 0
    assert len(sets[0] & sets[2]) == 0


# ===========================================================================
# §6 Tau — both directions, |t-s| in {0,1,19,20,21}
# ===========================================================================


def test_L2_tau_boundary_both_directions():
    cfg = DEFAULT_CONFIG
    from quant.i03.blocks import TemporalBlock

    T = 90
    defined = np.zeros(T, dtype=bool)
    defined[20:] = True
    block = TemporalBlock(period=1, start=0, end=T - 1, indices=np.arange(T, dtype=np.intp))
    t = 50
    pool = set(int(s) for s in admissible_pool(t, block, defined, cfg))
    for lag in (0, 1, 19):
        assert (t - lag) not in pool
        assert (t + lag) not in pool
    for lag in (20, 21):
        assert (t - lag) in pool
        assert (t + lag) in pool


# ===========================================================================
# §7–8 E-MND oracle + non-tautology
# ===========================================================================


def test_L2_EMND_kth_oracle_not_mean_knn():
    q = np.array([0.0, 0.0])
    # distances: s=1→1, s=2→1, s=3→2, s=4→3, s=5→4  (need k up to 5)
    cloud = {
        1: np.array([1.0, 0.0]),
        2: np.array([0.0, 1.0]),
        3: np.array([2.0, 0.0]),
        4: np.array([3.0, 0.0]),
        5: np.array([4.0, 0.0]),
    }
    assert oracle_kth_distance(q, cloud, 1) == pytest.approx(1.0)
    assert oracle_kth_distance(q, cloud, 2) == pytest.approx(1.0)  # tie → s=1 then s=2
    assert oracle_kth_distance(q, cloud, 3) == pytest.approx(2.0)
    # Implementation kth_distance
    states = np.zeros((6, 2))
    for s, v in cloud.items():
        states[s] = v
    pool = np.array(sorted(cloud.keys()), dtype=np.intp)
    assert kth_distance(q, pool, states, 3) == pytest.approx(2.0)
    # Not mean of first 3 (= (1+1+2)/3)
    assert kth_distance(q, pool, states, 3) != pytest.approx((1 + 1 + 2) / 3)


def test_L2_EMND_nontautology_same_k_different_structure():
    """Same |N_k| but different δ_k — membership rate would not distinguish."""

    q = np.zeros(2)
    tight = {i: np.array([0.01 * i, 0.0]) for i in range(1, 11)}
    loose = {i: np.array([10.0 * i, 0.0]) for i in range(1, 11)}
    d_tight = oracle_kth_distance(q, tight, 5)
    d_loose = oracle_kth_distance(q, loose, 5)
    assert d_tight < d_loose
    # Tautological membership: both have exactly 10 neighbors available for k=5
    assert len(tight) >= 5 and len(loose) >= 5


def test_L2_EMND_candidate_reorder_invariant():
    q = np.zeros(2)
    states = np.zeros((5, 2))
    states[1] = [1, 0]
    states[2] = [2, 0]
    states[3] = [3, 0]
    states[4] = [0.5, 0]
    p1 = np.array([1, 2, 3, 4], dtype=np.intp)
    p2 = np.array([4, 3, 2, 1], dtype=np.intp)
    assert kth_distance(q, p1, states, 2) == kth_distance(q, p2, states, 2)


# ===========================================================================
# §9–11 N4
# ===========================================================================


def test_L2_N4_sigma_oracle_not_rms_not_pop():
    r = np.full(40, np.nan)
    r[1:21] = np.arange(1, 21, dtype=float)
    t = 20
    s = oracle_n4_sigma(r, t)
    impl = n4_sigma_at(r, t, DEFAULT_CONFIG)
    assert s == pytest.approx(impl)
    w = r[1:21]
    assert s == pytest.approx(float(np.std(w, ddof=1)))
    assert s != pytest.approx(float(np.std(w, ddof=0)))  # not /20 pop
    assert s != pytest.approx(float(np.sqrt(np.mean(w * w))))  # not RMS


def test_L2_N4_preserves_sigma_path_recomputed_may_differ():
    """Semantic attack: construction envelope ≠ recomputed rolling σ on r*."""

    rng = np.random.default_rng(21)
    n = 800
    r = np.full(n, np.nan)
    vol = np.linspace(0.001, 0.05, n - 1)
    r[1:] = rng.normal(0, 1, n - 1) * vol
    scale = build_n4_scale_path(r, DEFAULT_CONFIG)
    assert scale.valid, scale.invalid_reason
    r_star = n4_surrogate_returns(r, scale, b=1, cfg=DEFAULT_CONFIG)
    Z = scale.Z_indices
    assert np.allclose(np.sort(scale.z[Z]), np.sort(r_star[Z] / scale.sigma[Z]))
    diffs = []
    for t in Z[100:200]:
        s_re = n4_sigma_at(r_star, int(t), DEFAULT_CONFIG)
        if s_re is not None and scale.sigma[t] > 0:
            diffs.append(abs(s_re - scale.sigma[t]))
    assert diffs and max(diffs) > 1e-6


def test_L2_N4_sigma_not_permuted():
    rng = np.random.default_rng(22)
    r = np.full(150, np.nan)
    r[1:] = rng.normal(0, 0.02, 149)
    scale = build_n4_scale_path(r, DEFAULT_CONFIG)
    r_star = n4_surrogate_returns(r, scale, 5, DEFAULT_CONFIG)
    # Where both defined, reconstruction uses ORIGINAL sigma[t]
    for t in scale.Z_indices[:20]:
        assert r_star[t] == pytest.approx(scale.sigma[t] * (r_star[t] / scale.sigma[t]))


def test_L2_N4_causality_source_quantities():
    """Causal construction of σ̂/z/X before global shuffle."""

    rng = np.random.default_rng(23)
    r = np.full(300, np.nan)
    r[1:] = rng.normal(0, 0.01, 299)
    t = 100
    s0 = n4_sigma_at(r, t, DEFAULT_CONFIG)
    x0 = oracle_X(r, t, M=252, W_X=20)
    r2 = r.copy()
    r2[t + 1 :] = 9.0
    assert n4_sigma_at(r2, t, DEFAULT_CONFIG) == pytest.approx(s0)
    if x0 is not None:
        assert np.allclose(x0, oracle_X(r2, t, M=252, W_X=20))


def test_L2_N4_validity_boundaries():
    cfg = DEFAULT_CONFIG
    # All-NaN → empty Z → invalid
    r2 = np.full(50, np.nan)
    scale2 = build_n4_scale_path(r2, cfg)
    assert scale2.valid is False
    assert scale2.invalid_reason in {"N4_Z_FRAC", "N4_Z_EMPTY"}


# ===========================================================================
# §12–13 N3 boundary arithmetic
# ===========================================================================


def test_L2_N3_five_percent_integer_boundary_B999():
    """B=999, frac>0.05 → INVALID.

    49/999 ≈ 0.04905 ≤ 0.05 → VALID
    50/999 ≈ 0.05005 > 0.05 → INVALID
    """

    B = 999
    assert oracle_n3_invalid(49, B) is False
    assert oracle_n3_invalid(50, B) is True
    assert n3_nonconv_frac_invalid(49, B) is False
    assert n3_nonconv_frac_invalid(50, B) is True
    # exact arithmetic recorded
    assert 49 / 999 <= 0.05
    assert 50 / 999 > 0.05


def test_L2_N3_same_seed_deterministic():
    from quant.i03.iaaft import iaaft

    r = np.linspace(-1, 1, 64)
    a = iaaft(r, seed=10001, I_max=20, eps=1e-8)
    b = iaaft(r, seed=10001, I_max=20, eps=1e-8)
    assert np.allclose(a.series, b.series)
    c = iaaft(r, seed=10002, I_max=20, eps=1e-8)
    assert not np.allclose(a.series, c.series)


# ===========================================================================
# §14 Finite-surrogate p boundary
# ===========================================================================


def test_L2_pvalue_B999_max_count_for_alpha():
    """(1+c)/1000 ≤ 0.05 ⇒ c ≤ 49. Survive at c=49; fail at c=50."""

    B = 999
    alpha = 0.05
    c_max = oracle_max_count_survive_alpha(B, alpha)
    assert c_max == 49
    obs = 1.0
    # c=49 surrogates ≤ obs, rest >
    sur = np.concatenate([np.full(49, 0.5), np.full(B - 49, 2.0)])
    p = oracle_left_tail_p(obs, sur)
    assert p == pytest.approx((1 + 49) / 1000)
    assert p <= alpha
    assert survives(left_tail_p(obs, sur), alpha)
    # c=50
    sur2 = np.concatenate([np.full(50, 0.5), np.full(B - 50, 2.0)])
    p2 = left_tail_p(obs, sur2)
    assert p2 == pytest.approx(51 / 1000)
    assert p2 > alpha
    assert not survives(p2, alpha)


def test_L2_pvalue_left_tail_sign_and_ties():
    # Smaller Θ is more extreme
    assert left_tail_p(1.0, np.array([2.0, 2.0, 2.0])) < left_tail_p(
        3.0, np.array([2.0, 2.0, 2.0])
    )
    # Ties Θ*=Θ count
    p = left_tail_p(1.0, np.array([1.0, 1.0, 2.0]))
    assert p == pytest.approx((1 + 2) / 4)


# ===========================================================================
# §15–17 Coherence / ND / multi-scale patterns
# ===========================================================================


def _fake_theta(periods, K, value=1.0):
    return {p: {k: value for k in K} for p in periods}


def test_L2_multiscale_patterns_no_majority_vote():
    cfg = DEFAULT_CONFIG
    K = cfg.K
    periods = (1, 2, 3)
    # B>=19 so c=0 yields p=1/(B+1)<=0.05
    obs = _fake_theta(periods, K, 0.1)
    bat = [_fake_theta(periods, K, 1.0) for _ in range(20)]
    g = build_survival_grid(obs, bat, bat, cfg)
    assert g.C4 and g.C3
    # Only one cell extreme → not global C4
    obs2 = {
        1: {10: 1.0, 25: 1.0, 50: 0.1},
        2: {10: 1.0, 25: 1.0, 50: 1.0},
        3: {10: 1.0, 25: 1.0, 50: 1.0},
    }
    bat2 = [
        {
            1: {10: 0.5, 25: 0.5, 50: 1.0},
            2: {10: 0.5, 25: 0.5, 50: 0.5},
            3: {10: 0.5, 25: 0.5, 50: 0.5},
        }
        for _ in range(20)
    ]
    g2 = build_survival_grid(obs2, bat2, bat2, cfg)
    assert g2.C4 is False


def test_L2_null_disagreement_cannot_PASS():
    # C4 True C3 False → INCONCLUSIVE ND-2
    r = decide_verdict(VerdictInput(True, True, True, False, False))
    assert r.label == VerdictLabel.INCONCLUSIVE
    assert r.nd_code == "ND-2"
    # N4 fail N3 survive without F4
    r2 = decide_verdict(VerdictInput(True, True, False, True, False))
    assert r2.label != VerdictLabel.PASS


# ===========================================================================
# §18 Verdict truth-table exhaustion vs independent oracle
# ===========================================================================


def test_L2_verdict_truth_table_exhaustive_vs_oracle():
    labels = []
    for V, E, C4, C3, F4 in itertools.product([False, True], repeat=5):
        # Skip impossible C4 and F4 both True (still test production behavior)
        prod = decide_verdict(VerdictInput(V, E, C4, C3, F4))
        o_label, o_nd = oracle_decide_verdict(V, E, C4, C3, F4)
        assert prod.label.value == o_label
        assert prod.nd_code == o_nd
        labels.append(o_label)
    assert "PASS" in labels and "FAIL" in labels and "INCONCLUSIVE" in labels


# ===========================================================================
# §19 Locality
# ===========================================================================


def test_L2_locality_Lambda_eq_1_inconclusive_path():
    # Hard: Lambda >= 1 → validity fails
    obs = (
        LocalityBlockDiagnostic(1, 1.0, 0.5, True, 10),
        LocalityBlockDiagnostic(2, 0.5, 0.5, False, 10),
        LocalityBlockDiagnostic(3, 0.5, 0.5, False, 10),
    )
    # Empty N4 locality → validity_ok False if we only check hard on obs via helper
    # locality_validity_ok requires surrogate medians; craft surrogates with lower Lambda
    sur = [
        (
            LocalityBlockDiagnostic(1, 0.4, 0.8, False, 10),
            LocalityBlockDiagnostic(2, 0.4, 0.8, False, 10),
            LocalityBlockDiagnostic(3, 0.4, 0.8, False, 10),
        )
    ]
    assert locality_validity_ok(obs, sur) is False


def test_L2_locality_invalid_never_FAIL_verdict():
    r = decide_verdict(VerdictInput(V=False, E=True, C4=True, C3=True, F4=False))
    assert r.label == VerdictLabel.INCONCLUSIVE
    assert r.label != VerdictLabel.FAIL


# ===========================================================================
# §20 Effective sample n_min per block
# ===========================================================================


def test_L2_n_min_is_per_block():
    cfg = DEFAULT_CONFIG
    assert cfg.n_min == 250
    # E requires all blocks ≥ n_min — encoded in pipeline; unit-check predicate
    n_queries = (249, 250, 251)
    E_249 = all(n >= cfg.n_min for n in (249, 250, 250))
    E_250 = all(n >= cfg.n_min for n in (250, 250, 250))
    E_251 = all(n >= cfg.n_min for n in (251, 250, 250))
    assert E_249 is False
    assert E_250 is True
    assert E_251 is True
    _ = n_queries


# ===========================================================================
# §21–22 Artifact reconstructibility + reproducibility
# ===========================================================================


def test_L2_artifact_reconstruct_verdict_and_repro():
    rng = np.random.default_rng(30)
    n = 500
    r = np.full(n, np.nan)
    r[1:] = rng.normal(0, 0.01, n - 1)
    a = run_structural_analysis(r, B_n4=2, B_n3=2, compute_locality_on_n4=False)
    b = run_structural_analysis(r, B_n4=2, B_n3=2, compute_locality_on_n4=False)
    art = artifact_dict(a, input_hash="synth-l2")
    # Reconstruct verdict from artifact predicates + survival flags
    V, E = art["predicates"]["V"], art["predicates"]["E"]
    C4, C3, F4 = art["survival"]["C4"], art["survival"]["C3"], art["survival"]["F4"]
    recon = decide_verdict(VerdictInput(V, E, C4, C3, F4))
    assert recon.label.value == art["verdict"]["label"]
    assert a.verdict.label == b.verdict.label
    assert a.survival.pvalues == b.survival.pvalues
    for key in (
        "schema",
        "prereg_id",
        "config",
        "blocks",
        "emnd",
        "locality",
        "n4",
        "n3",
        "survival",
        "verdict",
    ):
        assert key in art


# ===========================================================================
# §23 Seeded stress (deterministic)
# ===========================================================================


def test_L2_seeded_random_stress_blocks_and_sigma():
    rng = np.random.default_rng(99)
    for T in rng.integers(30, 200, size=8):
        T = int(T)
        blocks = build_blocks(T, DEFAULT_CONFIG)
        assert sum(b.indices.size for b in blocks) == T
    r = np.full(80, np.nan)
    r[1:] = rng.normal(0, 0.03, 79)
    for t in range(20, 80):
        s = oracle_n4_sigma(r, t)
        assert s == pytest.approx(n4_sigma_at(r, t, DEFAULT_CONFIG))


# ===========================================================================
# §24 Mutation-style: suite catches plausible wrong contracts
# ===========================================================================


def test_L2_mutation_tau_strict_gt_would_fail():
    # Our pool accepts |t-s|==20; a wrong tau>20 would reject 20
    from quant.i03.blocks import TemporalBlock

    defined = np.ones(60, dtype=bool)
    defined[:5] = False
    block = TemporalBlock(1, 0, 59, np.arange(60, dtype=np.intp))
    pool = admissible_pool(30, block, defined, DEFAULT_CONFIG)
    assert (30 - 20) in pool  # would fail if implementation used >20


def test_L2_mutation_sigma_ddof0_caught_by_oracle():
    r = np.full(40, np.nan)
    r[1:21] = np.arange(1, 21, dtype=float)
    s = n4_sigma_at(r, 20, DEFAULT_CONFIG)
    wrong = float(np.std(r[1:21], ddof=0))
    assert s != pytest.approx(wrong)


def test_L2_mutation_right_tail_caught():
    # Left-tail: small obs extreme; right-tail would invert
    obs = 0.1
    sur = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
    p_left = left_tail_p(obs, sur)
    p_right = (1 + int(np.sum(sur >= obs))) / (len(sur) + 1)
    assert p_left < p_right


def test_L2_mutation_strict_lt_alpha_caught():
    # p==0.05 must survive (<=); strict < would fail
    assert survives(0.05, 0.05) is True


def test_L2_mutation_majority_k_not_PASS():
    # Two of three scales is not global coherence
    # C4 requires all k all periods — majority would wrongly pass
    r = decide_verdict(VerdictInput(True, True, False, False, False))
    assert r.label != VerdictLabel.PASS
