"""The systematic move study - waaay more moves.

Directive (Andrea, Nov 2026): "You need to study waaay more moves." The
case file held six hand-picked anecdotes. This pass finds EVERY
significant move on the board - the TVC panel (5 years of history),
the top-500 klines cache (real venue volume), and the commodities/
equities set - reconstructs the causal pre-move state at the last quiet
day, and reports the aggregate: how often was a big move PRECEDED by a
coil, by quiet, by a blow-off?

Move definition (pre-declared, applied uniformly):
  crypto  : |30-day return| >= +100% (up) or <= -70% (down)
  eq/comm : >= +30% (up) or <= -25% (down) - their scales are smaller
  Episodes are deduplicated: overlapping 30d windows collapse to the
  single largest |move|, with a minimum 30-day gap between episodes.

Pre-move state (all CAUSAL, measured on the last day BEFORE the 30-day
move window opens): comp_days, rvol_pct, range_pos, evr, vol_ratio,
stretch_z, trend_52w. Artifacts are flagged, not deleted: rows with a
launch-era near-zero base (<30 days of history before the window) or a
re-denomination spike (>20x in a single day inside the window) carry the
flag and are excluded from the aggregate stats.

DESCRIPTIVE ONLY. This is a census of moves, not a test; C7 stays
sealed; multiplicity binds. The aggregate answers ONE question per
direction: what does the board look like the day before it moves?
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

OUT = Path("paper/research/clue_scan")
MOVES_CSV = OUT / "move_study.csv"
CHART_DIR = Path("docs/assets")

TVC = Path("paper/research/data")
T500 = Path("data/raw/top500_klines")
EQC = Path("data/raw/eq_commodity_klines")

EQ_SYMBOLS = None  # loaded from eq_commodity_scan universe names


def _pre_move_state(close, vol, i):
    """Causal state at index i (the last quiet day). i >= 60 required."""
    c = close[: i + 1]
    ret = np.concatenate([[0.0], np.diff(np.log(c))])
    rvol = pd.Series(ret).rolling(20).std().to_numpy()
    hist = rvol[~np.isnan(rvol)]
    if len(hist) < 40:
        return None
    rvol_pct = 100.0 * np.mean(hist <= rvol[-1])
    thresh = np.nanpercentile(hist, 33)
    comp_days = 0
    for v in rvol[::-1]:
        if np.isnan(v):
            break
        if v <= thresh:
            comp_days += 1
        else:
            break
    win = min(252, len(c))
    lo, hi = np.min(c[-win:]), np.max(c[-win:])
    range_pos = (c[-1] - lo) / (hi - lo) if hi > lo else 0.5
    chg = c[-1] / c[-61] - 1.0 if len(c) > 61 else np.nan
    evr = np.sum(vol[: i + 1][-60:]) / (abs(chg) + 1e-9) / 1e6 if chg == chg else np.nan
    med = np.median(vol[-65:-5]) if len(vol) > 65 else np.nan
    vol_ratio = np.mean(vol[-5:]) / med if med and med > 0 else np.nan
    mean, sd = np.mean(c[-100:]), np.std(c[-100:])
    stretch_z = (c[-1] - mean) / sd if sd > 0 else 0.0
    trend_52w = c[-1] / c[-253] - 1.0 if len(c) > 253 else np.nan
    return {
        "comp_days": int(comp_days),
        "rvol_pct": round(float(rvol_pct), 1),
        "range_pos": round(float(range_pos), 3),
        "evr_m": round(float(evr), 2) if evr == evr else np.nan,
        "vol_ratio": round(float(vol_ratio), 2) if vol_ratio == vol_ratio else np.nan,
        "stretch_z": round(float(stretch_z), 2),
        "trend_52w": round(float(trend_52w), 3) if trend_52w == trend_52w else np.nan,
    }


def find_moves(name, df, up_thr, dn_thr, cls, volume_flag):
    close = df["close"].to_numpy(float)
    vol = df["volume"].fillna(0).to_numpy(float)
    n = len(close)
    if n < 120:
        return []
    ret30 = np.full(n, np.nan)
    ret30[30:] = close[30:] / close[:-30] - 1.0
    day_ret = np.concatenate([[0.0], np.diff(np.log(close))])
    events = []
    i = 60
    while i < n - 5:
        r = ret30[i]
        if np.isnan(r):
            i += 1
            continue
        if r >= up_thr or r <= dn_thr:
            # local max of |ret30| within +-10 days
            j0 = max(60, i - 10)
            j1 = min(n - 1, i + 10)
            seg = np.nan_to_num(ret30[j0:j1 + 1], nan=0.0)
            k = j0 + int(np.argmax(np.abs(seg)))
            r = ret30[k]
            # artifact: >20x single day inside the window = re-denomination
            window_day = np.nanmax(np.abs(day_ret[k - 29:k + 1])) \
                if k - 29 >= 0 else 0.0
            artifact = bool(window_day > np.log(20)) or (k < 90)
            state = _pre_move_state(close, vol, k - 30)
            if state is not None:
                events.append({
                    "series": name, "class": cls, "direction":
                    "up" if r > 0 else "down",
                    "move30d": round(float(r), 3),
                    "move_end_index": k,
                    "move_end_date": str(df["date"].iloc[min(k, n - 1)]),
                    "synthetic_volume_flag": volume_flag,
                    "artifact": artifact,
                    **state,
                })
            i = k + 30  # dedupe: 30-day gap between episodes
        else:
            i += 1
    return events


def load_universe():
    """(name, df, cls, volume_flag) for every series on the board."""
    out = []
    for f in sorted(TVC.glob("*.csv")):
        name = f.stem
        n = name.lower()
        if n.endswith("usd") or n.endswith("usdt"):
            cls = "crypto"
        elif n.startswith("^") or n in {
                "axjo", "bvsp", "dji", "fchi", "ftse", "gdaxi", "gspc",
                "hsi", "ixic", "ks11", "n225", "nsei", "rut", "stoxx50e",
                "twii", "spy", "qqq", "iwm", "xle", "xlf"}:
            cls = "index"
        else:
            cls = "commodity"
        try:
            df = pd.read_csv(f).dropna(subset=["close"]).reset_index(drop=True)
        except Exception:
            continue
        if {"date", "close", "volume"} <= set(df.columns) and len(df) >= 120:
            out.append((name, df, cls, True))  # TVC volume often synthetic
    for f in sorted(T500.glob("*.csv")):
        name = f.stem
        if name.startswith("SPOT_"):
            name = name  # keep the SPOT_ prefix: no perp market
        try:
            df = pd.read_csv(f).dropna(subset=["close"]).reset_index(drop=True)
        except Exception:
            continue
        if len(df) >= 120:
            out.append((name, df, "crypto", False))  # real venue volume
    eq_names = {}
    try:
        sys.path.insert(0, "src")
        from eq_commodity_scan import UNIVERSE as EQ_UNIVERSE
        for sym, nm, cls in EQ_UNIVERSE:
            eq_names[sym.replace("=", "_").replace("^", "")] = (nm, cls)
    except Exception:
        pass
    for f in sorted(EQC.glob("*.csv")):
        nm, cls = eq_names.get(f.stem, (f.stem, "commodity"))
        try:
            df = pd.read_csv(f).dropna(subset=["close"]).reset_index(drop=True)
        except Exception:
            continue
        if len(df) >= 120:
            out.append((nm, df, cls, False))
    return out


def main():
    universe = load_universe()
    print(f"universe: {len(universe)} series with >=120 days of history")
    all_events = []
    for name, df, cls, volflag in universe:
        if cls == "crypto":
            up, dn = 1.0, -0.70
        else:
            up, dn = 0.30, -0.25
        all_events.extend(find_moves(name, df, up, dn, cls, volflag))
    if not all_events:
        print("no moves found")
        return
    ev = pd.DataFrame(all_events)
    ev.to_csv(MOVES_CSV, index=False)
    clean = ev[~ev["artifact"]]
    print(f"move episodes found: {len(ev)} "
          f"({int(ev['artifact'].sum())} flagged artifacts, excluded from stats)")

    def agg(sub, label):
        if not len(sub):
            return
        print(f"\n[{label}] n={len(sub)}")
        print(f"  preceded by deep coil (comp_days>=20): "
              f"{(sub['comp_days'] >= 20).mean():.1%}")
        print(f"  preceded by quiet (rvol_pct<=33):       "
              f"{(sub['rvol_pct'] <= 33).mean():.1%}")
        print(f"  preceded by blow-off (stretch_z>=2):   "
              f"{(sub['stretch_z'] >= 2).mean():.1%}")
        print(f"  at range bottom (range_pos<=0.25):      "
              f"{(sub['range_pos'] <= 0.25).mean():.1%}")
        print(f"  at range top (range_pos>=0.75):         "
              f"{(sub['range_pos'] >= 0.75).mean():.1%}")
        print(f"  median pre-move: comp_days={sub['comp_days'].median():.0f} "
              f"rvol_pct={sub['rvol_pct'].median():.0f} "
              f"stretch_z={sub['stretch_z'].median():.2f} "
              f"trend_52w={sub['trend_52w'].median():.2f}")

    crypto = clean[clean["class"] == "crypto"]
    agg(crypto[crypto["direction"] == "up"], "CRYPTO UP moves (>=+100%/30d)")
    agg(crypto[crypto["direction"] == "down"], "CRYPTO DOWN moves (<=-70%/30d)")
    noncrypto = clean[clean["class"] != "crypto"]
    agg(noncrypto[noncrypto["direction"] == "up"], "NON-CRYPTO UP (>=+30%/30d)")
    agg(noncrypto[noncrypto["direction"] == "down"], "NON-CRYPTO DOWN (<=-25%/30d)")

    # charts: top 16 clean crypto up-moves by size, with the window shaded
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        top = (crypto[crypto["direction"] == "up"]
               .sort_values("move30d", ascending=False))
        seen, picked = set(), []
        for _, r in top.iterrows():
            if r["series"] in seen:
                continue
            seen.add(r["series"])
            picked.append(r)
            if len(picked) == 16:
                break
        frames = {n: d for n, d, c, v in universe}
        for r in picked:
            df = frames.get(r["series"])
            if df is None:
                continue
            close = df["close"].to_numpy(float)
            k = int(r["move_end_index"])
            fig, ax = plt.subplots(figsize=(9, 4))
            x = pd.to_datetime(df["date"])
            ax.plot(x, close, lw=0.9, color="#8fa0b5")
            lo = max(0, k - 200)
            ax.plot(x[lo:k + 1], close[lo:k + 1], lw=1.1, color="#22d3ee")
            w0, w1 = max(0, k - 30), k
            ax.axvspan(x[w0], x[w1], color="#4ade80", alpha=0.18)
            ax.set_title(
                f"{r['series']}  +{r['move30d']*100:.0f}%/30d  "
                f"(pre-move: coil {r['comp_days']}d, rvol pct {r['rvol_pct']}, "
                f"range pos {r['range_pos']}, stretch z {r['stretch_z']})",
                fontsize=10)
            fig.tight_layout()
            fig.savefig(CHART_DIR / f"move_study_{r['series']}.png", dpi=110)
            plt.close(fig)
        print(f"\ncharts: 16 top up-moves saved to docs/assets/move_study_*.png")
    except ImportError:
        print("matplotlib unavailable; charts skipped")

    print("\nDESCRIPTIVE ONLY. A census of moves, not a test. "
          "C7 stays sealed; multiplicity binds.")


if __name__ == "__main__":
    main()
