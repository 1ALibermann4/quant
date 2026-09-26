"""I04-CAL unit / L1 / causality tests."""

from __future__ import annotations

import os

import numpy as np
import pytest

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

from quant.i04_cal.geometries import (
    g0_distance,
    g0_embed,
    soft_dtw_divergence,
    iter_geometry_specs,
    embed_and_distance_fns,
)
from quant.i04_cal.params import world_seed, WINDOWS
from quant.i04_cal.worlds import generate_world, gen_s0a, gen_s1
from quant.i04_cal.gates import compute_gates_for_spec, embargo_ok
from quant.i04_cal.types import GeometrySpec


def test_seed_map_stable():
    assert world_seed("S0a", 0) == 0
    assert world_seed("S1", 3) == 200003
    assert world_seed("S7", 31) == 800031


def test_s0a_reproducible():
    a = gen_s0a(0)
    b = gen_s0a(0)
    assert np.allclose(a.returns, b.returns)
    assert a.returns.shape[0] == 8192


def test_s1_has_latent_h():
    w = gen_s1(0)
    assert "h" in w.latent
    assert w.latent["h"].shape == w.returns.shape


def test_g0_self_distance_zero():
    r = gen_s0a(0).returns
    e = g0_embed(r, 100, 20)
    assert g0_distance(e, e) == 0.0


def test_soft_dtw_nonneg_div_approx():
    x = np.linspace(0, 1, 16)
    y = np.linspace(0, 1, 16) + 0.1
    d = soft_dtw_divergence(x, y, gamma=1.0)
    assert np.isfinite(d)


def test_causality_future_does_not_change_embed():
    r = gen_s0a(1).returns.copy()
    t, W = 200, 20
    e0 = g0_embed(r, t, W)
    r2 = r.copy()
    r2[t + 1 :] = 999.0
    e1 = g0_embed(r2, t, W)
    assert np.allclose(e0, e1)


def test_embargo():
    assert embargo_ok(100, 50, 20)
    assert not embargo_ok(100, 90, 20)


def test_no_best_w_in_spec_list():
    # all three windows must remain in config — smoke via WINDOWS constant
    assert WINDOWS == (20, 40, 60)


def test_gates_smoke_g0():
    w = generate_world("S0a", 0)
    spec = GeometrySpec("G0", "default", {})
    out = compute_gates_for_spec(w, spec, W=20, seed=123)
    assert out["k"]["5"]["CAL_G1_contrast_median"] is not None
    assert out["CAL_6"]["oracle_status"] == "NOT_APPLICABLE"


def test_geometry_specs_include_grids_no_single_best():
    specs = iter_geometry_specs()
    g1 = [s for s in specs if s.geometry_id == "G1"]
    assert len(g1) == 3
    gord = [s for s in specs if s.geometry_id == "GORD"]
    assert len(gord) == 2


def test_pipeline_max_cells(tmp_path):
    from quant.i04_cal.pipeline import run_calibration
    from quant.i04_cal.params import CalConfig

    cfg = CalConfig(
        B=1,
        worlds=("S0a",),
        geometries=("G0",),
        windows=(20,),
    )
    man = run_calibration(tmp_path / "out", cfg, max_cells=1)
    assert man["n_rows"] >= 1
