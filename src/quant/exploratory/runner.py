"""I01-E01 CLI — exploratory observation only."""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

from quant.exploratory.adapter import DEFAULT_TICKER, acquire_spy
from quant.exploratory.status import BANNER, print_banner, stamp
from quant.i01.params import DEFAULT_PARAMS
from quant.i01.pipeline import GeometryResult, run_geometry


def _distance_summary(distances: tuple[float, ...]) -> dict[str, float]:
    ordered = sorted(distances)
    return {
        "min": ordered[0],
        "median": statistics.median(ordered),
        "max": ordered[-1],
        "mean": statistics.fmean(ordered),
    }


def result_payload(result: GeometryResult, acquisition_meta: dict) -> dict:
    example = result.example
    assert example is not None
    return {
        **stamp(),
        "acquisition": acquisition_meta,
        "i01_params": {
            "W": DEFAULT_PARAMS.W,
            "M": DEFAULT_PARAMS.M,
            "h": DEFAULT_PARAMS.h,
            "k": DEFAULT_PARAMS.k,
            "tau": DEFAULT_PARAMS.tau,
            "L_min": DEFAULT_PARAMS.L_min,
            "epsilon": DEFAULT_PARAMS.epsilon,
            "B0_R": DEFAULT_PARAMS.B0_R,
            "B0_seed": DEFAULT_PARAMS.B0_seed,
        },
        "n_sessions": result.n_sessions,
        "period": {
            "first_session": result.first_session.isoformat(),
            "last_session": result.last_session.isoformat(),
        },
        "n_eval": result.n_eval,
        "eval_period": {
            "first": None if result.eval_first_session is None else result.eval_first_session.isoformat(),
            "last": None if result.eval_last_session is None else result.eval_last_session.isoformat(),
        },
        "example": {
            "t": example.t,
            "session": example.session.isoformat(),
            "X_t": list(example.x_t),
            "neighbors": [
                {
                    "rank": rank,
                    "session": session.isoformat(),
                    "distance": dist,
                }
                for rank, session, dist in zip(
                    example.neighbor_ranks,
                    example.neighbor_sessions,
                    example.distances,
                    strict=True,
                )
            ],
            "distance_distribution": _distance_summary(example.distances),
            "H_geo": example.geo,
            "H_B0": example.b0,
        },
        "mean_H_geo": result.mean_geo,
        "mean_H_B0": result.mean_b0,
        "mean_delta_B0_minus_geo": result.mean_delta,
        "reading": (
            "mean_delta > 0 means geometric neighborhoods were more homogeneous "
            "than B0 on this unqualified run. This is not a SCI verdict."
        ),
    }


def _maybe_plot(result: GeometryResult, out_dir: Path) -> list[str]:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return []
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[str] = []
    if result.example is not None:
        fig, ax = plt.subplots()
        ax.hist(result.example.distances, bins=15, color="steelblue")
        ax.set_title(f"{BANNER}\nexample neighbor distances @ {result.example.session}")
        ax.set_xlabel("L2 distance")
        path = out_dir / "UNQUALIFIED_example_distances.png"
        fig.savefig(path, bbox_inches="tight")
        plt.close(fig)
        paths.append(str(path))
    fig, ax = plt.subplots()
    ax.plot(result.per_t_geo_raw, label="H_raw geo", linewidth=0.8)
    ax.plot(result.per_t_b0_raw, label="H_raw B0", linewidth=0.8, alpha=0.7)
    ax.set_title(f"{BANNER}\nH_raw over T_eval")
    ax.legend()
    path = out_dir / "UNQUALIFIED_h_raw_series.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    paths.append(str(path))
    return paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=f"I01-E01 exploratory runner. {BANNER}",
    )
    parser.add_argument("--ticker", default=DEFAULT_TICKER)
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("data/exploratory"),
        help="UNQUALIFIED cache (gitignored)",
    )
    parser.add_argument("--skip-download", action="store_true", help="reserved; unused")
    return parser


def main(argv: list[str] | None = None) -> int:
    print_banner()
    args = build_parser().parse_args(argv)
    acquisition = acquire_spy(ticker=args.ticker, cache_dir=args.cache_dir)
    print(
        f"acquired {len(acquisition.series)} rows "
        f"{acquisition.series.sessions[0]} → {acquisition.series.sessions[-1]}"
    )
    def _progress(done: int, total: int) -> None:
        if done == 1 or done == total or done % 500 == 0:
            print(f"  eval {done}/{total}", flush=True)

    result = run_geometry(acquisition.series, progress=_progress)
    meta = {
        "ticker": acquisition.ticker,
        "source": acquisition.source,
        "yfinance_version": acquisition.yfinance_version,
        "request_parameters": acquisition.request_parameters,
        "acquired_at_utc": acquisition.acquired_at_utc.isoformat(),
        "price_field_used_by_i01": "Adj Close",
    }
    payload = result_payload(result, meta)
    figures = _maybe_plot(result, args.cache_dir)
    payload["figures"] = figures
    out_json = args.cache_dir / "UNQUALIFIED_i01_e01_last_run.json"
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print_banner()
    print(f"n_sessions     : {result.n_sessions}")
    print(f"period         : {result.first_session} → {result.last_session}")
    print(f"n_eval         : {result.n_eval}")
    if result.example is not None:
        print(f"example t      : {result.example.t} ({result.example.session})")
        print(f"X_t            : {list(result.example.x_t)}")
        print(f"50 neighbors   : {result.example.neighbor_sessions[0]} … {result.example.neighbor_sessions[-1]}")
        print(f"distances      : {_distance_summary(result.example.distances)}")
        print(f"H_geo          : {result.example.geo}")
        print(f"H_B0 (example) : {result.example.b0}")
    print(f"mean H_geo     : {result.mean_geo}")
    print(f"mean H_B0      : {result.mean_b0}")
    print(f"mean Δ (B0-geo): {result.mean_delta}")
    print(f"wrote          : {out_json}")
    print_banner()
    print("No SCI-PASS. No SCI-FAIL. No trading.")
    return 0
