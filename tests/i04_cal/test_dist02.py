"""DIST-02 targeted tests (T01-T20). Mini controlled universes only;
no real 12027-cell execution."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from quant.i04_cal.dist02 import (
    COST_MODEL_VERSION,
    KAGGLE_WORKERS,
    QUALIFIED_SOURCE_HEAD,
    classify_batch_output,
    estimate_cell_cost,
    load_batch,
    plan_batches,
    plan_diagnostics,
    queue_status,
    run_batch,
    save_batch_plan,
    snapshot_identity_hash,
    validate_global,
    validate_snapshot,
)
from quant.i04_cal.distributed import canonical_config, digest, scientific_identity
from quant.i04_cal.params import CalConfig
from quant.i04_cal.pipeline import (
    _checkpoint_path,
    _record_hash,
    expected_cell_ids,
    config_hash,
)

ROOT = Path(__file__).resolve().parents[2]
DIST01_HEAD = "00f9e046ea78ec4769f5ed3a051d0262a1363565"
MINI = CalConfig(geometries=("G0",), worlds=("S0a",), windows=(20,), B=4, workers=KAGGLE_WORKERS)
MINI_CFG_JSON = json.dumps({"geometries": ("G0",), "worlds": ("S0a",), "windows": (20,),
                            "B": 4, "workers": KAGGLE_WORKERS})


def mini_universe(cfg: CalConfig = MINI) -> list[str]:
    return expected_cell_ids(cfg)


def make_snapshot(cfg: CalConfig, remaining: list[str], run_id: str = "TEST") -> dict:
    universe = mini_universe(cfg) if cfg is MINI else expected_cell_ids(cfg)
    canonical = [k for k in universe if k in set(remaining)]
    return {
        "run_id": run_id,
        "completed_local": len(universe) - len(canonical),
        "remaining_count": len(canonical),
        "remaining_ids": canonical,
        "remaining_ids_hash": digest(canonical),
        **scientific_identity(cfg),
    }


def fake_row(cfg: CalConfig, key: str, marker: str = "ok") -> dict:
    row = {"cell_key": key, "status": "OK", "config_hash": config_hash(cfg),
           "marker": marker, "world_id": key.split("|")[0]}
    row["record_hash"] = _record_hash(row)
    return row


def write_ckpt(ckpt_dir: Path, row: dict) -> None:
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    _checkpoint_path(ckpt_dir, row["cell_key"]).write_text(json.dumps(row), encoding="utf-8")


def make_output(out_dir: Path, batch: dict, cfg: CalConfig, keys: list[str] | None = None,
                status: str = "COMPLETE") -> Path:
    keys = batch["cell_ids"] if keys is None else keys
    manifest = {
        "schema": "I04-CAL-SHARD-RUN-v1", "run_id": batch["run_id"], "shard_id": batch["shard_id"],
        "universe_hash": batch["universe_hash"], "requested_ids_hash": batch["requested_ids_hash"],
        "config_hash": batch["config_hash"], "seed_contract": batch["seed_contract"],
        "generator_oracle_version": batch["generator_oracle_version"], "code_head": "x",
        "cell_ids": batch["cell_ids"], "expected_cells": len(batch["cell_ids"]),
        "workers": KAGGLE_WORKERS, "status": status, "completed_cells": len(keys),
    }
    out_dir.mkdir(parents=True)
    (out_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    for key in keys:
        write_ckpt(out_dir / "ckpt", fake_row(cfg, key))
    return out_dir


def make_local_dir(local_dir: Path, cfg: CalConfig, keys: list[str]) -> Path:
    local_dir.mkdir(parents=True)
    (local_dir / "manifest.json").write_text(json.dumps({
        "git_commit": QUALIFIED_SOURCE_HEAD, "config_hash": config_hash(cfg),
        "seed_contract": "I04-CAL-SEED-v1", "generator_oracle_version": "I04-CAL-SPEC-v0.2",
        "expected_cells": len(expected_cell_ids(cfg))}), encoding="utf-8")
    for key in keys:
        write_ckpt(local_dir / "ckpt", fake_row(cfg, key))
    return local_dir


def make_plan(tmp: Path, cfg: CalConfig = MINI, remaining: list[str] | None = None,
              pcfg: dict | None = None) -> tuple[dict, Path]:
    remaining = mini_universe(cfg) if remaining is None else remaining
    snap = make_snapshot(cfg, remaining)
    plan = plan_batches(snap, cfg=cfg, planner_config=pcfg)
    plan_dir = tmp / "plan"
    save_batch_plan(plan_dir, plan)
    return plan, plan_dir


# T01 — snapshot identity accepted
def test_t01_snapshot_identity_accepted(tmp_path: Path) -> None:
    canon = canonical_config()
    remaining = expected_cell_ids(canon)[:6]
    snap = make_snapshot(canon, remaining)
    plan = plan_batches(snap, cfg=canon, planner_config={"batch_count": 2})
    assert sorted(c for b in plan["batches"] for c in b["cell_ids"]) == sorted(remaining)
    mini_snap = make_snapshot(MINI, mini_universe())
    plan_batches(mini_snap, cfg=MINI, planner_config={"batch_count": 2})


# T02 — wrong remaining_ids_hash rejected
def test_t02_wrong_remaining_ids_hash(tmp_path: Path) -> None:
    snap = make_snapshot(MINI, mini_universe())
    snap["remaining_ids_hash"] = "0" * 64
    with pytest.raises(RuntimeError, match="remaining_ids_hash"):
        plan_batches(snap, cfg=MINI, planner_config={"batch_count": 2})


# T03 — wrong universe_hash rejected
def test_t03_wrong_universe_hash(tmp_path: Path) -> None:
    snap = make_snapshot(MINI, mini_universe())
    snap["universe_hash"] = "0" * 64
    with pytest.raises(RuntimeError, match="universe_hash"):
        plan_batches(snap, cfg=MINI, planner_config={"batch_count": 2})


# T04/T05 — exact partition, no duplicates across batches
def test_t04_t05_exact_partition_no_duplicates(tmp_path: Path) -> None:
    remaining = mini_universe()
    snap = make_snapshot(MINI, remaining)
    plan = plan_batches(snap, cfg=MINI, planner_config={"batch_count": 3})
    union = [c for b in plan["batches"] for c in b["cell_ids"]]
    assert set(union) == set(remaining)
    assert len(union) == len(set(union))
    for i, a in enumerate(plan["batches"]):
        for b in plan["batches"][i + 1:]:
            assert not set(a["cell_ids"]) & set(b["cell_ids"])


# T06 — deterministic planner
def test_t06_deterministic_plan(tmp_path: Path) -> None:
    snap = make_snapshot(MINI, mini_universe())
    a = plan_batches(snap, cfg=MINI, planner_config={"batch_count": 2})
    b = plan_batches(snap, cfg=MINI, planner_config={"batch_count": 2})
    assert a["plan_hash"] == b["plan_hash"]
    assert [x["cell_ids"] for x in a["batches"]] == [x["cell_ids"] for x in b["batches"]]
    canon = lambda p: json.dumps({k: v for k, v in p.items() if k != "created_at"},
                                 sort_keys=True, default=str)
    assert canon(a) == canon(b)


# T07 — planner config change -> new planner identity and different partition
def test_t07_planner_config_identity(tmp_path: Path) -> None:
    snap = make_snapshot(MINI, mini_universe())
    a = plan_batches(snap, cfg=MINI, planner_config={"batch_count": 2})
    b = plan_batches(snap, cfg=MINI, planner_config={"batch_count": 4})
    assert a["planner_hash"] != b["planner_hash"]
    assert a["batch_count"] != b["batch_count"]
    c = plan_batches(snap, cfg=MINI, planner_config={"batch_target_cost_s": 1.0})
    assert c["planner_hash"] != a["planner_hash"]


# T08 — unknown batch rejected
def test_t08_unknown_batch(tmp_path: Path) -> None:
    _, plan_dir = make_plan(tmp_path, pcfg={"batch_count": 2})
    with pytest.raises(RuntimeError, match="unknown batch"):
        load_batch(plan_dir, "BATCH-9999", MINI)
    with pytest.raises(RuntimeError, match="unknown batch"):
        run_batch(plan_dir, "BATCH-9999", tmp_path / "out", cfg=MINI)


# T09 — wrong batch hash rejected
def test_t09_wrong_batch_hash(tmp_path: Path) -> None:
    _, plan_dir = make_plan(tmp_path, pcfg={"batch_count": 2})
    shard_path = plan_dir / "shard-00000.json"
    shard = json.loads(shard_path.read_text(encoding="utf-8"))
    shard["cell_ids_hash"] = "0" * 64
    shard_path.write_text(json.dumps(shard), encoding="utf-8")
    with pytest.raises(RuntimeError, match="STOP"):
        load_batch(plan_dir, "BATCH-0000", MINI)


# T10 — workers != 2 rejected
def test_t10_workers_not_two_rejected(tmp_path: Path) -> None:
    _, plan_dir = make_plan(tmp_path, pcfg={"batch_count": 2})
    with pytest.raises(RuntimeError, match="2 workers"):
        run_batch(plan_dir, "BATCH-0000", tmp_path / "o", workers=4,
                  cfg=CalConfig(**json.loads(MINI_CFG_JSON) | {"workers": 4}))
    with pytest.raises(RuntimeError, match="2 workers"):
        run_batch(plan_dir, "BATCH-0000", tmp_path / "o2", workers=1, cfg=MINI)


# T14 — unexpected checkpoint rejected
def test_t14_unexpected_checkpoint(tmp_path: Path) -> None:
    plan, plan_dir = make_plan(tmp_path, pcfg={"batch_count": 2})
    batch = plan["batches"][0]
    foreign = "S9|b=0|W=20|G0:default"
    out = make_output(tmp_path / "outs" / "b0", batch, MINI)
    write_ckpt(out / "ckpt", fake_row(MINI, foreign))
    status, _ = classify_batch_output(plan_dir, batch, out, MINI)
    assert status == "INVALID"
    with pytest.raises(RuntimeError, match="invalid batch outputs"):
        validate_global(plan_dir, tmp_path / "outs", cfg=MINI)


# T17 — missing batch/cell rejected
def test_t17_missing_batch_rejected(tmp_path: Path) -> None:
    plan, plan_dir = make_plan(tmp_path, pcfg={"batch_count": 2})
    make_output(tmp_path / "outs" / "b0", plan["batches"][0], MINI)
    report = validate_global(plan_dir, tmp_path / "outs", cfg=MINI)
    assert report["complete"] is False and report["batches_missing"] == ["BATCH-0001"]
    with pytest.raises(RuntimeError, match="merge refused"):
        validate_global(plan_dir, tmp_path / "outs", cfg=MINI, merge_out=tmp_path / "m")


# T18 — unexpected cell rejected
def test_t18_unexpected_cell_rejected(tmp_path: Path) -> None:
    plan, plan_dir = make_plan(tmp_path, pcfg={"batch_count": 2})
    out = make_output(tmp_path / "outs" / "b0", plan["batches"][0], MINI)
    write_ckpt(out / "ckpt", fake_row(MINI, "S0a|b=99|W=20|G0:default"))
    with pytest.raises(RuntimeError):
        validate_global(plan_dir, tmp_path / "outs", cfg=MINI)


# T15 — conflicting/duplicate cell rejected
def test_t15_conflicting_duplicate_rejected(tmp_path: Path) -> None:
    plan, plan_dir = make_plan(tmp_path, pcfg={"batch_count": 2})
    batch = plan["batches"][0]
    make_output(tmp_path / "outs" / "b0", batch, MINI)
    make_output(tmp_path / "outs" / "b1", plan["batches"][1], MINI)
    # local dir claiming one of batch-0's cells with a different payload -> conflict
    victim = batch["cell_ids"][0]
    local = make_local_dir(tmp_path / "local", MINI, [victim])
    with pytest.raises(RuntimeError, match="conflicting|duplicate"):
        validate_global(plan_dir, tmp_path / "outs", cfg=MINI, local_dir=local)


# T11/T12/T13 — crash, resume without recomputation, COMPLETE only at end
@pytest.mark.skipif(sys.platform != "win32", reason="crash test uses taskkill")
def test_t11_t12_t13_crash_resume(tmp_path: Path) -> None:
    plan, plan_dir = make_plan(tmp_path, pcfg={"batch_count": 1})
    assert plan["batches"][0]["cell_count"] == 4
    runner = ROOT / "tests" / "i04_cal" / "dist02_runner.py"
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    out = tmp_path / "out"
    proc = subprocess.Popen(
        [sys.executable, str(runner), str(plan_dir), "BATCH-0000", str(out), MINI_CFG_JSON],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        text=True)
    try:
        deadline = time.monotonic() + 300
        durable = {}
        while proc.poll() is None and time.monotonic() < deadline:
            progress = out / "progress.json"
            if progress.exists() and json.loads(progress.read_text())["durable_completed"] >= 2:
                break
            time.sleep(0.25)
        durable = {p.name: p.read_bytes() for p in (out / "ckpt").glob("*.json")}
        assert len(durable) >= 2
        manifest = json.loads((out / "manifest.json").read_text())
        assert manifest["status"] == "INCOMPLETE"  # T13: partial != complete
    finally:
        if proc.poll() is None:
            stopped = subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)],
                                     capture_output=True)
            if stopped.returncode and proc.poll() is None:
                raise AssertionError(stopped.stderr)
        proc.wait(timeout=30)
        proc.stderr.close()
    resumed = subprocess.run(
        [sys.executable, str(runner), str(plan_dir), "BATCH-0000", str(out), MINI_CFG_JSON],
        env=env, capture_output=True, text=True, timeout=900)
    assert resumed.returncode == 0, resumed.stderr
    # T12: previously durable checkpoints byte-identical (not recomputed)
    assert all((out / "ckpt" / name).read_bytes() == blob for name, blob in durable.items())
    assert len(list((out / "ckpt").glob("*.json"))) == 4
    manifest = json.loads((out / "manifest.json").read_text())
    assert manifest["status"] == "COMPLETE" and manifest["completed_cells"] == 4
    # T13: identical to a clean reference execution
    ref = tmp_path / "ref"
    clean = subprocess.run(
        [sys.executable, str(runner), str(plan_dir), "BATCH-0000", str(ref), MINI_CFG_JSON],
        env=env, capture_output=True, text=True, timeout=900)
    assert clean.returncode == 0, clean.stderr
    assert (out / "results.jsonl").read_text() == (ref / "results.jsonl").read_text()


# T16 — sequential independent batches on same runtime
def test_t16_sequential_batches(tmp_path: Path) -> None:
    plan, plan_dir = make_plan(tmp_path, pcfg={"batch_count": 2})
    m0 = run_batch(plan_dir, "BATCH-0000", tmp_path / "o0", cfg=MINI)
    m1 = run_batch(plan_dir, "BATCH-0001", tmp_path / "o1", cfg=MINI)
    assert m0["status"] == m1["status"] == "COMPLETE"
    r0 = {json.loads(l)["cell_key"] for l in (tmp_path / "o0" / "results.jsonl").read_text().splitlines()}
    r1 = {json.loads(l)["cell_key"] for l in (tmp_path / "o1" / "results.jsonl").read_text().splitlines()}
    assert r0 | r1 == set(mini_universe()) and not r0 & r1


# T19 — global validator accepts exactly local + distributed = universe
def test_t19_exact_global_acceptance(tmp_path: Path) -> None:
    universe = mini_universe()
    local_keys, remaining = universe[:2], universe[2:]
    local = make_local_dir(tmp_path / "local", MINI, local_keys)
    plan, plan_dir = make_plan(tmp_path, remaining=remaining, pcfg={"batch_count": 2})
    for i, batch in enumerate(plan["batches"]):
        make_output(tmp_path / "outs" / f"b{i}", batch, MINI)
    report = validate_global(plan_dir, tmp_path / "outs", cfg=MINI, local_dir=local,
                             merge_out=tmp_path / "merged")
    assert report["complete"] is True
    merged = report["merge"]
    assert merged["status"] == "COMPLETE"
    assert merged["completed_cells"] == len(universe) == 4
    rows = [json.loads(l) for l in (tmp_path / "merged" / "results.jsonl").read_text().splitlines()]
    assert [r["cell_key"] for r in rows] == universe


# T20 — no scientific source file modified vs DIST-01 base
def test_t20_scientific_sources_unchanged() -> None:
    protected = [
        "src/quant/i04_cal/assess.py", "src/quant/i04_cal/cache.py",
        "src/quant/i04_cal/distributed.py", "src/quant/i04_cal/gates.py",
        "src/quant/i04_cal/geometries.py", "src/quant/i04_cal/params.py",
        "src/quant/i04_cal/pipeline.py", "src/quant/i04_cal/runtime.py",
        "src/quant/i04_cal/spawn_probe.py", "src/quant/i04_cal/types.py",
        "src/quant/i04_cal/worker.py", "src/quant/i04_cal/worlds.py",
        "src/quant/i04_cal/__init__.py", "src/quant/i04_cal/__main__.py",
    ]
    try:
        diff = subprocess.check_output(
            ["git", "diff", "--name-only", DIST01_HEAD, "HEAD", "--", *protected],
            cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        pytest.skip("git unavailable")
    assert diff == "", f"scientific files modified: {diff}"


# Supplementary: queue status lifecycle
def test_queue_status_classification(tmp_path: Path) -> None:
    plan, plan_dir = make_plan(tmp_path, pcfg={"batch_count": 3})
    make_output(tmp_path / "outs" / "b0", plan["batches"][0], MINI)
    make_output(tmp_path / "outs" / "b1", plan["batches"][1], MINI,
                keys=plan["batches"][1]["cell_ids"][:1], status="INCOMPLETE")
    status = queue_status(plan_dir, tmp_path / "outs", cfg=MINI)
    assert status["batches"]["BATCH-0000"]["status"] == "COMPLETE"
    assert status["batches"]["BATCH-0001"]["status"] == "INCOMPLETE"
    assert status["batches"]["BATCH-0002"]["status"] == "NOT_STARTED"
    assert status["next_available"] == ["BATCH-0002"]


# Supplementary: cost model determinism and heterogeneity
def test_cost_model_properties() -> None:
    assert estimate_cell_cost("S0a|b=0|W=20|G0:default") == 9.0
    assert estimate_cell_cost("S0a|b=0|W=20|G1:gamma=0.1") == 104.0
    assert estimate_cell_cost("S0a|b=0|W=60|G1:gamma=0.1") == 104.0 * 9.0
    assert estimate_cell_cost("S0a|b=0|W=40|G5:p=2,lam=0.001") == 60.0
    assert COST_MODEL_VERSION == "I04-CAL-COST-v1"


# Supplementary: snapshot hash covers identity
def test_snapshot_identity_hash() -> None:
    snap = make_snapshot(MINI, mini_universe())
    h = snapshot_identity_hash(snap)
    snap2 = dict(snap)
    snap2["remaining_ids_hash"] = "1" * 64
    assert snapshot_identity_hash(snap2) != h
