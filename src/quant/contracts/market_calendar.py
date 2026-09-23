"""C02 v1.1 — MarketCalendarSnapshot : calendrier de séances matérialisé et versionné."""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from datetime import date, datetime, time
from typing import Any
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from quant.contracts.canonical import (
    QCC_1,
    canonical_calendar_bytes,
    canonical_json_fingerprint,
    require_iana_timezone,
    require_sha256_fingerprint,
    sha256_fingerprint,
)
from quant.contracts.knowledge import Knowable

CONTRACT_ID = "C02"
CONTRACT_VERSION = "1.1"


class EarlyClose(BaseModel):
    model_config = ConfigDict(frozen=True, revalidate_instances="always")

    session: date
    close_local: time


def _calendar_content_identity(
    *,
    market: str,
    timezone: str,
    regular_close_local: time,
    early_closes: tuple[EarlyClose, ...],
    sessions_fingerprint: str,
) -> dict[str, Any]:
    return {
        "kind": "C02.market_calendar",
        "canonical_representation": QCC_1,
        "market": market,
        "timezone": timezone,
        "regular_close_local": regular_close_local,
        "early_closes": [
            {"session": e.session, "close_local": e.close_local}
            for e in sorted(early_closes, key=lambda e: e.session)
        ],
        "sessions_fingerprint": sessions_fingerprint,
    }


class MarketCalendarSnapshot(BaseModel):
    """
    Liste matérialisée des séances utilisées pour les calculs en rangs.

    Identité de contenu (`content_fingerprint`) : marché, fuseau, heure de clôture régulière,
    clôtures anticipées et `sessions_fingerprint`. `source`, `source_version` et
    `generated_at` décrivent l'origine et n'entrent pas dans l'identité : deux sources
    produisant exactement le même contenu ont la même empreinte.
    """

    model_config = ConfigDict(frozen=True, revalidate_instances="always")

    contract_id: str = Field(default=CONTRACT_ID, frozen=True)
    contract_version: str = CONTRACT_VERSION
    calendar_snapshot_id: str
    market: str
    timezone: str
    source: Knowable[str]
    source_version: Knowable[str]
    generated_at: datetime
    regular_close_local: time
    early_closes: tuple[EarlyClose, ...] = ()
    sessions: tuple[date, ...]
    first_session: date
    last_session: date
    session_count: int
    canonical_representation: str = QCC_1
    sessions_fingerprint: str
    content_fingerprint: str

    @field_validator("timezone")
    @classmethod
    def _valid_timezone(cls, v: str) -> str:
        return require_iana_timezone(v)

    @field_validator("sessions_fingerprint", "content_fingerprint")
    @classmethod
    def _fingerprint_format(cls, v: str) -> str:
        return require_sha256_fingerprint(v, "calendar fingerprint")

    @field_validator("generated_at")
    @classmethod
    def _generated_at_aware(cls, v: datetime) -> datetime:
        if v.tzinfo is None or v.utcoffset() is None:
            raise ValueError("generated_at must be timezone-aware (UTC)")
        return v

    @model_validator(mode="after")
    def _consistency(self) -> MarketCalendarSnapshot:
        if self.canonical_representation != QCC_1:
            raise ValueError(f"unsupported calendar representation {self.canonical_representation}")
        if self.regular_close_local.tzinfo is not None:
            raise ValueError("regular_close_local must be a naive local time")
        raw = canonical_calendar_bytes(self.sessions)
        if self.first_session != self.sessions[0] or self.last_session != self.sessions[-1]:
            raise ValueError("first_session/last_session inconsistent with sessions")
        if self.session_count != len(self.sessions):
            raise ValueError("session_count inconsistent with sessions")
        if self.sessions_fingerprint != sha256_fingerprint(raw):
            raise ValueError("sessions_fingerprint does not match the QCC-1 session list")
        session_set = set(self.sessions)
        seen: set[date] = set()
        for early in self.early_closes:
            if early.session not in session_set:
                raise ValueError(f"early close {early.session} is not a calendar session")
            if early.session in seen:
                raise ValueError(f"duplicate early close {early.session}")
            if early.close_local.tzinfo is not None or early.close_local >= self.regular_close_local:
                raise ValueError(f"early close {early.session} must precede the regular close")
            seen.add(early.session)
        if self.content_fingerprint != self.compute_content_fingerprint():
            raise ValueError("content_fingerprint does not match calendar content")
        return self

    def content_identity(self) -> dict[str, Any]:
        return _calendar_content_identity(
            market=self.market,
            timezone=self.timezone,
            regular_close_local=self.regular_close_local,
            early_closes=self.early_closes,
            sessions_fingerprint=self.sessions_fingerprint,
        )

    def compute_content_fingerprint(self) -> str:
        return canonical_json_fingerprint(self.content_identity())

    def ref(self) -> MarketCalendarRef:
        return MarketCalendarRef(
            calendar_snapshot_id=self.calendar_snapshot_id,
            content_fingerprint=self.content_fingerprint,
        )

    def contains(self, session: date) -> bool:
        i = bisect_left(self.sessions, session)
        return i < len(self.sessions) and self.sessions[i] == session

    def rank(self, session: date) -> int:
        """Rang 0-indexé d'une séance (CAL-04) ; erreur si la date n'est pas une séance."""
        i = bisect_left(self.sessions, session)
        if i == len(self.sessions) or self.sessions[i] != session:
            raise ValueError(f"{session} is not a session of calendar {self.calendar_snapshot_id}")
        return i

    def sessions_between(self, first: date, last: date) -> int:
        """Nombre de séances dans [first, last] (bornes incluses)."""
        return bisect_right(self.sessions, last) - bisect_left(self.sessions, first)

    def close_instant(self, session: date) -> datetime:
        """Instant de clôture officielle (clôture anticipée comprise), fuseau du calendrier."""
        self.rank(session)
        close = next(
            (e.close_local for e in self.early_closes if e.session == session),
            self.regular_close_local,
        )
        return datetime.combine(session, close, tzinfo=ZoneInfo(self.timezone))


