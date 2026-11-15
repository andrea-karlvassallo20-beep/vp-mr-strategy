"""The global scan - the rest of the world joins the board.

Directive (Andrea, Nov 2026): "EVERYTHING, I mean EVERYTHING - we don't
care if it's Iranian indexes after war, or whatever; there is a lesson
in all." The board already held US commodities/indexes, the S&P 500 and
top-500 crypto; this scan adds the rest of the world: world indexes
(frontier and war-adjacent included), FX (majors, EM, and the Iranian
rial - the post-war lesson Yahoo actually carries; the Tehran equity
index itself is NOT on Yahoo, and that absence is recorded, not hidden),
US rates and the volatility complex, and non-US mega-cap equities.

Data source (honest and flagged):
  - Yahoo Finance chart API via eq_commodity_scan.fetch (shared CSV
    cache, ~10y lookback). FX series carry NO meaningful volume on
    Yahoo: evr and vol_ratio are meaningless for the fx class and are
    read as such. Rates (^TNX) are yields, not prices; the coil logic
    still applies to their level series.
  - FX series of chronic devaluers (TRY, ARS, NGN, EGP...) will trip the
    artifact flag (|30d| > 20%) after devaluation events - that is the
    flag working, not failing: a devaluation IS the move-already-happened
    state.

DESCRIPTIVE ONLY. No claim is tested; C7's dataset stays sealed; the
multiplicity caveat binds as everywhere. Candidates, not evidence.
"""

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clue_scan import expansion_stats, primed_score, scan_series  # noqa: E402
from eq_commodity_scan import fetch  # noqa: E402

OUT = Path("paper/research/clue_scan")
SCAN_CSV = OUT / "global_scan_table.csv"
GENESIS_MIN_DAYS = 90

# Symbols already covered by eq_commodity_scan (kospi, asx200, bovespa,
# nikkei, hangseng etc.) are NOT repeated here - one series, one tile.
WORLD_INDEXES = {
    "^TA125.TA": "telaviv125", "^MXX": "ipc_mexico", "^TWII": "taiwan",
    "^JKSE": "jakarta", "^NSEI": "nifty50", "^BSESN": "sensex",
    "^STI": "straits_times", "^JN0U.JO": "jse_top40", "^GSPTSE": "tsx_comp",
    "^IBEX": "ibex35", "^AEX": "aex", "^SSMI": "swiss_mkt",
    "^N100": "euronext100", "^FTMC": "ftse250", "^FTAS": "ftse_allshare",
    "^NZ50": "nz50", "^BFX": "bel20", "^OMX": "omx_stockholm",
    "^ATX": "atx_vienna", "^ISEQ": "iseq_irish", "^NDX": "nasdaq100",
    "^SOX": "sox", "^VIX3M": "vix3m", "^GVZ": "gold_vix", "^OVX": "oil_vix",
}
RATES = {
    "^TNX": "ust10y_yield", "^FVX": "ust5y_yield", "^TYX": "ust30y_yield",
}
FX = {
    "DX-Y.NYB": "dollar_index", "EURUSD=X": "eurusd", "USDJPY=X": "usdjpy",
    "GBPUSD=X": "gbpusd", "AUDUSD=X": "audusd", "NZDUSD=X": "nzdusd",
    "USDCHF=X": "usdchf", "USDCAD=X": "usdcad", "EURGBP=X": "eurgbp",
    "USDCNH=X": "usdcnh", "USDMXN=X": "usdmxn", "USDBRL=X": "usdbrl",
    "USDZAR=X": "usdzar", "USDTRY=X": "usdtry", "USDKRW=X": "usdkrw",
    "USDINR=X": "usdinr", "USDRUB=X": "usdrub", "USDIRR=X": "usdirr_rial",
    "USDCOP=X": "usdcop", "USDARS=X": "usdars", "USDNGN=X": "usdngn",
    "USDPKR=X": "usdpkr", "USDBDT=X": "usdbdt", "USDEGP=X": "usdegp",
    "USDVND=X": "usdvnd", "USDTHB=X": "usdthb", "USDPHP=X": "usdphp",
    "IDR=X": "usdidr", "CLP=X": "usdclp", "PEN=X": "usdpen",
    "USDILS=X": "usdils",
}
GLOBAL_EQUITIES = {
    "ASML": "asml", "SAP.DE": "sap", "SHEL": "shell", "UL": "unilever",
    "TM": "toyota", "NESN.SW": "nestle", "HSBC": "hsbc", "RY.TO": "rbc",
    "CNQ": "canadian_natural", "BHP": "bhp", "RIO": "rio_tinto",
    "7203.T": "toyota_jp", "005930.KS": "samsung_elec", "TCEHY": "tencent",
    "NSRGY": "danone", "MC.PA": "lvmh", "OR.PA": "loreal",
    "SIE.DE": "siemens", "AZN": "astrazeneca", "BRK-B": "berkshire_dup",
}
GLOBAL_EQUITIES.pop("BRK-B")  # already on the board via the S&P 500 scan

