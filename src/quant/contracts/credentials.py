"""
C02 — règle CRED-1 : indicateurs structurels de secret dans les métadonnées libres (C02-INV-18).

Objectif : empêcher la persistance *accidentelle* d'éléments d'authentification dans les
métadonnées d'acquisition et de transformation. Ce n'est pas un détecteur universel de
secrets : une valeur secrète dépourvue de marqueur structurel (jeton brut sous une clé
anodine, secret encodé ou fragmenté) n'est pas détectable. L'obligation première reste de ne
jamais transmettre de secret à ces champs.

Grammaire (indépendante de la position du marqueur dans la valeur, insensible à la casse
des mots-clés) :

- K1 — nom de clé contenant un mot d'identification (`token`, `api_key`, `secret`, …) ;
- V1 — sous-chaîne `authorization` suivie de `:` ou `=` (espaces admis), n'importe où ;
- V2 — mot de schéma (`bearer`, `basic`, `digest`, `token`) non précédé d'une lettre ou d'un
  chiffre, suivi d'espaces et d'un jeton de forme identifiant (`_is_credential_token`) ;
- V3 — paramètre `nom=` où `nom` est une suite maximale de caractères `[\\w.-]` satisfaisant
  K1 ; précédé de `?`, `&`, `;` ou `#` (contexte d'URL/requête), également `key`, `auth`,
  `sig`, `signature` et tout nom dont le dernier segment (`-`, `_`, `.`) est `sig`/`signature` ;
- V4 — userinfo avec mot de passe dans une URL : `scheme://[utilisateur]:[mot de passe]@`.
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
_URL_PARAM_EXACT = frozenset({"key", "auth", "sig", "signature"})
_URL_PARAM_SEGMENT_SUFFIX = frozenset({"sig", "signature"})

_AUTH_HEADER = re.compile(r"authorization\s*[:=]", re.IGNORECASE)
_AUTH_SCHEME = re.compile(
    r"(?<![^\W_])(?:bearer|basic|digest|token)\s+([A-Za-z0-9\-._~+/]+=*)",
    re.IGNORECASE,
)
_PARAM = re.compile(r"(?<![\w.\-])([\w.\-]+)\s*=")
_URL_CONTEXT = frozenset("?&;#")
_URL_USERINFO = re.compile(r"[a-z][a-z0-9+.\-]*://[^/\s@:?#]*:[^/\s@?#]*@", re.IGNORECASE)

_MIN_TOKEN_LENGTH = 8
_NATURAL_WORD = re.compile(r"^[A-Za-z][a-z]*$")


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

    Exclus (frontière lexicale) : jeton de moins de 8 caractères après retrait de la
    ponctuation finale, ou mot du langage naturel (lettres seules, majuscule initiale au
    plus). `Basic Materials`, `Token Ring`, `bearer bond` ne sont donc pas des indicateurs.
    """
    token = token.rstrip(".-_~+/")
    return len(token) >= _MIN_TOKEN_LENGTH and not _NATURAL_WORD.match(token)


def credential_indicator(text: str) -> str | None:
    """Premier indicateur V1–V4 trouvé dans une valeur textuelle, sinon None."""
    if _AUTH_HEADER.search(text):
        return "V1 authorization header"
    for match in _AUTH_SCHEME.finditer(text):
        if _is_credential_token(match.group(1)):
            return "V2 authentication scheme value"
    for match in _PARAM.finditer(text):
        name = match.group(1)
        in_url = match.start() > 0 and text[match.start() - 1] in _URL_CONTEXT
        if is_credential_name(name) or (in_url and _is_url_credential_param(name)):
            return f"V3 credential query parameter {name!r}"
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
