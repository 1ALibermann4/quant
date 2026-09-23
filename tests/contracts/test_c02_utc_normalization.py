"""
CA-03 / HAT3-A1 / HAT3-A2 — frontière temporelle unique : datetime aware → UTC canonique.

Après validation, aucun tzinfo fourni par l'appelant n'est conservé ; fold et offsets
équivalents se réduisent au même instant UTC.
"""

from datetime import datetime, timedelta, time, timezone, tzinfo
from zoneinfo import ZoneInfo

import pytest
from c02_synthetic import snapshot_kwargs, synthetic_calendar
from pydantic import ValidationError

from quant.contracts import DatasetSnapshot, EarlyClose, MarketCalendarSnapshot
from quant.contracts.canonical import canonical_table_bytes, to_canonical_utc

UTC = timezone.utc
NY = ZoneInfo("America/New_York")


class HostileTZ(tzinfo):
    """tzinfo mutable (modèle LocalTimezone de la documentation Python)."""

    def __init__(self) -> None:
        self.offset = timedelta(0)

    def utcoffset(self, dt):
        return self.offset

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "HOSTILE"


def test_hat3_a1_fold_fallback_rejected_when_cutoff_after_as_of():
    """2020-11-01 01:20 fold=1 (06:20Z) > 01:30 fold=0 (05:30Z) → INV-01."""
    kw = snapshot_kwargs()
    as_of = datetime(2020, 11, 1, 1, 30, tzinfo=NY)
    cutoff = datetime(2020, 11, 1, 1, 20, fold=1, tzinfo=NY)
    assert cutoff.astimezone(UTC) > as_of.astimezone(UTC)
    with pytest.raises(ValidationError, match="availability_cutoff"):
        DatasetSnapshot(**{**kw, "as_of": as_of, "availability_cutoff": cutoff})


def test_hat3_a1_same_wall_clock_two_folds_are_distinct_instants():
    a = datetime(2020, 11, 1, 1, 45, tzinfo=NY)  # 05:45Z
    b = datetime(2020, 11, 1, 1, 45, fold=1, tzinfo=NY)  # 06:45Z
    cols = [{"name": "t", "type": "datetime"}]
    with pytest.raises(ValueError, match="duplicate"):
        canonical_table_bytes(cols, ["t"], [{"t": a}, {"t": a}])
    raw = canonical_table_bytes(cols, ["t"], [{"t": a}, {"t": b}])
    utc = canonical_table_bytes(cols, ["t"], [{"t": a.astimezone(UTC)}, {"t": b.astimezone(UTC)}])
    assert raw == utc
    assert raw.index(b"2020-11-01T05:45:00.000000Z") < raw.index(b"2020-11-01T06:45:00.000000Z")


def test_hat3_a1_qct_datetime_pk_orders_by_utc_not_wall_clock():
    early_utc = datetime(2020, 11, 1, 1, 45, tzinfo=NY)  # 05:45Z
    later_wall_earlier_looking = datetime(2020, 11, 1, 1, 15, fold=1, tzinfo=NY)  # 06:15Z
    cols = [{"name": "t", "type": "datetime"}]
    ny = canonical_table_bytes(cols, ["t"], [{"t": early_utc}, {"t": later_wall_earlier_looking}])
    utc = canonical_table_bytes(
        cols, ["t"],
        [{"t": early_utc.astimezone(UTC)}, {"t": later_wall_earlier_looking.astimezone(UTC)}],
    )
    assert ny == utc == (
        b"t\n2020-11-01T05:45:00.000000Z\n2020-11-01T06:15:00.000000Z\n"
    )


def test_equivalent_offsets_store_the_same_utc_instant():
    kw = snapshot_kwargs()
    ny = datetime(2020, 7, 15, 12, 0, tzinfo=NY)
    utc = ny.astimezone(UTC)
    offset = datetime(2020, 7, 15, 16, 0, tzinfo=timezone(timedelta(hours=0)))  # 16:00Z
    a = DatasetSnapshot(**{**kw, "as_of": datetime(2020, 7, 15, 18, 0, tzinfo=UTC),
                           "availability_cutoff": ny})
    b = DatasetSnapshot(**{**kw, "as_of": datetime(2020, 7, 15, 18, 0, tzinfo=UTC),
                           "availability_cutoff": utc})
    assert a.availability_cutoff == b.availability_cutoff
    assert a.availability_cutoff.tzinfo is timezone.utc
    assert a.availability_cutoff == datetime(2020, 7, 15, 16, 0, tzinfo=UTC)
    assert offset == a.availability_cutoff  # 16:00Z == 12:00 NY in July


def test_hat3_a2_hostile_tzinfo_is_not_aliased():
    tz = HostileTZ()
    kw = snapshot_kwargs()
    snap = DatasetSnapshot(
        **{**kw, "availability_cutoff": datetime(2020, 7, 15, 12, 0, tzinfo=tz)}
    )
    assert snap.availability_cutoff.tzinfo is timezone.utc
    assert snap.availability_cutoff.tzinfo is not tz
    before = snap.model_dump_json()
    tz.offset = timedelta(hours=-5)
    assert snap.availability_cutoff <= snap.as_of
    assert snap.model_dump_json() == before


def test_spring_forward_gap_is_converted_or_rejected_consistently():
    """2020-03-08 02:30 n'existe pas à New York ; ZoneInfo lève ou fold-normalise."""
    gap = datetime(2020, 3, 8, 2, 30, tzinfo=NY)
    utc = to_canonical_utc(gap)
    assert utc.tzinfo is timezone.utc
    kw = snapshot_kwargs()
    snap = DatasetSnapshot(
        **{**kw, "as_of": datetime(2020, 3, 8, 12, 0, tzinfo=UTC), "availability_cutoff": gap}
    )
    assert snap.availability_cutoff == utc


def test_local_time_fold_rejected():
    cal = synthetic_calendar()
    with pytest.raises(ValidationError, match="fold"):
        MarketCalendarSnapshot(
            **{**dict(cal), "regular_close_local": time(16, 0, fold=1)}
        )
    with pytest.raises(ValidationError, match="fold"):
        EarlyClose(session=cal.sessions[0], close_local=time(13, 0, fold=1))
