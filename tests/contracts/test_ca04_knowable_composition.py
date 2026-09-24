"""
CA-04 — composition : strictness de T à travers Knowable et les objets C02.

Périmètre borné : T vs Knowable[T] vs conteneur vs modèle imbriqué. Pas un
ré-audit général de C02.
"""

from datetime import date

import pytest
from c02_synthetic import artifact, license_ref, snapshot_kwargs, synthetic_calendar
from pydantic import BaseModel, Field, ValidationError

from quant.contracts.dataset_snapshot import (
    AdjustmentMethod,
    DatasetSnapshot,
    ObservationCounts,
    SessionRange,
)
from quant.contracts.immutable import FrozenMap, FrozenMapping
from quant.contracts.knowledge import Knowable, KnowledgeStatus
from quant.contracts.lineage import LicenseRef, TransformationRecord
from quant.contracts.profiles.i01 import validate_i01_snapshot
from test_lineage import OUT, RAW, record


def test_observation_counts_reject_bool_and_float_through_knowable():
    with pytest.raises(ValidationError, match="exact int"):
        ObservationCounts(
            raw_observations=1,
            canonical_observations=1,
            expected_sessions=Knowable.known(True),
            missing_sessions=Knowable.known(False),
            invalidated_sessions=Knowable.known(0),
        )
    with pytest.raises(ValidationError, match="exact int"):
        ObservationCounts(
            raw_observations=1,
            canonical_observations=1,
            expected_sessions=Knowable[int].known(1.0),
            missing_sessions=Knowable.unknown(),
            invalidated_sessions=Knowable.unknown(),
        )


def test_transformation_counts_reject_coerced_ints():
    with pytest.raises(ValidationError, match="exact int"):
        record(0, [RAW], OUT, observations_in=Knowable.known(True))
    with pytest.raises(ValidationError, match="exact int"):
        record(0, [RAW], OUT, observations_dropped=Knowable.known(1.0))
    with pytest.raises(ValidationError, match="exact int"):
        record(0, [RAW], OUT, observations_out=Knowable.known("9"))


def test_license_ack_rejects_yes_one_and_string_true():
    for raw in ("yes", "true", 1, 0, 1.0):
        with pytest.raises(ValidationError, match="exact bool"):
            license_ref(raw_retention_permitted=Knowable.known(raw))
        with pytest.raises(ValidationError, match="exact bool"):
            LicenseRef.model_validate(
                {
                    **license_ref().model_dump(),
                    "raw_retention_permitted": {"status": "KNOWN", "value": raw},
                }
            )


def test_known_yes_never_becomes_known_true_on_license_or_i01():
    genuine = license_ref(raw_retention_permitted=Knowable.known(True))
    with pytest.raises(ValidationError, match="exact bool"):
        license_ref(raw_retention_permitted=Knowable.known("yes"))
    art = artifact(license=genuine)
    assert art.license.raw_retention_permitted.value is True
    report = validate_i01_snapshot(
        DatasetSnapshot(**snapshot_kwargs()),
        calendar=synthetic_calendar(),
        artifacts=[art],
    )
    assert report.data_pass_eligible
    forged = LicenseRef.model_construct(
        **{
            **dict(genuine),
            "raw_retention_permitted": Knowable.model_construct(
                status=KnowledgeStatus.KNOWN, value="yes"
            ),
        }
    )
    with pytest.raises(ValidationError, match="exact bool"):
        artifact(license=forged)
    forged_art = artifact().model_construct(**{**dict(artifact()), "license": forged})
    report_forged = validate_i01_snapshot(
        DatasetSnapshot(**snapshot_kwargs()),
        calendar=synthetic_calendar(),
        artifacts=[forged_art],
    )
    assert not report_forged.data_pass_eligible
    assert any("revalidation" in err or "exact bool" in err for err in report_forged.errors)


