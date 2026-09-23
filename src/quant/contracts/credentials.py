"""
C02 — règle CRED-1 : indicateurs structurels de secret dans les métadonnées libres (C02-INV-18).

Objectif : empêcher la persistance *accidentelle* d'éléments d'authentification dans les
métadonnées d'acquisition et de transformation. Ce n'est pas un détecteur universel de
secrets : une valeur secrète dépourvue de marqueur structurel (jeton brut sous une clé
anodine, secret encodé ou fragmenté) n'est pas détectable. L'obligation première reste de ne
jamais transmettre de secret à ces champs.

Indicateurs détectés :

- K1 — nom de clé d'identification (`token`, `api_key`, `secret`, `password`, …) ;
- V1 — en-tête HTTP d'autorisation dans une valeur (`Authorization: …`) ;
- V2 — valeur entière de la forme `<schéma> <identifiant>` (`Bearer …`, `Basic …`, …) ;
- V3 — paramètre d'URL ou de requête d'identification (`?token=…`, `&api_key=…`) ;
- V4 — identifiants dans l'URL (`scheme://user:password@host`).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

CRED_1 = "CRED-1"

_CREDENTIAL_NAME = re.compile(
    r"(token|api[_-]?key|secret|passw(?:or)?d|authorization|bearer|credential"
    r"|private[_-]?key|access[_-]?key)",
    re.IGNORECASE,
)
_CREDENTIAL_PARAM_EXACT = frozenset({"key", "auth", "sig", "signature"})
_AUTH_HEADER = re.compile(r"(?:^|[\s;,{\"'])(?:proxy-)?authorization\s*[:=]", re.IGNORECASE)
_AUTH_SCHEME_VALUE = re.compile(r"^\s*(?:bearer|basic|digest|token)\s+\S+\s*$", re.IGNORECASE)
_QUERY_PARAM = re.compile(r"[?&;#]([^=&;#?\s]+)=")
_URL_USERINFO = re.compile(r"[a-z][a-z0-9+.\-]*://[^/\s@:]+:[^/\s@]*@", re.IGNORECASE)


def is_credential_name(name: str) -> bool:
    """K1 — nom de clé désignant un élément d'authentification."""
    return bool(_CREDENTIAL_NAME.search(name))


def _is_credential_param(name: str) -> bool:
    # `key`, `sig`… ne sont des indicateurs que dans une URL : ce sont des clés de
    # paramètres légitimes ailleurs (ex. clé de tri).
    return is_credential_name(name) or name.lower() in _CREDENTIAL_PARAM_EXACT


def credential_indicator(text: str) -> str | None:
    """Premier indicateur V1–V4 trouvé dans une valeur textuelle, sinon None."""
    if _AUTH_HEADER.search(text):
        return "V1 authorization header"
    if _AUTH_SCHEME_VALUE.match(text):
        return "V2 authentication scheme value"
    for match in _QUERY_PARAM.finditer(text):
        if _is_credential_param(match.group(1)):
            return f"V3 credential query parameter {match.group(1)!r}"
    if _URL_USERINFO.search(text):
        return "V4 credentials in URL"
    return None


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
    """Applique CRED-1 (K1 sur les clés, V1–V4 sur les valeurs) récursivement."""
    for key, value in mapping.items():
        if is_credential_name(key):
            raise ValueError(f"{field}: credentials must never be recorded (K1 key {key!r})")
        _scan_value(value, field, f"{path}.{key}")


def require_no_credential_text(text: str, field: str) -> str:
    """Applique CRED-1 (V1–V4) à une valeur textuelle isolée."""
    _scan_value(text, field, "$")
    return text
