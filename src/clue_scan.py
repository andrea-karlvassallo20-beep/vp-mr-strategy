"""The clue scan — look at EVERY chart before building anything.

Directive (Andrea, Nov 2026): before building the priming score, look at
every possible chart, starting from daily price and volume, for clues.
The clues that prove true are found once in a lifetime — so this scan is
DESCRIPTIVE ONLY: it ranks, it does not test. No claim is evaluated here;
C7's kill lines remain untested until the panel test is specified. The
multiplicity warning is binding: scanning ~160 series for extremes finds
extremes by construction; everything below is a candidate list, not
evidence.

Descriptive variables computed per series (all causal, at the latest bar):
  range_pos     position in the 252-day price range (0 = at the low)
  rvol_pct      realized-vol (20d) percentile within its own 3-year history
  comp_days     consecutive days in the lowest tercile of rvol (coil depth)
  evr           effort-vs-result: sum(volume) / |price change| over 60d
  vol_ratio     last 5d volume / trailing 60d median volume
  stretch_z     z-score vs 100d mean
Primed candidates: deep compression (long comp_days, low rvol_pct) with
high effort-vs-result (absorption: volume without displacement).
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIRS = [Path("paper/research/data"), Path("paper/data")]
OUT = Path("paper/research/clue_scan")


def _load_all():
    frames = []
    for d in DATA_DIRS:
        if not d.exists():
            continue
        for f in sorted(d.glob("*.csv")):
            try:
                df = pd.read_csv(f)
            except Exception:
                continue
            if not {"close", "volume"} <= set(df.columns):
                continue
            df = df.dropna(subset=["close"]).reset_index(drop=True)
            if len(df) < 150:
                continue
            frames.append((f.stem, df))
    return frames


def scan_series(name, df):
    close = df["close"].to_numpy(float)
    vol = df["volume"].to_numpy(float)
    n = len(close)
    ret = np.concatenate([[0.0], np.diff(np.log(close))])
    rvol = pd.Series(ret).rolling(20).std().to_numpy()
    win = min(252, n - 1)
    lo, hi = np.min(close[-win:]), np.max(close[-win:])
    range_pos = (close[-1] - lo) / (hi - lo) if hi > lo else 0.5
    rvol_hist = rvol[~np.isnan(rvol)]
    rvol_pct = 100.0 * np.mean(rvol_hist <= rvol[-1]) if len(rvol_hist) else 50.0
    thresh = np.nanpercentile(rvol_hist, 33) if len(rvol_hist) else np.nan
    comp_days = 0
    for v in rvol[::-1]:
        if np.isnan(v):
            break
        if v <= thresh:
            comp_days += 1
        else:
            break
    chg = close[-1] / close[-61] - 1.0 if n > 61 else np.nan
    evr = np.sum(vol[-60:]) / (abs(chg) + 1e-9) / 1e6 if chg == chg else np.nan
    med = np.median(vol[-65:-5]) if n > 65 else np.nan
    vol_ratio = np.mean(vol[-5:]) / med if med and med > 0 else np.nan
    mean, sd = np.mean(close[-100:]), np.std(close[-100:])
    stretch_z = (close[-1] - mean) / sd if sd > 0 else 0.0
    return {
        "series": name, "last_date": str(df["date"].iloc[-1]),
        "n_days": n, "range_pos": round(float(range_pos), 3),
        "rvol_pct": round(float(rvol_pct), 1),
        "comp_days": int(comp_days),
        "evr_m": round(float(evr), 2) if evr == evr else np.nan,
        "vol_ratio": round(float(vol_ratio), 2) if vol_ratio == vol_ratio else np.nan,
        "stretch_z": round(float(stretch_z), 2),
    }


INDEXES = {
    "axjo", "bvsp", "dji", "fchi", "ftse", "gdaxi", "gspc", "hsi",
    "ixic", "ks11", "n225", "nsei", "rut", "stoxx50e", "twii",
    "spy", "qqq", "iwm", "xle", "xlf",
}


def classify(name):
    n = name.lower()
    if n in INDEXES or n.startswith("^"):
        return "index"
    if n.endswith("usd") or n.endswith("usdt") or n in {
        "kef", "zlf", "zwf", "alif", "barusd",
    }:
        return "crypto"
    return "commodity"


def expansion_stats(df):
    """EW-defying signature (descriptive): after a deep coil (>= 20 days in
    the lowest vol tercile), how violent is the resolution? Reports the max
    |10-day return| within 30 days of coil exit and whether it contained a
    single day beyond 4 sigma. Causal: the window is measured AFTER the coil
    is observable."""
    close = df["close"].to_numpy(float)
    ret = np.concatenate([[0.0], np.diff(np.log(close))])
    rvol = pd.Series(ret).rolling(20).std().to_numpy()
    hist = rvol[~np.isnan(rvol)]
    if len(hist) < 100:
        return None
    thresh = np.nanpercentile(hist, 33)
    events = []
    i = 40
    while i < len(close) - 40:
        if rvol[i] is not None and not np.isnan(rvol[i]) and rvol[i] <= thresh:
            j = i
            while j < len(close) and not np.isnan(rvol[j]) and rvol[j] <= thresh:
                j += 1
            if j - i >= 20:
                win = ret[j : min(j + 30, len(ret))]
                if len(win) >= 10:
                    fwd = close[min(j + 10, len(close) - 1)] / close[j] - 1.0
                    sig = rvol[j] if not np.isnan(rvol[j]) else np.nanstd(ret[j - 20 : j])
                    big = int(np.sum(np.abs(win) > 4 * sig)) if sig > 0 else 0
                    events.append((abs(fwd), big))
            i = j + 1
        else:
            i += 1
    if not events:
        return None
    return {
        "n_coil_exits": len(events),
        "median_max10d": float(np.median([e[0] for e in events])),
        "pct_with_4sigma_day": float(np.mean([e[1] > 0 for e in events])),
    }


def primed_score(r):
    """Descriptive only. Deep coil + absorption, no direction implied."""
    coil = min(r["comp_days"] / 30.0, 1.0)
    quiet = 1.0 - min(r["rvol_pct"] / 33.0, 1.0)
    return round(0.6 * coil + 0.4 * quiet, 3)


def main():
    frames = _load_all()
    print(f"scanned {len(frames)} series (daily price + volume)")
    rows = [scan_series(n, df) for n, df in frames]
    df = pd.DataFrame(rows)
    df["primed_score"] = [primed_score(r) for r in rows]
    df["class"] = [classify(n) for n, _ in frames]
    exp = []
    for n, raw in frames:
        s = expansion_stats(raw)
        exp.append(s or {})
    df["n_coil_exits"] = [e.get("n_coil_exits", 0) for e in exp]
    df["median_max10d"] = [e.get("median_max10d", np.nan) for e in exp]
    df["pct_with_4sigma_day"] = [e.get("pct_with_4sigma_day", np.nan) for e in exp]
    df = df.sort_values("primed_score", ascending=False).reset_index(drop=True)
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "clue_scan_table.csv", index=False)
    top = df.head(12)
    print(top[["series", "class", "primed_score", "comp_days", "rvol_pct",
               "range_pos", "vol_ratio"]].to_string(index=False))
    n_coiled = int((df["comp_days"] >= 20).sum())
    print(f"\nseries with comp_days >= 20 (deep coil): {n_coiled} of {len(df)}")
    print(f"series in the bottom rvol tercile: "
          f"{int((df['rvol_pct'] <= 33).sum())} of {len(df)}")
    print("\n=== per-class summary (the EW-defying question) ===")
    for cls in ("crypto", "index", "commodity"):
        sub = df[df["class"] == cls]
        withexp = sub.dropna(subset=["median_max10d"])
        print(f"[{cls}] n={len(sub)}  deep coils={int((sub['comp_days'] >= 20).sum())}  "
              f"median coil-exit |10d move|="
              f"{withexp['median_max10d'].median() if len(withexp) else float('nan'):.4f}  "
              f"pct of exits with a >4-sigma day="
              f"{withexp['pct_with_4sigma_day'].median() if len(withexp) else float('nan'):.3f}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        assets = Path("docs/assets")
        assets.mkdir(exist_ok=True)
        for _, r in df.head(6).iterrows():
            name = r["series"]
            src = None
            for d in DATA_DIRS:
                p = d / f"{name}.csv"
                if p.exists():
                    src = p
                    break
            if src is None:
                continue
            raw = pd.read_csv(src)
            fig, (ax1, ax2) = plt.subplots(
                2, 1, figsize=(10, 6), sharex=True,
                gridspec_kw={"height_ratios": [3, 1]})
            x = pd.to_datetime(raw["date"])
            ax1.plot(x, raw["close"], lw=0.9, color="#22d3ee")
            ax1.set_title(f"{name} — primed_score {r['primed_score']} "
                          f"(comp_days {r['comp_days']}, rvol_pct {r['rvol_pct']})")
            ax2.bar(x, raw["volume"], width=1.0, color="#f5b04c", alpha=0.8)
            ax2.set_ylabel("volume")
            fig.tight_layout()
            fig.savefig(assets / f"clue_{name}.png", dpi=110)
            plt.close(fig)
            print("chart:", name)
    except ImportError:
        print("matplotlib unavailable; charts skipped")


if __name__ == "__main__":
    main()
