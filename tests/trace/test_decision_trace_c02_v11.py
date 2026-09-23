"""Compatibilité C02 v1.1 avec C01 / C03 / C04 / C05 et DecisionTrace (invariant I4)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "contracts"))

from c02_synthetic import synthetic_snapshot  # noqa: E402

from quant.contracts.base import (  # noqa: E402
    ContractRef,
    DatasetSnapshotRef,
    GateResult,
    GateVerdict,
    MarketStateRef,
    SignalRef,
)
from quant.contracts.experiment import Experiment, ExperimentProtocol  # noqa: E402
from quant.contracts.market_state import MarketState  # noqa: E402
from quant.contracts.risk_decision import RiskDecision, RiskVerdict  # noqa: E402
from quant.contracts.strategy_signal import SignalDirection, StrategySignal  # noqa: E402
from quant.trace.decision_trace import DecisionTrace  # noqa: E402


def test_decision_trace_accepts_v11_snapshot_unchanged():
    snap = synthetic_snapshot()
    ref = DatasetSnapshotRef(snapshot_id=snap.snapshot_id, fingerprint=snap.fingerprint)
    ms = MarketState(market_state_id="ms-v11", as_of=snap.availability_cutoff,
                     dataset_snapshot_ref=ref)
    signal = StrategySignal(
        signal_id="sig-v11",
        strategy_id="fixture",
        strategy_version="0.0.0",
        market_state_ref=MarketStateRef(market_state_id=ms.market_state_id, as_of=ms.as_of),
        direction=SignalDirection.NEUTRAL,
        raw_signal=0.0,
        confidence=0.5,
    )
    decision = RiskDecision(
        decision_id="rd-v11",
        verdict=RiskVerdict.NO_TRADE,
        signal_refs=[SignalRef(signal_id=signal.signal_id, strategy_id=signal.strategy_id)],
        decided_at=snap.as_of,
        veto_reason="fixture NO_TRADE",
    )
    experiment = Experiment(
        experiment_id="I00-v11",
        hypothesis="fixture",
        success_criteria=["structure validates"],
        dataset_snapshot_ref=ref,
        baselines=["B0"],
        gates=[GateResult(gate_id="G", description="d", verdict=GateVerdict.PASS)],
        protocol=ExperimentProtocol.EXPLORATORY,
        contract_refs=ContractRef(c02="1.1"),
    )
    trace = DecisionTrace(
        experiment=experiment,
        dataset_snapshot=snap,
        market_state=ms,
        strategy_signals=[signal],
        risk_decision=decision,
    )
    trace.verify_fingerprint_chain()
    assert experiment.contract_refs.c02 == "1.1"
