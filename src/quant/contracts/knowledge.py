"""C02 v1.1 — valeurs à connaissance partielle (KNOWN / UNKNOWN / NOT_APPLICABLE)."""

from __future__ import annotations

from collections.abc import Mapping
from enum import Enum
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, field_serializer, field_validator, model_validator

from quant.contracts.immutable import C02Validated, deep_freeze, thaw

T = TypeVar("T")


class KnowledgeStatus(str, Enum):
    KNOWN = "KNOWN"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


def _scientific_value_type(cls: type) -> Any:
    """Paramètre T de `Knowable[T]`, ou None si le générique n'est pas spécialisé."""
    meta = getattr(cls, "__pydantic_generic_metadata__", None)
    if not isinstance(meta, dict):
        return None
    args = meta.get("args") or ()
    if not args:
        return None
    expected = args[0]
    if isinstance(expected, TypeVar):
        return None
    return expected


def _require_exact_scientific_type(expected: Any, raw: Any) -> None:
    """Contrôle le type brut avant toute conversion Pydantic (BC-14 transitif)."""
    if raw is None:
        return
    if expected is int and type(raw) is not int:
        raise ValueError(
            "Knowable[int]: scientific int requires an exact int "
            f"(got {type(raw).__name__}); bool, float and str are rejected"
        )
    if expected is bool and type(raw) is not bool:
        raise ValueError(
            "Knowable[bool]: scientific bool requires an exact bool "
            f"(got {type(raw).__name__})"
        )


class Knowable(C02Validated, Generic[T]):
    """
    Métadonnée dont la connaissance peut être partielle.

    Invariant C02-INV-K01 : `value` présent ⇔ `status == KNOWN`.
    Une information absente n'est jamais représentée par une valeur inventée.
    La valeur KNOWN est gelée en profondeur (aucune structure mutable atteignable).
    `Knowable[T]` n'est pas plus permissif que la politique de T : pour int et bool,
    le type brut est examiné avant toute coercition Pydantic.
    """

    status: KnowledgeStatus
    value: T | None = None
    note: str | None = None

    @model_validator(mode="before")
    @classmethod
    def _reject_destructive_coercion(cls, data: Any) -> Any:
        expected = _scientific_value_type(cls)
        if expected not in (int, bool):
            return data
        if isinstance(data, dict):
            if "value" not in data:
                return data
            raw = data["value"]
        elif isinstance(data, Knowable):
            raw = data.value
        else:
            return data
        _require_exact_scientific_type(expected, raw)
        return data

    @field_validator("value", mode="before")
    @classmethod
    def _reject_destructive_value_coercion(cls, value: Any) -> Any:
        expected = _scientific_value_type(cls)
        if expected in (int, bool):
            _require_exact_scientific_type(expected, value)
        return value

    @field_serializer("value", when_used="always")
    def _serialize_known_value(self, value: Any) -> Any:
        if value is None or isinstance(value, BaseModel):
            return value
        if isinstance(value, Mapping | tuple | list):
            return thaw(value)
        return value

    @model_validator(mode="after")
    def _value_iff_known(self) -> Knowable[T]:
        if self.status is KnowledgeStatus.KNOWN and self.value is None:
            raise ValueError("Knowable: status KNOWN requires a value")
        if self.status is not KnowledgeStatus.KNOWN and self.value is not None:
            raise ValueError(f"Knowable: status {self.status.value} forbids a value")
        if self.value is not None:
            frozen = deep_freeze(self.value)
            if frozen is not self.value:
                object.__setattr__(self, "value", frozen)
        return self

    @classmethod
    def known(cls, value: Any, note: str | None = None) -> Knowable[Any]:
        return cls(status=KnowledgeStatus.KNOWN, value=value, note=note)

    @classmethod
    def unknown(cls, note: str | None = None) -> Knowable[Any]:
        return cls(status=KnowledgeStatus.UNKNOWN, note=note)

    @classmethod
    def not_applicable(cls, note: str | None = None) -> Knowable[Any]:
        return cls(status=KnowledgeStatus.NOT_APPLICABLE, note=note)

    @property
    def is_known(self) -> bool:
        return self.status is KnowledgeStatus.KNOWN
