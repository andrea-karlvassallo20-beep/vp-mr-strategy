"""Equities and commodities clue scan - the other half of the board.

Directive (Andrea, Nov 2026): "Go through all main commodities and
equities data for interesting clues." The crypto half of the board was
scanned (top-500, PR #87); this is the non-crypto half - the same
descriptive coil/genesis questions asked of major commodity futures,
equity indexes, and large-cap equities.

Data source (honest and flagged):
  - Yahoo Finance chart API, daily bars, ~10y lookback. Volume on these
    series is REAL exchange volume (CME/CBOT/NYSE/NASDAQ), so the TVC
    synthetic-volume flag does not apply.
  - Yahoo futures are CONTINUOUS contracts, back-adjusted by roll - the
    price level is not a tradable price, and the very earliest bars can
    carry roll distortion. The genesis question is therefore NOT asked
    of futures here (a continuous contract has no true listing date);
    it IS asked of equities, whose first trade date is real.

DESCRIPTIVE ONLY. No claim is tested; C7's dataset stays sealed; the
multiplicity caveat binds as everywhere in the dossier. The standing
question is the per-class verdict from the first clue scan: crypto coil
exits are violent (median |10d| ~9.3% on the TVC panel) and index/commodity
exits are polite (~2.1%). Does that verdict survive a wider universe?
"""

import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clue_scan import expansion_stats, primed_score, scan_series  # noqa: E402

OUT = Path("paper/research/clue_scan")
CACHE = Path("data/raw/eq_commodity_klines")
SCAN_CSV = OUT / "eq_commodity_scan_table.csv"

COMMODITIES = {
    "CL=F": "wti_crude", "BZ=F": "brent_crude", "NG=F": "natgas",
    "RB=F": "gasoline", "HO=F": "heating_oil",
    "GC=F": "gold", "SI=F": "silver", "HG=F": "copper",
    "PL=F": "platinum", "PA=F": "palladium",
    "ZW=F": "wheat", "ZC=F": "corn", "ZS=F": "soybeans", "ZM=F": "soymeal",
    "SB=F": "sugar", "KC=F": "coffee", "CC=F": "cocoa", "CT=F": "cotton",
    "LE=F": "live_cattle", "HE=F": "lean_hogs",
    "ZB=F": "tbond", "ZN=F": "tnote", "ZF=F": "tnote5y", "ZT=F": "tbill2y",
}
INDEXES = {
    "^GSPC": "sp500", "^DJI": "dow", "^IXIC": "nasdaq", "^RUT": "russell2k",
    "^VIX": "vix", "^STOXX50E": "stoxx50e", "^FTSE": "ftse100",
    "^GDAXI": "dax", "^FCHI": "cac40", "^N225": "nikkei", "^HSI": "hangseng",
    "^AXJO": "asx200", "^KS11": "kospi", "^BVSP": "bovespa",
    "^GSPE": "sp_energy", "^IXIC-2": "dummy",
}
INDEXES.pop("^IXIC-2")
EQUITIES = {
    "AAPL": "apple", "MSFT": "microsoft", "NVDA": "nvidia", "AMZN": "amazon",
    "GOOGL": "alphabet", "META": "meta", "TSLA": "tesla", "BRK-B": "berkshire",
    "JPM": "jpmorgan", "V": "visa", "XOM": "exxonmobil", "UNH": "unitedhealth",
    "JNJ": "johnsonjohnson", "WMT": "walmart", "MA": "mastercard",
    "PG": "proctergamble", "HD": "homedepot", "CVX": "chevron",
    "MRK": "merck", "ABBV": "abbvie", "KO": "cocacola", "PEP": "pepsico",
    "BAC": "bankofamerica", "COST": "costco", "AVGO": "broadcom",
    "TSM": "tsmc", "AMD": "amd", "NFLX": "netflix", "INTC": "intel",
    "BA": "boeing", "CAT": "caterpillar", "GE": "ge", "DIS": "disney",
    "GS": "goldmansachs", "MS": "morganstanley", "CSCO": "cisco",
    "ORCL": "oracle", "CRM": "salesforce", "IBM": "ibm",
}
UNIVERSE = (
    [(s, n, "commodity") for s, n in COMMODITIES.items()]
    + [(s, n, "index") for s, n in INDEXES.items()]
    + [(s, n, "equity") for s, n in EQUITIES.items()]
)


