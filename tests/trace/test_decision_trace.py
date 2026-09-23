"""Tests DecisionTrace — invariant I4."""

import pytest

from quant.trace.decision_trace import DecisionTrace


def test_decision_trace_chain(
    sample_snapshot,
    sample_market_state,
    sample_signal,
    sample_no_trade_decision,
    sample_experiment,
):
    trace = DecisionTrace(
        experiment=sample_experiment,
        dataset_snapshot=sample_snapshot,
        market_state=sample_market_state,
        strategy_signals=[sample_signal],
        risk_decision=sample_no_trade_decision,
    )
    trace.verify_fingerprint_chain()
    assert sample_no_trade_decision.decision_id in {
        sample_no_trade_decision.decision_id
    }
    assert sample_signal.signal_id in trace.signal_ids_in_risk_decision()


def test_fingerprint_mismatch_rejected(
    sample_snapshot,
    sample_market_state,
    sample_signal,
    sample_no_trade_decision,
):
    bad_state = sample_market_state.model_copy(
        update={
            "dataset_snapshot_ref": sample_market_state.dataset_snapshot_ref.model_copy(
                update={"fingerprint": "sha256:wrong"}
            )
        }
    )
    trace = DecisionTrace(
        dataset_snapshot=sample_snapshot,
        market_state=bad_state,
        strategy_signals=[sample_signal],
        risk_decision=sample_no_trade_decision,
    )
    with pytest.raises(ValueError, match="fingerprint"):
        trace.verify_fingerprint_chain()
