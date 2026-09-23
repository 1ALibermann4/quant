"""
CRED-1 (C02-INV-18) — propriétés de la grammaire de détection (CA-02, HAT2-A1 / HAT2-A4).

Chaque marqueur doit être détecté quelle que soit sa position dans la valeur (début, milieu,
fin, après ponctuation ou délimiteur), quelle que soit la casse du mot-clé, et dans chacun des
champs du périmètre. Les faux positifs déclarés hors frontière lexicale restent acceptés.
"""

import itertools

import pytest
from c02_synthetic import artifact
from pydantic import ValidationError
from test_lineage import OUT, RAW, record

from quant.contracts.credentials import credential_indicator


def _case_variants(word: str) -> list[str]:
    mixed = "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(word))
    return sorted({word.lower(), word.upper(), word.title(), mixed})


V1_MARKERS = [
    f"{w}{sep}{rest}"
    for w in _case_variants("authorization") + _case_variants("proxy-authorization")
    for sep, rest in ((": ", "Bearer abc"), ("=", "x"), (" : ", "Basic Zm9v"))
]
V2_MARKERS = [
    f"{w} {token}"
    for w in ("bearer", "basic", "digest", "token")
    for w in _case_variants(w)
    for token in ("eyJhbGciOiJIUzI1NiJ9.e30.sig", "dXNlcjpwYXNz", "Zm9vOmJhcg==", "a1b2c3d4e5")
]
V3_MARKERS = [f"{name}=abc" for name in ("token", "API_KEY", "access-token", "Client_Secret", "pAsSwOrD")]
V3_URL_ONLY = ["key", "Auth", "SIG", "signature", "X-Amz-Signature", "x-goog-signature"]
V4_MARKERS = [
    "https://user:pw@host.example/path",
    "redis://:pw@host",
    "redis://:pw@cache.internal:6379/0",
    "postgres://user:@db.internal/x",
    "FTP://Anon:Guest@files.example",
]

SEPARATORS = ["", " ", "=", "(", "[", "<", "|", ":", "/", "-", "_", ".", ",", ";", "'", '"', "{", "\t"]


def _positions(marker: str, glued: bool = True) -> list[str]:
    """Début, milieu, fin, après chaque séparateur ; `glued` : collé à une lettre (camelCase)."""
    out = []
    for sep in SEPARATORS:
        out += [f"{sep}{marker}", f"lead text {sep}{marker} trailing"]
        if sep or glued:
            out.append(f"lead text{sep}{marker}")
    return out


@pytest.mark.parametrize("marker", V1_MARKERS)
def test_v1_detected_at_any_position(marker):
    for value in _positions(marker):
        assert credential_indicator(value) == "V1 authorization header", value


@pytest.mark.parametrize("marker", V2_MARKERS)
def test_v2_detected_at_any_position(marker):
    for value in _positions(marker, glued=False):
        assert credential_indicator(value) is not None, value


@pytest.mark.parametrize("marker", V3_MARKERS)
def test_v3_credential_names_detected_at_any_position(marker):
    for value in _positions(marker):
        assert credential_indicator(value) is not None, value


@pytest.mark.parametrize(("name", "delim"), list(itertools.product(V3_URL_ONLY, "?&;#")))
def test_v3_url_only_names_detected_in_url_context(name, delim):
    assert credential_indicator(f"https://api.example/v1{delim}{name}=abc") is not None
    assert credential_indicator(f"format=csv{delim}{name}=abc") is not None


@pytest.mark.parametrize("marker", V4_MARKERS)
def test_v4_userinfo_detected_at_any_position(marker):
    for sep in (" ", "(", "<", "=", '"'):
        for value in (marker, f"see{sep}{marker}", f"x {sep}{marker} y"):
            assert credential_indicator(value) == "V4 credentials in URL", value


SINK_SAMPLES = [
    "hdr=Authorization: Bearer abc",
    "x(Authorization: Bearer abc",
    "[authorization: x]",
    "<AUTHORIZATION: x>",
    "|Proxy-Authorization: x",
    "sent Bearer eyJhbGciOiJIUzI1NiJ9.e30.sig today",
    "token=abc&format=csv",
    "https://h/p;X-Amz-Signature=abc",
    "redis://:pw@cache.internal:6379/0",
]


@pytest.mark.parametrize("value", SINK_SAMPLES)
def test_every_cred1_field_rejects(value):
    with pytest.raises(ValidationError, match="credentials"):
        artifact(provenance_metadata={"h": value})
    with pytest.raises(ValidationError, match="credentials"):
        artifact(request_parameters={"note": value})
    with pytest.raises(ValidationError, match="credentials"):
        artifact(provider_interface=value)
    with pytest.raises(ValidationError, match="credentials"):
        record(0, [RAW], OUT, parameters={"note": value})
    with pytest.raises(ValidationError, match="credentials"):
        record(0, [RAW], OUT, parameters={"cols": ["ok", value]})


FALSE_POSITIVES = [
    "Basic Materials",
    "Token Ring",
    "bearer bond",
    "bearer bond etf",
    "Basic ETF",
    "a basic example.",
    "Digest of corporate actions",
    "token count 5",
    "tokens are counted per session",
    "authorization_status: ok",
    "authorization pending",
    "sort key=session_date",
    "https://api.example/v1/prices?symbol=SPY&monkey=1&keyword=x&sort=key",
    "ssh://git@github.com/org/repo",
    "http://host.example:8080/path",
    "http://host.example?x=a:b@c",
    "mailto:ops@example.org",
    "take literal YYYY-MM-DD date part; no timezone conversion",
]


@pytest.mark.parametrize("value", FALSE_POSITIVES)
def test_lexical_boundary_false_positives_accepted(value):
    assert credential_indicator(value) is None
    art = artifact(provenance_metadata={"h": value}, request_parameters={"note": value})
    assert art.provenance_metadata["h"] == value
    assert record(0, [RAW], OUT, parameters={"note": value}).parameters["note"] == value


@pytest.mark.parametrize("value", ["Bearer abc", "Bearer abcdefghij", "Basic Zm9v", "xBearer a1b2c3d4e5"])
def test_declared_v2_limit_not_detected(value):
    """Limite déclarée (CRED-1.limits) : jeton < 8 caractères, mot naturel, schéma collé à une lettre."""
    assert credential_indicator(value) is None
    assert credential_indicator(f"Authorization: {value}") == "V1 authorization header"


@pytest.mark.parametrize("value", ["preauthorization: none", "Basic 20221231", "token=3"])
def test_declared_false_positives_rejected(value):
    """Faux positifs déclarés (CRED-1.limits) : la grammaire privilégie la détection."""
    assert credential_indicator(value) is not None
