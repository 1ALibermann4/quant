"""
Constructeurs de fixtures C02 v1.1 **exclusivement synthétiques**.

Aucune donnée de marché réelle, aucun calendrier réel : le calendrier est une suite de
jours ouvrés (lundi–vendredi) marquée `SYNTHETIC`, les prix sont une progression
arithmétique, les artefacts « bruts » sont des octets fabriqués ici.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from typing import Any

from quant.contracts.canonical import raw_artifact_set_fingerprint, sha256_fingerprint
from quant.contracts.data_assessment import (
    CheckOutcome,
    CheckResult,
    DataGateAssessment,
    DataVerdict,
)
from quant.contracts.base import DatasetSnapshotRef
from quant.contracts.dataset_snapshot import (
    AdjustmentMethod,
    AdjustmentMethodology,
    AdjustmentReferenceDate,
    ColumnSpec,
    DatasetSnapshot,
    ObservationCounts,
    Provenance,
    SessionRange,
    TableSchema,
    TemporalConvention,
)
from quant.contracts.knowledge import Knowable
from quant.contracts.lineage import (
    InstrumentIdentifiers,
    LicenseRef,
    ProviderArtifact,
    TransformationRecord,
)
from quant.contracts.market_calendar import (
    EarlyClose,
    MarketCalendarSnapshot,
    build_market_calendar,
)

UTC = timezone.utc
NY = "America/New_York"

CAL_FIRST = date(2010, 1, 4)
CAL_LAST = date(2020, 12, 31)
DATA_FIRST = date(2010, 1, 4)
DATA_LAST = date(2020, 6, 30)
EARLY_CLOSE_DAY = date(2019, 7, 3)
MISSING_DAYS = (date(2015, 3, 10), date(2015, 3, 11))
ACQUIRED_AT = datetime(2020, 7, 15, 12, 0, tzinfo=UTC)
AS_OF = datetime(2020, 7, 15, 13, 0, tzinfo=UTC)


def weekdays(first: date, last: date) -> tuple[date, ...]:
    days = []
    d = first
    while d <= last:
        if d.weekday() < 5:
            days.append(d)
        d += timedelta(days=1)
    return tuple(days)


def synthetic_calendar(
    *,
    source: Knowable | None = None,
    source_version: Knowable | None = None,
    first: date = CAL_FIRST,
    last: date = CAL_LAST,
) -> MarketCalendarSnapshot:
    return build_market_calendar(
        calendar_snapshot_id="cal-synthetic-001",
        market="SYNTHETIC",
        timezone=NY,
        source=source or Knowable.known("synthetic-weekday-fixture"),
        source_version=source_version or Knowable.known("test-1"),
        generated_at=datetime(2020, 7, 1, tzinfo=UTC),
        regular_close_local=time(16, 0),
        early_closes=(EarlyClose(session=EARLY_CLOSE_DAY, close_local=time(13, 0)),),
        sessions=weekdays(first, last),
    )


def i01_schema() -> TableSchema:
    return TableSchema(
        schema_id="i01-daily-adjusted",
        schema_version="1.0",
        columns=(
            ColumnSpec(name="session_date", type="date"),
            ColumnSpec(name="adjusted_close", type="decimal", scale=6),
            ColumnSpec(name="close", type="decimal", scale=4, nullable=True),
        ),
        primary_key=("session_date",),
    )


def synthetic_rows(last: date = DATA_LAST) -> list[dict[str, Any]]:
    rows = []
    for i, day in enumerate(weekdays(DATA_FIRST, last)):
        if day in MISSING_DAYS:
            continue
        price = Decimal(100) + Decimal(i) / Decimal(100)
        rows.append({"session_date": day, "adjusted_close": price, "close": price})
    return rows


def synthetic_raw_bytes(last: date = DATA_LAST) -> bytes:
    lines = ["date,close,adjClose"]
    for row in synthetic_rows(last):
        lines.append(f"{row['session_date'].isoformat()}T00:00:00.000Z,{row['close']},"
                     f"{row['adjusted_close']}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def license_ref(**overrides: Any) -> LicenseRef:
    fields: dict[str, Any] = {
        "license_id": "synthetic-license#personal",
        "terms_ref": "fixture://terms",
        "terms_version": Knowable.known("2020-01-01"),
        "plan_tier": Knowable.known("fixture-tier"),
        "usage_basis_ref": Knowable.known("DR-003 ASSUMPTION A-1"),
        "raw_retention_permitted": Knowable.known(True),
        "retention_condition": Knowable.known("while subscription active"),
    }
    fields.update(overrides)
    return LicenseRef(**fields)


def instrument(**overrides: Any) -> InstrumentIdentifiers:
    fields: dict[str, Any] = {
        "ticker": "SYNTH",
        "venue": Knowable.known("SYNTHETIC-VENUE"),
        "isin": Knowable.known("XX0000000000"),
        "cusip": Knowable.unknown(),
        "figi": Knowable.not_applicable(),
        "vendor_permanent_id": Knowable.unknown(),
    }
    fields.update(overrides)
    return InstrumentIdentifiers(**fields)


def artifact(content: bytes | None = None, **overrides: Any) -> ProviderArtifact:
    content = synthetic_raw_bytes() if content is None else content
    fields: dict[str, Any] = {
        "artifact_id": "art-001",
        "provider_id": "synthetic-provider",
        "provider_product": "synthetic-eod",
        "provider_interface": "fixture://eod/prices",
        "provider_interface_version": Knowable.known("v1"),
        "instrument": instrument(),
        "request_parameters": {"startDate": "2010-01-01", "endDate": "2020-06-30", "format": "csv"},
        "requested_first_session": Knowable.known(date(2010, 1, 1)),
        "requested_last_session": Knowable.known(DATA_LAST),
        "acquired_at": ACQUIRED_AT,
        "content_sha256": sha256_fingerprint(content),
        "media_type": "text/csv",
        "encoding": Knowable.known("utf-8"),
        "byte_size": len(content),
        "license": license_ref(),
        "provenance_metadata": {"x-fixture": "true"},
    }
    fields.update(overrides)
    return ProviderArtifact(**fields)


def table_fingerprint(rows: list[dict[str, Any]] | None = None) -> str:
    rows = synthetic_rows() if rows is None else rows
    return sha256_fingerprint(i01_schema().canonical_bytes(rows))


def lineage(
    raw_hash: str, calendar_fp: str, terminal: str, n: int
) -> tuple[TransformationRecord, ...]:
    parsed = sha256_fingerprint(b"synthetic-parsed-intermediate")
    return (
        TransformationRecord(
            step_index=0,
            transformation_id="parse_vendor_csv",
            transformation_type="PARSE",
            implementation_version="0.1.0",
            parameters={"date_rule": "utc_literal_date_part", "columns": ["date", "adjClose", "close"]},
            input_fingerprints=(raw_hash,),
            output_fingerprint=parsed,
            executed_at=datetime(2020, 7, 15, 12, 5, tzinfo=UTC),
            observations_in=Knowable.known(n),
            observations_out=Knowable.known(n),
            observations_dropped=Knowable.known(0),
        ),
        TransformationRecord(
            step_index=1,
            transformation_id="align_to_calendar",
            transformation_type="CALENDAR_ALIGNMENT",
            implementation_version="0.1.0",
            parameters={"fill": "never"},
            input_fingerprints=(parsed, calendar_fp),
            output_fingerprint=terminal,
            executed_at=datetime(2020, 7, 15, 12, 6, tzinfo=UTC),
            observations_in=Knowable.known(n),
            observations_out=Knowable.known(n),
            observations_dropped=Knowable.known(0),
            justification="missing sessions are never filled (DATA-REQ §6)",
        ),
    )


def snapshot_kwargs(
    calendar: MarketCalendarSnapshot | None = None,
    artifacts: tuple[ProviderArtifact, ...] | None = None,
    data_last: date = DATA_LAST,
) -> dict[str, Any]:
    calendar = calendar or synthetic_calendar()
    artifacts = artifacts or (artifact(content=synthetic_raw_bytes(data_last)),)
    rows = synthetic_rows(data_last)
    fingerprint = table_fingerprint(rows)
    raw_hashes = [a.content_sha256 for a in artifacts]
    first_close = calendar.close_instant(DATA_FIRST)
    last_close = calendar.close_instant(data_last)
    n_rows = len(rows)
    expected = calendar.sessions_between(DATA_FIRST, data_last)
    return {
        "snapshot_id": "snap-synthetic-001",
        "fingerprint": fingerprint,
        "as_of": AS_OF,
        "availability_cutoff": last_close,
        "provenance": Provenance(
            source_label="synthetic-provider/synthetic-eod",
            universe_description="single synthetic instrument",
            time_range_start=first_close,
            time_range_end=last_close,
            survivorship_bias_acknowledged=True,
        ),
        "instruments": ["SYNTH"],
        "table_schema": i01_schema(),
        "source_artifacts": tuple(a.ref() for a in artifacts),
        "raw_fingerprint": raw_artifact_set_fingerprint(raw_hashes),
        "lineage": lineage(raw_hashes[0], calendar.content_fingerprint, fingerprint, n_rows),
        "market_calendar": calendar.ref(),
        "temporal_convention": TemporalConvention(
            source_timezone=Knowable.known("UTC"),
            canonical_timezone=NY,
            session_date_rule="take literal YYYY-MM-DD date part; no timezone conversion",
        ),
        "requested_range": Knowable.known(
            SessionRange(first_session=date(2010, 1, 1), last_session=data_last)
        ),
        "returned_range": SessionRange(first_session=DATA_FIRST, last_session=data_last),
        "canonical_range": SessionRange(first_session=DATA_FIRST, last_session=data_last),
        "counts": ObservationCounts(
            raw_observations=n_rows,
            canonical_observations=n_rows,
            expected_sessions=Knowable.known(expected),
            missing_sessions=Knowable.known(expected - n_rows),
            invalidated_sessions=Knowable.known(40),
        ),
        "adjustment_methodology": AdjustmentMethodology(
            events_covered=Knowable.known(("split", "cash_distribution")),
            method=Knowable.known(AdjustmentMethod.PROPORTIONAL),
            reference_date=Knowable.known(AdjustmentReferenceDate.EX_DATE),
            dividend_factor_formula=Knowable.known("(P_prev - D) / P_prev"),
            methodology_ref=Knowable.known("fixture://methodology"),
            methodology_version=Knowable.unknown(),
            numeric_precision=Knowable.known("6 decimals"),
            currency=Knowable.known("USD"),
        ),
        "instrument": instrument(),
        "intended_use": "confirmatory",
    }


def synthetic_snapshot(**overrides: Any) -> DatasetSnapshot:
    kwargs = snapshot_kwargs()
    kwargs.update(overrides)
    return DatasetSnapshot(**kwargs)


def assessment(snapshot: DatasetSnapshot, **overrides: Any) -> DataGateAssessment:
    fields: dict[str, Any] = {
        "assessment_id": "DATA-I01-001-synthetic",
        "snapshot_ref": DatasetSnapshotRef(
            snapshot_id=snapshot.snapshot_id, fingerprint=snapshot.fingerprint
        ),
        "evaluated_against": "DATA-REQ-I01 v0.1",
        "evaluated_at": datetime(2020, 7, 16, tzinfo=UTC),
        "intended_use": snapshot.intended_use,
        "coverage_tier": "CONFIRMATORY",
        "checks": tuple(
            CheckResult(check_id=f"Q-{i:02d}", outcome=CheckOutcome.PASS) for i in range(1, 15)
        ),
        "verdict": DataVerdict.PASS,
    }
    fields.update(overrides)
    return DataGateAssessment(**fields)
