"""Amendment B — canonical numerical input (synthetic only; no market E01)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from quant.i03.canonical_input import (
    AUTHORIZED_MANIFEST_GIT_TRANSPORT_SHA256,
    AUTHORIZED_MANIFEST_PRODUCER_WT_CRLF_SHA256,
    AUTHORIZED_RETURNS_NPY_FILE_SHA256,
    AUTHORIZED_RETURNS_SHA256,
    SCHEMA_ID,
    CanonicalInputError,
    canonicalize_returns,
    canonicalize_text_utf8_lf,
    file_sha256,
    load_canonical_artifact,
    payload_sha256,
    serialize_manifest_canonical,
    text_transport_sha256,
    write_canonical_artifact,
)
from quant.i03.compare_hat import compare_artifacts
from quant.i03.params import DEFAULT_CONFIG
from quant.i03.pipeline import artifact_dict, run_structural_analysis


def _synth_returns(n: int = 900, seed: int = 11) -> np.ndarray:
    rng = np.random.default_rng(seed)
    r = np.full(n, np.nan, dtype=np.float64)
    r[1:] = rng.normal(0.0, 0.01, size=n - 1)
    return canonicalize_returns(r)


def _write_synth(tmp: Path, returns: np.ndarray | None = None) -> tuple[np.ndarray, dict]:
    r = returns if returns is not None else _synth_returns()
    man = write_canonical_artifact(
        tmp,
        r,
        source_snapshot_stem="SYNTHETIC-TEST",
        source_csv_path=None,
        source_meta_path=None,
        source_csv_file_sha256=None,
        source_meta_file_sha256=None,
        n_sessions=int(r.shape[0]),
        first_session="1990-01-01",
        last_session="1990-01-02",
        acquired_at_utc="2026-01-01T00:00:00+00:00",
        price_payload_sha256="sha256:" + ("ab" * 32),
        producer_note="synthetic unit test",
    )
    return r, man


def test_valid_artifact_roundtrip(tmp_path: Path) -> None:
    original, man = _write_synth(tmp_path)
    loaded, man2 = load_canonical_artifact(tmp_path)
    assert man["schema"] == SCHEMA_ID
    assert man2["return_payload_sha256"] == payload_sha256(original)
    assert np.array_equal(original, loaded, equal_nan=True)
    assert original.dtype == np.dtype("<f8") or str(original.dtype) in ("float64", "<f8")


def test_wrong_file_hash(tmp_path: Path) -> None:
    _write_synth(tmp_path)
    man = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    man["returns_npy_file_sha256"] = "sha256:" + ("00" * 32)
    (tmp_path / "manifest.json").write_text(json.dumps(man), encoding="utf-8")
    with pytest.raises(CanonicalInputError, match="FILE HASH"):
        load_canonical_artifact(tmp_path)


def test_wrong_payload_hash(tmp_path: Path) -> None:
    _write_synth(tmp_path)
    man = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    man["return_payload_sha256"] = "sha256:" + ("11" * 32)
    # keep file hash consistent with file
    (tmp_path / "manifest.json").write_text(
        json.dumps(man, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with pytest.raises(CanonicalInputError, match="PAYLOAD HASH"):
        load_canonical_artifact(tmp_path)


def test_wrong_dtype_rejected(tmp_path: Path) -> None:
    r = _synth_returns()
    # float32 save
    bad = np.ascontiguousarray(r, dtype="<f4")
    np.save(tmp_path / "returns.npy", bad, allow_pickle=False)
    man = {
        "schema": SCHEMA_ID,
        "n_sessions": int(r.shape[0]),
        "shape": list(r.shape),
        "dtype": "<f8",
        "byte_order": "little",
        "return_payload_sha256": payload_sha256(r),
        "returns_npy_file_sha256": file_sha256(tmp_path / "returns.npy"),
        "source_snapshot_stem": "X",
        "first_session": "a",
        "last_session": "b",
        "acquired_at_utc": "c",
        "price_payload_sha256": "sha256:" + ("cd" * 32),
        "classification": "EXPLORATORY",
        "qualification": "UNQUALIFIED",
    }
    (tmp_path / "manifest.json").write_text(json.dumps(man), encoding="utf-8")
    with pytest.raises(CanonicalInputError):
        load_canonical_artifact(tmp_path)


def test_wrong_endian_rejected(tmp_path: Path) -> None:
    r = _synth_returns()
    be = np.ascontiguousarray(r, dtype=">f8")
    np.save(tmp_path / "returns.npy", be, allow_pickle=False)
    man = {
        "schema": SCHEMA_ID,
        "n_sessions": int(r.shape[0]),
        "shape": list(r.shape),
        "dtype": "<f8",
        "byte_order": "little",
        "return_payload_sha256": payload_sha256(r),
        "returns_npy_file_sha256": file_sha256(tmp_path / "returns.npy"),
        "source_snapshot_stem": "X",
        "first_session": "a",
        "last_session": "b",
        "acquired_at_utc": "c",
        "price_payload_sha256": "sha256:" + ("cd" * 32),
        "classification": "EXPLORATORY",
        "qualification": "UNQUALIFIED",
    }
    (tmp_path / "manifest.json").write_text(json.dumps(man), encoding="utf-8")
    with pytest.raises(CanonicalInputError, match="little-endian"):
        load_canonical_artifact(tmp_path)


def test_wrong_shape(tmp_path: Path) -> None:
    r = _synth_returns(n=900)
    write_canonical_artifact(
        tmp_path,
        r,
        source_snapshot_stem="X",
        source_csv_path=None,
        source_meta_path=None,
        source_csv_file_sha256=None,
        source_meta_file_sha256=None,
        n_sessions=900,
        first_session="a",
        last_session="b",
        acquired_at_utc="c",
        price_payload_sha256="sha256:" + ("cd" * 32),
    )
    man = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    man["n_sessions"] = 901
    man["shape"] = [901]
    (tmp_path / "manifest.json").write_text(json.dumps(man), encoding="utf-8")
    with pytest.raises(CanonicalInputError):
        load_canonical_artifact(tmp_path)


def test_incorrect_initial_nan(tmp_path: Path) -> None:
    r = _synth_returns()
    r = r.copy()
    r[0] = 0.0
    with pytest.raises(CanonicalInputError, match="returns\\[0\\]"):
        write_canonical_artifact(
            tmp_path,
            r,
            source_snapshot_stem="X",
            source_csv_path=None,
            source_meta_path=None,
            source_csv_file_sha256=None,
            source_meta_file_sha256=None,
            n_sessions=int(r.shape[0]),
            first_session="a",
            last_session="b",
            acquired_at_utc="c",
            price_payload_sha256="sha256:" + ("cd" * 32),
        )


def test_nonfinite_body(tmp_path: Path) -> None:
    r = _synth_returns()
    r = r.copy()
    r[5] = np.inf
    with pytest.raises(CanonicalInputError, match="finite"):
        write_canonical_artifact(
            tmp_path,
            r,
            source_snapshot_stem="X",
            source_csv_path=None,
            source_meta_path=None,
            source_csv_file_sha256=None,
            source_meta_file_sha256=None,
            n_sessions=int(r.shape[0]),
            first_session="a",
            last_session="b",
            acquired_at_utc="c",
            price_payload_sha256="sha256:" + ("cd" * 32),
        )


def test_modified_manifest_schema(tmp_path: Path) -> None:
    _write_synth(tmp_path)
    man = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    man["schema"] = "WRONG"
    (tmp_path / "manifest.json").write_text(json.dumps(man), encoding="utf-8")
    with pytest.raises(CanonicalInputError, match="schema"):
        load_canonical_artifact(tmp_path)


def test_incorrect_source_identity_authorized_gate(tmp_path: Path) -> None:
    _write_synth(tmp_path)
    with pytest.raises(CanonicalInputError, match="authorized SPY"):
        load_canonical_artifact(tmp_path, require_authorized_spy=True)


def test_object_array_forbidden(tmp_path: Path) -> None:
    # Construct an object-dtype npy via allow_pickle path then reject on load
    obj = np.array([np.nan, 0.1, 0.2], dtype=object)
    # np.save with object requires pickle; write then ensure our loader rejects
    np.save(tmp_path / "returns.npy", obj, allow_pickle=True)
    man = {
        "schema": SCHEMA_ID,
        "n_sessions": 3,
        "shape": [3],
        "dtype": "<f8",
        "byte_order": "little",
        "return_payload_sha256": "sha256:" + ("ee" * 32),
        "returns_npy_file_sha256": file_sha256(tmp_path / "returns.npy"),
        "source_snapshot_stem": "X",
        "first_session": "a",
        "last_session": "b",
        "acquired_at_utc": "c",
        "price_payload_sha256": "sha256:" + ("cd" * 32),
        "classification": "EXPLORATORY",
        "qualification": "UNQUALIFIED",
    }
    (tmp_path / "manifest.json").write_text(json.dumps(man), encoding="utf-8")
    with pytest.raises((CanonicalInputError, ValueError)):
        load_canonical_artifact(tmp_path)


def test_deterministic_roundtrip_and_pipeline_semantic_identity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("I03_ALLOW_TEST_OVERRIDES", "1")
    from quant.i03.fixture_hat import generate_hat_returns

    original = canonicalize_returns(generate_hat_returns())
    write_canonical_artifact(
        tmp_path,
        original,
        source_snapshot_stem="SYNTH-HAT-EQ",
        source_csv_path=None,
        source_meta_path=None,
        source_csv_file_sha256=None,
        source_meta_file_sha256=None,
        n_sessions=int(original.shape[0]),
        first_session="s0",
        last_session="s1",
        acquired_at_utc="t0",
        price_payload_sha256="sha256:" + ("aa" * 32),
    )
    loaded, _ = load_canonical_artifact(tmp_path)
    assert np.array_equal(original, loaded, equal_nan=True)
    assert payload_sha256(original) == payload_sha256(loaded)

    a = run_structural_analysis(
        original, DEFAULT_CONFIG, B_n4=2, B_n3=2, compute_locality_on_n4=False
    )
    b = run_structural_analysis(
        loaded, DEFAULT_CONFIG, B_n4=2, B_n3=2, compute_locality_on_n4=False
    )
    art_a = artifact_dict(a, input_hash=payload_sha256(original), mode="TEST")
    art_b = artifact_dict(b, input_hash=payload_sha256(loaded), mode="TEST")
    cmp = compare_artifacts(art_a, art_b)
    assert cmp["status"] == "SEMANTIC_IDENTICAL", cmp


def test_manifest_transport_identity_lf_canonical_and_crlf_invariant(
    tmp_path: Path,
) -> None:
    """Transport hash is LF Git identity; CRLF checkout must not change it."""

    original, man = _write_synth(tmp_path)
    man_path = tmp_path / "manifest.json"
    raw_lf = man_path.read_bytes()
    assert b"\r" not in raw_lf
    assert serialize_manifest_canonical(man) == raw_lf

    transport = text_transport_sha256(man_path)
    assert transport == text_transport_sha256(raw_lf)

    # Simulate Windows autocrlf checkout of the same logical JSON.
    crlf_path = tmp_path / "manifest_crlf.json"
    crlf_bytes = raw_lf.replace(b"\n", b"\r\n")
    assert b"\r\n" in crlf_bytes
    crlf_path.write_bytes(crlf_bytes)
    assert text_transport_sha256(crlf_path) == transport
    assert canonicalize_text_utf8_lf(crlf_bytes) == raw_lf

    # Raw working-tree hash may differ under CRLF; transport hash must not.
    assert file_sha256(crlf_path) != file_sha256(man_path)

    npy_before = file_sha256(tmp_path / "returns.npy")
    payload_before = payload_sha256(original)
    loaded, _ = load_canonical_artifact(tmp_path)
    assert file_sha256(tmp_path / "returns.npy") == npy_before
    assert payload_sha256(loaded) == payload_before
    assert np.array_equal(original, loaded, equal_nan=True)


def test_authorized_spy_manifest_transport_constants_and_crlf_checkout(
    tmp_path: Path,
) -> None:
    """M1 artifact: Git LF transport hash; CRLF WT hash is historical only."""

    root = Path(__file__).resolve().parents[2]
    src = root / "data" / "exploratory" / "canonical_i03_spy_v1"
    if not (src / "returns.npy").is_file():
        pytest.skip("authorized SPY canonical artifact not present")

    npy_h = file_sha256(src / "returns.npy")
    assert npy_h == AUTHORIZED_RETURNS_NPY_FILE_SHA256
    man_raw = (src / "manifest.json").read_bytes()
    transport = text_transport_sha256(man_raw)
    assert transport == AUTHORIZED_MANIFEST_GIT_TRANSPORT_SHA256
    # Historical M1 CRLF working-tree hash (NON-CANONICAL for transport).
    crlf = canonicalize_text_utf8_lf(man_raw).replace(b"\n", b"\r\n")
    assert (
        "sha256:" + __import__("hashlib").sha256(crlf).hexdigest()
        == AUTHORIZED_MANIFEST_PRODUCER_WT_CRLF_SHA256
    )

    # Copy artifact and force CRLF manifest; authorized gate must still PASS.
    dest = tmp_path / "canon"
    dest.mkdir()
    (dest / "returns.npy").write_bytes((src / "returns.npy").read_bytes())
    (dest / "manifest.json").write_bytes(crlf)
    loaded, man = load_canonical_artifact(dest, require_authorized_spy=True)
    assert payload_sha256(loaded) == AUTHORIZED_RETURNS_SHA256
    assert man["returns_npy_file_sha256"] == AUTHORIZED_RETURNS_NPY_FILE_SHA256
