# I04-CAL HP-OPT — Qualification Report (L9)

## Environments

| Env | Result |
|-----|--------|
| ASUS Windows 11 / Python 3.12.10 / numpy 2.x / numba 0.61.2 | QUALIFIED for engineering |
| Portable ZIP smoke (copy of pack, no venv bootstrap in CI sense) | PASS (1 G1 cell) |
| OptiPlex | **NOT QUALIFIED** until first-boot self-check |

## Tests executed

| ID | Test | Result |
|----|------|--------|
| T1 | Soft-DTW Numba ≡ ref (W∈{20,40,60}, γ∈{0.1,1,10}) | PASS |
| T2 | Soft-DTW speedup ≥5× microbench | PASS (~30×) |
| T3 | Bi-machine disjoint + coverage 12096 | PASS |
| T4 | Exclude 69 completed → 12027 remaining | PASS |
| T5 | max_runtime stops before cells | PASS |
| T6 | Pack ZIP + import + 1 canonical cell | PASS (9.2s) |
| T7 | Resume without recompute | PASS (0.008s) |
| T8 | Time-stop flag | PASS |
| T9 | Consolidate smoke+CANONICAL-02 | PASS (70 accepted, 0 conflict) |
| T10 | config_hash identity | PASS `70e996a1…` |

## Limitations

- Full G2/G5 cell timings deferred under host CPU contention (other jobs).
- Bootstrap `.venv` install path exercised by script presence; full offline cold-machine install should be re-run on OptiPlex.
- CANONICAL-02 must **not** be resumed under a different `git_commit`; new work uses new `out-dir` + consolidate.

## Scientific invariants

Unchanged: SPEC-v0.2, seeds, worlds, geometries, gates, universe, PASS criteria.
