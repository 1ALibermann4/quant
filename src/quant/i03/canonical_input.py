"""I03 Amendment B — canonical numerical input (transport only).

Materializes the authorized exploratory return vector as ``returns.npy`` +
``manifest.json`` for bit-identical Local → Cloud transfer.

Scientific pipeline entry remains ``run_structural_analysis(returns, cfg)``.
Does not alter prereg estimands, nulls, seeds, or verdict logic.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np

from quant.i01.returns import log_returns
from quant.i03.e01 import (
    AUTHORIZED_ACQUIRED,
    AUTHORIZED_CACHE_STEM,
    AUTHORIZED_FIRST,
    AUTHORIZED_LAST,
    AUTHORIZED_N_SESSIONS,
    AUTHORIZED_PRICE_SHA256,
    AUTHORIZED_RETURNS_SHA256,
)

SCHEMA_ID = "I03-CANONICAL-INPUT-v1"
RETURNS_FILENAME = "returns.npy"
MANIFEST_FILENAME = "manifest.json"

# Expected raw-file identities of the frozen git snapshot (transport layer).
AUTHORIZED_CSV_FILE_SHA256 = (
    "sha256:ac7c6a7f081e3548d94c6c744a31b3398ccffae5129799015b3331568159b2c2"
)
AUTHORIZED_META_FILE_SHA256 = (
    "sha256:c37b7ae0ed24dd6510feef5c753f1dca8201b793e066628e1730b43ebf507caf"
)
AUTHORIZED_CSV_SIZE = 1_080_047
AUTHORIZED_META_SIZE = 974

# Authorized SPY canonical artifact (M1) — dual hash disciplines for text vs binary.
AUTHORIZED_RETURNS_NPY_FILE_SHA256 = (
    "sha256:4aee1aaea6886a727b5f322e51af9e2c05132b32aaaa47d0d5c0dc68c795943e"
)
# Git blob / Cloud LF bytes — CANONICAL FOR GIT TRANSPORT (M2 discovery).
AUTHORIZED_MANIFEST_GIT_TRANSPORT_SHA256 = (
    "sha256:9d285f24f031424aa016313195b25917e189f8aa6cb0e5960c18587cee0cbf8f"
)
# M1 Windows working-tree CRLF bytes — historical provenance only; NON-CANONICAL.
AUTHORIZED_MANIFEST_PRODUCER_WT_CRLF_SHA256 = (
    "sha256:4cf1e219a824f5a73739c8eaaa160a81e4caf92a5b0e6fba91a70c690f5c6901"
)


class CanonicalInputError(RuntimeError):
    """Fail-closed validation / production error for Amendment B."""


def _git_head() -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None


def file_sha256(path: Path) -> str:
    """SHA-256 of raw file bytes (FILE HASH)."""

    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def payload_sha256(returns: np.ndarray) -> str:
    """SHA-256 of float64 little-endian C-order payload (FLOAT64 PAYLOAD HASH)."""

    arr = np.ascontiguousarray(returns, dtype="<f8")
    return "sha256:" + hashlib.sha256(arr.tobytes(order="C")).hexdigest()


def canonicalize_text_utf8_lf(raw: bytes) -> bytes:
    """Normalize UTF-8 text to LF-only (Git transport identity for JSON).

    CRLF working-tree checkouts hash to the same transport identity as the
    committed LF blob. Lone CR is rejected.
    """

    if b"\r\n" in raw:
        raw = raw.replace(b"\r\n", b"\n")
    if b"\r" in raw:
        raise CanonicalInputError("text artifact contains unexpected CR bytes")
    return raw


def text_transport_sha256(raw_or_path: bytes | Path) -> str:
    """SHA-256 of LF-canonical UTF-8 text (CANONICAL GIT TRANSPORT FILE HASH)."""

    raw = (
        Path(raw_or_path).read_bytes()
        if not isinstance(raw_or_path, (bytes, bytearray))
        else bytes(raw_or_path)
    )
    return "sha256:" + hashlib.sha256(canonicalize_text_utf8_lf(raw)).hexdigest()


def serialize_manifest_canonical(manifest: dict[str, Any]) -> bytes:
    """Deterministic UTF-8 JSON with LF newlines only (no OS text-mode translation)."""

    text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    raw = text.encode("utf-8")
    if b"\r" in raw:
        raise CanonicalInputError("canonical manifest serialization must be LF-only")
    return raw


def write_manifest_json(path: Path, manifest: dict[str, Any]) -> str:
    """Write manifest via binary LF bytes; return GIT TRANSPORT FILE HASH."""

    path = Path(path)
    raw = serialize_manifest_canonical(manifest)
    path.write_bytes(raw)
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def canonicalize_returns(returns: np.ndarray) -> np.ndarray:
    """Return a float64 little-endian C-contiguous copy (no value changes)."""

    return np.ascontiguousarray(np.asarray(returns), dtype="<f8")


def validate_returns_semantics(
    returns: np.ndarray,
    *,
    expected_n: int | None = None,
) -> None:
    """Structural checks on the return vector (not market science)."""

    if not isinstance(returns, np.ndarray):
        raise CanonicalInputError("returns must be a numpy.ndarray")
    if returns.dtype != np.dtype("<f8") and returns.dtype != np.dtype(">f8"):
        # allow native float64 only if it is little-endian on this platform
        if returns.dtype != np.dtype(np.float64):
            raise CanonicalInputError(f"dtype must be float64, got {returns.dtype}")
    if returns.ndim != 1:
        raise CanonicalInputError(f"returns must be 1-D, got shape {returns.shape}")
    if expected_n is not None and returns.shape[0] != expected_n:
        raise CanonicalInputError(
            f"shape must be ({expected_n},), got {returns.shape}"
        )
    if returns.shape[0] < 2:
        raise CanonicalInputError("returns length must be >= 2")
    if not np.isnan(returns[0]):
        raise CanonicalInputError("returns[0] must be NaN (I02/I03 padding)")
    body = returns[1:]
    if body.size == 0:
        raise CanonicalInputError("returns body is empty")
    if not np.isfinite(body).all():
        raise CanonicalInputError("returns[1:] must be entirely finite")


def write_returns_npy(path: Path, returns: np.ndarray) -> str:
    """Write ``returns.npy`` without pickle; return FILE HASH of the written file."""

    path = Path(path)
    arr = canonicalize_returns(returns)
    validate_returns_semantics(arr)
    np.save(path, arr, allow_pickle=False)
    return file_sha256(path)


def load_returns_npy(path: Path) -> np.ndarray:
    """Load ``returns.npy`` without pickle; reject object arrays."""

    path = Path(path)
    arr = np.load(path, allow_pickle=False)
    if arr.dtype == object or getattr(arr.dtype, "hasobject", False):
        raise CanonicalInputError("object / pickle arrays are forbidden")
    if arr.dtype.kind != "f" or arr.dtype.itemsize != 8:
        raise CanonicalInputError(
            f"returns.npy must be float64, got {arr.dtype}"
        )
    # Force explicit little-endian float64 view/copy without changing bits when LE
    if arr.dtype.byteorder == ">" or (
        arr.dtype.byteorder == "=" and not np.little_endian
    ):
        raise CanonicalInputError(
            f"returns.npy must be little-endian float64, got {arr.dtype}"
        )
    out = canonicalize_returns(arr)
    return out


def build_manifest(
    *,
    returns: np.ndarray,
    returns_file_sha256: str,
    source_snapshot_stem: str,
    source_csv_path: Path | None,
    source_meta_path: Path | None,
    source_csv_file_sha256: str | None,
    source_meta_file_sha256: str | None,
    n_sessions: int,
    first_session: str,
    last_session: str,
    acquired_at_utc: str,
    price_payload_sha256: str,
    classification: str = "EXPLORATORY",
    qualification: str = "UNQUALIFIED",
    producer_note: str = "",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build Amendment-B manifest (FILE HASH vs FLOAT64 PAYLOAD HASH)."""

    arr = canonicalize_returns(returns)
    manifest: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "amendment": "I03-AMENDMENT-B",
        "classification": classification,
        "qualification": qualification,
        "scientifically_promotable": False,
        "source_snapshot_stem": source_snapshot_stem,
        "source_csv_path": str(source_csv_path) if source_csv_path else None,
        "source_meta_path": str(source_meta_path) if source_meta_path else None,
        "source_csv_file_sha256": source_csv_file_sha256,
        "source_meta_file_sha256": source_meta_file_sha256,
        "n_sessions": int(n_sessions),
        "first_session": first_session,
        "last_session": last_session,
        "acquired_at_utc": acquired_at_utc,
        "producer_environment": {
            "python": sys.version.replace("\n", " "),
            "implementation": sys.implementation.name,
            "compiler": platform.python_compiler(),
            "executable": sys.executable,
            "platform": platform.platform(),
            "architecture": list(platform.architecture()),
            "machine": platform.machine(),
            "numpy": np.__version__,
        },
        "implementation_commit": _git_head(),
        "price_payload_sha256": price_payload_sha256,
        "return_payload_sha256": payload_sha256(arr),
        "returns_npy": RETURNS_FILENAME,
        "returns_npy_file_sha256": returns_file_sha256,
        "dtype": "<f8",
        "shape": list(arr.shape),
        "byte_order": "little",
        "c_contiguous": True,
        "r0_is_nan": True,
        "note": (
            "FLOAT64 PAYLOAD HASH = SHA-256 of float64 little-endian C-order bytes. "
            "RETURNS.NPY FILE HASH = SHA-256 of the on-disk .npy container. "
            "MANIFEST GIT TRANSPORT FILE HASH = SHA-256 of UTF-8 JSON with LF "
            "newlines (Git blob / transferred bytes); never use OS CRLF "
            "working-tree bytes as transport identity. "
            "Amendment B transport only — not a scientific redesign."
        ),
        "producer_note": producer_note,
    }
    if extra:
        manifest["extra"] = extra
    return manifest


