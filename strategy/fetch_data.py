"""Daily bar fetcher for the VP-MR paper-trading feed contract.

Real mode (requires network + yfinance, run in your environment or CI):
    python3 fetch_data.py --data-dir ./data --tickers SPY,QQQ,IWM,XLF,XLE

Synthetic mode (no network, deterministic — used by CI and local tests):
    python3 fetch_data.py --data-dir ./data --synthetic --bars 300

Writes one CSV per ticker: date,open,high,low,close,volume.
This is an operational harness, not strategy code.
"""
import argparse
import datetime
from pathlib import Path
from typing import List

SYNTHETIC_DEFAULTS = {"SPY": 450.0, "QQQ": 380.0, "IWM": 200.0,
                       "XLF": 38.0, "XLE": 88.0}


def write_csv(path: Path, rows: List[tuple]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".csv.tmp")
    with open(tmp, "w", newline="") as f:
        f.write("date,open,high,low,close,volume\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")
    tmp.replace(path)


def fetch_synthetic(ticker: str, bars: int, seed: int) -> List[tuple]:
    """Deterministic OU path — same generator family as the studies."""
    import numpy as np
    rng = np.random.default_rng(seed)
    s0 = SYNTHETIC_DEFAULTS.get(ticker.upper(), 100.0)
    p = np.empty(bars); p[0] = s0
    for i in range(1, bars):
        p[i] = p[i-1] + 0.05 * (s0 - p[i-1]) + rng.normal(0, s0 * 0.003)
    rows = []
    d0 = datetime.date.today() - datetime.timedelta(days=bars)
    for i in range(bars):
        c = round(float(p[i]), 4)
        d = (d0 + datetime.timedelta(days=i)).isoformat()
        rows.append((d, c, round(c * 1.002, 4), round(c * 0.998, 4),
                     c, 1_000_000))
    return rows


def fetch_yfinance(ticker: str, period: str = "5y",
                    max_retries: int = 3, base_wait: float = 2.0) -> List[tuple]:
    """Daily bars from yfinance. Only run where network is available.
    Retries with exponential backoff (cloud IPs are often throttled) and
    fails loudly on empty responses rather than writing a header-only CSV."""
    import time
    import yfinance as yf
    last_err = None
    for attempt in range(max_retries):
        try:
            df = yf.Ticker(ticker).history(period=period, interval="1d")
            if df is None or len(df) == 0:
                last_err = RuntimeError(f"empty frame for {ticker}")
            else:
                # yfinance may return tz-aware index and/or MultiIndex columns
                if isinstance(df.columns, __import__("pandas").MultiIndex):
                    df.columns = df.columns.get_level_values(-1)
                rows = []
                for idx, r in df.iterrows():
                    d = idx.date().isoformat()
                    rows.append((d, round(float(r["Open"]), 4),
                                 round(float(r["High"]), 4),
                                 round(float(r["Low"]), 4),
                                 round(float(r["Close"]), 4),
                                 int(r["Volume"])))
                return rows
        except Exception as e:  # network/throttle/schema errors: retry
            last_err = e
        if attempt < max_retries - 1:
            wait = base_wait * (2 ** attempt)
            print(f"fetch {ticker}: attempt {attempt + 1} failed "
                  f"({last_err}); retrying in {wait:.0f}s")
            time.sleep(wait)
    raise RuntimeError(
        f"yfinance fetch failed for {ticker} after {max_retries} attempts: "
        f"{last_err}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Fetch daily bars to feed CSVs")
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--tickers", default="SPY,QQQ,IWM,XLF,XLE")
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--bars", type=int, default=300,
                    help="bar count for synthetic mode")
    ap.add_argument("--drop-today", action="store_true",
                    help="drop bars dated today (UTC) — intraday/manual "
                         "fetches must not consume a partial bar as final")
    args = ap.parse_args()

    for i, t in enumerate(args.tickers.split(",")):
        t = t.strip().upper()
        if args.synthetic:
            rows = fetch_synthetic(t, args.bars, seed=1234 + i * 7)
        else:
            rows = fetch_yfinance(t)
            if args.drop_today:
                from datetime import datetime, timezone
                today = datetime.now(timezone.utc).date().isoformat()
                rows = [r for r in rows if r[0] != today]
        out = args.data_dir / f"{t.lower()}.csv"
        write_csv(out, rows)
        print(f"{t}: wrote {len(rows)} bars -> {out}")


if __name__ == "__main__":
    main()
