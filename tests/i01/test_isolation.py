"""The mathematical core must not import a vendor adapter."""

from __future__ import annotations

from pathlib import Path

import quant.i01 as i01

CORE_ROOT = Path(i01.__file__).resolve().parent


def test_i01_package_has_no_yfinance_import() -> None:
    for path in CORE_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
                continue
            if "import yfinance" in stripped or "from yfinance" in stripped:
                raise AssertionError(f"{path} imports a vendor library")
            if "quant.exploratory" in stripped and "import" in stripped:
                raise AssertionError(f"{path} imports exploratory adapter")


def test_i01_does_not_import_exploratory() -> None:
    for path in CORE_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                assert "quant.exploratory" not in stripped, f"{path} imports exploratory adapter"
