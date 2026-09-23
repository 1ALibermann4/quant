"""Tests du profil C02-I01 v1.0 (exigences DATA-REQ-I01 hors contrat générique)."""

from datetime import date, datetime, timezone

import pytest
from c02_synthetic import (
    DATA_LAST,
    artifact,
    assessment,
    license_ref,
    snapshot_kwargs,
    synthetic_calendar,
    synthetic_raw_bytes,
    synthetic_snapshot,
)
from quant.contracts.data_assessment import CheckOutcome, CheckResult, DataVerdict
from quant.contracts.dataset_snapshot import DatasetSnapshot, TemporalConvention
from quant.contracts.knowledge import Knowable
from quant.contracts.profiles.i01 import i01_depth_tier, validate_i01_snapshot

UTC = timezone.utc


def run(snapshot=None, calendar=None, artifacts=None, gate=None):
    snapshot = snapshot or synthetic_snapshot()
    return validate_i01_snapshot(
        snapshot,
        calendar=calendar or synthetic_calendar(),
        artifacts=artifacts if artifacts is not None else [artifact()],
        assessment=gate,
    )


def test_complete_synthetic_snapshot_conforms_and_is_eligible():
    report = run()
    assert report.errors == ()
    assert report.blocking_unknowns == ()
    assert report.conforms and report.data_pass_eligible
    assert report.depth_tier == "CONFIRMATORY"
    assert any("methodology_version" in w for w in report.warnings)


def test_generic_v10_snapshot_is_valid_c02_but_not_i01(sample_snapshot):
    report = run(snapshot=sample_snapshot)
    assert not report.conforms
    assert any("table_schema" in e for e in report.errors)
    assert any("lineage" in e for e in report.errors)


def test_unknown_interface_version_is_blocking_not_error():
    art = artifact(provider_interface_version=Knowable.unknown(note="DR-003 PA-14"))
    snap = DatasetSnapshot(**snapshot_kwargs(artifacts=(art,)))
    report = run(snapshot=snap, artifacts=[art])
    assert report.conforms
    assert not report.data_pass_eligible
    assert any("provider_interface_version" in b for b in report.blocking_unknowns)


def test_retention_forbidden_is_error_unknown_is_blocking():
    forbidden = artifact(license=license_ref(raw_retention_permitted=Knowable.known(False)))
    snap = DatasetSnapshot(**snapshot_kwargs(artifacts=(forbidden,)))
    assert any("REP-05" in e for e in run(snapshot=snap, artifacts=[forbidden]).errors)

    unknown = artifact(license=license_ref(raw_retention_permitted=Knowable.unknown()))
    snap = DatasetSnapshot(**snapshot_kwargs(artifacts=(unknown,)))
    report = run(snapshot=snap, artifacts=[unknown])
    assert report.conforms and not report.data_pass_eligible


def test_unversioned_calendar_is_blocking():
    cal = synthetic_calendar(source_version=Knowable.unknown())
    snap = DatasetSnapshot(**snapshot_kwargs(calendar=cal))
    report = run(snapshot=snap, calendar=cal)
    assert any("source_version" in b for b in report.blocking_unknowns)


def test_unknown_adjustment_method_is_blocking_not_applicable_is_error():
    kwargs = snapshot_kwargs()
    adj = kwargs["adjustment_methodology"]
    kwargs["adjustment_methodology"] = type(adj)(
        **{**adj.model_dump(), "method": Knowable.unknown()}
    )
    report = run(snapshot=DatasetSnapshot(**kwargs))
    assert any("adjustment.method" in b for b in report.blocking_unknowns)
    kwargs["adjustment_methodology"] = type(adj)(
        **{**adj.model_dump(), "currency": Knowable.not_applicable()}
    )
    report = run(snapshot=DatasetSnapshot(**kwargs))
    assert any("adjustment.currency" in e for e in report.errors)


def test_wrong_canonical_timezone_is_error():
    kwargs = snapshot_kwargs()
    kwargs["temporal_convention"] = TemporalConvention(
        source_timezone=Knowable.known("UTC"),
        canonical_timezone="UTC",
        session_date_rule="literal",
    )
    report = run(snapshot=DatasetSnapshot(**kwargs))
    assert any("canonical timezone" in e for e in report.errors)


def test_availability_cutoff_must_be_last_session_close():
    kwargs = snapshot_kwargs()
    kwargs["availability_cutoff"] = datetime(2020, 6, 30, 16, 0, tzinfo=UTC)
    report = run(snapshot=DatasetSnapshot(**kwargs))
    assert any("availability_cutoff" in e for e in report.errors)


def test_missing_venue_or_identifiers_are_blocking():
    kwargs = snapshot_kwargs()
    inst = kwargs["instrument"]
    kwargs["instrument"] = type(inst)(
        **{**inst.model_dump(), "isin": Knowable.unknown(), "venue": Knowable.unknown()}
    )
    report = run(snapshot=DatasetSnapshot(**kwargs))
    assert any("venue" in b for b in report.blocking_unknowns)
    assert any("ISIN/CUSIP/FIGI" in b for b in report.blocking_unknowns)


def test_intended_use_required():
    report = run(snapshot=synthetic_snapshot(intended_use=None))
    assert any("intended_use" in e for e in report.errors)


