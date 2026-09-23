"""
Tests C02-INV-05 — immuabilité transitive (CA-01, constat HAT-A1).

Aucune mutation atteignable depuis un objet C02 par son API publique ne doit modifier son
état ni une empreinte dérivée. Contournements délibérés hors garantie (documentés dans le
contrat) : `object.__setattr__`, attributs privés, `model_construct`, `model_copy(update=…)`.
"""

import copy
import hashlib
import pickle
from collections.abc import Mapping
from datetime import datetime, timezone

import pytest
from c02_synthetic import artifact, assessment, snapshot_kwargs, synthetic_calendar, synthetic_snapshot
from pydantic import BaseModel, ValidationError

from quant.contracts.base import DatasetSnapshotRef
from quant.contracts.dataset_snapshot import DatasetSnapshot
from quant.contracts.immutable import FrozenMap
from quant.contracts.knowledge import Knowable

UTC = timezone.utc

V10_PAYLOAD = {
    "contract_version": "1.0",
    "snapshot_id": "legacy",
    "fingerprint": "sha256:abc123",
    "as_of": "2024-01-15T16:00:00Z",
    "availability_cutoff": "2024-01-15T16:00:00Z",
    "provenance": {
        "source_label": "f",
        "universe_description": "u",
        "time_range_start": "2023-01-01T00:00:00Z",
        "time_range_end": "2024-01-15T00:00:00Z",
        "survivorship_bias_acknowledged": True,
    },
    "instruments": ["X"],
    "adjustments": [{"type": "split", "description": "2:1", "applied_at": "2023-06-01T00:00:00Z"}],
    "quality_flags": ["WARN:x"],
}


def _objects():
    snap = synthetic_snapshot()
    return {
        "snapshot_v11": snap,
        "snapshot_v10": DatasetSnapshot.model_validate(V10_PAYLOAD),
        "artifact": artifact(),
        "calendar": synthetic_calendar(),
        "assessment": assessment(snap),
    }


def _mutable_paths(value, path="$"):
    """Chemins de tout conteneur mutable ou modèle non gelé atteignable."""
    found = []
    if isinstance(value, BaseModel):
        if not value.model_config.get("frozen"):
            found.append(f"{path} ({type(value).__name__} not frozen)")
        for name in type(value).model_fields:
            found += _mutable_paths(getattr(value, name), f"{path}.{name}")
    elif isinstance(value, list | dict | set | bytearray):
        found.append(f"{path} ({type(value).__name__})")
    elif isinstance(value, Mapping):
        if not isinstance(value, FrozenMap):
            found.append(f"{path} ({type(value).__name__})")
        for key, item in value.items():
            found += _mutable_paths(item, f"{path}[{key!r}]")
    elif isinstance(value, tuple | frozenset):
        for i, item in enumerate(value):
            found += _mutable_paths(item, f"{path}[{i}]")
    return found


@pytest.mark.parametrize("name", list(_objects()))
def test_no_mutable_container_reachable(name):
    assert _mutable_paths(_objects()[name]) == []


# ------------------------------------------------------------------ mutations du HAT


def test_hat_a1_provenance_assignment_rejected():
    snap = synthetic_snapshot()
    before = snap.provenance.time_range_end
    with pytest.raises(ValidationError):
        snap.provenance.time_range_end = datetime(2030, 1, 1, tzinfo=UTC)
    assert snap.provenance.time_range_end == before


def test_hat_a1_instruments_append_rejected():
    snap = synthetic_snapshot()
    with pytest.raises(AttributeError):
        snap.instruments.append("OTHER")
    assert snap.instruments == ("SYNTH",)


def test_hat_a1_lineage_parameters_mutation_rejected_and_fingerprint_stable():
    snap = synthetic_snapshot()
    before = snap.lineage_fingerprint
    params = snap.lineage[0].parameters
    with pytest.raises(TypeError):
        params["date_rule"] = "tampered"
    with pytest.raises(AttributeError):
        params["columns"].append("x")
    with pytest.raises(AttributeError):
        params._data = {}
    assert snap.lineage_fingerprint == before


def test_hat_a1_request_parameters_injection_rejected():
    art = artifact()
    with pytest.raises(TypeError):
        art.request_parameters["apiKey"] = "SECRET"
    with pytest.raises(TypeError):
        art.provenance_metadata["x"] = "y"
    assert "apiKey" not in art.request_parameters


def test_adjustment_records_frozen():
    snap = DatasetSnapshot.model_validate(V10_PAYLOAD)
    with pytest.raises(ValidationError):
        snap.adjustments[0].description = "tampered"


def test_assessment_snapshot_ref_frozen_and_accepts_c01_ref():
    snap = synthetic_snapshot()
    gate = assessment(snap, snapshot_ref=DatasetSnapshotRef(
        snapshot_id=snap.snapshot_id, fingerprint=snap.fingerprint))
    assert isinstance(gate.snapshot_ref, DatasetSnapshotRef)
    with pytest.raises(ValidationError):
        gate.snapshot_ref.fingerprint = "sha256:other"


def test_input_containers_are_copied_not_aliased():
    params = {"startDate": "2010-01-01", "format": "csv"}
    art = artifact(request_parameters=params)
    params["format"] = "json"
    assert art.request_parameters["format"] == "csv"


