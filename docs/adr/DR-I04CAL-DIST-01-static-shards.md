# Decision Record: DIST-01 static CPU shards

**Status**: Proposed engineering qualification; dispatch requires separate governance approval
**Scope**: I04-CAL operational execution; frozen synthetic scientific contract unchanged

## Decision

The 12,096 IDs from `pipeline.expected_cell_ids` remain the sole authoritative scientific universe. Define a requested subset by mechanically subtracting validated durable local checkpoint IDs. Validate the original local manifest and preflight universe/spec hashes before producing a read-only snapshot; never use a hard-coded progress count. Do not snapshot for actual dispatch until immediately before an authorized ownership handoff.

Partition selected IDs deterministically by geometry variant, W and world with balanced greedy placement; distribute all realizations within each group across shards. No scientific result or oracle content is used. Each shard manifest records the full scientific identity, requested-set hash, seed contract, original source HEAD, ordered canonical cell IDs, shard identity and creation time. Operational worker count does not enter scientific identity.

The independent shard runner reuses `worker.execute_cal_cell` and EXEC-03 checkpoint serialization/checksums. It writes timing/host/PID/status in a sidecar record before its cell checkpoint; the scientific result row is unchanged. Only the parent writes results and checkpoint files. Failed shards retain completed cells, and resume schedules only missing IDs after code, seed, config, universe and shard identity checks. The merge validates local and shard checkpoints and their record hashes, expected IDs, configuration and universe identity; it rejects missing or conflicting cells. Identical duplicates are accepted only in an explicitly supplied reproducibility input.

## Local ownership constraint

`I04-CAL-CANONICAL-02` was launched with an unmodified EXEC-03 runner that keeps scheduling future cells. It cannot relinquish a subset while continuing without a cooperative scheduler change. Merely snapshotting its completed IDs does not prove that cloud shards and local future cells are disjoint. Accordingly, the production `plan` CLI requires a separately approved attestation that local scheduling has quiesced, followed by a new read-only snapshot. DIST-01 must not stop, modify or migrate that running process itself. Qualification-only lists of up to 64 cells remain available for independent tests and benchmarks; these are not canonical dispatch manifests. No paid compute or full shard is authorized by this record.

## Limits

Static sharding avoids a broker or distributed database. Operational durations are measured per cell, but no scientific outcome may influence placement. Python 3.12 and NumPy 2.5.3 are pinned for Linux qualification. Windows ↔ Linux equivalence must pass before any distributed canonical merge; exact equality is the default until a governed numerical equivalence policy is established. Cloud pricing and throughput require an authorized paid single-machine microbenchmark; extrapolations from local cores alone do not authorize a budget. Physical hardware power-loss durability retains the EXEC-03 limitation.
