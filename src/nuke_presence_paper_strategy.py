"""Nuke Presence Long - PAPER STRATEGY v0.1 (draft, owner-directed).

Directive (Andrea, 2026-11-18, in-session): "how many more articles are
you gonna read why don't you try build some strategy." Response: the
program's ONLY stability-passed conditional (session 47: the nuke chip -
P(first big move within 60d is UP) = 0.703/0.801 and 0.738/0.802 in the
two temporal halves, against baseline 0.556/0.599) is composed into ONE
pre-registered paper strategy. Multiplicity discipline: ONE strategy, ONE
spec, zero variants - a variant requires a new dated amendment.

PRE-REGISTERED PROTOCOL (declared here BEFORE the run):
  - Universe: every archive series (paper/research/data/*.csv) passing the
    dossier construction gate (NEED bars); daily OHLCV.
  - Signal night t: the causal nuke_down state is on (a >=4-sigma down day
    occurred within the last 2 trading days, trailing-20d sigma known at
    the night) and the night is valid (prior close > 0.01, no delisting
    zero close) - identical construction to the dossiers (37/47).
  - Entry: next day's OPEN after the signal night (the "press one button
    to be present" seat).
  - Episode de-contamination: ONE trade per nuke episode - after an
    entry, further signal nights are suppressed until the trade exits
    (non-overlapping trades per series). This is the answer to the
    session-47 episode-contamination caution.
  - Exit: take-profit at the first day with return >= +4-sigma (the
    dossier's up-move event ITSELF, the thing the chip measures), exit
    at that day's close; time-stop 60 trading days after entry, exit at
    close; whichever comes first. NO stop-loss in v0.1: the down tail is
    not insured, it is MEASURED (MAE and the losing-episode distribution
    are reported raw). Adding a stop requires a new dated amendment.
  - Costs: zero, declared. Slippage: zero, declared. Paper only.
  - Statistics reported (descriptive episode study, NOT validation):
    n episodes, win rate (episode return > 0), mean/median episode
    return, mean holding days, return percentiles (p5/p25/p50/p75/p95),
    mean max-adverse-excursion from entry open, per-half split (h1/h2).
  - IN-SAMPLE HONESTY (the binding caveat): the nuke chip was DISCOVERED
    on this same archive; every number below is an in-sample descriptive
    conditional. The per-half split is the only quasi-independent
    intra-archive check; W2 fresh-window confirmation remains mandatory.
    Nothing armed; nothing trades live.

DATA-QUALITY CORRECTION (declared, run 2, same date): flatlined low-priced
series drive trailing-20d sigma to EXACTLY 0, making |ret| >= 4*sigma
trivially true on zero-return days (391/1335 episodes exited with ret
columns of exactly 0.0 in run 1; e.g. series 'ehf' with constant open==close
bars). The dossier move definitions shared this hole. Correction: all move
flags now additionally require sigma > 0. This is a data-quality guard on
the construction, not a threshold change; the nuke chip stability split is
re-run under the same guard and both runs are reported.
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data")
OUT_CSV = CLUE / "nuke_presence_strategy.csv"
OUT_MD = CLUE / "nuke_presence_strategy.md"

SIGMA_WIN = 20
PCT_WIN = 756
MOVE_SIGMA = 4.0
HOLD_MAX = 60
NUKE_LOOKBACK = 2
NEED = PCT_WIN + SIGMA_WIN + 5


def percentile(a, q):
    return round(float(np.percentile(a, q)), 4) if len(a) else ""


def stats_block(episodes):
    if not episodes:
        return {"n": 0}
    rets = np.array([e["ret"] for e in episodes], dtype=float)
    holds = np.array([e["hold"] for e in episodes], dtype=int)
    maes = np.array([e["mae"] for e in episodes], dtype=float)
    return {
        "n": len(episodes),
        "win_rate": round(float((rets > 0).mean()), 4),
        "mean_ret": round(float(rets.mean()), 4),
        "median_ret": round(float(np.median(rets)), 4),
        "p5_ret": percentile(rets, 5),
        "p25_ret": percentile(rets, 25),
        "p75_ret": percentile(rets, 75),
        "p95_ret": percentile(rets, 95),
        "mean_hold_days": round(float(holds.mean()), 1),
        "median_hold_days": int(np.median(holds)),
        "mean_mae": round(float(maes.mean()), 4),
        "p5_mae": percentile(maes, 5),
    }


def fmt_md(title, row):
    if row.get("n", 0) == 0:
        return f"### {title}\n\n(no episodes)\n"
    keys = list(row.keys())
    cells = " | ".join(k.replace("_", " ") for k in keys)
    vals = " | ".join(str(row[k]) for k in keys)
    return f"### {title}\n\n| {cells} |\n|{'---|' * len(keys)}\n| {vals} |\n"


def main():
    KEYS = ["n", "win_rate", "mean_ret", "median_ret", "p5_ret", "p25_ret",
            "p75_ret", "p95_ret", "mean_hold_days", "median_hold_days",
            "mean_mae", "p5_mae"]

    all_eps = []
    series_count = 0
    for data_file in sorted(DATA.glob("*.csv")):
        try:
            df = pd.read_csv(data_file)
        except Exception:
            continue
        for col in ("open", "high", "low", "close", "volume"):
            if col not in df.columns:
                df = None
                break
        if df is None or len(df) < NEED:
            continue
        df = df.reset_index(drop=True)
        close = pd.Series(df["close"].to_numpy(), dtype=float)
        n = len(df)
        ret = close.pct_change()
        sigma = ret.rolling(SIGMA_WIN).std().shift(1)
        move_up = ((ret >= MOVE_SIGMA * sigma) & (sigma > 0)).to_numpy()
        move_dn = ((ret <= -MOVE_SIGMA * sigma)
                   & (sigma > 0)).astype(float)
        nd = move_dn.rolling(NUKE_LOOKBACK).max().shift(1).to_numpy() > 0
        valid = ((close > 0.01).astype(float).shift(1)
                 .fillna(0.0).to_numpy()) > 0

        op = df["open"].to_numpy(dtype=float)
        hi = df["high"].to_numpy(dtype=float)
        lo = df["low"].to_numpy(dtype=float)
        cl = df["close"].to_numpy(dtype=float)

        series_count += 1
        in_trade_until = -1
        for t in range(n - 1):
            if t <= in_trade_until or not nd[t] or not valid[t]:
                continue
            entry = t + 1
            ep_ret = None
            exit_i = None
            for j in range(entry, min(entry + HOLD_MAX, n)):
                if move_up[j] or j == min(entry + HOLD_MAX, n) - 1 or j == n - 1:
                    exit_i = j
                    break
            if exit_i is None:
                continue
            if op[entry] <= 0 or np.isnan(op[entry]):
                continue
            ep_ret = cl[exit_i] / op[entry] - 1.0
            mae = lo[entry:exit_i + 1].min() / op[entry] - 1.0
            all_eps.append({
                "series": data_file.stem,
                "entry_idx": entry,
                "ret": ep_ret,
                "hold": exit_i - entry + 1,
                "mae": mae,
            })
            in_trade_until = exit_i

    n_eps = len(all_eps)
    pooled_rows = {"ALL (in-sample)": stats_block(all_eps)}

    half_rows = {}
    by_series = {}
    for e in all_eps:
        by_series.setdefault(e["series"], []).append(e)
    h1_eps, h2_eps = [], []
    for sname, eps in by_series.items():
        eps.sort(key=lambda e: e["entry_idx"])
        split = eps[len(eps) // 2]["entry_idx"] if eps else 0
        for e in eps:
            h1_eps.append(e) if e["entry_idx"] <= split else h2_eps.append(e)
    pooled_rows["HALF 1 (earlier, in-sample)"] = stats_block(h1_eps)
    pooled_rows["HALF 2 (later, in-sample)"] = stats_block(h2_eps)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["block"] + KEYS)
        for name, row in pooled_rows.items():
            if row.get("n", 0) == 0:
                continue
            w.writerow([name] + [row.get(k, "") for k in KEYS])
    with open(OUT_CSV, "a", newline="") as f:
        w = csv.writer(f)
        w.writerow([])
        w.writerow(["series", "entry_idx", "ret", "hold", "mae"])
        for e in all_eps:
            w.writerow([e["series"], e["entry_idx"], round(e["ret"], 4),
                        e["hold"], round(e["mae"], 4)])

    md = ["# Nuke Presence Long - PAPER STRATEGY v0.1 (draft, owner-directed)",
          "",
          "One pre-registered rule, zero variants. Signal: causal nuke_down",
          "night (>=4-sigma down day within 2 days). Entry: next open.",
          "One trade per episode. Take-profit: the first >=4-sigma UP day",
          "(the event the chip measures). Time-stop: 60 trading days.",
          "No stop-loss (the down tail is measured, not insured). Zero",
          "costs, zero slippage, declared. ALL NUMBERS IN-SAMPLE: the chip",
          "was discovered on this same archive; the halves are the only",
          "quasi-independent intra-archive check; W2 fresh-window",
          "confirmation mandatory. Nothing armed; nothing trades live.",
          "",
          f"Series scanned: {series_count}; episodes: {n_eps}.",
          ""]
    for name, row in pooled_rows.items():
        md.append(fmt_md(name, row))
        md.append("")
    OUT_MD.write_text("\n".join(md))
    for name, row in pooled_rows.items():
        print(name, row)


if __name__ == "__main__":
    main()
