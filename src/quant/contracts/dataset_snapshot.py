"""C02 — Data Provenance & Dataset Snapshot (v1.1, rétrocompatible v1.0)."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from datetime import date, datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from quant.contracts.canonical import (
    QCT_1,
    canonical_table_bytes,
    raw_artifact_set_fingerprint,
    require_iana_timezone,
    require_sha256_fingerprint,
    sha256_fingerprint,
)
from quant.contracts.immutable import FrozenList
from quant.contracts.knowledge import Knowable
from quant.contracts.lineage import (
    InstrumentIdentifiers,
    ProviderArtifact,
    ProviderArtifactRef,
    TransformationRecord,
    lineage_fingerprint,
    verify_lineage,
)
from quant.contracts.market_calendar import MarketCalendarRef, MarketCalendarSnapshot

CONTRACT_ID = "C02"
CONTRACT_VERSION = "1.1"
SUPPORTED_CONTRACT_VERSIONS = frozenset({"1.0", "1.1"})

V1_1_FIELDS = (
    "table_schema",
    "source_artifacts",
    "raw_fingerprint",
    "lineage",
    "market_calendar",
    "temporal_convention",
    "requested_range",
    "returned_range",
    "canonical_range",
    "counts",
    "adjustment_methodology",
    "instrument",
    "intended_use",
)

_COLUMN_NAME = re.compile(r"^[a-z][a-z0-9_]*$")


class AdjustmentRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: str
    description: str
    applied_at: datetime


class Provenance(BaseModel):
    model_config = ConfigDict(frozen=True)

    source_label: str
    universe_description: str
    time_range_start: datetime
    time_range_end: datetime
    survivorship_bias_acknowledged: bool


class ColumnSpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    type: Literal["date", "datetime", "decimal", "integer", "string"]
    scale: int | None = None
    nullable: bool = False

    @model_validator(mode="after")
    def _scale_iff_decimal(self) -> ColumnSpec:
        if not _COLUMN_NAME.match(self.name):
            raise ValueError(f"invalid column name {self.name!r}")
        if self.type == "decimal":
            if self.scale is None or not 0 <= self.scale <= 18:
                raise ValueError(f"decimal column {self.name!r} requires scale in [0, 18]")
        elif self.scale is not None:
            raise ValueError(f"scale is only allowed on decimal columns ({self.name!r})")
        return self


class TableSchema(BaseModel):
    """Schéma versionné de la table canonique ; porte la représentation QCT-1."""

    model_config = ConfigDict(frozen=True)

    schema_id: str
    schema_version: str
    canonical_representation: str = QCT_1
    columns: tuple[ColumnSpec, ...]
    primary_key: tuple[str, ...]

    @model_validator(mode="after")
    def _consistency(self) -> TableSchema:
        if self.canonical_representation != QCT_1:
            raise ValueError(f"unsupported table representation {self.canonical_representation}")
        names = [c.name for c in self.columns]
        if not names:
            raise ValueError("schema must declare at least one column")
        if len(set(names)) != len(names):
            raise ValueError("duplicate column names in schema")
        if not self.primary_key:
            raise ValueError("schema must declare a primary key")
        by_name = {c.name: c for c in self.columns}
        for key in self.primary_key:
            column = by_name.get(key)
            if column is None:
                raise ValueError(f"primary key column {key!r} not in schema")
            if column.type == "decimal" or column.nullable:
                raise ValueError(f"primary key column {key!r} must be orderable and non-null")
        return self

    def column(self, name: str) -> ColumnSpec | None:
        return next((c for c in self.columns if c.name == name), None)

    def canonical_bytes(self, rows: Iterable[Mapping[str, Any]]) -> bytes:
        return canonical_table_bytes(
            [c.model_dump() for c in self.columns], self.primary_key, rows
        )


class SessionRange(BaseModel):
    model_config = ConfigDict(frozen=True)

    first_session: date
    last_session: date

    @model_validator(mode="after")
    def _ordered(self) -> SessionRange:
        if self.first_session > self.last_session:
            raise ValueError("first_session must be <= last_session")
        return self

    def contains(self, other: SessionRange) -> bool:
        return (
            self.first_session <= other.first_session
            and other.last_session <= self.last_session
        )


class TemporalConvention(BaseModel):
    """Fuseaux source/canonique et règle de dérivation de `session_date` (TS-01…TS-04)."""

    model_config = ConfigDict(frozen=True)

    source_timezone: Knowable[str]
    canonical_timezone: str
    session_date_rule: str

    @field_validator("canonical_timezone")
    @classmethod
    def _valid_timezone(cls, v: str) -> str:
        return require_iana_timezone(v)


class ObservationCounts(BaseModel):
    model_config = ConfigDict(frozen=True)

    raw_observations: int = Field(ge=0)
    canonical_observations: int = Field(ge=0)
    expected_sessions: Knowable[int]
    missing_sessions: Knowable[int]
    invalidated_sessions: Knowable[int]

    @model_validator(mode="after")
    def _arithmetic(self) -> ObservationCounts:
        if self.canonical_observations > self.raw_observations:
            raise ValueError("canonical_observations must be <= raw_observations")
        for count in (self.expected_sessions, self.missing_sessions, self.invalidated_sessions):
            if count.is_known and count.value < 0:
                raise ValueError("session counts must be >= 0")
        if self.expected_sessions.is_known and self.missing_sessions.is_known:
            expected = self.expected_sessions.value
            if self.canonical_observations + self.missing_sessions.value != expected:
                raise ValueError(
                    "canonical_observations + missing_sessions must equal expected_sessions"
                )
        return self


class AdjustmentMethod(str, Enum):
    PROPORTIONAL = "PROPORTIONAL"
    ADDITIVE = "ADDITIVE"
    NONE = "NONE"


class AdjustmentReferenceDate(str, Enum):
    EX_DATE = "EX_DATE"
    PAYMENT_DATE = "PAYMENT_DATE"
    OTHER = "OTHER"


class AdjustmentMethodology(BaseModel):
    """Méthodologie d'ajustement, propriété du snapshot (DATA-REQ §3.3, §5)."""

    model_config = ConfigDict(frozen=True)

    events_covered: Knowable[tuple[str, ...]]
    method: Knowable[AdjustmentMethod]
    reference_date: Knowable[AdjustmentReferenceDate]
    dividend_factor_formula: Knowable[str]
    methodology_ref: Knowable[str]
    methodology_version: Knowable[str]
    numeric_precision: Knowable[str]
    currency: Knowable[str]


