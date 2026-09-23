"""Tests C02 — DatasetSnapshot (v1.0 conservé, extensions v1.1)."""

from datetime import date, datetime, timedelta, timezone

import pytest
from c02_synthetic import (
    artifact,
    snapshot_kwargs,
    synthetic_calendar,
    synthetic_rows,
    synthetic_snapshot,
)
from pydantic import ValidationError

from quant.contracts.base import DatasetSnapshotRef
from quant.contracts.canonical import sha256_fingerprint
from quant.contracts.dataset_snapshot import (
    DatasetSnapshot,
    Provenance,
    SessionRange,
    TemporalConvention,
)
from quant.contracts.knowledge import Knowable
from quant.contracts.market_state import MarketState

UTC = timezone.utc
T = datetime(2024, 1, 15, tzinfo=UTC)


def v10_payload(**overrides):
    payload = {
        "contract_id": "C02",
        "contract_version": "1.0",
        "snapshot_id": "legacy-001",
        "fingerprint": "sha256:abc123",
        "as_of": "2024-01-15T16:00:00Z",
        "availability_cutoff": "2024-01-15T16:00:00Z",
        "provenance": {
            "source_label": "fixture",
            "universe_description": "TEST_UNIVERSE",
            "time_range_start": "2023-01-01T00:00:00Z",
            "time_range_end": "2024-01-15T00:00:00Z",
            "survivorship_bias_acknowledged": True,
        },
        "instruments": ["X"],
        "adjustments": [
            {"type": "split", "description": "2:1", "applied_at": "2023-06-01T00:00:00Z"}
        ],
        "quality_flags": ["WARN:x"],
        "storage_hint": "csv",
    }
    payload.update(overrides)
    return payload


# ------------------------------------------------------------------ v1.0 (conservé)


def test_snapshot_valid(sample_snapshot):
    assert sample_snapshot.contract_id == "C02"
    assert sample_snapshot.fingerprint.startswith("sha256:")


def test_availability_cutoff_after_as_of_rejected():
    t = datetime(2024, 1, 15, tzinfo=UTC)
    with pytest.raises(ValueError, match="availability_cutoff"):
        DatasetSnapshot(
            snapshot_id="bad",
            fingerprint="sha256:x",
            as_of=t,
            availability_cutoff=datetime(2024, 1, 16, tzinfo=UTC),
            provenance=Provenance(
                source_label="x",
                universe_description="u",
                time_range_start=datetime(2023, 1, 1, tzinfo=UTC),
                time_range_end=t,
                survivorship_bias_acknowledged=False,
            ),
        )


def test_invalid_time_range():
    t = datetime(2024, 1, 15, tzinfo=UTC)
    with pytest.raises(ValueError, match="time_range"):
        DatasetSnapshot(
            snapshot_id="bad",
            fingerprint="sha256:x",
            as_of=t,
            availability_cutoff=t,
            provenance=Provenance(
                source_label="x",
                universe_description="u",
                time_range_start=t,
                time_range_end=t,
                survivorship_bias_acknowledged=False,
            ),
        )


# ------------------------------------------------------------------ DATA-GAP-02 (erratum E-01)


def test_erratum_e01_cutoff_equal_to_as_of_is_valid():
    snap = DatasetSnapshot.model_validate(v10_payload())
    assert snap.availability_cutoff == snap.as_of


def test_erratum_e01_cutoff_before_as_of_is_valid():
    snap = DatasetSnapshot.model_validate(
        v10_payload(availability_cutoff="2024-01-12T21:00:00Z")
    )
    assert snap.availability_cutoff < snap.as_of


def test_erratum_e01_cutoff_after_as_of_is_rejected():
    with pytest.raises(ValidationError, match="availability_cutoff must be <= as_of"):
        DatasetSnapshot.model_validate(v10_payload(availability_cutoff="2024-01-16T00:00:00Z"))


