"""
C02 — règle CRED-1 : indicateurs structurels de secret dans les métadonnées libres (C02-INV-18).

Scanner déterministe à règles séparées (K1, V1, V2, V3, V4), chacune avec un domaine
d'application explicite. Ce n'est pas un détecteur universel de secrets.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

CRED_1 = "CRED-1"

# K1 — sous-chaîne, insensible à la casse. Variantes de séparateur [_-]? incluses
# (api_key / apikey / api-key, private_key / privatekey / private-key, idem access).
_CREDENTIAL_NAME = re.compile(
    r"(token|api[_-]?key|secret|passw(?:or)?d|authorization|bearer|credential"
    r"|private[_-]?key|access[_-]?key)",
    re.IGNORECASE,
)
_URL_PARAM_EXACT = frozenset({"key", "auth", "sig", "signature"})
_URL_PARAM_SEGMENT_SUFFIX = frozenset({"sig", "signature"})

_AUTH_HEADER = re.compile(r"authorization\s*[:=]", re.IGNORECASE)
_SCHEME_WORD = re.compile(r"(?<![^\W_])(bearer|basic|digest|token)(?![^\W_])", re.IGNORECASE)
_TOKEN_AFTER_SCHEME = re.compile(r"\s+([A-Za-z0-9\-._~+/]+=*)")
_PARAM = re.compile(r"(?<![\w.\-])([\w.\-]+)\s*=")
_URL_CONTEXT = frozenset("?&;#")
_SCHEME_URL = re.compile(r"[a-z][a-z0-9+.\-]*://", re.IGNORECASE)
_AUTHORITY_END = frozenset("/?# \t\r\n")

_MIN_TOKEN_LENGTH = 8
_NATURAL_WORD = re.compile(r"^[A-Za-z][a-z]*$")
_TOKEN_TRAILING_PUNCT = ".-_~+/="


def is_credential_name(name: str) -> bool:
    """K1 — nom de clé désignant un élément d'authentification."""
    return bool(_CREDENTIAL_NAME.search(name))


def _is_url_credential_param(name: str) -> bool:
    lowered = name.lower()
    if lowered in _URL_PARAM_EXACT:
        return True
    return re.split(r"[-_.]", lowered)[-1] in _URL_PARAM_SEGMENT_SUFFIX


def _is_credential_token(token: str) -> bool:
    """
    Jeton de forme identifiant après un schéma V2.

    La ponctuation finale (y compris le padding ``=``) est retirée avant le test
    de longueur et le filtre « mot naturel ».
    """
    token = token.rstrip(_TOKEN_TRAILING_PUNCT)
    return len(token) >= _MIN_TOKEN_LENGTH and not _NATURAL_WORD.match(token)


def _v1_indicator(text: str) -> str | None:
    if _AUTH_HEADER.search(text):
        return "V1 authorization header"
    return None


def _v2_indicator(text: str) -> str | None:
    """Chaque mot de schéma est examiné indépendamment (correspondances chevauchantes)."""
    for match in _SCHEME_WORD.finditer(text):
        after = _TOKEN_AFTER_SCHEME.match(text, match.end())
        if after and _is_credential_token(after.group(1)):
            return "V2 authentication scheme value"
    return None


def _v3_indicator(text: str) -> str | None:
    for match in _PARAM.finditer(text):
        name = match.group(1)
        in_url = match.start() > 0 and text[match.start() - 1] in _URL_CONTEXT
        if is_credential_name(name) or (in_url and _is_url_credential_param(name)):
            return f"V3 credential query parameter {name!r}"
    return None


def _v4_indicator(text: str) -> str | None:
    """
    Userinfo URI : le dernier ``@`` avant ``/ ? #`` ou espace termine le userinfo.

    Un ``@`` dans le nom d'utilisateur n'empêche pas de détecter ``user:password``.
    """
    for match in _SCHEME_URL.finditer(text):
        rest = text[match.end() :]
        end = next((i for i, ch in enumerate(rest) if ch in _AUTHORITY_END), len(rest))
        authority = rest[:end]
        last_at = authority.rfind("@")
        if last_at == -1:
            continue
        if ":" in authority[:last_at]:
            return "V4 credentials in URL"
    return None


def credential_indicator(text: str) -> str | None:
    """Premier indicateur V1–V4 trouvé, sinon None. Ordre de priorité : V1, V2, V3, V4."""
    return _v1_indicator(text) or _v2_indicator(text) or _v3_indicator(text) or _v4_indicator(text)


def _scan_value(value: Any, field: str, path: str) -> None:
    if isinstance(value, str):
        indicator = credential_indicator(value)
        if indicator:
            raise ValueError(f"{field}: credentials must never be recorded ({indicator} at {path})")
    elif isinstance(value, Mapping):
        require_no_credentials(value, field, path)
    elif isinstance(value, list | tuple):
        for i, item in enumerate(value):
            _scan_value(item, field, f"{path}[{i}]")


def require_no_credentials(mapping: Mapping[str, Any], field: str, path: str = "$") -> None:
    """
    CRED-1 : K1 sur les clés ; V1–V4 sur les clés et les valeurs, récursivement.

    Les clés portent les mêmes indicateurs lexicaux que les valeurs (une clé
    ``https://u:p@host`` est un indicateur V4). K1 reste prioritaire sur une clé.
    """
    for key, value in mapping.items():
        if is_credential_name(key):
            raise ValueError(f"{field}: credentials must never be recorded (K1 key {key!r})")
        indicator = credential_indicator(key)
        if indicator:
            raise ValueError(
                f"{field}: credentials must never be recorded ({indicator} at {path} key {key!r})"
            )
        _scan_value(value, field, f"{path}.{key}")


def require_no_credential_text(text: str, field: str) -> str:
    """Applique CRED-1 (V1–V4) à une valeur textuelle isolée."""
    _scan_value(text, field, "$")
    return text
