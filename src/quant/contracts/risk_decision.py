"""C05 — RiskDecision (souverain)."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator

from quant.contracts.base import AuthorizedExposure, SignalRef

CONTRACT_ID = "C05"
CONTRACT_VERSION = "1.0"


class RiskVerdict(str, Enum):
    AUTHORISE = "AUTHORISE"
    REDUCE = "REDUCE"
    DELAY = "DELAY"
    VETO = "VETO"
    NO_TRADE = "NO_TRADE"


class RiskDecision(BaseModel):
    """Verdict souverain du Risk Engine."""

    contract_id: str = Field(default=CONTRACT_ID, frozen=True)
    contract_version: str = Field(default=CONTRACT_VERSION)
    decision_id: str
    verdict: RiskVerdict
    signal_refs: list[SignalRef] = Field(default_factory=list)
    decided_at: datetime
    authorized_exposure: AuthorizedExposure | None = None
    constraints_applied: list[str] = Field(default_factory=list)
    veto_reason: str | None = None
    reduce_factor: float | None = None
    delay_until: datetime | None = None
    risk_budget_ref: str | None = None

    @model_validator(mode="after")
    def validate_verdict_fields(self) -> RiskDecision:
        if self.verdict == RiskVerdict.REDUCE:
            if self.reduce_factor is None:
                raise ValueError("reduce_factor required for REDUCE")
            if not 0.0 <= self.reduce_factor <= 1.0:
                raise ValueError("reduce_factor must be in [0, 1]")

        if self.verdict == RiskVerdict.DELAY and self.delay_until is None:
            raise ValueError("delay_until required for DELAY")

        if self.verdict in {RiskVerdict.VETO, RiskVerdict.NO_TRADE}:
            if not self.veto_reason:
                raise ValueError(f"veto_reason required for {self.verdict.value}")

        if self.verdict in {RiskVerdict.VETO, RiskVerdict.NO_TRADE}:
            if self.authorized_exposure is not None:
                raise ValueError(
                    f"authorized_exposure must be absent for {self.verdict.value}"
                )

        if self.verdict == RiskVerdict.NO_TRADE and not self.signal_refs:
            # NO_TRADE système sans signal — autorisé avec veto_reason explicite
            pass
        elif self.verdict != RiskVerdict.NO_TRADE and not self.signal_refs:
            raise ValueError("signal_refs required unless system-level NO_TRADE")

        return self

    @property
    def is_no_trade(self) -> bool:
        return self.verdict == RiskVerdict.NO_TRADE
