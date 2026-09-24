"""E04 D_t anatomy — prefixed bins, no threshold search."""

from __future__ import annotations

from datetime import date

import numpy as np

from quant.i01.anatomy import (
    CALENDAR_BLOCKS,
    CHRONO_LABELS,
    distribution,
    equal_count_tertiles,
    summarize_anatomy,
    top_share_of_sum,
)
from quant.i01.mechanism import PairedHomogeneity, collect_paired_homogeneity
from quant.i01.params import DEFAULT_PARAMS


def _paired() -> PairedHomogeneity:
    n = 12
    sessions = tuple(date(2000 + i // 4, 6, 1 + (i % 4)) for i in range(n))
    # Right tail of D_vol: nine small negatives, three large positives.
    d_vol = np.array([-1.0] * 9 + [10.0, 12.0, 14.0], dtype=np.float64)
    h_vol_ctrl = np.ones(n)
    h_vol_geo = h_vol_ctrl - d_vol
    d_raw = np.full(n, 0.1)
    return PairedHomogeneity(
        ranks=tuple(range(n)),
        sessions=sessions,
        h_raw_geo=np.ones(n) - d_raw,
        h_vol_geo=h_vol_geo,
        h_raw_ctrl=np.ones(n),
        h_vol_ctrl=h_vol_ctrl,
        rv_w=np.linspace(0.01, 0.12, n),
        x_norm=np.linspace(1.0, 2.0, n),
        window_sum=np.linspace(-0.05, 0.05, n),
    )


def test_parameters_still_frozen() -> None:
    assert DEFAULT_PARAMS.W == 20
    assert DEFAULT_PARAMS.k == 50
    assert DEFAULT_PARAMS.h == 10


def test_prefixed_blocks_are_literals() -> None:
    assert CHRONO_LABELS == ("early", "middle", "late")
    assert CALENDAR_BLOCKS[0] == (1994, 1999, "1994-1999")
    assert CALENDAR_BLOCKS[-1] == (2020, 2026, "2020-2026")


def test_mean_can_exceed_median_when_right_tailed() -> None:
    stats = distribution(_paired().h_vol_ctrl - _paired().h_vol_geo)
    assert stats["mean"] > stats["median"]
    assert stats["frac_positive"] < 0.5
    assert stats["skewness"] > 0.0


def test_top_share_detects_concentration() -> None:
    d = _paired().h_vol_ctrl - _paired().h_vol_geo
    assert top_share_of_sum(d, 0.25) > 0.9


def test_tertiles_are_equal_count_not_a_searched_cut() -> None:
    values = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    labels = equal_count_tertiles(values)
    assert list(labels).count(0) == 2
    assert list(labels).count(1) == 2
    assert list(labels).count(2) == 2


def test_summarize_has_four_views_and_no_sci() -> None:
    bundle = summarize_anatomy(_paired())
    assert set(bundle["vol"]) >= {
        "distribution",
        "concentration",
        "yearly",
        "stability",
        "state_tertiles_descriptive",
    }
    assert "raw" in bundle
    text = str(bundle).lower()
    assert "sci-pass" not in text
    assert "threshold" not in bundle["note"].lower() or "not" in bundle["note"].lower()
    assert "regime classifier" in bundle["note"]


def test_collect_paired_matches_eval_length(small_series, small_params) -> None:
    paired = collect_paired_homogeneity(small_series, small_params)
    assert paired.h_vol_geo.shape[0] == len(paired.sessions)
    assert paired.h_raw_ctrl.shape[0] == len(paired.sessions)
