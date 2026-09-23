"""C02 v1.1 — ProviderArtifact et TransformationRecord (provenance brute → scientifique)."""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from quant.contracts.canonical import (
    canonical_json_bytes,
    canonical_json_fingerprint,
    require_sha256_fingerprint,
)
from quant.contracts.knowledge import Knowable

CONTRACT_ID = "C02"
CONTRACT_VERSION = "1.1"

JsonScalar = str | int | bool | None

_CREDENTIAL_KEY = re.compile(
    r"(token|api[_-]?key|secret|password|authorization|bearer)", re.IGNORECASE
)


def _require_utc_aware(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware (UTC)")
    return value


def _require_qcj(parameters: dict[str, Any], field: str) -> dict[str, Any]:
    canonical_json_bytes(parameters)
    for key in parameters:
        if _CREDENTIAL_KEY.search(key):
            raise ValueError(f"{field}: credentials must never be recorded (key {key!r})")
    return parameters


class InstrumentIdentifiers(BaseModel):
    """Identifiants d'instrument (DATA-REQ INS-05) — aucun identifiant n'est inventé."""

    model_config = ConfigDict(frozen=True)

    ticker: str
    venue: Knowable[str]
    isin: Knowable[str]
    cusip: Knowable[str]
    figi: Knowable[str]
    vendor_permanent_id: Knowable[str]


class LicenseRef(BaseModel):
    """
    Transport de la licence d'un artefact.

    `usage_basis_ref` référence la décision qui fonde l'usage (ex. l'ASSUMPTION A-1 de
    DR-003) ; C02 ne constitue pas une seconde source normative de cette hypothèse.
    """

    model_config = ConfigDict(frozen=True)

    license_id: str
    terms_ref: str
    terms_version: Knowable[str]
    plan_tier: Knowable[str]
    usage_basis_ref: Knowable[str]
    raw_retention_permitted: Knowable[bool]
    retention_condition: Knowable[str]


class ProviderArtifact(BaseModel):
    """
    Artefact brut effectivement reçu d'une source externe, avant toute interprétation.

    Identité de contenu : `content_sha256` (octets exacts reçus). `acquired_at` est une
    métadonnée d'exécution et ne participe à aucune empreinte.
    """

    model_config = ConfigDict(frozen=True)

    contract_id: str = Field(default=CONTRACT_ID, frozen=True)
    contract_version: str = CONTRACT_VERSION
    artifact_id: str
    provider_id: str
    provider_product: str
    provider_interface: str
    provider_interface_version: Knowable[str]
    instrument: InstrumentIdentifiers
    request_parameters: dict[str, JsonScalar] = Field(default_factory=dict)
    requested_first_session: Knowable[date]
    requested_last_session: Knowable[date]
    acquired_at: datetime
    content_sha256: str
    media_type: str
    encoding: Knowable[str]
    byte_size: int = Field(ge=0)
    license: LicenseRef
    provenance_metadata: dict[str, str] = Field(default_factory=dict)

    @field_validator("content_sha256")
    @classmethod
    def _content_hash_format(cls, v: str) -> str:
        return require_sha256_fingerprint(v, "content_sha256")

    @field_validator("acquired_at")
    @classmethod
    def _acquired_at_aware(cls, v: datetime) -> datetime:
        return _require_utc_aware(v, "acquired_at")

    @field_validator("request_parameters")
    @classmethod
    def _parameters_canonical(cls, v: dict[str, Any]) -> dict[str, Any]:
        return _require_qcj(v, "request_parameters")

    @field_validator("provenance_metadata")
    @classmethod
    def _metadata_without_credentials(cls, v: dict[str, str]) -> dict[str, str]:
        return _require_qcj(v, "provenance_metadata")

    @model_validator(mode="after")
    def _requested_range_order(self) -> ProviderArtifact:
        first, last = self.requested_first_session, self.requested_last_session
        if first.is_known and last.is_known and first.value > last.value:
            raise ValueError("requested_first_session must be <= requested_last_session")
        return self

    def ref(self) -> ProviderArtifactRef:
        return ProviderArtifactRef(
            artifact_id=self.artifact_id,
            content_sha256=self.content_sha256,
            license=self.license,
        )


class ProviderArtifactRef(BaseModel):
    """Référence immuable d'un DatasetSnapshot vers un ProviderArtifact."""

    model_config = ConfigDict(frozen=True)

    artifact_id: str
    content_sha256: str
    license: LicenseRef

    @field_validator("content_sha256")
    @classmethod
    def _content_hash_format(cls, v: str) -> str:
        return require_sha256_fingerprint(v, "content_sha256")


class TransformationRecord(BaseModel):
    """
    Une étape déterministe entre artefact(s) brut(s) et table scientifique.

    Identité d'application (`application_key`) : type, identifiant, version d'implémentation,
    paramètres canoniques et empreintes d'entrée — jamais `executed_at`.
    """

    model_config = ConfigDict(frozen=True)

    step_index: int = Field(ge=0)
    transformation_id: str
    transformation_type: str
    implementation_version: str
    parameters: dict[str, JsonScalar | list[JsonScalar]] = Field(default_factory=dict)
    input_fingerprints: tuple[str, ...]
    output_fingerprint: str
    executed_at: datetime
    observations_in: Knowable[int]
    observations_out: Knowable[int]
    observations_dropped: Knowable[int]
    justification: str | None = None

    @field_validator("input_fingerprints")
    @classmethod
    def _inputs_format(cls, v: tuple[str, ...]) -> tuple[str, ...]:
        if not v:
            raise ValueError("input_fingerprints must not be empty")
        for item in v:
            require_sha256_fingerprint(item, "input_fingerprints")
        return v

    @field_validator("output_fingerprint")
    @classmethod
    def _output_format(cls, v: str) -> str:
        return require_sha256_fingerprint(v, "output_fingerprint")

    @field_validator("executed_at")
    @classmethod
    def _executed_at_aware(cls, v: datetime) -> datetime:
        return _require_utc_aware(v, "executed_at")

    @field_validator("parameters")
    @classmethod
    def _parameters_canonical(cls, v: dict[str, Any]) -> dict[str, Any]:
        return _require_qcj(v, "parameters")

    @model_validator(mode="after")
    def _observation_arithmetic(self) -> TransformationRecord:
        counts = (self.observations_in, self.observations_out, self.observations_dropped)
        for count in counts:
            if count.is_known and count.value < 0:
                raise ValueError("observation counts must be >= 0")
        if all(c.is_known for c in counts):
            n_in, n_out, n_drop = (c.value for c in counts)
            if n_in - n_drop != n_out:
                raise ValueError(
                    "observations_out must equal observations_in - observations_dropped"
                )
        if self.output_fingerprint in self.input_fingerprints:
            raise ValueError("output_fingerprint must differ from its inputs")
        return self

    def application_identity(self) -> dict[str, Any]:
        return {
            "transformation_id": self.transformation_id,
            "transformation_type": self.transformation_type,
            "implementation_version": self.implementation_version,
            "parameters": self.parameters,
            "input_fingerprints": list(self.input_fingerprints),
        }

    @property
    def application_key(self) -> str:
        return canonical_json_fingerprint(self.application_identity())

    def record_identity(self) -> dict[str, Any]:
        return {
            "step_index": self.step_index,
            **self.application_identity(),
            "output_fingerprint": self.output_fingerprint,
        }


def lineage_fingerprint(records: tuple[TransformationRecord, ...]) -> str:
    """Empreinte QCJ-1 de la chaîne ordonnée (hors métadonnées d'exécution)."""
    return canonical_json_fingerprint(
        {"kind": "C02.lineage", "steps": [r.record_identity() for r in records]}
    )


def verify_lineage(
    records: tuple[TransformationRecord, ...],
    *,
    source_hashes: tuple[str, ...],
    terminal_fingerprint: str,
    auxiliary_hashes: tuple[str, ...] = (),
) -> None:
    """
    Vérifie la chaîne ProviderArtifact → T1 → … → Tn → table canonique.

    - `step_index` = 0…n-1 dans l'ordre de la liste ;
    - chaque entrée est un artefact source, une sortie d'étape antérieure ou une
      dépendance auxiliaire déclarée (ex. empreinte du calendrier) ;
    - chaque artefact source est consommé ;
    - les sorties sont uniques ;
    - la sortie de la dernière étape est l'empreinte de la table canonique.
    """
    if not records:
        raise ValueError("lineage must contain at least one transformation")
    available = set(source_hashes) | set(auxiliary_hashes)
    consumed: set[str] = set()
    outputs: set[str] = set()
    for expected_index, record in enumerate(records):
        if record.step_index != expected_index:
            raise ValueError(
                f"lineage step_index {record.step_index} at position {expected_index}"
            )
        for item in record.input_fingerprints:
            if item not in available:
                raise ValueError(
                    f"step {record.step_index}: input {item} is neither a source artifact, "
                    "an earlier output nor a declared auxiliary dependency"
                )
            consumed.add(item)
        if record.output_fingerprint in outputs or record.output_fingerprint in available:
            raise ValueError(f"step {record.step_index}: output fingerprint is not unique")
        outputs.add(record.output_fingerprint)
        available.add(record.output_fingerprint)
    unconsumed = set(source_hashes) - consumed
    if unconsumed:
        raise ValueError(f"source artifacts never consumed by lineage: {sorted(unconsumed)}")
    if records[-1].output_fingerprint != terminal_fingerprint:
        raise ValueError("last transformation output does not match the dataset fingerprint")


def assert_deterministic(records: tuple[TransformationRecord, ...]) -> None:
    """Deux applications de même identité doivent produire la même sortie."""
    seen: dict[str, str] = {}
    for record in records:
        key = record.application_key
        if key in seen and seen[key] != record.output_fingerprint:
            raise ValueError(
                f"non-deterministic transformation {record.transformation_id!r}: "
                "same application identity, different outputs"
            )
        seen[key] = record.output_fingerprint
