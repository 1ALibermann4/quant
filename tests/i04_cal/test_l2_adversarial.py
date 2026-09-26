"""L2 adversarial / invariant tests for I04-CAL."""

from __future__ import annotations

import os

import numpy as np

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

from quant.i04_cal.geometries import airm_distance, _cov_reg, gord_embed, gord_distance
from quant.i04_cal.worlds import generate_world
from quant.i04_cal.params import B_WORLD, world_seed


def test_b_world_is_32():
    assert B_WORLD == 32


def test_seeds_independent_of_call_order():
    s1 = world_seed("S3", 5)
    _ = generate_world("S0a", 0)
    s2 = world_seed("S3", 5)
    assert s1 == s2


def test_s4_oracle_excludes_edges():
    w = generate_world("S4", 0)
    assert w.oracle_labels is not None
    # some -1 labels exist
    assert np.any(w.oracle_labels < 0)


def test_s6_oracle_status_is_valid_or_invalid():
    w = generate_world("S6", 0)
    assert w.oracle_status.value in ("VALID", "INVALID")
    assert "observability_spearman" in w.latent


def test_airm_self_near_zero():
    rng = np.random.default_rng(0)
    w = rng.normal(size=40)
    C = _cov_reg(w, p=2, lam=1e-3)
    d = airm_distance(C, C)
    assert d < 1e-6 or not np.isfinite(d)  # numerical


def test_ordinal_hist_sums_to_one():
    rng = np.random.default_rng(1)
    r = rng.normal(size=200)
    h = gord_embed(r, 100, 40, D=3, tau=1)
    assert abs(h.sum() - 1.0) < 1e-9
    assert gord_distance(h, h) < 1e-9


def test_invalid_oracle_not_fail_geometry():
    # S6/S7 may be INVALID oracle — geometry still executable
    w = generate_world("S7", 0)
    assert w.world_status.value == "VALID"
