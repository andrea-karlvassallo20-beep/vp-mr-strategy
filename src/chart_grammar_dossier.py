"""Chart Grammar v0.1 - the human chart-read, discretized
(owner-directed, 2026-11-18).

Directive (Andrea, in-session): "you are missing the chart reading
aspect... tops and bottoms or reversions, U at extremities or V tops
that must come down... nor even the sequentiality and relative price
to flow position in space and their relation in time at that point -
why not try discretinize these. It is a human who uses charts not
robots."

THE GRAMMAR (registered BEFORE the run; nothing tuned after):
  1. Pivots: fractal swing highs/lows, W=3 bars each side; a pivot is
     confirmed (and knowable) W bars after its bar.
  2. Legs: consecutive alternating pivots define legs; consecutive
     same-type candidates keep the more extreme.
  3. Leg symbols (the discretization), each leg -> ONE symbol:
       dir     U/D
       mag     by leg |return| / (sqrt(len)*sigma20): s <1.5,
               m 1.5-3, l >=3
       dur     s <=4 bars, m 5-12, l >12
       wake    fraction of the pivot-to-pivot move completed in the
               first half of the leg's bars (by closes):
               f >=0.65 (front-loaded SPIKE/V),
               b <=0.35 (back-loaded BASE/U - the move builds late),
               e otherwise (even)
     A "U-base" per this grammar = back-loaded leg (wake b);
     a "V-spike" = front-loaded (wake f).
  4. At each night t (causal; all values from day t-1 and pivots
     confirmed by t-1): the last completed leg's SYMBOL (the
     sequentiality: 1-gram; the previous leg is stored for the
     2-gram test), the close's position in its trailing 252d range
     (range_pos), the session-40 flow decile (vfi_pct, construction
     of record).
  5. The chart-reader's claims, measured (the questions, declared):
     (a) at range BOTTOMS (range_pos<=0.20): U-base up-legs (wake b)
         vs V-spike up-legs (wake f) - P(first >=4-sigma move within
         60d is UP), sigma>0-guarded;
     (b) at range TOPS (range_pos>=0.80): U-base down-legs (washy
         distribution) vs V-spike down-legs ("V top that must come
         down") - P(first move UP): the chart-read says a V top at
         the extreme resolves DOWN first (low P_first_up);
     (c) sequentiality: at tops, does the ORDER (last leg = sharp
         down-V vs up-V, each preceded by an up leg) change
         P_first_up beyond the components alone - 2-gram cells
         vs the matching 1-gram cells;
     (d) flow relation in space and time: within bottom cells, split
         by flow state (bottom-decile washout vs other) - the U and
         V shapes read WITH the flow axis, as the owner draws them.
All cells report n and split-half (h1/h2) where n permits; the
state-night baseline (all nights) is printed for reference.
In-sample descriptive; nothing armed; nothing trades live.
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data")
OUT_CSV = CLUE / "chart_grammar.csv"
OUT_MD = CLUE / "chart_grammar.md"

W = 3
RANGE_WIN = 252
VOL_MA = 23
Z_WIN = 252
PCT_WIN = 756
SIGMA_WIN = 20
MOVE_SIGMA = 4.0
MOVE_HORIZON = 60
NEED = PCT_WIN + RANGE_WIN + SIGMA_WIN + 5


def pivots_legs(high, low, close, sigma):
    n = len(close)
    hh = pd.Series(high).rolling(2 * W + 1, center=True).max()
    ll = pd.Series(low).rolling(2 * W + 1, center=True).min()
    sh = (pd.Series(high) >= hh).to_numpy()
    sl = (pd.Series(low) <= ll).to_numpy()
    pts = []
    for j in range(W, n - W):
        if sh[j]:
            pts.append((j, "H", high[j]))
        if sl[j]:
            pts.append((j, "L", low[j]))
    legs = []
    last = None
    for j, kind, px in pts:
        if last is None:
            last = [j, kind, px]
            continue
        if kind == last[1]:
            if ((kind == "H" and px >= last[2])
                    or (kind == "L" and px <= last[2])):
                last = [j, kind, px]
            continue
        i1, p1 = last[0], last[2]
        legs.append((i1, j, p1, px))
        last = [j, kind, px]
    out = []
    for i1, i2, p1, p2 in legs:
        if p1 == 0 or p2 == 0 or i2 == i1:
            continue
        ret = abs(p2 / p1 - 1.0)
        s = sigma[i2]
        z = ret / (np.sqrt(i2 - i1) * (s + 1e-12)) if s > 0 else 0.0
        mag = "l" if z >= 3 else ("m" if z >= 1.5 else "s")
        dur = i2 - i1
        d = "s" if dur <= 4 else ("m" if dur <= 12 else "l")
        mid = (i1 + i2) // 2
        seg = close[i1:mid + 1]
        span = abs(p2 - p1)
        if span <= 0:
            continue
        if p2 > p1:
            prog = (seg.max() - p1) / span
            direction = "U"
        else:
            prog = (p1 - seg.min()) / span
            direction = "D"
        wake = "f" if prog >= 0.65 else ("b" if prog <= 0.35 else "e")
        symbol = f"{direction}{mag}{d}{wake}"
        out.append({"i1": i1, "i2": i2, "sym": symbol})
    return out


def flow_pct(close, volume):
    ret = close.pct_change()
    v = (volume / volume.shift(1).rolling(VOL_MA).mean()
         .replace(0, np.nan) - 1.0).clip(0, 3.0)
    v = v.fillna(0.0)
    up_g = (close >= close.shift(1) * 1.01).astype(float)
    dn_g = (close <= close.shift(1) * 0.99).astype(float)
    vfi = (v * (up_g - dn_g)).cumsum()
    vfi_z = ((vfi - vfi.rolling(Z_WIN).mean())
             / vfi.rolling(Z_WIN).std().replace(0, np.nan)).clip(-10, 10)
    return vfi_z.rolling(PCT_WIN).rank(pct=True) * 100.0


def main():
    cells = {}
    base = {"h1": [], "h2": []}

    def add(key, half, val):
        cells.setdefault(key, {"h1": [], "h2": []})
        cells[key][half].append(val)

    for data_file in sorted(DATA.glob("*.csv")):
        try:
            df = pd.read_csv(data_file)
        except Exception:
            continue
        if len(df) < NEED or "volume" not in df.columns:
            continue
        for c in ("open", "high", "low", "close"):
            if c not in df.columns:
                df = None
                break
        if df is None:
            continue
        df = df.reset_index(drop=True)
        close = pd.Series(df["close"].to_numpy(), dtype=float)
        high = pd.Series(df["high"].to_numpy(), dtype=float)
        low = pd.Series(df["low"].to_numpy(), dtype=float)
        n = len(df)
        ret = close.pct_change()
        sigma = ret.rolling(SIGMA_WIN).std().shift(1)
        sigma_a = sigma.to_numpy()
        move = ((ret.abs() >= MOVE_SIGMA * sigma)
                & (sigma > 0)).to_numpy()
        up = ((ret >= MOVE_SIGMA * sigma) & (sigma > 0)).to_numpy()
        rng_hi = high.rolling(RANGE_WIN).max()
        rng_lo = low.rolling(RANGE_WIN).min()
        rp = ((close - rng_lo) / (rng_hi - rng_lo).replace(0, np.nan))
        vp = flow_pct(close, pd.Series(df["volume"].to_numpy(),
                                       dtype=float))
        rp_a = rp.shift(1).to_numpy()
        vp_a = vp.shift(1).to_numpy()
        valid = ((close > 0.01).astype(float)
                 .shift(1).fillna(0.0).to_numpy()) > 0
        mid = n // 2

        legs = pivots_legs(high.to_numpy(), low.to_numpy(),
                           close.to_numpy(), sigma_a)
        last_by_night = {}
        prev_by_night = {}
        k = 0
        last_leg = None
        prev_leg = None
        for t in range(n):
            while k < len(legs) and legs[k]["i2"] + W <= t - 1:
                prev_leg = last_leg if last_leg else prev_leg
                last_leg = legs[k]
                k += 1
            last_by_night[t] = last_leg
            prev_by_night[t] = prev_leg

        for i in range(n - MOVE_HORIZON - 1):
            if not valid[i]:
                continue
            h = "h1" if i < mid else "h2"
            first_dir = None
            for j in range(i + 1, min(i + MOVE_HORIZON, n - 1) + 1):
                if move[j]:
                    first_dir = 1.0 if up[j] else -1.0
                    break
            if first_dir is None:
                continue
            base[h].append(first_dir)
            leg = last_by_night[i].copy() if last_by_night[i] else None
            if leg is None:
                continue
            sym = leg["sym"]
            r = rp_a[i]
            v = vp_a[i]
            if np.isnan(r):
                continue
            if r <= 0.20 and sym[0] == "U":
                wake = sym[3]
                key = f"bottom_{wake}_upleg" if wake in "fb" else \
                    f"bottom_{wake}_upleg"
                add(key, h, first_dir)
                if not np.isnan(v):
                    add(key + ("_washout" if v <= 10.0 else "_flowmid"),
                        h, first_dir)
            if r >= 0.80 and sym[0] == "D":
                wake = sym[3]
                key = f"top_{wake}_downleg"
                add(key, h, first_dir)
                if not np.isnan(v):
                    add(key + ("_euphoric" if v >= 90.0 else "_flowmid"),
                        h, first_dir)
            # sequentiality 2-gram: V-spike down leg right after an up leg
            pl = prev_by_night[i]
            if r >= 0.80 and sym[0] == "D" and sym[3] == "f" and pl \
                    and pl["sym"][0] == "U":
                add("top_2gram_upV_then_downV", h, first_dir)

    rows = []

    def block(key, arr):
        if not len(arr):
            return
        a = np.array(arr)
        rows.append({"cell": key, "n": len(a),
                     "P_first_up": round(float((a > 0).mean()), 4)})

    block("baseline_all_nights_h1", base["h1"])
    block("baseline_all_nights_h2", base["h2"])
    for key in sorted(cells):
        for h in ("h1", "h2", "all"):
            arr = cells[key][h] if h != "all" else (
                cells[key]["h1"] + cells[key]["h2"])
            block(f"{key}_{h}" if h != "all" else f"{key}_ALL", arr)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["cell", "n", "P_first_up"])
        w.writeheader()
        w.writerows(rows)
    md = ["# Chart Grammar v0.1 - the human chart-read, discretized",
          "",
          "Fractal pivots (W=3) -> legs -> symbols (dir, size z-scaled,",
          "duration, wake shape f/b/e). U-base = back-loaded leg (the",
          "move builds late); V-spike = front-loaded. Cells: P(first",
          ">=4-sigma move within 60d is UP), sigma>0-guarded, measured",
          "at range-extreme nights by shape and flow. Registered",
          "constants; in-sample descriptive; nothing armed; nothing",
          "trades live.",
          "", "| cell | n | P_first_up |", "|---|---|---|"]
    for r in rows:
        md.append(f"| {r['cell']} | {r['n']} | {r['P_first_up']} |")
    OUT_MD.write_text("\n".join(md) + "\n")
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
