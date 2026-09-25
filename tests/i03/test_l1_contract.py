"""I03 L1 synthetic contract tests (no market data)."""

from __future__ import annotations

import numpy as np
import pytest

from quant.i03.blocks import block_membership, build_blocks
from quant.i03.emnd import admissible_pool, compute_emnd_block, kth_distance
from quant.i03.g0 import build_states_x, state_vector_x
from quant.i03.inference import left_tail_p, survives
from quant.i03.n3 import generate_n3_battery
from quant.i03.n4 import build_n4_scale_path, n4_sigma_at, n4_surrogate_returns
from quant.i03.params import DEFAULT_CONFIG
from quant.i03.pipeline import artifact_dict, run_structural_analysis
from quant.i03.verdict import VerdictInput, VerdictLabel, decide_verdict


# ---------------------------------------------------------------------------
# A — causality / G0
# ---------------------------------------------------------------------------


def test_A_future_suffix_does_not_change_earlier_X(synthetic_returns):
    from quant.i02.params import DEFAULT_PARAMS as I02P

    r = synthetic_returns.copy()
    t = 400
    x0 = state_vector_x(r, t, I02P)
    r2 = r.copy()
    r2[t + 1 :] = 999.0
    x1 = state_vector_x(r2, t, I02P)
    assert np.allclose(x0, x1)


def test_A_zero_sigma_undefined():
    from quant.i02.params import DEFAULT_PARAMS
    from quant.i02.states_x import XUndefinedError

    r = np.full(300, np.nan)
    r[1:] = 0.0
    with pytest.raises(XUndefinedError):
        state_vector_x(r, 252, DEFAULT_PARAMS)


# ---------------------------------------------------------------------------
# B — tau boundary
# ---------------------------------------------------------------------------