UNIVERSE = (
    [(s, n, "world_index") for s, n in WORLD_INDEXES.items()]
    + [(s, n, "rate") for s, n in RATES.items()]
    + [(s, n, "fx") for s, n in FX.items()]
    + [(s, n, "global_equity") for s, n in GLOBAL_EQUITIES.items()]
)

# Probed 2026-11-15 and NOT carried by Yahoo - recorded, not hidden.
NOT_ON_YAHOO = [
    "^TEDPIX (Tehran TEDPIX)", "^TASI (Saudi)", "^DFMGI (Dubai)",
    "^MERVAL (Argentina)", "^IPSA (Chile)", "^CASE30 (Egypt, 1 bar only)",
    "^WIG20 (Warsaw)", "^BUX (Budapest)", "^PX (Prague)",
    "^XU100 (Istanbul)", "^SET.BK (Thailand, 1 bar only)",
    "^PSEI (Manila)", "^COLCAP (Colombia)", "^MSM30 (Oman)",
    "^QSI (Qatar)",
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, failures = [], []
    for symbol, name, cls in UNIVERSE:
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
        exp = expansion_stats(df)
        s["n_coil_exits"] = exp["n_coil_exits"] if exp else 0
        s["median_max10d"] = (exp["median_max10d"] if exp else np.nan)
        s["pct_with_4sigma_day"] = (
            exp["pct_with_4sigma_day"] if exp else np.nan)
        s["primed_score"] = primed_score(s)
        if cls == "fx":
            # FX carries no volume on Yahoo: evr/vol_ratio are noise,
            # and chronic devaluers trip the artifact flag honestly.
            s["evr_m"] = np.nan
            s["vol_ratio"] = np.nan
        rows.append(s)
        time.sleep(0.05)

    scan = pd.DataFrame(rows).sort_values(
        "primed_score", ascending=False).reset_index(drop=True)
    scan.to_csv(SCAN_CSV, index=False)
    with (OUT / "global_scan.meta.txt").open("w") as f:
        f.write(
            f"scanned {len(scan)} of {len(UNIVERSE)} global series "
            f"({len(failures)} failed: {failures}); Yahoo carries no "
            f"volume for fx (evr/vol_ratio read as missing for fx); "
            "probed and NOT carried by Yahoo, recorded not hidden: "
            f"{NOT_ON_YAHOO}; DESCRIPTIVE ONLY - multiplicity binds, "
            "C7 stays sealed.\n")

    print(f"scanned {len(scan)} series ({len(failures)} failed: {failures})")
    print(f"\nNOT on Yahoo (recorded, not hidden): {NOT_ON_YAHOO}")
    print("\n=== top-10 primed (global) ===")
    cols = ["series", "class", "primed_score", "comp_days", "rvol_pct",
            "range_pos", "ret30"]
    print(scan.head(10)[cols].to_string(index=False))
    print("\n=== per-class summary ===")
    for cls in ("world_index", "rate", "fx", "global_equity"):
        sub = scan[scan["class"] == cls]
        print(f"[{cls}] n={len(sub)}  deep coils="
              f"{int((sub['comp_days'] >= 20).sum())}  "
              f"artifact-flagged={int(sub['artifact_flag'].sum())}")
    print("\nDESCRIPTIVE ONLY. Multiplicity binds. C7 stays sealed.")


if __name__ == "__main__":
    main()
