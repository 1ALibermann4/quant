# I03-E01 RUN2 — CLI Wiring Closure

> **Status :** CLOSED  
> **Class :** OPERATIONAL PREREQUISITE ONLY  
> **Depends on :** I03-PERF-FINAL-HAT PASS (`38ce793`)

```text
NO SCIENTIFIC RESULT WAS PRODUCED.
NO E01 · NO E02 · NO PARAMETER CHANGE · NO ENGINE OPTIMIZATION
```

**Verdict:** `I03-E01-RUN2-CLI-WIRING: PASS`

---

## 1. Discovered blocker

Final HAT (`research/I03/perf/I03-PERF-01-FINAL-HAT.md`) qualified the pipeline stack
(`workers=4`, ProcessPool, checkpoint/resume, bitwise resume).

CLI argparse already exposed:

- `--workers`
- `--checkpoint-dir`
- `--resume`

for `--mode e01`, but `runtime.main` did **not** forward them into `run_e01`,
and `run_e01` always called `run_structural_analysis(returns, cfg)` with defaults
(`workers=1`, no checkpoint).

The proposed RUN2 command would therefore silently execute the serial /
non-checkpoint path.

---

## 2. Root cause

Integration gap only:

| Layer | Status before |
|-------|----------------|
| `argparse` flags | present |
| `--mode hat` forwarding | wired (Phase 1C) |
| `--mode e01` → `run_e01(...)` | **missing kwargs** |
| `run_e01` → `run_structural_analysis(...)` | **missing kwargs** |

No defect in Phase 1A/1B/1C engine.

---

## 3. Files changed

**Production (wiring only):**

- `src/quant/i03/runtime.py` — forward `workers` / `checkpoint_dir` / `resume` to `run_e01`; reject `workers < 1` without `or 1` coercion
- `src/quant/i03/e01.py` — accept operational kwargs; pass through to pipeline; catch `CheckpointError` fail-closed; record operational timing/operator fields

**Tests:**

- `tests/i03/test_e01_cli_wiring.py` — forwarding, defaults, fail-closed, bounded CLI smoke

**Docs:**

- this file

---

## 4. Exact wiring change

```text
CLI --mode e01 --workers N --checkpoint-dir PATH [--resume]
  → runtime.main validates workers>=1; resume requires checkpoint-dir
  → run_e01(..., workers=N, checkpoint_dir=PATH, resume=...)
  → run_structural_analysis(..., workers=N, checkpoint_dir=PATH, resume=...)
```

Defaults when flags omitted: `workers=1`, `checkpoint_dir=None`, `resume=False`
(historical serial path preserved).

---

## 5. CLI tests

`tests/i03/test_e01_cli_wiring.py` (8 tests):

| Test | Covers |
|------|--------|
| `test_cli_e01_forwards_workers` | A — workers=4 reaches pipeline |
| `test_cli_e01_forwards_checkpoint_dir` | B — checkpoint path enabled |
| `test_cli_e01_forwards_resume` | C — resume=True forwarded |
| `test_cli_e01_defaults_preserve_serial_no_checkpoint` | D — defaults |
| `test_cli_e01_resume_without_checkpoint_dir_fails` | E — invalid combo |
| `test_cli_e01_workers_invalid_fails` | E — workers=0 |
| `test_cli_e01_resume_empty_checkpoint_fail_closed` | E / Phase-1C fail-closed |
| `test_bounded_cli_smoke_parallel_checkpoint_resume` | smoke W6–W8 |

Result: **8 passed**

---

## 6. Bounded CLI smoke

Via `quant.i03.runtime.main` (same entry as `python -m quant.i03`):

- synthetic engineering returns (not SPY)
- engineering B via test-only override reinjected inside spy (production path still clears `I03_ALLOW_TEST_OVERRIDES`)
- `--workers 2 --checkpoint-dir ...` → COMPLETE, `workers_used=2`
- controlled INCOMPLETE (delete trailing `b` records)
- `--resume` → COMPLETE again, only missing `b` scheduled

Confirms CLI no longer falls back to serial / non-checkpoint when flags are set.

---

## 7. Regressions

```text
py -3.12 -m pytest tests/i03 -q
→ 114 passed in 147.57s
```

Includes Phase 1A/1B/1C equivalence suites + new CLI wiring tests (8).
No tests weakened.

---

## 8. Gates W1–W10

| Gate | Result |
|------|--------|
| W1 E01 workers forwarding | **PASS** |
| W2 E01 checkpoint-dir forwarding | **PASS** |
| W3 E01 resume forwarding | **PASS** |
| W4 defaults/backward compatibility | **PASS** |
| W5 checkpoint fail-closed preserved | **PASS** |
| W6 CLI smoke reaches parallel path | **PASS** |
| W7 CLI smoke reaches checkpoint path | **PASS** |
| W8 CLI resume completes | **PASS** |
| W9 regressions | **PASS** (see §7) |
| W10 no scientific/engine change | **PASS** (wiring only) |

---

## 9. Final proposed RUN2 command

```powershell
$env:PYTHONPATH = "src"
$env:OMP_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"

py -3.12 -m quant.i03 --mode e01 `
  --canonical-dir data/exploratory/canonical_i03_spy_v1 `
  --out-dir research/I03/e01/run2 `
  --workers 4 `
  --checkpoint-dir research/I03/e01/run2_ckpt

# If interrupted:
py -3.12 -m quant.i03 --mode e01 `
  --canonical-dir data/exploratory/canonical_i03_spy_v1 `
  --out-dir research/I03/e01/run2 `
  --workers 4 `
  --checkpoint-dir research/I03/e01/run2_ckpt `
  --resume
```

**Not executed in this task.** Authorization for real E01 RUN2 is separate.

---

## Engineering verdict

```text
I03-E01-RUN2-CLI-WIRING: PASS
```
