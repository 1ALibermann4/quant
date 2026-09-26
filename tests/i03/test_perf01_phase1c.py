"""PERF-01 Phase 1C — deterministic checkpoint / resume tests (non-market)."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from quant.i03.blocks import build_blocks
from quant.i03.checkpoint import (
    CheckpointError,
    CheckpointStore,
    RunStatus,
    atomic_write_bytes,
    compute_run_id,
    returns_input_sha256,
)
from quant.i03.fixture_hat import generate_hat_returns
from quant.i03.n4 import build_n4_scale_path
from quant.i03.params import DEFAULT_CONFIG
from quant.i03.parallel import run_n3_battery_parallel, run_n4_battery_parallel
from quant.i03.pipeline import artifact_dict, run_structural_analysis


def _fbits(a: float, b: float) -> bool:
    if math.isnan(a) and math.isnan(b):
        return True
    if math.isinf(a) and math.isinf(b):
        return math.copysign(1.0, a) == math.copysign(1.0, b)
    return a == b


def _theta_eq(a, b) -> bool:
    if len(a) != len(b):
        return False
    for xa, xb in zip(a, b):
        if set(xa) != set(xb):
            return False
        for p in xa:
            if set(xa[p]) != set(xb[p]):
                return False
            for k in xa[p]:
                if not _fbits(float(xa[p][k]), float(xb[p][k])):
                    return False
    return True


def _loc_eq(a, b) -> bool:
    if len(a) != len(b):
        return False
    for ba, bb in zip(a, b):
        if len(ba) != len(bb):
            return False
        for da, db in zip(ba, bb):
            if (
                da.period != db.period
                or da.hard_degenerate != db.hard_degenerate
                or da.n_queries_used != db.n_queries_used
                or not _fbits(da.Lambda, db.Lambda)
                or not _fbits(da.Gamma, db.Gamma)
            ):
                return False
    return True


def _art_eq(a, b) -> bool:
    aa = artifact_dict(a, mode="TEST")
    bb = artifact_dict(b, mode="TEST")
    for art in (aa, bb):
        art.pop("execution", None)
        art.pop("implementation_id", None)
        art.pop("input_hash", None)
        art.pop("timing", None)
    return aa == bb


def test_atomic_write_ignores_tmp_and_rejects_corrupt(tmp_path: Path) -> None:
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    store = CheckpointStore(tmp_path)
    run_id = compute_run_id(
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=4,
        B_n3=4,
        do_loc_n4=True,
    )
    store.write_new_manifest(
        run_id=run_id,
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=4,
        B_n3=4,
        do_loc_n4=True,
    )
    # Interrupted persistence: only .tmp present
    tmp = store.record_path("N4", 1).with_name("b_000001.json.tmp")
    atomic_write_bytes(tmp, b'{"truncated": true}')
    assert store.list_completed("N4", run_id=run_id, B=4) == {}

    # Valid then corrupt
    scale = build_n4_scale_path(r, cfg)
    blocks = build_blocks(len(r), cfg)
    run_n4_battery_parallel(
        r,
        scale,
        cfg,
        B=2,
        workers=1,
        do_loc_n4=True,
        blocks=blocks,
        checkpoint_store=store,
        run_id=run_id,
    )
    path = store.record_path("N4", 1)
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["payload_sha256"] = "sha256:" + ("00" * 32)
    path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(CheckpointError, match="hash mismatch"):
        store.load_record("N4", 1, run_id=run_id)


def test_n4_partial_resume_bitwise(tmp_path: Path) -> None:
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    scale = build_n4_scale_path(r, cfg)
    blocks = build_blocks(len(r), cfg)
    B = 6
    th_ref, loc_ref = run_n4_battery_parallel(
        r, scale, cfg, B=B, workers=1, do_loc_n4=True, blocks=blocks
    )

    store = CheckpointStore(tmp_path / "ck")
    run_id = compute_run_id(
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=B,
        B_n3=2,
        do_loc_n4=True,
    )
    store.write_new_manifest(
        run_id=run_id,
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=B,
        B_n3=2,
        do_loc_n4=True,
    )
    # First wave: only b=1..3 via temporary B trick — write by running B=3 then
    # expand? Better: run full with store but pre-delete later files.
    run_n4_battery_parallel(
        r,
        scale,
        cfg,
        B=3,
        workers=1,
        do_loc_n4=True,
        blocks=blocks,
        checkpoint_store=store,
        run_id=run_id,
    )
    # Upgrade B in manifest is forbidden — use same B from start with partial schedule.
    # Rebuild store for clean partial of B=6
    store2 = CheckpointStore(tmp_path / "ck2")
    run_id2 = compute_run_id(
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=B,
        B_n3=2,
        do_loc_n4=True,
    )
    store2.write_new_manifest(
        run_id=run_id2,
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=B,
        B_n3=2,
        do_loc_n4=True,
    )
    # Manually run missing subset by calling parallel with injected completed empty
    # and only mapping 1..3 using internal API: save results for 1..3
    from quant.i03.parallel import _init_worker, _n4_worker, map_surrogate_b

    payload = {
        "returns": r,
        "n4_scale": scale,
        "blocks": blocks,
        "cfg": cfg,
        "do_loc_n4": True,
        "include_returns": False,
    }
    partial = map_surrogate_b(
        _n4_worker, range(1, 4), workers=1, initargs=(payload,)
    )
    for row in partial:
        store2.save_result(
            row, run_id=run_id2, expected_seed=int(cfg.master_seed + row["b"])
        )
    assert store2.missing_b("N4", run_id=run_id2, B=B) == [4, 5, 6]

    th_res, loc_res = run_n4_battery_parallel(
        r,
        scale,
        cfg,
        B=B,
        workers=2,
        do_loc_n4=True,
        blocks=blocks,
        checkpoint_store=store2,
        run_id=run_id2,
    )
    assert _theta_eq(th_ref, th_res)
    assert _loc_eq(loc_ref, loc_res)
    assert store2.missing_b("N4", run_id=run_id2, B=B) == []


def test_n3_resume_preserves_nonconvergence(tmp_path: Path) -> None:
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    blocks = build_blocks(len(r), cfg)
    B = 5
    meta_ref, th_ref, rows_ref = run_n3_battery_parallel(
        r, cfg, B=B, workers=1, blocks=blocks, include_returns=True
    )

    store = CheckpointStore(tmp_path)
    run_id = compute_run_id(
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=2,
        B_n3=B,
        do_loc_n4=False,
    )
    store.write_new_manifest(
        run_id=run_id,
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=2,
        B_n3=B,
        do_loc_n4=False,
    )
    from quant.i03.parallel import map_surrogate_b, _n3_worker

    payload = {
        "returns": r,
        "blocks": blocks,
        "cfg": cfg,
        "include_returns": False,
    }
    partial = map_surrogate_b(_n3_worker, [1, 2], workers=1, initargs=(payload,))
    for row in partial:
        store.save_result(row, run_id=run_id, expected_seed=10_000 + int(row["b"]))
    # Non-converged rows among 1..2 must remain as completed
    for b in (1, 2):
        loaded = store.load_record("N3", b, run_id=run_id)
        assert loaded["converged"] == rows_ref[b - 1]["converged"]

    meta, th, rows = run_n3_battery_parallel(
        r,
        cfg,
        B=B,
        workers=4,
        blocks=blocks,
        include_returns=True,
        checkpoint_store=store,
        run_id=run_id,
    )
    assert meta == meta_ref
    assert _theta_eq(th_ref, th)
    for a, b in zip(rows_ref, rows):
        assert a["converged"] == b["converged"]
        assert a["iterations"] == b["iterations"]
        assert a["seed"] == b["seed"]
        assert np.array_equal(a["returns"], b["returns"], equal_nan=True)


def test_cross_worker_resume_pipeline(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("I03_ALLOW_TEST_OVERRIDES", "1")
    r = generate_hat_returns()
    cfg = DEFAULT_CONFIG
    ref = run_structural_analysis(
        r, cfg, B_n4=6, B_n3=4, compute_locality_on_n4=True, workers=1
    )

    ck = tmp_path / "run"
    # Start with workers=4, only complete N4 partially then crash simulation
    store = CheckpointStore(ck)
    # Use pipeline for first partial via direct battery after init
    from quant.i03.checkpoint import compute_run_id, returns_input_sha256

    run_id = compute_run_id(
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=6,
        B_n3=4,
        do_loc_n4=True,
    )
    store.write_new_manifest(
        run_id=run_id,
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=6,
        B_n3=4,
        do_loc_n4=True,
    )
    scale = build_n4_scale_path(r, cfg)
    blocks = build_blocks(len(r), cfg)
    from quant.i03.parallel import map_surrogate_b, _n4_worker, _n3_worker

    p4 = {
        "returns": r,
        "n4_scale": scale,
        "blocks": blocks,
        "cfg": cfg,
        "do_loc_n4": True,
        "include_returns": False,
    }
    for row in map_surrogate_b(_n4_worker, range(1, 4), workers=4, initargs=(p4,)):
        store.save_result(
            row, run_id=run_id, expected_seed=int(cfg.master_seed + row["b"])
        )
    p3 = {
        "returns": r,
        "blocks": blocks,
        "cfg": cfg,
        "include_returns": False,
    }
    for row in map_surrogate_b(_n3_worker, [1], workers=1, initargs=(p3,)):
        store.save_result(row, run_id=run_id, expected_seed=10_000 + int(row["b"]))

    # Resume with different worker count
    resumed = run_structural_analysis(
        r,
        cfg,
        B_n4=6,
        B_n3=4,
        compute_locality_on_n4=True,
        workers=1,
        checkpoint_dir=ck,
        resume=True,
    )
    assert _art_eq(ref, resumed)
    assert store.status() == RunStatus.COMPLETE

    # Resume again with workers=4 from COMPLETE should schedule nothing new
    resumed2 = run_structural_analysis(
        r,
        cfg,
        B_n4=6,
        B_n3=4,
        compute_locality_on_n4=True,
        workers=4,
        checkpoint_dir=ck,
        resume=True,
    )
    assert _art_eq(ref, resumed2)


def test_fail_closed_wrong_identity_and_family(tmp_path: Path) -> None:
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    store = CheckpointStore(tmp_path)
    run_id = compute_run_id(
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=3,
        B_n3=3,
        do_loc_n4=True,
    )
    store.write_new_manifest(
        run_id=run_id,
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=3,
        B_n3=3,
        do_loc_n4=True,
    )
    # wrong input
    r2 = r.copy()
    r2[10] = 0.123456
    with pytest.raises(CheckpointError, match="identity mismatch"):
        store.assert_compatible(
            run_id=compute_run_id(
                input_sha256=returns_input_sha256(r2),
                cfg=cfg,
                B_n4=3,
                B_n3=3,
                do_loc_n4=True,
            ),
            input_sha256=returns_input_sha256(r2),
            cfg=cfg,
            B_n4=3,
            B_n3=3,
            do_loc_n4=True,
        )
    # stale other family in N4 path
    bad = {
        "b": 1,
        "family": "N3",
        "seed": 10001,
        "theta": {1: {10: 0.0}},
        "converged": True,
        "iterations": 1,
    }
    store.save_result(bad, run_id=run_id, expected_seed=10001)
    # saved under N3 family dir because save uses row family
    assert (tmp_path / "N3" / "b_000001.json").is_file()
    # Place N3-shaped file into N4 directory
    n4_path = store.record_path("N4", 1)
    n4_path.parent.mkdir(parents=True, exist_ok=True)
    n4_path.write_text(
        (tmp_path / "N3" / "b_000001.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    with pytest.raises(CheckpointError):
        store.load_record("N4", 1, run_id=run_id)


def test_resume_requires_flag(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("I03_ALLOW_TEST_OVERRIDES", "1")
    r = generate_hat_returns()
    cfg = DEFAULT_CONFIG
    ck = tmp_path / "c"
    run_structural_analysis(
        r,
        cfg,
        B_n4=2,
        B_n3=2,
        workers=1,
        checkpoint_dir=ck,
        resume=False,
    )
    with pytest.raises(CheckpointError, match="--resume"):
        run_structural_analysis(
            r,
            cfg,
            B_n4=2,
            B_n3=2,
            workers=1,
            checkpoint_dir=ck,
            resume=False,
        )


def test_checkpoint_overhead_small(tmp_path: Path) -> None:
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    scale = build_n4_scale_path(r, cfg)
    blocks = build_blocks(len(r), cfg)
    B = 8
    import time

    t0 = time.perf_counter()
    run_n4_battery_parallel(
        r, scale, cfg, B=B, workers=2, do_loc_n4=True, blocks=blocks
    )
    t_plain = time.perf_counter() - t0

    store = CheckpointStore(tmp_path)
    run_id = compute_run_id(
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=B,
        B_n3=2,
        do_loc_n4=True,
    )
    store.write_new_manifest(
        run_id=run_id,
        input_sha256=returns_input_sha256(r),
        cfg=cfg,
        B_n4=B,
        B_n3=2,
        do_loc_n4=True,
    )
    t0 = time.perf_counter()
    run_n4_battery_parallel(
        r,
        scale,
        cfg,
        B=B,
        workers=2,
        do_loc_n4=True,
        blocks=blocks,
        checkpoint_store=store,
        run_id=run_id,
    )
    t_ckpt = time.perf_counter() - t0
    sizes = [p.stat().st_size for p in (tmp_path / "N4").glob("b_*.json")]
    assert sizes
    mean_bytes = float(np.mean(sizes))
    # Overhead should not be pathological (>3x) on this tiny HAT workload
    assert t_ckpt < t_plain * 3.0 + 5.0
    assert mean_bytes < 50_000
    # ESTIMATED B=999 storage for N4 only
    est_n4 = mean_bytes * 999
    assert est_n4 < 50_000_000  # < 50 MB
