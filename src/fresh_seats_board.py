"""The fresh seats board - who is in which measured seat RIGHT NOW
(owner-directed: "charts my guy, go get dailies 1356 length or 144
or 89 weekly").

Fresh daily cache: paper/research/data_fresh/ (1356 bars, fetched
this session, overlaps the archive vintage - this board is a
CURRENT-STATE observation display, NOT a W2 confirmation; the fresh
windows still owe their registered confirmation).

Per pair, all causal at the latest bar:
  rvol_pct (20d vol percentile, 756d), range_pos (252d),
  fresh 20d low/high, vfi_pct (session-40 flow percentile),
  last completed grammar leg (dir, size, dur, wake),
  weekly 89/144 momentum signs (W-FRI aggregation, owner lengths),
  nuke states (>=4-sigma day within 2 days, sigma>0-guarded),
  absorption day flag (rho>=1.5 & z<=0.5).
SEATS (registered compositions, printed with their measured chips):
  FLAGSHIP_BOTTOM  = bottom 20% range + fresh 20d low + vfi <= 10
                    (the A2 washout seat; with U-base leg shape ->
                    the 0.731 formation)
  ABSORBED_LOW     = low third + absorption day within last 5 bars
  PRESENCE         = quiet (rvol_pct<=33) base (0.645 seat)
  NEAR             = base x vfi_ext_low (0.601)
  DIVTOP_EXIT      = fresh 20d high with flow fade (0.481 exit read)
  NUKE_STATE       = within 2 days of a >=4-sigma day
Nothing armed; nothing trades live; the board is an observation
display exactly like the owner's AVFI panel.
"""
import csv
from pathlib import Path
import numpy as np
import pandas as pd

from chart_grammar_dossier import pivots_legs

FRESH = Path("paper/research/data_fresh")
OUT = Path("paper/research/clue_scan/fresh_seats_board.csv")

VOL_MA, Z_WIN, PCT_WIN = 23, 252, 756
SIGMA_WIN, MOVE_SIGMA, RANGE_WIN, FRESH_WIN = 20, 4.0, 252, 20


def flow_pct(close, volume):
    v = (volume / volume.shift(1).rolling(VOL_MA).mean()
         .replace(0, np.nan) - 1.0).clip(0, 3.0).fillna(0.0)
    up_g = (close >= close.shift(1) * 1.01).astype(float)
    dn_g = (close <= close.shift(1) * 0.99).astype(float)
    vfi = (v * (up_g - dn_g)).cumsum()
    z = ((vfi - vfi.rolling(Z_WIN).mean())
         / vfi.rolling(Z_WIN).std().replace(0, np.nan)).clip(-10, 10)
    return z.rolling(PCT_WIN).rank(pct=True) * 100.0


def main():
    rows = []
    for f in sorted(FRESH.glob("*.csv")):
        df = pd.read_csv(f)
        if len(df) < 800:
            continue
        df = df.reset_index(drop=True)
        for c in ("open", "high", "low", "close", "volume"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
        close = pd.Series(df["close"].to_numpy(), dtype=float)
        high = pd.Series(df["high"].to_numpy(), dtype=float)
        low = pd.Series(df["low"].to_numpy(), dtype=float)
        volume = pd.Series(df["volume"].to_numpy(), dtype=float)
        n = len(close)
        ret = close.pct_change()
        sigma = ret.rolling(SIGMA_WIN).std()
        rvol = ret.rolling(SIGMA_WIN).std()
        rvol_pct = rvol.rolling(PCT_WIN).rank(pct=True) * 100.0
        rho = volume / volume.shift(1).rolling(VOL_MA).mean()
        rho_vol_lag = (volume / volume.shift(1).rolling(VOL_MA)
                       .mean().replace(0, np.nan))
        z = (ret / sigma).abs()
        rng_hi = high.rolling(RANGE_WIN).max()
        rng_lo = low.rolling(RANGE_WIN).min()
        rp = (close - rng_lo) / (rng_hi - rng_lo).replace(0, np.nan)
        fresh_lo = close == close.rolling(FRESH_WIN).min()
        fresh_hi = close == close.rolling(FRESH_WIN).max()
        vp = flow_pct(close, volume)
        up_g = (close >= close.shift(1) * 1.01).astype(float)
        dn_g = (close <= close.shift(1) * 0.99).astype(float)

        move_up = (ret >= MOVE_SIGMA * sigma) & (sigma > 0)
        move_dn = (ret <= -MOVE_SIGMA * sigma) & (sigma > 0)
        nuke = (move_up | move_dn)
        nuke_recent = bool(nuke.iloc[-3:].any())

        legs = pivots_legs(high.to_numpy(), low.to_numpy(),
                           close.to_numpy(), sigma.shift(1).to_numpy())
        last_leg = legs[-1]["sym"] if legs else ""
        leg_kind = (last_leg if not nuke_recent else "")

        w = pd.Series(close.to_numpy(),
                      index=pd.to_datetime(df["date"])).resample(
            "W-FRI").last().dropna()
        m89 = (np.log(w.iloc[-1] / w.iloc[-89]) > 0
               if len(w) > 89 else None)
        m144 = (np.log(w.iloc[-1] / w.iloc[-144]) > 0
                if len(w) > 144 else None)

        rvol_pct_v = rvol_pct.iloc[-1]
        rp_v = rp.iloc[-1]
        vp_v = vp.iloc[-1]
        fl_v = bool(fresh_lo.iloc[-1])
        fh_v = bool(fresh_hi.iloc[-1])
        abs_recent = bool(((rho_vol_lag >= 1.5) & (z <= 0.5))
                          .iloc[-5:].any())
        date = df["date"].iloc[-1]

        seats = []
        if rp_v <= 0.20 and fl_v and vp_v <= 10.0:
            seats.append("FLAGSHIP_BOTTOM" +
                         ("+U_BASE" if last_leg[0] == "U"
                          and last_leg[3] == "b" else ""))
        elif rp_v <= 1/3 and abs_recent:
            seats.append("ABSORBED_LOW")
        if rvol_pct_v <= 33.0 and rp_v is not None and rp_v <= 0.30:
            if not seats:
                seats.append("PRESENCE(quiet base)")
        if fh_v and vp_v is not None and vp_v >= 90.0:
            seats.append("DIVTOP_EXIT(flow fade read)")
        if nuke_recent:
            seats.append("NUKE_STATE")

        rows.append({
            "pair": f.stem, "date": date,
            "rvol_pct": round(rvol_pct_v, 1) if np.isfinite(rvol_pct_v)
            else "",
            "range_pos": round(rp_v, 2) if np.isfinite(rp_v) else "",
            "vfi_pct": round(vp_v, 1) if np.isfinite(vp_v) else "",
            "fresh_low": fl_v, "fresh_high": fh_v,
            "last_leg": last_leg, "abs_recent_low": (
                abs_recent and rp_v <= 1/3),
            "m89w": "" if m89 is None else ("UP" if m89 else "DOWN"),
            "m144w": "" if m144 is None else ("UP" if m144 else "DOWN"),
            "seat": ("; ".join(seats) if seats else "-")
            + ("" if str(date) >= "2026-11-11" else " [STALE VINTAGE"
               " - pair stopped trading]"),
        })

    with open(OUT, "w", newline="") as fcsv:
        w = csv.DictWriter(fcsv, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    in_seat = [r for r in rows if r["seat"] != "-"]
    print(f"board: {len(rows)} pairs, {len(in_seat)} in a seat")
    for r in sorted(in_seat, key=lambda r: r["seat"])[:40]:
        print(r)


if __name__ == "__main__":
    main()
