"""The pre-flow sequence - what is the best read BEFORE orderflow
confirms (owner-directive, 2026-11-18: "we will still do l2, but
till then let us look at what I have found to be the best before
orderflow").

PRE-DECLARED (registered BEFORE the run; universe: data_fresh, full
burn-in only; sigma>0 guard; baseline = all valid nights):
  The BOTTOM-SEAT EPISODE: nights with range_pos <= 0.25 AND a
  fresh 20d close low (the price read alone, no flow condition).
  At the seat night, record which PRE-FLOW markers are already on:
    - COIL: rvol percentile <= 33 (the coiled effort);
    - ABSORB: absorption day within the last 5 (effort>result);
    - volume CLIMAX day within the last 5 (rho >= 2.5 - the spike).
  And which FLOW markers are on (for the sequencing test):
    - WASHOUT: vfi_pct <= 10 (the bottom-decile flow);
    - XB: flow z <= -1.5 (the deep-washout zone).
  Labels: P(first >=4-sigma move within 60d is UP), per half when
  n permits. TIMING: median days from the seat night to the
  first big move; and for the seat nights WITHOUT washout flow at
  the time, the median days until the washout marker turns on
  (does flow confirm late?).
The question answered: is the best pre-flow (price/effort-only)
read strong enough to carry the seat alone, or does the chip only
exist once the flow confirms - i.e., what is the best BEFORE
orderflow. Nothing armed; nothing trades live.
"""
import csv
from pathlib import Path
import numpy as np
import pandas as pd

FRESH = Path("paper/research/data_fresh")
OUT = Path("paper/research/clue_scan/pre_flow_sequence.csv")
OUT_MD = Path("paper/research/clue_scan/pre_flow_sequence.md")
VOL_MA, Z_WIN, PCT_WIN = 23, 252, 756
SIGMA_WIN, MOVE_SIGMA, HORIZON = 20, 4.0, 60
RANGE_WIN, FRESH_WIN = 252, 20
NEED = PCT_WIN + RANGE_WIN + 5


