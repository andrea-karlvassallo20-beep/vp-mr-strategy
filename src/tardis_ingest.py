"""Tardis.dev raw replay ingestion for BTCUSDT USDS-M perpetual futures
(exchange="binance-futures").

CRITICAL SCHEMA RULE (binding): we do NOT use the pre-normalized
incremental_book_L2 CSVs - they strip Binance's native sequence fields
(U, u, pu) required by the sequence-gap kill line. We pull RAW WebSocket
replay channels via tardis_dev.replay for symbol btcusdt across:
  - depth         (native depthUpdate diffs: U, u, pu, b, a)
  - depthSnapshot (initial book snapshots: bids, asks arrays)
  - trade         (p, q, isBuyerMaker, T)

Storage: partitioned NDJSON.gz under data/raw/tardis_btcusdt/date=YYYY-MM-DD/
with timestamps normalized to int64 UTC microseconds:
  exchange_ts_us (from the exchange event time), local_ts_us (from the
  Tardis localTimestamp). All raw fields (U, u, pu, lastUpdateId when
  present, price/qty arrays, isBuyerMaker) are preserved verbatim in the
  `data` payload.

Resume/retry: one partition per UTC day; a day is complete only when its
`.done` marker exists, so network drops never corrupt completed files and
re-runs skip finished days.

No API key is ever read from a file in this repo - only from the
TARDIS_API_KEY environment variable.
"""

import argparse
import asyncio
import datetime as dt
import gzip
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data/raw/tardis_btcusdt"
CHANNELS = ("depth", "depthSnapshot", "trade")
SYMBOL = "btcusdt"
EXCHANGE = "binance-futures"
RETRIES_PER_DAY = 5


def _to_us(ts) -> int:
    """Normalize a Tardis/Binance timestamp to int64 UTC microseconds.

    Binance exchange event times (E/T) are MILLISECONDS; a numeric value
    below 1e14 is treated as ms and scaled x1000 (16-digit values are
    already microseconds). ISO strings / datetimes convert normally.
    """
    if ts is None:
        return 0
    if isinstance(ts, str):
        ts = ts.replace("Z", "+00:00")
        ts = dt.datetime.fromisoformat(ts)
    if isinstance(ts, dt.datetime):
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=dt.timezone.utc)
        return int(ts.timestamp() * 1_000_000)
    v = int(ts)
    if 0 < v < 10**14:  # milliseconds (Binance E/T) -> microseconds
        v *= 1000
    return v


def day_range(start: str, end: str):
    d = dt.date.fromisoformat(start)
    e = dt.date.fromisoformat(end)
    while d <= e:
        yield d.isoformat()
        d += dt.timedelta(days=1)


def day_dir(out_root: Path, day: str) -> Path:
    return out_root / f"date={day}"


def day_complete(out_root: Path, day: str) -> bool:
    return (day_dir(out_root, day) / ".done").exists()


async def _replay_day(day: str, out_root: Path, api_key: str,
                      cache_dir: str = "/tmp/.tardis-cache") -> None:
    """Replay one UTC day and write per-channel NDJSON.gz partitions."""
    import tardis_dev
    from tardis_dev.channel import Channel

    ddir = day_dir(out_root, day)
    ddir.mkdir(parents=True, exist_ok=True)
    tmp = ddir / ".partial"
    tmp.mkdir(exist_ok=True)
    handles = {}
    counts = {ch: 0 for ch in CHANNELS}
    try:
        async for resp in tardis_dev.replay(
            from_date=day,
            to_date=(dt.date.fromisoformat(day)
                     + dt.timedelta(days=1)).isoformat(),
            exchange=EXCHANGE,
            filters=[Channel(ch, [SYMBOL]) for ch in CHANNELS],
            api_key=api_key,
            cache_dir=cache_dir,
            with_disconnects=True,
        ):
            if resp is None:  # disconnect marker (with_disconnects=True)
                continue
            msg = resp.message if hasattr(resp, "message") else resp
            if isinstance(msg, (bytes, bytearray)):
                msg = msg.decode("utf-8")
            if isinstance(msg, str):
                try:
                    obj = json.loads(msg)
                except json.JSONDecodeError:
                    continue
            else:
                obj = msg
            stream = obj.get("stream") or ""
            if "@depth" in stream and "depthSnapshot" not in stream:
                ch = "depth"
            elif "depthSnapshot" in stream:
                ch = "depthSnapshot"
            elif "@trade" in stream or "trade" in stream:
                ch = "trade"
            else:
                ch = "other"
            if ch not in CHANNELS:
                continue
            data = obj.get("data", obj)
            local_us = _to_us(getattr(resp, "local_timestamp", None)
                              if not isinstance(resp, (str, bytes, dict))
                              else data.get("localTimestamp"))
            rec = {
                "local_ts_us": local_us,
                "exchange_ts_us": _to_us(data.get("E") or data.get("T")
                                         or data.get("timestamp")),
                "channel": ch,
                "data": data,  # raw payload, all native fields preserved
            }
            if ch not in handles:
                handles[ch] = gzip.open(tmp / f"{ch}.ndjson.gz", "wt")
            handles[ch].write(json.dumps(rec, separators=(",", ":")) + "\n")
            counts[ch] += 1
    finally:
        for h in handles.values():
            h.close()
    # atomic-ish completion: move tmp files into place, then mark done
    for ch in CHANNELS:
        src = tmp / f"{ch}.ndjson.gz"
        if src.exists():
            os.replace(src, ddir / f"{ch}.ndjson.gz")
    if tmp.exists():
        tmp.rmdir()
    (ddir / ".done").write_text(
        json.dumps(counts) + "\n", encoding="utf-8")
    print(f"[ingest] {day}: " + ", ".join(f"{k}={v:,}" for k, v in counts.items()))