def test_cutoff_chain_compatible_with_market_state(sample_snapshot):
    """C03 : MarketState.as_of <= availability_cutoff <= DatasetSnapshot.as_of."""
    ref = DatasetSnapshotRef(
        snapshot_id=sample_snapshot.snapshot_id, fingerprint=sample_snapshot.fingerprint
    )
    ms = MarketState(market_state_id="ms", as_of=sample_snapshot.availability_cutoff,
                     dataset_snapshot_ref=ref)
    ms.assert_temporal_integrity(sample_snapshot.availability_cutoff)
    late = MarketState(market_state_id="ms2",
                       as_of=sample_snapshot.availability_cutoff + timedelta(seconds=1),
                       dataset_snapshot_ref=ref)
    with pytest.raises(ValueError, match="exceeds"):
        late.assert_temporal_integrity(sample_snapshot.availability_cutoff)


# ------------------------------------------------------------------ rétrocompatibilité


def test_v10_serialized_object_still_valid():
    snap = DatasetSnapshot.model_validate(v10_payload())
    assert snap.contract_version == "1.0"
    assert snap.fingerprint == "sha256:abc123"
    assert snap.table_schema is None and snap.source_artifacts == () and snap.lineage == ()


def test_v10_roundtrip_preserves_v10_fields():
    snap = DatasetSnapshot.model_validate(v10_payload())
    again = DatasetSnapshot.model_validate(snap.model_dump(mode="json"))
    assert again == snap


def test_v10_object_cannot_carry_v11_fields():
    with pytest.raises(ValidationError, match="must not carry v1.1 fields"):
        DatasetSnapshot.model_validate(v10_payload(intended_use="technical"))


def test_unsupported_contract_version_rejected():
    with pytest.raises(ValidationError, match="unsupported C02 contract_version"):
        DatasetSnapshot.model_validate(v10_payload(contract_version="2.0"))


def test_default_version_is_v11_and_v10_fields_only_is_valid(sample_snapshot):
    assert sample_snapshot.contract_version == "1.1"
    assert sample_snapshot.table_schema is None


def test_v10_fingerprint_format_not_retroactively_enforced():
    snap = DatasetSnapshot.model_validate(v10_payload(fingerprint="legacy-free-text"))
    assert snap.fingerprint == "legacy-free-text"


# ------------------------------------------------------------------ immuabilité logique


def test_snapshot_is_frozen():
    snap = synthetic_snapshot()
    with pytest.raises(ValidationError):
        snap.fingerprint = sha256_fingerprint(b"other")
    with pytest.raises(ValidationError):
        snap.availability_cutoff = snap.as_of


def test_mutation_requires_new_snapshot_id_semantics():
    snap = synthetic_snapshot()
    rows = synthetic_rows()
    rows[0] = {**rows[0], "adjusted_close": rows[0]["adjusted_close"] + 1}
    with pytest.raises(ValueError, match="table fingerprint mismatch"):
        snap.verify_table(rows)


# ------------------------------------------------------------------ v1.1 complet


def test_v11_synthetic_snapshot_valid():
    snap = synthetic_snapshot()
    assert snap.contract_version == "1.1"
    snap.verify_table(synthetic_rows())
    snap.verify_artifacts([artifact()])
    snap.verify_calendar(synthetic_calendar())
    assert snap.lineage_fingerprint.startswith("sha256:")


def test_table_fingerprint_format_enforced_with_schema():
    with pytest.raises(ValidationError, match="fingerprint must match"):
        synthetic_snapshot(fingerprint="sha256:abc")


def test_raw_fingerprint_required_and_consistent():
    with pytest.raises(ValidationError, match="raw_fingerprint is required"):
        synthetic_snapshot(raw_fingerprint=None)
    with pytest.raises(ValidationError, match="does not match the source artifact set"):
        synthetic_snapshot(raw_fingerprint=sha256_fingerprint(b"x"))
    with pytest.raises(ValidationError, match="requires source_artifacts"):
        synthetic_snapshot(source_artifacts=(), lineage=())


def test_lineage_must_end_at_dataset_fingerprint():
    kwargs = snapshot_kwargs()
    kwargs["fingerprint"] = sha256_fingerprint(b"another table")
    with pytest.raises(ValidationError, match="dataset fingerprint"):
        DatasetSnapshot(**kwargs)


def test_lineage_calendar_input_requires_calendar_reference():
    with pytest.raises(ValidationError, match="auxiliary"):
        synthetic_snapshot(market_calendar=None)


