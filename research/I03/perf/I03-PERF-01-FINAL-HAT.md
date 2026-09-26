# I03-PERF-01 — Final Local Execution HAT (Pre-E01 RUN2)

> **Status :** CLOSED  
> **Class :** ENGINEERING QUALIFICATION ONLY  
> **Stack :** Phase 1A (kernel) + 1B (ProcessPool) + 1C (checkpoint/resume)  
> **Git HEAD @ HAT :** `bb5d1eeff6d3be80037463626c9d3a0f8d6de9ea`  
> **Evidence dir :** [`final_hat/`](final_hat/)

```text
NO SCIENTIFIC RESULT WAS PRODUCED.
NO E01 · NO E02 · NO PARAMETER CHANGE · NO OPTIMIZATION DURING HAT
NO PARTIAL-RESULT INTERPRETATION
```

**Verdict:** `I03-PERF-FINAL-HAT: PASS`

---

## 1. Environment

| Item | Value |
|------|--------|
| OS | Windows 11 (`10.0.26200`) |
| CPU | Intel Core i5-1035G1 @ 1.00 GHz |
| Physical cores | 4 |
| Logical processors | 8 |
| RAM | ~11.8 GiB (12681240576 B) |
| Python | `C:\Users\Jean Marie\AppData\Local\Programs\Python\Python312\python.exe` 3.12.10 |
| NumPy | 2.5.3 |
| Workers requested | **4** |
| `OMP_NUM_THREADS` | 1 |
| `OPENBLAS_NUM_THREADS` | 1 |
| `MKL_NUM_THREADS` | 1 |

`git status` at freeze: **clean**, branch `master` synced with `origin/master`.

---

## 2. Git baseline

Frozen at Phase-1C tip `bb5d1ee`. No production code modified during this HAT.

---

## 3. Canonical SPY input identity (check only — no E01)

| Kind | SHA-256 | Match |
|------|---------|-------|
| RETURNS FLOAT64 PAYLOAD | `bde9a304…1c02e` | PASS |
| RETURNS.NPY FILE | `4aee1aae…5943e` | PASS |
| MANIFEST GIT TRANSPORT | `9d285f24…bf8f` | PASS |

Loader: `load_canonical_artifact(..., require_authorized_spy=True)`.

---

## 4. HAT fixture identity

| Item | Value |
|------|--------|
| Fixture | `I03-HAT-FIXTURE-v1` (committed, **not regenerated**) |
| Path | `research/I03/hat/` |
| SHA-256 | `sha256:0ed3625a7ed4a19e2fb75e04c8b906a92cc01be54446f61eb53c6cde1cf142dc` |
| T | 2400 |

**Engineering battery sizes** (stack qualification, **not** scientific \(B=999\)):

- `B_N4 = 24`
- `B_N3 = 16`
- `workers = 4`
- checkpoint enabled

Runner: [`_final_hat_run.py`](_final_hat_run.py)

---

## 5. Uninterrupted reference

| Metric | Value |
|--------|--------|
| Wall time | **19.10 s** |
| N4 records | 24 |
| N3 records | 16 |
| N3 converged / non-converged | 0 / 16 |
| Checkpoint size | 43669 bytes |
| Verdict label (engineering) | INCONCLUSIVE |
| Status | COMPLETE |

Artifacts: `final_hat/artifact_uninterrupted.json`, `final_hat/ckpt_uninterrupted/`.

---

## 6. Controlled interruption

| Item | Value |
|------|--------|
| Method | Stop after valid per-`b` JSON records (same resume surface as CTRL-C/crash) |
| Elapsed | 5.55 s |
| Status | **INCOMPLETE** |
| Completed N4 `b` | 1..10 |
| Completed N3 `b` | {1} |
| Missing N4 | 11..24 |
| Missing N3 | 2..16 |

**INCOMPLETE is not a scientific result.**

Evidence: `final_hat/interrupt_state.json`, `final_hat/ckpt_interrupted/` (pre-resume).

---

## 7. Resume

