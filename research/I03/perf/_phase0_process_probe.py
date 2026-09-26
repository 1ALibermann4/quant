"""Phase-0 process-pool scaling probe (non-scientific; HAT fixture only)."""

from __future__ import annotations

import json
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from quant.i03.blocks import build_blocks
from quant.i03.fixture_hat import generate_hat_returns
from quant.i03.n4 import build_n4_scale_path, n4_surrogate_returns
from quant.i03.params import DEFAULT_CONFIG
from quant.i03.pipeline import _emnd_on_returns

_CFG = DEFAULT_CONFIG
_HAT: np.ndarray | None = None
_BLOCKS = None
_SCALE = None


def _init_worker() -> None:
    global _HAT, _BLOCKS, _SCALE
    _HAT = generate_hat_returns()
    _BLOCKS = build_blocks(len(_HAT), _CFG)
    _SCALE = build_n4_scale_path(_HAT, _CFG)


def _one_n4_emnd(b: int) -> tuple[int, float]:
    assert _HAT is not None and _BLOCKS is not None and _SCALE is not None
    rs = n4_surrogate_returns(_HAT, _SCALE, b, _CFG)
    _, _, em = _emnd_on_returns(rs, _BLOCKS, _CFG)
    theta = float(em[0].theta_by_k[10])
    return b, theta


def main() -> None:
    _init_worker()
    assert _HAT is not None
    bs = list(range(1, 9))

    t0 = time.perf_counter()
    serial = [_one_n4_emnd(b) for b in bs]
    t_serial = time.perf_counter() - t0

    scale: dict[str, float] = {"serial": t_serial}
    for n in (1, 2, 4):
        t0 = time.perf_counter()
        with ProcessPoolExecutor(max_workers=n, initializer=_init_worker) as ex:
            out = list(ex.map(_one_n4_emnd, bs))
        scale[f"proc_{n}"] = time.perf_counter() - t0
        # determinism: same theta by b
        assert sorted(out) == sorted(serial)

    payload = {
        "fixture": "I03-HAT",
        "B": 8,
        "unit": "n4_surrogate_gen + emnd",
        "times_s": scale,
        "speedup_vs_serial": {k: t_serial / v for k, v in scale.items() if k != "serial"},
        "cpu_count": __import__("os").cpu_count(),
    }
    outp = Path("research/I03/perf/phase0_process_scaling.json")
    outp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
