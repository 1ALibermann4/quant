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
from decimal import ROUND_HALF_EVEN, Context, Decimal, DivisionByZero, InvalidOperation, Overflow
from enum import Enum
from typing import Annotated, Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import AfterValidator, BaseModel

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


def require_utf8_text(value: str, path: str = "$") -> str:
    """Rejette les chaînes non encodables en UTF-8 (surrogates isolés, etc.)."""
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"text is not UTF-8 encodable at {path}") from exc
    return value


def scan_utf8(value: Any, path: str = "$") -> None:
    """Parcourt récursivement chaînes, mappings, séquences et modèles."""
    if isinstance(value, str):
        require_utf8_text(value, path)
        return
    if isinstance(value, BaseModel):
        for name, item in value.__dict__.items():
            if name.startswith("_"):
                continue
            scan_utf8(item, f"{path}.{name}")
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_path = f"{path}.{key}"
            if isinstance(key, str):
                require_utf8_text(key, key_path)
            scan_utf8(item, key_path)
        return
    if isinstance(value, list | tuple):
        for i, item in enumerate(value):
            scan_utf8(item, f"{path}[{i}]")


def to_canonical_utc(value: datetime, field: str = "instant") -> datetime:
    """
    Frontière temporelle unique : datetime aware → datetime UTC canonique.

    L'instant est converti via ``astimezone(UTC)`` puis reconstruit avec le
    ``tzinfo`` singleton ``timezone.utc``. Aucun objet timezone de l'appelant
    n'est conservé (fold résolu, tzinfo mutable isolé).
    """
    if not isinstance(value, datetime):
        raise ValueError(f"{field} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware (UTC)")
    try:
        utc = value.astimezone(timezone.utc)
    except OverflowError as exc:
        raise ValueError(f"{field}: instant outside the UTC range 0001-01-01..9999-12-31") from exc
    if utc.year < 1 or utc.year > 9999:
        raise ValueError(f"{field}: instant outside the UTC range 0001-01-01..9999-12-31")
    return datetime(
        utc.year, utc.month, utc.day, utc.hour, utc.minute, utc.second, utc.microsecond,
        tzinfo=timezone.utc,
    )


def to_canonical_local_time(value: time, field: str = "local time") -> time:
    """Heure murale naïve HH:MM:SS[.ffffff] ; ``fold`` n'est pas représentable."""
    if not isinstance(value, time) or isinstance(value, datetime):
        raise ValueError(f"{field} must be a time")
    if value.tzinfo is not None:
        raise ValueError(f"{field} must be a naive local time")
    if value.fold:
        raise ValueError(
            f"{field}: fold is not representable on a local time; encode an instant instead"
        )
    return time(value.hour, value.minute, value.second, value.microsecond)


CanonicalInstant = Annotated[datetime, AfterValidator(lambda v: to_canonical_utc(v, "instant"))]
CanonicalLocalTime = Annotated[time, AfterValidator(lambda v: to_canonical_local_time(v, "local time"))]


def format_utc_datetime(value: datetime) -> str:
    """
    Instant UTC ``YYYY-MM-DDTHH:MM:SS.ffffffZ`` sur tout le domaine 0001–9999.

    Formatage explicite (et non ``strftime``, dont ``%Y`` ne complète pas les années < 1000
    sur toutes les plateformes). Un instant dont la conversion UTC sort de 0001–9999 est rejeté.
    """
    u = to_canonical_utc(value, "instant")
    return (
        f"{u.year:04d}-{u.month:02d}-{u.day:02d}"
        f"T{u.hour:02d}:{u.minute:02d}:{u.second:02d}.{u.microsecond:06d}Z"
    )


def format_date(value: date) -> str:
    return f"{value.year:04d}-{value.month:02d}-{value.day:02d}"


# --------------------------------------------------------------------------- QCJ-1


def _qcj_normalize(value: Any, path: str) -> Any:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, str):
        return require_utf8_text(value, path)
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
        return format_date(value)
    if isinstance(value, time):
        local = to_canonical_local_time(value, path)
        if local.microsecond:
            raise ValueError(f"QCJ-1: sub-second local time is not representable at {path}")
        return f"{local.hour:02d}:{local.minute:02d}:{local.second:02d}"
    if isinstance(value, Mapping):
        out: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError(f"QCJ-1: object keys must be strings at {path}")
            require_utf8_text(key, path)
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


QCT_DECIMAL_PRECISION = 28
_QCT_DECIMAL_CONTEXT = Context(
    prec=QCT_DECIMAL_PRECISION,
    rounding=ROUND_HALF_EVEN,
    Emin=-999999,
    Emax=999999,
    traps=[InvalidOperation, DivisionByZero, Overflow],
)


