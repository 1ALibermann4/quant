"""C02 — DatasetSnapshot."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, model_validator

CONTRACT_ID = "C02"
CONTRACT_VERSION = "1.0"


class AdjustmentRecord(BaseModel):
    type: str
    description: str
    applied_at: datetime


class Provenance(BaseModel):
    source_label: str
    universe_description: str
    time_range_start: datetime
    time_range_end: datetime
    survivorship_bias_acknowledged: bool


class DatasetSnapshot(BaseModel):
    """Empreinte versionnée et provenance d'un ensemble de données figé."""

    contract_id: str = Field(default=CONTRACT_ID, frozen=True)
    contract_version: str = Field(default=CONTRACT_VERSION)
    snapshot_id: str
    fingerprint: str
    as_of: datetime
    availability_cutoff: datetime
    provenance: Provenance
    instruments: list[str] = Field(default_factory=list)
    adjustments: list[AdjustmentRecord] = Field(default_factory=list)
    quality_flags: list[str] = Field(default_factory=list)
    storage_hint: str | None = Field(
        default=None,
        description="Indication non normative — format de stockage différé",
    )

    @model_validator(mode="after")
    def validate_temporal_bounds(self) -> DatasetSnapshot:
        if self.availability_cutoff > self.as_of:
            raise ValueError(
                "availability_cutoff must be <= as_of (anti look-ahead)"
            )
        prov = self.provenance
        if prov.time_range_start >= prov.time_range_end:
            raise ValueError("time_range_start must be < time_range_end")
        return self