def write_canonical_artifact(
    out_dir: Path,
    returns: np.ndarray,
    *,
    source_snapshot_stem: str,
    source_csv_path: Path | None,
    source_meta_path: Path | None,
    source_csv_file_sha256: str | None,
    source_meta_file_sha256: str | None,
    n_sessions: int,
    first_session: str,
    last_session: str,
    acquired_at_utc: str,
    price_payload_sha256: str,
    classification: str = "EXPLORATORY",
    qualification: str = "UNQUALIFIED",
    producer_note: str = "",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Write ``returns.npy`` + ``manifest.json``; return the written manifest."""

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    arr = canonicalize_returns(returns)
    validate_returns_semantics(arr, expected_n=n_sessions)
    npy_path = out_dir / RETURNS_FILENAME
    file_h = write_returns_npy(npy_path, arr)
    manifest = build_manifest(
        returns=arr,
        returns_file_sha256=file_h,
        source_snapshot_stem=source_snapshot_stem,
        source_csv_path=source_csv_path,
        source_meta_path=source_meta_path,
        source_csv_file_sha256=source_csv_file_sha256,
        source_meta_file_sha256=source_meta_file_sha256,
        n_sessions=n_sessions,
        first_session=first_session,
        last_session=last_session,
        acquired_at_utc=acquired_at_utc,
        price_payload_sha256=price_payload_sha256,
        classification=classification,
        qualification=qualification,
        producer_note=producer_note,
        extra=extra,
    )
    write_manifest_json(out_dir / MANIFEST_FILENAME, manifest)
    return manifest


def load_canonical_artifact(
    directory: Path,
    *,
    require_authorized_spy: bool = False,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Load and fail-closed validate a canonical artifact directory."""

    directory = Path(directory)
    man_path = directory / MANIFEST_FILENAME
    npy_path = directory / RETURNS_FILENAME
    if not man_path.is_file() or not npy_path.is_file():
        raise CanonicalInputError(
            f"missing {MANIFEST_FILENAME} and/or {RETURNS_FILENAME} in {directory}"
        )

    try:
        manifest = json.loads(man_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise CanonicalInputError(f"manifest JSON invalid: {e}") from e

    if manifest.get("schema") != SCHEMA_ID:
        raise CanonicalInputError(
            f"schema must be {SCHEMA_ID}, got {manifest.get('schema')!r}"
        )

    file_h = file_sha256(npy_path)
    if file_h != manifest.get("returns_npy_file_sha256"):
        raise CanonicalInputError(
            f"returns.npy FILE HASH mismatch: {file_h} != "
            f"{manifest.get('returns_npy_file_sha256')}"
        )

    returns = load_returns_npy(npy_path)
    expected_n = manifest.get("n_sessions")
    if not isinstance(expected_n, int):
        raise CanonicalInputError("manifest.n_sessions must be int")
    validate_returns_semantics(returns, expected_n=expected_n)

    if list(returns.shape) != list(manifest.get("shape", [])):
        raise CanonicalInputError("shape mismatch vs manifest")
    if manifest.get("dtype") != "<f8":
        raise CanonicalInputError(
            f"manifest.dtype must be '<f8', got {manifest.get('dtype')}"
        )
    if manifest.get("byte_order") != "little":
        raise CanonicalInputError("manifest.byte_order must be 'little'")

    payload_h = payload_sha256(returns)
    if payload_h != manifest.get("return_payload_sha256"):
        raise CanonicalInputError(
            f"FLOAT64 PAYLOAD HASH mismatch: {payload_h} != "
            f"{manifest.get('return_payload_sha256')}"
        )

    if require_authorized_spy:
        _assert_authorized_manifest(
            manifest,
            payload_h,
            npy_file_h=file_h,
            man_path=man_path,
        )

    return returns, manifest


def _assert_authorized_manifest(
    manifest: dict[str, Any],
    payload_h: str,
    *,
    npy_file_h: str,
    man_path: Path,
) -> None:
    transport_h = text_transport_sha256(man_path)
    checks = {
        "stem": manifest.get("source_snapshot_stem") == AUTHORIZED_CACHE_STEM,
        "n": manifest.get("n_sessions") == AUTHORIZED_N_SESSIONS,
        "first": manifest.get("first_session") == AUTHORIZED_FIRST,
        "last": manifest.get("last_session") == AUTHORIZED_LAST,
        "acquired": manifest.get("acquired_at_utc") == AUTHORIZED_ACQUIRED,
        "price": manifest.get("price_payload_sha256") == AUTHORIZED_PRICE_SHA256,
        "returns": payload_h == AUTHORIZED_RETURNS_SHA256,
        "csv_file": manifest.get("source_csv_file_sha256") == AUTHORIZED_CSV_FILE_SHA256,
        "meta_file": manifest.get("source_meta_file_sha256")
        == AUTHORIZED_META_FILE_SHA256,
        "npy_file": npy_file_h == AUTHORIZED_RETURNS_NPY_FILE_SHA256,
        "manifest_git_transport": transport_h
        == AUTHORIZED_MANIFEST_GIT_TRANSPORT_SHA256,
        "class": manifest.get("classification") == "EXPLORATORY",
        "qual": manifest.get("qualification") == "UNQUALIFIED",
    }
    if not all(checks.values()):
        raise CanonicalInputError(
            "authorized SPY identity checks failed: " + json.dumps(checks, indent=2)
        )


def produce_authorized_canonical(
    *,
    cache_dir: Path,
    out_dir: Path,
) -> dict[str, Any]:
    """Produce canonical artifact from the exact authorized SPY snapshot.

    Fail-closed. Does not download. Does not call yfinance.
    """

    from quant.exploratory.adapter import load_cache_by_stem

    cache_dir = Path(cache_dir)
    csv_path = cache_dir / f"{AUTHORIZED_CACHE_STEM}.csv"
    meta_path = cache_dir / f"{AUTHORIZED_CACHE_STEM}.meta.json"
    if not csv_path.is_file() or not meta_path.is_file():
        raise CanonicalInputError(
            f"authorized snapshot missing under {cache_dir}: "
            f"need {AUTHORIZED_CACHE_STEM}.csv and .meta.json"
        )

    csv_file_h = file_sha256(csv_path)
    meta_file_h = file_sha256(meta_path)
    if csv_file_h != AUTHORIZED_CSV_FILE_SHA256 or csv_path.stat().st_size != AUTHORIZED_CSV_SIZE:
        raise CanonicalInputError(
            f"CSV FILE HASH/size mismatch: {csv_file_h} size={csv_path.stat().st_size}"
        )
    if (
        meta_file_h != AUTHORIZED_META_FILE_SHA256
        or meta_path.stat().st_size != AUTHORIZED_META_SIZE
    ):
        raise CanonicalInputError(
            f"meta FILE HASH/size mismatch: {meta_file_h} size={meta_path.stat().st_size}"
        )

    acq = load_cache_by_stem(cache_dir, AUTHORIZED_CACHE_STEM)
    returns = canonicalize_returns(log_returns(acq.series))
    prices = np.asarray(acq.series.adjusted_price, dtype=np.float64)
    price_h = "sha256:" + hashlib.sha256(
        np.ascontiguousarray(prices, dtype=np.float64).tobytes(order="C")
    ).hexdigest()
    ret_h = payload_sha256(returns)

    if len(acq.series) != AUTHORIZED_N_SESSIONS:
        raise CanonicalInputError("session count mismatch")
    if acq.series.sessions[0].isoformat() != AUTHORIZED_FIRST:
        raise CanonicalInputError("first session mismatch")
    if acq.series.sessions[-1].isoformat() != AUTHORIZED_LAST:
        raise CanonicalInputError("last session mismatch")
    if acq.acquired_at_utc.isoformat() != AUTHORIZED_ACQUIRED:
        raise CanonicalInputError("acquired_at_utc mismatch")
    if price_h != AUTHORIZED_PRICE_SHA256:
        raise CanonicalInputError(f"price payload mismatch: {price_h}")
    if ret_h != AUTHORIZED_RETURNS_SHA256:
        raise CanonicalInputError(
            f"return payload mismatch: {ret_h} "
            "(use canonical Windows MSC NumPy environment)"
        )

    validate_returns_semantics(returns, expected_n=AUTHORIZED_N_SESSIONS)

    write_canonical_artifact(
        out_dir,
        returns,
        source_snapshot_stem=AUTHORIZED_CACHE_STEM,
        source_csv_path=csv_path,
        source_meta_path=meta_path,
        source_csv_file_sha256=csv_file_h,
        source_meta_file_sha256=meta_file_h,
        n_sessions=AUTHORIZED_N_SESSIONS,
        first_session=AUTHORIZED_FIRST,
        last_session=AUTHORIZED_LAST,
        acquired_at_utc=AUTHORIZED_ACQUIRED,
        price_payload_sha256=price_h,
        classification="EXPLORATORY",
        qualification="UNQUALIFIED",
        producer_note=(
            "Produced via load_cache_by_stem + log_returns on the authorized "
            "DR-008 snapshot. Amendment B transport only."
        ),
    )
    loaded, man2 = load_canonical_artifact(out_dir, require_authorized_spy=True)
    if payload_sha256(loaded) != AUTHORIZED_RETURNS_SHA256:
        raise CanonicalInputError("post-write payload gate failed")
    if not np.array_equal(loaded, returns, equal_nan=True):
        raise CanonicalInputError("post-write bitwise equality failed")
    return man2