def format_decimal(value: Any, scale: int) -> str:
    """
    Décimal à échelle fixe, arrondi au pair le plus proche sur la valeur exacte.

    Domaine : résultat d'au plus ``QCT_DECIMAL_PRECISION`` chiffres significatifs (partie
    entière + ``scale``). Le contexte décimal est explicite : le contexte global du processus
    n'influence ni le résultat ni le domaine. Hors domaine → ``ValueError``.
    """
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
    if isinstance(scale, bool) or not isinstance(scale, int) or scale < 0:
        raise ValueError(f"QCT-1: decimal scale must be a non-negative integer; got {scale!r}")
    try:
        quantized = exact.quantize(Decimal((0, (1,), -scale)), context=_QCT_DECIMAL_CONTEXT)
    except InvalidOperation as exc:
        raise ValueError(
            f"QCT-1: decimal {value!r} exceeds {QCT_DECIMAL_PRECISION} significant digits "
            f"at scale {scale}"
        ) from exc
    if quantized.is_zero():
        quantized = quantized.copy_abs()
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
        return format_date(value)
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
    names: list[str] = []
    for i, column in enumerate(columns):
        if not isinstance(column, Mapping):
            raise ValueError(f"QCT-1: column descriptor {i} must be a mapping")
        if "name" not in column:
            raise ValueError(f"QCT-1: column descriptor {i} missing 'name'")
        if "type" not in column:
            raise ValueError(f"QCT-1: column {column['name']!r} missing 'type'")
        names.append(column["name"])
    if len(set(names)) != len(names):
        raise ValueError("QCT-1: duplicate column names in schema")
    by_name = {c["name"]: c for c in columns}
    for key in primary_key:
        if key not in by_name:
            raise ValueError(f"QCT-1: primary key column {key!r} not in schema")
        if by_name[key]["type"] not in {"date", "datetime", "integer", "string"}:
            raise ValueError(f"QCT-1: primary key column {key!r} has non-orderable type")
        if by_name[key].get("nullable", False):
            raise ValueError(f"QCT-1: primary key column {key!r} must not be nullable")

    def _pk_tuple(row: Mapping[str, Any]) -> tuple[Any, ...]:
        keys: list[Any] = []
        for key in primary_key:
            value = row[key]
            if by_name[key]["type"] == "datetime":
                keys.append(to_canonical_utc(value, f"column {key!r}"))
            else:
                keys.append(value)
        return tuple(keys)

    # Chaque cellule est validée avant le tri. Les erreurs de toutes les lignes sont
    # collectées puis triées par clé primaire canonique (invariance par permutation).
    formatted: list[tuple[tuple[Any, ...], str]] = []
    errors: list[tuple[str, str]] = []
    for row in rows:
        if not isinstance(row, Mapping):
            errors.append(("", f"QCT-1: each row must be a mapping; got {type(row).__name__}"))
            continue
        try:
            for key in row:
                if not isinstance(key, str):
                    raise ValueError(
                        f"QCT-1: row keys must be strings; got {type(key).__name__}"
                    )
            extra = set(row) - set(names)
            if extra:
                raise ValueError(f"QCT-1: row has columns outside schema: {sorted(extra)}")
            line = ",".join(_format_cell(by_name[n], row.get(n)) for n in names)
            pk = _pk_tuple(row)
            formatted.append((pk, line))
        except ValueError as exc:
            try:
                pk_repr = repr(_pk_tuple(row))
            except Exception:
                pk_repr = ""
            errors.append((pk_repr, str(exc)))
    if errors:
        errors.sort()
        raise ValueError(errors[0][1])

    formatted.sort(key=lambda item: item[0])
    for previous, current in zip(formatted, formatted[1:], strict=False):
        if previous[0] == current[0]:
            raise ValueError(f"QCT-1: duplicate primary key {current[0]!r}")

    lines = [",".join(names), *(line for _, line in formatted)]
    return ("\n".join(lines) + "\n").encode("utf-8")


# --------------------------------------------------------------------------- QCC-1


def canonical_calendar_bytes(sessions: Sequence[date]) -> bytes:
    """QCC-1 : une date ISO ``YYYY-MM-DD`` par ligne, strictement croissante, ``\\n`` final."""
    if not sessions:
        raise ValueError("QCC-1: session list must not be empty")
    for session in sessions:
        if isinstance(session, datetime) or not isinstance(session, date):
            raise ValueError("QCC-1: sessions must be dates")
    for previous, current in zip(sessions, sessions[1:], strict=False):
        if not previous < current:
            raise ValueError("QCC-1: sessions must be strictly increasing")
    return "".join(f"{format_date(s)}\n" for s in sessions).encode("utf-8")
