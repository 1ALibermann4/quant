from __future__ import annotations

import sys
from pathlib import Path

from quant.i04_cal.params import CalConfig
from quant.i04_cal.pipeline import run_calibration


def main() -> None:
    out_dir, workers, resume = sys.argv[1:]
    cfg = CalConfig(B=2, windows=(20, 40), worlds=("S0a", "S0b"), geometries=("G0",), workers=int(workers))
    result = run_calibration(Path(out_dir), cfg, resume=resume == "1")
    if result["status"] != "COMPLETE" or result["n_rows"] != 8:
        raise RuntimeError(f"incomplete: {result['status']} {result['n_rows']}")


if __name__ == "__main__":
    main()
