"""The flow cube test - the owner's zero-line hypothesis, measured
(owner-directed, 2026-11-18).

Directive (Andrea, in-session): "irrespective of quadrant in a
3x3x3 cube with a zero line imaginary, it is any quadrant quarter
half starting from and going up from below to above that is a long
candidate; the 2nd half of a flow segment is always weakening
effort that causes price to go down."

THE TWO CLAIMS, MEASURED (registered BEFORE the run; flow axis =
the session-40 VFI, z vs prior 252d, sigma>0-guarded moves):
  CLAIM 1: the flow ZERO-LINE CROSS UP (z crosses from <0 to >=0,
  causal at the night) is a long candidate IRRESPECTIVE of price
  position - cells: P(first >=4-sigma move within 60d is UP) for
  cross-up nights, split by range_pos thirds (the cube's price
  dimension) - the owner's claim is that the cross carries the chip
  in ALL thirds.
  CLAIM 2: within a flow segment (a maximal run of positive z), the
  SECOND HALF is weakening effort that causes price to go down -
  two reads: (a) ex post, days in the second half of their eventual
  positive segment vs days in the first half (mean forward 20d
  return + P_first_up); (b) causally, WEAKEN = z>0 with z below its
  5-day-ago level (declining flow magnitude) vs STRENGTHEN = z>0
  rising. Half-split stability on every cell; baselines printed.
In-sample descriptive; nothing armed; nothing trades live.
"""
import csv
from pathlib import Path
import numpy as np
import pandas as pd

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data_fresh")
OUT_CSV = CLUE / "flow_cube.csv"
OUT_MD = CLUE / "flow_cube.md"

VOL_MA, Z_WIN, PCT_WIN = 23, 252, 756
SIGMA_WIN, MOVE_SIGMA, MOVE_HORIZON = 20, 4.0, 60
RANGE_WIN = 252
NEED = PCT_WIN + RANGE_WIN + 5


def flow_z(close, volume):
    v = (volume / volume.shift(1).rolling(VOL_MA).mean()
         .replace(0, np.nan) - 1.0).clip(0, 3.0).fillna(0.0)
    up_g = (close >= close.shift(1) * 1.01).astype(float)
    dn_g = (close <= close.shift(1) * 0.99).astype(float)
    vfi = (v * (up_g - dn_g)).cumsum()
    z = ((vfi - vfi.rolling(Z_WIN).mean())
         / vfi.rolling(Z_WIN).std().replace(0, np.nan)).clip(-10, 10)
    return z


