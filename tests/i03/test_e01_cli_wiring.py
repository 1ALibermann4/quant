"""I03-E01 CLI operational wiring — workers / checkpoint / resume (no SPY E01)."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from quant.i03.checkpoint import CheckpointStore, RunStatus
from quant.i03.pipeline import run_structural_analysis
from quant.i03.runtime import main as runtime_main


def _fake_canon_returns(T: int = 400) -> tuple[np.ndarray, dict[str, Any]]:
    rng = np.random.default_rng(7)
    r = np.empty(T, dtype=np.float64)
    r[0] = np.nan
    r[1:] = rng.normal(0.0, 0.01, size=T - 1)
    man = {
        "schema": "i03.canonical_input.v1",
        "acquired_at_utc": "2026-09-24T12:00:16.920799+00:00",
        "n_sessions": T,
        "first_session": "1993-01-29",
        "last_session": "1994-01-01",
        "source_snapshot_stem": "ENG-SMOKE",
        "price_payload_sha256": "sha256:" + "aa" * 32,
        "return_payload_sha256": "sha256:"
        + hashlib.sha256(r.tobytes(order="C")).hexdigest(),
        "returns_npy_file_sha256": "sha256:" + "bb" * 32,
        "source_csv_file_sha256": "sha256:" + "cc" * 32,
        "source_meta_file_sha256": "sha256:" + "dd" * 32,
    }
    return r, man


def _patch_canon(monkeypatch: pytest.MonkeyPatch, returns: np.ndarray, man: dict) -> None:
    monkeypatch.setattr(
        "quant.i03.canonical_input.load_canonical_artifact",
        lambda *a, **k: (returns, man),
    )


def _bounded_spy(
    calls: list[dict[str, Any]] | None = None, *, B_n4: int = 2, B_n3: int = 2
):
    def spy(*a, **k):
        if calls is not None:
            calls.append(dict(k))
        os.environ["I03_ALLOW_TEST_OVERRIDES"] = "1"
        return run_structural_analysis(
            a[0],
            a[1],
            B_n4=B_n4,
            B_n3=B_n3,
            compute_locality_on_n4=True,
            workers=k.get("workers", 1),
            checkpoint_dir=k.get("checkpoint_dir"),
            resume=k.get("resume", False),
        )

    return spy


def test_cli_e01_forwards_workers(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    returns, man = _fake_canon_returns()
    _patch_canon(monkeypatch, returns, man)
    calls: list[dict[str, Any]] = []
    monkeypatch.setattr("quant.i03.e01.run_structural_analysis", _bounded_spy(calls))
    rc = runtime_main(
        [
            "--mode",
            "e01",
            "--canonical-dir",
            str(tmp_path / "canon"),
            "--out-dir",
            str(tmp_path / "out"),
            "--workers",
            "4",
        ]
    )
    assert rc == 0
    assert calls[0]["workers"] == 4


def test_cli_e01_forwards_checkpoint_dir(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    returns, man = _fake_canon_returns()
    _patch_canon(monkeypatch, returns, man)
    ck = tmp_path / "ckpt"
    calls: list[dict[str, Any]] = []
    monkeypatch.setattr("quant.i03.e01.run_structural_analysis", _bounded_spy(calls))
    rc = runtime_main(
        [
            "--mode",
            "e01",
            "--canonical-dir",
            str(tmp_path / "canon"),
            "--out-dir",
            str(tmp_path / "out"),
            "--checkpoint-dir",
            str(ck),
        ]
    )
    assert rc == 0
    assert Path(calls[0]["checkpoint_dir"]) == ck
    assert CheckpointStore(ck).status() == RunStatus.COMPLETE


def test_cli_e01_forwards_resume(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    returns, man = _fake_canon_returns()
    _patch_canon(monkeypatch, returns, man)
    ck = tmp_path / "ckpt"
    calls: list[dict[str, Any]] = []
    monkeypatch.setattr("quant.i03.e01.run_structural_analysis", _bounded_spy(calls))

    assert (
        runtime_main(
            [
                "--mode",
                "e01",
                "--canonical-dir",
                str(tmp_path / "canon"),
                "--out-dir",
                str(tmp_path / "out1"),
                "--checkpoint-dir",
                str(ck),
                "--workers",
                "2",
            ]
        )
        == 0
    )

    rc = runtime_main(
        [
            "--mode",
            "e01",
            "--canonical-dir",
            str(tmp_path / "canon"),
            "--out-dir",
            str(tmp_path / "out2"),
            "--checkpoint-dir",
            str(ck),
            "--workers",
            "2",
            "--resume",
        ]
    )
    assert rc == 0
    assert calls[-1].get("resume") is True
    assert Path(calls[-1]["checkpoint_dir"]) == ck


def test_cli_e01_defaults_preserve_serial_no_checkpoint(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    returns, man = _fake_canon_returns()
    _patch_canon(monkeypatch, returns, man)
    calls: list[dict[str, Any]] = []
    monkeypatch.setattr("quant.i03.e01.run_structural_analysis", _bounded_spy(calls))
    rc = runtime_main(
        [
            "--mode",
            "e01",
            "--canonical-dir",
            str(tmp_path / "canon"),
            "--out-dir",
            str(tmp_path / "out"),
        ]
    )
    assert rc == 0
    assert calls[0].get("workers") == 1
    assert calls[0].get("checkpoint_dir") is None
    assert calls[0].get("resume") is False


def test_cli_e01_resume_without_checkpoint_dir_fails(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="--resume requires --checkpoint-dir"):
        runtime_main(
            [
                "--mode",
                "e01",
                "--canonical-dir",
                str(tmp_path / "canon"),
                "--out-dir",
                str(tmp_path / "out"),
                "--resume",
            ]
        )


def test_cli_e01_workers_invalid_fails(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="--workers must be >= 1"):
        runtime_main(
            [
                "--mode",
                "e01",
                "--canonical-dir",
                str(tmp_path / "canon"),
                "--out-dir",
                str(tmp_path / "out"),
                "--workers",
                "0",
            ]
        )


def test_cli_e01_resume_empty_checkpoint_fail_closed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    returns, man = _fake_canon_returns()
    _patch_canon(monkeypatch, returns, man)
    ck = tmp_path / "empty_ckpt"
    ck.mkdir()
    monkeypatch.setattr("quant.i03.e01.run_structural_analysis", _bounded_spy())
    rc = runtime_main(
        [
            "--mode",
            "e01",
            "--canonical-dir",
            str(tmp_path / "canon"),
            "--out-dir",
            str(tmp_path / "out"),
            "--checkpoint-dir",
            str(ck),
            "--resume",
        ]
    )
    assert rc == 2


def test_bounded_cli_smoke_parallel_checkpoint_resume(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """End-to-end through runtime.main: workers>1 + checkpoint + resume.

    Engineering-sized batteries only (via spy reinjecting B overrides).
    No canonical SPY / no scientific E01.
    """
    returns, man = _fake_canon_returns(T=500)
    _patch_canon(monkeypatch, returns, man)
    ck = tmp_path / "smoke_ckpt"
    out1 = tmp_path / "smoke_out1"
    out2 = tmp_path / "smoke_out2"
    calls: list[dict[str, Any]] = []
    monkeypatch.setattr(
        "quant.i03.e01.run_structural_analysis",
        _bounded_spy(calls, B_n4=6, B_n3=4),
    )

    rc1 = runtime_main(
        [
            "--mode",
            "e01",
            "--canonical-dir",
            str(tmp_path / "canon"),
            "--out-dir",
            str(out1),
            "--workers",
            "2",
            "--checkpoint-dir",
            str(ck),
        ]
    )
    assert rc1 == 0
    assert calls[0]["workers"] == 2
    assert Path(calls[0]["checkpoint_dir"]) == ck
    store = CheckpointStore(ck)
    assert store.status() == RunStatus.COMPLETE
    man_ck = store.load_manifest()
    run_id = man_ck["run_id"]
    assert len(store.list_completed("N4", run_id=run_id, B=6)) == 6
    assert len(store.list_completed("N3", run_id=run_id, B=4)) == 4

    art1 = json.loads((out1 / "artifact.json").read_text(encoding="utf-8"))
    assert art1["timing"]["workers_requested"] == 2
    assert art1["timing"]["workers_used"] == 2
    assert art1["execution"]["workers_used"] == 2

    for b in (5, 6):
        (ck / "N4" / f"b_{b:06d}.json").unlink()
    for b in (3, 4):
        (ck / "N3" / f"b_{b:06d}.json").unlink()
    assert (
        store.mark_complete_if_done(run_id=run_id, B_n4=6, B_n3=4) == RunStatus.INCOMPLETE
    )

    rc2 = runtime_main(
        [
            "--mode",
            "e01",
            "--canonical-dir",
            str(tmp_path / "canon"),
            "--out-dir",
            str(out2),
            "--workers",
            "2",
            "--checkpoint-dir",
            str(ck),
            "--resume",
        ]
    )
    assert rc2 == 0
    assert calls[1]["resume"] is True
    assert calls[1]["workers"] == 2
    assert store.status() == RunStatus.COMPLETE
    assert len(store.list_completed("N4", run_id=run_id, B=6)) == 6
    assert len(store.list_completed("N3", run_id=run_id, B=4)) == 4

    art2 = json.loads((out2 / "artifact.json").read_text(encoding="utf-8"))
    assert art2["timing"]["resume"] is True
    assert art2["timing"]["workers_used"] == 2
