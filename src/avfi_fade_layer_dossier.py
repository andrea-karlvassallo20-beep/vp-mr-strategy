"""The AVFI fade-layer dossier - the owner's H8 construction (AVFI
v3.2 tops/bottoms layer), encoded and measured on the archive.

Directive (Andrea, 2026-11-18, in-session): the owner shared the
AVFI v3.2 research indicator (spread axis + tops/bottoms layer,
registered draft H8/H9 amendment) and the "Andrea" VPVI candles
script, said "these 2 are the best I could find, nothing else
works, you can either find what does, or help mine which seems to
me on the right track." This session mines the H8 fade layer.

THE OWNER'S H8 RULE, ENCODED (declared before the run; AVFI v3.2,
weekly edition, re-instantiated here at the DAILY grain of the
archive - a different grain is a different construction, declared):
  - evaluation at the night before (all windows causal);
  - flow axis: VFI z (session 40's declared Fedenko construction,
    23d volume MA, prior-252d z base) as the flow-fade proxy for
    the AVFI spread robust z (both are "flow vs its own recent
    distribution"; the archive has no AVFI series, the VFI is the
    registered stand-in and the substitution is DECLARED, dated);
  - fresh extremes: closing 20-bar low / 20-bar high (the
    registered pbN = 20);
  - H8 BOTTOM FADE  = fresh 20d LOW  AND flow z >= 0 (flow holding
    up into the low - the v3.2 divBot gate sp_rz >= -fadeZ, 0);
  - H8 TOP FADE     = fresh 20d HIGH AND flow z <= 0 (flow fading
    at the high - the v3.2 divTop gate sp_rz <= fadeZ, 0);
  - component cells measured separately: fresh-low alone,
    fresh-high alone, flow gate alone, both gates composed.

PRE-DECLARED QUESTIONS:
  Q1 (chip): P(first >=4-sigma move within 60d is UP) for each
    cell, against the all-nights baseline;
  Q2 (arrival): P(any >=4-sigma move within 5d) for each cell.
Descriptive only; no threshold chosen, nothing armed, W2
confirmation mandatory. No kill line moves; nothing trades live.

Output: paper/research/clue_scan/avfi_fade_layer_dossier.csv and
paper/research/clue_scan/avfi_fade_layer_dossier.md
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data")
OUT_CSV = CLUE / "avfi_fade_layer_dossier.csv"
OUT_MD = CLUE / "avfi_fade_layer_dossier.md"

SIGMA_WIN = 20
PCT_WIN = 756
VOL_MA = 23
Z_WIN = 252
MOVE_SIGMA = 4.0
PB_N = 20
MOVE_HORIZON = 60
NEED = PCT_WIN + SIGMA_WIN + 5

GROUPS = ("fresh_low", "fresh_high", "flow_up_at_low", "flow_dn_at_high",
          "bottom_fade", "top_fade", "all")


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

    # flow axis: session-40 VFI z (declared stand-in for the AVFI
    # spread robust z)
    vol_ma = volume.shift(1).rolling(VOL_MA).mean()
    v = (volume / vol_ma.replace(0, np.nan) - 1.0).clip(0, 3.0)
    up_g = (close >= close.shift(1) * 1.01).astype(float)
    dn_g = (close <= close.shift(1) * 0.99).astype(float)
    vfi = (v * (up_g - dn_g)).cumsum()
    vfi_z = ((vfi - vfi.rolling(Z_WIN).mean())
             / vfi.rolling(Z_WIN).std().replace(0, np.nan)).clip(-10, 10)

    # fresh registered 20-bar closing extremes (causal: prior bars only)
    fresh_low = (close <= close.rolling(PB_N).min()).astype(float)
    fresh_high = (close >= close.rolling(PB_N).max()).astype(float)

    state = {
        "fresh_low": fresh_low,
        "fresh_high": fresh_high,
        "vfi_z": vfi_z,
        "bottom_fade": ((fresh_low > 0) & (vfi_z >= 0)).astype(float),
        "top_fade": ((fresh_high > 0) & (vfi_z <= 0)).astype(float),
    }
    state = {k: s.shift(1) for k, s in state.items()}
    valid = (close > 0.01).astype(float).shift(1).fillna(0.0)

    # event: move within 5 days after the evaluation night
    rev = move.iloc[::-1]
    event5 = (rev.rolling(5, min_periods=1).max().iloc[::-1]
              .shift(-1).astype(float))

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
    first_acc = {g: [] for g in GROUPS}
    move5_acc = {g: [] for g in GROUPS}

    for data_file in sorted(DATA.glob("*.csv")):
        try:
            df = pd.read_csv(data_file)
        except Exception:
            continue
        if ("close" not in df.columns or "volume" not in df.columns
                or len(df) < NEED):
            continue
        out = series_panel(df["close"].to_numpy(),
                           df["volume"].to_numpy())
        if out is None:
            continue
        state, event5, first_dir, valid = out
        vc = valid.to_numpy(dtype=float)
        fl = state["fresh_low"].to_numpy(dtype=float)
        fh = state["fresh_high"].to_numpy(dtype=float)
        bf = state["bottom_fade"].to_numpy(dtype=float)
        tf = state["top_fade"].to_numpy(dtype=float)
        vz = state["vfi_z"].to_numpy(dtype=float)
        e5 = event5.to_numpy(dtype=float)
        fd = first_dir.to_numpy(dtype=float)
        ok = (vc > 0) & ~np.isnan(e5)
        grp = {
            "fresh_low": (fl > 0) & ok,
            "fresh_high": (fh > 0) & ok,
            "flow_up_at_low": ((fl > 0) & (vz >= 0) & ok),
            "flow_dn_at_high": ((fh > 0) & (vz <= 0) & ok),
            "bottom_fade": (bf > 0) & ok,
            "top_fade": (tf > 0) & ok,
            "all": ok,
        }
        for g in GROUPS:
            m = grp[g]
            if not m.any():
                continue
            f = fd[m]
            first_acc[g].extend(f[~np.isnan(f)].tolist())
            move5_acc[g].extend(e5[m].tolist())

    rows = []
    for g in GROUPS:
        fd = np.array(first_acc[g])
        m5 = np.array(move5_acc[g])
        rows.append({
            "cell": g,
            "P_first_up": (round(float((fd > 0).mean()), 4)
                           if len(fd) else ""),
            "n_first": len(fd),
            "P_move5": (round(float((m5 > 0).mean()), 4)
                        if len(m5) else ""),
            "n_move5": len(m5),
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["cell", "P_first_up",
                                          "n_first", "P_move5",
                                          "n_move5"])
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
