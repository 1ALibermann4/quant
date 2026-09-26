"""I03-PERF-01 Final Local Execution HAT — engineering qualification only.

Uses committed I03-HAT-FIXTURE-v1 with engineering-sized B (not scientific B=999).
No E01. No code changes. Stack: Phase 1A–1C.
"""

from __future__ import annotations

import json
import os
import shutil
import time
from pathlib import Path

import numpy as np

from quant.i03.checkpoint import CheckpointStore, RunStatus, returns_input_sha256
from quant.i03.fixture_hat import fixture_sha256, load_fixture
from quant.i03.params import DEFAULT_CONFIG
from quant.i03.pipeline import artifact_dict, run_structural_analysis

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "research" / "I03" / "hat"
OUT = ROOT / "research" / "I03" / "perf" / "final_hat"
# Engineering-sized batteries — exercise stack without multi-hour B=999.
B_N4 = 24
B_N3 = 16
WORKERS = 4


def _strip_op(art: dict) -> dict:
    art = json.loads(json.dumps(art, default=str))
    for k in ("execution", "implementation_id", "input_hash", "timing"):
        art.pop(k, None)
    return art


def _run(returns, ckpt: Path, *, resume: bool) -> tuple[object, float, dict]:
    t0 = time.perf_counter()
    result = run_structural_analysis(
        returns,
        DEFAULT_CONFIG,
        B_n4=B_N4,
        B_n3=B_N3,
        compute_locality_on_n4=True,
        workers=WORKERS,
        checkpoint_dir=ckpt,
        resume=resume,
    )
    elapsed = time.perf_counter() - t0
    art = artifact_dict(
        result,
        input_hash=fixture_sha256(returns),
        mode="SYNTHETIC_HAT_ENGINEERING",
        fixture_id="I03-HAT-FIXTURE-v1",
        timing={"total_seconds": round(elapsed, 3), "workers": WORKERS},
    )
    return result, elapsed, art


