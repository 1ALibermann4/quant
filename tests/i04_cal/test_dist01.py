from __future__ import annotations

import json
import os
import signal
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

from quant.i04_cal.distributed import (
    canonical_config,
    digest,
    load_shard,
    merge,
    plan_shards,
    run_shard,
    save_plan,
    scientific_identity,
)
from quant.i04_cal.pipeline import _record_hash, expected_cell_ids


def test_plan_full_universe_balanced_and_reproducible() -> None:
    cfg = canonical_config()
    ids = expected_cell_ids(cfg)
    assert len(ids) == 12096
    a = plan_shards(cfg, "TEST-FULL", 32, ids)
    b = plan_shards(cfg, "TEST-FULL", 32, ids)
    assert a["universe_hash"] == scientific_identity(cfg)["universe_hash"]
    assert [shard["cell_ids"] for shard in a["shards"]] == [shard["cell_ids"] for shard in b["shards"]]
    assert max(shard["cell_count"] for shard in a["shards"]) - min(shard["cell_count"] for shard in a["shards"]) <= 1
    assert len({key for shard in a["shards"] for key in shard["cell_ids"]}) == len(ids)
    for family in ("G0", "G1", "G2", "G3", "G4", "G5", "G7", "GORD"):
        counts = [sum(f"|{family}:" in key for key in shard["cell_ids"]) for shard in a["shards"]]
        assert max(counts) - min(counts) <= 1
    with pytest.raises(ValueError):
        plan_shards(cfg, "TEST-FULL", 3, [ids[0], ids[0], ids[1]])
    with pytest.raises(ValueError):
        plan_shards(cfg, "TEST-FULL", 3, [ids[0], ids[1]])


def test_three_shard_execution_and_fail_closed_merge(tmp_path: Path) -> None:
    cfg = canonical_config()
    ids = expected_cell_ids(cfg)
    subset = [key for key in ids if key in {
        "S0a|b=0|W=20|G0:default", "S0a|b=1|W=20|G0:default", "S0b|b=0|W=20|G0:default"
    }]
    plan = plan_shards(cfg, "TEST-MERGE", 3, subset)
    plan_dir = tmp_path / "plan"
    save_plan(plan_dir, plan)
    results = []
    for i in range(3):
        shard = load_shard(plan_dir / f"shard-{i:05d}.json", cfg)
        assert shard["cell_count"] == 1
        out = tmp_path / f"result-{i}"
        manifest = run_shard(plan_dir / f"shard-{i:05d}.json", out, workers=1, cfg=cfg)
        assert manifest["status"] == "COMPLETE"
        assert len(list((out / "ckpt").glob("*.json"))) == 1
        telemetry = json.loads(next((out / "timings").glob("*.json")).read_text(encoding="utf-8"))
        assert telemetry["cell_id"] == shard["cell_ids"][0]
        assert telemetry["wall_duration_s"] > 0
        assert telemetry["host_id"] and telemetry["worker_pid"] and telemetry["finished_at"]
        assert json.loads((out / "progress.json").read_text(encoding="utf-8"))["durable_completed"] == 1
        results.append(out)
    merged = merge(plan_dir, results, tmp_path / "merged", cfg=cfg)
    assert merged["completed_cells"] == 3
    rows = [json.loads(line) for line in (tmp_path / "merged" / "results.jsonl").read_text(encoding="utf-8").splitlines()]
    assert [row["cell_key"] for row in rows] == subset
    with pytest.raises(RuntimeError, match="missing/unexpected"):
        merge(plan_dir, results[:2], tmp_path / "missing", cfg=cfg)
    with pytest.raises(RuntimeError, match="duplicate"):
        merge(plan_dir, results + results[:1], tmp_path / "duplicate", cfg=cfg)
    with pytest.raises(RuntimeError, match="duplicate"):
        merge(plan_dir, results, tmp_path / "duplicate_repro", cfg=cfg, repro_dirs=results[:1], allow_identical_duplicates=False)
    assert merge(plan_dir, results, tmp_path / "identical", cfg=cfg,
                 repro_dirs=results[:1], allow_identical_duplicates=True)["identical_duplicates"] == 1
    conflict = tmp_path / "conflict_shard"
    shutil.copytree(results[0], conflict)
    checkpoint = next((conflict / "ckpt").glob("*.json"))
    row = json.loads(checkpoint.read_text(encoding="utf-8"))
    row["seed"] += 1
    row["record_hash"] = _record_hash(row)
    checkpoint.write_text(json.dumps(row), encoding="utf-8")
    with pytest.raises(RuntimeError, match="duplicate/conflicting"):
        merge(plan_dir, results, tmp_path / "conflicting", cfg=cfg,
              repro_dirs=[conflict], allow_identical_duplicates=True)
    wrong_config = tmp_path / "wrong_config"
    shutil.copytree(results[0], wrong_config)
    manifest_path = wrong_config / "manifest.json"
    bad = json.loads(manifest_path.read_text(encoding="utf-8"))
    bad["config_hash"] = "invalid"
    manifest_path.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(RuntimeError, match="scientific identity"):
        merge(plan_dir, [wrong_config, *results[1:]], tmp_path / "bad_config", cfg=cfg)
    bad["config_hash"] = scientific_identity(cfg)["config_hash"]
    bad["universe_hash"] = "invalid"
    manifest_path.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(RuntimeError, match="scientific identity"):
        merge(plan_dir, [wrong_config, *results[1:]], tmp_path / "bad_universe", cfg=cfg)