class DatasetSnapshot(BaseModel):
    """
    Objet scientifique immuable consommé par les expériences.

    `fingerprint` (v1.0, conservé) : empreinte du contenu. Lorsque `table_schema` est
    présent, c'est l'empreinte SHA-256 de la représentation QCT-1 de la table canonique.
    """

    model_config = ConfigDict(frozen=True)

    contract_id: str = Field(default=CONTRACT_ID, frozen=True)
    contract_version: str = Field(default=CONTRACT_VERSION)
    snapshot_id: str
    fingerprint: str
    as_of: datetime
    availability_cutoff: datetime
    provenance: Provenance
    instruments: FrozenList[str] = ()
    adjustments: FrozenList[AdjustmentRecord] = ()
    quality_flags: FrozenList[str] = ()
    storage_hint: str | None = Field(
        default=None,
        description="Indication non normative — format de stockage différé",
    )

    table_schema: TableSchema | None = None
    source_artifacts: tuple[ProviderArtifactRef, ...] = ()
    raw_fingerprint: str | None = None
    lineage: tuple[TransformationRecord, ...] = ()
    market_calendar: MarketCalendarRef | None = None
    temporal_convention: TemporalConvention | None = None
    requested_range: Knowable[SessionRange] | None = None
    returned_range: SessionRange | None = None
    canonical_range: SessionRange | None = None
    counts: ObservationCounts | None = None
    adjustment_methodology: AdjustmentMethodology | None = None
    instrument: InstrumentIdentifiers | None = None
    intended_use: str | None = None

    @model_validator(mode="after")
    def validate_temporal_bounds(self) -> DatasetSnapshot:
        if self.availability_cutoff > self.as_of:
            raise ValueError(
                "availability_cutoff must be <= as_of (anti look-ahead)"
            )
        prov = self.provenance
        if prov.time_range_start >= prov.time_range_end:
            raise ValueError("time_range_start must be < time_range_end")
        return self

    @model_validator(mode="after")
    def validate_v1_1_extensions(self) -> DatasetSnapshot:
        if self.contract_version not in SUPPORTED_CONTRACT_VERSIONS:
            raise ValueError(
                f"unsupported C02 contract_version {self.contract_version!r}; "
                f"supported: {sorted(SUPPORTED_CONTRACT_VERSIONS)}"
            )
        used = [name for name in V1_1_FIELDS if getattr(self, name) not in (None, ())]
        if self.contract_version == "1.0" and used:
            raise ValueError(f"C02 v1.0 object must not carry v1.1 fields: {used}")

        if self.table_schema is not None:
            require_sha256_fingerprint(self.fingerprint, "fingerprint")

        ids = [a.artifact_id for a in self.source_artifacts]
        hashes = [a.content_sha256 for a in self.source_artifacts]
        if len(set(ids)) != len(ids) or len(set(hashes)) != len(hashes):
            raise ValueError("source_artifacts must have unique ids and content hashes")
        if self.source_artifacts:
            if self.raw_fingerprint is None:
                raise ValueError("raw_fingerprint is required when source_artifacts are declared")
            if self.raw_fingerprint != raw_artifact_set_fingerprint(hashes):
                raise ValueError("raw_fingerprint does not match the source artifact set")
        elif self.raw_fingerprint is not None:
            raise ValueError("raw_fingerprint requires source_artifacts")

        if self.lineage:
            if not self.source_artifacts:
                raise ValueError("lineage requires source_artifacts")
            auxiliary = (
                (self.market_calendar.content_fingerprint,) if self.market_calendar else ()
            )
            verify_lineage(
                self.lineage,
                source_hashes=tuple(hashes),
                terminal_fingerprint=self.fingerprint,
                auxiliary_hashes=auxiliary,
            )

        if (
            self.returned_range is not None
            and self.canonical_range is not None
            and not self.returned_range.contains(self.canonical_range)
        ):
            raise ValueError("canonical_range must lie within returned_range")

        if self.instrument is not None and self.instruments:
            if self.instrument.ticker not in self.instruments:
                raise ValueError("instrument.ticker must appear in instruments")
        return self

    @property
    def lineage_fingerprint(self) -> str | None:
        return lineage_fingerprint(self.lineage) if self.lineage else None

    def verify_table(self, rows: Iterable[Mapping[str, Any]]) -> None:
        """Recalcule l'empreinte QCT-1 de la table et la compare à `fingerprint`."""
        if self.table_schema is None:
            raise ValueError("verify_table requires table_schema (C02 v1.1)")
        actual = sha256_fingerprint(self.table_schema.canonical_bytes(rows))
        if actual != self.fingerprint:
            raise ValueError(f"table fingerprint mismatch: {actual} != {self.fingerprint}")

    def verify_artifacts(self, artifacts: Iterable[ProviderArtifact]) -> None:
        """
        Les artefacts fournis sont exactement ceux référencés (id, empreinte, licence).

        Précondition : identifiants deux à deux distincts dans la collection fournie. Le
        résultat (succès ou message d'erreur) est invariant par permutation de la collection.
        """
        artifacts = list(artifacts)
        ids = [a.artifact_id for a in artifacts]
        duplicates = sorted({i for i in ids if ids.count(i) > 1})
        if duplicates:
            raise ValueError(f"provided artifacts contain duplicate artifact_id: {duplicates}")
        provided = dict(zip(ids, artifacts, strict=True))
        declared = {r.artifact_id: r for r in self.source_artifacts}
        if set(provided) != set(declared):
            raise ValueError(
                f"artifact set mismatch: provided {sorted(provided)} vs declared {sorted(declared)}"
            )
        mismatched = sorted(i for i, ref in declared.items() if provided[i].ref() != ref)
        if mismatched:
            names = ", ".join(repr(i) for i in mismatched)
            raise ValueError(f"artifact {names} does not match its reference")

    def verify_calendar(self, calendar: MarketCalendarSnapshot) -> None:
        """Référence valide + bornes et comptages cohérents avec le calendrier."""
        if self.market_calendar is None:
            raise ValueError("snapshot declares no market_calendar")
        if calendar.ref() != self.market_calendar:
            raise ValueError("calendar does not match the snapshot market_calendar reference")
        if self.temporal_convention is not None:
            if self.temporal_convention.canonical_timezone != calendar.timezone:
                raise ValueError("canonical_timezone differs from the calendar timezone")
        rng = self.canonical_range
        if rng is not None:
            for bound in (rng.first_session, rng.last_session):
                if not calendar.contains(bound):
                    raise ValueError(f"canonical bound {bound} is not a calendar session")
            if self.counts is not None and self.counts.expected_sessions.is_known:
                expected = calendar.sessions_between(rng.first_session, rng.last_session)
                if self.counts.expected_sessions.value != expected:
                    raise ValueError(
                        f"expected_sessions {self.counts.expected_sessions.value} "
                        f"!= calendar sessions in canonical_range ({expected})"
                    )
