"""
C02 v1.1 — DataGateAssessment : verdict de qualité évalué sur un snapshot déjà figé.

Objet distinct du DatasetSnapshot : le gate DATA est évalué *après* le figement, et
l'inscrire dans le snapshot violerait son immuabilité (REV-D-02).
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from quant.contracts.base import DatasetSnapshotRef

CONTRACT_ID = "C02"
CONTRACT_VERSION = "1.1"


class CheckOutcome(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    INCONCLUSIVE = "INCONCLUSIVE"
    REJECT = "REJECT"


class DataVerdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"


class CheckResult(BaseModel):
    model_config = ConfigDict(frozen=True, revalidate_instances="always")

    check_id: str
    outcome: CheckOutcome
    measurement: str | None = None
    detail: str | None = None


class FrozenDatasetSnapshotRef(DatasetSnapshotRef):
    """`DatasetSnapshotRef` (C01, non gelé) figé pour l'état d'un objet C02."""

    model_config = ConfigDict(frozen=True, revalidate_instances="always")


class DataGateAssessment(BaseModel):
    model_config = ConfigDict(frozen=True, revalidate_instances="always")

    contract_id: str = Field(default=CONTRACT_ID, frozen=True)
    contract_version: str = CONTRACT_VERSION
    assessment_id: str
    snapshot_ref: FrozenDatasetSnapshotRef
    evaluated_against: str
    evaluated_at: datetime
    intended_use: str
    coverage_tier: str
    checks: tuple[CheckResult, ...]
    verdict: DataVerdict

    @field_validator("snapshot_ref", mode="before")
    @classmethod
    def _freeze_ref(cls, v: object) -> object:
        if isinstance(v, DatasetSnapshotRef) and not isinstance(v, FrozenDatasetSnapshotRef):
            return v.model_dump()
        return v

    @field_validator("evaluated_at")
    @classmethod
    def _aware(cls, v: datetime) -> datetime:
        if v.tzinfo is None or v.utcoffset() is None:
            raise ValueError("evaluated_at must be timezone-aware (UTC)")
        return v

    @model_validator(mode="after")
    def _verdict_consistency(self) -> DataGateAssessment:
        ids = [c.check_id for c in self.checks]
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate check_id in assessment")
        outcomes = {c.outcome for c in self.checks}
        if CheckOutcome.REJECT in outcomes and self.verdict is not DataVerdict.FAIL:
            raise ValueError("a REJECT check requires verdict FAIL")
        if CheckOutcome.INCONCLUSIVE in outcomes and self.verdict is DataVerdict.PASS:
            raise ValueError("an INCONCLUSIVE check forbids verdict PASS")
        return self

    @property
    def warnings(self) -> tuple[CheckResult, ...]:
        return tuple(c for c in self.checks if c.outcome is CheckOutcome.WARN)
