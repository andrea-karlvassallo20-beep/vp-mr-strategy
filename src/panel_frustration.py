"""Panel frustration — the grievance of every coiled candidate.

Continuation of the clue program: the deep-coil candidates (from
clue_scan_table.csv) get their structural frustration scored (funding trap,
OI divergence, basis extreme — the same pre-declared definitions as
structural_inevitability.py), producing the combined WHAT ranking:
primed_score (the coil) + frustration_score (the grievance).

Data: last ~130 days of Binance daily metrics (OI, long/short ratios) +
monthly funding + monthly perp klines for the candidate symbols. Free
public archives. DESRIPTIVE ONLY: candidates, not claims; C7's kill lines
remain unfaced.
"""

import io
import sys
import urllib.request
import zipfile

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from structural_inevitability import frustration_features  # noqa: E402

RAW = Path("data/raw/panel")
Z30 = 30


def _fetch(url, dst):
    dst = Path(dst)
    if dst.exists():
        return "skip"
    try:
        urllib.request.urlretrieve(url, dst)
        return "ok"
    except Exception:
        return "fail"


def download_candidates(symbols, days=130):
    (RAW / "metrics").mkdir(parents=True, exist_ok=True)
    (RAW / "funding").mkdir(parents=True, exist_ok=True)
    (RAW / "klines").mkdir(parents=True, exist_ok=True)
    base = "https://data.binance.vision/data/futures/um"
    dates = pd.date_range(end=pd.Timestamp.now(tz="UTC").normalize()
                          - pd.Timedelta(days=1), periods=days, freq="D")
    jobs = []
    for s in symbols:
        for d in dates:
            ds = d.strftime("%Y-%m-%d")
            jobs.append((f"{base}/daily/metrics/{s}/{s}-metrics-{ds}.zip",
                         RAW / "metrics" / f"{s}-metrics-{ds}.zip"))
        for m in pd.date_range(end=dates[-1], periods=5, freq="MS"):
            ms = m.strftime("%Y-%m")
            jobs.append((f"{base}/monthly/fundingRate/{s}/{s}-fundingRate-{ms}.zip",
                         RAW / "funding" / f"{s}-fundingRate-{ms}.zip"))
            jobs.append((f"{base}/monthly/klines/{s}/1d/{s}-1d-{ms}.zip",
                         RAW / "klines" / f"{s}-1d-{ms}.zip"))
    with ThreadPoolExecutor(max_workers=12) as ex:
        res = list(ex.map(lambda j: _fetch(*j), jobs))
    ok = sum(1 for r in res if r in ("ok", "skip"))
    print(f"panel archive: {ok} of {len(jobs)} files present/downloaded")


def _read_zip(path):
    with zipfile.ZipFile(path) as zf:
        name = [n for n in zf.namelist() if n.lower().endswith(".csv")][0]
        head = zf.read(name)[:200].decode("utf-8", errors="replace")
        has_header = any(k in head.lower() for k in
                         ("price", "calc_time", "create_time", "open_time"))
        return pd.read_csv(io.BytesIO(zf.read(name)),
                           header=0 if has_header else None)


