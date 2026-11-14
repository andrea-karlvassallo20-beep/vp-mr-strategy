"""Top-500 frustration - the grievance of every deep coil on the whole board.

Continuation of the clue program (Andrea, Nov 2026): the top-500 scan found
17 clean deep coils. A coil alone is not a grievance. This pass scores each
coiled candidate's structural frustration (funding trap, OI divergence,
basis extreme - the SAME pre-declared definitions that caught FTX 12 days
early and honestly missed the exogenous Aug-2024 shock), producing the
combined WHAT ranking for the whole board: primed_score (the coil) +
frustration_score (the grievance).

Data: Binance Vision monthly fundingRate + daily metrics (OI) archives for
the candidate perps; perp closes from the top-500 scan cache; spot closes
from the Binance spot API. Where a coin has no spot pair, the perp close is
used as its own spot proxy - basis is then ZERO BY CONSTRUCTION and the
basis_extreme component is flagged as unavailable, not scored.

DESCRIPTIVE ONLY. Candidates, not claims; C7's dataset stays sealed; the
multiplicity caveat binds. The frustration score is a CLUE about the
grievance, never a direction and never a date.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from panel_frustration import _read_zip, download_candidates  # noqa: E402

RAW = Path("data/raw/panel")
from structural_inevitability import frustration_features  # noqa: E402
from top500_scan import fetch_spot_klines  # noqa: E402

CACHE = Path("data/raw/top500_klines")
OUT = Path("paper/research/clue_scan")
TABLE = OUT / "top500_frustration.csv"


def _funding_rest(symbol):
    """Funding history from the fapi REST endpoint - current, unlike the
    monthly archives which stop at the last completed month."""
    import json
    import time as _t
    import urllib.request
    CACHE.mkdir(parents=True, exist_ok=True)
    cache = CACHE / f"{symbol}_funding.csv"
    if cache.exists():
        s = pd.read_csv(cache, parse_dates=["date"])
        return pd.Series(s["rate"].values,
                         index=pd.DatetimeIndex(s["date"])).astype(float)
    out, page = [], 0
    while page < 4:
        url = ("https://fapi.binance.com/fapi/v1/fundingRate"
               f"?symbol={symbol}&limit=1000&startTime={0 if page == 0 else int(out[-1]['fundingTime']) + 1}")
        req = urllib.request.Request(url, headers={"User-Agent": "salient/1.0"})
        try:
            data = json.load(urllib.request.urlopen(req, timeout=20))
        except Exception:
            return None
        if not data:
            break
        out.extend(data)
        if len(data) < 1000:
            break
        page += 1
        _t.sleep(0.2)
    if not out:
        return None
    df = pd.DataFrame(out)
    df["fundingRate"] = df["fundingRate"].astype(float)
    df["date"] = pd.to_datetime(df["fundingTime"], unit="ms", utc=True)
    daily = df.groupby(df["date"].dt.date)["fundingRate"].mean()
    s = pd.Series(daily.values.astype(float),
                  index=pd.to_datetime(pd.Index(daily.index), utc=True))
    pd.DataFrame({"date": s.index, "rate": s.values}).to_csv(cache, index=False)
    return s


def _archive_series(symbol, sub, col, time_col, unit="ms"):
    frames = []
    for p in sorted((RAW / sub).glob(f"{symbol}-*.zip")):
        try:
            df = _read_zip(p)
        except Exception:
            continue
        df.columns = [str(c).strip().lower() for c in df.columns]
        if time_col not in df.columns or col not in df.columns:
            continue
        raw = df[time_col]
        if pd.api.types.is_numeric_dtype(raw):
            ts = pd.to_datetime(raw, unit=unit, utc=True)
        else:
            ts = pd.to_datetime(raw, utc=True, format="mixed")
            if ts.isna().all():
                ts = pd.to_datetime(raw, unit=unit, utc=True)
        frames.append(pd.DataFrame({"date": ts.dt.date, "value": df[col]}))
    if not frames:
        return None
    s = pd.concat(frames).groupby("date")["value"].last()
    return pd.Series(s.values, index=pd.to_datetime(pd.Index(s.index), utc=True))


def frame_for(symbol):
    """Structural frame built from Binance archives alone - no TVC panel
    dependency: funding (monthly), OI (daily metrics), perp close (cache),
    spot close (Binance spot API, or perp as flagged proxy)."""
    perp_f = CACHE / f"{symbol}.csv"
    if not perp_f.exists():
        return None, False
    perp = pd.read_csv(perp_f)
    perp["date"] = pd.to_datetime(perp["date"], utc=True)
    perp_s = pd.Series(perp["close"].values, index=perp["date"]).astype(float)

    funding = _funding_rest(symbol)
    oi = _archive_series(symbol, "metrics", "sum_open_interest",
                         "create_time", unit="s")
    if funding is None or oi is None:
        return None, False

    sym = symbol[:-4]  # strip USDT
    spot_df = fetch_spot_klines(sym)
    proxied = False
    if spot_df is not None and len(spot_df):
        spot_df = spot_df.copy()
        spot_df["date"] = pd.to_datetime(spot_df["date"], utc=True)
        spot_s = pd.Series(spot_df["close"].values,
                           index=spot_df["date"]).astype(float)
    else:
        spot_s = perp_s.copy()  # proxy: basis is zero by construction
        proxied = True

    df = pd.DataFrame({"spot": spot_s, "perp": perp_s,
                       "funding": funding, "oi": oi}).dropna()
    return df, proxied


def main():
    scan = pd.read_csv(OUT / "top500_scan_table.csv")
    coiled = scan[(scan["comp_days"] >= 20)
                  & (~scan["artifact_flag"])
                  & (~scan["stablecoin"])]
    perps = [s for s in coiled["series"] if not s.startswith("SPOT_")]
    spots = [s for s in coiled["series"] if s.startswith("SPOT_")]
    print(f"clean deep coils: {len(coiled)} "
          f"({len(perps)} perp, {len(spots)} spot-only - no funding/OI exist "
          f"for spot-only coins; they are flagged, not scored)")
    download_candidates(perps)
    rows = []
    for _, r in coiled.iterrows():
        sym = r["series"]
        row = {
            "series": sym, "rank": int(r["rank"]),
            "comp_days": int(r["comp_days"]),
            "primed_score": float(r["primed_score"]),
            "venue": r["venue"],
        }
        if sym.startswith("SPOT_"):
            row["note"] = "spot-only: no funding/OI market, grievance unmeasurable"
            rows.append(row)
            continue
        df, proxied = frame_for(sym)
        if df is None or len(df) < 45:
            row["note"] = "insufficient aligned perp data"
            rows.append(row)
            continue
        feat = frustration_features(df)
        if len(feat) == 0:
            row["note"] = "insufficient aligned perp data"
            rows.append(row)
            continue
        last = feat.iloc[-1]
        row.update({
            "days": len(feat),
            "funding_trap": round(float(last["funding_trap"]), 1),
            "oi_divergence": round(float(last["oi_divergence"]), 1),
            "basis_extreme": round(float(last["basis_extreme"]), 1),
            "basis_proxied": proxied,
            "frustration_score": round(float(last["frustration_score"]), 1),
            "funding_last_8h_pct": round(
                float(df["funding"].iloc[-1]) * 100, 4),
            "oi_change_30d": round(
                float(df["oi"].iloc[-1] / df["oi"].iloc[-31] - 1), 3)
                if len(df) > 30 else np.nan,
        })
        rows.append(row)
    out = pd.DataFrame(rows)
    if "frustration_score" not in out.columns:
        print("NO candidate scored")
        out.to_csv(TABLE, index=False)
        return
    scored = out[out["frustration_score"].notna()].sort_values(
        "frustration_score", ascending=False)
    unscored = out[out["frustration_score"].isna()]
    cols = ["series", "rank", "comp_days", "primed_score", "frustration_score",
            "funding_trap", "oi_divergence", "basis_extreme",
            "funding_last_8h_pct", "oi_change_30d"]
    cols = [c for c in cols if c in scored.columns]
    print("\n=== the grievance ranking (frustration score, 0-100) ===")
    print(scored[cols].to_string(index=False))
    if len(unscored):
        print("\nflagged, not hidden:")
        print(unscored[["series", "note"]].to_string(index=False))
    out.to_csv(TABLE, index=False)
    print("\nDESCRIPTIVE ONLY. The frustration score is a clue about the "
          "grievance - never a direction, never a date. C7 stays sealed.")


if __name__ == "__main__":
    main()
