"""Mega-universe dormancy scan: pull EVERYTHING the free sources expose.

Universe (all venues, all classes, no curation):
  - ALL Binance USDS-M perpetual USDT pairs (fapi exchangeInfo, TRADING)
  - ALL Binance spot USDT pairs (api exchangeInfo, TRADING)
  - S&P 500 constituents (Wikipedia table, Yahoo klines)
  - Extended world indexes, commodities, and major ETFs (Yahoo)
  - CoinGecko top-500 coins not on Binance, via Yahoo "{SYM}-USD" tickers

Per series: the same causal metrics as the board (scan_series from
clue_scan: comp_days, rvol_pct, range_pos) plus days since the last
>=4-sigma day. Stablecoins are detected by price behavior and excluded.

DESCRIPTIVE ONLY. Multiplicity caveat binding at this scale: scanning
thousands of series finds silence by construction. No claims tested, no
edge claimed, the 0.505 direction boundary remains in force.
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from clue_scan import scan_series  # noqa: E402
from top500_scan import (  # noqa: E402
    _get, _validate, fetch_klines, fetch_spot_klines, is_stablecoin,
)
from eq_commodity_scan import fetch as yahoo_fetch  # noqa: E402

CLUE = ROOT / "paper/research/clue_scan"
MEGA_CACHE = ROOT / "data/raw/mega_klines"

# Extended Yahoo universe: world indexes, commodities, major ETFs.
EXTRA_YAHOO = [
    # world indexes
    "^GSPC", "^DJI", "^IXIC", "^RUT", "^VIX", "^STOXX50E", "^FTSE",
    "^GDAXI", "^FCHI", "^N225", "^HSI", "^AXJO", "^KS11", "^BVSP",
    "^NSEI", "^BSESN", "^TA125.TA", "^TASI.SR", "^JNJO.JO", "^MXX",
    "^GSPTSE", "^MERV", "^IPSAX", "^ATX", "^BFX", "^AEX", "^OMXC20",
    "^OMXSTOPI", "^FTSEMIB.MI", "^IBEX", "^PSI20", "^WIG20.WA",
    "^BIST", "^XU100.IS", "^RTS.RS", "^UAUX", "^CASE30.CA",
    "^NZ50", "^SSMI", "^DSEX", "^SET.BK", "^JKSE", "^PSEI.PS",
    "^TWII", "^STI.SI", "^KLSE", "^VNI", "^IPSA.CL", "^SPMerval",
    # commodities
    "ZW=F", "ZC=F", "ZS=F", "ZO=F", "ZR=F", "ZM=F", "ZL=F", "CT=F",
    "SB=F", "KC=F", "CC=F", "OJ=F", "LE=F", "HE=F", "GF=F", "CL=F",
    "BZ=F", "NG=F", "HO=F", "RB=F", "GC=F", "SI=F", "HG=F", "PL=F",
    "PA=F", "SIH25.F", "HGK25.CME", "ALI=F", "ZN=F", "ZB=F", "ZF=F",
    "ZT=F", "UB=F", "6E=F", "6J=F", "6B=F", "6A=F", "6C=F", "6S=F",
    "DX-Y.NYB", "10Y-MM", "ES=F", "NQ=F", "RTY=F", "YM=F",
    # major ETFs / sectors
    "SPY", "QQQ", "IWM", "DIA", "VTI", "VOO", "EFA", "EEM", "VWO",
    "AGG", "TLT", "IEF", "LQD", "HYG", "TIP", "GLD", "SLV", "GDX",
    "USO", "UNG", "DBC", "XLF", "XLE", "XLK", "XLV", "XLY", "XLP",
    "XLI", "XLB", "XLRE", "XLU", "XLC", "SMH", "SOXX", "IBIT", "FBTC",
    "ARKK", "VNQ", "REM", "EWJ", "FXI", "INDA", "EWZ", "EWW", "EWT",
]


def _days_since_4sigma(df, min_hist=90):
    c = pd.to_numeric(df["close"], errors="coerce").dropna()
    if len(c) < min_hist:
        return None
    ret = c.pct_change()
    sigma = ret.rolling(60).std()
    big = (ret.abs() >= 4.0 * sigma).fillna(False)
    ago = int(len(c) - 1 - big.values.nonzero()[0][-1]) if big.any() else int(len(c) - 1)
    return {"n_hist": int(len(c)), "last_4sigma_days_ago": ago}


def _row(series, cls, df, venue):
    if df is None or len(df) < 90:
        return None
    s = scan_series(series, df)
    k = _days_since_4sigma(df)
    if k is None:
        return None
    return {
        "series": series, "class": cls, "venue": venue,
        "n_days": s["n_days"], "comp_days": s["comp_days"],
        "rvol_pct": s["rvol_pct"], "range_pos": s["range_pos"],
        "stretch_z": s["stretch_z"], "ret30": df["close"].iloc[-1] /
        df["close"].iloc[-31] - 1.0 if len(df) > 31 else np.nan,
        "last_4sigma_days_ago": k["last_4sigma_days_ago"],
        "primed": bool(s["comp_days"] >= 20 and s["rvol_pct"] <= 33
                       and s["range_pos"] <= 0.35),
    }


def binance_universe():
    perp = _get("https://fapi.binance.com/fapi/v1/exchangeInfo")
    spot = _get("https://api.binance.com/api/v3/exchangeInfo")
    ps = [s["symbol"] for s in perp["symbols"]
          if s["status"] == "TRADING" and s["quoteAsset"] == "USDT"
          and s.get("contractType") == "PERPETUAL"]
    ss = [s["symbol"] for s in spot["symbols"]
          if s["status"] == "TRADING" and s["quoteAsset"] == "USDT"]
    perp_set = set(ps)
    spot_only = [s for s in ss if s not in perp_set]
    return ps, spot_only


def sp500_tickers():
    """S&P 500 constituents from the Wikipedia table."""
    url = ("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        tables = pd.read_html(urllib.request.urlopen(req, timeout=30))
        df = tables[0]
        syms = df["Symbol"].astype(str).tolist()
        return [s.replace(".", "-") for s in syms]
    except Exception as e:
        print(f"[warn] S&P 500 table fetch failed: {e}")
        return []


def coingecko_symbols():
    """Top-500 CoinGecko symbols (uppercased), for Yahoo -USD tickers."""
    out = []
    try:
        for page in range(1, 5):
            data = _get("https://api.coingecko.com/api/v3/coins/markets"
                        f"?vs_currency=usd&order=market_cap_desc"
                        f"&per_page=100&page={page}")
            if not data:
                break
            out.extend(d["symbol"].upper() for d in data)
            time.sleep(1.2)
    except Exception as e:
        print(f"[warn] coingecko fetch failed: {e}")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path,
                    default=CLUE / "mega_dormancy_table.csv")
    ap.add_argument("--skip-sp500", action="store_true")
    args = ap.parse_args(argv)

    MEGA_CACHE.mkdir(parents=True, exist_ok=True)
    rows = []

    # 1) ALL Binance perps + spot-only pairs
    perps, spot_only = binance_universe()
    print(f"universe: {len(perps)} perps + {len(spot_only)} spot-only pairs")
    for i, p in enumerate(perps):
        df = fetch_klines(p)
        if df is None:
            continue
        close = df["close"].astype(float)
        if is_stablecoin(close):
            continue
        r = _row(p, "crypto", df, "perp")
        if r:
            r["n_days"] = len(df)
            rows.append(r)
        if i % 100 == 0:
            print(f"  perps {i}/{len(perps)}")
    for i, s in enumerate(spot_only):
        df = fetch_spot_klines(s.replace("USDT", ""))
        if df is None:
            continue
        close = df["close"].astype(float)
        if is_stablecoin(close):
            continue
        r = _row(f"SPOT_{s}", "crypto", df, "spot")
        if r:
            r["n_days"] = len(df)
            rows.append(r)
        if i % 100 == 0:
            print(f"  spot {i}/{len(spot_only)}")

    # 2) Yahoo: extras + S&P 500 + CoinGecko-via-Yahoo
    def _cls(s):
        if s.endswith("=F") or s.endswith(".CME"):
            return "commodity"
        if s.startswith("^") or s in ("DX-Y.NYB", "10Y-MM"):
            return "index"
        return "etf"
    yahoo_syms = [(s, s, _cls(s)) for s in EXTRA_YAHOO]
    if not args.skip_sp500:
        for t in sp500_tickers():
            yahoo_syms.append((t, t, "equity"))
        # CoinGecko coins not on Binance, via Yahoo -USD tickers
        binance_base = {p[:-4] for p in perps} | {s[:-4] for s in spot_only}
        for sym in coingecko_symbols():
            if sym and sym not in binance_base and len(sym) <= 10:
                yahoo_syms.append((f"{sym}-USD", f"CG_{sym}", "crypto"))
    print(f"yahoo universe: {len(yahoo_syms)} tickers")
    for i, (ysym, name, cls) in enumerate(yahoo_syms):
        cache = MEGA_CACHE / f"{ysym.replace('=','_').replace('^','')}.csv"
        if cache.exists():
            df = pd.read_csv(cache)
        else:
            url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
                   f"{urllib.parse.quote(ysym)}?interval=1d&range=10y")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            try:
                data = json.load(urllib.request.urlopen(req, timeout=20))
                r_ = data["chart"]["result"][0]
                q = r_["indicators"]["quote"][0]
                df = pd.DataFrame({
                    "date": pd.to_datetime(r_["timestamp"], unit="s").strftime("%Y-%m-%d"),
                    "close": q["close"], "volume": q["volume"]})
                df = df.dropna(subset=["close"]).reset_index(drop=True)
                df.to_csv(cache, index=False)
                time.sleep(0.35)
            except Exception:
                continue
        if df is None or len(df) < 90:
            continue
        close = df["close"].astype(float)
        if cls == "crypto" and is_stablecoin(close):
            continue
        r = _row(name, cls, df, "yahoo")
        if r:
            r["n_days"] = len(df)
            rows.append(r)
        if i % 100 == 0:
            print(f"  yahoo {i}/{len(yahoo_syms)}")

    out = pd.DataFrame(rows)
    out["dormancy_score"] = (
        np.log1p(out["last_4sigma_days_ago"].clip(lower=0)) * 0.5
        + np.log1p(out["comp_days"].clip(lower=0)) * 0.3
        + (1.0 - out["rvol_pct"] / 100.0) * 0.2
    )
    out = out.sort_values("dormancy_score", ascending=False).reset_index(drop=True)
    out.to_csv(args.out, index=False)
    print(f"mega dormancy table: {len(out)} series -> {args.out}")
    print(out["class"].value_counts().to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
