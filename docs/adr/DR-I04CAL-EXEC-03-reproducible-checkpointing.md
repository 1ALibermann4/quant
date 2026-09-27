# Decision Record: I04-CAL EXEC-03 reproducible crash-safe execution

**Status**: ACCEPTED by governance EXEC-03 mandate
**Date**: 2026-09-27
**Scope**: Synthetic I04-CAL execution infrastructure only

## Decision

Use the expanded `iter_geometry_specs` registry as the single source of the cell universe. The frozen full configuration has nine worlds, 32 realizations, three windows and fourteen geometry variants (12,096 cells). Operational worker count does not affect scientific identity.

Replace the old process-randomized `hash(spec.variant_id)` gate RNG derivation with `I04-CAL-SEED-v1`. Serialize `[version, world_seed(world,b), W, geometry_id, variant_id, gate]` as compact ASCII JSON with separators `(',', ':')`, take SHA-256, interpret the first eight digest bytes as a big-endian unsigned integer, then mask to 31 bits. The world RNG and geometry-specific auxiliary seeds remain unchanged. This corrects reproducibility, not an experimental parameter choice. Gate-level subseeds inside `gates.py` are existing deterministic arithmetic transformations and are not changed by this decision. Results produced by the previous hash-randomized implementation are not compatible.

Parent-only persistence uses one checksum-protected JSON checkpoint per successful cell, written to a temporary file, flushed and fsynced, then atomically replaced. The parent appends/fsyncs results.jsonl after that checkpoint and only then updates in-memory completion/progress. On resume it validates the manifest identity (code HEAD, scientific config hash, generator/oracle version, geometry specs, seed contract, expected count), validates checkpoint identity and checksum, and atomically reconstructs results.jsonl from authoritative checkpoints. A torn JSONL tail is recoverable; a corrupt checkpoint fails closed. On Windows, atomic rename and fsync of the file are available, but directory metadata persistence across arbitrary physical power loss is not guaranteed by Python. The strongest practical guarantee is abrupt-process termination durability, not hardware power-loss proof.

Production entry point: `python -m quant.i04_cal --canonical --out-dir <new-dir> --workers 4`; it rejects test overrides. Test workloads use the same `run_calibration` production engine with scoped test configurations. The old `run_cal_monitored.py` belongs to the aborted historical incident, not to the production path. No Full CAL launch is authorized by this record.
