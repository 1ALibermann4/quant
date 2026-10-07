# Decision Record: DIST-02 cost-aware Kaggle batch queue

**Status**: Engineering qualification; production dispatch requires separate governance approval
**Scope**: I04-CAL operational execution of the 12 027 remaining canonical cells; frozen synthetic scientific contract unchanged
**Parent**: DR-I04CAL-DIST-01-static-shards (`dist-01 @ 00f9e04`)
**Module**: `src/quant/i04_cal/dist02.py` (`python -m quant.i04_cal.dist02`)

## Decision

The verified `snapshot_local_remaining` of `I04-CAL-CANONICAL-02` (69 durable local
cells, 12 027 remaining) is converted into a deterministic queue of small
cost-balanced batches. Each batch is persisted as a DIST-01 shard manifest
(`shard-NNNNN.json`, schema `I04-CAL-DIST-v1`) extended with DIST-02 fields, so
execution (`run_shard`), crash-resume checkpointing, telemetry and the final
fail-closed `merge` reuse DIST-01 qualified primitives verbatim. A batch never
changes cell content, seeds, gates or expected results — only which cells share
a batch (SAME WORK, DIFFERENT ORDER).

## Cost model (`I04-CAL-COST-v1`)

Scheduling estimate only; no scientific meaning. Family anchors come from
qualified measurements:

| Family | Anchor s/cell | Source |
|---|---|---|
| G0 | 9.0 | Mandate benchmark, Kaggle ~8-9 s |
| G3 | 14.0 | Qualified Windows refs 13.5-14.3 s |
| GORD | 14.6 | Qualified Windows refs 14.2-15.0 s |
| G1 | 104.0 | Kaggle benchmark ~103.7 s/cell @ 2 workers |

Unmeasured families (G2, G4, G5, G7): deterministic conservative fallback
60 s, between G0-class and G1-class per PERF-02. Cost is flat in W for all
families (pair counts are ~constant in W; measured W20 vs W60 anchors are
within noise) except G1, whose soft-DTW distance is O(W^2) per pair:
`cost = anchor * (W/20)^2`. Timings never select, drop or alter a cell.

## Batching strategy (`I04-CAL-PLANNER-v1`)

Longest-processing-time (LPT) greedy placement: remaining cells sorted by
(-estimated_cost, canonical index), each assigned to the least-loaded batch
(lowest index on ties). Batch count = `ceil(total_cost / batch_target_cost_s)`
with `batch_target_cost_s = 1800` (~15-30 min wall at 2 workers), producing far
more batches than notebooks. Fully deterministic: same snapshot + same planner
config + same code -> identical `plan_hash`.

## Invariants

D02-I1 snapshot identity fail-closed · D02-I2 exact partition · D02-I3 no
scientific mutation · D02-I4 deterministic plan · D02-I5 exactly 2 workers ·
D02-I6 durable resume (DIST-01 `run_shard`) · D02-I7 fail-closed identities ·
D02-I8 partial != complete · D02-I9 full CAL complete only at 69 + 12 027 =
12 096 unique cells · D02-I10 no scientific peeking (progress/ids/timings only).

## Plan format

`plan.json`: `schema`, `dist_version`, `run_id` (`<snapshot.run_id>-DIST02`),
`created_at`, `source_code_head` (qualified science `a2680294`),
`distribution_code_head`, `snapshot_hash`, `requested_ids_hash`,
`requested_count`, `batch_count`/`shard_count`, `ordered_batch_ids`,
`batch_manifest_hashes` (SHA-256 pin per batch file), `workers_per_notebook=2`,
`planner` (versioned config), `planner_hash`, `cost_model_version`,
`total_estimated_cost_s`, `plan_hash`, plus the scientific identity fields.
`plan_hash` excludes only `created_at`/`plan_hash`.

`shard-NNNNN.json`: all DIST-01 shard fields (identity, `run_id`, `shard_id`
`batch-NNNNN`, `shard_index`, `cell_ids` canonical order, `requested_ids_hash`,
`source_code_head`) plus `batch_id` `BATCH-NNNN`, `cell_ids_hash`,
`estimated_cost_s`, `planner`, `planner_hash`, `snapshot_hash`,
`distribution_code_head`, `workers_per_notebook`.

## Runner

`run-batch --plan-dir P --batch BATCH-0037 --out-dir OUT` resolves the batch,
verifies plan identity + plan_hash + batch pin + cell_ids_hash, checks code
HEAD when git is available, enforces BLAS env = 1 and exactly 2 workers, then
delegates to DIST-01 `run_shard`. Existing `OUT` -> verified resume; completed
checkpoints are never recomputed. `status` classifies repatriated outputs
COMPLETE / INCOMPLETE / NOT_STARTED / INVALID and lists next available batches.
`export` packs an output dir as `tar.gz`. `validate` recomputes global status
and calls DIST-01 `merge` only at exact completion (with `--local-dir` for the
69 canonical checkpoints). `diagnostics` prints counts/costs distribution.

## Operator procedure

1. Fresh notebook: clone repo, checkout `dist-02`, `pip install -r requirements`, `PYTHONPATH=src`.
2. Copy the plan directory (`plan.json` + `shard-*.json`) onto the notebook.
3. `python -m quant.i04_cal.dist02 run-batch --plan-dir plan --batch BATCH-0000 --out-dir out/BATCH-0000`
4. On notebook death: rerun the same command (resume is automatic and verified).
5. On COMPLETE: `export --out-dir out/BATCH-0000 --dest BATCH-0000.tar.gz`, repatriate, pick the next batch from `status`' `next_available`.

## Limits

Unmeasured families use the 60 s fallback; real stragglers remain possible but
bounded by small batch size. `distribution_code_head` is verified only when a
git checkout is present. No network scheduler: batch assignment is manual via
`status`. Scientific analysis is blocked until the DIST-01 `merge` reports the
exact 12 096-cell universe.
