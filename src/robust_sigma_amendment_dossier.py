"""The robust-sigma amendment comparison - what the library taught the
formula (owner-challenged, 2026-11-18).

Directive (Andrea, in-session): "all those articles have taught you
nothing to modify the formula or anything?" Response: the library's
port ledger exists, and the session-48 read (Filimonov-Sornette
apparent-criticality critique) licenses exactly ONE concrete
construction amendment for the dossiers' own formula: moment-based
scale estimators (trailing-20d STDEV of returns) are outlier-fragile
on fat-tailed data - the critique demonstrated synthetic criticality
from tiny outlier fractions, and its remedy is robust
median/quartile scale (PDF pp. 8, 34); the owner's own AVFI v3.2
robust-z layer (IQR, median/quartiles, prior-bar window) is the same
lesson already applied on their side.

PRE-DECLARED PROTOCOL (declared here BEFORE the run):
  - This session does NOT change the registered construction. It runs
    the REGISTERED moment sigma and the CANDIDATE robust sigma side by
    side and reports the deltas; the amendment is QUEUED PENDING OWNER
    RATIFICATION and nothing is swapped until the owner's word.
  - registered: sigma_m = stdev of trailing-20d returns, shifted
    (prior-night known); sigma>0 guard (session 49) on both variants.
  - candidate: sigma_r = 1.4826 * median(|r - median(r)|) over the
    same trailing-20d window, similarly shifted (MAD scale; the
    same robust-scale family as the owner's AVFI v3.2 IQR layer).
  - measured under BOTH scales: (1) the chip states (all/nuke_down/
    nuke_up): P(first move within 60d is UP) per half (h1/h2);
    (2) the A2 washout-bottom niche arm (session 50): n, win rate,
    mean/median episode return per half, event-exit discipline
    unchanged (first >=4-sigma UP day under the scale in question,
    60d time stop, one position per 60 days, no corrections).
  - Also report the move densities: P(any >=4-sigma day) under each
    scale (the robust scale changes the event RATE, not only the
    direction shares - both must be seen).
  - ALL numbers in-sample descriptive; this is a construction
    comparison, NOT a ratification; nothing armed; nothing trades
    live.
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data")
OUT_CSV = CLUE / "robust_sigma_comparison.csv"
OUT_MD = CLUE / "robust_sigma_comparison.md"

SIGMA_WIN = 20
PCT_WIN = 756
VOL_MA = 23
Z_WIN = 252
MOVE_SIGMA = 4.0
MOVE_HORIZON = 60
NUKE_LOOKBACK = 2
FRESH_WIN = 20
HOLD_MAX = 60
NEED = PCT_WIN + SIGMA_WIN + 5


def build(close, volume, robust):
    n = len(close)
    close = pd.Series(close, dtype=float)
    ret = close.pct_change()
    if robust:
        med = ret.rolling(SIGMA_WIN).median()
        mad = (ret - med).abs().rolling(SIGMA_WIN).median()
        sigma = (1.4826 * mad).shift(1)
    else:
        sigma = ret.rolling(SIGMA_WIN).std().shift(1)
    ok = sigma > 0
    move = ((ret.abs() >= MOVE_SIGMA * sigma) & ok)
    move_up = ((ret >= MOVE_SIGMA * sigma) & ok)
    move_dn = ((ret <= -MOVE_SIGMA * sigma) & ok)
    nd = move_dn.astype(float).rolling(NUKE_LOOKBACK).max().shift(1) > 0
    nu = move_up.astype(float).rolling(NUKE_LOOKBACK).max().shift(1) > 0

    vol_ma = volume.shift(1).rolling(VOL_MA).mean()
    v = (volume / vol_ma.replace(0, np.nan) - 1.0).clip(0, 3.0)
    up_g = (close >= close.shift(1) * 1.01).astype(float)
    dn_g = (close <= close.shift(1) * 0.99).astype(float)
    vfi = (v * (up_g - dn_g)).cumsum()
    vfi_z = ((vfi - vfi.rolling(Z_WIN).mean())
             / vfi.rolling(Z_WIN).std().replace(0, np.nan)).clip(-10, 10)
    vfi_pct = vfi_z.rolling(PCT_WIN).rank(pct=True) * 100.0

    fresh_lo = (close == close.rolling(FRESH_WIN).min()).astype(float)
    a2 = ((fresh_lo > 0) & (vfi_pct <= 10.0)
          & vfi_pct.notna()).astype(float).shift(1) > 0
    valid = ((close > 0.01).astype(float)
             .shift(1).fillna(0.0).to_numpy()) > 0

    return {
        "ret": ret.to_numpy(),
        "move": move.to_numpy(),
        "move_up": move_up.to_numpy(),
        "nd": nd.to_numpy(),
        "nu": nu.to_numpy(),
        "a2": a2.to_numpy(),
        "valid": valid,
    }


def collect(col, label):
    chips = {(h, s): [] for h in ("h1", "h2")
             for s in ("all", "nuke_down", "nuke_up")}
    dens = {"h1": [], "h2": []}
    a2_eps = []
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
        p = build(df["close"].to_numpy(),
                  pd.Series(df["volume"].to_numpy(), dtype=float),
                  label == "robust_mad_candidate")
        n = len(df)
        op = df["open"].to_numpy(dtype=float)
        cl = df["close"].to_numpy(dtype=float)
        valid = p["valid"]

        mid = n // 2
        move_a = p["move"]
        up_a = p["move_up"]
        for i in range(n - MOVE_HORIZON - 1):
            if not valid[i]:
                continue
            h = "h1" if i < mid else "h2"
            dens[h].append(1.0 if move_a[i + 1] else 0.0)
            for j in range(i + 1, min(i + MOVE_HORIZON, n - 1) + 1):
                if move_a[j]:
                    chips[(h, "all")].append(1.0 if up_a[j] else -1.0)
                    break
            if p["nd"][i]:
                for j in range(i + 1, min(i + MOVE_HORIZON, n - 1) + 1):
                    if move_a[j]:
                        chips[(h, "nuke_down")].append(
                            1.0 if up_a[j] else -1.0)
                        break
            if p["nu"][i]:
                for j in range(i + 1, min(i + MOVE_HORIZON, n - 1) + 1):
                    if move_a[j]:
                        chips[(h, "nuke_up")].append(
                            1.0 if up_a[j] else -1.0)
                        break

        in_pos_until = -1
        for t in range(n - 1):
            if t <= in_pos_until or not p["a2"][t] or not valid[t]:
                continue
            entry = t + 1
            if entry >= n or op[entry] <= 0 or np.isnan(op[entry]):
                continue
            win = min(entry + HOLD_MAX, n)
            exit_i = win - 1
            for j in range(entry, win):
                if p["move_up"][j]:
                    exit_i = j
                    break
            a2_eps.append({
                "ret": cl[exit_i] / op[entry] - 1.0,
                "series": data_file.stem,
                "entry": entry,
            })
            in_pos_until = exit_i

    rows = []
    for s in ("all", "nuke_down", "nuke_up"):
        for h in ("h1", "h2"):
            arr = np.array(chips[(h, s)])
            rows.append({
                "scale": label, "block": f"{s}_{h}",
                "n": len(arr),
                "value": round(float((arr > 0).mean()), 4) if len(arr) else "",
            })
    for h in ("h1", "h2"):
        m = np.array(dens[h])
        rows.append({
            "scale": label, "block": f"move_density_nextday_{h}",
            "n": len(m),
            "value": round(float(m.mean()), 4),
        })
    by_s = {}
    for e in a2_eps:
        by_s.setdefault(e["series"], []).append(e)
    h1_eps, h2_eps = [], []
    for sname, eset in by_s.items():
        eset.sort(key=lambda e: e["entry"])
        split = eset[len(eset) // 2]["entry"] if eset else 0
        for e in eset:
            (h1_eps if e["entry"] <= split else h2_eps).append(e)
    eps_all = np.array([e["ret"] for e in a2_eps])
    eps_h1 = np.array([e["ret"] for e in h1_eps])
    eps_h2 = np.array([e["ret"] for e in h2_eps])
    for name, arr in (("A2_all", eps_all), ("A2_h1", eps_h1),
                      ("A2_h2", eps_h2)):
        if len(arr):
            rows.append({
                "scale": label, "block": f"{name}_win_rate",
                "n": len(arr),
                "value": round(float((arr > 0).mean()), 4),
            })
            rows.append({
                "scale": label, "block": f"{name}_mean",
                "n": len(arr),
                "value": round(float(arr.mean()), 4),
            })
    return rows


def main():
    rows = collect(False, "moment_std_registered") + \
        collect(True, "robust_mad_candidate")
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["scale", "block", "n", "value"])
        w.writeheader()
        w.writerows(rows)

    md = ["# Robust-sigma amendment comparison - what the library taught",
          "",
          "Filimonov-Sornette (session 48): moment-based scale estimators",
          "are outlier-fragile on fat-tailed returns; robust median/quartile",
          "scale is the remedy (their pp. 8, 34) - the same lesson as the",
          "owner's AVFI v3.2 robust-z IQR layer. Registered moment sigma",
          "vs candidate robust MAD sigma (1.4826 x median absolute",
          "deviation, trailing 20d, prior-night). sigma>0 guard on both.",
          "Construction COMPARISON only; the amendment is QUEUED PENDING",
          "OWNER RATIFICATION; nothing swapped; nothing armed; nothing",
          "trades live.",
          "",
          "| scale | block | n | value |",
          "|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['scale']} | {r['block']} | {r['n']} "
                  f"| {r['value']} |")
    OUT_MD.write_text("\n".join(md) + "\n")
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
