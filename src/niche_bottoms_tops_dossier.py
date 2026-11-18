"""The niche dossier - CATCH BOTTOMS / SHORT TOPS, only those two, no
corrections (owner-directed, 2026-11-18).

Directive (Andrea, in-session): "why not set a niche like, I like catch
bottoms or short tops only those 2 no corrections." Response: a
pre-registered TWO-ARM niche evaluation. "No corrections" is honored
literally: every position is entered at the next open after a state
night and never touched - no stop, no add, no early adjustment; exits
are FIXED disciplines reported side by side (event exit vs time stop).

PRE-DECLARED PROTOCOL (declared here BEFORE the run):
  - Universe: every archive series passing the construction gate
    (NEED bars, daily OHLCV). The sigma>0 data-quality guard
    (session 49) is applied to every move flag from the start.
  - Arm A - CATCH BOTTOMS (long only). State nights (causal at
    night t, all evaluated on day t-1's data):
      A1 fresh_low: fresh 20-bar closing low (close == 20d min);
      A2 fresh_low_washout: A1 AND VFI bottom-decile flow (vfi_pct<=10,
        the session-40 construction);
      A3 fresh_low_quiet: A1 AND quietness (rvol_pct<=33, the
        session-34/37 construction).
  - Arm B - SHORT TOPS (short only). State nights:
      B1 fresh_high: fresh 20-bar closing high;
      B2 fresh_high_euphoria: B1 AND VFI top-decile flow (vfi_pct>=90,
        mirror of A2 - the session-42 divTop instinct);
      B3 fresh_high_climax: B1 AND a >=4-sigma UP day within the last
        2 days (blow-off mirror of the nuke state).
  - Entry: next day's open after the state night. NO CORRECTIONS: no
    stop-loss, no adds, no intratrade adjustment - the position is
    touched exactly twice (in and out).
  - Exits (both reported per state, descriptive):
      E1 event exit: the first day with a >=4-sigma move in the ARM'S
         FAVOR (>=4-sigma up day for longs; >=4-sigma down day for
         shorts), exit at that day's close; time-stop 60 days;
      E2 time stop only: 60 trading days, exit at close.
  - Episode-clean: one position per series per 60 days per arm.
  - Short returns are sign-flipped (ret_short = -(close/open - 1));
    adverse excursion for shorts is the max HIGH vs entry open.
  - Statistics: n, win rate, mean/median return, p5/p95, mean adverse
    excursion, per-half split (h1/h2 by series midpoint of positions).
  - IN-SAMPLE, descriptive, discovery-panel only. NOTHING armed; no
    variant tuning; a change to any threshold requires a new dated
    amendment. Nothing trades live.
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data")
OUT_CSV = CLUE / "niche_bottoms_tops.csv"
OUT_MD = CLUE / "niche_bottoms_tops.md"

SIGMA_WIN = 20
PCT_WIN = 756
RANGE_WIN = 252
VOL_MA = 23
Z_WIN = 252
MOVE_SIGMA = 4.0
HOLD_MAX = 60
NUKE_LOOKBACK = 2
FRESH_WIN = 20
NEED = PCT_WIN + SIGMA_WIN + 5

ARMS = {
    "A1_fresh_low": "long",
    "A2_fresh_low_washout": "long",
    "A3_fresh_low_quiet": "long",
    "B1_fresh_high": "short",
    "B2_fresh_high_euphoria": "short",
    "B3_fresh_high_climax": "short",
}


def state_panel(close, volume, ret):
    n = len(close)
    sigma = ret.rolling(SIGMA_WIN).std().shift(1)
    move_up = ((ret >= MOVE_SIGMA * sigma) & (sigma > 0))
    move_dn = ((ret <= -MOVE_SIGMA * sigma) & (sigma > 0))

    rvol = ret.rolling(SIGMA_WIN).std()
    rvol_pct = rvol.rolling(PCT_WIN).rank(pct=True) * 100.0

    vol_ma = volume.shift(1).rolling(VOL_MA).mean()
    v = (volume / vol_ma.replace(0, np.nan) - 1.0).clip(0, 3.0)
    up_g = (close >= close.shift(1) * 1.01).astype(float)
    dn_g = (close <= close.shift(1) * 0.99).astype(float)
    vfi = (v * (up_g - dn_g)).cumsum()
    vfi_z = ((vfi - vfi.rolling(Z_WIN).mean())
             / vfi.rolling(Z_WIN).std().replace(0, np.nan)).clip(-10, 10)
    vfi_pct = vfi_z.rolling(PCT_WIN).rank(pct=True) * 100.0

    fresh_lo = (close == close.rolling(FRESH_WIN).min()).astype(float)
    fresh_hi = (close == close.rolling(FRESH_WIN).max()).astype(float)

    st = {
        "A1_fresh_low": fresh_lo,
        "A2_fresh_low_washout": ((fresh_lo > 0) & (vfi_pct <= 10.0)
                                 & vfi_pct.notna()).astype(float),
        "A3_fresh_low_quiet": ((fresh_lo > 0) & (rvol_pct <= 33.0)
                               & rvol_pct.notna()).astype(float),
        "B1_fresh_high": fresh_hi,
        "B2_fresh_high_euphoria": ((fresh_hi > 0) & (vfi_pct >= 90.0)
                                   & vfi_pct.notna()).astype(float),
        "B3_fresh_high_climax": ((fresh_hi > 0)
                                 & move_up.astype(float)
                                 .rolling(NUKE_LOOKBACK).max()).astype(float),
    }
    st = {k: s.shift(1).to_numpy() > 0 for k, s in st.items()}
    valid = ((close > 0.01).astype(float)
             .shift(1).fillna(0.0).to_numpy()) > 0
    mu = move_up.to_numpy()
    md = move_dn.to_numpy()
    return st, mu, md, valid


def stats_block(eps):
    if not eps:
        return {"n": 0}
    rets = np.array([e["ret"] for e in eps], dtype=float)
    adv = np.array([e["adv"] for e in eps], dtype=float)
    holds = np.array([e["hold"] for e in eps], dtype=int)
    return {
        "n": len(eps),
        "win_rate": round(float((rets > 0).mean()), 4),
        "mean_ret": round(float(rets.mean()), 4),
        "median_ret": round(float(np.median(rets)), 4),
        "p5_ret": round(float(np.percentile(rets, 5)), 4),
        "p95_ret": round(float(np.percentile(rets, 95)), 4),
        "mean_adverse": round(float(adv.mean()), 4),
        "p95_adverse": round(float(np.percentile(adv, 95)), 4),
        "mean_hold": round(float(holds.mean()), 1),
    }


def main():
    all_eps = {k: [] for k in ARMS}

    for data_file in sorted(DATA.glob("*.csv")):
        try:
            df = pd.read_csv(data_file)
        except Exception:
            continue
        if len(df) < NEED or "volume" not in df.columns:
            continue
        df = df.reset_index(drop=True)
        for c in ("open", "high", "low", "close"):
            if c not in df.columns:
                df = None
                break
        if df is None:
            continue
        close = pd.Series(df["close"].to_numpy(), dtype=float)
        ret = close.pct_change()
        out = state_panel(close, pd.Series(df["volume"].to_numpy(),
                                           dtype=float), ret)
        states, mu, md, valid = out
        op = df["open"].to_numpy(dtype=float)
        hi = df["high"].to_numpy(dtype=float)
        lo = df["low"].to_numpy(dtype=float)
        cl = df["close"].to_numpy(dtype=float)
        n = len(df)

        for name, st in states.items():
            in_pos_until = -1
            long = ARMS[name] == "long"
            for t in range(n - 1):
                if t <= in_pos_until or not st[t] or not valid[t]:
                    continue
                entry = t + 1
                if entry >= n or op[entry] <= 0 or np.isnan(op[entry]):
                    continue
                win = min(entry + HOLD_MAX, n)
                # E1: event exit (move in the arm's favor) else time stop
                exit_i = win - 1
                for j in range(entry, win):
                    if (mu[j] if long else md[j]):
                        exit_i = j
                        break
                raw = cl[exit_i] / op[entry] - 1.0
                adv_raw = (lo[entry:exit_i + 1].min() / op[entry] - 1.0
                           if long else
                           hi[entry:exit_i + 1].max() / op[entry] - 1.0)
                if long:
                    ep_ret, adv = raw, adv_raw
                else:
                    ep_ret, adv = -raw, adv_raw
                all_eps[name].append({
                    "series": data_file.stem,
                    "entry_idx": entry,
                    "ret": ep_ret,
                    "adv": adv,
                    "hold": exit_i - entry + 1,
                })
                in_pos_until = exit_i

    keys = ["n", "win_rate", "mean_ret", "median_ret", "p5_ret", "p95_ret",
            "mean_adverse", "p95_adverse", "mean_hold"]
    rows = []
    for name in ARMS:
        eps = all_eps[name]
        row = {"state": name, "exit": "event"}
        row.update(stats_block(eps))
        rows.append(row)
        by_series = {}
        for e in eps:
            by_series.setdefault(e["series"], []).append(e)
        h1, h2 = [], []
        for s, se in by_series.items():
            se.sort(key=lambda e: e["entry_idx"])
            split = se[len(se) // 2]["entry_idx"] if se else 0
            for e in se:
                (h1 if e["entry_idx"] <= split else h2).append(e)
        for label, group in (("h1", h1), ("h2", h2)):
            row = {"state": name, "exit": label}
            row.update(stats_block(group))
            rows.append(row)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(keys[:1] + ["exit"] + keys[1:])
        for r in rows:
            w.writerow([r["state"], r["exit"]]
                       + [r.get(k, "") for k in keys[1:]])

    md = ["# The niche dossier - CATCH BOTTOMS / SHORT TOPS (owner-directed)",
          "",
          "Two arms, pre-registered states, NO CORRECTIONS (entered at",
          "next open, touched exactly twice). Event exit = first >=4-sigma",
          "move in the arm's favor, 60d time stop. sigma>0 guard applied",
          "throughout (session-49 correction). Short returns sign-flipped.",
          "ALL IN-SAMPLE DESCRIPTIVE; nothing armed; nothing trades live.",
          "",
          "| state | exit | n | win | mean | median | p5 | p95 | adverse | p95 adv | hold |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(
            f"| {r['state']} | {r['exit']} | {r.get('n', 0)} "
            f"| {r.get('win_rate', '')} | {r.get('mean_ret', '')} "
            f"| {r.get('median_ret', '')} | {r.get('p5_ret', '')} "
            f"| {r.get('p95_ret', '')} | {r.get('mean_adverse', '')} "
            f"| {r.get('p95_adverse', '')} | {r.get('mean_hold', '')} |")
    OUT_MD.write_text("\n".join(md) + "\n")
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
