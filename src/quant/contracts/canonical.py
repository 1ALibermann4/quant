"""
C02 v1.1 — représentations canoniques normatives et empreintes.

Trois représentations, définies par le contrat `specs/contracts/C02/C02_v1.1.yaml` :

- QCJ-1 : JSON canonique des objets d'identité (paramètres, lignée, agrégats) ;
- QCT-1 : table scientifique canonique (texte délimité, décimaux à échelle fixe) ;
- QCC-1 : liste ordonnée des séances d'un calendrier.

Empreinte : ``sha256:`` suivi des 64 caractères hexadécimaux minuscules du SHA-256
calculé sur les octets canoniques.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections.abc import Iterable, Mapping, Sequence
from datetime import date, datetime, time, timezone
from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation
from enum import Enum
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

QCJ_1 = "QCJ-1"
QCT_1 = "QCT-1"
QCC_1 = "QCC-1"

SHA256_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
MAX_SAFE_INTEGER = 2**53 - 1
_FORBIDDEN_TEXT_CHARS = re.compile(r'[,"\r\n]')


def sha256_fingerprint(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def is_sha256_fingerprint(value: str) -> bool:
    return bool(SHA256_PATTERN.match(value))


def require_sha256_fingerprint(value: str, field: str) -> str:
    if not is_sha256_fingerprint(value):
        raise ValueError(f"{field} must match 'sha256:<64 lowercase hex>'; got {value!r}")
    return value


def require_iana_timezone(value: str) -> str:
    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError(f"unknown IANA timezone {value!r}") from exc
    return value


def format_utc_datetime(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("naive datetime is not canonicalizable (timezone required)")
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


# --------------------------------------------------------------------------- QCJ-1


def _qcj_normalize(value: Any, path: str) -> Any:
    if value is None or isinstance(value, bool) or isinstance(value, str):
        return value
    if isinstance(value, Enum):
        return _qcj_normalize(value.value, path)
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise ValueError(f"QCJ-1: integer out of safe range at {path}")
        return value
    if isinstance(value, float | Decimal):
        raise ValueError(
            f"QCJ-1: non-integer numbers are forbidden at {path}; "
            "encode them as decimal strings"
        )
    if isinstance(value, datetime):
        return format_utc_datetime(value)
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, time):
        if value.tzinfo is not None:
            raise ValueError(f"QCJ-1: time with tzinfo is forbidden at {path}")
        return value.strftime("%H:%M:%S")
    if isinstance(value, Mapping):
        out: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError(f"QCJ-1: object keys must be strings at {path}")
            out[key] = _qcj_normalize(item, f"{path}.{key}")
        return out
    if isinstance(value, list | tuple):
        return [_qcj_normalize(item, f"{path}[{i}]") for i, item in enumerate(value)]
    raise ValueError(f"QCJ-1: unsupported type {type(value).__name__} at {path}")


def canonical_json_bytes(value: Any) -> bytes:
    """QCJ-1 : clés triées par point de code, séparateurs minimaux, UTF-8, sans flottant."""
    normalized = _qcj_normalize(value, "$")
    text = json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return text.encode("utf-8")


def canonical_json_fingerprint(value: Any) -> str:
    return sha256_fingerprint(canonical_json_bytes(value))


def raw_artifact_set_fingerprint(content_hashes: Iterable[str]) -> str:
    """
    Agrégat déterministe des artefacts bruts d'un snapshot (sémantique d'ensemble).

    QCJ-1 de ``{"kind": "C02.raw_artifact_set", "members": [...]}`` avec membres triés
    lexicographiquement ; doublons interdits ; ensemble vide interdit.
    """
    members = list(content_hashes)
    if not members:
        raise ValueError("raw artifact set must not be empty")
    for member in members:
        require_sha256_fingerprint(member, "raw artifact member")
    if len(set(members)) != len(members):
        raise ValueError("raw artifact set contains duplicate content hashes")
    return canonical_json_fingerprint(
        {"kind": "C02.raw_artifact_set", "members": sorted(members)}
    )


# --------------------------------------------------------------------------- QCT-1


def format_decimal(value: Any, scale: int) -> str:
    """Décimal à échelle fixe, arrondi au pair le plus proche sur la valeur exacte."""
    if isinstance(value, bool):
        raise ValueError("QCT-1: boolean is not a decimal")
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("QCT-1: non-finite decimal value")
        exact = Decimal(value)
    elif isinstance(value, int | Decimal):
        exact = Decimal(value)
    elif isinstance(value, str):
        try:
            exact = Decimal(value)
        except InvalidOperation as exc:
            raise ValueError(f"QCT-1: invalid decimal literal {value!r}") from exc
    else:
        raise ValueError(f"QCT-1: unsupported decimal type {type(value).__name__}")
    if not exact.is_finite():
        raise ValueError("QCT-1: non-finite decimal value")
    quantized = exact.quantize(Decimal(1).scaleb(-scale), rounding=ROUND_HALF_EVEN)
    if quantized.is_zero():
        quantized = abs(quantized)
    return f"{quantized:f}"


def _format_cell(column: Mapping[str, Any], value: Any) -> str:
    name = column["name"]
    if value is None:
        if not column.get("nullable", False):
            raise ValueError(f"QCT-1: null value in non-nullable column {name!r}")
        return ""
    ctype = column["type"]
    if ctype == "date":
        if isinstance(value, datetime) or not isinstance(value, date):
            raise ValueError(f"QCT-1: column {name!r} expects a date")
        return value.isoformat()
    if ctype == "datetime":
        if not isinstance(value, datetime):
            raise ValueError(f"QCT-1: column {name!r} expects a datetime")
        return format_utc_datetime(value)
    if ctype == "decimal":
        return format_decimal(value, column["scale"])
    if ctype == "integer":
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"QCT-1: column {name!r} expects an integer")
        return str(value)
    if ctype == "string":
        if not isinstance(value, str):
            raise ValueError(f"QCT-1: column {name!r} expects a string")
        if _FORBIDDEN_TEXT_CHARS.search(value):
            raise ValueError(f"QCT-1: forbidden character in column {name!r}")
        return value
    raise ValueError(f"QCT-1: unsupported column type {ctype!r}")


def canonical_table_bytes(
    columns: Sequence[Mapping[str, Any]],
    primary_key: Sequence[str],
    rows: Iterable[Mapping[str, Any]],
) -> bytes:
    """
    QCT-1 : en-tête puis une ligne par enregistrement, colonnes dans l'ordre du schéma,
    lignes triées par clé primaire (valeurs typées), séparateur ``,``, fin de ligne ``\\n``
    après chaque ligne (y compris la dernière), UTF-8 sans BOM.
    """
    names = [c["name"] for c in columns]
    by_name = {c["name"]: c for c in columns}
    for key in primary_key:
        if key not in by_name:
            raise ValueError(f"QCT-1: primary key column {key!r} not in schema")
        if by_name[key]["type"] not in {"date", "datetime", "integer", "string"}:
            raise ValueError(f"QCT-1: primary key column {key!r} has non-orderable type")
        if by_name[key].get("nullable", False):
            raise ValueError(f"QCT-1: primary key column {key!r} must not be nullable")

    materialized = []
    for row in rows:
        extra = set(row) - set(names)
        if extra:
            raise ValueError(f"QCT-1: row has columns outside schema: {sorted(extra)}")
        materialized.append(row)

    def sort_key(row: Mapping[str, Any]) -> tuple[Any, ...]:
        return tuple(row[k] for k in primary_key)

    materialized.sort(key=sort_key)
    for previous, current in zip(materialized, materialized[1:], strict=False):
        if sort_key(previous) == sort_key(current):
            raise ValueError(f"QCT-1: duplicate primary key {sort_key(current)!r}")

    lines = [",".join(names)]
    for row in materialized:
        lines.append(",".join(_format_cell(by_name[n], row.get(n)) for n in names))
    return ("\n".join(lines) + "\n").encode("utf-8")


# --------------------------------------------------------------------------- QCC-1


def canonical_calendar_bytes(sessions: Sequence[date]) -> bytes:
    """QCC-1 : une date ISO ``YYYY-MM-DD`` par ligne, strictement croissante, ``\\n`` final."""
    if not sessions:
        raise ValueError("QCC-1: session list must not be empty")
    for previous, current in zip(sessions, sessions[1:], strict=False):
        if not previous < current:
            raise ValueError("QCC-1: sessions must be strictly increasing")
    for session in sessions:
        if isinstance(session, datetime) or not isinstance(session, date):
            raise ValueError("QCC-1: sessions must be dates")
    return "".join(f"{s.isoformat()}\n" for s in sessions).encode("utf-8")
