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


def test_serialization_roundtrip():
    k = Knowable[str].unknown(note="n")
    dumped = k.model_dump(mode="json")
    assert dumped == {"status": "UNKNOWN", "value": None, "note": "n"}
    assert Knowable[str].model_validate(dumped) == k
