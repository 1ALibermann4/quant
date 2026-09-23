"""
Frontière de confiance C02 (CA-02, HAT2-A6) et frontière de garantie de C02-INV-14.

Décision : toute frontière validante revalide profondément les instances reçues —
constructeurs et `model_validate*` des modèles C02 (`revalidate_instances="always"`), ainsi
que `verify_artifacts`, `verify_calendar` et `validate_i01_snapshot`. Un objet forgé par une
API de contournement (`model_construct`, `model_copy(update=…)`) reste hors garantie tant
qu'il n'a franchi aucune de ces frontières ; il ne peut pas contaminer un objet racine validé.
"""

from datetime import date, datetime, time, timezone

import pytest
from c02_synthetic import (
    DATA_LAST,
    artifact,
    assessment,
    snapshot_kwargs,
    synthetic_calendar,
    synthetic_snapshot,
)
from pydantic import ValidationError

from quant.contracts import (
    DatasetSnapshot,
    FrozenMap,
    Provenance,
    TransformationRecord,
)
from quant.contracts.data_assessment import CheckResult
from quant.contracts.knowledge import Knowable, KnowledgeStatus
from quant.contracts.lineage import InstrumentIdentifiers, ProviderArtifact
from quant.contracts.market_calendar import EarlyClose, MarketCalendarSnapshot
from quant.contracts.dataset_snapshot import ObservationCounts, SessionRange
from quant.contracts.profiles.i01 import validate_i01_snapshot

CAL = synthetic_calendar()


def _forged_record(record, **fields):
    return TransformationRecord.model_construct(**{**dict(record), **fields})


# ------------------------------------------------------------------ reproduction HAT2-A6


def test_hat2_a6_forged_record_cannot_contaminate_validated_snapshot():
    kwargs = snapshot_kwargs()
    first, *rest = kwargs["lineage"]
    forged = _forged_record(first, parameters={"api_key": "s3cr3t"})
    assert isinstance(forged.parameters, dict)  # le contournement lui-même reste hors garantie
    with pytest.raises(ValidationError, match="credentials"):
        DatasetSnapshot(**{**kwargs, "lineage": (forged, *rest)})


def test_forged_but_valid_record_is_revalidated_into_frozen_state():
    kwargs = snapshot_kwargs()
    first, *rest = kwargs["lineage"]
    forged = _forged_record(first, parameters=dict(first.parameters))
    snap = DatasetSnapshot(**{**kwargs, "lineage": (forged, *rest)})
    stored = snap.lineage[0]
    assert stored is not forged
    assert isinstance(stored.parameters, FrozenMap)
    assert snap.lineage_fingerprint == synthetic_snapshot().lineage_fingerprint


def test_model_copy_update_cannot_contaminate_validated_snapshot():
    kwargs = snapshot_kwargs()
    first, *rest = kwargs["lineage"]
    copied = first.model_copy(update={"parameters": {"note": "Authorization: Bearer abc"}})
    with pytest.raises(ValidationError, match="credentials"):
        DatasetSnapshot(**{**kwargs, "lineage": (copied, *rest)})


@pytest.mark.parametrize(
    ("field", "forged_factory", "match"),
    [
        (
            "provenance",
            lambda kw: Provenance.model_construct(
                **{**dict(kw["provenance"]), "time_range_start": kw["provenance"].time_range_end}
            ),
            "time_range_start",
        ),
        (
            "instrument",
            lambda kw: InstrumentIdentifiers.model_construct(
                **{**dict(kw["instrument"]), "venue": Knowable.model_construct(status=KnowledgeStatus.KNOWN)}
            ),
            "KNOWN requires a value",
        ),
        (
            "counts",
            lambda kw: ObservationCounts.model_construct(**{**dict(kw["counts"]), "raw_observations": -1}),
            "greater than or equal",
        ),
    ],
)
def test_forged_nested_models_are_revalidated(field, forged_factory, match):
    kwargs = snapshot_kwargs()
    with pytest.raises(ValidationError, match=match):
        DatasetSnapshot(**{**kwargs, field: forged_factory(kwargs)})