def test_knowable_value_list_input_is_frozen():
    kwargs = snapshot_kwargs()
    adj = kwargs["adjustment_methodology"]
    frozen = type(adj)(**{**dict(adj), "events_covered": Knowable.known(["split"])})
    assert frozen.events_covered.value == ("split",)


# ------------------------------------------------------------------ compatibilité


# Valeurs capturées à 3c684b7, avant CA-01 (référence de compatibilité).
PINNED = {
    "fingerprint": "sha256:c169b01d731a2efa330e50ec578b456f74b1dd37245d116363e2308ac6c862d3",
    "raw_fingerprint": "sha256:5e761c7a872a75cb9b499330d2c2b0edec1b2078dde7176c40a6d3a5caf40057",
    "lineage_fingerprint": "sha256:8e612ccb4cba3ecf88174632e73a759a78dfaf79bf607d284eee4e7ad79943de",
    "application_keys": [
        "sha256:9dcae3fda6c68de32d6fb1a8820b16e489143d0e714420402647fd7354e63c3d",
        "sha256:e300da73b35f391fad8f8ebe2b7de21e8ae4956f98528e4cf78abb11b87867f0",
    ],
    "calendar_content": "sha256:1c56441f70a341e3fb5b53f731911eb5e8e413814388ac94432167ca7de628b9",
    "json_sha256": {
        # CA-03 / BC-12 : instants NY de close_instant désormais stockés et sérialisés en UTC.
        "snapshot_v11": "c33dae5bcddbb35371bf641e916b5d2fd9d7e0c76b310a7f8349b6c530327ef0",
        "snapshot_v10": "c8125a1c5f0490a1753949be6e4e789b9ea4c43039b6b1a969077c8f5955f8c0",
        "artifact": "f5771b88659f5f702581da2d454e68928612a61f504847e46808dde26e23867d",
        "calendar": "edaec204f7be127bdcdb3359356c6db934065ebc6d03c6fa5b4dbdee06812388",
        "assessment": "693a86f61fc66b7696ed84f4cbf6857a9fcb41f5c204d3cecfa70ae78e9a96d2",
    },
}


def test_fingerprints_unchanged_by_deep_freeze():
    snap = synthetic_snapshot()
    assert snap.fingerprint == PINNED["fingerprint"]
    assert snap.raw_fingerprint == PINNED["raw_fingerprint"]
    assert snap.lineage_fingerprint == PINNED["lineage_fingerprint"]
    assert [r.application_key for r in snap.lineage] == PINNED["application_keys"]
    assert synthetic_calendar().content_fingerprint == PINNED["calendar_content"]


@pytest.mark.parametrize("name", list(PINNED["json_sha256"]))
def test_json_serialization_unchanged_by_deep_freeze(name):
    dumped = _objects()[name].model_dump_json()
    assert hashlib.sha256(dumped.encode("utf-8")).hexdigest() == PINNED["json_sha256"][name]


def test_python_dump_keeps_v10_container_types():
    dumped = DatasetSnapshot.model_validate(V10_PAYLOAD).model_dump()
    assert dumped["instruments"] == ["X"] and isinstance(dumped["instruments"], list)
    assert isinstance(dumped["adjustments"], list) and isinstance(dumped["quality_flags"], list)
    art = artifact().model_dump()
    assert type(art["request_parameters"]) is dict
    lineage = synthetic_snapshot().model_dump()["lineage"][0]["parameters"]
    assert type(lineage) is dict and type(lineage["columns"]) is list


@pytest.mark.parametrize("name", list(_objects()))
def test_roundtrip_python_and_json(name):
    obj = _objects()[name]
    cls = type(obj)
    assert cls.model_validate(obj.model_dump()) == obj
    assert cls.model_validate_json(obj.model_dump_json()) == obj


@pytest.mark.parametrize("name", list(_objects()))
def test_deepcopy_preserves_equality(name):
    obj = _objects()[name]
    assert copy.deepcopy(obj) == obj


def test_v10_object_pickle_roundtrip():
    snap = DatasetSnapshot.model_validate(V10_PAYLOAD)
    assert pickle.loads(pickle.dumps(snap)) == snap


def test_hat3_m8_fields_set_is_outside_scientific_state():
    """INV-05 : model_fields_set est une métadonnée Pydantic, pas l'état C02."""
    snap = synthetic_snapshot()
    before_fp = (snap.fingerprint, snap.raw_fingerprint, snap.lineage_fingerprint)
    before_json = snap.model_dump_json()
    snap.model_fields_set.add("storage_hint")
    assert (snap.fingerprint, snap.raw_fingerprint, snap.lineage_fingerprint) == before_fp
    assert snap.model_dump_json() == before_json
    assert snap.storage_hint is None


def test_frozen_map_equality_hash_and_pickle():
    fm = FrozenMap({"a": 1, "b": ("x",)})
    assert fm == {"a": 1, "b": ("x",)}
    assert hash(fm) == hash(FrozenMap({"b": ("x",), "a": 1}))
    assert pickle.loads(pickle.dumps(fm)) == fm


# ------------------------------------------------------------------ limites documentées


def test_model_copy_update_never_alters_original():
    snap = synthetic_snapshot()
    before = snap.model_dump_json()
    snap.model_copy(update={"fingerprint": "sha256:" + "0" * 64})
    assert snap.model_dump_json() == before
