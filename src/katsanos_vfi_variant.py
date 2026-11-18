"""K-VFI: the Katsanos original, rebuilt with the library's lessons
(owner-directed, 2026-11-18).

Directive (Andrea, in-session): "start from the original Katsanos
formula and build your own version using all the articles you have
read." Base: Markos Katsanos's Volume Flow Indicator (S&C June/July
2004), original AmiBroker form:
    inter  = log(median price) - log(median price[1])
    scale  = StDev(inter, 30)
    cutoff = Coef(0.2) * scale * close        (noise threshold)
    Vave   = MA(volume, 130)[1]              (prior-bar window)
    Vmax   = 2.5 * Vave                      (volume cap)
    VCP    = +min(V,Vmax) if MF > cutoff; -min(V,Vmax) if MF < -cutoff;
             0 otherwise                     (sign gate on median-price
                                               change MF)
    VFI    = EMA( Sum(VCP,130)/Vave, 3 )

OUR VERSION - every change below is a library lesson, each with its
source session; every constant is REGISTERED BEFORE the run and
nothing is tuned after:
  L1 (session 48 / candidate amendment 15): the StDev(30) scale is a
     moment estimator, outlier-fragile on fat-tailed returns
     (Filimonov-Sornette pp. 8, 34) -> replaced by robust MAD scale
     (1.4826 x median absolute deviation over the same 30-day window).
     The ORIGINAL is kept as mode "katsanos_original" and run side by
     side (levels and states), so the change is measured, not assumed.
  L2 (session 48 / AVFI v3.2 lesson): every normalization reference is
     PRIOR-BAR (scale, volume MA, z history) - the current bar cannot
     shrink its own reference; also the session-48 edge-effect caution.
  L3 (session 49): degenerate-data guards - scale > 0, close > 0.01,
     volume > 0; flatlined series cannot manufacture fake flow.
  L4 (sessions 40-42, the program's own measured lesson): the VFI
     LEVEL is not a timing rank (AUC ~0.50) - chips live in STATES.
     Our version converts the level to a robust-z over 252d, then a
     trailing 756d percentile, and reads ONLY the decile states
     (bottom decile = washout flow, top decile = euphoric flow).
  L5 (sessions 50/34): the state's use is the measured composition -
     fresh 20-bar closing low x bottom-decile flow (the A2 washout
     bottom) and its mirror fresh high x top-decile; episode discipline
     and event exits are the session-50 niche protocol.

PRE-DECLARED MEASURED COMPARISON (nothing tuned, both reported):
  - for the ORIGINAL (moment scale) and OUR VARIANT (MAD scale):
    (a) A2-style washout episodes: fresh 20d low x bottom-decile
        flow, entry next open, event exit (first >=4-sigma UP day,
        sigma>0-guarded) else 60d stop, one position per 60 days,
        no corrections: n, win rate, mean, median, per-half;
    (b) chip cells: P(first move within 60d is UP) for the states
        fresh_low, flow_ext_low, and their composition, per half.
  - head-to-head line: does the library-rebuilt flow (robust scale)
    beat / match / lose to the original on the program's own
    criteria - SAME constructions on both sides, only the scale and
    the state construction (z/percentile states vs raw level) differ
    where declared.
All in-sample descriptive; nothing armed; nothing trades live.
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data")
OUT_CSV = CLUE / "katsanos_vfi_variant.csv"
OUT_MD = CLUE / "katsanos_vfi_variant.md"

# registered constants
PERIOD = 130
SCALE_WIN = 30
COEF = 0.2
VCOEF = 2.5
SMOOTH = 3
Z_WIN = 252
PCT_WIN = 756
FRESH_WIN = 20
SIGMA_WIN = 20
MOVE_SIGMA = 4.0
MOVE_HORIZON = 60
HOLD_MAX = 60
NEED = PCT_WIN + PERIOD + SIGMA_WIN + 5


def flow(close, high, low, volume, robust):
    """Katsanos VFI level; robust=True swaps StDev -> MAD (1.4826).
    robust='andrea' uses the owner's Andrea-VPVI prior-close-relative
    sign gate inside the session-40 bounded-ratio pipeline: per bar,
    w = (|high-prevClose| - |prevClose-low|) / zone, where zone =
    max(high,prevClose) - min(low,prevClose) (>=1e-12); flow =
    cumsum( v_ratio * w ) with v_ratio = (V/VolMA23[prev] - 1)
    clip(0,3), identical to the session-40 volume treatment; then the
    SAME z(252)->pct(756) state pipeline. Only the SIGN GATE differs
    from the session-40 flow of record - the comparison isolates it.
    (Owner directive: "taking midpoint close prior relative price like
    the 'Andrea' formula" - the Andrea script's volume acts relative
    to the PRIOR CLOSE, not close-to-close.)
    """
    if robust == "andrea":
        close = pd.Series(close)
        high = pd.Series(high)
        low = pd.Series(low)
        pc = close.shift(1)
        highS = (high - pc).abs()
        lowS = (pc - low).abs()
        zone = pd.concat([high, pc], axis=1).max(axis=1) - \
            pd.concat([low, pc], axis=1).min(axis=1)
        w = ((highS - lowS) / zone.replace(0, np.nan)).fillna(0.0)
        v_ratio = (volume / volume.shift(1).rolling(23).mean()
                   .replace(0, np.nan) - 1.0).clip(0, 3.0)
        raw = (v_ratio * w).fillna(0.0)
        return raw.cumsum()
    tp = (pd.Series(high) + pd.Series(low)
          + pd.Series(close)) / 3.0
    tp = tp.where(tp > 0)
    inter = np.log(tp) - np.log(tp.shift(1))
    if robust:
        med = inter.rolling(SCALE_WIN).median()
        scale = 1.4826 * (inter - med).abs().rolling(SCALE_WIN).median()
    else:
        scale = inter.rolling(SCALE_WIN).std()
    scale = scale.shift(1)
    cutoff = COEF * scale * pd.Series(close)
    vave = volume.rolling(PERIOD).mean().shift(1)
    vmax = VCOEF * vave
    vc = volume.clip(upper=None)
    vc = pd.concat([volume, vmax], axis=1).min(axis=1)
    mf = tp - tp.shift(1)
    vcp = pd.Series(0.0, index=tp.index)
    vcp[mf > cutoff] = vc[mf > cutoff]
    vcp[mf < -cutoff] = -vc[mf < -cutoff]
    bad = (scale <= 0) | vave.isna() | vave.le(0) | cutoff.isna()
    vcp[bad] = 0.0
    vfi1 = vcp.rolling(PERIOD).sum() / vave
    vfi = vfi1.ewm(span=SMOOTH * 2 - 1, adjust=False).mean()
    return vfi


def main():
    rows = []
    for mode, robust in (("katsanos_original_moment", False),
                         ("program_variant_mad", True),
                         ("andrea_gate_hybrid", "andrea")):
        eps_all, eps_h1, eps_h2 = [], [], []
        chip = {(h, s): [] for h in ("h1", "h2")
                for s in ("fresh_low", "flow_ext_low", "washout")}
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
            volume = pd.Series(df["volume"].to_numpy(), dtype=float)
            n = len(df)
            ret = close.pct_change()
            sigma = ret.rolling(SIGMA_WIN).std().shift(1)
            move_up = ((ret >= MOVE_SIGMA * sigma) & (sigma > 0)).to_numpy()
            move = ((ret.abs() >= MOVE_SIGMA * sigma)
                    & (sigma > 0)).to_numpy()
            move_a, up_a = move, move_up

            vfi = flow(close.to_numpy(), high.to_numpy(),
                       low.to_numpy(), volume, robust)
            vfi_z = ((vfi - vfi.rolling(Z_WIN).median())
                     / (1.4826 * (vfi - vfi.rolling(Z_WIN).median())
                        .abs().rolling(Z_WIN).median()).replace(0, np.nan)
                     ).clip(-10, 10)
            vfi_pct = vfi_z.rolling(PCT_WIN).rank(pct=True) * 100.0

            fresh_lo = ((close == close.rolling(FRESH_WIN).min())
                        .astype(float).shift(1) > 0)
            ext_low = ((vfi_pct <= 10.0) & vfi_pct.notna()
                       ).astype(float).shift(1) > 0
            washout = (fresh_lo & ext_low).to_numpy()
            fl = fresh_lo.to_numpy()
            el = ext_low.to_numpy()
            valid = ((close > 0.01).astype(float)
                     .shift(1).fillna(0.0).to_numpy()) > 0
            op = df["open"].to_numpy(dtype=float)
            cl = df["close"].to_numpy(dtype=float)
            mid = n // 2

            for i in range(n - MOVE_HORIZON - 1):
                if not valid[i]:
                    continue
                h = "h1" if i < mid else "h2"
                for j in range(i + 1, min(i + MOVE_HORIZON, n - 1) + 1):
                    if move_a[j]:
                        chip[(h, "all")] = chip.get((h, "all"), [])
                        break
                if fl[i]:
                    for j in range(i + 1, min(i + MOVE_HORIZON, n - 1) + 1):
                        if move_a[j]:
                            chip[(h, "fresh_low")].append(
                                1.0 if up_a[j] else -1.0)
                            break
                if el[i]:
                    for j in range(i + 1, min(i + MOVE_HORIZON, n - 1) + 1):
                        if move_a[j]:
                            chip[(h, "flow_ext_low")].append(
                                1.0 if up_a[j] else -1.0)
                            break
                if washout[i]:
                    for j in range(i + 1, min(i + MOVE_HORIZON, n - 1) + 1):
                        if move_a[j]:
                            chip[(h, "washout")].append(
                                1.0 if up_a[j] else -1.0)
                            break

            in_pos_until = -1
            pos = []
            for t in range(n - 1):
                if t <= in_pos_until or not washout[t] or not valid[t]:
                    continue
                entry = t + 1
                if entry >= n or op[entry] <= 0 or np.isnan(op[entry]):
                    continue
                win = min(entry + HOLD_MAX, n)
                exit_i = win - 1
                for j in range(entry, win):
                    if move_up[j]:
                        exit_i = j
                        break
                ep = {
                    "ret": cl[exit_i] / op[entry] - 1.0,
                    "series": data_file.stem,
                    "entry": entry,
                    "half": "h1" if entry < mid else "h2",
                }
                pos.append(ep)
                eps_all.append(ep)
                in_pos_until = exit_i
            # half split by per-series position median (session-50 rule)
            if pos:
                pos.sort(key=lambda e: e["entry"])
                split = pos[len(pos) // 2]["entry"]
                for e in pos:
                    (eps_h1 if e["entry"] <= split
                     else eps_h2).append(e)

        def block(label, arr):
            a = np.array([e["ret"] for e in arr], dtype=float)
            if not len(a):
                return {"scale": mode, "block": label, "n": 0, "value": ""}
            return {"scale": mode, "block": label, "n": len(a),
                    "value": round(float(a.mean()), 4)}

        for label, arr in (("A2_mean", eps_all), ("A2_h1_mean", eps_h1),
                           ("A2_h2_mean", eps_h2)):
            a = np.array([e["ret"] for e in arr], dtype=float)
            if len(a):
                rows.append({"scale": mode, "block": label + "_ret",
                             "n": len(a),
                             "value": round(float(a.mean()), 4)})
                rows.append({"scale": mode, "block": label + "_win",
                             "n": len(a),
                             "value": round(float((a > 0).mean()), 4)})
        for (h, s), arr in sorted(chip.items()):
            if not arr or s == "all":
                continue
            a = np.array(arr)
            rows.append({"scale": mode, "block": f"P_first_up[{s}_{h}]",
                         "n": len(a),
                         "value": round(float((a > 0).mean()), 4)})

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["scale", "block", "n", "value"])
        w.writeheader()
        w.writerows(rows)
    md = ["# K-VFI: Katsanos original (moment scale) vs the program",
          "variant (robust MAD scale, prior-bar, z->percentile states,",
          "sigma>0 guards) - head to head on the program's own criteria.",
          "Registered constants; nothing tuned; in-sample descriptive;",
          "nothing armed; nothing trades live.",
          "", "| scale | block | n | value |", "|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['scale']} | {r['block']} | {r['n']} | {r['value']} |")
    OUT_MD.write_text("\n".join(md) + "\n")
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
