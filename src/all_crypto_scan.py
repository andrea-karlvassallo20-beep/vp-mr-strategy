"""The all-crypto scan - every Binance USDT market, not just top-500 mcap.

Directive (Andrea, Nov 2026): "5000 more, whatever it is - pull
everything." The top-500 scan covered the market-cap leaders; this scan
takes the FULL Binance USDT universe: every USDT-M perpetual AND every
spot USDT pair (leveraged tokens excluded), minus the series the top-500
scan already holds. If it trades against Tether on Binance, it is on the
board.

Universe construction (honest and dated):
  - fapi exchangeInfo (all PERPETUAL/USDT/TRADING) + api/v3 exchangeInfo
    (all spot USDT pairs), snapshot date recorded in the output.
  - Leveraged tokens (UP/DOWN/BULL/BEAR) excluded: a leveraged token is
    a derivative of a derivative, not a market.
  - Series with <150 bars are skipped by scan_series (listing too recent
    for even the descriptive questions); they are counted, not hidden.

DESCRIPTIVE ONLY. The multiplicity warning is binding and worst of all
here: scanning every listed crypto market for extremes finds extremes by
construction. Nothing tests a claim; C7's dataset stays sealed.
Candidates, not evidence. The genesis filter applies: <90 days of
listing history can never be a primed candidate (the launch, not a
coil). Stablecoins are flagged by the peg (is_stablecoin) and can never
be candidates either.
"""

import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clue_scan import expansion_stats, primed_score, scan_series  # noqa: E402
from top500_scan import (  # noqa: E402
    CACHE, SCAN_CSV as TOP500_CSV, _get, _validate, fetch_klines,
    fetch_spot_klines, is_stablecoin)

OUT = Path("paper/research/clue_scan")
SCAN_CSV = OUT / "all_crypto_scan_table.csv"
UNIVERSE_CSV = OUT / "all_crypto_universe.csv"
GENESIS_MIN_DAYS = 90


def _fapi_perps():
    info = _get("https://fapi.binance.com/fapi/v1/exchangeInfo")
    return sorted(
        s["symbol"] for s in info["symbols"]
        if s["quoteAsset"] == "USDT"
        and s["contractType"] == "PERPETUAL"
        and s["status"] == "TRADING")


def _spot_pairs():
    req = urllib.request.Request(
        "https://api.binance.com/api/v3/exchangeInfo",
        headers={"User-Agent": "Mozilla/5.0"})
    info = json.load(urllib.request.urlopen(req, timeout=30))
    out = []
    for s in info["symbols"]:
        if (s["quoteAsset"] == "USDT" and s["status"] == "TRADING"
                and s.get("isSpotTradingAllowed")):
            base = s["baseAsset"]
            if any(k in base for k in ("UP", "DOWN", "BULL", "BEAR")):
                continue
            out.append(base)
    return sorted(set(out))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    snap = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    perps = _fapi_perps()
    bases = _spot_pairs()
    perp_set = {p[:-4] for p in perps}
    spot_only = [b for b in bases if b not in perp_set]
    pd.DataFrame({
        "perp": perps + [""] * len(spot_only),
        "spot_only_base": [""] * len(perps) + spot_only,
        "snapshot_date": snap,
    }).to_csv(UNIVERSE_CSV, index=False)
    print(f"universe: {len(perps)} perps + {len(spot_only)} spot-only "
          f"({snap})")

    already = set()
    if TOP500_CSV.exists():
        already = set(pd.read_csv(TOP500_CSV)["series"])
    print(f"already on the board from the top-500 scan: {len(already)}")

    rows, failures, skipped_short = [], [], 0

    def _scan(sym, df, venue):
        nonlocal skipped_short
        if df is None or len(df) < 150:
            skipped_short += 1 if df is not None else 0
            if df is None:
                failures.append(sym)
            return
        s = scan_series(sym, df)
        s["class"] = "crypto"
        s["venue"] = venue
        ret30 = df["close"].iloc[-1] / df["close"].iloc[-31] - 1.0
        s["ret30"] = round(float(ret30), 3)
        s["artifact_flag"] = bool(abs(ret30) > 0.20)
        s["stablecoin"] = bool(is_stablecoin(df["close"]))
        s["genesis_flag"] = bool(len(df) < GENESIS_MIN_DAYS)
        s["data_file"] = str(CACHE / f"{sym}.csv")
        exp = expansion_stats(df)
        s["n_coil_exits"] = exp["n_coil_exits"] if exp else 0
        s["median_max10d"] = (exp["median_max10d"] if exp else np.nan)
        s["pct_with_4sigma_day"] = (
            exp["pct_with_4sigma_day"] if exp else np.nan)
        s["primed_score"] = primed_score(s)
        rows.append(s)

    for p in perps:
        if p in already:
            continue
        _scan(p, fetch_klines(p), "perp")
    for b in spot_only:
        sym = f"SPOT_{b}USDT"
        if sym in already:
            continue
        _scan(sym, fetch_spot_klines(b), "spot")

    scan = pd.DataFrame(rows).sort_values(
        "primed_score", ascending=False).reset_index(drop=True)
    scan.to_csv(SCAN_CSV, index=False)
    print(f"scanned {len(scan)} new series "
          f"({len(failures)} fetch failures, {skipped_short} <150d skipped)")
    clean = scan[~scan["artifact_flag"] & ~scan["stablecoin"]
                 & ~scan["genesis_flag"]]
    print("\n=== top-10 primed candidates (all filters) ===")
    cols = ["series", "primed_score", "comp_days", "rvol_pct",
            "range_pos", "ret30"]
    print(clean.head(10)[cols].to_string(index=False))
    print(f"\nstablecoins flagged: {int(scan['stablecoin'].sum())}  "
          f"genesis-flagged: {int(scan['genesis_flag'].sum())}")
    print("\nDESCRIPTIVE ONLY. Multiplicity binds. C7 stays sealed.")


if __name__ == "__main__":
    main()
