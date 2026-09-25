"""Deterministic synthetic HAT fixture for I02 (software validation only).

Construction (fully specified, no RNG, no market calibration):

    r_0 = NaN
    for t = 1..N-1:
        base_t = 0.012 * sin(2π t / 17)
               + 0.006 * sin(2π t / 53)
               + 0.003 * cos(2π t / 7)
        amp_t  = 1 + 0.35 * sin(2π t / 251)
        r_t    = base_t * amp_t

N = 900 (enough for M=252, |A_t|≥50, Z^(21), h=10, Spearman, b∈{20,40,80}).

NOT scientific evidence. NOT SPY. NOT market-derived.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

FIXTURE_ID = "I02-HAT-FIXTURE-v1"
FIXTURE_N = 900
FIXTURE_FILENAME = "fixture_v1.npz"


def generate_hat_returns(n: int = FIXTURE_N) -> np.ndarray:
    """Return length-``n`` synthetic log-return series (index 0 = NaN)."""

    if n < 400:
        raise ValueError("HAT fixture requires n >= 400")
    r = np.full(n, np.nan, dtype=np.float64)
    t = np.arange(1, n, dtype=np.float64)
    base = (
        0.012 * np.sin(2.0 * np.pi * t / 17.0)
        + 0.006 * np.sin(2.0 * np.pi * t / 53.0)
        + 0.003 * np.cos(2.0 * np.pi * t / 7.0)
    )
    amp = 1.0 + 0.35 * np.sin(2.0 * np.pi * t / 251.0)
    r[1:] = base * amp
    return r


def fixture_sha256(returns: np.ndarray) -> str:
    """Content hash of float64 little-endian payload (scientific identity)."""

    payload = np.asarray(returns, dtype=np.float64).tobytes(order="C")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def write_fixture(directory: Path) -> dict:
    """Write versioned fixture + metadata; return metadata dict."""

    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    returns = generate_hat_returns()
    digest = fixture_sha256(returns)
    npz_path = directory / FIXTURE_FILENAME
    np.savez_compressed(npz_path, returns=returns, fixture_id=np.array(FIXTURE_ID))
    meta = {
        "fixture_id": FIXTURE_ID,
        "n": int(returns.shape[0]),
        "sha256": digest,
        "filename": FIXTURE_FILENAME,
        "construction": (
            "r[0]=NaN; r[t]=(0.012*sin(2*pi*t/17)+0.006*sin(2*pi*t/53)+"
            "0.003*cos(2*pi*t/7))*(1+0.35*sin(2*pi*t/251)) for t=1..n-1"
        ),
        "purpose": "I02 HAT software validation only — not scientific evidence",
        "market_data": False,
    }
    meta_path = directory / "fixture_v1.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return meta


def load_fixture(path: Path) -> tuple[np.ndarray, str]:
    """Load returns array and return ``(returns, sha256)``."""

    path = Path(path)
    if path.suffix == ".npz":
        data = np.load(path, allow_pickle=False)
        returns = np.asarray(data["returns"], dtype=np.float64)
    elif path.suffix == ".npy":
        returns = np.asarray(np.load(path), dtype=np.float64)
    else:
        raise ValueError(f"unsupported fixture format: {path.suffix}")
    return returns, fixture_sha256(returns)