def test_duplicate_artifact_references_rejected():
    kwargs = snapshot_kwargs()
    ref = kwargs["source_artifacts"][0]
    kwargs["source_artifacts"] = (ref, ref)
    with pytest.raises(ValidationError, match="unique"):
        DatasetSnapshot(**kwargs)


def test_canonical_range_within_returned_range():
    with pytest.raises(ValidationError, match="within returned_range"):
        synthetic_snapshot(
            returned_range=SessionRange(first_session=date(2012, 1, 2),
                                        last_session=date(2020, 6, 30))
        )


def test_instrument_consistent_with_instruments_list():
    with pytest.raises(ValidationError, match="instrument.ticker"):
        synthetic_snapshot(instruments=["OTHER"])


def test_counts_arithmetic():
    kwargs = snapshot_kwargs()
    counts = kwargs["counts"]
    with pytest.raises(ValidationError, match="expected_sessions"):
        type(counts)(**{**counts.model_dump(), "missing_sessions": Knowable.known(99)})
    with pytest.raises(ValidationError, match="canonical_observations must be <="):
        type(counts)(**{**counts.model_dump(), "raw_observations": 1})


def test_verify_artifacts_detects_mismatch():
    snap = synthetic_snapshot()
    with pytest.raises(ValueError, match="artifact set mismatch"):
        snap.verify_artifacts([])
    other = artifact(content=b"different bytes")
    with pytest.raises(ValueError, match="does not match its reference"):
        snap.verify_artifacts([other])


def test_verify_calendar_detects_wrong_calendar_and_counts():
    snap = synthetic_snapshot()
    with pytest.raises(ValueError, match="does not match"):
        snap.verify_calendar(synthetic_calendar(last=date(2020, 12, 30)))
    kwargs = snapshot_kwargs()
    counts = kwargs["counts"]
    kwargs["counts"] = type(counts)(
        **{
            **counts.model_dump(),
            "expected_sessions": Knowable.known(counts.expected_sessions.value + 1),
            "missing_sessions": Knowable.known(counts.missing_sessions.value + 1),
        }
    )
    with pytest.raises(ValueError, match="expected_sessions"):
        DatasetSnapshot(**kwargs).verify_calendar(synthetic_calendar())


def test_inv14_canonical_timezone_must_equal_calendar_timezone():
    tc = TemporalConvention(source_timezone=Knowable.known("UTC"), canonical_timezone="UTC",
                            session_date_rule="literal")
    snap = synthetic_snapshot(temporal_convention=tc)
    with pytest.raises(ValueError, match="canonical_timezone differs"):
        snap.verify_calendar(synthetic_calendar())


def test_inv14_canonical_bounds_must_be_calendar_sessions():
    saturday = date(2010, 1, 9)
    snap = synthetic_snapshot(
        canonical_range=SessionRange(first_session=saturday, last_session=date(2020, 6, 30))
    )
    with pytest.raises(ValueError, match="is not a calendar session"):
        snap.verify_calendar(synthetic_calendar())


def test_inv14_snapshot_without_calendar_reference_cannot_be_verified(sample_snapshot):
    with pytest.raises(ValueError, match="declares no market_calendar"):
        sample_snapshot.verify_calendar(synthetic_calendar())


def test_inv15_negative_session_counts_rejected():
    counts = snapshot_kwargs()["counts"]
    for field in ("expected_sessions", "missing_sessions", "invalidated_sessions"):
        with pytest.raises(ValidationError, match=">= 0"):
            type(counts)(**{**dict(counts), field: Knowable.known(-1),
                            **({"expected_sessions": Knowable.unknown()}
                               if field != "expected_sessions" else
                               {"missing_sessions": Knowable.unknown()})})


def test_inv12_table_fingerprint_independent_of_as_of():
    later = synthetic_snapshot(as_of=datetime(2021, 1, 1, tzinfo=UTC))
    later.verify_table(synthetic_rows())
    assert later.fingerprint == synthetic_snapshot().fingerprint


def test_v11_json_roundtrip():
    snap = synthetic_snapshot()
    again = DatasetSnapshot.model_validate_json(snap.model_dump_json())
    assert again == snap
