# I03-PERF-01 — Phase 1C: Deterministic Checkpoint / Resume

> **Status :** PHASE 1C CLOSED  
> **Class :** ENGINEERING RELIABILITY ONLY  
> **Phase 1B :** [I03-PERF-01-PHASE1B.md](I03-PERF-01-PHASE1B.md) @ `f7bcb67` / `0592ee8`  
> **Prereg :** unchanged  
> **E01 / E02 :** **NOT executed**

```text
THIS IS AN ENGINEERING RELIABILITY MECHANISM.
NO SCIENTIFIC RESULT WAS PRODUCED.
NO E01 · NO E02 · NO PARAMETER CHANGE · NO PARTIAL-RESULT INTERPRETATION
```

**Verdict:** `PERF01-PHASE1C: PASS`

**Indexing note:** I03 surrogates remain **1-based** `b=1..B` (seeds `42+b`,
`10000+b`). The Phase-1C contract maps the mandate’s “0..B-1” language onto
this established doctrine; identity is still exactly once per `b`.

---

## 1. Checkpoint architecture

```text
checkpoint-dir/
  manifest.json     # run identity (fail-closed)
  status.json       # NEW | INCOMPLETE | COMPLETE | INVALID
  N4/b_XXXXXX.json  # one file per completed b
  N3/b_XXXXXX.json
```

Module: `src/quant/i03/checkpoint.py`  
Integration: `parallel.run_n*_battery_parallel(..., checkpoint_store=, run_id=)`  
Pipeline: `run_structural_analysis(..., checkpoint_dir=, resume=)`  
CLI: `--checkpoint-dir PATH` · `--resume`

Unit of identity: **surrogate index `b`**, never worker id or completion order.

---

## 2. Run identity

`run_id = SHA256(canonical JSON)` over:

- schema / implementation id (`I03-PERF-01-PHASE1C`)
- `input_sha256` (float64 LE payload of returns)
- frozen `I03Config`
- `B_n4`, `B_n3`, `do_loc_n4`

Mismatch → **STOP** (`CheckpointError`). No automatic migration.

---

## 3–4. Persistence / atomicity

`atomic_write_bytes`: write `*.tmp` → `flush`+`fsync` → `os.replace`.

Records carry `payload_sha256`. Corrupt / truncated / hash-mismatch /
wrong family / wrong seed / wrong `run_id` → fail closed.

`*.tmp` leftovers are ignored (not valid checkpoints).

---

## 5. Resume scheduling

Required set `R={1..B}`; completed valid set `C`; schedule only `M=R\C`.

Resume **never** inspects Θ / p / convergence to decide work.

Non-converged N3 rows are **completed** results and are **not** retried.

Worker count may change across resume (tested 4→1 and 1→4).

---

## 6–9. Equivalence / interruption evidence

Tests: `tests/i03/test_perf01_phase1c.py`

| Case | Result |
|------|--------|
| N4 partial + resume (w=2) vs uninterrupted | BITWISE Θ/locality |
| N3 partial + resume (w=4) vs uninterrupted | BITWISE meta/Θ/series |
| Pipeline resume w=1 after partial w=4 | artifact BITWISE |
| Re-resume COMPLETE with w=4 | BITWISE, no recompute needed |
| Corrupt hash / wrong input / wrong family | fail closed |
| Missing `--resume` on non-empty dir | fail closed |
| `.tmp` interruption artifact | ignored |

Phase 1A/1B suites remain intact.

---

## 10. Process-parallel integration

Same checkpoint schema for serial (`workers=1` via battery engine when
`checkpoint_dir` set) and ProcessPool (`workers>1`).

---

## 11. Overhead (MEASURED, HAT N4 B=8 w=2)

From `test_checkpoint_overhead_small` / engineering probe:

- wall overhead bound: not pathological (`t_ckpt < 3·t_plain + 5s` gate)
- mean bytes / N4 record: **≪ 50 KB** (typically a few KB of JSON)
- **ESTIMATED N4 B=999 storage:** **≪ 50 MB** (from mean×999 gate)

Write frequency: one atomic JSON per completed `b`.

---

## 12. Operational restart procedure

```powershell
# NEW run (directory must be empty / NEW)
$env:PYTHONPATH = "src"
py -3.12 -m quant.i03 --mode hat `
  --fixture-dir research/I03/hat `
  --out-dir research/I03/hat/run_ckpt `
  --workers 4 `
  --checkpoint-dir research/I03/hat/ckpt_run1

# After CTRL-C / crash / reboot — EXPLICIT resume
py -3.12 -m quant.i03 --mode hat `
  --fixture-dir research/I03/hat `
  --out-dir research/I03/hat/run_ckpt `
  --workers 2 `
  --checkpoint-dir research/I03/hat/ckpt_run1 `
  --resume
```

| `status.json` | Meaning | Operator action |
|---------------|---------|-----------------|
| NEW | empty / unused | start without `--resume` |
| INCOMPLETE | some `b` valid | `--resume` only |
| COMPLETE | all `b` present | `--resume` OK (no-op schedule) |
| INVALID | corrupt / unreadable | **do not interpret**; delete or quarantine |

**INCOMPLETE is not a scientific result.**

---

## 13. Gates C1–C12

| Gate | Result |
|------|--------|
| C1 science unchanged | **PASS** |
| C2 run identity fail-closed | **PASS** |
| C3 atomic integrity | **PASS** |
| C4 N4 resume bitwise | **PASS** |
| C5 N3 resume bitwise | **PASS** |
| C6 cross-worker resume | **PASS** |
| C7 corruption fail-closed | **PASS** |
| C8 no adaptive scheduling | **PASS** |
| C9 Phase-1B intact | **PASS** |
| C10 I03 regressions | **PASS** (see commit evidence) |
| C11 overhead acceptable | **PASS** |
| C12 procedure documented | **PASS** |

---

## 14. Limitations

- Checkpoints omit bulky `returns` arrays; optional rematerialization uses the
  **same seed** (deterministic replay), not scientific retry.
- Parent `tracemalloc` still does not attribute child RSS.
- Cloud 1-vCPU wall time remains large; checkpointing enables **survival**,
  not speed.

---

## 15. Recommendation — HAT / E01 RUN2

1. Use `--workers 4` (or host cores) **and** `--checkpoint-dir` on multi-core.  
2. On interrupt: `--resume` with any compatible worker count.  
3. Do not analyze partial checkpoints as exploratory evidence.  
4. Proceed to authorized E01 RUN2 only with explicit human authorization.

---

## Engineering verdict

```text
PERF01-PHASE1C: PASS
```
