"""C01 — Experiment."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, model_validator

from quant.contracts.base import (
    ArtifactRef,
    ContractRef,
    DataSplits,
    DatasetSnapshotRef,
    GateResult,
    GateVerdict,
    PromotionRecord,
)

CONTRACT_ID = "C01"
CONTRACT_VERSION = "1.0"


class ExperimentProtocol(str, Enum):
    STATISTICAL = "statistical"
    PREDICTIVE = "predictive"
    ECONOMIC = "economic"
    PAPER = "paper"
    OPERATIONAL = "operational"
    EXPLORATORY = "exploratory"


class Experiment(BaseModel):
    """Unité reproductible d'investigation."""

    contract_id: str = Field(default=CONTRACT_ID, frozen=True)
    contract_version: str = Field(default=CONTRACT_VERSION)
    experiment_id: str
    hypothesis: str
    success_criteria: list[str]
    dataset_snapshot_ref: DatasetSnapshotRef
    baselines: list[str]
    gates: list[GateResult]
    protocol: ExperimentProtocol
    contract_refs: ContractRef = Field(default_factory=ContractRef)
    experiment_run_id: str | None = None
    implementation_version: str | None = None
    git_commit: str | None = None
    promotion_record: PromotionRecord | None = None
    artifacts: list[ArtifactRef] = Field(default_factory=list)
    data_splits: DataSplits | None = None
    non_goals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_experiment_invariants(self) -> Experiment:
        if not self.baselines:
            raise ValueError("at least one baseline is required (SCI-000)")

        if self.protocol in {
            ExperimentProtocol.PREDICTIVE,
            ExperimentProtocol.ECONOMIC,
            ExperimentProtocol.PAPER,
            ExperimentProtocol.OPERATIONAL,
        } and self.data_splits is None:
            raise ValueError(
                f"data_splits required for protocol {self.protocol.value}"
            )
        return self

    def is_closed(self) -> bool:
        """True si toutes les gates ont un verdict final."""
        return all(g.verdict != GateVerdict.PENDING for g in self.gates)

    def assert_closed(self) -> None:
        if not self.is_closed():
            pending = [g.gate_id for g in self.gates if g.verdict == GateVerdict.PENDING]
            raise ValueError(f"experiment not closed; pending gates: {pending}")
