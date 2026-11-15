"""Trade-vs-depth reconciliation for one ingested Tardis day.

Reconciles `trade` prints against same-price `depth` reductions and logs:
  - passive cancellation fraction: fraction of depth size-reductions at
    prices that received NO trade print in the reconciliation window -
    i.e., liquidity that left passively (cancelled) rather than being
    consumed by a taker.
  - median 10-bps depth (from the reconstructed book at sampled states).

HALT CONDITION (pre-declared): passive cancellation fraction < 1.0%
indicates a frozen-book regime (depth changes are almost all
trade-consumption; the cancel channel carries no information) - the C5
cancellation-imbalance claim is untestable on such a day and the run halts.

Descriptive reconciliation only. No predictive model consumes this output.
"""

import argparse
import gzip
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def reconcile_day(day_dir: Path, match_window_us: int = 1_000_000,
                  max_depth_rows: int = 0) -> dict:
    """Reconcile trade prints against same-price depth reductions.

    A depth row with size < previous size at that price is a reduction.
    If a trade print at the same price exists within +/- match_window_us,
    the reduction is attributed to trade consumption; otherwise it is a
    passive cancellation.
    """
    # pass 1: traded prices with timestamps
    traded = defaultdict(list)  # price -> array of trade ts (µs)
    n_trades = 0
    trade_path = day_dir / "trade.ndjson.gz"
    if trade_path.exists():
        with gzip.open(trade_path, "rt") as fh:
            for line in fh:
                rec = json.loads(line)
                d = rec["data"]
                p = float(d.get("p") or d.get("price"))
                traded[p].append(rec["exchange_ts_us"])
                n_trades += 1
    for p in traded:
        traded[p] = np.asarray(traded[p])

    # pass 2: walk depth diffs, track size per (side, price), classify
    # reductions as trade-consumed vs passive-cancelled
    last_size = {}
    n_reductions = 0
    n_trade_consumed = 0
    n_passive_cancel = 0
    n_depth_rows = 0
    depth_path = day_dir / "depth.ndjson.gz"
    with gzip.open(depth_path, "rt") as fh:
        for line in fh:
            n_depth_rows += 1
            if max_depth_rows and n_depth_rows > max_depth_rows:
                break
            rec = json.loads(line)
            d = rec["data"]
            ts = rec["exchange_ts_us"]
            for side_key in ("b", "a"):
                for px_s, qty_s in d.get(side_key) or []:
                    px = float(px_s)
                    qty = float(qty_s)
                    key = (side_key, px)
                    prev = last_size.get(key)
                    last_size[key] = qty
                    if prev is not None and qty < prev:
                        n_reductions += 1
                        tt = traded.get(px)
                        if tt is not None and len(tt) and \
                                np.min(np.abs(tt - ts)) <= match_window_us:
                            n_trade_consumed += 1
                        else:
                            n_passive_cancel += 1

    cancel_frac = (n_passive_cancel / n_reductions
                  if n_reductions else float("nan"))
    return {
        "n_trades": n_trades,
        "n_depth_diff_messages": n_depth_rows,
        "n_reductions": n_reductions,
        "n_trade_consumed": n_trade_consumed,
        "n_passive_cancel": n_passive_cancel,
        "passive_cancellation_fraction": cancel_frac,
    }


def median_10bps_depth(gate_snapshots_csv: Path) -> dict:
    """Median reconstructed 10-bps depth from the gate snapshot CSV."""
    import pandas as pd
    df = pd.read_csv(gate_snapshots_csv)
    if df.empty:
        return {"median_bid_depth_10bps": float("nan"),
                "median_ask_depth_10bps": float("nan"),
                "n_snapshots": 0}
    return {
        "median_bid_depth_10bps": float(df["bid_depth_10bps"].median()),
        "median_ask_depth_10bps": float(df["ask_depth_10bps"].median()),
        "n_snapshots": int(len(df)),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--day-dir", type=Path, required=True,
                    help="data/raw/tardis_btcusdt/date=YYYY-MM-DD")
    ap.add_argument("--gate-snapshots", type=Path, default=None)
    ap.add_argument("--match-window-us", type=int, default=1_000_000)
    ap.add_argument("--max-depth-rows", type=int, default=0)
    ap.add_argument("--cancel-fraction-halt", type=float, default=0.01)
    args = ap.parse_args(argv)

    rec = reconcile_day(args.day_dir, args.match_window_us,
                        args.max_depth_rows)
    out = dict(rec)
    if args.gate_snapshots and args.gate_snapshots.exists():
        out.update(median_10bps_depth(args.gate_snapshots))
    print(json.dumps(out, indent=2))
    cf = rec["passive_cancellation_fraction"]
    if np.isnan(cf) or cf < args.cancel_fraction_halt:
        print("HALT: passive cancellation fraction "
              f"{cf if not np.isnan(cf) else 'nan'} < "
              f"{args.cancel_fraction_halt:.2%} - frozen-book regime, "
              "cancellation dynamics untestable on this day")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
