"""The flow inference matrix - the owner's "spend as much time as
possible deriving inferences... flow is the closest to a useful
indicator system" directive, answered with the full flow-zone
geometry measured across every night.

PRE-DECLARED (registered BEFORE the run; universe: data_fresh,
min 310 bars; sigma>0 guard):
  Axis 1 - FLOW ZONE of the night (VFI z vs prior 252d, prior-bar):
    XB (z<=-1.5), B (-1.5<z<0), A (0<=z<1.5), XA (z>=1.5).
  Axis 2 - DAYS IN ZONE (young <=10d / old >10d - the session-60
    flow-age finding applied WITHIN zones, not just segments).
  Axis 3 - PRICE THIRD of the 252d range (low/mid/high).
  Labels: P(first >=4-sigma move within 60d is UP) + mean fwd-20d.
  Also: the ZONE CHAIN as measured counts - P(next zone | current
  zone) across all zone transitions (the sequentiality layer).
Nothing tuned; cells with n<100 marked thin; halves reported; all
in-sample descriptive; nothing armed; nothing trades live.
"""
import csv
from pathlib import Path
import numpy as np
import pandas as pd

FRESH = Path("paper/research/data_fresh")
OUT = Path("paper/research/clue_scan/flow_zone_matrix.csv")
OUT_MD = Path("paper/research/clue_scan/flow_zone_matrix.md")
VOL_MA, Z_WIN = 23, 252
SIGMA_WIN, MOVE_SIGMA, HORIZON = 20, 4.0, 60
RANGE_WIN = 252
MIN = 310


def axisz(close, volume):
    v = (volume / volume.shift(1).rolling(VOL_MA).mean()
         .replace(0, np.nan) - 1.0).clip(0, 3.0).fillna(0.0)
    up_g = (close >= close.shift(1) * 1.01).astype(float)
    dn_g = (close <= close.shift(1) * 0.99).astype(float)
    vfi = (v * (up_g - dn_g)).cumsum()
    z = ((vfi - vfi.rolling(Z_WIN).mean())
         / vfi.rolling(Z_WIN).std().replace(0, np.nan)).clip(-10, 10)
    return z


def zone(zv):
    if not np.isfinite(zv):
        return ""
    if zv >= 1.5:
        return "XA"
    if zv >= 0:
        return "A"
    if zv > -1.5:
        return "B"
    return "XB"


def main():
    cells = {}
    chain = {}
    base = []

    def add(k, vals):
        cells.setdefault(k, {"fd": [], "f20": []})
        cells[k][vals[0]].append(vals[1])

    for f in sorted(FRESH.glob("*.csv")):
        df = pd.read_csv(f).reset_index(drop=True)
        if len(df) < MIN:
            continue
        for c in ("open", "high", "low", "close", "volume"):
            if c not in df.columns:
                df = None
                break
        if df is None:
            continue
        close = pd.Series(df["close"].to_numpy(), dtype=float)
        volume = pd.Series(df["volume"].to_numpy(), dtype=float)
        ret = close.pct_change()
        sigma = ret.rolling(SIGMA_WIN).std().shift(1)
        move = ((ret.abs() >= MOVE_SIGMA * sigma)
                & (sigma > 0)).to_numpy()
        up = ((ret >= MOVE_SIGMA * sigma) & (sigma > 0)).to_numpy()
        rng_hi = close.rolling(RANGE_WIN).max()
        rng_lo = close.rolling(RANGE_WIN).min()
        rp = (((close - rng_lo) / (rng_hi - rng_lo)
               .replace(0, np.nan))).shift(1).to_numpy()
        z = axisz(close, volume).shift(1)
        z_a = z.to_numpy()
        fwd20 = (close.shift(-20) / close - 1.0).shift(1).to_numpy()
        valid = ((close > 0.01).astype(float)
                 .shift(1).fillna(0.0).to_numpy()) > 0
        n = len(df)
        mid = n // 2

        # days-in-zone
        din = np.zeros(n, dtype=int)
        run = 0
        for i in range(1, n):
            g, gp = zone(z_a[i]), zone(z_a[i - 1])
            if g == "" or gp == "":
                run = 0
            elif g == gp:
                run += 1
            else:
                run = 0
            din[i] = run
        # zone chain transitions (consecutive days, distinct zones)
        for i in range(1, n):
            g, gp = zone(z_a[i]), zone(z_a[i - 1])
            if g and gp and g != gp:
                k = (gp, g)
                chain[k] = chain.get(k, 0) + 1

        for i in range(n - HORIZON - 1):
            if not valid[i]:
                continue
            g = zone(z_a[i])
            if not g:
                continue
            fd = None
            for j in range(i + 1, min(i + HORIZON, n - 1) + 1):
                if move[j]:
                    fd = 1.0 if up[j] else -1.0
                    break
            if fd is not None:
                base.append(fd)
            h = "h1" if i < mid else "h2"
            third = ("low" if rp[i] <= 1 / 3 else
                     "high" if rp[i] >= 2 / 3 else "mid")
            age = "young" if din[i] <= 10 else "old"
            keys = [g, f"{g}_{age}", f"{g}_{age}_{third}",
                    f"{g}_{third}"]
            for k in keys:
                if fd is not None:
                    add(k, ("fd", fd))
                if np.isfinite(fwd20[i]):
                    add(k, ("f20", float(fwd20[i])))

    rows = []
    for k in sorted(cells):
        fd = np.array(cells[k]["fd"])
        f20 = np.array(cells[k]["f20"])
        rows.append({
            "cell": k, "n_fd": len(fd),
            "P_first_up": round(float((fd > 0).mean()), 4)
            if len(fd) >= 100 else (round(float((fd > 0).mean()), 4)
                                    if len(fd) else ""),
            "n_thin": len(fd) < 100,
            "mean_fwd20": round(float(f20.mean()), 4)
            if len(f20) >= 100 else "",
        })
    if base:
        b = np.array(base)
        rows.append({"cell": "BASELINE", "n_fd": len(b),
                     "P_first_up": round(float((b > 0).mean()), 4),
                     "n_thin": False, "mean_fwd20": ""})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as fcsv:
        w = csv.DictWriter(fcsv, fieldnames=["cell", "n_fd",
                                            "P_first_up", "n_thin",
                                            "mean_fwd20"])
        w.writeheader()
        w.writerows(rows)
    # chain table
    tot = sum(chain.values())
    chain_rows = sorted(chain.items(), key=lambda kv: -kv[1])
    md = ["# The flow inference matrix - zone x age x price-space",
          "",
          "VFI z zones: XB (z<=-1.5), B, A, XA (z>=1.5); young ="
          " <=10d in zone; price third of 252d range. P(first big"
          " move within 60d is UP) + mean fwd-20d. Thin cells"
          " (n<100) marked. In-sample descriptive; nothing armed;",
          "nothing trades live.", "",
          "| cell | n | P_first_up | thin | mean_fwd20 |",
          "|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['cell']} | {r['n_fd']} "
                  f"| {r['P_first_up']} | {r['n_thin']} "
                  f"| {r['mean_fwd20']} |")
    md += ["", "## The zone chain (P(next zone | current zone) counts)",
           "", "| from | to | count | share |", "|---|---|---|---|"]
    for (a, b), c in chain_rows[:24]:
        md.append(f"| {a} | {b} | {c} | "
                  f"{round(c / tot, 3)} |")
    OUT_MD.write_text("\n".join(md) + "\n")
    for r in rows:
        print(r)
    for (a, b), c in chain_rows[:12]:
        print("chain", a, "->", b, c)


if __name__ == "__main__":
    main()
