from __future__ import annotations

import json
import sys
from pathlib import Path

from quant.i04_cal.dist02 import run_batch
from quant.i04_cal.params import CalConfig


def main() -> None:
    plan_dir, batch, out_dir, cfg_json = sys.argv[1:5]
    cfg = CalConfig(**json.loads(cfg_json))
    manifest = run_batch(Path(plan_dir), batch, Path(out_dir), workers=cfg.workers, cfg=cfg)
    if manifest["status"] != "COMPLETE":
        raise RuntimeError(f"batch incomplete: {manifest['status']}")


if __name__ == "__main__":
    main()
