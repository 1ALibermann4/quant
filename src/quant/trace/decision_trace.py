"""Reconstruction intégrale d'une décision (invariant I4)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from quant.contracts.dataset_snapshot import DatasetSnapshot
from quant.contracts.experiment import Experiment
from quant.contracts.market_state import MarketState
from quant.contracts.risk_decision import RiskDecision
from quant.contracts.strategy_signal import StrategySignal


class DecisionTrace(BaseModel):
    """
    Chaîne C02 → C03 → C04 → C05 pour audit et reproductibilité.

    P0 : structure de traçabilité sans pipeline d'exécution.
    """

    experiment: Experiment | None = None
    dataset_snapshot: DatasetSnapshot
    market_state: MarketState
    strategy_signals: list[StrategySignal] = Field(default_factory=list)
    risk_decision: RiskDecision

    def verify_fingerprint_chain(self) -> None:
        """Vérifie la cohérence des empreintes et références."""
        ms_ref = self.market_state.dataset_snapshot_ref
        if ms_ref.snapshot_id != self.dataset_snapshot.snapshot_id:
            raise ValueError("market_state snapshot_id mismatch")
        if ms_ref.fingerprint != self.dataset_snapshot.fingerprint:
            raise ValueError("market_state fingerprint mismatch")

        for signal in self.strategy_signals:
            if signal.market_state_ref.market_state_id != self.market_state.market_state_id:
                raise ValueError(
                    f"signal {signal.signal_id} market_state_id mismatch"
                )

        self.market_state.assert_temporal_integrity(
            self.dataset_snapshot.availability_cutoff
        )

    def signal_ids_in_risk_decision(self) -> set[str]:
        return {ref.signal_id for ref in self.risk_decision.signal_refs}
