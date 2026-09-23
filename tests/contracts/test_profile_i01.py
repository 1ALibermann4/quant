"""Tests du profil C02-I01 v1.0 (exigences DATA-REQ-I01 hors contrat générique)."""

from datetime import date, datetime, timedelta, timezone

import pytest
from c02_synthetic import (
    DATA_LAST,
    artifact,
    assessment,
    instrument,
    license_ref,
    snapshot_kwargs,
    synthetic_calendar,
    synthetic_raw_bytes,
    synthetic_snapshot,
)
from quant.contracts.data_assessment import CheckOutcome, CheckResult, DataVerdict
from quant.contracts.dataset_snapshot import (
    ColumnSpec,
    DatasetSnapshot,
    TableSchema,
    TemporalConvention,
)
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


def test_missing_v11_representations_are_errors():
    """Branches « absent » : P-01, P-02, P-03, P-07, P-10, P-12, P-14–P-18, P-20, P-21."""
    legacy = DatasetSnapshot.model_validate(
        {**synthetic_snapshot().model_dump(
            include={"snapshot_id", "fingerprint", "as_of", "availability_cutoff", "provenance"}
        ), "contract_version": "1.0"}
    )
    errors = run(snapshot=legacy, artifacts=[]).errors
    expected = [
        "contract_version: I01 requires C02 v1.1",
        "table_schema: missing",
        "source_artifacts: missing",
        "instrument: missing",
        "temporal_convention: missing",
        "market_calendar: missing",
        "requested_range: missing",
        "returned_range: missing",
        "canonical_range: missing",
        "counts: missing",
        "adjustment_methodology: missing",
        "lineage: missing",
        "intended_use: must be one of",
    ]
    for prefix in expected:
        assert any(e.startswith(prefix) for e in errors), prefix


def _with_schema(columns):
    return synthetic_snapshot(
        table_schema=TableSchema(schema_id="i01", schema_version="1", columns=columns,
                                 primary_key=("session_date",))
    )


def test_p02_schema_rules():
    date_col = ColumnSpec(name="session_date", type="date")
    adj = ColumnSpec(name="adjusted_close", type="decimal", scale=6)
    cases = {
        "out of I01 scope": (date_col, adj, ColumnSpec(name="open", type="decimal", scale=4)),
        "has type string": (date_col, ColumnSpec(name="adjusted_close", type="string")),
        "required column 'adjusted_close' missing": (date_col,),
        "must not be nullable": (
            date_col, ColumnSpec(name="adjusted_close", type="decimal", scale=6, nullable=True)
        ),
    }
    for message, columns in cases.items():
        assert any(message in e for e in run(snapshot=_with_schema(columns)).errors), message
    wrong_key = synthetic_snapshot(table_schema=TableSchema(
        schema_id="i01", schema_version="1",
        columns=(date_col, adj, ColumnSpec(name="volume", type="integer")),
        primary_key=("session_date", "volume"),
    ))
    assert any("primary key" in e for e in run(snapshot=wrong_key).errors)


def _art_report(**overrides):
    art = artifact(**overrides)
    snap = DatasetSnapshot(**snapshot_kwargs(artifacts=(art,)))
    return run(snapshot=snap, artifacts=[art])


def test_p04_interface_version_not_applicable_is_error():
    report = _art_report(provider_interface_version=Knowable.not_applicable())
    assert any("provider_interface_version: NOT_APPLICABLE" in e for e in report.errors)


def test_p05_usage_basis_unknown_blocking_not_applicable_error():
    unknown = _art_report(license=license_ref(usage_basis_ref=Knowable.unknown()))
    assert unknown.conforms and not unknown.data_pass_eligible
    assert any("usage_basis_ref: UNKNOWN" in b for b in unknown.blocking_unknowns)
    na = _art_report(license=license_ref(usage_basis_ref=Knowable.not_applicable()))
    assert any("usage_basis_ref: NOT_APPLICABLE" in e for e in na.errors)


def test_p07_instrument_rules():
    multi = run(snapshot=synthetic_snapshot(instruments=["SYNTH", "OTHER"]))
    assert any("univariate" in e for e in multi.errors)
    mismatch = _art_report(instrument=instrument(ticker="OTHER"))
    assert any("ticker differs" in e for e in mismatch.errors)


def test_p10_empty_session_date_rule_is_error():
    tc = TemporalConvention(source_timezone=Knowable.known("UTC"),
                            canonical_timezone="America/New_York", session_date_rule="  ")
    assert any("session_date_rule" in e for e in run(snapshot=synthetic_snapshot(
        temporal_convention=tc)).errors)


def test_p11_source_timezone_unknown_blocking_not_applicable_admitted():
    def report(status):
        tc = TemporalConvention(source_timezone=status,
                                canonical_timezone="America/New_York", session_date_rule="r")
        return run(snapshot=synthetic_snapshot(temporal_convention=tc))

    unknown = report(Knowable.unknown())
    assert unknown.conforms and not unknown.data_pass_eligible
    assert any("source_timezone" in b for b in unknown.blocking_unknowns)
    na = report(Knowable.not_applicable(note="dates without instants"))
    assert na.conforms and na.data_pass_eligible