def test_B_tau_19_rejected_20_accepted(synthetic_returns):
    cfg = DEFAULT_CONFIG
    states = build_states_x(synthetic_returns, cfg)
    defined = ~np.isnan(states[:, 0])
    blocks = build_blocks(len(synthetic_returns), cfg)
    # pick a query deep in block 2
    b = blocks[1]
    t = int(b.start + (b.end - b.start) // 2)
    pool = admissible_pool(t, b, defined, cfg)
    assert np.all(np.abs(pool - t) >= 20)
    assert not np.any(np.abs(pool - t) == 19)


# ---------------------------------------------------------------------------
# C — blocks
# ---------------------------------------------------------------------------


def test_C_block_remainder_appended_to_last():
    cfg = DEFAULT_CONFIG
    T = 100  # 100 // 3 = 33, R = 1 → B3 length 34
    blocks = build_blocks(T, cfg)
    assert len(blocks) == 3
    assert blocks[0].indices.size == 33
    assert blocks[1].indices.size == 33
    assert blocks[2].indices.size == 34
    assert blocks[2].end == T - 1


def test_C_no_cross_block_neighbors(synthetic_returns):
    cfg = DEFAULT_CONFIG
    states = build_states_x(synthetic_returns, cfg)
    defined = ~np.isnan(states[:, 0])
    blocks = build_blocks(len(synthetic_returns), cfg)
    b0 = blocks[0]
    t = int(b0.end)
    if not defined[t]:
        pytest.skip("edge undefined")
    pool = admissible_pool(t, b0, defined, cfg)
    for s in pool:
        assert block_membership(blocks, int(s)) == 1


# ---------------------------------------------------------------------------
# D/E — k-th distance oracle + ties
# ---------------------------------------------------------------------------


def test_D_E_kth_distance_oracle_and_ties():
    # query at origin; library points with known distances
    q = np.zeros(3)
    states = np.zeros((10, 3))
    # s=1 dist 1, s=2 dist 1 (tie → lower s first), s=3 dist 2, s=4 dist 3
    states[1] = [1, 0, 0]
    states[2] = [0, 1, 0]
    states[3] = [2, 0, 0]
    states[4] = [3, 0, 0]
    pool = np.array([4, 3, 2, 1], dtype=np.intp)
    assert kth_distance(q, pool, states, 1) == pytest.approx(1.0)
    assert kth_distance(q, pool, states, 2) == pytest.approx(1.0)
    assert kth_distance(q, pool, states, 3) == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# H/I — N4 sigma
# ---------------------------------------------------------------------------


def test_H_I_sample_stdev_denominator_19_includes_rt():
    cfg = DEFAULT_CONFIG
    r = np.full(50, np.nan)
    r[1:21] = np.arange(1, 21, dtype=float)
    t = 20
    s = n4_sigma_at(r, t, cfg)
    window = r[1:21]
    expected = float(np.std(window, ddof=1))
    assert s == pytest.approx(expected)
    # distinct from RMS RV
    rms = float(np.sqrt(np.mean(window * window)))
    assert s != pytest.approx(rms)


def test_J_K_N4_preserves_sigma_path_not_recomputed(synthetic_returns):
    cfg = DEFAULT_CONFIG
    scale = build_n4_scale_path(synthetic_returns, cfg)
    assert scale.valid
    r_star = n4_surrogate_returns(synthetic_returns, scale, b=1, cfg=cfg)
    # By construction: where Z, r* / sigma == z*
    Z = scale.Z_indices
    z_star_implied = r_star[Z] / scale.sigma[Z]
    # Original z multiset equals z_star multiset
    assert np.allclose(np.sort(scale.z[Z]), np.sort(z_star_implied))
    # sigma path used is the OBSERVED path (stored), not recomputed claim
    # Recomputed stdev on r* may differ — document/assert may-differ
    s_re_t = None
    for t in Z[:5]:
        s_re = n4_sigma_at(r_star, int(t), cfg)
        if s_re is not None and scale.sigma[t] > 0:
            s_re_t = s_re
            break
    # Not required equal; only that construction used scale.sigma
    assert scale.sigma is not None
    _ = s_re_t  # may differ; no assertion of equality


def test_N4_deterministic_same_seed(synthetic_returns):
    cfg = DEFAULT_CONFIG
    scale = build_n4_scale_path(synthetic_returns, cfg)
    a = n4_surrogate_returns(synthetic_returns, scale, 3, cfg)
    b = n4_surrogate_returns(synthetic_returns, scale, 3, cfg)
    assert np.allclose(a, b, equal_nan=True)


def test_N4_different_seed_may_differ(synthetic_returns):
    cfg = DEFAULT_CONFIG
    scale = build_n4_scale_path(synthetic_returns, cfg)
    a = n4_surrogate_returns(synthetic_returns, scale, 1, cfg)
    b = n4_surrogate_returns(synthetic_returns, scale, 2, cfg)
    assert not np.allclose(a, b, equal_nan=True)


# ---------------------------------------------------------------------------
# O/P — inference
# ---------------------------------------------------------------------------


def test_O_P_pvalue_and_alpha_equality():
    # Construct surrogates so p == 0.05 exactly with B=19:
    # p = (1+c)/(B+1) = 0.05 ⇒ 1+c = 1 ⇒ c=0 when B=19 → p=1/20=0.05
    obs = 1.0
    sur = np.full(19, 2.0)  # all > obs ⇒ count 0 ⇒ p=1/20=0.05
    p = left_tail_p(obs, sur)
    assert p == pytest.approx(0.05)
    assert survives(p, 0.05) is True
    assert survives(0.0500001, 0.05) is False


# ---------------------------------------------------------------------------
# T/U/V/W/Y — verdict engine
# ---------------------------------------------------------------------------


def test_T_PASS():
    r = decide_verdict(VerdictInput(V=True, E=True, C4=True, C3=True, F4=False))
    assert r.label == VerdictLabel.PASS
    assert r.nd_code == "ND-1"


def test_U_FAIL_F4():
    r = decide_verdict(VerdictInput(V=True, E=True, C4=False, C3=False, F4=True))
    assert r.label == VerdictLabel.FAIL


def test_V_INCONCLUSIVE_ND2():
    r = decide_verdict(VerdictInput(V=True, E=True, C4=True, C3=False, F4=False))
    assert r.label == VerdictLabel.INCONCLUSIVE
    assert r.nd_code == "ND-2"


def test_W_locality_invalid_INCONCLUSIVE():
    r = decide_verdict(VerdictInput(V=False, E=True, C4=True, C3=True, F4=False))
    assert r.label == VerdictLabel.INCONCLUSIVE
    assert r.reason == "NEG_V"


def test_Y_diagnostic_cannot_rescue_fail():
    # Even if we imagined diagnostics saying "almost", F4 still FAIL
    r = decide_verdict(VerdictInput(V=True, E=True, C4=False, C3=True, F4=True))
    assert r.label == VerdictLabel.FAIL


def test_insufficient_E():
    r = decide_verdict(VerdictInput(V=True, E=False, C4=True, C3=True, F4=False))
    assert r.label == VerdictLabel.INCONCLUSIVE


# ---------------------------------------------------------------------------
# M — IAAFT accounting
# ---------------------------------------------------------------------------


def test_M_n3_requested_vs_converged(synthetic_returns):
    cfg = DEFAULT_CONFIG
    meta, series = generate_n3_battery(synthetic_returns, cfg, B=5)
    assert meta.B_requested == 5
    assert len(series) == 5
    assert meta.n_converged + meta.n_nonconverged == 5
    assert len(meta.converged_flags) == 5


# ---------------------------------------------------------------------------
# X — deterministic rerun (small B)
# ---------------------------------------------------------------------------


def test_X_pipeline_deterministic_small_B():
    """Short synthetic series + tiny B — determinism, not PASS power."""

    rng = np.random.default_rng(1)
    n = 600
    r = np.full(n, np.nan, dtype=np.float64)
    r[1:] = rng.normal(0.0, 0.01, size=n - 1)
    a = run_structural_analysis(r, B_n4=2, B_n3=2, compute_locality_on_n4=False)
    b = run_structural_analysis(r, B_n4=2, B_n3=2, compute_locality_on_n4=False)
    assert a.survival.pvalues == b.survival.pvalues
    assert a.verdict.label == b.verdict.label
    art = artifact_dict(a, input_hash="synthetic")
    assert art["n4"]["preserves"].startswith("sigma_hat_path")
    assert "recomputed" in art["n4"]["does_not_claim"]


def test_params_reject_retune():
    with pytest.raises(ValueError):
        from quant.i03.params import I03Config

        I03Config(W_X=21)  # type: ignore[call-arg]
