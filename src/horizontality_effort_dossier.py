"""Horizontality x effort-vs-result - the owner's clue, measured
(owner-directed, 2026-11-18).

Directive (Andrea, in-session): "price charts and the relative
position in space relative to historical horizontalite of time and
current sequence of what should have happened (effort va result) I
think is the clue to dictate what moves next."

THE CONSTRUCTION (registered BEFORE the run; nothing tuned after):
  1. HORIZONTALITY: time-at-price histogram (TAPH) of daily closes
     over the trailing 504d, 24 log-uniform bins over the window's
     close range, built PRIOR-BAR (night t sees the histogram of
     days t-504..t-1). A bin is a SHELF if its day-count >= 1.5x the
     window's mean bin count - the horizontal levels where price
     historically spent its time.
  2. POSITION IN SPACE (all read on day t-1): the close's bin is ON A
     SHELF or not; the shelf's occupancy as a POSITION within the
     trailing 252d range (bottom third / top third / middle); the
     SHELF AGE = number of days in the histogram spent at this bin
     (its accumulated time - the tested-ness of the level).
  3. EFFORT vs RESULT (the current session's bar, day t-1):
     effort rho = volume / prior-23d volume MA (the owner's volume
     surprise, H9 draft's rho);
     result z = |close-to-close return| / trailing-20d sigma
     (sigma>0-guarded);
     classes: ABSORPTION = rho >= 1.5 and z <= 0.5 (big effort, dead
     result - effort EXISTS where the move SHOULD have happened and
     didn't); SLICE = rho <= 0.8 and z >= 1.5 (big result, thin
     effort - price went where it should have been resisted);
     DEAD = otherwise.
  4. THE MEASURED QUESTIONS (declared):
     (a) ABSORPTION on a shelf vs off-shelf - P(first >=4-sigma move
         within 60d is UP), split by space position (bottom third /
         top third): the chart-read is absorption at a LOW shelf
         precedes UP moves (accumulation) and at a HIGH shelf
         precedes DOWN moves (distribution);
     (b) SLICE direction continuation: SLICE days split by the
         RESULT's sign - does thin-effort movement through supposed
         resistance CONTINUE (first big move same direction) more
         than baseline?
     (c) SHELF AGE interaction: absorption on OLD shelves (age
         quartile 4) vs young shelves (Q1) - the tested level is the
         stronger tell per the owner's "what should have happened".
All cells report n and h1/h2 where n permits; baselines printed.
In-sample descriptive; sigma>0 guard throughout; nothing armed;
nothing trades live.
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data")
OUT_CSV = CLUE / "horizontality_effort.csv"
OUT_MD = CLUE / "horizontality_effort.md"

TAPH_WIN = 504
NBINS = 24
SHELF_MULT = 1.5
RANGE_WIN = 252
VOL_MA = 23
SIGMA_WIN = 20
MOVE_SIGMA = 4.0
MOVE_HORIZON = 60
NEED = TAPH_WIN + RANGE_WIN + 5


def main():
    cells = {}
    base = {"h1": [], "h2": []}

    def add(key, half, val):
        cells.setdefault(key, {"h1": [], "h2": []})
        cells[key][half].append(val)

    age_store = []

    for data_file in sorted(DATA.glob("*.csv")):
        try:
            df = pd.read_csv(data_file)
        except Exception:
            continue
        if "volume" not in df.columns or len(df) < NEED:
            continue
        for c in ("open", "high", "low", "close"):
            if c not in df.columns:
                df = None
                break
        if df is None:
            continue
        df = df.reset_index(drop=True)
        close = pd.Series(df["close"].to_numpy(), dtype=float)
        volume = pd.Series(df["volume"].to_numpy(), dtype=float)
        n = len(close)
        ret = close.pct_change()
        sigma = ret.rolling(SIGMA_WIN).std().shift(1)
        sig_a = sigma.to_numpy()
        move = ((ret.abs() >= MOVE_SIGMA * sigma)
                & (sigma > 0)).to_numpy()
        up = ((ret >= MOVE_SIGMA * sigma) & (sigma > 0)).to_numpy()
        rho = (volume / volume.shift(1).rolling(VOL_MA).mean()
               .replace(0, np.nan)).to_numpy()
        z = (ret.abs() / sigma).to_numpy()
        rng_hi = close.rolling(RANGE_WIN).max()
        rng_lo = close.rolling(RANGE_WIN).min()
        rp = (((close - rng_lo) / (rng_hi - rng_lo)
               .replace(0, np.nan)) * 1.0).shift(1).to_numpy()
        valid = ((close > 0.01).astype(float)
                 .shift(1).fillna(0.0).to_numpy()) > 0
        ret_a = ret.to_numpy()
        mid = n // 2
        cl_a = close.to_numpy()

        for i in range(TAPH_WIN, n - MOVE_HORIZON - 1):
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

            # TAPH over trailing window, prior-bar (days i-TAPH..i-1)
            win = cl_a[i - TAPH_WIN:i]
            if len(win) < TAPH_WIN:
                continue
            lo, hi = win.min(), win.max()
            if hi <= 0 or hi <= lo:
                continue
            edges = np.exp(np.linspace(np.log(lo), np.log(hi),
                                       NBINS + 1))
            counts, _ = np.histogram(win, bins=edges)
            mean_c = counts.mean()
            last_c = cl_a[i - 1]
            b = np.searchsorted(edges, last_c) - 1
            b = min(max(b, 0), NBINS - 1)
            on_shelf = counts[b] >= SHELF_MULT * mean_c
            r = rp[i]
            if np.isnan(r) or np.isnan(rho[i - 1]) or \
                    not np.isfinite(z[i - 1]):
                continue
            rho_d = rho[i - 1]
            z_d = z[i - 1]
            ret_d = ret_a[i - 1] if i > 0 else np.nan

            pos = ("low" if r <= 1 / 3 else
                   "high" if r >= 2 / 3 else "mid")
            absorption = rho_d >= 1.5 and z_d <= 0.5
            slice_day = rho_d <= 0.8 and z_d >= 1.5

            if absorption:
                key = "absorption_shelf" if on_shelf else \
                    "absorption_offshelf"
                add(key, h, first_dir)
                add(f"{key}_{pos}", h, first_dir)
                age_store.append({"series": data_file.stem,
                                  "age": counts[b], "fd": first_dir,
                                  "on": on_shelf, "pos": pos})
            if slice_day and np.isfinite(ret_d):
                key = ("slice_up" if ret_d > 0 else "slice_dn")
                add(key + ("_shelf" if on_shelf else "_offshelf"),
                    h, first_dir)

    rows = []

    def block(key, arr):
        if not len(arr):
            return
        a = np.array(arr)
        rows.append({"cell": key, "n": len(a),
                     "P_first_up": round(float((a > 0).mean()), 4)})

    block("baseline_h1", base["h1"])
    block("baseline_h2", base["h2"])
    for key in sorted(cells):
        for h in ("h1", "h2", "ALL"):
            arr = cells[key][h] if h != "ALL" else (
                cells[key]["h1"] + cells[key]["h2"])
            block(f"{key}_{h}" if h != "ALL" else f"{key}_ALL", arr)

    # shelf-age quartiles on absorption days, ALL
    if age_store:
        ages = np.array([a["age"] for a in age_store])
        fds = np.array([a["fd"] for a in age_store])
        qs = np.percentile(ages, [25, 50, 75])
        for q, lab in (((0, qs[0]), "Q1_young"),):
            pass
        masks = [(ages <= qs[0], "Q1_young"),
                 ((ages > qs[0]) & (ages <= qs[2]), "Q23"),
                 (ages > qs[2], "Q4_old")]
        for m, lab in masks:
            if m.sum() > 30:
                rows.append({
                    "cell": f"absorption_age_{lab}", "n": int(m.sum()),
                    "P_first_up": round(float(
                        (fds[m] > 0).mean()), 4)})

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["cell", "n", "P_first_up"])
        w.writeheader()
        w.writerows(rows)
    md = ["# Horizontality x effort-vs-result (the owner's clue,",
          "measured): time-at-price shelves (504d, 24 log bins,",
          "day-count >= 1.5x mean = shelf), absorption (rho>=1.5,",
          "z<=0.5) and slice (rho<=0.8, z>=1.5) at shelves, position",
          "in 252d-range space, shelf-age quartiles. P(first >=4-sigma",
          "move within 60d is UP); sigma>0 guard; registered",
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
