"""Types partagés entre contrats C01–C05."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class GateVerdict(str, Enum):
    """Verdict d'une gate d'expérience."""

    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"
    PENDING = "PENDING"


class PromotionVerdictScientific(str, Enum):
    PROMOTED = "PROMOTED"
    NO_PROMOTION = "NO_PROMOTION"
    DEFERRED = "DEFERRED"
    REJECTED = "REJECTED"


class PromotionVerdictOperational(str, Enum):
    GO = "GO"
    NO_GO = "NO_GO"
    DEFERRED = "DEFERRED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class DatasetSnapshotRef(BaseModel):
    snapshot_id: str
    fingerprint: str


class MarketStateRef(BaseModel):
    market_state_id: str
    as_of: datetime


class SignalRef(BaseModel):
    signal_id: str
    strategy_id: str


class ContractRef(BaseModel):
    """Versions de contrats verrouillées pour reproductibilité."""

    c01: str = Field(default="1.0", description="C01 Experiment contract version")
    c02: str = Field(default="1.0", description="C02 DatasetSnapshot contract version")
    c03: str = Field(default="1.0", description="C03 MarketState contract version")
    c04: str = Field(default="1.0", description="C04 StrategySignal contract version")
    c05: str = Field(default="1.0", description="C05 RiskDecision contract version")


class GateResult(BaseModel):
    gate_id: str
    description: str
    verdict: GateVerdict = GateVerdict.PENDING
    evidence_ref: str | None = None


class ArtifactRef(BaseModel):
    name: str
    path: str
    content_type: str
    fingerprint: str | None = None


class PromotionRecord(BaseModel):
    """Distinction scientifique vs opérationnelle (deux niveaux de promotion)."""

    scientific_verdict: PromotionVerdictScientific
    operational_verdict: PromotionVerdictOperational
    notes: str | None = None


class DataSplits(BaseModel):
    train_end: datetime | None = None
    validation_end: datetime | None = None
    test_end: datetime | None = None


class AuthorizedExposure(BaseModel):
    """Exposition autorisée post-décision risque — structure minimale P0."""

    gross: float = Field(ge=0.0)
    net: float
    by_instrument: dict[str, float] = Field(default_factory=dict)


def require_fields_for_verdict(
    verdict: str,
    required: dict[str, Any],
    mapping: dict[str, set[str]],
) -> None:
    """Helper interne — lève ValueError si champs manquants pour un verdict."""
    needed = mapping.get(verdict, set())
    missing = [k for k in needed if required.get(k) is None]
    if missing:
        raise ValueError(f"verdict {verdict!r} requires fields: {missing}")
