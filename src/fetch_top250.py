"""Fetch the TOP-250 crypto universe (owner directive: 'stick to main
250 crypto'): Binance USDT pairs ranked by 24h quote volume, with
leveraged-token and non-crypto/stable filters, 1356 daily bars each,
replacing data_fresh as THE universe cache (read-only public
endpoints; no auth)."""
import csv
import json
import time
import urllib.request
from pathlib import Path
import pandas as pd

FRESH = Path("paper/research/data_fresh")
BASE = "https://api.binance.com/api/v3"
EXCLUDE_SUB = ("UPUSDT", "DOWNUSDT", "BULLUSDT", "BEARUSDT")
STABLES = {"USDCUSDT", "FDUSDUSDT", "TUSDUSDT", "BUSDUSDT", "DAIUSDT",
           "EURUSDT", "AEURUSDT", "USDPUSDT", "PAXGUSDT", "XUSDUSDT"}
WANT = 1356


def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read())


def main():
    tick = get(f"{BASE}/ticker/24hr")
    rows = [t for t in tick if t["symbol"].endswith("USDT")
            and t["quoteVolume"] and float(t["quoteVolume"]) > 0
            and not any(t["symbol"].endswith(s) and s != "USDT"
                        for s in EXCLUDE_SUB)
            and t["symbol"] not in STABLES
            and t["count"] and int(t["count"]) > 0]
    rows.sort(key=lambda t: -float(t["quoteVolume"]))
    top = [t["symbol"] for t in rows[:250]]
    print("top250 universe size:", len(top))
    FRESH.mkdir(exist_ok=True)
    keep = set()
    ok, fail = 0, []
    for sym in top:
        stem = sym.lower()[:-4] + "usd"
        keep.add(stem + ".csv")
        try:
            k1 = get(f"{BASE}/klines?symbol={sym}&interval=1d&limit=1000")
            oldest = k1[0][0]
            if len(k1) < 120:
                fail.append(sym)
                continue
            if len(k1) < WANT:
                k2 = get(f"{BASE}/klines?symbol={sym}&interval=1d"
                         f"&limit=1000&endTime={oldest - 1}")
                k1 = k2 + k1
            out = [{
                "date": pd.to_datetime(k[0], unit="ms").strftime(
                    "%Y-%m-%d"),
                "open": k[1], "high": k[2], "low": k[3],
                "close": k[4], "volume": k[5],
            } for k in k1[-WANT:]]
            with open(FRESH / f"{stem}.csv", "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=["date", "open",
                                                  "high", "low",
                                                  "close", "volume"])
                w.writeheader()
                w.writerows(out)
            ok += 1
            time.sleep(0.12)
        except Exception:
            fail.append(sym)
    for p in sorted(FRESH.glob("*.csv")):
        if p.name not in keep:
            p.unlink()
    print(f"fetched {ok} ok, {len(fail)} failed: {fail[:20]}")


if __name__ == "__main__":
    main()
