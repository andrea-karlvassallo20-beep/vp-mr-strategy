"""The mid/small scan - S&P 400 and S&P 600 join the board.

Directive (Andrea, Nov 2026): "5000 more, whatever it is - pull
everything." The S&P 500 is on the board; this scan adds the other two
tiers of the US market: the S&P 400 mid caps and the S&P 600 small caps
(Wikipedia constituent snapshots, dated), same Yahoo daily bars via
the shared cache, same coil/genesis questions.

DESCRIPTIVE ONLY. The multiplicity warning is binding: scanning ~1000
more equities for extremes finds extremes by construction. Candidates,
not evidence; C7's dataset stays sealed. The genesis filter applies:
<150 days of history flags a recent addition (the launch, not a coil).
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
from eq_commodity_scan import fetch  # noqa: E402
from sp500_scan import MIN_HISTORY_DAYS  # noqa: E402

OUT = Path("paper/research/clue_scan")
SCAN_CSV = OUT / "midsmall_scan_table.csv"

PAGES = {
    "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies": "sp400",
    "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies": "sp600",
}


def fetch_universe():
    """S&P 400 + S&P 600 constituents from Wikipedia (snapshot, dated)."""
    tickers = []
    snap = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for url, cls in PAGES.items():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=30).read().decode()
        m = re.search(r'<table[^>]*id="constituents"[^>]*>(.*?)</table>',
                      html, re.S)
        if not m:
            raise SystemExit(f"could not find the constituents table: {url}")
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(1), re.S)
        for r in rows[1:]:
            tds = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)
            if not tds:
                continue
            tick = re.sub(r"<[^>]+>", "", tds[0]).strip()
            if tick and tick != "Symbol":
                tickers.append((tick, cls))
    if len(tickers) < 900:
        raise SystemExit(f"suspiciously short constituent list: {len(tickers)}")
    return tickers, snap


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    universe, snap = fetch_universe()
    print(f"universe snapshot: {len(universe)} constituents ({snap})")

    rows, failures = [], []
    for symbol, cls in universe:
        name = symbol.lower().replace(".", "_")
        df = fetch(symbol)
        if df is None or len(df) < 150:
            failures.append(symbol)
            continue
        s = scan_series(name, df)
        s["yahoo_symbol"] = symbol
        s["class"] = cls
        s["venue"] = "yahoo"
        ret30 = df["close"].iloc[-1] / df["close"].iloc[-31] - 1.0
        s["ret30"] = round(float(ret30), 3)
        s["artifact_flag"] = bool(abs(ret30) > 0.20)
        s["short_history"] = bool(len(df) < MIN_HISTORY_DAYS + 60)
        exp = expansion_stats(df)
        s["n_coil_exits"] = exp["n_coil_exits"] if exp else 0
        s["median_max10d"] = (exp["median_max10d"] if exp else np.nan)
        s["pct_with_4sigma_day"] = (
            exp["pct_with_4sigma_day"] if exp else np.nan)
        s["primed_score"] = primed_score(s)
        rows.append(s)
        time.sleep(0.05)

    scan = pd.DataFrame(rows).sort_values(
        "primed_score", ascending=False).reset_index(drop=True)
    scan.to_csv(SCAN_CSV, index=False)
    print(f"scanned {len(scan)} series ({len(failures)} failed)")
    clean = scan[~scan["artifact_flag"] & ~scan["short_history"]]
    print("\n=== top-10 primed (mid/small, all filters) ===")
    cols = ["series", "class", "primed_score", "comp_days", "rvol_pct",
            "range_pos", "ret30"]
    print(clean.head(10)[cols].to_string(index=False))
    for cls in ("sp400", "sp600"):
        sub = scan[scan["class"] == cls]
        print(f"[{cls}] n={len(sub)}  deep coils="
              f"{int((sub['comp_days'] >= 20).sum())}")
    print("\nDESCRIPTIVE ONLY. Multiplicity binds. C7 stays sealed.")


if __name__ == "__main__":
    main()
