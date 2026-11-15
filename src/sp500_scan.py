"""S&P 500 clue scan - the equity half of the board at full width.

Directive (Andrea, Nov 2026): the heat map covers EVERYTHING - all
commodities, all indexes, crypto, and the main 500 stocks. The crypto
half was scanned in top500_scan (PR #87) and the non-crypto half in
eq_commodity_scan, but that equity universe held only ~50 large caps.
This scan extends the descriptive clue program to the FULL S&P 500
constituents: the same coil/genesis questions, the same honest caveats.

Universe construction (honest and dated):
  - The current constituent list from the Wikipedia
    "List of S&P 500 companies" table, snapshot date recorded in the
    output. The list is a SNAPSHOT, not a permanent truth; the scan
    reports the date it looked.
  - Daily bars from the Yahoo chart API via eq_commodity_scan.fetch
    (shared CSV cache in data/raw/eq_commodity_klines, real exchange
    volume, ~10y lookback).

DESCRIPTIVE ONLY. The multiplicity warning is binding and worse here
than anywhere: scanning 500 equities for extremes finds extremes by
construction. Nothing in this file tests a claim; C7's dataset is
sealed and this scan does not touch it. Candidates, not evidence.
The genesis filter from the crypto scan applies: <90 days of history
excludes an asset from primed candidacy (recent IPOs hold their ATH
inside the launch window - the launch, not a coil).
"""

import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clue_scan import expansion_stats, primed_score, scan_series  # noqa: E402
from eq_commodity_scan import fetch, genesis_metrics  # noqa: E402

OUT = Path("paper/research/clue_scan")
UNIVERSE_CSV = OUT / "sp500_universe.csv"
SCAN_CSV = OUT / "sp500_scan_table.csv"
GENESIS_CSV = OUT / "sp500_genesis.csv"
MIN_HISTORY_DAYS = 90


def fetch_universe():
    """Current S&P 500 constituents from Wikipedia (snapshot, dated)."""
    req = urllib.request.Request(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
        headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=30).read().decode()
    m = re.search(r'<table[^>]*id="constituents"[^>]*>(.*?)</table>', html, re.S)
    if not m:
        raise SystemExit("could not find the constituents table")
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(1), re.S)
    tickers = []
    for r in rows[1:]:
        tds = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)
        if not tds:
            continue
        tick = re.sub(r"<[^>]+>", "", tds[0]).strip()
        if tick and tick not in ("Symbol",):
            tickers.append(tick)
    if len(tickers) < 400:
        raise SystemExit(f"suspiciously short constituent list: {len(tickers)}")
    snap = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    df = pd.DataFrame({
        "symbol": tickers,
        "snapshot_date": snap,
        "source": "wikipedia_list_of_sp500_companies",
    })
    return df


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    uni = fetch_universe()
    uni.to_csv(UNIVERSE_CSV, index=False)
    print(f"universe snapshot: {len(uni)} constituents "
          f"({uni['snapshot_date'].iloc[0]})")

    rows, genesis_rows, failures = [], [], []
    for symbol in uni["symbol"]:
        name = symbol.lower().replace(".", "_")
        df = fetch(symbol)
        if df is None or len(df) < 150:
            failures.append(symbol)
            continue
        s = scan_series(name, df)
        s["yahoo_symbol"] = symbol
        s["class"] = "sp500"
        ret30 = df["close"].iloc[-1] / df["close"].iloc[-31] - 1.0
        s["ret30"] = round(float(ret30), 3)
        s["artifact_flag"] = bool(abs(ret30) > 0.20)
        exp = expansion_stats(df)
        s["n_coil_exits"] = exp["n_coil_exits"] if exp else 0
        s["median_max10d"] = (exp["median_max10d"] if exp else np.nan)
        s["pct_with_4sigma_day"] = (
            exp["pct_with_4sigma_day"] if exp else np.nan)
        s["primed_score"] = primed_score(s)
        s["short_history"] = bool(len(df) < MIN_HISTORY_DAYS + 60)
        g = genesis_metrics(df)
        g["series"] = name
        genesis_rows.append(g)
        rows.append(s)
        time.sleep(0.05)

    scan = pd.DataFrame(rows).sort_values(
        "primed_score", ascending=False).reset_index(drop=True)
    scan.to_csv(SCAN_CSV, index=False)
    if genesis_rows:
        pd.DataFrame(genesis_rows).sort_values(
            "first_bar").reset_index(drop=True).to_csv(GENESIS_CSV, index=False)

    print(f"scanned {len(scan)} series ({len(failures)} failed: {failures})")
    clean = scan[~scan["artifact_flag"] & ~scan["short_history"]]
    print("\n=== top-10 primed candidates (artifact + genesis filtered) ===")
    cols = ["series", "primed_score", "comp_days", "rvol_pct",
            "range_pos", "vol_ratio", "ret30"]
    print(clean.head(10)[cols].to_string(index=False))
    withexp = scan.dropna(subset=["median_max10d"])
    print(f"\n[sp500] deep coils (comp_days>=20)="
          f"{int((scan['comp_days'] >= 20).sum())}  "
          f"median coil-exit |10d|="
          f"{withexp['median_max10d'].median() if len(withexp) else float('nan'):.4f}")
    print("\nDESCRIPTIVE ONLY. Multiplicity binds. C7 stays sealed.")


if __name__ == "__main__":
    main()
