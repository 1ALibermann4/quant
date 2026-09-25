"""HAT infrastructure unit tests — no full B=999 run."""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pytest

from quant.i03.compare_hat import compare_artifacts
from quant.i03.fixture_hat import (
    FIXTURE_ID,
    FIXTURE_LENGTH,
    FIXTURE_SEED,
    fixture_sha256,
    generate_hat_returns,
    load_fixture,
    write_fixture,
)
from quant.i03.params import DEFAULT_CONFIG
from quant.i03.pipeline import artifact_dict, run_structural_analysis
from quant.i03.report import render_report
from quant.i03.validate_hat import _recon_verdict_independent
from quant.i03.verdict import VerdictLabel


def test_fixture_deterministic_and_hashed(tmp_path: Path) -> None:
    a = generate_hat_returns()
    b = generate_hat_returns()
    assert a.shape == (FIXTURE_LENGTH,)
    assert np.array_equal(a, b, equal_nan=True)
    assert np.isnan(a[0])
    assert np.nanstd(a[1:]) > 0.0
    meta = write_fixture(tmp_path)
    assert meta["fixture_id"] == FIXTURE_ID
    assert meta["seed"] == FIXTURE_SEED
    assert meta["sha256"] == fixture_sha256(a)
    loaded, meta2 = load_fixture(tmp_path)
    assert meta2["sha256"] == meta["sha256"]
    assert np.array_equal(loaded, a, equal_nan=True)


def test_production_path_rejects_overrides_without_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("I03_ALLOW_TEST_OVERRIDES", raising=False)
    r = generate_hat_returns(length=900)
    with pytest.raises(RuntimeError, match="I03_ALLOW_TEST_OVERRIDES"):
        run_structural_analysis(r, DEFAULT_CONFIG, B_n4=2, B_n3=2)


def test_mini_pipeline_artifact_and_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("I03_ALLOW_TEST_OVERRIDES", "1")
    # Short series still needs enough length for P=3 / n_min under default
    # blocks — use full fixture but tiny B for speed.
    r = generate_hat_returns()
    result = run_structural_analysis(
        r,
        DEFAULT_CONFIG,
        B_n4=2,
        B_n3=2,
        compute_locality_on_n4=False,
    )
    art = artifact_dict(
        result,
        input_hash=fixture_sha256(r),
        implementation_id="test",
        mode="SYNTHETIC_HAT",
        fixture_id=FIXTURE_ID,
        timing={"total_seconds": 0.0},
    )
    assert art["schema"] == "I03-ARTIFACT-v1"
    assert art["contract_surface"]["P"] == 3
    assert art["contract_surface"]["tau"] == 20
    assert list(art["config"]["K"]) == [10, 25, 50]
    assert art["n4"]["B_used"] == 2
    assert art["n3"]["method"] == "IAAFT"
    recon_l, recon_nd = _recon_verdict_independent(art)
    assert recon_l == art["verdict"]["label"]
    assert recon_nd == art["verdict"]["nd_code"]
    assert art["verdict"]["label"] in {
        VerdictLabel.PASS.value,
        VerdictLabel.FAIL.value,
        VerdictLabel.INCONCLUSIVE.value,
    }
    report = render_report(art)
    assert "SYNTHETIC HAT" in report
    assert "NOT MARKET EVIDENCE" in report
    assert "NOT SCIENTIFIC EVIDENCE" in report
    # Semantic identity of self
    cmp = compare_artifacts(art, json.loads(json.dumps(art)))
    assert cmp["status"] == "SEMANTIC_IDENTICAL"
    (tmp_path / "artifact.json").write_text(json.dumps(art), encoding="utf-8")


def test_runtime_clears_test_overrides(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Operator path must clear I03_ALLOW_TEST_OVERRIDES before science."""

    from quant.i03 import runtime as rt

    write_fixture(tmp_path)
    out = tmp_path / "out"
    monkeypatch.setenv("I03_ALLOW_TEST_OVERRIDES", "1")

    calls: list[dict] = []

    def fake_run(returns, cfg, **kwargs):
        calls.append({"env": os.environ.get("I03_ALLOW_TEST_OVERRIDES"), "kwargs": kwargs})
        # Minimal stub using real tiny overrides path after clear — env must be gone
        assert os.environ.get("I03_ALLOW_TEST_OVERRIDES") is None
        monkeypatch.setenv("I03_ALLOW_TEST_OVERRIDES", "1")
        return run_structural_analysis(
            returns, cfg, B_n4=1, B_n3=1, compute_locality_on_n4=False
        )

    monkeypatch.setattr(rt, "run_structural_analysis", fake_run)
    rc = rt.main(
        [
            "--mode",
            "hat",
            "--fixture-dir",
            str(tmp_path),
            "--out-dir",
            str(out),
        ]
    )
    assert rc == 0
    assert calls and calls[0]["env"] is None
    assert (out / "artifact.json").exists()
    assert (out / "report.md").exists()