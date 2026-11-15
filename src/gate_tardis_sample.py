"""Zero-cost Tardis sample validation - the free first-of-month CSVs.

Registry directive: before purchasing the full Tardis L2 dataset, pull
the free 1st-of-the-month samples for btcusdt on binance-futures
(incremental_book_L2, book_snapshot_25, trades) and validate the replay
engine against the gate criteria.

HONEST BOUNDARY, stated before running: the free incremental_book_L2
CSV schema is (exchange, symbol, timestamp, local_timestamp,
is_snapshot, side, price, amount) - NO U/u/pu sequence numbers. Gate
criterion 1 (sequence gap rate, pu != last_u) CANNOT be evaluated on
this sample; it waits for the raw @depth API data. What this run DOES
validate: criteria 2 and 3 - mid-price agreement within one tick and
10-bps cumulative depth agreement at >= 99% of sampled timestamps,
reconstructed from the incremental stream against the independent
book_snapshot_25 ground truth.

Replay semantics (confirmed against the delivered file): amount == 0 ->
delete the price level; amount > 0 -> upsert. Between two check
timestamps, applying only the LAST update per (side, price) is exactly
equivalent to sequential application of every update - which makes the
replay vectorizable over a 40M-row day.
"""

import argparse
import gzip
from pathlib import Path

import numpy as np
import pandas as pd

TICK = 0.10  # BTCUSDT USDS-M tick size


