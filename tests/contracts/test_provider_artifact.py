"""Tests C02 v1.1 — ProviderArtifact, LicenseRef, InstrumentIdentifiers."""

from datetime import date, datetime

import pytest
from c02_synthetic import ACQUIRED_AT, artifact, license_ref
from pydantic import ValidationError

from quant.contracts.canonical import sha256_fingerprint
from quant.contracts.knowledge import Knowable, KnowledgeStatus


def test_artifact_valid_and_frozen():
    a = artifact()
    assert a.contract_id == "C02"
    assert a.contract_version == "1.1"
    with pytest.raises(ValidationError):
        a.byte_size = 0


def test_interface_version_may_be_unknown_without_inventing_value():
    a = artifact(provider_interface_version=Knowable.unknown(note="no versioning published"))
    assert a.provider_interface_version.status is KnowledgeStatus.UNKNOWN
    assert a.provider_interface_version.value is None


def test_content_hash_format_enforced():
    with pytest.raises(ValidationError, match="content_sha256"):
        artifact(content_sha256="sha256:abc")
    with pytest.raises(ValidationError, match="content_sha256"):
        artifact(content_sha256="sha256:" + "A" * 64)


def test_acquired_at_must_be_timezone_aware():
    with pytest.raises(ValidationError, match="timezone-aware"):
        artifact(acquired_at=datetime(2020, 7, 15, 12, 0))


@pytest.mark.parametrize("key", ["token", "api_key", "apiKey", "X-Secret", "password"])
def test_credentials_never_recorded(key):
    with pytest.raises(ValidationError, match="credentials"):
        artifact(request_parameters={key: "value"})
    with pytest.raises(ValidationError, match="credentials"):
        artifact(provenance_metadata={key: "value"})


def test_request_parameters_must_be_canonicalizable():
    with pytest.raises(ValidationError):
        artifact(request_parameters={"threshold": 1.5})


def test_requested_range_order():
    with pytest.raises(ValidationError, match="requested_first_session"):
        artifact(
            requested_first_session=Knowable.known(date(2021, 1, 1)),
            requested_last_session=Knowable.known(date(2020, 1, 1)),
        )


def test_identity_is_content_hash_not_acquisition_time():
    content = b"same bytes"
    a1 = artifact(content=content, acquired_at=ACQUIRED_AT)
    a2 = artifact(content=content, acquired_at=datetime(2021, 1, 1, tzinfo=ACQUIRED_AT.tzinfo))
    assert a1.content_sha256 == a2.content_sha256 == sha256_fingerprint(content)


def test_ref_carries_license():
    a = artifact()
    ref = a.ref()
    assert ref.artifact_id == a.artifact_id
    assert ref.content_sha256 == a.content_sha256
    assert ref.license == a.license


def test_license_can_record_unknown_retention():
    lic = license_ref(raw_retention_permitted=Knowable.unknown())
    assert not lic.raw_retention_permitted.is_known
