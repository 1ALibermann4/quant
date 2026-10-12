"""Build quant-I04-CAL-runner portable ZIP (engineering packaging only)."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist" / "quant-I04-CAL-runner"
ZIP_PATH = ROOT / "dist" / "quant-I04-CAL-runner.zip"

# Scientific + runtime modules required offline
COPY_TREES = [
    ("src/quant/__init__.py", "src/quant/__init__.py"),
    ("src/quant/__version__.py", "src/quant/__version__.py"),
    ("src/quant/i04_cal", "src/quant/i04_cal"),
]

REQUIREMENTS = """\
numpy>=1.26,<3
pydantic>=2.0
numba>=0.59,<0.62
"""

README = """\
quant-I04-CAL-runner — portable One-Command (Windows)
====================================================

SYNTHETIC CALIBRATION ONLY — NO MARKET DATA — NO GEOMETRY WINNER

What this does
--------------
Runs I04-CAL cells on this machine with checkpoints, optional 16h stop,
and a disjoint cell allowlist (ASUS vs OPTIPLEX).

Requirements
------------
- Windows 10/11
- Python 3.11 or 3.12 on PATH (`py -3.12` or `python`)
- ~4+ GB free disk; prefer plugged-in power

First launch (one command)
--------------------------
1. Unzip this folder anywhere (example: Desktop\\quant-I04-CAL-runner).
2. Double-click START_WINDOWS.cmd  OR  run it from cmd.
3. Confirm dependency install when asked (user-local venv only).
4. Leave the machine running. Results land in results\\ and checkpoints\\.

Default: 16h max runtime, 20 min shutdown margin, workers=auto.

Recover results
---------------
Copy the whole folder (or results\\ + checkpoints\\ + logs\\ + reports\\)
back to the main PC. On the ASUS repo:

  py -3.12 -m quant.i04_cal.consolidate --out-dir research/I04/calibration/MERGED \\
    --source <path-to-optiplex-results> --source <path-to-asus-results> \\
    --source research/I04/calibration/I04-CAL-CANONICAL-02

Do not edit JSON checkpoints by hand.
"""

START_CMD = r"""@echo off
setlocal
cd /d "%~dp0"
echo === quant I04-CAL portable runner ===
echo SYNTHETIC ONLY — NO MARKET DATA — NO GEOMETRY WINNER
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0bootstrap.ps1" %*
set ERR=%ERRORLEVEL%
if %ERR% NEQ 0 (
  echo.
  echo Runner exited with code %ERR%. See logs\
  pause
)
endlocal
exit /b %ERR%
"""

BOOTSTRAP_PS1 = r"""
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Find-Python {
  foreach ($c in @("py -3.12", "py -3.11", "python", "python3")) {
    try {
      $parts = $c -split " "
      & $parts[0] $parts[1..($parts.Length-1)] -c "import sys; assert sys.version_info[:2]>=(3,11); print(sys.executable)" 2>$null
      if ($LASTEXITCODE -eq 0) { return $c }
    } catch {}
  }
  return $null
}

$py = Find-Python
if (-not $py) {
  Write-Host "ERROR: Python 3.11+ not found. Install from python.org (user install) then retry."
  exit 1
}
Write-Host "Using launcher: $py"

$venv = Join-Path $PSScriptRoot ".venv"
if (-not (Test-Path $venv)) {
  Write-Host "Will create isolated venv at $venv and install:"
  Get-Content (Join-Path $PSScriptRoot "requirements.lock")
  $ans = Read-Host "Proceed with user-local install? [Y/N]"
  if ($ans -notin @("Y","y")) { exit 2 }
  $parts = $py -split " "
  & $parts[0] $parts[1..($parts.Length-1)] -m venv $venv
}

$venvPy = Join-Path $venv "Scripts\python.exe"
& $venvPy -m pip install --upgrade pip
& $venvPy -m pip install -r (Join-Path $PSScriptRoot "requirements.lock")

$env:PYTHONPATH = (Join-Path $PSScriptRoot "src")
$env:OMP_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
# Never carry test overrides into canonical portable runs
Remove-Item Env:I04_CAL_ALLOW_TEST_OVERRIDES -ErrorAction SilentlyContinue
if (Test-Path (Join-Path $PSScriptRoot "CODE_COMMIT.txt")) {
  $env:QUANT_I04_CAL_GIT_COMMIT = (Get-Content (Join-Path $PSScriptRoot "CODE_COMMIT.txt") -TotalCount 1).Trim()
}

# Hardware snapshot
$hw = Join-Path $PSScriptRoot "reports\hardware.json"
New-Item -ItemType Directory -Force -Path (Join-Path $PSScriptRoot "reports") | Out-Null
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1 Name, NumberOfCores, NumberOfLogicalProcessors
$gpu = Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion
$ram = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)
@{ cpu = $cpu; gpu = $gpu; ram_gb = $ram; python = (& $venvPy -c "import sys; print(sys.version)") } |
  ConvertTo-Json -Depth 5 | Set-Content -Encoding utf8 $hw

