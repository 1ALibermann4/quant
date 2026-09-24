"""E02 diagnostic summaries — synthetic, frozen parameters."""

from __future__ import annotations

from datetime import date

import numpy as np

from quant.i01.diagnostics import (
    PerTDiagnostics,
    descriptive_raw_association,
    relative_reductions,
    summarize,
    temporal_by_year,
)
from quant.i01.params import DEFAULT_PARAMS
from quant.i01.pipeline import run_geometry


def _per_t() -> PerTDiagnostics:
    sessions = (
        date(2000, 6, 1),
        date(2000, 6, 2),
        date(2000, 6, 5),
        date(2000, 6, 6),
        date(2001, 6, 1),
        date(2001, 6, 4),
        date(2001, 6, 5),
        date(2001, 6, 6),
        date(2002, 6, 3),
        date(2002, 6, 4),
        date(2002, 6, 5),
        date(2002, 6, 6),
    )
    n = len(sessions)
    # Δ_raw tracks Δ_vol; Δ_shape stays near zero.
    raw_geo = (1.0, 1.1, 0.9, 1.2, 1.0, 1.0, 1.0, 1.0, 1.0, 1.05, 0.95, 1.0)
    raw_b0 = (2.0, 2.2, 1.8, 2.4, 1.0, 1.0, 1.0, 1.0, 1.1, 1.15, 1.05, 1.1)
    vol_geo = (0.10, 0.11, 0.09, 0.12, 0.20, 0.20, 0.20, 0.20, 0.20, 0.21, 0.19, 0.20)
    vol_b0 = (0.40, 0.44, 0.36, 0.48, 0.20, 0.20, 0.20, 0.20, 0.22, 0.23, 0.21, 0.22)
    shape_geo = tuple(1.0 for _ in range(n))
    shape_b0 = tuple(1.01 for _ in range(n))
    return PerTDiagnostics(
        ranks=tuple(range(n)),
        sessions=sessions,
        geo_raw=tuple(raw_geo),
        geo_vol=tuple(vol_geo),
        geo_shape=tuple(shape_geo),
        b0_raw=tuple(raw_b0),
        b0_vol=tuple(vol_b0),
        b0_shape=tuple(shape_b0),
        age_median=tuple(float(20 + i) for i in range(n)),
        age_q10=tuple(10.0 for _ in range(n)),
        age_q90=tuple(40.0 for _ in range(n)),
        d_rank1=tuple(1.0 for _ in range(n)),
        d_rank_k=tuple(2.0 for _ in range(n)),
        d_lib_median=tuple(4.0 for _ in range(n)),
        mean_distance_by_rank=(1.0, 1.5, 2.0),
        pooled_age_quantiles={"median": 25.0, "q10": 10.0, "q90": 40.0, "mean": 25.0},
        neighbor_age_share={"gt_252": 0.0, "gt_1260": 0.0, "gt_2520": 0.0},
    )


def test_parameters_still_frozen() -> None:
    assert DEFAULT_PARAMS.W == 20
    assert DEFAULT_PARAMS.k == 50
    assert DEFAULT_PARAMS.h == 10
    assert DEFAULT_PARAMS.B0_R == 200
    assert DEFAULT_PARAMS.B0_seed == 42


def test_relative_reductions_numeric() -> None:
    rel = relative_reductions(
        {"H_raw": 0.0391, "H_vol": 1.55e-4, "H_shape": 1.385},
        {"H_raw": 0.0453, "H_vol": 3.38e-4, "H_shape": 1.388},
    )
    np.testing.assert_allclose(rel["H_raw"], 1.0 - 0.0391 / 0.0453)
    assert rel["H_vol"] > 0.5
    assert rel["H_shape"] < 0.01


def test_temporal_identifies_concentrated_year() -> None:
    rows = temporal_by_year(_per_t())
    by_year = {int(row["year"]): row for row in rows}
    assert float(by_year[2000]["mean_delta_raw"]) > 0.5
    assert float(by_year[2001]["mean_delta_raw"]) == 0.0
    assert float(by_year[2000]["share_of_sum_delta_raw"]) > 0.9


def test_association_links_raw_to_vol_not_shape() -> None:
    assoc = descriptive_raw_association(_per_t())
    assert assoc["corr_raw_vol"] > 0.9
    assert assoc["r_squared"] > 0.9


def test_summarize_has_four_blocks() -> None:
    per_t = _per_t()
    bundle = summarize(
        per_t,
        {"H_raw": 1.0, "H_vol": 0.1, "H_shape": 1.0},
        {"H_raw": 2.0, "H_vol": 0.4, "H_shape": 1.01},
    )
    assert set(bundle) >= {
        "relative_reduction_vs_b0",
        "temporal",
        "neighbor_age",
        "neighborhood_structure",
        "raw_vol_shape",
    }


def test_pipeline_emits_diagnostics(small_series, small_params) -> None:
    result = run_geometry(small_series, small_params)
    assert result.diagnostics is not None
    assert len(result.diagnostics.sessions) == result.n_eval
    assert len(result.diagnostics.mean_distance_by_rank) == small_params.k
    assert result.diagnostics.pooled_age_quantiles["median"] >= small_params.tau + 1
