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


def fetch_yfinance(ticker: str, period: str = "2y") -> List[tuple]:
    """Daily bars from yfinance. Only run where network is available."""
    import yfinance as yf
    df = yf.Ticker(ticker).history(period=period, interval="1d")
    rows = []
    for idx, r in df.iterrows():
        d = idx.date().isoformat()
        rows.append((d, round(float(r["Open"]), 4), round(float(r["High"]), 4),
                     round(float(r["Low"]), 4), round(float(r["Close"]), 4),
                     int(r["Volume"])))
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description="Fetch daily bars to feed CSVs")
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--tickers", default="SPY,QQQ,IWM,XLF,XLE")
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--bars", type=int, default=300,
                    help="bar count for synthetic mode")
    args = ap.parse_args()

    for i, t in enumerate(args.tickers.split(",")):
        t = t.strip().upper()
        if args.synthetic:
            rows = fetch_synthetic(t, args.bars, seed=1234 + i * 7)
        else:
            rows = fetch_yfinance(t)
        out = args.data_dir / f"{t.lower()}.csv"
        write_csv(out, rows)
        print(f"{t}: wrote {len(rows)} bars -> {out}")


if __name__ == "__main__":
    main()
