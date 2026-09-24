"""I01-E04 — conditional effect anatomy. Frozen I01. No threshold search."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from quant.exploratory.adapter import DEFAULT_TICKER, acquire_spy, load_latest_cache
from quant.exploratory.status import BANNER, print_banner, stamp
from quant.i01.anatomy import summarize_anatomy
from quant.i01.mechanism import collect_paired_homogeneity
from quant.i01.params import DEFAULT_PARAMS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=f"I01-E04 D_t anatomy. {BANNER}")
    parser.add_argument("--ticker", default=DEFAULT_TICKER)
    parser.add_argument("--cache-dir", type=Path, default=Path("data/exploratory"))
    parser.add_argument("--from-cache", action="store_true", default=True)
    parser.add_argument(
        "--redownload",
        action="store_true",
        help="ignore cache and call yfinance (not the E04 default)",
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
    years = [int(row["year"]) for row in summary["vol"]["yearly"]]
    fig, axes = plt.subplots(2, 1, sharex=True, figsize=(9, 6))
    axes[0].bar(years, [float(row["mean_d"]) for row in summary["vol"]["yearly"]], color="steelblue")
    axes[0].axhline(0.0, color="black", linewidth=0.6)
    axes[0].set_title(f"{BANNER}\nmean D_vol by year")
    axes[1].bar(years, [float(row["mean_d"]) for row in summary["raw"]["yearly"]], color="steelblue")
    axes[1].axhline(0.0, color="black", linewidth=0.6)
    axes[1].set_title("mean D_raw by year")
    fig.tight_layout()
    path = out_dir / "UNQUALIFIED_e04_d_by_year.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    paths.append(str(path))
    return paths


def main(argv: list[str] | None = None) -> int:
    print_banner()
    print("I01-E04 — where/when is D_t large? Prefixed blocks. No threshold search.")
    args = build_parser().parse_args(argv)
    if args.redownload:
        acquisition = acquire_spy(ticker=args.ticker, cache_dir=args.cache_dir)
        print("redownloaded (not the E04 default)")
    else:
        acquisition = load_latest_cache(args.cache_dir, ticker=args.ticker)
        print(
            f"cache {acquisition.acquired_at_utc.isoformat()} "
            f"{len(acquisition.series)} rows "
            f"{acquisition.series.sessions[0]} → {acquisition.series.sessions[-1]}"
        )

    assert DEFAULT_PARAMS.W == 20 and DEFAULT_PARAMS.k == 50 and DEFAULT_PARAMS.h == 10
    paired = collect_paired_homogeneity(acquisition.series, progress=_progress)
    summary = summarize_anatomy(paired)

    payload = {
        **stamp(),
        "experiment": "I01-E04",
        "parent": "I01-E03",
        "parameters_frozen": True,
        "no_threshold_search": True,
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
        "diagnostics": summary,
    }
    figures = _maybe_plot(summary, args.cache_dir)
    payload["figures"] = figures
    out_json = args.cache_dir / "UNQUALIFIED_i01_e04_last_run.json"
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    vol = summary["vol"]
    raw = summary["raw"]
    print_banner()
    print(f"n_eval                 : {summary['n_eval']}")
    print(f"D_vol mean/median/skew : {vol['distribution']['mean']:.6e} / {vol['distribution']['median']:.6e} / {vol['distribution']['skewness']:.3f}")
    print(f"D_vol frac>0           : {vol['distribution']['frac_positive']:.3f}")
    print(f"D_vol top 5% share     : {vol['concentration']['top_05pct_share_of_sum']:.3f}")
    print(f"D_vol max year share   : {vol['concentration']['max_year_share_of_sum']:.3f}")
    print(f"D_raw mean/median      : {raw['distribution']['mean']:.5f} / {raw['distribution']['median']:.5f}")
    print(f"D_raw frac>0           : {raw['distribution']['frac_positive']:.3f}")
    print(f"wrote                  : {out_json}")
    print_banner()
    print("No parameter change. No threshold search. No SCI-PASS. No SCI-FAIL. No trading.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
