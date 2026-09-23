"""
Domaine des représentations canoniques (CA-02, HAT2-A3 / HAT2-A4 et audit transversal).

- années sur 4 chiffres dans tout le domaine 0001–9999 (QCJ-1, QCT-1, QCC-1) ;
- instant dont la conversion UTC sort du domaine → ValueError (pas d'OverflowError) ;
- décimaux : domaine de précision explicite, ValueError hors domaine, contexte global ignoré ;
- aucune exception interne (TypeError, KeyError, InvalidOperation) sur des entrées mal typées.
"""

import decimal
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal

import pytest

from quant.contracts.canonical import (
    QCT_DECIMAL_PRECISION,
    canonical_calendar_bytes,
    canonical_json_bytes,
    canonical_table_bytes,
    format_decimal,
    format_utc_datetime,
)

UTC = timezone.utc
YEARS = [1, 9, 10, 99, 100, 999, 1000, 1969, 2020, 9999]


@pytest.mark.parametrize("year", YEARS)
def test_instant_year_is_always_four_digits(year):
    value = datetime(year, 6, 15, 12, 30, 45, 7, tzinfo=UTC)
    expected = f"{year:04d}-06-15T12:30:45.000007Z"
    assert format_utc_datetime(value) == expected
    assert canonical_json_bytes({"t": value}) == f'{{"t":"{expected}"}}'.encode()
    cols = [{"name": "t", "type": "datetime"}]
    assert canonical_table_bytes(cols, ["t"], [{"t": value}]) == f"t\n{expected}\n".encode()


@pytest.mark.parametrize("year", YEARS)
def test_date_year_is_always_four_digits(year):
    d = date(year, 1, 2)
    expected = f"{year:04d}-01-02"
    assert canonical_json_bytes({"d": d}) == f'{{"d":"{expected}"}}'.encode()
    assert canonical_calendar_bytes([d]) == f"{expected}\n".encode()
    cols = [{"name": "d", "type": "date"}]
    assert canonical_table_bytes(cols, ["d"], [{"d": d}]) == f"d\n{expected}\n".encode()


def test_hat2_a3_reproduction_year_999():
    assert format_utc_datetime(datetime(999, 1, 1, tzinfo=UTC)) == "0999-01-01T00:00:00.000000Z"


def test_offset_conversion_at_domain_edges():
    plus1 = timezone(timedelta(hours=1))
    minus1 = timezone(timedelta(hours=-1))
    assert format_utc_datetime(datetime(1, 1, 1, 1, 0, tzinfo=plus1)) == "0001-01-01T00:00:00.000000Z"
    assert (
        format_utc_datetime(datetime(9999, 12, 31, 22, 59, 59, 999999, tzinfo=minus1))
        == "9999-12-31T23:59:59.999999Z"
    )
    for out_of_range in (
        datetime(1, 1, 1, 0, 30, tzinfo=plus1),
        datetime(9999, 12, 31, 23, 30, tzinfo=minus1),
    ):
        with pytest.raises(ValueError, match="outside the UTC range"):
            format_utc_datetime(out_of_range)
        with pytest.raises(ValueError):
            canonical_json_bytes({"t": out_of_range})


# ------------------------------------------------------------------------ décimaux


def test_hat2_a4_reproduction_decimal_out_of_domain_raises_value_error():
    with pytest.raises(ValueError, match="significant digits") as info:
        format_decimal(Decimal("1e30"), 6)
    assert not isinstance(info.value, decimal.InvalidOperation)


@pytest.mark.parametrize(
    ("value", "scale", "expected"),
    [
        (10**21, 6, "1000000000000000000000.000000"),
        ("9" * 22, 6, "9" * 22 + ".000000"),
        ("-" + "9" * 22 + ".4999994", 6, "-" + "9" * 22 + ".499999"),
        ("9" * QCT_DECIMAL_PRECISION, 0, "9" * QCT_DECIMAL_PRECISION),
        ("1e-999999999", 6, "0.000000"),
        ("-1e-30", 6, "0.000000"),
    ],
)
def test_decimal_domain_upper_edge_accepted(value, scale, expected):
    assert format_decimal(value, scale) == expected


@pytest.mark.parametrize(
    ("value", "scale"),
    [
        (10**22, 6),
        ("9" * 22 + ".9999995", 6),
        ("9" * (QCT_DECIMAL_PRECISION + 1), 0),
        ("1E+999999999", 0),
        (Decimal("1e30"), 0),
        (1e30, 6),
    ],
)
def test_decimal_beyond_domain_rejected_with_value_error(value, scale):
    with pytest.raises(ValueError, match="significant digits"):
        format_decimal(value, scale)


@pytest.mark.parametrize("scale", [-1, 1.0, True, "6"])
def test_decimal_scale_must_be_non_negative_integer(scale):
    with pytest.raises(ValueError, match="scale"):
        format_decimal("1.5", scale)


def test_decimal_result_independent_of_global_context():
    cases = [("100.1234565", 6), ("0.000025", 5), ("-0.0000001", 4), (0.1, 20), (10**21, 6)]
    reference = [format_decimal(v, s) for v, s in cases]
    with decimal.localcontext() as ctx:
        ctx.prec = 3
        ctx.rounding = decimal.ROUND_UP
        ctx.traps[decimal.Inexact] = True
        ctx.traps[decimal.Rounded] = True
        assert [format_decimal(v, s) for v, s in cases] == reference


# ------------------------------------------------------------ exceptions internes (audit)


def test_qct_mixed_types_in_primary_key_raise_value_error_not_type_error():
    cols = [{"name": "d", "type": "date"}]
    with pytest.raises(ValueError, match="expects a date"):
        canonical_table_bytes(cols, ["d"], [{"d": date(2020, 1, 2)}, {"d": "2020-01-03"}])
    with pytest.raises(ValueError, match="expects a date"):
        canonical_table_bytes(cols, ["d"], [{"d": date(2020, 1, 2)}, {"d": datetime(2020, 1, 3, tzinfo=UTC)}])


def test_qct_missing_primary_key_raises_value_error_not_key_error():
    cols = [{"name": "d", "type": "date"}, {"name": "v", "type": "integer", "nullable": True}]
    with pytest.raises(ValueError, match="non-nullable"):
        canonical_table_bytes(cols, ["d"], [{"v": 1}])


def test_qct_duplicate_column_names_rejected():
    cols = [{"name": "d", "type": "date"}, {"name": "d", "type": "string"}]
    with pytest.raises(ValueError, match="duplicate column"):
        canonical_table_bytes(cols, ["d"], [{"d": date(2020, 1, 2)}])


def test_qcc_mixed_date_and_datetime_raise_value_error_not_type_error():
    with pytest.raises(ValueError, match="must be dates"):
        canonical_calendar_bytes([date(2020, 1, 2), datetime(2020, 1, 3)])


def test_qcj_sub_second_local_time_rejected_to_avoid_identity_collision():
    assert canonical_json_bytes({"t": time(16, 0)}) == b'{"t":"16:00:00"}'
    with pytest.raises(ValueError, match="sub-second"):
        canonical_json_bytes({"t": time(16, 0, 0, 500000)})
