"""Regression tests for governance invariants (GOV-I04CAL-001).

These tests enforce that the scientific contract remains compliant with
governance resolutions GOV-01, GOV-02, GOV-03.
"""

from __future__ import annotations

import os

import pytest

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

from quant.i04_cal.params import (
    B_WORLD,
    CANDIDATE_STRIDE,
    EXPENSIVE_CANDIDATE_STRIDE,
    EXPENSIVE_GEOMETRIES,
    EXPENSIVE_QUERY_STRIDE,
    QUERY_STRIDE,
    WINDOWS,
)


def test_gov_01_core_stride_contract():
    """GOV-01: Core geometries must use original frozen contract (8/4)."""
    assert QUERY_STRIDE == 8, f"QUERY_STRIDE must be 8 (GOV-01), got {QUERY_STRIDE}"
    assert CANDIDATE_STRIDE == 4, f"CANDIDATE_STRIDE must be 4 (GOV-01), got {CANDIDATE_STRIDE}"


def test_gov_01_g1_stride_contract():
    """GOV-01: G1 Soft-DTW must use preregistered stride (32/32)."""
    assert EXPENSIVE_QUERY_STRIDE == 32, f"EXPENSIVE_QUERY_STRIDE must be 32 (GOV-01), got {EXPENSIVE_QUERY_STRIDE}"
    assert EXPENSIVE_CANDIDATE_STRIDE == 32, f"EXPENSIVE_CANDIDATE_STRIDE must be 32 (GOV-01), got {EXPENSIVE_CANDIDATE_STRIDE}"
    assert "G1" in EXPENSIVE_GEOMETRIES, "G1 must be in EXPENSIVE_GEOMETRIES (GOV-01)"


def test_gov_01_no_16_16_contract():
    """GOV-01: Ensure 16/16 drift is not active in scientific contract."""
    # Core strides must not be 16
    assert QUERY_STRIDE != 16, "QUERY_STRIDE must not be 16 (drift value from GOV-01 audit)"
    assert CANDIDATE_STRIDE != 16, "CANDIDATE_STRIDE must not be 16 (drift value from GOV-01 audit)"


def test_gov_02_no_automatic_threshold_in_params():
    """GOV-02: Parameters should not contain automatic qualification thresholds."""
    # The old OBSERVABILITY_SPEARMAN_MIN threshold should not exist or be used for qualification
    from quant.i04_cal import params

    # Check that OBSERVABILITY_SPEARMAN_MIN is not defined or is clearly diagnostic-only
    if hasattr(params, "OBSERVABILITY_SPEARMAN_MIN"):
        # If it exists, it should be clearly marked as diagnostic-only
        # This test ensures we don't accidentally introduce automatic qualification
        assert False, "OBSERVABILITY_SPEARMAN_MIN should not exist in params (GOV-02)"


def test_gov_02_assess_reports_distributions():
    """GOV-02: Assessment module should report distributions, not binary verdicts."""
    from quant.i04_cal.assess import assess
    from quant.i04_cal.pipeline import run_calibration
    from quant.i04_cal.params import CalConfig
    import tempfile
    from pathlib import Path

    # Run a tiny calibration
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg = CalConfig(B=1, worlds=("S0a",), geometries=("G0",), windows=(20,))
        out_dir = Path(tmpdir) / "test"
        run_calibration(out_dir, cfg, max_cells=1)

        # Assess should return distributions, not pass/fail based on thresholds
        report = assess(out_dir)

        # Check that report contains distributional data
        assert "distributions" in report, "Assessment must report distributions (GOV-02)"
        assert "C1_S0_contrast" in report["distributions"], "Must report C1 contrast distributions"

        # Check that qualification status is pending governance, not automatic pass/fail
        assert "qualification_status" in report, "Must report qualification status (GOV-02)"
        # The status should not be "CAL-PASS" or "CAL-FAIL" based on automatic thresholds
        # It should be "CALIBRATION DATA COMPLETE" or "CALIBRATION DATA INCOMPLETE"
        assert report["qualification_status"] in [
            "CALIBRATION DATA COMPLETE",
            "CALIBRATION DATA INCOMPLETE",
        ], f"Qualification status should be pending governance, got {report['qualification_status']}"


