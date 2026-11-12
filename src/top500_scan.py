"""Top-500 clue scan - the whole board, not just the TVC panel.

Directive (Andrea, Nov 2026): "Scan through the top 500 crypto for
interesting clues." The TVC panel held ~160 pairs; this scan extends the
descriptive clue program to the top 500 crypto assets by market cap.

Universe construction (honest and dated):
  - CoinGecko /coins/markets, top 500 by market cap, 2 pages of 250,
    snapshot date recorded in the output. The list is a SNAPSHOT, not a
    permanent truth: ranks move, the scan reports the date it looked.
  - Mapped to Binance USDT-M perpetuals via fapi exchangeInfo. A coin
    with no Binance perp is reported as unmapped - it is NOT silently
    dropped from the universe file.

Data advantage over the TVC panel: Binance perp daily klines carry REAL
venue volume (TVC-contracted pairs carry synthetic volume). vol_ratio
and effort-vs-result are therefore meaningful here without the synthetic
caveat - but the caveat is replaced by another: perp volume includes
wash-prone venues' own noise, and the klines start at the perp listing,
not the spot genesis.

DESCRIPTIVE ONLY. The multiplicity warning is binding and worse here than
on the 160-pair panel: scanning 500 series for extremes finds extremes by
construction. Nothing in this file tests a claim; C7's dataset is sealed
and this scan does not touch it. Candidates, not evidence.
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

OUT = Path("paper/research/clue_scan")
CACHE = Path("data/raw/top500_klines")
UNIVERSE_CSV = OUT / "top500_universe.csv"
SCAN_CSV = OUT / "top500_scan_table.csv"
GENESIS_CSV = OUT / "top500_genesis.csv"


def _get(url, retries=2):
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "salient-research/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception:
            if attempt == retries:
                return None
            time.sleep(1.5)
    return None


def fetch_universe():
    """Top 500 by market cap (CoinGecko snapshot) mapped to Binance USDT perps."""
    coins = []
    for page in (1, 2):
        data = _get(
            "https://api.coingecko.com/api/v3/coins/markets"
            f"?vs_currency=usd&order=market_cap_desc&per_page=250&page={page}"
        )
        if not data:
            raise SystemExit(f"could not fetch CoinGecko page {page}")
        coins.extend(data)
        time.sleep(1.2)
    info = _get("https://fapi.binance.com/fapi/v1/exchangeInfo")
    perps = {
        s["symbol"]
        for s in info["symbols"]
        if s["quoteAsset"] == "USDT"
        and s["contractType"] == "PERPETUAL"
        and s["status"] == "TRADING"
    }
    snapshot = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    seen = set()
    rows = []
    for rank, c in enumerate(coins[:500], start=1):
        sym = c["symbol"].upper()
        perp = f"{sym}USDT"
        if sym in seen:
            # symbol collision: highest-cap coin already owns this ticker
            rows.append({"rank": rank, "coingecko_id": c["id"], "symbol": sym,
                         "binance_perp": "", "mapped": False,
                         "collision": True})
            continue
        seen.add(sym)
        mapped = perp in perps
        rows.append({"rank": rank, "coingecko_id": c["id"], "symbol": sym,
                     "binance_perp": perp if mapped else "",
                     "mapped": mapped, "collision": False})
    return pd.DataFrame(rows), snapshot


def fetch_klines(perp):
    """Daily klines from Binance futures REST, cached as CSV."""
    CACHE.mkdir(parents=True, exist_ok=True)
    cache = CACHE / f"{perp}.csv"
    if cache.exists():
        return pd.read_csv(cache)
    data = _get(
        "https://fapi.binance.com/fapi/v1/klines"
        f"?symbol={perp}&interval=1d&limit=1000"
    )
    if not data:
        return None
    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "qv", "n", "tbb", "tbq", "ig"])
    df["date"] = pd.to_datetime(df["open_time"], unit="ms").dt.strftime("%Y-%m-%d")
    df = df[["date", "open", "high", "low", "close", "volume"]].astype(
        {"open": float, "high": float, "low": float, "close": float, "volume": float})
    df.to_csv(cache, index=False)
    time.sleep(0.15)
    return df


def genesis_metrics(df):
    """Binance first bar IS the perp listing date - true genesis data,
    unlike the TVC panel's shared export window."""
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
    if UNIVERSE_CSV.exists():
        uni = pd.read_csv(UNIVERSE_CSV)
        snapshot = str(pd.read_csv(UNIVERSE_CSV).attrs.get(
            "snapshot", "")) or None
    else:
        uni, snapshot = fetch_universe()
        uni.to_csv(UNIVERSE_CSV, index=False)
    (OUT / "top500_universe.meta.txt").write_text(
        f"coingecko top-500 snapshot date: {snapshot}\n")
    mapped = uni[uni["mapped"] == True]  # noqa: E712
    print(f"universe: top 500 by cap (snapshot {snapshot}); "
          f"{len(mapped)} mapped to Binance USDT-M perps, "
          f"{500 - len(mapped)} unmapped "
          f"({int(uni['collision'].sum())} symbol collisions)")

    rows, genesis_rows = [], []
    failures = []
    for _, r in mapped.iterrows():
        perp = r["binance_perp"]
        df = fetch_klines(perp)
        if df is None or len(df) < 150:
            failures.append(perp)
            continue
        s = scan_series(perp, df)
        s["rank"] = int(r["rank"])
        s["coingecko_id"] = r["coingecko_id"]
        ret30 = df["close"].iloc[-1] / df["close"].iloc[-31] - 1.0
        s["ret30"] = round(float(ret30), 3)
        s["artifact_flag"] = bool(abs(ret30) > 0.20)
        exp = expansion_stats(df)
        s["n_coil_exits"] = exp["n_coil_exits"] if exp else 0
        s["median_max10d"] = (exp["median_max10d"] if exp else np.nan)
        s["pct_with_4sigma_day"] = (
            exp["pct_with_4sigma_day"] if exp else np.nan)
        s["primed_score"] = primed_score(s)
        g = genesis_metrics(df)
        g["pair"] = perp
        g["rank"] = int(r["rank"])
        genesis_rows.append(g)
        rows.append(s)

    scan = pd.DataFrame(rows).sort_values(
        "primed_score", ascending=False).reset_index(drop=True)
    scan.to_csv(SCAN_CSV, index=False)
    gen = pd.DataFrame(genesis_rows).sort_values("first_bar").reset_index(drop=True)
    gen.to_csv(GENESIS_CSV, index=False)

    print(f"scanned {len(scan)} perps ({len(failures)} failed/short history)")
    clean = scan[~scan["artifact_flag"]]
    print("\n=== top-12 primed candidates (artifact-filtered) ===")
    cols = ["binance_perp" if False else "series", "rank", "primed_score",
            "comp_days", "rvol_pct", "range_pos", "vol_ratio", "ret30"]
    print(clean.head(12)[cols].to_string(index=False))
    deep = clean[clean["comp_days"] >= 20]
    print(f"\ndeep coils (comp_days >= 20, artifact-filtered): "
          f"{len(deep)} of {len(clean)}")
    withexp = clean.dropna(subset=["median_max10d"])
    if len(withexp):
        print(f"median coil-exit |10d| move across the universe: "
              f"{withexp['median_max10d'].median():.4f}; "
              f"median pct of exits with a >4-sigma day: "
              f"{withexp['pct_with_4sigma_day'].median():.3f}")
    n = len(gen)
    if n:
        ath_rate = gen["ath_in_genesis"].mean()
        nulls = (90 / gen["n_days"]).mean()
        print(f"\n=== genesis (true listing dates from Binance) ===")
        print(f"n={n} perps; ATH still inside first 90 days: {ath_rate:.1%} "
              f"(random-window null {nulls:.1%})")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        assets = Path("docs/assets")
        assets.mkdir(exist_ok=True)
        for _, r in clean.head(6).iterrows():
            perp = r["series"]
            df = pd.read_csv(CACHE / f"{perp}.csv")
            fig, (ax1, ax2) = plt.subplots(
                2, 1, figsize=(10, 6), sharex=True,
                gridspec_kw={"height_ratios": [3, 1]})
            x = pd.to_datetime(df["date"])
            ax1.plot(x, df["close"], lw=0.9, color="#22d3ee")
            ax1.set_title(
                f"{perp} (cap rank {int(r['rank'])}) - primed_score "
                f"{r['primed_score']} (comp_days {r['comp_days']}, "
                f"rvol_pct {r['rvol_pct']}) - REAL venue volume")
            ax2.bar(x, df["volume"], width=1.0, color="#f5b04c", alpha=0.8)
            ax2.set_ylabel("volume")
            fig.tight_layout()
            fig.savefig(assets / f"top500_{perp}.png", dpi=110)
            plt.close(fig)
            print("chart:", perp)
    except ImportError:
        print("matplotlib unavailable; charts skipped")

    print("\nDESCRIPTIVE ONLY. Scanning 500 series for extremes finds "
          "extremes by construction. C7's dataset stays sealed.")


if __name__ == "__main__":
    main()