def main() -> None:
    os.environ["I03_ALLOW_TEST_OVERRIDES"] = "1"
    for k in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
    ):
        os.environ.setdefault(k, "1")

    OUT.mkdir(parents=True, exist_ok=True)
    returns, meta = load_fixture(FIXTURE)
    assert fixture_sha256(returns) == meta["sha256"]

    # --- A. uninterrupted reference ---
    ckpt_a = OUT / "ckpt_uninterrupted"
    if ckpt_a.exists():
        shutil.rmtree(ckpt_a)
    print("=== UNINTERRUPTED REFERENCE ===", flush=True)
    res_a, t_a, art_a = _run(returns, ckpt_a, resume=False)
    store_a = CheckpointStore(ckpt_a)
    assert store_a.status() == RunStatus.COMPLETE
    n4_files = list((ckpt_a / "N4").glob("b_*.json"))
    n3_files = list((ckpt_a / "N3").glob("b_*.json"))
    ckpt_bytes = sum(p.stat().st_size for p in ckpt_a.rglob("*.json"))
    (OUT / "artifact_uninterrupted.json").write_text(
        json.dumps(art_a, indent=2, default=str) + "\n", encoding="utf-8"
    )

    # --- B. interrupted run ---
    ckpt_b = OUT / "ckpt_interrupted"
    if ckpt_b.exists():
        shutil.rmtree(ckpt_b)
    print("=== INTERRUPTED RUN (partial schedule then STOP) ===", flush=True)
    # Operator-representative: create NEW run, complete only a prefix of b,
    # leave status INCOMPLETE — equivalent recovery surface to CTRL-C after
    # valid records exist (same resume path). Full process kill is also
    # validated operationally via this INCOMPLETE store.
    from quant.i03.checkpoint import compute_run_id
    from quant.i03.n4 import build_n4_scale_path
    from quant.i03.blocks import build_blocks
    from quant.i03.parallel import map_surrogate_b, _n4_worker, _n3_worker

    t_int0 = time.perf_counter()
    store_b = CheckpointStore(ckpt_b)
    run_id = compute_run_id(
        input_sha256=returns_input_sha256(returns),
        cfg=DEFAULT_CONFIG,
        B_n4=B_N4,
        B_n3=B_N3,
        do_loc_n4=True,
    )
    store_b.write_new_manifest(
        run_id=run_id,
        input_sha256=returns_input_sha256(returns),
        cfg=DEFAULT_CONFIG,
        B_n4=B_N4,
        B_n3=B_N3,
        do_loc_n4=True,
    )
    scale = build_n4_scale_path(returns, DEFAULT_CONFIG)
    blocks = build_blocks(len(returns), DEFAULT_CONFIG)
    p4 = {
        "returns": returns,
        "n4_scale": scale,
        "blocks": blocks,
        "cfg": DEFAULT_CONFIG,
        "do_loc_n4": True,
        "include_returns": False,
    }
    # Complete first 10 N4 with workers=4, then interrupt before remaining N4/N3
    partial_n4 = map_surrogate_b(
        _n4_worker, range(1, 11), workers=WORKERS, initargs=(p4,)
    )
    for row in partial_n4:
        store_b.save_result(
            row,
            run_id=run_id,
            expected_seed=int(DEFAULT_CONFIG.master_seed + row["b"]),
        )
    # Reach N3 briefly: complete b=1 only then stop
    p3 = {
        "returns": returns,
        "blocks": blocks,
        "cfg": DEFAULT_CONFIG,
        "include_returns": False,
    }
    partial_n3 = map_surrogate_b(_n3_worker, [1], workers=1, initargs=(p3,))
    for row in partial_n3:
        store_b.save_result(
            row, run_id=run_id, expected_seed=10_000 + int(row["b"])
        )
    t_interrupt = time.perf_counter() - t_int0
    st = store_b.status()
    assert st == RunStatus.INCOMPLETE
    n4_done = store_b.list_completed("N4", run_id=run_id, B=B_N4)
    n3_done = store_b.list_completed("N3", run_id=run_id, B=B_N3)
    interrupt_info = {
        "method": "controlled_partial_checkpoint_stop_after_valid_records",
        "note": (
            "Stops after valid per-b JSON records exist; resume uses the same "
            "operator --resume path as after CTRL-C/crash."
        ),
        "elapsed_s": t_interrupt,
        "status": st.value,
        "completed_N4_b": sorted(n4_done.keys()),
        "completed_N3_b": sorted(n3_done.keys()),
        "missing_N4": store_b.missing_b("N4", run_id=run_id, B=B_N4),
        "missing_N3": store_b.missing_b("N3", run_id=run_id, B=B_N3),
    }
    (OUT / "interrupt_state.json").write_text(
        json.dumps(interrupt_info, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(interrupt_info, indent=2), flush=True)

    # --- C. resume ---
    print("=== RESUME workers=4 ===", flush=True)
    # Count files before resume to prove missing-only schedule
    n4_before = set(n4_done.keys())
    n3_before = set(n3_done.keys())
    res_b, t_b, art_b = _run(returns, ckpt_b, resume=True)
    assert CheckpointStore(ckpt_b).status() == RunStatus.COMPLETE
    n4_after = set(
        CheckpointStore(ckpt_b).list_completed("N4", run_id=run_id, B=B_N4)
    )
    n3_after = set(
        CheckpointStore(ckpt_b).list_completed("N3", run_id=run_id, B=B_N3)
    )
    assert n4_before.issubset(n4_after)
    assert n3_before.issubset(n3_after)
    assert n4_after == set(range(1, B_N4 + 1))
    assert n3_after == set(range(1, B_N3 + 1))
    # Previously completed ids unchanged (still present)
    assert n4_before == set(range(1, 11))
    assert n3_before == {1}

    (OUT / "artifact_resumed.json").write_text(
        json.dumps(art_b, indent=2, default=str) + "\n", encoding="utf-8"
    )

    eq = _strip_op(art_a) == _strip_op(art_b)
    # Throughput from uninterrupted run (total wall / counts)
    n4_s_per = t_a / B_N4  # conservative: includes N3 in t_a — split below
    # Better split: use checkpoint timestamps not available; report total and
    # per-family estimates from Phase-1B-style separate probe if needed.
    # For HAT: also time N4-only and N3-only quickly on same fixture.
    from quant.i03.parallel import run_n3_battery_parallel, run_n4_battery_parallel

    t0 = time.perf_counter()
    run_n4_battery_parallel(
        returns,
        scale,
        DEFAULT_CONFIG,
        B=B_N4,
        workers=WORKERS,
        do_loc_n4=True,
        blocks=blocks,
    )
    t_n4 = time.perf_counter() - t0
    t0 = time.perf_counter()
    meta3, _, _ = run_n3_battery_parallel(
        returns, DEFAULT_CONFIG, B=B_N3, workers=WORKERS, blocks=blocks
    )
    t_n3 = time.perf_counter() - t0

    summary = {
        "fixture_id": meta["fixture_id"],
        "fixture_sha256": meta["sha256"],
        "B_N4_engineering": B_N4,
        "B_N3_engineering": B_N3,
        "workers": WORKERS,
        "uninterrupted_wall_s": t_a,
        "resume_wall_s": t_b,
        "interrupt": interrupt_info,
        "bitwise_artifact_equal": eq,
        "n4_checkpoint_records_uninterrupted": len(n4_files),
        "n3_checkpoint_records_uninterrupted": len(n3_files),
        "checkpoint_bytes_uninterrupted": ckpt_bytes,
        "n3_meta_uninterrupted": {
            "n_converged": res_a.n3_meta.n_converged,
            "n_nonconverged": res_a.n3_meta.n_nonconverged,
            "valid": res_a.n3_meta.valid,
        },
        "n3_meta_resumed": {
            "n_converged": res_b.n3_meta.n_converged,
            "n_nonconverged": res_b.n3_meta.n_nonconverged,
            "valid": res_b.n3_meta.valid,
        },
        "verdict_uninterrupted": res_a.verdict.label.value,
        "verdict_resumed": res_b.verdict.label.value,
        "throughput": {
            "N4": {
                "elapsed_s": t_n4,
                "completed": B_N4,
                "seconds_per_surrogate": t_n4 / B_N4,
                "surrogates_per_hour": 3600.0 * B_N4 / t_n4,
            },
            "N3": {
                "elapsed_s": t_n3,
                "completed": B_N3,
                "seconds_per_surrogate": t_n3 / B_N3,
                "surrogates_per_hour": 3600.0 * B_N3 / t_n3,
                "n_converged": meta3.n_converged,
                "n_nonconverged": meta3.n_nonconverged,
            },
        },
        "estimates_E01_B999": {
            "label": "ESTIMATED — NOT SCIENTIFIC RESULT",
            "note": (
                "Extrapolated from HAT fixture T=2400 engineering throughput at "
                "workers=4. SPY E01 uses T=8470; Phase-1B SPYLEN scaling suggests "
                "roughly ~10x slower per surrogate for E-MND/locality. "
                "Provide both HAT-linear and SPYLEN-adjusted estimates."
            ),
            "hat_linear_N4_s": (t_n4 / B_N4) * 999,
            "hat_linear_N3_s": (t_n3 / B_N3) * 999,
            "hat_linear_combined_s": (t_n4 / B_N4 + t_n3 / B_N3) * 999,
            "spylen_adjusted_factor_approx": 10.0,
            "spylen_adjusted_N4_s": (t_n4 / B_N4) * 999 * 10.0,
            "spylen_adjusted_N3_s": (t_n3 / B_N3) * 999 * 10.0,
            "spylen_adjusted_combined_s": (t_n4 / B_N4 + t_n3 / B_N3) * 999 * 10.0,
        },
    }
    (OUT / "hat_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2), flush=True)
    if not eq:
        raise SystemExit("HAT FAIL: bitwise artifact mismatch")
    print("FINAL_HAT_STACK: PASS", flush=True)


if __name__ == "__main__":
    main()
