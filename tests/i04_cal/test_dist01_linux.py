from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.skipif(sys.platform != "win32" or not os.environ.get("DIST01_LINUX_PYTHON"),
                    reason="requires explicit local Linux interpreter for cross-platform qualification")
def test_windows_linux_scientific_identity() -> None:
    root = Path(__file__).resolve().parents[2]
    code = """import sys,json
sys.path.insert(0,'src')
from quant.i04_cal.geometries import iter_geometry_specs
from quant.i04_cal.worker import execute_cal_cell
spec=next(s for s in iter_geometry_specs() if s.geometry_id==sys.argv[1] and s.variant_id==sys.argv[2])
row=execute_cal_cell('S0a',0,int(sys.argv[3]),{'geometry_id':spec.geometry_id,'variant_id':spec.variant_id,'params':spec.params,'status':spec.status.value})
print(json.dumps(row,sort_keys=True,default=str))
"""
    selected = [("G0", "default", "20"), ("G3", "M=2", "20"),
                ("GORD", "D=3,tau=1", "60"), ("G1", "gamma=0.1", "20")]
    env = {**os.environ, "PYTHONPATH": str(root / "src"), "OMP_NUM_THREADS": "1",
           "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1"}
    for spec in selected:
        windows = subprocess.run([sys.executable, "-c", code, *spec], env=env, cwd=root,
                                 capture_output=True, text=True, timeout=600)
        linux = subprocess.run(["wsl", "--exec", os.environ["DIST01_LINUX_PYTHON"], "-c", code, *spec],
                               env=env, cwd=root, capture_output=True, text=True, timeout=600)
        assert windows.returncode == 0, windows.stderr
        assert linux.returncode == 0, linux.stderr
        actual, reference = json.loads(linux.stdout), json.loads(windows.stdout)
        assert actual["status"] == reference["status"] == "OK"
        differing: list[tuple[str, object, object]] = []

        def compare(a: object, b: object, path: str = "") -> None:
            if isinstance(a, dict) and isinstance(b, dict):
                for key in a.keys() | b.keys():
                    compare(a.get(key), b.get(key), f"{path}/{key}")
            elif isinstance(a, list) and isinstance(b, list):
                for i, (left, right) in enumerate(zip(a, b)):
                    compare(left, right, f"{path}/{i}")
                if len(a) != len(b):
                    differing.append((path, len(a), len(b)))
            elif a != b:
                differing.append((path, a, b))

        compare(actual, reference)
        numerical = [abs(a - b) for _, a, b in differing if isinstance(a, (int, float)) and isinstance(b, (int, float))]
        assert not differing, f"Windows/Linux divergence for {spec}: {differing[:5]} max_abs={max(numerical, default=0)}"
