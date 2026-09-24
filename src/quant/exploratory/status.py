"""Visible status for every exploratory artefact."""

from __future__ import annotations

BANNER = "EXPLORATORY / UNQUALIFIED / NOT SCIENTIFICALLY PROMOTABLE"
DATA_CLASS = "EXPLORATORY"
QUALIFICATION = "UNQUALIFIED"
PROMOTABLE = False


def stamp() -> dict[str, object]:
    """Return the mandatory exploratory labels."""

    return {
        "data_class": DATA_CLASS,
        "qualification": QUALIFICATION,
        "scientifically_promotable": PROMOTABLE,
        "banner": BANNER,
        "sci_verdict": None,
        "note": (
            "Exploratory observation only. Not DATA-PASS, not SCI-PASS, "
            "not SCI-FAIL, not PRED, not ECON."
        ),
    }


def print_banner(file=None) -> None:
    """Write the banner to stdout (or ``file``)."""

    line = "=" * len(BANNER)
    print(line, file=file)
    print(BANNER, file=file)
    print(line, file=file)
