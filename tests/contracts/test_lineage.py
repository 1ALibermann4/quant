"""Tests C02 v1.1 — TransformationRecord, chaînage et déterminisme."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from quant.contracts.canonical import sha256_fingerprint
from quant.contracts.knowledge import Knowable
from quant.contracts.lineage import (
    TransformationRecord,
    assert_deterministic,
    lineage_fingerprint,
    verify_lineage,
)

UTC = timezone.utc
RAW = sha256_fingerprint(b"raw")
MID = sha256_fingerprint(b"mid")
OUT = sha256_fingerprint(b"out")
CAL = sha256_fingerprint(b"calendar")


def record(step, inputs, output, **overrides):
    fields = {
        "step_index": step,
        "transformation_id": f"t{step}",
        "transformation_type": "PARSE",
        "implementation_version": "0.1.0",
        "parameters": {"p": "x"},
        "input_fingerprints": tuple(inputs),
        "output_fingerprint": output,
        "executed_at": datetime(2020, 1, 1, tzinfo=UTC),
        "observations_in": Knowable.known(10),
        "observations_out": Knowable.known(9),
        "observations_dropped": Knowable.known(1),
    }
    fields.update(overrides)
    return TransformationRecord(**fields)


def test_valid_chain():
    chain = (record(0, [RAW], MID), record(1, [MID, CAL], OUT))
    verify_lineage(chain, source_hashes=(RAW,), terminal_fingerprint=OUT, auxiliary_hashes=(CAL,))


def test_step_order_enforced():
    chain = (record(1, [RAW], MID), record(0, [MID], OUT))
    with pytest.raises(ValueError, match="step_index"):
        verify_lineage(chain, source_hashes=(RAW,), terminal_fingerprint=OUT)


def test_input_must_come_from_source_or_earlier_step():
    chain = (record(0, [MID], OUT),)
    with pytest.raises(ValueError, match="neither a source artifact"):
        verify_lineage(chain, source_hashes=(RAW,), terminal_fingerprint=OUT)
    forward = (record(0, [RAW, OUT], MID), record(1, [MID], OUT))
    with pytest.raises(ValueError, match="neither a source artifact"):
        verify_lineage(forward, source_hashes=(RAW,), terminal_fingerprint=OUT)


def test_undeclared_calendar_input_rejected():
    chain = (record(0, [RAW], MID), record(1, [MID, CAL], OUT))
    with pytest.raises(ValueError, match="auxiliary"):
        verify_lineage(chain, source_hashes=(RAW,), terminal_fingerprint=OUT)


def test_terminal_must_match_dataset_fingerprint():
    chain = (record(0, [RAW], MID),)
    with pytest.raises(ValueError, match="dataset fingerprint"):
        verify_lineage(chain, source_hashes=(RAW,), terminal_fingerprint=OUT)


def test_every_source_consumed():
    other = sha256_fingerprint(b"other-raw")
    chain = (record(0, [RAW], OUT),)
    with pytest.raises(ValueError, match="never consumed"):
        verify_lineage(chain, source_hashes=(RAW, other), terminal_fingerprint=OUT)


def test_outputs_unique_and_distinct_from_inputs():
    with pytest.raises(ValidationError, match="differ from its inputs"):
        record(0, [RAW], RAW)
    dup = (record(0, [RAW], MID), record(1, [MID], OUT), record(2, [OUT], MID))
    with pytest.raises(ValueError, match="not unique"):
        verify_lineage(dup, source_hashes=(RAW,), terminal_fingerprint=MID)


def test_hat3_m5_output_equal_to_unused_auxiliary_is_rejected():
    """INV-10 : unicité dans l'univers (sources + auxiliaires + sorties), pas seulement vs entrées."""
    chain = (record(0, [RAW], CAL),)
    with pytest.raises(ValueError, match="not unique"):
        verify_lineage(chain, source_hashes=(RAW,), terminal_fingerprint=CAL, auxiliary_hashes=(CAL,))


def test_hat3_m7_surrogate_in_transformation_id_rejected_at_construction():
    with pytest.raises(ValidationError, match="UTF-8"):
        record(0, [RAW], OUT, transformation_id="t\ud800")


def test_empty_lineage_rejected():
    with pytest.raises(ValueError, match="at least one"):
        verify_lineage((), source_hashes=(RAW,), terminal_fingerprint=OUT)


def test_observation_arithmetic():
    with pytest.raises(ValidationError, match="observations_out"):
        record(0, [RAW], OUT, observations_dropped=Knowable.known(0))
    with pytest.raises(ValidationError, match=">= 0"):
        record(0, [RAW], OUT, observations_dropped=Knowable.known(-1),
               observations_out=Knowable.known(11))
    partial = record(0, [RAW], OUT, observations_dropped=Knowable.unknown())
    assert not partial.observations_dropped.is_known


def test_execution_timestamp_excluded_from_identity():
    a = record(0, [RAW], OUT)
    b = record(0, [RAW], OUT, executed_at=datetime(2030, 6, 1, tzinfo=UTC))
    assert a.application_key == b.application_key
    assert lineage_fingerprint((a,)) == lineage_fingerprint((b,))


@pytest.mark.parametrize(
    "change",
    [
        {"implementation_version": "0.2.0"},
        {"parameters": {"p": "y"}},
        {"transformation_id": "other"},
        {"transformation_type": "SORT"},
    ],
)
def test_identity_changes_with_version_parameters_and_type(change):
    assert record(0, [RAW], OUT).application_key != record(0, [RAW], OUT, **change).application_key


def test_parameter_key_order_irrelevant():
    a = record(0, [RAW], OUT, parameters={"a": "1", "b": "2"})
    b = record(0, [RAW], OUT, parameters={"b": "2", "a": "1"})
    assert a.application_key == b.application_key


def test_determinism_violation_detected():
    a = record(0, [RAW], MID)
    b = record(1, [RAW], OUT, transformation_id="t0")
    with pytest.raises(ValueError, match="non-deterministic"):
        assert_deterministic((a, b))


def test_parameters_reject_credentials_in_keys_and_values():
    with pytest.raises(ValidationError, match="K1"):
        record(0, [RAW], OUT, parameters={"api_key": "x"})
    with pytest.raises(ValidationError, match="V1"):
        record(0, [RAW], OUT, parameters={"note": "Authorization: Bearer x"})
    with pytest.raises(ValidationError, match="V2"):
        record(0, [RAW], OUT, parameters={"cols": ["a", "Bearer zzz.9876"]})


def test_parameters_accept_ordinary_sort_key():
    r = record(0, [RAW], OUT, parameters={"key": "session_date", "columns": ["a", "b"]})
    assert r.parameters["key"] == "session_date"


def test_executed_at_timezone_required_and_inputs_non_empty():
    with pytest.raises(ValidationError, match="timezone-aware"):
        record(0, [RAW], OUT, executed_at=datetime(2020, 1, 1))
    with pytest.raises(ValidationError, match="must not be empty"):
        record(0, [], OUT)