def test_p12_calendar_mismatch_is_error():
    report = run(calendar=synthetic_calendar(last=date(2020, 12, 30)))
    assert any(e.startswith("market_calendar:") for e in report.errors)


def test_p13_calendar_source_unknown_blocking_not_applicable_error():
    for field in ("source", "source_version"):
        cal = synthetic_calendar(**{field: Knowable.not_applicable()})
        report = run(snapshot=DatasetSnapshot(**snapshot_kwargs(calendar=cal)), calendar=cal)
        assert any(f"calendar.{field} (CAL-01): NOT_APPLICABLE" in e for e in report.errors)
    cal = synthetic_calendar(source=Knowable.unknown())
    report = run(snapshot=DatasetSnapshot(**snapshot_kwargs(calendar=cal)), calendar=cal)
    assert report.conforms and any("calendar.source" in b for b in report.blocking_unknowns)


def test_p14_requested_range_unknown_blocking_not_applicable_error():
    unknown = run(snapshot=synthetic_snapshot(requested_range=Knowable.unknown()))
    assert unknown.conforms and "requested_range: UNKNOWN" in unknown.blocking_unknowns
    na = run(snapshot=synthetic_snapshot(requested_range=Knowable.not_applicable()))
    assert any(e.startswith("requested_range: NOT_APPLICABLE") for e in na.errors)


def test_p15_canonical_range_required_even_with_returned_range():
    report = run(snapshot=synthetic_snapshot(canonical_range=None))
    assert "canonical_range: missing" in report.errors


def _counts(**changes):
    counts = snapshot_kwargs()["counts"]
    return type(counts)(**{**dict(counts), **changes})


def test_p16_expected_and_missing_sessions_must_be_known():
    for field in ("expected_sessions", "missing_sessions"):
        report = run(snapshot=synthetic_snapshot(counts=_counts(**{field: Knowable.unknown()})))
        assert any(e.startswith(f"counts.{field}: must be KNOWN") for e in report.errors)


def test_p17_invalidated_sessions_unknown_blocking_not_applicable_error():
    unknown = run(snapshot=synthetic_snapshot(
        counts=_counts(invalidated_sessions=Knowable.unknown())))
    assert unknown.conforms and "counts.invalidated_sessions: UNKNOWN" in unknown.blocking_unknowns
    na = run(snapshot=synthetic_snapshot(
        counts=_counts(invalidated_sessions=Knowable.not_applicable())))
    assert any(e.startswith("counts.invalidated_sessions: NOT_APPLICABLE") for e in na.errors)


@pytest.mark.parametrize(
    "field",
    ["events_covered", "method", "reference_date", "numeric_precision", "currency",
     "methodology_ref"],
)
def test_p18_each_adjustment_field_required(field):
    adj = snapshot_kwargs()["adjustment_methodology"]
    for status, bucket in ((Knowable.unknown(), "blocking"), (Knowable.not_applicable(), "error")):
        snap = synthetic_snapshot(adjustment_methodology=type(adj)(**{**dict(adj), field: status}))
        report = run(snapshot=snap)
        findings = report.blocking_unknowns if bucket == "blocking" else report.errors
        assert any(f"adjustment.{field}" in x for x in findings), (field, bucket)


def test_p19_recommended_fields_only_warn():
    adj = snapshot_kwargs()["adjustment_methodology"]
    snap = synthetic_snapshot(adjustment_methodology=type(adj)(
        **{**dict(adj), "dividend_factor_formula": Knowable.unknown()}))
    report = run(snapshot=snap)
    assert report.data_pass_eligible
    assert any("dividend_factor_formula" in w for w in report.warnings)


def test_p23_provenance_bounds_must_match_session_closes():
    prov = snapshot_kwargs()["provenance"]
    early = type(prov)(**{**dict(prov), "time_range_start": prov.time_range_start - timedelta(hours=1)})
    assert any("time_range_start" in e for e in run(snapshot=synthetic_snapshot(provenance=early)).errors)
    kwargs = snapshot_kwargs()
    late_end = kwargs["availability_cutoff"] - timedelta(minutes=1)
    kwargs["provenance"] = type(prov)(**{**dict(prov), "time_range_end": late_end})
    assert any("time_range_end" in e for e in run(snapshot=DatasetSnapshot(**kwargs)).errors)


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


def test_assessment_below_technical_requires_fail_whatever_the_use():
    short_last = date(2014, 6, 30)
    art = artifact(content=synthetic_raw_bytes(short_last))
    kwargs = snapshot_kwargs(artifacts=(art,), data_last=short_last)
    kwargs["intended_use"] = "technical"
    snap = DatasetSnapshot(**kwargs)

    def check(verdict):
        return validate_i01_snapshot(
            snap, calendar=synthetic_calendar(), artifacts=[art],
            assessment=assessment(snap, coverage_tier="BELOW_TECHNICAL", verdict=verdict),
        )

    passing = check(DataVerdict.PASS)
    assert passing.depth_tier == "BELOW_TECHNICAL"
    assert any("requires FAIL" in e for e in passing.errors)
    assert not any("requires FAIL" in e for e in check(DataVerdict.FAIL).errors)


def test_confirmatory_fixture_ends_at_data_last():
    assert synthetic_snapshot().canonical_range.last_session == DATA_LAST