def test_shard_abrupt_crash_resume_without_recomputation(tmp_path: Path) -> None:
    cfg = canonical_config()
    chosen = [key for key in expected_cell_ids(cfg)
              if key in {f"S0a|b={b}|W={W}|G0:default" for b in (0, 1, 2, 3) for W in (20, 40)}]
    plan_dir = tmp_path / "plan"
    save_plan(plan_dir, plan_shards(cfg, "TEST-CRASH", 1, chosen))
    shard = plan_dir / "shard-00000.json"
    out = tmp_path / "interrupted"
    runner = Path(__file__).with_name("dist01_runner.py")
    env = {**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[2] / "src")}
    proc = subprocess.Popen([sys.executable, str(runner), str(shard), str(out), "4", "0"],
                            env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                            start_new_session=sys.platform != "win32", text=True)
    try:
        deadline = time.monotonic() + 300
        while proc.poll() is None and time.monotonic() < deadline:
            progress = out / "progress.json"
            if progress.exists() and json.loads(progress.read_text(encoding="utf-8"))["durable_completed"] >= 2:
                break
            time.sleep(0.25)
        durable = {p.name: p.stat().st_mtime_ns for p in (out / "ckpt").glob("*.json")}
        assert 2 <= len(durable) < len(chosen)
        assert len(list((out / "timings").glob("*.json"))) >= len(durable)
    finally:
        if proc.poll() is None:
            if sys.platform == "win32":
                stopped = subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
                if stopped.returncode and proc.poll() is None:
                    raise AssertionError(stopped.stderr)
            else:
                os.killpg(proc.pid, signal.SIGKILL)
        proc.wait(timeout=30)
        proc.stderr.close()
    resumed = subprocess.run([sys.executable, str(runner), str(shard), str(out), "1", "1"],
                             env=env, capture_output=True, text=True, timeout=900)
    assert resumed.returncode == 0, resumed.stderr
    assert all((out / "ckpt" / name).stat().st_mtime_ns == mtime for name, mtime in durable.items())
    assert len(list((out / "ckpt").glob("*.json"))) == len(chosen)
    ref = tmp_path / "reference"
    reference = subprocess.run([sys.executable, str(runner), str(shard), str(ref), "1", "0"],
                               env=env, capture_output=True, text=True, timeout=900)
    assert reference.returncode == 0, reference.stderr
    assert (out / "results.jsonl").read_text(encoding="utf-8") == (ref / "results.jsonl").read_text(encoding="utf-8")