def fetch(symbol):
    """Daily bars from the Yahoo chart API, cached as CSV."""
    CACHE.mkdir(parents=True, exist_ok=True)
    cache = CACHE / f"{symbol.replace('=','_').replace('^','')}.csv"
    if cache.exists():
        df = pd.read_csv(cache)
        if len(df):
            return df
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
           f"{urllib.parse.quote(symbol)}?interval=1d&range=10y")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(3):
        try:
            data = json.load(urllib.request.urlopen(req, timeout=20))
            r = data["chart"]["result"][0]
            ts = r["timestamp"]
            q = r["indicators"]["quote"][0]
            df = pd.DataFrame({
                "date": pd.to_datetime(ts, unit="s").strftime("%Y-%m-%d"),
                "open": q["open"], "high": q["high"], "low": q["low"],
                "close": q["close"], "volume": q["volume"]})
            df = df.dropna(subset=["close"]).reset_index(drop=True)
            df.to_csv(cache, index=False)
            time.sleep(0.4)
            return df if len(df) else None
        except Exception:
            time.sleep(2)
    return None


def genesis_metrics(df):
    close = df["close"].to_numpy(float)
    g = close[:90]
    ath = close.max()
    return {
        "first_bar": df["date"].iloc[0],
        "n_days": len(close),
        "genesis_ret_90d": round(float(g[-1] / g[0] - 1.0), 3),
        "ath_in_genesis": bool(g.max() >= ath * 0.999),
        "ath_vs_now": round(float(close[-1] / ath), 3),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, genesis_rows = [], []
    failures = []
    for symbol, name, cls in UNIVERSE:
        df = fetch(symbol)
        if df is None or len(df) < 150:
            failures.append(symbol)
            continue
        s = scan_series(name, df)
        s["yahoo_symbol"] = symbol
        s["class"] = cls
        ret30 = df["close"].iloc[-1] / df["close"].iloc[-31] - 1.0
        s["ret30"] = round(float(ret30), 3)
        s["artifact_flag"] = bool(abs(ret30) > 0.20)
        exp = expansion_stats(df)
        s["n_coil_exits"] = exp["n_coil_exits"] if exp else 0
        s["median_max10d"] = (exp["median_max10d"] if exp else np.nan)
        s["pct_with_4sigma_day"] = (
            exp["pct_with_4sigma_day"] if exp else np.nan)
        s["primed_score"] = primed_score(s)
        if cls == "equity":
            g = genesis_metrics(df)
            g["series"] = name
            genesis_rows.append(g)
        rows.append(s)

    scan = pd.DataFrame(rows).sort_values(
        "primed_score", ascending=False).reset_index(drop=True)
    scan.to_csv(SCAN_CSV, index=False)
    if genesis_rows:
        gen = pd.DataFrame(genesis_rows).sort_values("first_bar").reset_index(drop=True)
        gen.to_csv(OUT / "eq_genesis.csv", index=False)

    print(f"scanned {len(scan)} series ({len(failures)} failed: {failures})")
    clean = scan[~scan["artifact_flag"]]
    print("\n=== top-10 primed candidates (artifact-filtered) ===")
    cols = ["series", "class", "primed_score", "comp_days", "rvol_pct",
            "range_pos", "vol_ratio", "ret30"]
    print(clean.head(10)[cols].to_string(index=False))
    print("\n=== per-class summary (the EW-defying question, non-crypto) ===")
    for cls in ("commodity", "index", "equity"):
        sub = scan[scan["class"] == cls]
        withexp = sub.dropna(subset=["median_max10d"])
        print(f"[{cls}] n={len(sub)}  deep coils={int((sub['comp_days'] >= 20).sum())}  "
              f"median coil-exit |10d|="
              f"{withexp['median_max10d'].median() if len(withexp) else float('nan'):.4f}  "
              f"median pct of exits with a >4-sigma day="
              f"{withexp['pct_with_4sigma_day'].median() if len(withexp) else float('nan'):.3f}")
    if genesis_rows:
        gen = pd.DataFrame(genesis_rows)
        n = len(gen)
        print(f"\n=== genesis (equities only - futures are continuous, no listing date) ===")
        print(f"n={n}; ATH still inside first 90 days: "
              f"{gen['ath_in_genesis'].mean():.1%} "
              f"(random-window null {(90 / gen['n_days']).mean():.1%})")
    print("\nDESCRIPTIVE ONLY. Multiplicity binds. C7 stays sealed.")


if __name__ == "__main__":
    main()