# Workers: leave one logical CPU free
$logical = [int]$cpu.NumberOfLogicalProcessors
if ($logical -lt 1) { $logical = 2 }
$workers = [Math]::Max(1, $logical - 1)

$machine = $env:I04_CAL_MACHINE
if (-not $machine) { $machine = "OPTIPLEX" }
$allow = Join-Path $PSScriptRoot "config\allowlist_$machine.txt"
if (-not (Test-Path $allow)) {
  Write-Host "Missing $allow — set I04_CAL_MACHINE=ASUS or OPTIPLEX, or place allowlist."
  exit 3
}

$out = Join-Path $PSScriptRoot "results\$machine"
New-Item -ItemType Directory -Force -Path $out, (Join-Path $PSScriptRoot "logs"), (Join-Path $PSScriptRoot "checkpoints") | Out-Null

$maxH = 16
if ($env:MAX_RUNTIME_HOURS) { $maxH = [double]$env:MAX_RUNTIME_HOURS }
$margin = 20
if ($env:SHUTDOWN_MARGIN_MINUTES) { $margin = [double]$env:SHUTDOWN_MARGIN_MINUTES }

$resume = @()
if (Test-Path (Join-Path $out "manifest.json")) { $resume = @("--resume") }

Write-Host "Starting I04-CAL machine=$machine workers=$workers max_hours=$maxH margin_min=$margin"
$log = Join-Path $PSScriptRoot ("logs\run_{0:yyyyMMdd_HHmmss}.log" -f (Get-Date))
$argList = @(
  "-m", "quant.i04_cal",
  "--canonical",
  "--out-dir", $out,
  "--workers", "$workers",
  "--cell-list", $allow,
  "--max-runtime-hours", "$maxH",
  "--shutdown-margin-minutes", "$margin"
) + $resume
& $venvPy @argList 2>&1 | Tee-Object -FilePath $log
exit $LASTEXITCODE
"""


def _git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def _copy() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for src_rel, dst_rel in COPY_TREES:
        src = ROOT / src_rel
        dst = DIST / dst_rel
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    # Ensure package importable
    (DIST / "src" / "quant" / "i04_cal").mkdir(parents=True, exist_ok=True)
    for name in ("results", "checkpoints", "logs", "reports", "config", "tests"):
        (DIST / name).mkdir(exist_ok=True)
    (DIST / "requirements.lock").write_text(REQUIREMENTS, encoding="utf-8")
    (DIST / "README.txt").write_text(README, encoding="utf-8")
    (DIST / "START_WINDOWS.cmd").write_text(START_CMD, encoding="utf-8")
    (DIST / "bootstrap.ps1").write_text(BOOTSTRAP_PS1.lstrip("\n"), encoding="utf-8")
    head = _git_head()
    (DIST / "CODE_COMMIT.txt").write_text(head + "\n", encoding="utf-8")
    # Placeholder allowlists — replaced by pack after split
    (DIST / "config" / "allowlist_ASUS.txt").write_text("# fill via bimachine split\n", encoding="utf-8")
    (DIST / "config" / "allowlist_OPTIPLEX.txt").write_text("# fill via bimachine split\n", encoding="utf-8")
    manifest = {
        "name": "quant-I04-CAL-runner",
        "kind": "engineering_portable_runner",
        "code_commit": head,
        "spec_id": "I04-CAL-SPEC-v0.2",
        "note": "Not a scientific identifier. Packaging only.",
    }
    (DIST / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _zip() -> str:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    shutil.make_archive(str(ZIP_PATH.with_suffix("")), "zip", DIST.parent, DIST.name)
    h = hashlib.sha256(ZIP_PATH.read_bytes()).hexdigest()
    (ZIP_PATH.with_suffix(".zip.sha256")).write_text(
        f"{h}  {ZIP_PATH.name}\n", encoding="utf-8"
    )
    return h


def main() -> int:
    print("Packing", DIST)
    _copy()
    # Generate split excluding CANONICAL-02 if present
    completed = ROOT / "research/I04/calibration/I04-CAL-CANONICAL-02"
    sys.path.insert(0, str(ROOT / "src"))
    from quant.i04_cal.bimachine import write_split

    split_dir = DIST / "config"
    man = write_split(
        split_dir,
        completed_run=completed if completed.is_dir() else None,
        capacity_a=1.0,
        capacity_b=1.0,
    )
    # write_split names allowlist_ASUS.txt already in config/
    print("split", json.dumps({k: man[k] for k in ("remaining", "n_a", "n_b", "config_hash")}, indent=2))
    digest = _zip()
    print("ZIP", ZIP_PATH, "sha256", digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
