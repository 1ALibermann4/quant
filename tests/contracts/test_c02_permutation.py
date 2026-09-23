"""
C02-INV-09 / profil P-03 — unicité des artifact_id et invariance par permutation (CA-02, HAT2-A2).

Propriété métamorphique : l'ordre d'une collection d'artefacts fournie n'a aucune
signification contractuelle, donc V(S) = V(π(S)) pour toute permutation π, pour
`DatasetSnapshot.verify_artifacts` comme pour `validate_i01_snapshot`.
"""

import itertools

import pytest
from c02_synthetic import (
    artifact,
    license_ref,
    synthetic_calendar,
    synthetic_raw_bytes,
    synthetic_snapshot,
    snapshot_kwargs,
)

from quant.contracts import DatasetSnapshot, TransformationRecord
from quant.contracts.knowledge import Knowable
from quant.contracts.profiles.i01 import validate_i01_snapshot

CAL = synthetic_calendar()


def _artifacts():
    base = synthetic_raw_bytes()
    return tuple(
        artifact(content=base + suffix, artifact_id=f"art-00{i}")
        for i, suffix in enumerate((b"", b"#2", b"#3"), start=1)
    )


def _multi_snapshot(artifacts):
    kwargs = snapshot_kwargs(calendar=CAL, artifacts=artifacts)
    first, *rest = kwargs["lineage"]
    hashes = tuple(a.content_sha256 for a in artifacts)
    kwargs["lineage"] = (
        TransformationRecord(**{**first.model_dump(), "input_fingerprints": hashes}),
        *rest,
    )
    return DatasetSnapshot(**kwargs)


A1, A2, A3 = _artifacts()
MULTI = _multi_snapshot((A1, A2, A3))
FORGED_A2 = artifact(content=b"forged bytes", artifact_id="art-002")
UNKNOWN_A4 = artifact(content=b"unreferenced", artifact_id="art-004")
OTHER_LICENSE_A1 = artifact(
    content=synthetic_raw_bytes(),
    artifact_id="art-001",
    license=license_ref(plan_tier=Knowable.known("pro")),
)


def _outcome(snapshot, collection):
    try:
        snapshot.verify_artifacts(collection)
    except ValueError as exc:
        return str(exc)
    return None


def _report(snapshot, collection):
    return validate_i01_snapshot(snapshot, calendar=CAL, artifacts=collection)


# --------------------------------------------------------------- reproductions HAT2-A2


def test_hat2_a2_reproduction_real_then_forged_and_forged_then_real():
    snap = synthetic_snapshot()
    real = artifact()
    forged = artifact(content=b"forged-bytes")
    assert real.artifact_id == forged.artifact_id
    for collection in ([real, forged], [forged, real]):
        with pytest.raises(ValueError, match="duplicate artifact_id: \\['art-001'\\]"):
            snap.verify_artifacts(collection)
        report = _report(snap, collection)
        assert not report.data_pass_eligible
        assert any("duplicate artifact_id" in e for e in report.errors)
    assert _report(snap, [real, forged]) == _report(snap, [forged, real])


def test_two_identical_artifacts_with_same_id_rejected():
    snap = synthetic_snapshot()
    real = artifact()
    with pytest.raises(ValueError, match="duplicate artifact_id"):
        snap.verify_artifacts([real, real])
    assert not _report(snap, [real, real]).data_pass_eligible


def test_several_duplicates_reported_deterministically():
    collection = [A3, A1, A2, A1, FORGED_A2, A2]
    messages = {_outcome(MULTI, list(p)) for p in itertools.permutations(collection)}
    assert messages == {"provided artifacts contain duplicate artifact_id: ['art-001', 'art-002']"}


def test_valid_collection_accepted_in_every_order():
    for perm in itertools.permutations((A1, A2, A3)):
        MULTI.verify_artifacts(perm)
        assert _report(MULTI, perm).data_pass_eligible


def test_duplicates_block_temporal_checks_on_unverified_artifacts():
    report = _report(MULTI, [A1, A2, A3, FORGED_A2])
    assert not any(FORGED_A2.artifact_id in w and "REV-D-04" in w for w in report.warnings)


# --------------------------------------------------------------- propriété métamorphique

COLLECTIONS = {
    "valid": (A1, A2, A3),
    "forged duplicate": (A1, A2, A3, FORGED_A2),
    "identical duplicate": (A1, A1, A2, A3),
    "missing": (A1, A2),
    "unreferenced extra": (A1, A2, A3, UNKNOWN_A4),
    "licence mismatch": (OTHER_LICENSE_A1, A2, A3),
    "multiple mismatches": (OTHER_LICENSE_A1, artifact(content=b"x", artifact_id="art-002"), A3),
}


@pytest.mark.parametrize("name", sorted(COLLECTIONS))
def test_permutation_invariance_of_verification_and_profile(name):
    collection = COLLECTIONS[name]
    outcomes = set()
    reports = set()
    for perm in itertools.permutations(collection):
        outcomes.add(_outcome(MULTI, list(perm)))
        reports.add(_report(MULTI, list(perm)).model_dump_json())
    assert len(outcomes) == 1, outcomes
    assert len(reports) == 1
    (outcome,) = outcomes
    assert (outcome is None) == (name == "valid")
