"""I01-E02 — exploratory diagnostics. Frozen I01 parameters. No SCI verdict."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from quant.exploratory.adapter import DEFAULT_TICKER, acquire_spy, load_latest_cache
from quant.exploratory.status import BANNER, print_banner, stamp
from quant.i01.diagnostics import summarize
from quant.i01.params import DEFAULT_PARAMS
from quant.i01.pipeline import run_geometry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=f"I01-E02 diagnostics. {BANNER}")
    parser.add_argument("--ticker", default=DEFAULT_TICKER)
    parser.add_argument("--cache-dir", type=Path, default=Path("data/exploratory"))
    parser.add_argument(
        "--from-cache",
        action="store_true",
        default=True,
        help="reuse the E01 UNQUALIFIED download (default)",
    )
    parser.add_argument(
        "--redownload",
        action="store_true",
        help="ignore cache and call yfinance (not the E02 default)",
    )
    return parser


def _progress(done: int, total: int) -> None:
    if done == 1 or done == total or done % 500 == 0:
        print(f"  eval {done}/{total}", flush=True)


def _maybe_plot(summary: dict, out_dir: Path) -> list[str]:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return []
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[str] = []
    years = [int(row["year"]) for row in summary["temporal"]["by_year"]]
    fig, axes = plt.subplots(3, 1, sharex=True, figsize=(9, 7))
    for ax, key, title in (
        (axes[0], "mean_delta_raw", "Δ_raw by year"),
        (axes[1], "mean_delta_vol", "Δ_vol by year"),
        (axes[2], "mean_delta_shape", "Δ_shape by year"),
    ):
        ax.bar(years, [float(row[key]) for row in summary["temporal"]["by_year"]], color="steelblue")
        ax.axhline(0.0, color="black", linewidth=0.6)
        ax.set_title(f"{BANNER}\n{title}")
    fig.tight_layout()
    path = out_dir / "UNQUALIFIED_e02_delta_by_year.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    paths.append(str(path))

    ranks = list(range(1, len(summary["neighborhood_structure"]["mean_distance_by_rank"]) + 1))
    fig, ax = plt.subplots()
    ax.plot(ranks, summary["neighborhood_structure"]["mean_distance_by_rank"])
    ax.axhline(
        summary["neighborhood_structure"]["mean_library_median"],
        color="orange",
        linestyle="--",
        label="mean library median distance",
    )
    ax.set_xlabel("neighbor rank")
    ax.set_ylabel("mean L2")
    ax.set_title(f"{BANNER}\nmean L2 by neighbor rank")
    ax.legend()
    path = out_dir / "UNQUALIFIED_e02_distance_by_rank.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    paths.append(str(path))
    return paths


def main(argv: list[str] | None = None) -> int:
    print_banner()
    print("I01-E02 — explain the E01 Δ. Parameters frozen. No SCI verdict.")
    args = build_parser().parse_args(argv)
    if args.redownload:
        acquisition = acquire_spy(ticker=args.ticker, cache_dir=args.cache_dir)
        print("redownloaded (not the E02 default)")
    else:
        acquisition = load_latest_cache(args.cache_dir, ticker=args.ticker)
        print(
            f"cache {acquisition.acquired_at_utc.isoformat()} "
            f"{len(acquisition.series)} rows "
            f"{acquisition.series.sessions[0]} → {acquisition.series.sessions[-1]}"
        )

    result = run_geometry(acquisition.series, progress=_progress)
    assert result.diagnostics is not None
    assert DEFAULT_PARAMS.W == 20 and DEFAULT_PARAMS.k == 50 and DEFAULT_PARAMS.h == 10
    summary = summarize(result.diagnostics, result.mean_geo, result.mean_b0)

    payload = {
        **stamp(),
        "experiment": "I01-E02",
        "parent": "I01-E01",
        "parameters_frozen": True,
        "i01_params": {
            "W": DEFAULT_PARAMS.W,
            "M": DEFAULT_PARAMS.M,
            "h": DEFAULT_PARAMS.h,
            "k": DEFAULT_PARAMS.k,
            "tau": DEFAULT_PARAMS.tau,
            "L_min": DEFAULT_PARAMS.L_min,
            "B0_R": DEFAULT_PARAMS.B0_R,
            "B0_seed": DEFAULT_PARAMS.B0_seed,
        },
        "acquisition": {
            "ticker": acquisition.ticker,
            "source": acquisition.source,
            "yfinance_version": acquisition.yfinance_version,
            "acquired_at_utc": acquisition.acquired_at_utc.isoformat(),
            "request_parameters": acquisition.request_parameters,
            "n_sessions": len(acquisition.series),
        },
        "mean_H_geo": result.mean_geo,
        "mean_H_B0": result.mean_b0,
        "mean_delta_B0_minus_geo": result.mean_delta,
        "diagnostics": summary,
    }
    figures = _maybe_plot(summary, args.cache_dir)
    payload["figures"] = figures
    out_json = args.cache_dir / "UNQUALIFIED_i01_e02_last_run.json"
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    rel = summary["relative_reduction_vs_b0"]
    age = summary["neighbor_age"]
    struct = summary["neighborhood_structure"]
    assoc = summary["raw_vol_shape"]
    temporal = summary["temporal"]
    print_banner()
    print(f"n_eval              : {result.n_eval}")
    print(f"rel drop H_raw/vol/shape : {rel['H_raw']:.4f} / {rel['H_vol']:.4f} / {rel['H_shape']:.4f}")
    print(f"frac years Δ_raw>0  : {temporal['frac_years_mean_raw_positive']:.3f}")
    print(f"max year share Δ_raw: {temporal['max_year_share_of_sum_delta_raw']:.3f}")
    print(f"neighbor age median : {age['pooled_quantiles_session_ranks']['median']:.1f} sessions")
    print(f"age share >10y      : {age['share_of_neighbors']['gt_2520']:.3f}")
    print(f"rank-k / lib median : {struct['mean_rank_k_over_lib_median']:.3f}")
    print(f"corr Δ_raw~Δ_vol    : {assoc['corr_raw_vol']:.3f}")
    print(f"corr Δ_raw~Δ_shape  : {assoc['corr_raw_shape']:.3f}")
    print(f"OLS R² vol+shape    : {assoc['r_squared']:.3f}")
    print(f"wrote               : {out_json}")
    print_banner()
    print("No parameter change. No SCI-PASS. No SCI-FAIL. No trading.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
