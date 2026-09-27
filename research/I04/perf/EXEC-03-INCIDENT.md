# EXEC-03 incident: aborted noncanonical executions

Snapshot 2026-09-27 09:56:33 +02:00, before termination. No scientific results inspected. Source: psutil process metadata, git status, existing manifests, results and telemetry.

HEAD: `493337dc491f37ee6e00f54c7c10d1335cacccef`. Git tree dirty (untracked execution artifacts, `run_cal_monitored.py`, test directories, prior reports). Both manifests have `git_dirty: true`, scientific config hash `0554179cb46995d9adc0e60a689e0c8505e09351856412124eed8d8912feefd0`, B=32, windows=20/40/60, worlds=S0a/S0b/S1/S2/S3/S4/S5/S6/S7, geometries=G0/G1/G2/G3/G4/G5/G7/GORD, core strides=8/4, workers=4. Actual expanded universe: 14 specs, 12,096 cells. Both results.jsonl files contained 0 bytes at inspection; canonical_run/ckpt was empty. Monitor snapshot at 09:56:19 showed 0/6912 (incorrect denominator), status INCOMPLETE, elapsed 970.19 seconds. `cal_execution.log` and `full_cal_execution.log` were empty at inspection.

Authorized replacement tree:
- PID 13372 parent, start 09:40:09.088636 +02:00, CPU user 1.015625s system 1.296875s, RSS 71,573,504 bytes, status running; command `python run_cal_monitored.py`.
- PID 8472 child, start 09:40:09.912754, CPU user 829.9375s system 7.125s, RSS 266,067,968 bytes, running.
- PID 8552 child, start 09:40:09.897021, CPU user 860.53125s system 4.765625s, RSS 64,118,784 bytes, running.
- PID 17764 child, start 09:40:09.882089, CPU user 833.03125s system 4.984375s, RSS 67,706,880 bytes, running.
- PID 31276 child, start 09:40:09.929378, CPU user 865.09375s system 4.890625s, RSS 258,662,400 bytes, running.

Authorized `test_full` tree:
- PID 26920 parent, start 09:45:09.437816 +02:00, CPU user 0.59375s system 0.375s, RSS 40,091,648 bytes, running; `python -c` test-only `max_cells=5` in `test_full`.
- PID 11684 child, start 09:45:11.137737, CPU user 242.453125s system 1.09375s, RSS 49,901,568 bytes, running.
- PID 17156 child, start 09:45:11.112933, CPU user 240.421875s system 1.109375s, RSS 50,003,968 bytes, running.
- PID 24896 child, start 09:45:11.057241, CPU user 601.859375s system 3.28125s, RSS 54,571,008 bytes, running.
- PID 27664 child, start 09:45:11.085923, CPU user 233.21875s system 1.75s, RSS 50,069,504 bytes, running.

Prior original run: same HEAD reported, original parent 18372 and workers 12096/14224/15572/17616. It was forcibly stopped without deadlock evidence; original canonical_run directory was deleted and recreated. Last original result observation: 0 bytes; checkpoint empty. Exact termination time and any in-memory completed cells UNKNOWN. Original run1 is historical, noncanonical and unrelated.

At 2026-09-27 09:57:11.831127 +02:00, psutil verified both parent creation times and exact child sets. Only PIDs 17764, 8552, 8472, 31276, 24896, 27664, 17156, 11684, 13372 and 26920 were terminated with `Process.terminate()`, between 09:57:11.832592 and 09:57:11.835610 +02:00. All exited within the 10-second wait; none needed escalation. Per-process exit status was mostly unavailable (`None`); PID 31276 reported 15.

The replacement and test_full artifacts are preserved as ABORTED_NONCANONICAL; do not reuse for scientific assessment. The old parallel pipeline buffers all results until executor exit and does not write per-cell checkpoints. The earlier PASS qualification was overstated.
