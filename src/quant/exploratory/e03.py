"""I01-E03 — exploratory volatility-mechanism diagnostic. Frozen I01. No SCI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from quant.exploratory.adapter import DEFAULT_TICKER, acquire_spy, load_latest_cache
from quant.exploratory.status import BANNER, print_banner, stamp
from quant.i01.mechanism import run_vol_mechanism, summarize_mechanism
from quant.i01.params import DEFAULT_PARAMS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=f"I01-E03 vol mechanism. {BANNER}")
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
        help="ignore cache and call yfinance (not the E03 default)",
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
    years = [int(row["year"]) for row in summary["yearly_h_vol"]]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(years, [float(row["mean_h_vol_geo"]) for row in summary["yearly_h_vol"]], label="L2")
    ax.plot(
        years,
        [float(row["mean_h_vol_volctrl"]) for row in summary["yearly_h_vol"]],
        label="past-vol control",
    )
    ax.plot(years, [float(row["mean_h_vol_b0"]) for row in summary["yearly_h_vol"]], label="B0")
    ax.set_title(f"{BANNER}\nmean H_vol by year")
    ax.legend()
    path = out_dir / "UNQUALIFIED_e03_h_vol_by_year.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    paths.append(str(path))

    prox = summary["past_vol_proximity"]
    fig, ax = plt.subplots()
    ax.bar(
        ["L2 neighbors", "vol control", "library typical"],
        [
            prox["mean_abs_drv_geo_neighbors"],
            prox["mean_abs_drv_volctrl_neighbors"],
            prox["mean_median_abs_drv_library"],
        ],
        color=["steelblue", "darkorange", "0.6"],
    )
    ax.set_ylabel("mean |Δ rv_W|")
    ax.set_title(f"{BANNER}\npast-vol proximity")
    path = out_dir / "UNQUALIFIED_e03_past_vol_proximity.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    paths.append(str(path))
    return paths


def main(argv: list[str] | None = None) -> int:
    print_banner()
    print("I01-E03 — does L2 add structure beyond past-vol persistence? Parameters frozen.")
    args = build_parser().parse_args(argv)
    if args.redownload:
        acquisition = acquire_spy(ticker=args.ticker, cache_dir=args.cache_dir)
        print("redownloaded (not the E03 default)")
    else:
        acquisition = load_latest_cache(args.cache_dir, ticker=args.ticker)
        print(
            f"cache {acquisition.acquired_at_utc.isoformat()} "
            f"{len(acquisition.series)} rows "
            f"{acquisition.series.sessions[0]} → {acquisition.series.sessions[-1]}"
        )

    assert DEFAULT_PARAMS.W == 20 and DEFAULT_PARAMS.k == 50 and DEFAULT_PARAMS.h == 10
    result = run_vol_mechanism(acquisition.series, progress=_progress)
    summary = summarize_mechanism(result)

    payload = {
        **stamp(),
        "experiment": "I01-E03",
        "parent": "I01-E02",
        "parameters_frozen": True,
        "volctrl_is_not_b0": True,
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
    out_json = args.cache_dir / "UNQUALIFIED_i01_e03_last_run.json"
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    prox = summary["past_vol_proximity"]
    assoc = summary["associations"]
    print_banner()
    print(f"n_eval                 : {result.n_eval}")
    print(f"mean H_vol L2/ctrl/B0  : {result.mean_geo['H_vol']:.6e} / {result.mean_volctrl['H_vol']:.6e} / {result.mean_b0['H_vol']:.6e}")
    print(f"mean H_raw L2/ctrl/B0  : {result.mean_geo['H_raw']:.5f} / {result.mean_volctrl['H_raw']:.5f} / {result.mean_b0['H_raw']:.5f}")
    print(f"frac t  H_vol L2<ctrl  : {result.frac_t_geo_vol_lt_ctrl:.3f}")
    print(f"|Δrv| L2/ctrl/library  : {prox['mean_abs_drv_geo_neighbors']:.6f} / {prox['mean_abs_drv_volctrl_neighbors']:.6f} / {prox['mean_median_abs_drv_library']:.6f}")
    print(f"corr rv_W ~ ||Y||      : {assoc['corr_rv_w_future_amp']:.3f}")
    print(f"corr ||X|| ~ ||Y||     : {assoc['corr_x_norm_future_amp']:.3f}")
    print(f"wrote                  : {out_json}")
    print_banner()
    print("No parameter change. Vol-control is not B0. No SCI-PASS. No SCI-FAIL. No trading.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
