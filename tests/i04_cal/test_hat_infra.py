"""Aggregate assessment + HAT smoke for I04-CAL."""

from __future__ import annotations

import json
import os
from pathlib import Path

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

from quant.i04_cal.assess import write_assessment
from quant.i04_cal.params import CalConfig
from quant.i04_cal.pipeline import run_calibration


def test_hat_deterministic_rerun(tmp_path: Path) -> None:
    cfg = CalConfig(B=1, worlds=("S0a", "S1"), geometries=("G0",), windows=(20,))
    out1 = tmp_path / "a"
    out2 = tmp_path / "b"
    run_calibration(out1, cfg, max_cells=2)
    run_calibration(out2, cfg, max_cells=2)
    r1 = [json.loads(l) for l in (out1 / "results.jsonl").read_text(encoding="utf-8").splitlines() if l]
    r2 = [json.loads(l) for l in (out2 / "results.jsonl").read_text(encoding="utf-8").splitlines() if l]
    assert r1[0]["gates"]["k"]["5"]["CAL_G1_contrast_median"] == r2[0]["gates"]["k"]["5"]["CAL_G1_contrast_median"]


def test_resume_skips_completed(tmp_path: Path) -> None:
    cfg = CalConfig(B=1, worlds=("S0a",), geometries=("G0",), windows=(20, 40))
    out = tmp_path / "r"
    run_calibration(out, cfg, max_cells=1)
    man = run_calibration(out, cfg, resume=True, max_cells=2)
    assert man["n_rows"] >= 2
