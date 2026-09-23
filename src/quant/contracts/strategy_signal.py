"""C04 — StrategySignal."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator

from quant.contracts.base import MarketStateRef

CONTRACT_ID = "C04"
CONTRACT_VERSION = "1.0"


class SignalDirection(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    NEUTRAL = "NEUTRAL"
    ABSTAIN = "ABSTAIN"


class StrategySignal(BaseModel):
    """Proposition normalisée d'une stratégie — sans autorité de risque."""

    contract_id: str = Field(default=CONTRACT_ID, frozen=True)
    contract_version: str = Field(default=CONTRACT_VERSION)
    signal_id: str
    strategy_id: str
    strategy_version: str
    market_state_ref: MarketStateRef
    direction: SignalDirection
    raw_signal: float | None = None
    confidence: float | None = None
    expected_edge: float | None = None
    expected_risk: float | None = None
    validity_horizon: str | None = None
    evidence: list[str] = Field(default_factory=list)
    abstain_reason: str | None = None
    eligible_universe: list[str] = Field(default_factory=list)
    time_horizon: str | None = None

    @field_validator("confidence")
    @classmethod
    def validate_confidence_range(cls, v: float | None) -> float | None:
        if v is not None and not 0.0 <= v <= 1.0:
            raise ValueError("confidence must be in [0, 1]")
        return v

    @model_validator(mode="after")
    def validate_abstain_reason(self) -> StrategySignal:
        if self.direction == SignalDirection.ABSTAIN and not self.abstain_reason:
            raise ValueError("abstain_reason required when direction is ABSTAIN")
        return self
