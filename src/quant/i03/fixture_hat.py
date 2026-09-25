"""Deterministic synthetic fixture for I03 HAT (no market data).

Fixture ID: I03-HAT-FIXTURE-v1
Not tuned for recurrence significance or any scientific verdict.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

FIXTURE_ID = "I03-HAT-FIXTURE-v1"
GENERATOR_VERSION = "1.0.0"
FIXTURE_SEED = 20260926
FIXTURE_LENGTH = 2400  # index 0 unused padding; scientific length T=2400


def generate_hat_returns(
    *,
    length: int = FIXTURE_LENGTH,
    seed: int = FIXTURE_SEED,
) -> np.ndarray:
    """Build synthetic returns with mild structure, not market-calibrated.

    Components (transparent):
      - seeded Gaussian innovations;
      - low-frequency sinusoidal mean drift (tiny);
      - deterministic heteroskedastic envelope.

    Index 0 is NaN padding (I02/I03 G0 convention).
    """

    rng = np.random.default_rng(seed)
    r = np.full(length, np.nan, dtype=np.float64)
    n = length - 1
    t = np.arange(n, dtype=np.float64)
    innov = rng.normal(0.0, 1.0, size=n)
    low_freq = 0.0005 * np.sin(2.0 * np.pi * t / 250.0)
    vol = 0.008 + 0.004 * (0.5 + 0.5 * np.sin(2.0 * np.pi * t / 80.0))
    r[1:] = low_freq + vol * innov
    return r


def fixture_sha256(returns: np.ndarray) -> str:
    """SHA-256 of float64 little-endian payload (nan-preserving bytes)."""

    raw = np.ascontiguousarray(returns, dtype=np.float64).tobytes()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def write_fixture(directory: Path) -> dict:
    """Write ``fixture_v1.npy`` + ``fixture_v1.meta.json``; return metadata."""

    directory.mkdir(parents=True, exist_ok=True)
    returns = generate_hat_returns()
    digest = fixture_sha256(returns)
    npy_path = directory / "fixture_v1.npy"
    meta_path = directory / "fixture_v1.meta.json"
    np.save(npy_path, returns)
    meta = {
        "fixture_id": FIXTURE_ID,
        "generator_version": GENERATOR_VERSION,
        "seed": FIXTURE_SEED,
        "length": FIXTURE_LENGTH,
        "sha256": digest,
        "npy": str(npy_path.name),
        "note": "SYNTHETIC HAT FIXTURE — NOT MARKET DATA — NOT TUNED FOR VERDICT",
        "components": [
            "seeded_gaussian_innovations",
            "tiny_sinusoidal_mean",
            "deterministic_heteroskedastic_envelope",
        ],
    }
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    # verify round-trip
    loaded = np.load(npy_path)
    assert fixture_sha256(loaded) == digest
    return meta


def load_fixture(directory: Path) -> tuple[np.ndarray, dict]:
    """Load fixture and verify hash against metadata."""

    meta = json.loads((directory / "fixture_v1.meta.json").read_text(encoding="utf-8"))
    returns = np.load(directory / "fixture_v1.npy")
    digest = fixture_sha256(returns)
    if digest != meta["sha256"]:
        raise RuntimeError(f"fixture hash mismatch: {digest} != {meta['sha256']}")
    return returns, meta