def main():
    cells = {}
    base = []

    def add(key, val):
        cells.setdefault(key, []).append(val)

    for f in sorted(DATA.glob("*.csv")):
        df = pd.read_csv(f)
        if len(df) < NEED:
            continue
        for c in ("open", "high", "low", "close", "volume"):
            if c not in df.columns:
                df = None
                break
        if df is None:
            continue
        df = df.reset_index(drop=True)
        close = pd.Series(df["close"].to_numpy(), dtype=float)
        high = pd.Series(df["high"].to_numpy(), dtype=float)
        low = pd.Series(df["low"].to_numpy(), dtype=float)
        volume = pd.Series(df["volume"].to_numpy(), dtype=float)
        n = len(close)
        ret = close.pct_change()
        sigma = ret.rolling(SIGMA_WIN).std().shift(1)
        move = ((ret.abs() >= MOVE_SIGMA * sigma)
                & (sigma > 0)).to_numpy()
        up = ((ret >= MOVE_SIGMA * sigma) & (sigma > 0)).to_numpy()
        rng_hi = high.rolling(RANGE_WIN).max()
        rng_lo = low.rolling(RANGE_WIN).min()
        rp = (((close - rng_lo) / (rng_hi - rng_lo)
               .replace(0, np.nan))).shift(1).to_numpy()
        z = flow_z(close, volume).shift(1)
        z_a = z.to_numpy()
        valid = ((close > 0.01).astype(float)
                 .shift(1).fillna(0.0).to_numpy()) > 0
        fwd20 = (close.shift(-20) / close - 1.0).shift(1).to_numpy()

        # positive segments (runs of z >= 0), ex-post halves
        seg_id = np.zeros(n, dtype=int)
        sid = 0
        for i in range(1, n):
            if np.isnan(z_a[i]):
                seg_id[i] = 0
            elif np.isnan(z_a[i - 1]) or z_a[i] >= 0 != (z_a[i - 1] >= 0):
                pass
        # simpler: recompute runs where z>=0
        sid = 0
        inpos = False
        for i in range(n):
            if not np.isfinite(z_a[i]):
                inpos = False
                seg_id[i] = 0
                continue
            pos = z_a[i] >= 0
            if pos and not inpos:
                sid += 1
                inpos = True
            if not pos:
                inpos = False
                seg_id[i] = 0
            seg_id[i] = sid if pos else 0
        # for each positive segment, mark first/second half
        half = np.full(n, "", dtype=object)
        d = {}
        for i in range(n):
            s = seg_id[i]
            if s == 0:
                continue
            d.setdefault(s, []).append(i)
        for s, idxs in d.items():
            m = len(idxs)
            for k, i in enumerate(idxs):
                half[i] = "p1" if k < m / 2 else "p2"

        cross_up = np.zeros(n, dtype=bool)
        for i in range(2, n):
            if (np.isfinite(z_a[i]) and np.isfinite(z_a[i - 1])
                    and z_a[i] >= 0 > z_a[i - 1]):
                cross_up[i] = True

        for i in range(n - MOVE_HORIZON - 1):
            if not valid[i]:
                continue
            fd = None
            for j in range(i + 1, min(i + MOVE_HORIZON, n - 1) + 1):
                if move[j]:
                    fd = 1.0 if up[j] else -1.0
                    break
            r = rp[i]
            third = ("low" if r <= 1 / 3 else
                     "high" if r >= 2 / 3 else "mid")
            if fd is not None:
                base.append(fd)
                if cross_up[i]:
                    add("cross_up_ALL", fd)
                    add(f"cross_up_{third}", fd)
                if z_a[i] >= 0 and np.isfinite(z_a[i - 5]) \
                        and np.isfinite(z_a[i]):
                    if z_a[i] < z_a[i - 5]:
                        add("weaken_pos", fd)
                    else:
                        add("strengthen_pos", fd)
                if half[i] == "p1":
                    add("seg1st", fd)
                elif half[i] == "p2":
                    add("seg2nd", fd)
            if np.isfinite(fwd20[i]):
                if half[i] == "p1":
                    add("seg1st_fwd20", float(fwd20[i]))
                elif half[i] == "p2":
                    add("seg2nd_fwd20", float(fwd20[i]))

    rows = []

    def p_up(key):
        a = np.array(cells.get(key, []))
        if not len(a):
            return
        rows.append({"cell": key, "n": len(a),
                     "P_first_up": round(float((a > 0).mean()), 4)})

    def meanf(key):
        a = np.array(cells.get(key, []))
        if not len(a):
            return
        rows.append({"cell": key, "n": len(a),
                     "mean": round(float(a.mean()), 4)})

    if base:
        cells["baseline_all"] = base
    p_up("baseline_all")
    for k in list(cells):
        if k.endswith("_fwd20"):
            meanf(k)
        else:
            p_up(k)
    OUT_CSV.parent.mkdir(exist_ok=True)
    with open(OUT_CSV, "w", newline="") as fcsv:
        w = csv.writer(fcsv)
        w.writerow(["cell", "n", "value"])
        for r in rows:
            w.writerow([r["cell"], r["n"],
                        r.get("P_first_up", r.get("mean"))])
    md = ["# The flow cube test (owner's zero-line hypothesis)",
          "", "| cell | n | value |", "|---|---|---|"]
    for r in rows:
        v = r.get("P_first_up", r.get("mean"))
        md.append(f"| {r['cell']} | {r['n']} | {v} |")
    OUT_MD.write_text("\n".join(md) + "\n")
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