def test_gov_02_observability_not_automatic():
    """GOV-02: Observability should not automatically VALID/INVALID oracle."""
    from quant.i04_cal.worlds import generate_world

    # S6 and S7 should not have automatic VALID/INVALID based on threshold
    w6 = generate_world("S6", 0)
    w7 = generate_world("S7", 0)

    # Oracle status should be VALID (pending governance evaluation of diagnostic)
    # Not INVALID based on automatic threshold
    from quant.i04_cal.types import OracleStatus

    assert w6.oracle_status == OracleStatus.VALID, "S6 oracle should be VALID pending governance (GOV-02)"
    assert w7.oracle_status == OracleStatus.VALID, "S7 oracle should be VALID pending governance (GOV-02)"

    # Notes should indicate diagnostic-only status
    assert any("diagnostic" in str(note).lower() for note in w6.notes), "S6 notes should mention diagnostic-only (GOV-02)"
    assert any("diagnostic" in str(note).lower() for note in w7.notes), "S7 notes should mention diagnostic-only (GOV-02)"


def test_gov_03_tier_documentation():
    """GOV-03: Execution tiers should be documented as performance-only."""
    from quant.i04_cal.params import CalConfig, DEFAULT_CAL_CONFIG

    # Check that default config has Tier A geometries
    tier_a_geos = {"G0", "G3", "G4", "G7", "GORD"}
    assert set(DEFAULT_CAL_CONFIG.geometries) == tier_a_geos, "Default config should be Tier A (GOV-03)"

    # Check docstring mentions performance-only
    assert "performance" in CalConfig.__doc__.lower(), "CalConfig docstring should mention performance (GOV-03)"
    assert "scientific" in CalConfig.__doc__.lower(), "CalConfig docstring should clarify scientific status (GOV-03)"


def test_gov_03_tier_no_scientific_hierarchy():
    """GOV-03: Tier configuration should not imply scientific hierarchy."""
    from quant.i04_cal.params import CalConfig

    # Config should allow all families when explicitly requested
    # No hardcoded logic that makes Tier A "required" and Tier B "optional"
    all_families = ("G0", "G1", "G2", "G3", "G4", "G5", "G7", "GORD")
    cfg = CalConfig(geometries=all_families)
    assert set(cfg.geometries) == set(all_families), "Should be able to configure all families (GOV-03)"


def test_gov_invariant_checkpoint_includes_restored_config():
    """Checkpoint identity must include the restored scientific configuration."""
    from quant.i04_cal.pipeline import config_hash
    from quant.i04_cal.params import CalConfig

    cfg = CalConfig()
    h = config_hash(cfg)

    # Config hash should include the restored stride values
    # If someone changes strides, hash should change
    cfg2 = CalConfig(query_stride=999)  # Invalid but for testing
    h2 = config_hash(cfg2)
    assert h != h2, "Config hash must depend on stride values (GOV-01)"


def test_gov_invariant_no_best_w():
    """All three windows must remain in configuration."""
    assert WINDOWS == (20, 40, 60), f"WINDOWS must be (20, 40, 60), got {WINDOWS}"


def test_gov_invariant_b_world():
    """B_WORLD must remain 32."""
    assert B_WORLD == 32, f"B_WORLD must be 32, got {B_WORLD}"


def test_gov_spec_governance_history():
    """Specification should document governance history."""
    from pathlib import Path

    spec_path = Path("research/I04/calibration/I04-CAL-SPEC-v0.2.md")
    if spec_path.exists():
        content = spec_path.read_text(encoding="utf-8")
        # Should mention governance history
        assert "GOV-01" in content or "governance" in content.lower(), "Spec should document governance history"