def build_market_calendar(
    *,
    calendar_snapshot_id: str,
    market: str,
    timezone: str,
    source: Knowable[str],
    source_version: Knowable[str],
    generated_at: datetime,
    regular_close_local: time,
    sessions: tuple[date, ...],
    early_closes: tuple[EarlyClose, ...] = (),
) -> MarketCalendarSnapshot:
    """Construit un snapshot en calculant les champs dérivés et les empreintes."""
    sessions_fp = sha256_fingerprint(canonical_calendar_bytes(sessions))
    identity = _calendar_content_identity(
        market=market,
        timezone=timezone,
        regular_close_local=regular_close_local,
        early_closes=early_closes,
        sessions_fingerprint=sessions_fp,
    )
    return MarketCalendarSnapshot(
        calendar_snapshot_id=calendar_snapshot_id,
        market=market,
        timezone=timezone,
        source=source,
        source_version=source_version,
        generated_at=generated_at,
        regular_close_local=regular_close_local,
        early_closes=early_closes,
        sessions=sessions,
        first_session=sessions[0],
        last_session=sessions[-1],
        session_count=len(sessions),
        sessions_fingerprint=sessions_fp,
        content_fingerprint=canonical_json_fingerprint(identity),
    )


class MarketCalendarRef(BaseModel):
    """Référence immuable d'un DatasetSnapshot vers un MarketCalendarSnapshot."""

    model_config = ConfigDict(frozen=True, revalidate_instances="always")

    calendar_snapshot_id: str
    content_fingerprint: str

    @field_validator("content_fingerprint")
    @classmethod
    def _fingerprint_format(cls, v: str) -> str:
        return require_sha256_fingerprint(v, "calendar content_fingerprint")
