"""
Changements de comportement déclarés (C02 v1.1 `compatibility.behaviour_changes`) — CA-02, HAT2-A5.

Ces tests figent le comportement réellement observé que la documentation décrit.
"""

import json
from datetime import datetime, timezone

import pytest
from c02_synthetic import artifact, snapshot_kwargs, synthetic_calendar, synthetic_snapshot
from pydantic import ValidationError

from quant.contracts import DatasetSnapshot, Provenance
from quant.contracts.dataset_snapshot import ObservationCounts, V1_1_FIELDS
from quant.contracts.knowledge import Knowable

UTC = timezone.utc


def _v10():
    return DatasetSnapshot(
        contract_version="1.0",
        snapshot_id="s",
        fingerprint="f",
        as_of=datetime(2020, 1, 2, tzinfo=UTC),
        availability_cutoff=datetime(2020, 1, 1, tzinfo=UTC),
        provenance=Provenance(
            source_label="x",
            universe_description="u",
            time_range_start=datetime(2019, 1, 1, tzinfo=UTC),
            time_range_end=datetime(2019, 12, 31, tzinfo=UTC),
            survivorship_bias_acknowledged=True,
        ),
        instruments=["X"],
    )


def test_bc03_model_dump_and_json_of_v10_object_carry_the_13_v11_keys():
    snap = _v10()
    dumped = snap.model_dump()
    assert len(V1_1_FIELDS) == 13
    assert all(k in dumped for k in V1_1_FIELDS)
    assert {k for k in V1_1_FIELDS if dumped[k] is not None} == {"source_artifacts", "lineage"}
    assert dumped["source_artifacts"] == () and dumped["lineage"] == ()
    assert dumped["instruments"] == ["X"]
    as_json = snap.model_dump(mode="json")
    assert as_json["source_artifacts"] == [] and as_json["lineage"] == []
    assert all(f'"{k}"' in snap.model_dump_json() for k in V1_1_FIELDS)


def test_bc06_frozenmap_equals_dict_only_when_nested_lists_are_tuples():
    record = synthetic_snapshot().lineage[0]
    as_lists = {"date_rule": "utc_literal_date_part", "columns": ["date", "adjClose", "close"]}
    as_tuples = {"date_rule": "utc_literal_date_part", "columns": ("date", "adjClose", "close")}
    assert record.parameters != as_lists
    assert record.parameters == as_tuples
    assert record.model_dump()["parameters"] == as_lists
    assert synthetic_snapshot().lineage[1].parameters == {"fill": "never"}


def test_bc08_models_are_hashable_consistently_with_equality():
    for build in (synthetic_snapshot, artifact, synthetic_calendar, _v10):
        a, b = build(), build()
        assert a == b and hash(a) == hash(b)
    assert len({synthetic_snapshot(), synthetic_snapshot()}) == 1


def test_hat3_m6_v10_json_with_homonymous_v11_key_is_rejected():
    """BC-13 : une clé v1.1 dans un JSON déclaré 1.0 n'est plus ignorée."""
    payload = {
        "contract_version": "1.0",
        "snapshot_id": "s",
        "fingerprint": "f",
        "as_of": "2020-01-02T00:00:00Z",
        "availability_cutoff": "2020-01-01T00:00:00Z",
        "provenance": {
            "source_label": "x",
            "universe_description": "u",
            "time_range_start": "2019-01-01T00:00:00Z",
            "time_range_end": "2019-12-31T00:00:00Z",
            "survivorship_bias_acknowledged": True,
        },
        "counts": {"legacy": 1},
    }
    with pytest.raises(ValidationError):
        DatasetSnapshot.model_validate_json(json.dumps(payload))


def test_hat3_m9_scientific_bool_and_int_are_strict():
    with pytest.raises(ValidationError):
        Provenance(
            source_label="x",
            universe_description="u",
            time_range_start=datetime(2019, 1, 1, tzinfo=UTC),
            time_range_end=datetime(2019, 12, 31, tzinfo=UTC),
            survivorship_bias_acknowledged="yes",  # type: ignore[arg-type]
        )
    with pytest.raises(ValidationError):
        ObservationCounts(
            raw_observations=True,  # type: ignore[arg-type]
            canonical_observations=0,
            expected_sessions=Knowable.unknown(),
            missing_sessions=Knowable.unknown(),
            invalidated_sessions=Knowable.unknown(),
        )


def test_ca04_bc14_is_transitive_through_knowable_counts():
    """HAT4-B1 : True/False ne doivent plus devenir 1/0 via Knowable[int]."""
    with pytest.raises(ValidationError, match="exact int"):
        ObservationCounts(
            raw_observations=1,
            canonical_observations=1,
            expected_sessions=Knowable.known(True),
            missing_sessions=Knowable.known(False),
            invalidated_sessions=Knowable.known(0),
        )


def test_bc12_non_utc_input_is_stored_and_serialized_as_utc():
    from datetime import timedelta
    from zoneinfo import ZoneInfo

    ny = ZoneInfo("America/New_York")
    snap = DatasetSnapshot(
        contract_version="1.0",
        snapshot_id="s",
        fingerprint="f",
        as_of=datetime(2020, 1, 2, 0, 0, tzinfo=ny),
        availability_cutoff=datetime(2020, 1, 1, 0, 0, tzinfo=ny),
        provenance=Provenance(
            source_label="x",
            universe_description="u",
            time_range_start=datetime(2019, 1, 1, tzinfo=UTC),
            time_range_end=datetime(2019, 12, 31, tzinfo=UTC),
            survivorship_bias_acknowledged=True,
        ),
    )
    assert snap.as_of.tzinfo is timezone.utc
    assert snap.as_of == datetime(2020, 1, 2, 5, 0, tzinfo=UTC)
    assert "2020-01-02T05:00:00Z" in snap.model_dump_json()
    assert snap.as_of == datetime(2020, 1, 2, 0, 0, tzinfo=timezone(timedelta(hours=-5)))


def test_bc09_nested_instances_are_stored_as_revalidated_copies():
    kwargs = snapshot_kwargs()
    record = kwargs["lineage"][0]
    snap = DatasetSnapshot(**kwargs)
    assert snap.lineage[0] == record
    assert snap.lineage[0] is not record
