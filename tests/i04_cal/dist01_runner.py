from __future__ import annotations

import sys
from pathlib import Path

from quant.i04_cal.distributed import canonical_config, run_shard


def main() -> None:
    shard_path, out_dir, workers, resume = sys.argv[1:]
    result = run_shard(Path(shard_path), Path(out_dir), int(workers),
                       resume=resume == "1", cfg=canonical_config(int(workers)))
    if result["status"] != "COMPLETE":
        raise RuntimeError(f"shard incomplete: {result['status']}")


if __name__ == "__main__":
    main()
