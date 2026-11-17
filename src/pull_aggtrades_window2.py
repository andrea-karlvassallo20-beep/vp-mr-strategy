"""Download the second aggTrades window (2024-08-01 -> 2025-02-28) from
Binance Vision public archives into data/raw/aggTrades/. Free data,
public archives, the exact window prepared in
paper/research/aggtrades_second_window_2024-08_2025-02.md. Skips files
that already exist with non-trivial size. Parallel, resumable.
"""

import concurrent.futures
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

OUT = Path("data/raw/aggTrades")
BASE = ("https://data.binance.vision/data/futures/um/daily/aggTrades/"
        "BTCUSDT/BTCUSDT-aggTrades-{d}.zip")


def fetch(d: date) -> tuple:
    dest = OUT / f"BTCUSDT-aggTrades-{d.isoformat()}.zip"
    if dest.exists() and dest.stat().st_size > 10_000_000:
        return (str(dest), "exists")
    try:
        urllib.request.urlretrieve(BASE.format(d=d.isoformat()), dest)
        return (str(dest), f"ok {dest.stat().st_size}")
    except Exception as e:  # noqa: BLE001
        return (str(dest), f"FAIL {type(e).__name__} {e}")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    days = []
    d = date(2024, 8, 1)
    end = date(2025, 2, 28)
    while d <= end:
        days.append(d)
        d += timedelta(days=1)
    n_fail = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for i, (path, status) in enumerate(
                ex.map(fetch, days), 1):
            if status.startswith("FAIL"):
                n_fail += 1
            if i % 20 == 0 or status.startswith("FAIL"):
                print(f"[{i}/{len(days)}] {Path(path).name}: {status}",
                      flush=True)
    print(f"done: {len(days)} days, {n_fail} failures", flush=True)
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
