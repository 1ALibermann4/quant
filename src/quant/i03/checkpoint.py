"""PERF-01 Phase 1C — deterministic surrogate checkpoint / resume.

Execution-state persistence only. Does not alter seeds, B, nulls, or science.
Checkpoint identity is surrogate index ``b`` (1-based, matching I03 doctrine).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict
from enum import Enum
from pathlib import Path
from typing import Any

import numpy as np

from quant.i03.params import I03Config

SCHEMA_MANIFEST = "I03-CHECKPOINT-MANIFEST-v1"
SCHEMA_RECORD = "I03-CHECKPOINT-RECORD-v1"
IMPLEMENTATION_ID = "I03-PERF-01-PHASE1C"


class CheckpointError(RuntimeError):
    """Fail-closed checkpoint / resume error."""


class RunStatus(str, Enum):
    NEW = "NEW"
    INCOMPLETE = "INCOMPLETE"
    COMPLETE = "COMPLETE"
    INVALID = "INVALID"


_B_FILE = re.compile(r"^b_(\d{6})\.json$")


def returns_input_sha256(returns: np.ndarray) -> str:
    """Canonical float64 C-order payload hash of the analysis return vector."""

    arr = np.ascontiguousarray(np.asarray(returns, dtype=np.float64), dtype="<f8")
    return "sha256:" + hashlib.sha256(arr.tobytes(order="C")).hexdigest()


def config_identity(cfg: I03Config) -> dict[str, Any]:
    d = asdict(cfg)
    d["K"] = list(cfg.K)
    return d


def compute_run_id(
    *,
    input_sha256: str,
    cfg: I03Config,
    B_n4: int,
    B_n3: int,
    do_loc_n4: bool,
) -> str:
    """Deterministic run identity (hex SHA-256, no prefix)."""

    payload = {
        "schema": SCHEMA_MANIFEST,
        "implementation": IMPLEMENTATION_ID,
        "input_sha256": input_sha256,
        "config": config_identity(cfg),
        "B_n4": int(B_n4),
        "B_n3": int(B_n3),
        "do_loc_n4": bool(do_loc_n4),
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _payload_sha256(payload: dict[str, Any]) -> str:
    raw = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _json_sanitize(obj: Any) -> Any:
    """Convert numpy scalars/arrays for stable JSON (tests may include returns)."""

    if isinstance(obj, dict):
        return {str(k): _json_sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_sanitize(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, float) and (obj != obj or obj in (float("inf"), float("-inf"))):
        # allow_nan=False path: encode non-finites as strings for integrity
        if obj != obj:
            return "NaN"
        return "Infinity" if obj > 0 else "-Infinity"
    return obj


def _restore_floats(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _restore_floats(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_restore_floats(v) for v in obj]
    if obj == "NaN":
        return float("nan")
    if obj == "Infinity":
        return float("inf")
    if obj == "-Infinity":
        return float("-inf")
    return obj


def normalize_worker_payload(row: dict[str, Any]) -> dict[str, Any]:
    """Restore int keys for theta maps after JSON round-trip."""

    out = dict(row)
    out["b"] = int(out["b"])
    out["seed"] = int(out["seed"])
    if "theta" in out and isinstance(out["theta"], dict):
        out["theta"] = {
            int(p): {int(k): float(v) for k, v in ks.items()}
            for p, ks in out["theta"].items()
        }
    if out.get("locality") is not None:
        loc = []
        for d in out["locality"]:
            loc.append(
                {
                    "period": int(d["period"]),
                    "Lambda": float(d["Lambda"]),
                    "Gamma": float(d["Gamma"]),
                    "hard_degenerate": bool(d["hard_degenerate"]),
                    "n_queries_used": int(d["n_queries_used"]),
                }
            )
        out["locality"] = loc
    if "converged" in out:
        out["converged"] = bool(out["converged"])
    if "iterations" in out:
        out["iterations"] = int(out["iterations"])
    return out


def atomic_write_bytes(path: Path, data: bytes) -> None:
    """Write bytes via temp file + fsync + os.replace (crash-safe replace)."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    try:
        with tmp.open("wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except Exception:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass
        raise


def atomic_write_json(path: Path, obj: dict[str, Any]) -> None:
    data = (
        json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")
    atomic_write_bytes(path, data)


class CheckpointStore:
    """On-disk checkpoint store for N4/N3 surrogate results keyed by ``b``."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.manifest_path = self.root / "manifest.json"
        self.status_path = self.root / "status.json"

    def status(self) -> RunStatus:
        if not self.root.exists():
            return RunStatus.NEW
        if not self.manifest_path.is_file():
            # leftover empties / only tmp → treat as NEW if no records
            if not any(self.root.rglob("b_*.json")):
                return RunStatus.NEW
            return RunStatus.INVALID
        try:
            man = json.loads(self.manifest_path.read_text(encoding="utf-8"))
            st = json.loads(self.status_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return RunStatus.INVALID
        if man.get("schema") != SCHEMA_MANIFEST:
            return RunStatus.INVALID
        label = st.get("status")
        try:
            return RunStatus(label)
        except ValueError:
            return RunStatus.INVALID

    def _family_dir(self, family: str) -> Path:
        if family not in ("N4", "N3"):
            raise CheckpointError(f"unknown family {family!r}")
        return self.root / family

    def record_path(self, family: str, b: int) -> Path:
        return self._family_dir(family) / f"b_{int(b):06d}.json"

    def write_new_manifest(
        self,
        *,
        run_id: str,
        input_sha256: str,
        cfg: I03Config,
        B_n4: int,
        B_n3: int,
        do_loc_n4: bool,
    ) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        man = {
            "schema": SCHEMA_MANIFEST,
            "implementation": IMPLEMENTATION_ID,
            "run_id": run_id,
            "input_sha256": input_sha256,
            "config": config_identity(cfg),
            "B_n4": int(B_n4),
            "B_n3": int(B_n3),
            "do_loc_n4": bool(do_loc_n4),
        }
        atomic_write_json(self.manifest_path, man)
        self._write_status(RunStatus.INCOMPLETE, run_id=run_id, note="initialized")

    def _write_status(
        self, status: RunStatus, *, run_id: str, note: str = ""
    ) -> None:
        atomic_write_json(
            self.status_path,
            {
                "schema": "I03-CHECKPOINT-STATUS-v1",
                "run_id": run_id,
                "status": status.value,
                "note": note,
            },
        )

    def load_manifest(self) -> dict[str, Any]:
        if not self.manifest_path.is_file():
            raise CheckpointError("missing checkpoint manifest")
        try:
            man = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            raise CheckpointError(f"manifest unreadable: {e}") from e
        if man.get("schema") != SCHEMA_MANIFEST:
            raise CheckpointError("incompatible checkpoint schema")
        return man

    def assert_compatible(
        self,
        *,
        run_id: str,
        input_sha256: str,
        cfg: I03Config,
        B_n4: int,
        B_n3: int,
        do_loc_n4: bool,
    ) -> dict[str, Any]:
        man = self.load_manifest()
        expected = {
            "run_id": run_id,
            "input_sha256": input_sha256,
            "config": config_identity(cfg),
            "B_n4": int(B_n4),
            "B_n3": int(B_n3),
            "do_loc_n4": bool(do_loc_n4),
            "implementation": IMPLEMENTATION_ID,
        }
        for key, val in expected.items():
            if man.get(key) != val:
                raise CheckpointError(
                    f"checkpoint run identity mismatch on {key}: "
                    f"store={man.get(key)!r} expected={val!r}"
                )
        return man

    def save_result(
        self,
        row: dict[str, Any],
        *,
        run_id: str,
        expected_seed: int,
    ) -> None:
        """Persist one completed surrogate result atomically."""

        if "b" not in row or "family" not in row:
            raise CheckpointError("cannot checkpoint malformed result")
        b = int(row["b"])
        family = str(row["family"])
        if int(row.get("seed", -1)) != int(expected_seed):
            raise CheckpointError(
                f"seed mismatch for {family} b={b}: "
                f"{row.get('seed')} != {expected_seed}"
            )
        # Drop optional bulky arrays from durable store unless explicitly kept
        payload = {k: v for k, v in row.items() if k != "returns"}
        payload = _json_sanitize(payload)
        body = {
            "schema": SCHEMA_RECORD,
            "run_id": run_id,
            "family": family,
            "b": b,
            "seed": int(expected_seed),
            "payload": payload,
        }
        body["payload_sha256"] = _payload_sha256(payload)
        atomic_write_json(self.record_path(family, b), body)
        self._write_status(
            RunStatus.INCOMPLETE, run_id=run_id, note=f"saved {family} b={b}"
        )

    def load_record(self, family: str, b: int, *, run_id: str) -> dict[str, Any]:
        path = self.record_path(family, b)
        if not path.is_file():
            raise CheckpointError(f"missing checkpoint {family} b={b}")
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            raise CheckpointError(f"corrupt checkpoint {family} b={b}: {e}") from e
        if raw.get("schema") != SCHEMA_RECORD:
            raise CheckpointError(f"bad schema for {family} b={b}")
        if raw.get("run_id") != run_id:
            raise CheckpointError(f"run_id mismatch in {family} b={b}")
        if raw.get("family") != family or int(raw.get("b", -1)) != b:
            raise CheckpointError(f"identity mismatch in {family} b={b}")
        payload = raw.get("payload")
        if not isinstance(payload, dict):
            raise CheckpointError(f"missing payload for {family} b={b}")
        digest = _payload_sha256(payload)
        if digest != raw.get("payload_sha256"):
            raise CheckpointError(f"payload hash mismatch for {family} b={b}")
        if int(raw.get("seed", -1)) != int(payload.get("seed", -2)):
            raise CheckpointError(f"seed field mismatch for {family} b={b}")
        return normalize_worker_payload(_restore_floats(payload))

    def list_completed(self, family: str, *, run_id: str, B: int) -> dict[int, dict[str, Any]]:
        """Load all valid completed records for ``family``; fail closed on corruption."""

        d = self._family_dir(family)
        out: dict[int, dict[str, Any]] = {}
        if not d.is_dir():
            return out
        for path in sorted(d.glob("b_*.json")):
            m = _B_FILE.match(path.name)
            if not m:
                raise CheckpointError(f"unexpected checkpoint filename {path.name}")
            b = int(m.group(1))
            if b < 1 or b > B:
                raise CheckpointError(f"unexpected b={b} in store (B={B})")
            if b in out:
                raise CheckpointError(f"duplicate checkpoint file for b={b}")
            out[b] = self.load_record(family, b, run_id=run_id)
        # Ignore *.tmp leftovers by not globbing them
        return out

    def missing_b(self, family: str, *, run_id: str, B: int) -> list[int]:
        done = self.list_completed(family, run_id=run_id, B=B)
        return [b for b in range(1, B + 1) if b not in done]

    def mark_complete_if_done(self, *, run_id: str, B_n4: int, B_n3: int) -> RunStatus:
        m4 = self.missing_b("N4", run_id=run_id, B=B_n4)
        m3 = self.missing_b("N3", run_id=run_id, B=B_n3)
        if not m4 and not m3:
            self._write_status(RunStatus.COMPLETE, run_id=run_id, note="all b present")
            return RunStatus.COMPLETE
        self._write_status(
            RunStatus.INCOMPLETE,
            run_id=run_id,
            note=f"missing N4={len(m4)} N3={len(m3)}",
        )
        return RunStatus.INCOMPLETE
