"""C03 — MarketState."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from quant.contracts.base import DatasetSnapshotRef

CONTRACT_ID = "C03"
CONTRACT_VERSION = "1.0"


class ExperimentalBranch(str, Enum):
    CLASSICAL = "classical"
    P_ADIC = "p_adic"
    DYNAMICS = "dynamics"


class FeatureRef(BaseModel):
    name: str
    version: str
    value_ref: str


class MarketState(BaseModel):
    """État de marché contextualisé à l'instant t."""

    contract_id: str = Field(default=CONTRACT_ID, frozen=True)
    contract_version: str = Field(default=CONTRACT_VERSION)
    market_state_id: str
    as_of: datetime
    dataset_snapshot_ref: DatasetSnapshotRef
    feature_refs: list[FeatureRef] = Field(default_factory=list)
    regime_label: str | None = None
    regime_uncertainty: float | None = None
    stability_indicators: dict[str, float] = Field(default_factory=dict)
    representation_id: str | None = None
    experimental_branch: ExperimentalBranch = ExperimentalBranch.CLASSICAL

    @field_validator("regime_uncertainty")
    @classmethod
    def validate_uncertainty_range(cls, v: float | None) -> float | None:
        if v is not None and not 0.0 <= v <= 1.0:
            raise ValueError("regime_uncertainty must be in [0, 1]")
        return v

    def assert_temporal_integrity(self, availability_cutoff: datetime) -> None:
        """Invariant I3 — as_of must not exceed dataset availability."""
        if self.as_of > availability_cutoff:
            raise ValueError(
                f"market_state.as_of ({self.as_of}) exceeds "
                f"availability_cutoff ({availability_cutoff})"
            )