def ingest(start: str, end: str, out_root: Path = DEFAULT_OUT,
           api_key: str = None) -> int:
    """Ingest [start, end] inclusive, day by day, with retry/resume."""
    api_key = api_key or os.environ.get("TARDIS_API_KEY", "")
    if not api_key:
        print("TARDIS_API_KEY not set", file=sys.stderr)
        return 2
    failures = []
    for day in day_range(start, end):
        if day_complete(out_root, day):
            print(f"[ingest] {day}: already complete, skipping")
            continue
        ok = False
        for attempt in range(1, RETRIES_PER_DAY + 1):
            try:
                asyncio.run(_replay_day(day, out_root, api_key))
                ok = True
                break
            except KeyboardInterrupt:
                raise
            except Exception as e:  # noqa: BLE001 - resume-safe retry
                print(f"[ingest] {day}: attempt {attempt} failed: "
                      f"{type(e).__name__}: {str(e)[:200]}")
        if not ok:
            failures.append(day)
    if failures:
        print(f"[ingest] FAILED days (rerun to resume): {failures}",
              file=sys.stderr)
        return 1
    return 0


# ---------------------------------------------------------------------------
# Conversion to the Layer 0 gate input (expanded per-level CSVs)
# ---------------------------------------------------------------------------

def day_to_gate_csv(out_root: Path, day: str, tick_size: float = 0.1,
                    max_diff_rows: int = 0) -> dict:
    """Convert one ingested day into src/verify_l2_gate.py inputs:

      diffs CSV   : ts_exchange_us, seq_U, seq_u, seq_pu, side, price, size
                    (b/a arrays expanded per level, native U/u/pu preserved)
      snapshot CSV: ts_exchange_us, bid_price, ask_price,
                    bid_depth_10bps, ask_depth_10bps (from depthSnapshot)

    Returns {"diffs": path, "snapshots": path, "n_diff_rows": int}.
    """
    ddir = day_dir(out_root, day)
    diffs_p = ddir / "gate_diffs.csv"
    snap_p = ddir / "gate_snapshots.csv"
    n_rows = 0
    with gzip.open(ddir / "depth.ndjson.gz", "rt") as fh, \
            open(diffs_p, "w", newline="") as out:
        out.write("ts_exchange_us,local_ts_us,seq_U,seq_u,seq_pu,side,"
                  "price,size\n")
        for line in fh:
            rec = json.loads(line)
            d = rec["data"]
            ts = rec["exchange_ts_us"]
            lts = rec["local_ts_us"]
            U, u, pu = d.get("U", ""), d.get("u", ""), d.get("pu", "")
            for side_key, side in (("b", "bid"), ("a", "ask")):
                for px, qty in d.get(side_key) or []:
                    out.write(f"{ts},{lts},{U},{u},{pu},{side},{px},{qty}\n")
                    n_rows += 1
                    if max_diff_rows and n_rows >= max_diff_rows:
                        break
                if max_diff_rows and n_rows >= max_diff_rows:
                    break
            if max_diff_rows and n_rows >= max_diff_rows:
                break
    with gzip.open(ddir / "depthSnapshot.ndjson.gz", "rt") as fh, \
            open(snap_p, "w", newline="") as out:
        out.write("ts_exchange_us,bid_price,ask_price,"
                  "bid_depth_10bps,ask_depth_10bps\n")
        for line in fh:
            rec = json.loads(line)
            d = rec["data"]
            ts = rec["exchange_ts_us"]
            bids = d.get("bids") or []
            asks = d.get("asks") or []
            if not bids or not asks:
                continue
            bid_px = max(float(p) for p, _ in bids)
            ask_px = min(float(p) for p, _ in asks)
            mid = (bid_px + ask_px) / 2.0
            band = mid * 0.001  # 10 bps
            bd = sum(float(q) for p, q in bids if float(p) >= mid - band)
            ad = sum(float(q) for p, q in asks if float(p) <= mid + band)
            out.write(f"{ts},{bid_px},{ask_px},{bd},{ad}\n")
    return {"diffs": diffs_p, "snapshots": snap_p, "n_diff_rows": n_rows}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--start", default="2026-05-01")
    ap.add_argument("--end", default="2026-11-01")
    ap.add_argument("--out-root", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--gate-csv", metavar="DAY",
                    help="convert one ingested day to gate CSVs and exit")
    args = ap.parse_args(argv)
    if args.gate_csv:
        info = day_to_gate_csv(args.out_root, args.gate_csv)
        print(json.dumps({k: str(v) for k, v in info.items()}))
        return 0
    return ingest(args.start, args.end, args.out_root)


if __name__ == "__main__":
    sys.exit(main())