| Item | Value |
|------|--------|
| Command semantics | `resume=True`, same `checkpoint-dir`, `workers=4` |
| Wall time | **12.18 s** |
| Pre-completed `b` retained | N4 1..10, N3 1 |
| Only missing scheduled | YES |
| Final status | COMPLETE |
| Seeds | unchanged (`42+b`, `10000+b`) |
| N3 non-converged | not retried (still 0/16) |

---

## 8. Bitwise comparison

`artifact_uninterrupted` vs `artifact_resumed` (operational fields stripped):

**BITWISE_EQUIVALENT = true**

Includes ordered `b`, seeds, N4/N3 Θ & locality inputs, N3 convergence flags, survival/p-value inputs, validity, verdict fields.

---

## 9–10. Throughput (MEASURED @ workers=4, HAT T=2400)

| Family | elapsed | count | s/surrogate | surrogates/hour |
|--------|---------|-------|-------------|-----------------|
| N4 (+loc) | 10.07 s | 24 | 0.420 | ~8578 |
| N3 | 4.44 s | 16 | 0.277 | ~12984 |

N3 non-convergence on this synthetic fixture: 16/16 (engineering observation only).

---

## 11. Resource observations

- 4 logical workers requested on 4P/8L CPU; BLAS threads pinned to 1 → no intentional oversubscription.
- Checkpoint I/O ~44 KB for full engineering battery — not material vs compute.
- Peak process RSS not instrumented with child attribution; no OOM / thrashing observed.
- Four-worker ProcessPool path exercised (Phase 1B architecture).

---

## 12. Runtime estimates for E01 \(B=999\)

**ESTIMATED — NOT SCIENTIFIC RESULT**

| Basis | N4 | N3 | Combined |
|-------|----|----|----------|
| HAT-linear (\(T=2400\)) | ~419 s (~7 min) | ~277 s (~5 min) | ~696 s (~12 min) |
| SPYLEN-adjusted (~10× from Phase 1B \(T=8470\)) | ~4192 s (~1.2 h) | ~2770 s (~0.8 h) | **~6962 s (~1.9 h)** |

Limitation: HAT fixture length ≠ SPY \(T=8470\). Prefer SPYLEN-adjusted band for planning; still estimate only.

---

## 13. Regressions

```text
py -3.12 -m pytest tests/i03 -q
→ 106 passed
```

Includes Phase 1A/1B/1C equivalence suites. No tests weakened.

---

## 14. Gates H1–H15

| Gate | Result |
|------|--------|
| H1 env/Git recorded | **PASS** |
| H2 canonical input identity | **PASS** |
| H3 workers=4 ProcessPool | **PASS** |
| H4 uninterrupted checkpointed HAT | **PASS** |
| H5 INCOMPLETE after interrupt | **PASS** |
| H6 resume only missing `b` | **PASS** |
| H7 no seed/identity drift | **PASS** |
| H8 uninterrupted vs resumed BITWISE | **PASS** |
| H9 N4 checkpoint semantics | **PASS** |
| H10 N3 checkpoint semantics | **PASS** |
| H11 N3 non-convergence preserved | **PASS** |
| H12 canonical reassembly | **PASS** |
| H13 resources acceptable | **PASS** |
| H14 tests/i03 | **PASS** (106) |
| H15 PERF-01 regressions | **PASS** |

---

## 15. Proposed E01 RUN2 command (authorized later)

**Intended operator form** (after a wire-only CLI change; see blocker below):

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

**Pre-RUN2 blocker (out of scope for this HAT — do not fix here):**  
`--mode hat` already forwards `--workers` / `--checkpoint-dir` / `--resume` into `run_structural_analysis`.  
`--mode e01` currently **accepts** those argparse flags but **does not pass** them into `run_e01` → pipeline defaults (`workers=1`, no checkpoint).  
This HAT qualifies the **pipeline stack** (H1–H15). Authorizing E01 RUN2 requires a separate wire-only change so the command above actually exercises that stack.

---

## Engineering verdict

```text
I03-PERF-FINAL-HAT: PASS
```

Local multi-core execution stack is qualified for an authorized I03-E01 RUN2 attempt with workers=4 + checkpoint/resume. No scientific claim.
