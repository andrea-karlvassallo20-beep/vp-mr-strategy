"""Chip stability split - do the measured chips survive a temporal
split of the archive? (The owner's "works only once" experiment.)

Directive (Andrea, 2026-11-18, in-session): "keep experimenting you
gotta find something that works only once." The sharpest available
experiment: recompute the session-37/40/42 chips on the FIRST HALF
and SECOND HALF of every series' history separately. If a chip
holds in both halves beyond sampling noise, it is a Robustness-PASS
candidate; if it flips or vanishes, that is today's honest news,
recorded the same way.

PRE-DECLARED PROTOCOL (descriptive, robustness pass - NOT W2):
  - split: each series' valid evaluation nights are divided at the
    series' own midpoint (half 1 = earlier nights, half 2 =
    later); the split is by series so mixed vintages contribute to
    both halves;
  - states: all / nuke_down / nuke_up / base / vfi_ext_low /
    near (base x vfi_ext_low) - identical constructions to the
    dossiers (37/40/42), all causal at the night;
  - labels: P(first >=4-sigma move within 60d is UP) and
    P(any >=4-sigma move within 5d), per half;
  - a chip STABLE if both halves are within 5 points of the
    pooled value AND on the same side of the baseline in both
    halves; the cells' half-to-half movement is reported raw;
  - NOT a confirmation: this is intra-archive temporal
    robustness only; W2 (fresh windows, registered thresholds)
    remains mandatory.
No kill line moves; nothing armed; nothing trades live.

Output: paper/research/clue_scan/chip_stability_split.csv and .md
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data")
OUT_CSV = CLUE / "chip_stability_split.csv"

SIGMA_WIN = 20
PCT_WIN = 756
RANGE_WIN = 252
VOL_MA = 23
Z_WIN = 252
MOVE_SIGMA = 4.0
MOVE_HORIZON = 60
NUKE_LOOKBACK = 2
NEED = PCT_WIN + SIGMA_WIN + 5

STATES = ("all", "nuke_down", "nuke_up", "base", "vfi_ext_low", "near")


def series_panel(close, volume):
    close = pd.Series(close, dtype=float).reset_index(drop=True)
    volume = pd.Series(volume, dtype=float).reset_index(drop=True)
    n = len(close)
    if n < NEED:
        return None
    ret = close.pct_change()
    sigma = ret.rolling(SIGMA_WIN).std().shift(1)
    move = (ret.abs() >= MOVE_SIGMA * sigma) & sigma.notna()
    move_up = (ret >= MOVE_SIGMA * sigma) & sigma.notna()
    move_dn = (ret <= -MOVE_SIGMA * sigma) & sigma.notna()

    rvol = ret.rolling(SIGMA_WIN).std()
    rvol_pct = rvol.rolling(PCT_WIN).rank(pct=True) * 100.0
    hi = close.rolling(RANGE_WIN).max()
    lo = close.rolling(RANGE_WIN).min()
    rng = (hi - lo).replace(0, np.nan)
    range_pos = (close - lo) / rng

    vol_ma = volume.shift(1).rolling(VOL_MA).mean()
    v = (volume / vol_ma.replace(0, np.nan) - 1.0).clip(0, 3.0)
    up_g = (close >= close.shift(1) * 1.01).astype(float)
    dn_g = (close <= close.shift(1) * 0.99).astype(float)
    vfi = (v * (up_g - dn_g)).cumsum()
    vfi_z = ((vfi - vfi.rolling(Z_WIN).mean())
             / vfi.rolling(Z_WIN).std().replace(0, np.nan)).clip(-10, 10)
    vfi_pct = vfi_z.rolling(PCT_WIN).rank(pct=True) * 100.0

    nd = move_dn.astype(float).rolling(NUKE_LOOKBACK).max()
    nu = move_up.astype(float).rolling(NUKE_LOOKBACK).max()

    state = {
        "nuke_down": nd, "nuke_up": nu,
        "base": (((rvol_pct <= 33.0) & (range_pos <= 0.15)
                  & range_pos.notna()).astype(float)),
        "vfi_ext_low": (vfi_pct <= 10.0).astype(float),
    }
    state = {k: s.shift(1) for k, s in state.items()}
    state["all"] = pd.Series(np.ones(n))
    state["near"] = ((state["base"] > 0)
                     & (state["vfi_ext_low"] > 0)).astype(float)

    valid = (close > 0.01).astype(float).shift(1).fillna(0.0)

    rev = move.iloc[::-1]
    event5 = rev.rolling(5, min_periods=1).max().iloc[::-1].shift(-1)

    first_dir = np.full(n, np.nan)
    move_a = move.to_numpy()
    up_a = move_up.to_numpy()
    for i in range(n - MOVE_HORIZON - 1):
        for j in range(i + 1, min(i + MOVE_HORIZON, n - 1) + 1):
            if move_a[j]:
                first_dir[i] = 1.0 if up_a[j] else -1.0
                break
    return state, event5, pd.Series(first_dir), valid


def main():
    acc = {(h, s): {"first": [], "move5": []}
           for h in ("h1", "h2") for s in STATES}

    for data_file in sorted(DATA.glob("*.csv")):
        try:
            df = pd.read_csv(data_file)
        except Exception:
            continue
        if "close" not in df.columns or len(df) < NEED:
            continue
        if "volume" not in df.columns:
            continue
        out = series_panel(df["close"].to_numpy(),
                           df["volume"].to_numpy())
        if out is None:
            continue
        state, event5, first_dir, valid = out
        n = len(df)
        mid = n // 2
        vc = valid.to_numpy(dtype=float)
        e5 = event5.to_numpy(dtype=float)
        fd = first_dir.to_numpy(dtype=float)
        # valid midpoint: median of the valid night indices
        ok_idx = np.where(vc > 0)[0]
        if len(ok_idx) < 200:
            continue
        split = ok_idx[len(ok_idx) // 2]
        for s in STATES:
            st = state[s].to_numpy(dtype=float)
            ok = (vc > 0) & (st > 0) & ~np.isnan(e5)
            for h, lo_, hi_ in (("h1", 0, split), ("h2", split, n)):
                m = ok.copy()
                m[:lo_] = False
                m[hi_:] = False
                if not m.any():
                    continue
                f = fd[m]
                acc[(h, s)]["first"].extend(f[~np.isnan(f)].tolist())
                acc[(h, s)]["move5"].extend(e5[m].tolist())

    rows = []
    for s in STATES:
        r = {"state": s}
        for h in ("h1", "h2"):
            fd = np.array(acc[(h, s)]["first"])
            m5 = np.array(acc[(h, s)]["move5"])
            r[f"P_first_up_{h}"] = (round(float((fd > 0).mean()), 4)
                                    if len(fd) else "")
            r[f"P_move5_{h}"] = (round(float((m5 > 0).mean()), 4)
                                 if len(m5) else "")
            r[f"n_{h}"] = len(fd)
        rows.append(r)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