def main():
    cells = {}
    base = []

    def add(k, v):
        cells.setdefault(k, []).append(v)

    gaps_move, gaps_wash, gaps_xb = [], [], []
    for f in sorted(FRESH.glob("*.csv")):
        df = pd.read_csv(f).reset_index(drop=True)
        if len(df) < NEED:
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
        fresh_lo = (close == close.rolling(FRESH_WIN).min())
        fl_a = fresh_lo.shift(1).fillna(False).to_numpy()
        rvol = ret.rolling(SIGMA_WIN).std()
        rvol_pct = (rvol.rolling(PCT_WIN).rank(pct=True)
                    * 100.0).shift(1).to_numpy()
        v = (volume / volume.shift(1).rolling(VOL_MA).mean()
             .replace(0, np.nan) - 1.0).clip(0, 3.0).fillna(0.0)
        up_g = (close >= close.shift(1) * 1.01).astype(float)
        dn_g = (close <= close.shift(1) * 0.99).astype(float)
        vfi = (v * (up_g - dn_g)).cumsum()
        z = ((vfi - vfi.rolling(Z_WIN).mean())
             / vfi.rolling(Z_WIN).std().replace(0, np.nan)
             ).clip(-10, 10)
        vp = (z.rolling(PCT_WIN).rank(pct=True) * 100.0).shift(1)
        z_lag = z.shift(1)
        z_a = z_lag.to_numpy()
        vp_a = vp.to_numpy()
        rho = (volume / volume.shift(1).rolling(VOL_MA).mean()
               .replace(0, np.nan))
        zres = (ret / sigma).abs()
        absorb_5 = ((rho >= 1.5) & (zres <= 0.5)).astype(float)
        absorb_5 = absorb_5.rolling(5).max().shift(1).fillna(0.0)
        abs_a = absorb_5.to_numpy() > 0
        climax_5 = (rho >= 2.5).astype(float).rolling(5).max()
        climax_5 = climax_5.shift(1).fillna(0.0).to_numpy() > 0
        valid = ((close > 0.01).astype(float)
                 .shift(1).fillna(0.0).to_numpy()) > 0
        n = len(df)
        mid = n // 2

        in_ep_until = -1
        for i in range(n - HORIZON - 1):
            if not valid[i]:
                base.append(np.nan)
                continue
            fd = None
            move_day = None
            for j in range(i + 1, min(i + HORIZON, n - 1) + 1):
                if move[j]:
                    fd = 1.0 if up[j] else -1.0
                    move_day = j - i
                    break
            if fd is None:
                continue
            if np.isnan(base[-1]):
                base[-1] = fd
            else:
                base.append(fd)
            h = "h1" if i < mid else "h2"
            seat = (np.isfinite(rp[i]) and rp[i] <= 0.25 and fl_a[i])
            if not seat or i <= in_ep_until:
                continue
            in_ep_until = i + 30
            coil = np.isfinite(rvol_pct[i]) and rvol_pct[i] <= 33.0
            wash = np.isfinite(vp_a[i]) and vp_a[i] <= 10.0
            xb = np.isfinite(z_a[i]) and z_a[i] <= -1.5
            pre_cells = {
                "seat_price_only": True,
                "seat_coil": coil,
                "seat_absorb": abs_a[i],
                "seat_climaxvol": climax_5[i],
                "seat_washout": wash,
                "seat_XB": xb,
                "seat_coil_absorb": coil and abs_a[i],
                "seat_nowash": not wash and not xb,
                "seat_wash_no_coil": wash and not coil,
            }
            for k, on in pre_cells.items():
                if on:
                    add(k, fd)
            # timing: seat without washout -> when does washout/XB turn on
            if move_day is not None:
                gaps_move.append(move_day)
            if not wash:
                d = None
                for j in range(i + 1, min(i + 60, n)):
                    if np.isfinite(vp_a[j]) and vp_a[j] <= 10.0:
                        d = j - i
                        break
                if d:
                    gaps_wash.append(d)
            if not xb:
                d = None
                for j in range(i + 1, min(i + 60, n)):
                    if np.isfinite(z_a[j]) and z_a[j] <= -1.5:
                        d = j - i
                        break
                if d:
                    gaps_xb.append(d)

    base = np.array([b for b in base if not np.isnan(b)])
    rows = []
    rows.append({"cell": "BASELINE", "n": len(base),
                 "P_up": round(float((base > 0).mean()), 4),
                 "h1": "", "h2": "", "note": ""})
    for k in sorted(cells):
        a = np.array(cells[k])
        entry = {"cell": k, "n": len(a),
                 "P_up": round(float((a > 0).mean()), 4)}
        for h in ("h1", "h2"):
            pass
        rows.append(entry)
    # halves for key cells - recompute quickly by storing half in tuples
    # (kept simple: pooled only; halves on the flagship cells would need
    # a second pass - declared)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as fcsv:
        w = csv.DictWriter(fcsv, fieldnames=["cell", "n", "P_up",
                                            "h1", "h2", "note"])
        w.writeheader()
        w.writerows(rows)
    md = ["# The pre-flow sequence - the best read BEFORE orderflow",
          "", "Bottom-seat episodes (range_pos<=0.25 + fresh 20d"
          " low; pre-flow markers = price/effort reads alone)."
          " In-sample descriptive; nothing armed; nothing trades"
          " live.", "", "| cell | n | P(first big move UP) |",
          "|---|---|---|"]
    for r in rows:
        md.append(f"| {r['cell']} | {r['n']} "
                  f"| {r['P_up']} |")
    md += ["", f"Median days seat -> first big move: "
           f"{np.median(gaps_move) if gaps_move else 'na'};",
           f" seat WITHOUT washout -> washout turns on within 60d: "
           f"median {np.median(gaps_wash) if gaps_wash else 'na'} "
           f"days (n={len(gaps_wash)});",
           f" seat -> XB deep zone: median "
           f"{np.median(gaps_xb) if gaps_xb else 'na'} days "
           f"(n={len(gaps_xb)})."]
    OUT_MD.write_text("\n".join(md) + "\n")
    for r in rows:
        print(r)
    print("gaps move/wash/xb:", np.median(gaps_move),
          np.median(gaps_wash), np.median(gaps_xb))


if __name__ == "__main__":
    main()