def series_for(symbol):
    """Daily funding, OI, perp close, spot close for one symbol."""
    tvc = symbol.lower().replace("usdt", "usd")
    spot_f = Path("paper/research/data") / f"{tvc}.csv"
    if not spot_f.exists():
        return None
    spot = pd.read_csv(spot_f)
    spot["date"] = pd.to_datetime(spot["date"], utc=True)
    s = pd.Series(spot["close"].values, index=spot["date"])

    fund_rows, oi_rows, perp_rows = [], [], []
    for p in sorted((RAW / "funding").glob(f"{symbol}-fundingRate-*.zip")):
        df = _read_zip(p)
        df.columns = [str(c).strip().lower() for c in df.columns]
        if "calc_time" not in df.columns:
            continue
        ts = pd.to_datetime(df["calc_time"], unit="ms", utc=True)
        fund_rows.append(pd.DataFrame({"date": ts.dt.date,
                                        "rate": df["last_funding_rate"]}))
    for p in sorted((RAW / "metrics").glob(f"{symbol}-metrics-*.zip")):
        df = _read_zip(p)
        df.columns = [str(c).strip().lower() for c in df.columns]
        if "create_time" not in df.columns:
            continue
        ts = pd.to_datetime(df["create_time"], utc=True, format="mixed")
        oi_rows.append(pd.DataFrame({"date": ts.dt.date,
                                     "oi": df["sum_open_interest"]}))
    for p in sorted((RAW / "klines").glob(f"{symbol}-1d-*.zip")):
        df = _read_zip(p)
        ts = pd.to_datetime(df.iloc[:, 0], unit="ms", utc=True)
        perp_rows.append(pd.DataFrame({"date": ts.dt.date,
                                        "close": df.iloc[:, 4]}))
    if not (fund_rows and oi_rows and perp_rows):
        return None
    f = pd.concat(fund_rows).groupby("date")["rate"].mean()
    o = pd.concat(oi_rows).groupby("date")["oi"].last()
    k = pd.concat(perp_rows).groupby("date")["close"].last()

    def _ix(x):
        return pd.Series(x.values, index=pd.to_datetime(pd.Index(x.index), utc=True))

    df = pd.DataFrame({"spot": s, "perp": _ix(k), "funding": _ix(f),
                       "oi": _ix(o)}).dropna()
    return df if len(df) >= 45 else None


def main():
    scan = pd.read_csv("paper/research/clue_scan/clue_scan_table.csv")
    coiled = scan[(scan["class"] == "crypto") & (scan["comp_days"] >= 20)]
    # TVC USD pair -> Binance USDT-M perp symbol (1000X-prefixed tickers
    # where Binance uses them; candidates with no perp are flagged, not
    # hidden)
    symbols = [r.replace("usd", "usdt").upper() for r in coiled["series"]]
    print(f"scoring frustration for {len(symbols)} coiled candidates")
    download_candidates(symbols)
    rows = []
    for sym in symbols:
        df = series_for(sym)
        if df is None:
            rows.append({"symbol": sym, "note": "insufficient perp data"})
            continue
        feat = frustration_features(df)
        last = feat.iloc[-1]
        coil = coiled[coiled["series"] == sym.lower().replace("usdt", "usd")]
        rows.append({
            "symbol": sym,
            "days": len(feat),
            "funding_trap": round(float(last["funding_trap"]), 1),
            "oi_divergence": round(float(last["oi_divergence"]), 1),
            "basis_extreme": round(float(last["basis_extreme"]), 1),
            "frustration_score": round(float(last["frustration_score"]), 1),
            "comp_days": int(coil["comp_days"].iloc[0]) if len(coil) else 0,
            "primed_score": float(coil["primed_score"].iloc[0]) if len(coil) else np.nan,
            "funding_last": round(float(df["funding"].iloc[-1]) * 100, 4),
            "oi_change_30d": round(float(df["oi"].iloc[-1] / df["oi"].iloc[-31] - 1), 3)
                             if len(df) > 30 else np.nan,
        })
    out = pd.DataFrame(rows)
    Path("paper/research/clue_scan").mkdir(exist_ok=True)
    if "frustration_score" not in out.columns:
        print("NO candidate had sufficient perp data — nothing scored")
        out.to_csv("paper/research/clue_scan/panel_frustration.csv", index=False)
        return
    scored = out[out["frustration_score"].notna()].sort_values(
        "frustration_score", ascending=False).reset_index(drop=True)
    unscored = out[out["frustration_score"].isna()]
    print(scored.to_string(index=False))
    if len(unscored):
        print("\nno Binance perp data (TVC-only candidates, flagged not hidden):")
        print(unscored[["symbol", "note"]].to_string(index=False))
    scored.to_csv("paper/research/clue_scan/panel_frustration.csv", index=False)


if __name__ == "__main__":
    main()