def test_forged_nested_objects_rejected_in_calendar_and_assessment():
    early = EarlyClose.model_construct(session=date(2019, 7, 3), close_local=time(13, 0, tzinfo=timezone.utc))
    with pytest.raises(ValidationError, match="early close"):
        MarketCalendarSnapshot(**{**dict(CAL), "early_closes": (early,)})
    good = assessment(synthetic_snapshot())
    forged_check = CheckResult.model_construct(check_id="Q-01", outcome="MAYBE")
    with pytest.raises(ValidationError):
        type(good)(**{**dict(good), "checks": (forged_check, *good.checks[1:])})


# ------------------------------------------------------------ fonctions de vérification


def test_verify_artifacts_revalidates_forged_artifact():
    real = artifact()
    forged = ProviderArtifact.model_construct(
        **{**dict(real), "provenance_metadata": {"h": "Authorization: Bearer abc"}}
    )
    assert forged.ref() == real.ref()
    snap = synthetic_snapshot()
    with pytest.raises(ValueError, match="credentials"):
        snap.verify_artifacts([forged])
    report = validate_i01_snapshot(snap, calendar=CAL, artifacts=[forged])
    assert not report.data_pass_eligible
    assert any("credentials" in e for e in report.errors)


def test_verify_calendar_revalidates_forged_calendar():
    forged = MarketCalendarSnapshot.model_construct(**{**dict(CAL), "session_count": 1})
    with pytest.raises(ValueError, match="session_count"):
        synthetic_snapshot().verify_calendar(forged)


def test_profile_rejects_forged_snapshot():
    snap = synthetic_snapshot()
    forged = DatasetSnapshot.model_construct(**{**dict(snap), "availability_cutoff": datetime(2030, 1, 1, tzinfo=timezone.utc)})
    with pytest.raises(ValidationError, match="availability_cutoff"):
        validate_i01_snapshot(forged, calendar=CAL, artifacts=[artifact()])


# ------------------------------------------------------------ exceptions internes (audit)


def test_naive_aware_mix_raises_validation_error_not_type_error():
    kwargs = snapshot_kwargs()
    with pytest.raises(ValidationError, match="pairwise comparable"):
        DatasetSnapshot(**{**kwargs, "as_of": datetime(2020, 8, 1)})
    prov = Provenance(**{**dict(kwargs["provenance"]), "time_range_start": datetime(2010, 1, 4)})
    with pytest.raises(ValidationError, match="pairwise comparable"):
        DatasetSnapshot(**{**kwargs, "provenance": prov})


# ------------------------------------------------------------ frontière de C02-INV-14


def test_inv14_is_not_enforced_at_construction_but_at_verify_calendar_and_profile():
    saturday = date(2010, 1, 9)
    snap = synthetic_snapshot(canonical_range=SessionRange(first_session=saturday, last_session=DATA_LAST))
    with pytest.raises(ValueError, match="is not a calendar session"):
        snap.verify_calendar(CAL)
    report = validate_i01_snapshot(snap, calendar=CAL, artifacts=[artifact()])
    assert not report.conforms
    assert any("is not a calendar session" in e for e in report.errors)


def test_inv14_conditional_clauses_are_vacuous_without_fields_but_profile_requires_them():
    no_range = synthetic_snapshot(canonical_range=None)
    no_range.verify_calendar(CAL)
    assert "canonical_range: missing" in validate_i01_snapshot(no_range, calendar=CAL, artifacts=[artifact()]).errors

    counts = snapshot_kwargs()["counts"]
    unknown = ObservationCounts(
        **{**dict(counts), "expected_sessions": Knowable.unknown(), "missing_sessions": Knowable.unknown()}
    )
    snap = synthetic_snapshot(counts=unknown)
    snap.verify_calendar(CAL)
    errors = validate_i01_snapshot(snap, calendar=CAL, artifacts=[artifact()]).errors
    assert any(e.startswith("counts.expected_sessions: must be KNOWN") for e in errors)
