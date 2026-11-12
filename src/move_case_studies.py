"""Move case studies — how could the big move have been anticipated?

Directive (Andrea, Nov 2026): for the biggest moves (the XRPs, the ZECs,
the crashes you wish you'd shorted), reconstruct what was visible the day
BEFORE — the pre-move clue state, computed causally: only data strictly
before the move's first bar. The question is not "what predicted it"
(hindsight) but "what would the clue-scan have shown me at the last quiet
day, and would I have looked twice?"

Method (pre-declared):
  1. For every panel series, find the max |30-trading-day return| window
     over its full available history.
  2. Take the top up-moves and top down-moves (crashes).
  3. At t0 = the last bar BEFORE each window, compute the causal pre-move
     state with the clue-scan variables (coil depth, vol percentile,
     range position, effort-vs-result, volume ratio, stretch, and the
     52-week trend into the move).
  4. Report honestly: which clues were present, which were absent.
DESCRIPTIVE: a handful of extreme cases is a case file, not a test.
"""

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("paper/research/data")
WIN = 30


def best_window(close, direction="abs"):
    """Best 30d window: 'up' = max return, 'down' = min return,
    'abs' = max |return|."""
    n = len(close)
    if n < WIN + 60:
        return None
    fwd = close[WIN:] / close[:-WIN] - 1.0
    if not np.isfinite(fwd).all():
        return None
    if direction == "up":
        i = int(np.argmax(fwd))
    elif direction == "down":
        i = int(np.argmin(fwd))
    else:
        i = int(np.argmax(np.abs(fwd)))
    return {"i0": i, "i_end": i + WIN, "ret": float(fwd[i])}


def pre_move_state(df, i0):
    close = df["close"].to_numpy(float)
    vol = df["volume"].to_numpy(float)
    c = close[: i0 + 1]
    v = vol[: i0 + 1]
    if len(c) < 150:
        return None
    ret = np.concatenate([[0.0], np.diff(np.log(c))])
    rvol = pd.Series(ret).rolling(20).std().to_numpy()
    hist = rvol[~np.isnan(rvol)]
    thresh = np.nanpercentile(hist, 33)
    rvol_pct = 100.0 * np.mean(hist <= rvol[-1])
    comp_days = 0
    for x in rvol[::-1]:
        if np.isnan(x) or x > thresh:
            break
        comp_days += 1
    win = min(252, len(c) - 1)
    lo, hi = np.min(c[-win:]), np.max(c[-win:])
    range_pos = (c[-1] - lo) / (hi - lo) if hi > lo else 0.5
    chg = c[-1] / c[-61] - 1.0 if len(c) > 61 else np.nan
    evr = float(np.sum(v[-60:]) / (abs(chg) + 1e-9) / 1e6) if chg == chg else np.nan
    med = np.median(v[-65:-5]) if len(v) > 65 else np.nan
    vol_ratio = float(np.mean(v[-5:]) / med) if med and med > 0 else np.nan
    sd = np.std(c[-100:])
    stretch = float((c[-1] - np.mean(c[-100:])) / sd) if sd > 0 else 0.0
    trend52 = float(c[-1] / c[-min(252, len(c))] - 1.0)
    return {
        "rvol_pct": round(float(rvol_pct), 1),
        "comp_days": int(comp_days),
        "range_pos": round(range_pos, 3),
        "evr_m": round(evr, 2) if evr == evr else np.nan,
        "vol_ratio": round(vol_ratio, 2) if vol_ratio == vol_ratio else np.nan,
        "stretch_z": round(stretch, 2),
        "trend_52w": round(trend52, 3),
    }


def main():
    cases = []
    for f in sorted(DATA.glob("*.csv")):
        if not (f.stem.endswith("usd") or f.stem.endswith("usdt")):
            continue
        df = pd.read_csv(f).dropna(subset=["close"]).reset_index(drop=True)
        df = df[df["close"] > 0].reset_index(drop=True)
        close = df["close"].to_numpy(float)
        for direction in ("up", "down"):
            bw = best_window(close, direction)
            if not bw:
                continue
            cases.append({
                "pair": f.stem, "dir": direction,
                "ret30": round(bw["ret"], 3),
                "start": str(df["date"].iloc[bw["i0"]]),
                "end": str(df["date"].iloc[bw["i0"] + WIN - 1]),
                "i0": bw["i0"],
            })
    t = pd.DataFrame(cases)
    # artifact filter: |30d move| > 2000% is a re-denomination or
    # launch-era near-zero price, not a tradeable move. Flagged, excluded.
    artifacts = t[np.abs(t["ret30"]) > 20.0]
    if len(artifacts):
        print(f"FLAGGED as data artifacts (excluded): "
              f"{artifacts[['pair','dir','ret30','start']].to_dict('records')}")
    t = t[np.abs(t["ret30"]) <= 20.0]
    ups = t[t["dir"] == "up"].sort_values("ret30", ascending=False).head(8)
    downs = t[t["dir"] == "down"].sort_values("ret30").head(6)
    sel = pd.concat([ups, downs])
    rows = []
    for _, r in sel.iterrows():
        df = pd.read_csv(DATA / f"{r['pair']}.csv")
        st = pre_move_state(df, int(r["i0"]))
        if st is None:
            continue
        rows.append({"pair": r["pair"], "move30d": r["ret30"],
                     "move_start": r["start"], **st})
    out = pd.DataFrame(rows).sort_values("move30d", ascending=False)
    out = out.reset_index(drop=True)
    Path("paper/research/clue_scan").mkdir(exist_ok=True)
    out.to_csv("paper/research/clue_scan/move_case_studies.csv", index=False)
    print("=== THE BIGGEST MOVES IN THE PANEL, AND WHAT WAS VISIBLE THE DAY BEFORE ===")
    print(out.to_string(index=False))
    deep = out[out["comp_days"] >= 20]
    print(f"\npre-move deep coil (>=20d) present in {len(deep)} of {len(out)} cases")
    print(f"pre-move bottom-tercile volatility in "
          f"{int((out['rvol_pct'] <= 33).sum())} of {len(out)} cases")
    print(f"pre-move range_pos <= 0.3 (near lows) in "
          f"{int((out['range_pos'] <= 0.3).sum())} of {len(out)} cases")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        assets = Path("docs/assets")
        for _, r in out.head(6).iterrows():
            df = pd.read_csv(DATA / f"{r['pair']}.csv")
            i0 = int(df[df["date"] == r["move_start"]].index[0])
            fig, ax = plt.subplots(figsize=(10, 4))
            x = pd.to_datetime(df["date"])
            ax.plot(x, df["close"], lw=0.9, color="#22d3ee")
            ax.axvspan(x.iloc[i0], x.iloc[min(i0 + WIN, len(df) - 1)],
                       color="#f5b04c", alpha=0.25)
            ax.axvline(x.iloc[max(i0 - 1, 0)], color="#f87171", lw=1, ls="--")
            ax.set_title(f"{r['pair']} — the {r['move30d']:+.0%} / 30d move "
                         f"(shaded) and the last quiet day (dashed): "
                         f"comp_days {r['comp_days']}, rvol_pct {r['rvol_pct']}, "
                         f"range_pos {r['range_pos']}")
            fig.tight_layout()
            fig.savefig(assets / f"case_{r['pair']}.png", dpi=110)
            plt.close(fig)
            print("chart:", r["pair"])
    except ImportError:
        pass


if __name__ == "__main__":
    main()