def load_snapshots(path: Path) -> pd.DataFrame:
    cols = ["timestamp", "asks[0].price", "asks[0].amount", "bids[0].price",
            "bids[0].amount", "asks[24].price", "bids[24].price"]
    df = pd.read_csv(path, usecols=lambda c: c in cols or c == "timestamp")
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diffs", required=True, help="incremental_book_L2 csv.gz")
    ap.add_argument("--snapshots", required=True, help="book_snapshot_25 csv.gz")
    ap.add_argument("--tick-size", type=float, default=TICK)
    ap.add_argument("--n-checks", type=int, default=100)
    ap.add_argument("--depth-bps", type=float, default=10.0)
    ap.add_argument("--depth-rel-tol", type=float, default=0.05)
    ap.add_argument("--max-rows", type=int, default=0, help="optional cap")
    args = ap.parse_args()

    # two-pass snapshot load: timestamps first (cheap), then only the
    # n_checks selected rows with full columns - bounded memory
    ts_only = pd.read_csv(args.snapshots, usecols=["timestamp"])
    idx = np.linspace(0, len(ts_only) - 1, args.n_checks).astype(int)
    keep = set(idx.tolist())
    import csv as _csv
    import gzip as _gzip
    rows = []
    with _gzip.open(args.snapshots, "rt") as fh:
        rd = _csv.reader(fh)
        header = next(rd)
        for i, row in enumerate(rd):
            if i in keep:
                rows.append(row)
    checks = pd.DataFrame(rows, columns=header)
    for c in checks.columns:
        if c != "timestamp" and not isinstance(checks[c].dtype, object):
            pass
    num_cols = [c for c in checks.columns
                if c.startswith(("asks[", "bids["))]
    checks[num_cols] = checks[num_cols].astype(float)
    checks["timestamp"] = checks["timestamp"].astype(np.int64)
    checks = checks.sort_values("timestamp").reset_index(drop=True)
    check_ts = checks["timestamp"].to_numpy()
    print(f"snapshots: {len(ts_only):,} | checks: {len(checks)} "
          f"spanning {check_ts[0]} .. {check_ts[-1]}")

    bids: dict[float, float] = {}
    asks: dict[float, float] = {}
    mid_ok = depth_ok = total = 0
    results = []

    def evaluate(check_row, ts):
        nonlocal mid_ok, depth_ok, total
        mid = (min(asks) + max(bids)) / 2 if bids and asks else np.nan
        # snapshot mid from level 0
        s_ask = check_row["asks[0].price"]
        s_bid = check_row["bids[0].price"]
        s_mid = (s_ask + s_bid) / 2
        mid_pass = (not np.isnan(mid)) and abs(mid - s_mid) <= args.tick_size
        # depth within 10 bps of snapshot mid, capped at snapshot coverage
        lo = s_mid * (1 - args.depth_bps / 10000)
        hi = s_mid * (1 + args.depth_bps / 10000)
        # cap comparison range at the snapshot's 25th level coverage
        lo = max(lo, check_row["bids[24].price"])
        hi = min(hi, check_row["asks[24].price"])
        d_bid = sum(v for p, v in bids.items() if lo <= p <= s_bid)
        d_ask = sum(v for p, v in asks.items() if s_ask <= p <= hi)
        s_ask_cols = [c for c in check_row.index if c.startswith("asks[") and c.endswith(".amount")]
        s_bid_cols = [c for c in check_row.index if c.startswith("bids[") and c.endswith(".amount")]
        # snapshot depth within the same capped range
        sd_bid = sum(check_row[c] for c in s_bid_cols
                     if lo <= check_row[c.replace(".amount", ".price")] <= s_bid)
        sd_ask = sum(check_row[c] for c in s_ask_cols
                     if s_ask <= check_row[c.replace(".amount", ".price")] <= hi)
        depth_pass = (sd_bid + sd_ask > 0 and
                      abs(d_bid - sd_bid) <= args.depth_rel_tol * sd_bid and
                      abs(d_ask - sd_ask) <= args.depth_rel_tol * sd_ask)
        total += 1
        mid_ok += bool(mid_pass)
        depth_ok += bool(depth_pass)
        results.append((ts, mid, s_mid, d_bid, sd_bid, d_ask, sd_ask,
                        bool(mid_pass), bool(depth_pass)))

    # stream the incremental diffs (bounded memory: one chunk at a time)
    read = 0
    check_i = 0
    initialized = False
    chunk_iter = pd.read_csv(
        args.diffs,
        usecols=["timestamp", "is_snapshot", "side", "price", "amount"],
        dtype={"timestamp": np.int64, "side": str, "price": float, "amount": float},
        chunksize=500_000,
        compression={"method": "gzip"},
    )
    def apply_rows(grp):
        last = grp.groupby(["side", "price"], sort=False)["amount"].tail(1)
        sides = grp.loc[last.index, "side"].to_numpy()
        prices = grp.loc[last.index, "price"].to_numpy()
        amounts = last.to_numpy()
        for side, price, amount in zip(sides, prices, amounts):
            book = bids if side == "bid" else asks
            if amount == 0:
                book.pop(price, None)
            else:
                book[price] = amount

    for chunk in chunk_iter:
        if args.max_rows and read + len(chunk) > args.max_rows:
            chunk = chunk.iloc[: args.max_rows - read]
        read += len(chunk)
        pos = 0
        n = len(chunk)
        ts_arr = chunk["timestamp"].to_numpy()
        snap_mask = chunk["is_snapshot"].to_numpy()
        # find snapshot blocks (full resets)
        snap_change = np.flatnonzero(np.diff(snap_mask.astype(int)) != 0) + 1
        bounds = [0] + list(snap_change) + [n]
        for bi in range(len(bounds) - 1):
            b0, b1 = bounds[bi], bounds[bi + 1]
            block = chunk.iloc[b0:b1]
            if bool(snap_mask[b0]):
                bids.clear(); asks.clear()
                for side, price, amount in zip(block["side"], block["price"],
                                              block["amount"]):
                    (bids if side == "bid" else asks)[price] = amount
                initialized = True
                pos = b1
                continue
            if not initialized:
                pos = b1
                continue
            # apply this incremental block up to each check boundary
            bts = block["timestamp"].to_numpy()
            while check_i < len(check_ts) and check_ts[check_i] <= bts[-1]:
                ts = check_ts[check_i]
                k = np.searchsorted(bts, ts, side="right")
                if k > 0:
                    apply_rows(block.iloc[:k])
                    block = block.iloc[k:]
                    bts = block["timestamp"].to_numpy()
                evaluate(checks.iloc[check_i], ts)
                check_i += 1
            apply_rows(block)
            pos = b1
        if args.max_rows and read >= args.max_rows:
            break
        if check_i >= len(check_ts):
            break

    print(f"\nrows read: {read:,} | checks evaluated: {total}")
    if total == 0:
        print("GATE SAMPLE: NO CHECKS EVALUATED - FAIL")
        raise SystemExit(1)
    mid_rate = mid_ok / total
    depth_rate = depth_ok / total
    print(f"mid agreement (1 tick):   {mid_ok}/{total} = {mid_rate:.1%} "
          f"(gate: >= 99%)")
    print(f"depth agreement (10bps): {depth_ok}/{total} = {depth_rate:.1%} "
          f"(gate: >= 99%, rel tol {args.depth_rel_tol:.0%})")
    seq_note = ("N/A on this sample: free incremental_book_L2 CSV carries "
                "no U/u/pu sequence numbers - criterion 1 waits for the "
                "raw @depth API data")
    print(f"sequence gap rate:        {seq_note}")
    ok = mid_rate >= 0.99 and depth_rate >= 0.99
    print("\nGATE SAMPLE: " + ("PASS (criteria 2 and 3)" if ok else "FAIL"))
    out = Path("paper/research/gate_sample_"
               + Path(args.diffs).stem.split("_")[2] + ".txt")
    out.parent.mkdir(exist_ok=True)
    out.write_text(
        f"diffs: {args.diffs}\nsnapshots: {args.snapshots}\n"
        f"rows read: {read}\nchecks: {total}\nmid agreement: {mid_rate:.1%}\n"
        f"depth agreement: {depth_rate:.1%}\nsequence gap rate: {seq_note}\n"
        f"verdict: {'PASS (criteria 2 and 3)' if ok else 'FAIL'}\n")
    print("written:", out)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
