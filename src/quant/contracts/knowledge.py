"""C02 v1.1 — valeurs à connaissance partielle (KNOWN / UNKNOWN / NOT_APPLICABLE)."""

from __future__ import annotations

from enum import Enum
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, model_validator

T = TypeVar("T")


class KnowledgeStatus(str, Enum):
    KNOWN = "KNOWN"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class Knowable(BaseModel, Generic[T]):
    """
    Métadonnée dont la connaissance peut être partielle.

    Invariant C02-INV-K01 : `value` présent ⇔ `status == KNOWN`.
    Une information absente n'est jamais représentée par une valeur inventée.
    """

    model_config = ConfigDict(frozen=True)

    status: KnowledgeStatus
    value: T | None = None
    note: str | None = None

    @model_validator(mode="after")
    def _value_iff_known(self) -> Knowable[T]:
        if self.status is KnowledgeStatus.KNOWN and self.value is None:
            raise ValueError("Knowable: status KNOWN requires a value")
        if self.status is not KnowledgeStatus.KNOWN and self.value is not None:
            raise ValueError(f"Knowable: status {self.status.value} forbids a value")
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
