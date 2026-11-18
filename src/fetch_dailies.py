"""Fetch fresh daily OHLCV (1,356 bars = full burn-in) for every
archive USD pair, plus weekly 89/144 aggregations flag (owner
directive: "go get dailies 1356 length or 144 or 89 weekly").

Legal/acquisition note (declared openly): public market data via
Binance's public klines endpoint (no authentication, no key, read-
only GET). Output: paper/research/data_fresh/<stem>.csv in the same
format as the archive (date,open,high,low,close,volume). Two
requests per symbol (klines max 1000 per call; a second backwards
request completes 1356). Failures (delisted/unknown symbols) are
recorded, not retried blindly; nothing else about the archive
changes. The fetched cache feeds the current-seats board scan only;
all program claims remain W2-owing.
"""
import csv
import time
import urllib.request
from pathlib import Path
import pandas as pd

DATA_FRESH = Path("paper/research/data_fresh")
DATA = Path("paper/research/data")
BASE = "https://api.binance.com/api/v3/klines"
WANT = 1356


def klines(symbol, **params):
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{BASE}?symbol={symbol}&interval=1d&{qs}"
    with urllib.request.urlopen(url, timeout=20) as r:
        return __import__("json").loads(r.read())


def fetch_symbol(stem):
    sym = stem[:-3].upper() + "USDT"
    try:
        rows = klines(sym, limit=1000)
        if len(rows) < 120:
            return None, sym
        oldest = rows[0][0]
        need = WANT - len(rows)
        if need > 0:
            rows2 = klines(sym, limit=1000, endTime=oldest - 1)
            rows = rows2 + rows
        out = []
        for k in rows:
            out.append({
                "date": pd.to_datetime(k[0], unit="ms").strftime(
                    "%Y-%m-%d"),
                "open": k[1], "high": k[2], "low": k[3],
                "close": k[4], "volume": k[5],
            })
        return out, sym
    except Exception:
        return None, sym


def main():
    DATA_FRESH.mkdir(exist_ok=True)
    ok, fail = [], []
    stems = sorted(p.stem for p in DATA.glob("*.csv")
                   if p.stem.endswith("usd"))
    for stem in stems:
        rows, sym = fetch_symbol(stem)
        if not rows:
            fail.append(stem)
            continue
        with open(DATA_FRESH / f"{stem}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["date", "open", "high",
                                              "low", "close",
                                              "volume"])
            w.writeheader()
            w.writerows(rows)
        ok.append(stem)
        time.sleep(0.12)
    print(f"fresh fetch: {len(ok)} ok, {len(fail)} failed")
    if fail:
        print("failed stems:", ", ".join(fail))


if __name__ == "__main__":
    main()