def test_rev_d_04_warning_when_acquired_too_close():
    late = artifact(acquired_at=datetime(2020, 7, 2, 12, 0, tzinfo=UTC))
    snap = DatasetSnapshot(**snapshot_kwargs(artifacts=(late,)))
    report = run(snapshot=snap, artifacts=[late])
    assert report.conforms
    assert any("REV-D-04" in w for w in report.warnings)


def test_wrong_artifacts_supplied_is_error():
    report = run(artifacts=[artifact(content=b"other")])
    assert any("source_artifacts" in e for e in report.errors)


# ------------------------------------------------------------------ paliers de profondeur


@pytest.mark.parametrize(
    ("sessions", "first", "last", "tier"),
    [
        (1499, date(2000, 1, 3), date(2020, 1, 3), "BELOW_TECHNICAL"),
        (1500, date(2014, 1, 2), date(2020, 1, 2), "TECHNICAL"),
        (2520, date(2010, 1, 4), date(2020, 1, 3), "TECHNICAL"),
        (2520, date(2010, 1, 4), date(2020, 1, 4), "CONFIRMATORY"),
        (3780, date(2005, 1, 3), date(2020, 1, 2), "CONFIRMATORY"),
        (3780, date(2005, 1, 3), date(2020, 1, 3), "PREFERRED"),
        (2400, date(1990, 1, 2), date(2020, 1, 2), "TECHNICAL"),
    ],
)
def test_depth_tier(sessions, first, last, tier):
    assert i01_depth_tier(sessions, first, last) == tier


def test_depth_tier_leap_day_anniversary():
    assert i01_depth_tier(2520, date(2008, 2, 29), date(2018, 2, 28)) == "CONFIRMATORY"
    assert i01_depth_tier(2520, date(2008, 2, 29), date(2018, 2, 27)) == "TECHNICAL"


# ------------------------------------------------------------------ DataGateAssessment


def test_consistent_assessment_passes_profile():
    snap = synthetic_snapshot()
    report = run(snapshot=snap, gate=assessment(snap))
    assert report.errors == ()


def test_assessment_must_reference_snapshot_and_cover_q01_q14():
    snap = synthetic_snapshot()
    from quant.contracts.base import DatasetSnapshotRef

    wrong_ref = assessment(snap, snapshot_ref=DatasetSnapshotRef(snapshot_id="x", fingerprint="y"))
    assert any("snapshot_ref" in e for e in run(snapshot=snap, gate=wrong_ref).errors)
    partial = assessment(snap, checks=(CheckResult(check_id="Q-01", outcome=CheckOutcome.PASS),))
    assert any("Q-01..Q-14" in e for e in run(snapshot=snap, gate=partial).errors)


def test_assessment_tier_and_intended_use_consistency():
    snap = synthetic_snapshot()
    wrong_tier = assessment(snap, coverage_tier="PREFERRED")
    assert any("coverage_tier" in e for e in run(snapshot=snap, gate=wrong_tier).errors)
    wrong_use = assessment(snap, intended_use="technical")
    assert any("intended_use" in e for e in run(snapshot=snap, gate=wrong_use).errors)


def test_data_pass_forbidden_with_blocking_unknowns():
    art = artifact(provider_interface_version=Knowable.unknown())
    snap = DatasetSnapshot(**snapshot_kwargs(artifacts=(art,)))
    report = run(snapshot=snap, artifacts=[art], gate=assessment(snap))
    assert any("DATA-PASS with profile errors or blocking unknowns" in e for e in report.errors)
    ok = run(snapshot=snap, artifacts=[art],
             gate=assessment(snap, verdict=DataVerdict.INCONCLUSIVE))
    assert not any("DATA-PASS" in e for e in ok.errors)


def test_assessment_generic_verdict_rules():
    snap = synthetic_snapshot()
    checks = list(assessment(snap).checks)
    checks[0] = CheckResult(check_id="Q-01", outcome=CheckOutcome.REJECT)
    with pytest.raises(ValueError, match="REJECT"):
        assessment(snap, checks=tuple(checks), verdict=DataVerdict.INCONCLUSIVE)
    checks[0] = CheckResult(check_id="Q-01", outcome=CheckOutcome.INCONCLUSIVE)
    with pytest.raises(ValueError, match="INCONCLUSIVE"):
        assessment(snap, checks=tuple(checks), verdict=DataVerdict.PASS)


def test_assessment_confirmatory_on_technical_tier_requires_fail():
    short_last = date(2016, 6, 30)
    art = artifact(content=synthetic_raw_bytes(short_last))
    snap = DatasetSnapshot(**snapshot_kwargs(artifacts=(art,), data_last=short_last))
    assert snap.intended_use == "confirmatory"

    def check(verdict):
        return validate_i01_snapshot(
            snap,
            calendar=synthetic_calendar(),
            artifacts=[art],
            assessment=assessment(snap, coverage_tier="TECHNICAL", verdict=verdict),
        )

    passing = check(DataVerdict.PASS)
    assert passing.depth_tier == "TECHNICAL"
    assert any("requires FAIL" in e for e in passing.errors)
    assert not any("requires FAIL" in e for e in check(DataVerdict.FAIL).errors)


def test_confirmatory_fixture_ends_at_data_last():
    assert synthetic_snapshot().canonical_range.last_session == DATA_LAST