def test_invalid_raw_type_cannot_produce_data_pass_eligible_counts():
    kwargs = snapshot_kwargs()
    forged_counts = ObservationCounts.model_construct(
        raw_observations=1,
        canonical_observations=1,
        expected_sessions=Knowable.model_construct(
            status=KnowledgeStatus.KNOWN, value=True
        ),
        missing_sessions=Knowable.model_construct(
            status=KnowledgeStatus.KNOWN, value=False
        ),
        invalidated_sessions=Knowable.known(0),
    )
    with pytest.raises(ValidationError, match="exact int"):
        DatasetSnapshot(**{**kwargs, "counts": forged_counts})


def test_nested_parameters_survive_snapshot_revalidation_and_fingerprint():
    kwargs = snapshot_kwargs()
    first, *rest = kwargs["lineage"]
    nested = {
        "align": {"calendar": "SYNTHETIC", "rule": "intersect"},
        "keep": ["session_date", "close"],
    }
    replaced = TransformationRecord(
        **{**dict(first), "parameters": nested, "observations_dropped": first.observations_dropped}
    )
    snap = DatasetSnapshot(**{**kwargs, "lineage": (replaced, *rest)})
    stored = snap.lineage[0].parameters
    assert stored["align"]["rule"] == "intersect"
    again = DatasetSnapshot.model_validate_json(snap.model_dump_json())
    assert again.lineage[0].parameters == stored
    assert again.lineage_fingerprint == snap.lineage_fingerprint


class _Holder(BaseModel):
    count: Knowable[int]
    ack: Knowable[bool]


def test_wrapper_is_not_more_permissive_than_isolated_strict_fields():
    class Isolated(BaseModel):
        count: int = Field(strict=True)
        ack: bool = Field(strict=True)

    for raw in (True, False, 1.0, "1"):
        with pytest.raises(ValidationError):
            Isolated(count=raw, ack=True)  # type: ignore[arg-type]
        with pytest.raises(ValidationError):
            _Holder(count=Knowable[int].known(raw), ack=Knowable[bool].known(True))
    for raw in (1, 0, "yes", "true"):
        with pytest.raises(ValidationError):
            Isolated(count=1, ack=raw)  # type: ignore[arg-type]
        with pytest.raises(ValidationError):
            _Holder(count=Knowable[int].known(1), ack=Knowable[bool].known(raw))


def test_tuple_and_frozenmap_do_not_reintroduce_int_coercion_via_knowable():
    class Boxed(BaseModel):
        values: tuple[Knowable[int], ...]
        keyed: FrozenMapping[Knowable[int]]

    with pytest.raises(ValidationError, match="exact int"):
        Boxed(
            values=({"status": "KNOWN", "value": True},),
            keyed={"n": Knowable[int].known(1)},
        )
    with pytest.raises(ValidationError, match="exact int"):
        Boxed(
            values=(Knowable[int].known(1),),
            keyed={"n": {"status": "KNOWN", "value": True}},
        )
    ok = Boxed(values=(Knowable[int].known(2),), keyed={"n": Knowable[int].known(3)})
    assert ok.values[0].value == 2
    assert ok.keyed["n"].value == 3
    assert isinstance(ok.keyed, FrozenMap)


def test_knowable_date_enum_and_session_range_keep_normative_json_coercions():
    day = Knowable[date].model_validate({"status": "KNOWN", "value": "2010-01-04"})
    assert day.value == date(2010, 1, 4)
    method = Knowable[AdjustmentMethod].model_validate(
        {"status": "KNOWN", "value": "PROPORTIONAL"}
    )
    assert method.value is AdjustmentMethod.PROPORTIONAL
    rng = Knowable[SessionRange].model_validate(
        {
            "status": "KNOWN",
            "value": {"first_session": "2010-01-04", "last_session": "2010-01-05"},
        }
    )
    assert rng.value.first_session == date(2010, 1, 4)
    restored = Knowable[SessionRange].model_validate_json(
        Knowable[SessionRange].known(rng.value).model_dump_json()
    )
    assert restored == rng
