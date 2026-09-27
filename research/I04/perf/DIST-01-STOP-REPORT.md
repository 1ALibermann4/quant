# DIST-01 — STOP: cross-platform scientific equivalence failed

**Disposition:** STOP — GOVERNANCE DECISION REQUIRED. This is not distributed-execution qualification, not a cloud throughput estimate, and not authorization for paid compute. The running `I04-CAL-CANONICAL-02` directory and process were not modified, stopped or restarted. DIST-01 work was isolated on branch `dist-01` in a separate Git worktree based on `a268029`.

## Architecture implemented but not qualified

`quant.i04_cal.distributed` consumes the existing `pipeline.expected_cell_ids` and full frozen `config_hash`. Static manifests include original run code HEAD, config hash, full-universe SHA-256, geometry-spec SHA-256, seed-contract version, run/shard identities and explicit canonical cell IDs. Groups by geometry variant, W and world distribute realizations across shards via deterministic balanced greedy placement, without scientific values. `snapshot_local_remaining` validates local manifest/preflight/checkpoint hashes and derives `EXPECTED - COMPLETED_LOCAL` on demand; **no live snapshot was taken for cloud dispatch** and no count (such as 44) was hard-coded. The production `plan` CLI requires an attested local-scheduler handoff before accepting a local snapshot; qualification-only plans are capped at 64 cells.

`run_shard` uses the unchanged `worker.execute_cal_cell` scientific callable. Parent-owned fsynced per-cell checkpoint/results persistence is inherited from EXEC-03 helpers; timing lives in separate per-cell sidecars (cell ID, shard, host, PID, start/finish, duration, execution status), not in the scientific payload. Resume validates code/scientific/shard identities and runs only missing IDs. Deterministic merge verifies shard manifests and checkpoint record hashes, rejects missing/unexpected/conflicting cells, and permits identical duplicates only from an explicit reproducibility input. No paid resource, cloud VM, Docker cluster or Full CAL shard was launched.

**Concurrency blocker:** the current local canonical runner continues scheduling the entire universe. A read-only snapshot of completed cells cannot establish disjoint future ownership while it continues. No cooperative scheduling handoff exists in that already-running binary. DIST-01 did not interrupt it. Safe concurrent paid dispatch needs a governance-approved clean handoff after local assignment stops; the current mandate prohibits taking that action ourselves.

## Verification reached before the stop

- Static plan: 12,096 IDs, 32 shards, no overlap, balanced family allocation, deterministic reproduction; PASS.
- Three independent small G0 shards: durable checkpoints, parent timing sidecars, deterministic merge, invalid missing shard, duplicate, conflicting duplicate, wrong config hash and wrong universe hash; PASS.
- Local abrupt parent-tree termination and shard resume: durable checkpoints were preserved, not recomputed; final output matched uninterrupted reference; PASS.
- Full Windows I04 suite: **51 passed, 0 failed in 1024.80 seconds**, including prior 48 tests and three DIST-01 tests. The running canonical local process remained untouched.
- Linux environment: WSL2 Ubuntu 24.04, Python 3.12.3, NumPy 2.5.3 in an independent virtual environment; Windows reference Python 3.12.10, NumPy 2.5.3. No Linux cloud VM was provisioned.

**Mandatory Windows ↔ Linux equivalence: FAIL.** Fresh interpreters ran the same frozen `S0a`, realization 0, W=20, `G0:default` cell through `worker.execute_cal_cell`. Both returned `OK` with the same identity and seeds, but the full scientific result payloads differed in CAL-G4:

- `c=0.05`, Linux `0.991232143594706`, Windows `0.9915330693840462`;
- `c=0.1`, Linux `0.9829072184819573`, Windows `0.9826937185183436`;
- `c=0.2`, Linux `0.9221891466098645`, Windows `0.9226002151717736`.

Maximum observed absolute difference: **0.00041106856190908925**. All other compared fields of this first cell were equal. No root cause was established; numerical-library/platform behavior is a hypothesis, not a conclusion. The cross-platform test stopped at its first failing cell, so G1/G2/G3/G5/G7/GORD and other W were **not** cross-platform qualified. The test uses exact output equality because no frozen cross-platform numerical tolerance authorizes accepting these deviations; no post-hoc tolerance was introduced. The Linux comparison failed in 65.42 seconds. This directly triggers the mandate's STOP condition.

## Not claimed

There was no representative all-family completed timing benchmark, no 8/16/32-worker cloud scaling measurement, no Linux cloud crash HAT, no measured cloud price/throughput and no qualified Windows+Linux merge. The pinned Linux runtime requirement is `numpy==2.5.3`; environment installation succeeded in WSL only. ECONOMY, BALANCED and FAST machine counts, completion times and euro costs cannot be calculated from measured cloud throughput because no paid cloud microbenchmark was authorized or run. Assigning numbers now would be speculative; no <6h or 1–3h claim is supported. The initial local `44+` cells were not discarded, copied or dispatched.

## Next governance decision

Decide whether to authorize a separate investigation of the CAL-G4 cross-platform difference (without changing frozen scientific semantics or inventing a threshold), whether Linux may be used only if exact outputs can be recovered, and how/when to grant an explicit clean handoff from the still-running local scheduler. Only then can a paid single-machine microbenchmark measure throughput and cost to choose ECONOMY/BALANCED/FAST. Scientific contract, seed map, cell universe, worlds, gates, W and hyperparameters were unchanged on the qualified local branch.
