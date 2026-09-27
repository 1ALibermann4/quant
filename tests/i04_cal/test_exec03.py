from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from quant.i04_cal.params import CalConfig, gate_seed
from quant.i04_cal.pipeline import config_hash, expected_cell_ids, run_calibration

ROOT = Path(__file__).resolve().parents[2]
RUNNER = Path(__file__).with_name("exec03_runner.py")
VECTORS = [
    (("S0a", 0, 20, "G0", "default", "CAL"), 1727443771),
    (("S1", 7, 40, "G1", "gamma=0.1", "CAL"), 42257716),
    (("S7", 31, 60, "GORD", "D=4,tau=1", "CAL"), 1236980653),
    (("S6", 3, 20, "G5", "p=2,lam=0.001", "CAL_G4"), 57051067),
]


def _rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in (path / "results.jsonl").read_text(encoding="utf-8").splitlines()]


def test_frozen_universe() -> None:
    cfg = CalConfig(geometries=("G0", "G1", "G2", "G3", "G4", "G5", "G7", "GORD"))
    ids = expected_cell_ids(cfg)
    assert len(ids) == len(set(ids)) == 12096


def test_golden_seeds_across_interpreters() -> None:
    assert [gate_seed(*args) for args, _ in VECTORS] == [value for _, value in VECTORS]
    code = "from quant.i04_cal.params import gate_seed; print(gate_seed('S1',7,40,'G1','gamma=0.1'))"
    for hashseed in ("0", "1", "9173", "random"):
        env = {**os.environ, "PYTHONHASHSEED": hashseed, "PYTHONPATH": str(ROOT / "src")}
        output = subprocess.check_output([sys.executable, "-c", code], env=env, cwd=ROOT, text=True)
        assert int(output.strip()) == 42257716


def test_partial_write_recovery_and_identity(tmp_path: Path) -> None:
    cfg = CalConfig(B=1, windows=(20,), worlds=("S0a",), geometries=("G0",))
    out = tmp_path / "partial"
    assert run_calibration(out, cfg)["status"] == "COMPLETE"
    original = _rows(out)
    assert len(original) == 1
    with (out / "results.jsonl").open("ab") as f:
        f.write(b'{"cell_key":"torn"')
    assert run_calibration(out, cfg, resume=True)["status"] == "COMPLETE"
    assert _rows(out) == original
    assert len(list((out / "ckpt").glob("*.json"))) == 1
    with pytest.raises(RuntimeError, match="identity mismatch"):
        run_calibration(out, CalConfig(B=1, windows=(40,), worlds=("S0a",), geometries=("G0",)), resume=True)
    with pytest.raises(RuntimeError, match="identity mismatch"):
        run_calibration(out, CalConfig(B=1, windows=(20,), worlds=("S0a",), geometries=("G1",)), resume=True)
    assert config_hash(cfg) == config_hash(CalConfig(B=1, windows=(20,), worlds=("S0a",), geometries=("G0",), workers=4))
    assert json.loads((out / "progress.json").read_text(encoding="utf-8"))["completed_cells"] == 1
    checkpoint = next((out / "ckpt").glob("*.json"))
    tampered = json.loads(checkpoint.read_text(encoding="utf-8"))
    tampered["seed"] = 987654
    checkpoint.write_text(json.dumps(tampered), encoding="utf-8")
    with pytest.raises(RuntimeError, match="invalid/duplicate checkpoint"):
        run_calibration(out, cfg, resume=True)


def test_worker_failure_persists_diagnostics(tmp_path: Path) -> None:
    cfg = CalConfig(B=1, windows=(20,), worlds=("S0a", "UNKNOWN"), geometries=("G0",), workers=2)
    out = tmp_path / "failure"
    result = run_calibration(out, cfg)
    assert result["status"] == "FAILED_TECHNICAL"
    assert result["n_rows"] == 1
    assert len(list((out / "ckpt").glob("*.json"))) == 1
    failures = json.loads((out / "technical_failures.json").read_text(encoding="utf-8"))["failures"]
    assert len(failures) == 1 and failures[0]["cell_key"].startswith("UNKNOWN|")
    assert failures[0]["traceback"]


def _stop_tree(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    if sys.platform == "win32":
        result = subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True, text=True)
        if result.returncode and proc.poll() is None:
            raise AssertionError(f"test process tree termination failed: {result.stdout} {result.stderr}")
    else:
        proc.kill()
    proc.wait(timeout=30)


@pytest.mark.parametrize("first,second", [(4, 1), (1, 4)])
def test_abrupt_crash_cross_worker_resume(tmp_path: Path, first: int, second: int) -> None:
    out = tmp_path / "crash"
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    proc = subprocess.Popen([sys.executable, str(RUNNER), str(out), str(first), "0"], cwd=ROOT, env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    try:
        deadline = time.monotonic() + 300
        while time.monotonic() < deadline and proc.poll() is None:
            progress_path = out / "progress.json"
            if progress_path.exists() and json.loads(progress_path.read_text(encoding="utf-8"))["completed_cells"] >= 2:
                break
            time.sleep(0.2)
        n = len(list((out / "ckpt").glob("*.json")))
        assert 2 <= n < 8, f"durable before crash: {n}; process exit={proc.poll()}"
        progress = json.loads((out / "progress.json").read_text(encoding="utf-8"))
        assert progress["expected_cells"] == 8
        assert 2 <= progress["completed_cells"] <= n
    finally:
        _stop_tree(proc)
        proc.stderr.close()
    before = {row["cell_key"]: row for row in _rows(out)}
    checkpoint_mtimes = {p.name: p.stat().st_mtime_ns for p in (out / "ckpt").glob("*.json")}
    assert len(before) >= 2
    print(f"EXEC03_CRASH workers={first}->{second} durable={len(checkpoint_mtimes)} results={len(before)}")
    completed = subprocess.run([sys.executable, str(RUNNER), str(out), str(second), "1"], cwd=ROOT, env=env,
                               capture_output=True, text=True, timeout=900)
    assert completed.returncode == 0, completed.stderr
    final = _rows(out)
    assert len(final) == len({r["cell_key"] for r in final}) == 8
    assert all(row in final for row in before.values())
    assert len(list((out / "ckpt").glob("*.json"))) == 8
    assert all((out / "ckpt" / name).stat().st_mtime_ns == mtime for name, mtime in checkpoint_mtimes.items())
    assert json.loads((out / "manifest.json").read_text(encoding="utf-8"))["status"] == "COMPLETE"
    reference = tmp_path / "reference"
    ref = subprocess.run([sys.executable, str(RUNNER), str(reference), "1", "0"], cwd=ROOT, env=env,
                         capture_output=True, text=True, timeout=900)
    assert ref.returncode == 0, ref.stderr
    assert final == _rows(reference)
