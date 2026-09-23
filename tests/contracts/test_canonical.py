"""Tests des représentations canoniques QCJ-1 / QCT-1 / QCC-1 et des vecteurs normatifs."""

import hashlib
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal

import pytest

from quant.contracts.canonical import (
    canonical_calendar_bytes,
    canonical_json_bytes,
    canonical_table_bytes,
    format_decimal,
    raw_artifact_set_fingerprint,
    sha256_fingerprint,
)

UTC = timezone.utc

VECTOR_COLUMNS = [
    {"name": "session_date", "type": "date", "nullable": False},
    {"name": "adjusted_close", "type": "decimal", "scale": 6, "nullable": False},
    {"name": "close", "type": "decimal", "scale": 4, "nullable": True},
]
VECTOR_ROWS = [
    {"session_date": date(2020, 1, 3), "adjusted_close": "101.5", "close": None},
    {"session_date": date(2020, 1, 2), "adjusted_close": Decimal("100.1234565"), "close": 100},
]
VECTOR_QCT_BYTES = (
    b"session_date,adjusted_close,close\n"
    b"2020-01-02,100.123456,100.0000\n"
    b"2020-01-03,101.500000,\n"
)
VECTOR_QCC_BYTES = b"2020-01-02\n2020-01-03\n2020-01-06\n"
VECTOR_QCJ_BYTES = '{"a":[1,true,null],"b":"é","d":"2020-01-02","t":"2020-01-02T21:00:00.000000Z"}'.encode()


def test_qct_vector_bytes():
    assert canonical_table_bytes(VECTOR_COLUMNS, ["session_date"], VECTOR_ROWS) == VECTOR_QCT_BYTES


VECTOR_QCT_SHA256 = "sha256:c815b68ff3ed0ee548e79700e2a9651b3365e0e79cb1ae5202151182469771d0"
VECTOR_QCC_SHA256 = "sha256:e481bd671c59e4d9b6da6f0a0ff7db42b2cbf70aae3bb6b24706ffd56fcf09c5"
VECTOR_QCJ_SHA256 = "sha256:4ad22465ed2282ab01f2f58a2ba885f36d8477f5a74bc0c38328b72c019b6828"


def test_qct_vector_hash_matches_independent_sha256():
    assert "sha256:" + hashlib.sha256(VECTOR_QCT_BYTES).hexdigest() == VECTOR_QCT_SHA256
    actual = sha256_fingerprint(
        canonical_table_bytes(VECTOR_COLUMNS, ["session_date"], VECTOR_ROWS)
    )
    assert actual == VECTOR_QCT_SHA256


def test_qcc_and_qcj_vector_hashes():
    sessions = [date(2020, 1, 2), date(2020, 1, 3), date(2020, 1, 6)]
    assert sha256_fingerprint(canonical_calendar_bytes(sessions)) == VECTOR_QCC_SHA256
    assert sha256_fingerprint(VECTOR_QCJ_BYTES) == VECTOR_QCJ_SHA256


def test_qct_row_order_independent_of_input_order():
    a = canonical_table_bytes(VECTOR_COLUMNS, ["session_date"], VECTOR_ROWS)
    b = canonical_table_bytes(VECTOR_COLUMNS, ["session_date"], list(reversed(VECTOR_ROWS)))
    assert a == b


def test_qct_numeric_input_forms_are_equivalent():
    forms = [Decimal("100.5"), "100.5", "1.005E2", 100.5]
    outputs = {format_decimal(v, 6) for v in forms}
    assert outputs == {"100.500000"}


def test_qct_rounding_half_even_on_exact_value():
    assert format_decimal("0.000015", 5) == "0.00002"
    assert format_decimal("0.000025", 5) == "0.00002"
    assert format_decimal("2.5", 0) == "2"
    assert format_decimal("3.5", 0) == "4"
    assert format_decimal(0.1, 20) == "0.10000000000000000555"


