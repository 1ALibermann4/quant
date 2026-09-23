"""Tests C02 v1.1 — MarketCalendarSnapshot (fixtures synthétiques uniquement)."""

from datetime import date, datetime, time, timezone

import pytest
from c02_synthetic import EARLY_CLOSE_DAY, synthetic_calendar, weekdays
from pydantic import ValidationError

from quant.contracts.canonical import canonical_calendar_bytes, sha256_fingerprint
from quant.contracts.knowledge import Knowable
from quant.contracts.market_calendar import EarlyClose, MarketCalendarSnapshot

UTC = timezone.utc


def test_calendar_valid_and_fingerprints():
    cal = synthetic_calendar()
    assert cal.session_count == len(cal.sessions)
    assert cal.sessions_fingerprint == sha256_fingerprint(canonical_calendar_bytes(cal.sessions))
    assert cal.content_fingerprint == cal.compute_content_fingerprint()


def test_source_and_generation_metadata_excluded_from_identity():
    a = synthetic_calendar()
    b = synthetic_calendar(
        source=Knowable.known("another-library"), source_version=Knowable.known("9.9")
    )
    assert a.content_fingerprint == b.content_fingerprint
    c = a.model_copy(update={"generated_at": datetime(2030, 1, 1, tzinfo=UTC)})
    assert c.compute_content_fingerprint() == a.content_fingerprint


def test_session_list_change_changes_identity():
    a = synthetic_calendar()
    b = synthetic_calendar(last=date(2020, 12, 30))
    assert a.sessions_fingerprint != b.sessions_fingerprint
    assert a.content_fingerprint != b.content_fingerprint


def _kwargs(cal: MarketCalendarSnapshot, **overrides):
    fields = cal.model_dump()
    fields.update(overrides)
    return fields


def test_tampered_sessions_rejected():
    cal = synthetic_calendar()
    tampered = cal.sessions[:10] + cal.sessions[11:]
    with pytest.raises(ValidationError, match="first_session|session_count|sessions_fingerprint"):
        MarketCalendarSnapshot(**_kwargs(cal, sessions=tampered))


def test_bounds_and_count_consistency():
    cal = synthetic_calendar()
    with pytest.raises(ValidationError, match="session_count"):
        MarketCalendarSnapshot(**_kwargs(cal, session_count=cal.session_count + 1))
    with pytest.raises(ValidationError, match="first_session"):
        MarketCalendarSnapshot(**_kwargs(cal, first_session=date(2009, 1, 1)))


def test_content_fingerprint_mismatch_rejected():
    cal = synthetic_calendar()
    with pytest.raises(ValidationError, match="content_fingerprint"):
        MarketCalendarSnapshot(**_kwargs(cal, market="OTHER"))


def test_early_close_rules():
    cal = synthetic_calendar()
    saturday = date(2019, 7, 6)
    with pytest.raises(ValidationError, match="not a calendar session"):
        MarketCalendarSnapshot(
            **_kwargs(cal, early_closes=(EarlyClose(session=saturday, close_local=time(13)),))
        )
    with pytest.raises(ValidationError, match="precede the regular close"):
        MarketCalendarSnapshot(
            **_kwargs(cal, early_closes=(EarlyClose(session=EARLY_CLOSE_DAY, close_local=time(17)),))
        )


def test_invalid_timezone_rejected():
    cal = synthetic_calendar()
    with pytest.raises(ValidationError):
        MarketCalendarSnapshot(**_kwargs(cal, timezone="Mars/Olympus"))


def test_rank_is_session_rank_not_row_number():
    cal = synthetic_calendar()
    assert cal.rank(cal.first_session) == 0
    friday, monday = date(2010, 1, 8), date(2010, 1, 11)
    assert cal.rank(monday) - cal.rank(friday) == 1
    with pytest.raises(ValueError, match="not a session"):
        cal.rank(date(2010, 1, 9))


def test_sessions_between_and_contains():
    cal = synthetic_calendar()
    assert cal.sessions_between(date(2010, 1, 4), date(2010, 1, 15)) == 10
    assert cal.contains(date(2010, 1, 4))
    assert not cal.contains(date(2010, 1, 2))


def test_close_instant_regular_early_and_dst():
    cal = synthetic_calendar()
    winter = cal.close_instant(date(2010, 1, 4)).astimezone(UTC)
    summer = cal.close_instant(date(2010, 7, 6)).astimezone(UTC)
    early = cal.close_instant(EARLY_CLOSE_DAY).astimezone(UTC)
    assert (winter.hour, summer.hour, early.hour) == (21, 20, 17)


def test_weekday_fixture_is_synthetic():
    cal = synthetic_calendar()
    assert cal.market == "SYNTHETIC"
    assert cal.sessions == weekdays(cal.first_session, cal.last_session)
