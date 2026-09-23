"""Tests C01 — Experiment."""

import pytest

from quant.contracts.base import DatasetSnapshotRef, GateResult, GateVerdict
from quant.contracts.experiment import Experiment, ExperimentProtocol


def test_experiment_requires_baseline(sample_snapshot):
    with pytest.raises(ValueError, match="baseline"):
        Experiment(
            experiment_id="I-bad",
            hypothesis="h",
            success_criteria=["c"],
            dataset_snapshot_ref=DatasetSnapshotRef(
                snapshot_id=sample_snapshot.snapshot_id,
                fingerprint=sample_snapshot.fingerprint,
            ),
            baselines=[],
            gates=[],
            protocol=ExperimentProtocol.EXPLORATORY,
        )


def test_predictive_requires_data_splits(sample_snapshot):
    with pytest.raises(ValueError, match="data_splits"):
        Experiment(
            experiment_id="I-bad",
            hypothesis="h",
            success_criteria=["c"],
            dataset_snapshot_ref=DatasetSnapshotRef(
                snapshot_id=sample_snapshot.snapshot_id,
                fingerprint=sample_snapshot.fingerprint,
            ),
            baselines=["B0"],
            gates=[],
            protocol=ExperimentProtocol.PREDICTIVE,
        )


def test_experiment_closure(sample_experiment):
    assert sample_experiment.is_closed()
    sample_experiment.assert_closed()


def test_pending_gate_not_closed(sample_snapshot):
    exp = Experiment(
        experiment_id="I-pending",
        hypothesis="h",
        success_criteria=["c"],
        dataset_snapshot_ref=DatasetSnapshotRef(
            snapshot_id=sample_snapshot.snapshot_id,
            fingerprint=sample_snapshot.fingerprint,
        ),
        baselines=["B0"],
        gates=[
            GateResult(
                gate_id="G1",
                description="pending",
                verdict=GateVerdict.PENDING,
            )
        ],
        protocol=ExperimentProtocol.EXPLORATORY,
    )
    assert not exp.is_closed()
    with pytest.raises(ValueError, match="pending"):
        exp.assert_closed()