def test_qct_negative_zero_normalized():
    assert format_decimal("-0.0000001", 4) == "0.0000"


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), "NaN", "abc", True])
def test_qct_rejects_non_finite_or_invalid(bad):
    with pytest.raises(ValueError):
        format_decimal(bad, 4)


def test_qct_rejects_duplicate_key_and_null_in_required_column():
    dup = [VECTOR_ROWS[0], dict(VECTOR_ROWS[0])]
    with pytest.raises(ValueError, match="duplicate primary key"):
        canonical_table_bytes(VECTOR_COLUMNS, ["session_date"], dup)
    with pytest.raises(ValueError, match="non-nullable"):
        canonical_table_bytes(
            VECTOR_COLUMNS,
            ["session_date"],
            [{"session_date": date(2020, 1, 2), "adjusted_close": None}],
        )


def test_qct_rejects_columns_outside_schema_and_forbidden_chars():
    with pytest.raises(ValueError, match="outside schema"):
        canonical_table_bytes(
            VECTOR_COLUMNS, ["session_date"], [{**VECTOR_ROWS[0], "volume": 1}]
        )
    cols = [{"name": "k", "type": "string"}]
    with pytest.raises(ValueError, match="forbidden character"):
        canonical_table_bytes(cols, ["k"], [{"k": "a,b"}])


def test_qcc_vector_bytes_and_ordering():
    sessions = [date(2020, 1, 2), date(2020, 1, 3), date(2020, 1, 6)]
    assert canonical_calendar_bytes(sessions) == VECTOR_QCC_BYTES
    with pytest.raises(ValueError, match="strictly increasing"):
        canonical_calendar_bytes([date(2020, 1, 3), date(2020, 1, 2)])
    with pytest.raises(ValueError, match="strictly increasing"):
        canonical_calendar_bytes([date(2020, 1, 2), date(2020, 1, 2)])


def test_qcj_vector_bytes():
    ny_offset = timezone(timedelta(hours=-5))
    value = {
        "t": datetime(2020, 1, 2, 16, 0, tzinfo=ny_offset),
        "d": date(2020, 1, 2),
        "b": "é",
        "a": (1, True, None),
    }
    assert canonical_json_bytes(value) == VECTOR_QCJ_BYTES


def test_qcj_key_order_independent():
    assert canonical_json_bytes({"b": 1, "a": 2}) == canonical_json_bytes({"a": 2, "b": 1})


@pytest.mark.parametrize(
    "bad",
    [1.5, Decimal("1.5"), 2**53, datetime(2020, 1, 1), {1: "x"}, time(1, tzinfo=UTC), object()],
)
def test_qcj_rejects_non_canonicalizable(bad):
    with pytest.raises(ValueError):
        canonical_json_bytes({"x": bad})


def test_raw_artifact_set_is_order_insensitive_and_strict():
    h1 = sha256_fingerprint(b"a")
    h2 = sha256_fingerprint(b"b")
    assert raw_artifact_set_fingerprint([h1, h2]) == raw_artifact_set_fingerprint([h2, h1])
    assert raw_artifact_set_fingerprint([h1]) != h1
    with pytest.raises(ValueError, match="duplicate"):
        raw_artifact_set_fingerprint([h1, h1])
    with pytest.raises(ValueError, match="empty"):
        raw_artifact_set_fingerprint([])
    with pytest.raises(ValueError, match="sha256"):
        raw_artifact_set_fingerprint(["md5:abc"])


def test_raw_artifact_set_vector():
    h1 = sha256_fingerprint(b"a")
    h2 = sha256_fingerprint(b"b")
    payload = (
        '{"kind":"C02.raw_artifact_set","members":["' + min(h1, h2) + '","' + max(h1, h2) + '"]}'
    ).encode()
    assert raw_artifact_set_fingerprint([h2, h1]) == sha256_fingerprint(payload)
