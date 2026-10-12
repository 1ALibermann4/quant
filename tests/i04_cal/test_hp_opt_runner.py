"""Tests for bi-machine disjoint split and time-stop (engineering)."""

from __future__ import annotations

import json
from pathlib import Path

from quant.i04_cal.bimachine import canonical_config, split_remaining, write_split
from quant.i04_cal.pipeline import config_hash, expected_cell_ids, run_calibration
from quant.i04_cal.params import CalConfig, QUERY_STRIDE, CANDIDATE_STRIDE, K_NEIGHBORS


def test_bimachine_disjoint_and_coverage() -> None:
    cfg = canonical_config()
    universe = set(expected_cell_ids(cfg))
    assert len(universe) == 12096
    assert config_hash(cfg) == "70e996a15397c91e8db12edee6cadc4e96615fbdf0424811cb7f20eb396ba1f5"
    split = split_remaining(completed=())
    a = set(split["allowlist_a"])
    b = set(split["allowlist_b"])
    assert not (a & b)
    assert a | b == universe
    assert split["manifest"]["n_a"] + split["manifest"]["n_b"] == 12096


def test_bimachine_excludes_completed() -> None:
    cfg = canonical_config()
    keys = expected_cell_ids(cfg)
    done = set(keys[:69])
    split = split_remaining(completed=done)
    a = set(split["allowlist_a"])
    b = set(split["allowlist_b"])
    assert not (a & done)
    assert not (b & done)
    assert a | b == set(keys) - done


def test_write_split_files(tmp_path: Path) -> None:
    man = write_split(tmp_path, completed_run=None)
    assert (tmp_path / "allowlist_ASUS.txt").is_file()
    assert (tmp_path / "allowlist_OPTIPLEX.txt").is_file()
    assert man["config_hash"].startswith("70e996a1")


def test_max_runtime_stops(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("I04_CAL_ALLOW_TEST_OVERRIDES", "1")
    cfg = CalConfig(
        B=1,
        windows=(20,),
        query_stride=QUERY_STRIDE,
        candidate_stride=CANDIDATE_STRIDE,
        k_neighbors=K_NEIGHBORS,
        workers=1,
        worlds=("S0a",),
        geometries=("G0",),
    )
    # Immediate deadline: margin > runtime → stop before any cell if deadline at t0
    man = run_calibration(
        tmp_path / "t",
        cfg,
        resume=False,
        max_cells=1,
        use_cache=True,
        max_runtime_seconds=0.001,
        shutdown_margin_seconds=1.0,
    )
    assert man.get("stopped_for_time") is True
    assert man.get("n_rows", 0) == 0
