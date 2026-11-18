"""SMH Presence Indicator v0.1 — the program's own indicator, built
from the measured dossiers (and the owner's AVFI lineage).

Directive (Andrea, 2026-11-18, in-session): "why not try and make
your own indicator, or improve on mine or try go flip a coin."
The coin has already been flipped: 289,262 archive nights, four
measured dossiers (closeness 34, coin-chip 37, VFI-extremity 40,
AVFI-fade-layer 42). This module composes their findings into ONE
state machine with every constant REGISTERED from a measured
dossier — nothing tuned, nothing armed, W2 confirmation pending.

REGISTRED CONSTRUCTION (per the dossiers; none adjustable):
  quiet      rvol_pct <= 33   (20d vol percentile in 756d;
             closeness AUC 0.323 at K=5 — the dominant criterion)
  deep_quiet rvol_pct <= 10   (closeness dossier: strongest)
  base       range_pos <= 0.15 (quiet + basis; coin-chip dossier)
  comp       comp_days >= 20  (closeness: mild, ~0.54)
  vfi_ext_low  bottom DECILE of the VFI z distribution in 756d
             (NOT a median gate: owner's H8 improvement, session 42)
  fresh_low / fresh_high  fresh 20-bar closing extreme
             (session 42: arrival 1.6-1.8x baseline)
  nuke_down / nuke_up  >=4-sigma day within last 2 days (session 37)

REGISTERED CHIP TABLE (discovery-panel conditionals, W2 pending;
P(first >=4-sigma move within 60d is UP)):
  all nights .576 | nuke_down .748 | nuke_up .767 | base .645 |
  primed .635 | vfi_ext_low .686 | base x vfi_ext_low .601.
ARRIVAL TABLE (P(move within 5d)): all .0497 | base .0817 |
  base x vfi_ext_low .0943 | fresh_low .0809 | fresh_high .0896.

VERDICT RULE (registered): PRESENCE state = base(quiet + range) —
  the timing seat; NEAR = presence x vfi_ext_low (1.9x arrival);
  post-nuke states carry the largest chips. Direction is a LEAN,
  never a promise; the instrument times the FIRST BIG MOVE, never
  a drift; medians are negative on the panel (session 37). This
  is an INDICATOR: no equity curve, no win rate, nothing armed,
  nothing trades live.

Output: for each series CSV on the archive (default: all), the
last-night state row. The Pine port
(paper/research/when_instrument/smh_presence_pine.md) mirrors
this construction for TradingView, declared UNTESTED in Pine.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data")

SIGMA_WIN = 20
PCT_WIN = 756
RANGE_WIN = 252
VOL_MA = 23
Z_WIN = 252
PB_N = 20
MOVE_SIGMA = 4.0
NUKE_LOOKBACK = 2
NEED = PCT_WIN + SIGMA_WIN + 5


def read_chip_tables():
    chip = pd.read_csv(CLUE / "coin_chip_dossier.csv")
    return chip


def smh_state(close, volume, dates=None):
    """Compute the presence state as of the LAST night of the
    series (all windows causal). Returns a dict of state values
    and the registered verdict."""
    close = pd.Series(close, dtype=float).reset_index(drop=True)
    volume = pd.Series(volume, dtype=float).reset_index(drop=True)
    n = len(close)
    if n < NEED:
        return None
    ret = close.pct_change()
    sigma = ret.rolling(SIGMA_WIN).std().shift(1)
    move = (ret.abs() >= MOVE_SIGMA * sigma) & sigma.notna()
    move_down = ((ret <= -MOVE_SIGMA * sigma) & sigma.notna()).astype(float)
    move_up = ((ret >= MOVE_SIGMA * sigma) & sigma.notna()).astype(float)

    rvol = ret.rolling(SIGMA_WIN).std()
    rvol_pct = rvol.rolling(PCT_WIN).rank(pct=True) * 100.0
    low_vol = (rvol_pct <= 33.0) & rvol_pct.notna()
    comp_days = low_vol.rolling(20).sum()
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

    fresh_low = bool(close.iloc[-1] <= close.rolling(PB_N).min().iloc[-1])
    fresh_high = bool(close.iloc[-1] >= close.rolling(PB_N).max().iloc[-1])

    nuked = (move_down.rolling(NUKE_LOOKBACK).max().iloc[-1] > 0
             or move_up.rolling(NUKE_LOOKBACK).max().iloc[-1] > 0)
    nuke_side = ""
    if move_down.rolling(NUKE_LOOKBACK).max().iloc[-1] > 0:
        nuke_side = "down"
    elif move_up.rolling(NUKE_LOOKBACK).max().iloc[-1] > 0:
        nuke_side = "up"

    quiet = float(rvol_pct.iloc[-1]) <= 33.0
    deep_quiet = float(rvol_pct.iloc[-1]) <= 10.0
    base = quiet and float(range_pos.iloc[-1]) <= 0.15
    comp = float(comp_days.iloc[-1]) >= 20.0
    vfi_ext_low = float(vfi_pct.iloc[-1]) <= 10.0

    presence = base and quiet
    near = presence and vfi_ext_low

    chip = 0.576
    if nuke_side == "down":
        chip = 0.748
    elif nuke_side == "up":
        chip = 0.767
    elif near:
        chip = 0.601
    elif presence:
        chip = 0.645
    elif vfi_ext_low:
        chip = 0.686

    verdict = "NO PRESENCE"
    if near:
        verdict = "PRESENCE + NEAR (x1.9 arrival)"
    elif presence:
        verdict = "PRESENCE (in the base, quiet)"
    elif nuke_side:
        verdict = f"post-nuke ({nuke_side}) chip state"

    return {
        "date": str(dates.iloc[-1]) if dates is not None else "",
        "rvol_pct": round(float(rvol_pct.iloc[-1]), 1),
        "range_pos": round(float(range_pos.iloc[-1]), 3),
        "comp_days": int(comp_days.iloc[-1]),
        "vfi_pct": round(float(vfi_pct.iloc[-1]), 1),
        "fresh_low": fresh_low, "fresh_high": fresh_high,
        "nuke": nuke_side or "—",
        "presence": presence, "near": near,
        "chip": chip, "verdict": verdict,
    }


def main(argv):
    series_files = argv[1:] or None
    files = ([Path(f) for f in series_files]
             if series_files else sorted(DATA.glob("*.csv")))
    rows = []
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        if "close" not in df.columns or len(df) < NEED:
            continue
        vol = (df["volume"].to_numpy() if "volume" in df.columns
               else np.full(len(df), np.nan))
        dates = df["date"] if "date" in df.columns else None
        st = smh_state(df["close"].to_numpy(), vol, dates)
        if st is None:
            continue
        st["series"] = f.stem
        rows.append(st)
    out = pd.DataFrame(rows)
    (CLUE / "smh_presence_scan.csv").write_text(
        out.to_csv(index=False)) if not out.empty else None
    cols = ["series", "date", "rvol_pct", "range_pos", "comp_days",
            "vfi_pct", "fresh_low", "fresh_high", "nuke",
            "presence", "near", "chip", "verdict"]
    present = out[out["presence"] | (out["nuke"] != "—")]
    print(f"scanned {len(out)} series -> "
          f"{len(present)} in a present/nuke state")
    if not present.empty:
        print(present[cols].head(25).to_string(index=False))
    print(f"full scan: {CLUE / 'smh_presence_scan.csv'}")


if __name__ == "__main__":
    main(sys.argv)
