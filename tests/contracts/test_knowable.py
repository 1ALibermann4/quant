"""Tests C02-INV-K01 — KNOWN / UNKNOWN / NOT_APPLICABLE."""

import pytest
from pydantic import BaseModel, ValidationError

from quant.contracts.knowledge import Knowable, KnowledgeStatus


def test_known_requires_value():
    with pytest.raises(ValidationError, match="requires a value"):
        Knowable[str](status=KnowledgeStatus.KNOWN)


@pytest.mark.parametrize("status", [KnowledgeStatus.UNKNOWN, KnowledgeStatus.NOT_APPLICABLE])
def test_non_known_forbids_value(status):
    with pytest.raises(ValidationError, match="forbids a value"):
        Knowable[str](status=status, value="invented")


def test_constructors_and_note():
    assert Knowable.known("v1").value == "v1"
    unknown = Knowable.unknown(note="vendor does not publish interface versions")
    assert unknown.status is KnowledgeStatus.UNKNOWN
    assert unknown.value is None
    assert not unknown.is_known
    assert Knowable.not_applicable().status is KnowledgeStatus.NOT_APPLICABLE


def test_value_type_validated_when_parametrized():
    with pytest.raises(ValidationError):
        Knowable[int](status=KnowledgeStatus.KNOWN, value="not-an-int")


def test_unparametrized_instance_revalidated_in_typed_field():
    class Holder(BaseModel):
        version: Knowable[int]

    with pytest.raises(ValidationError):
        Holder(version=Knowable.known("abc"))
    assert Holder(version=Knowable.known(3)).version.value == 3


def test_frozen():
    k = Knowable.known("x")
    with pytest.raises(ValidationError):
        k.status = KnowledgeStatus.UNKNOWN


def test_known_list_and_mapping_are_deep_frozen():
    k = Knowable.known(["a", {"b": ["c"]}])
    assert k.value == ("a", {"b": ("c",)})
    with pytest.raises((AttributeError, TypeError)):
        k.value.append("X")  # type: ignore[union-attr]
    inner = k.value[1]
    with pytest.raises((AttributeError, TypeError)):
        inner["b"] = "mutated"  # type: ignore[index]


def test_known_value_inside_model_is_frozen():
    class Holder(BaseModel):
        tags: Knowable[list[str]]

    holder = Holder(tags=Knowable.known(["x"]))
    assert holder.tags.value == ("x",)
    with pytest.raises((AttributeError, TypeError)):
        holder.tags.value.append("y")  # type: ignore[union-attr]


def test_serialization_roundtrip():
    k = Knowable[str].unknown(note="n")
    dumped = k.model_dump(mode="json")
    assert dumped == {"status": "UNKNOWN", "value": None, "note": "n"}
    assert Knowable[str].model_validate(dumped) == k


@pytest.mark.parametrize("raw", [True, False, 1.0, "1", 1.5])
def test_knowable_int_rejects_non_exact_int(raw):
    with pytest.raises(ValidationError, match="exact int"):
        Knowable[int].known(raw)
    with pytest.raises(ValidationError, match="exact int"):
        Knowable[int](status=KnowledgeStatus.KNOWN, value=raw)
    with pytest.raises(ValidationError, match="exact int"):
        Knowable[int].model_validate({"status": "KNOWN", "value": raw})


def test_knowable_int_rejects_json_true_and_accepts_json_int():
    with pytest.raises(ValidationError, match="exact int"):
        Knowable[int].model_validate_json('{"status":"KNOWN","value":true}')
    accepted = Knowable[int].model_validate_json('{"status":"KNOWN","value":1}')
    assert accepted.value == 1
    assert type(accepted.value) is int


@pytest.mark.parametrize("raw", [1, 0, "yes", "true", 1.0, 1.5])
def test_knowable_bool_rejects_non_exact_bool(raw):
    with pytest.raises(ValidationError, match="exact bool"):
        Knowable[bool].known(raw)
    with pytest.raises(ValidationError, match="exact bool"):
        Knowable[bool](status=KnowledgeStatus.KNOWN, value=raw)
    with pytest.raises(ValidationError, match="exact bool"):
        Knowable[bool].model_validate({"status": "KNOWN", "value": raw})


def test_knowable_bool_rejects_json_one_and_accepts_json_true():
    with pytest.raises(ValidationError, match="exact bool"):
        Knowable[bool].model_validate_json('{"status":"KNOWN","value":1}')
    accepted = Knowable[bool].model_validate_json('{"status":"KNOWN","value":true}')
    assert accepted.value is True


def test_known_yes_and_known_true_are_not_scientifically_indistinguishable():
    true = Knowable[bool].known(True)
    with pytest.raises(ValidationError, match="exact bool"):
        Knowable[bool].known("yes")
    assert true.value is True
    assert true.model_dump()["value"] is True


def test_knowable_mapping_official_json_roundtrip():
    raw = {"a": ["b", {"c": 1, "d": True}]}
    k = Knowable.known(raw)
    dumped = k.model_dump(mode="json")
    assert dumped["value"] == raw
    assert Knowable.model_validate(dumped) == k
    encoded = k.model_dump_json()
    assert Knowable.model_validate_json(encoded) == k
    python_dump = k.model_dump()
    assert python_dump["value"] == raw
    assert Knowable.model_validate(python_dump) == k
