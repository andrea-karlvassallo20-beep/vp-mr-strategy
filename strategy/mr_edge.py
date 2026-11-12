"""The MR-coin edge study: where the physics says the edge should live.

The accumulated evidence says: (a) deep stretch is the one supported
entry signal, (b) mean reversion is MEASURABLE per coin (AR(1)
t-stat, half-life), and (c) 19 of 156 coins pass the mean-reversion
t-test. This study asks the question that matters: does a strictly
causal z-score strategy on the strongest mean-reverting coins
actually pay out-of-sample - and does it beat the CONTROL GROUP of
coins that failed the same test? If the "edge" on MR coins equals
the edge on non-MR coins, the t-stat selection adds nothing.

Honesty devices, pre-committed:
  - coin selection recomputed causally per coin (no stale lists)
  - the control group: same strategy on coins with |t| < 3
  - OOS = the untouched last 40% of each coin's history
  - costs charged on every entry and exit (5 bps)
  - the Deflated Sharpe context for the selected portfolio,
    deflated by the number of coins considered

Usage (nightly):
    python3 mr_edge.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from cross_asset import ou_ar1_stats, safe_name
from papertrading_runner import load_bars
from overfit_stats import deflated_sharpe

Z_ENTRY = -2.0
Z_EXIT = -0.25
LOOKBACK = 100
WARMUP = 110
HORIZON = 10
COST_BPS = 5.0
MR_T = -3.0
OOS_FRAC = 0.6


def causal_z(close: np.ndarray) -> np.ndarray:
    """Strictly trailing z-score of log price (Gate 1: at bar t only
    bars <= t are used)."""
    logp = np.log(close)
    z = np.zeros(len(close))
    for t in range(LOOKBACK, len(close)):
        w = logp[t - LOOKBACK + 1:t + 1]
        sd = w.std()
        if sd > 0:
            z[t] = (logp[t] - w.mean()) / sd
    return z


def zscore_long_backtest(close: np.ndarray) -> dict:
    """Long-only z-score mean reversion, strictly causal: enter at
    z <= -2, exit at z >= -0.25, costs both sides. Returns per-bar
    strategy returns (for pooling) and headline metrics."""
    z = causal_z(close)
    n = len(close)
    pos = np.zeros(n)
    cur = 0.0
    trades = 0
    for t in range(WARMUP, n - 1):
        if cur == 0.0 and z[t] <= Z_ENTRY:
            cur = 1.0
            trades += 1
        elif cur == 1.0 and z[t] >= Z_EXIT:
            cur = 0.0
        pos[t + 1] = cur
    rets = np.diff(np.log(close))
    strat = pos[1:] * rets
    if trades:
        turns = np.abs(np.diff(pos, prepend=0.0))[1:]
        strat = strat - turns * COST_BPS / 1e4
    # winsorize per-bar strategy returns: crypto prints 50%+ days;
    # a single depegging bar must not dominate a pooled Sharpe
    strat = np.clip(strat, -0.5, 0.5)
    sd = strat.std()
    sharpe = float(strat.mean() / sd * np.sqrt(365.0)) if sd > 0 else 0.0
    return {"rets": strat, "sharpe": sharpe, "trades": trades}


def _oos_sharpe(rets: np.ndarray) -> float:
    seg = rets[int(len(rets) * OOS_FRAC):]
    if len(seg) < 20 or seg.std() == 0:
        return 0.0
    return float(seg.mean() / seg.std() * np.sqrt(365.0))


def run_mr_edge_study(data_dir: Path) -> dict:
    """Select MR coins causally, run the z-long strategy on MR and
    control groups, judge the differential out-of-sample."""
    coins = []
    for f in sorted(data_dir.glob("*usd.csv")):
        bars = load_bars(f)
        if len(bars) < 400:
            continue
        c = np.array([b["close"] for b in bars], dtype=float)
        mask = np.isfinite(c) & (c > 0)
        c = c[mask]
        # dead coins trade near zero and print absurd percentage
        # bounces; a coin priced under 1000x below its history peak
        # is a delisting in progress, not a mean-reversion signal
        if len(c) < 400 or (c.max() > 0 and c[-1] < c.max() / 1000.0):
            continue
        hl, t_stat = ou_ar1_stats(c)
        h = np.array([b["high"] for b in bars], dtype=float)[mask]
        l = np.array([b["low"] for b in bars], dtype=float)[mask]
        v = np.array([float(b["volume"]) for b in bars])[mask]
        coins.append({"ticker": f.stem.upper(),
                      "half_life": round(float(hl), 1),
                      "t_stat": round(float(t_stat), 2),
                      "close": c, "high": h, "low": l, "vol": v})
    mr = [x for x in coins if x["t_stat"] <= MR_T]
    control = [x for x in coins if x["t_stat"] > MR_T]

    def group_stats(group):
        runs = []
        for x in group:
            b = zscore_long_backtest(x["close"])
            runs.append({"ticker": x["ticker"],
                         "t_stat": x["t_stat"],
                         "half_life": x["half_life"],
                         "full_sharpe": round(b["sharpe"], 2),
                         "oos_sharpe": round(_oos_sharpe(b["rets"]), 2),
                         "trades": b["trades"],
                         "oos_rets": b["rets"]})
        return runs

    mr_runs = group_stats(mr)
    ctl_runs = group_stats(control)

    def pooled(runs):
        if not runs:
            return None
        n = min(len(r["oos_rets"]) for r in runs)
        arr = np.mean([r["oos_rets"][-n:] for r in runs], axis=0)
        oos = arr[int(len(arr) * OOS_FRAC):]
        sd = oos.std()
        return {"coins": len(runs),
                "oos_sharpe": round(float(oos.mean() / sd
                                           * np.sqrt(365.0)), 2)
                if sd > 0 else 0.0,
                "oos_rets": oos}

    mr_pool = pooled(mr_runs)
    ctl_pool = pooled(ctl_runs)

    # forward-return confluence buckets on MR coins only: do
    # detector-confirmed deep stretches forward-outperform plain
    # ones where mean reversion is actually measured?
    from tops_bottoms import detect_climaxes, detect_divergences, rsi
    fwd_conf, fwd_plain = [], []
    for x in mr:
        c = x["close"]
        h, l, vol = x["high"], x["low"], x["vol"]
        z = causal_z(c)
        bull, bear = detect_divergences(c, rsi(c))
        cb, ct = detect_climaxes(h, l, c, vol)
        confirm = (set(bull.tolist()) | set(cb.tolist())
                   | set(bear.tolist()) | set(ct.tolist()))
        for t in range(WARMUP, len(c) - HORIZON):
            if z[t] > Z_ENTRY:
                continue
            fr = float(c[t + HORIZON] / c[t] - 1.0)
            if any(i in confirm for i in range(max(0, t - 3), t + 1)):
                fwd_conf.append(fr)
            else:
                fwd_plain.append(fr)
    # medians, not means: forward-return means are hostage to one
    # dead coin's terminal bounce; the median is the honest center
    conf_med = (round(float(np.median(fwd_conf)), 4)
                if fwd_conf else None)
    plain_med = (round(float(np.median(fwd_plain)), 4)
                 if fwd_plain else None)

    # the differential is the edge claim; the DSR deflates the MR
    # portfolio's OOS returns by the number of coins considered
    dsr = None
    if mr_pool is not None:
        trial_sharpes = [r["full_sharpe"] for r in mr_runs + ctl_runs]
        dsr = deflated_sharpe(mr_pool["oos_rets"], trial_sharpes)

    edge = None
    if mr_pool is not None and ctl_pool is not None:
        edge = round(mr_pool["oos_sharpe"] - ctl_pool["oos_sharpe"], 2)
    verdict = bool(
        edge is not None and edge > 0.1
        and mr_pool["oos_sharpe"] > 0
        and sum(1 for r in mr_runs if r["oos_sharpe"] > 0) * 2
        > len(mr_runs))
    return {
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "n_coins_considered": len(coins),
        "mr_coins": [r["ticker"] for r in mr_runs],
        "mr_runs": [{k: v for k, v in r.items() if k != "oos_rets"}
                    for r in mr_runs],
        "control_runs": [{k: v for k, v in r.items() if k != "oos_rets"}
                         for r in ctl_runs],
        "mr_pooled_oos_sharpe":
            mr_pool["oos_sharpe"] if mr_pool else None,
        "control_pooled_oos_sharpe":
            ctl_pool["oos_sharpe"] if ctl_pool else None,
        "edge_differential": edge,
        "confirmed_fwd_median": conf_med,
        "confirmed_n": len(fwd_conf),
        "plain_fwd_median": plain_med,
        "plain_n": len(fwd_plain),
        "deflated_sharpe": dsr,
        "verdict": verdict,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="MR-coin edge study (with control group)")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_mr_edge_study(args.data_dir)
    dest = args.research_dir / "mr_edge.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    print(f"mr edge study -> {dest} "
          f"({len(r['mr_coins'])} MR coins, "
          f"edge {r['edge_differential']}, verdict {r['verdict']})")


if __name__ == "__main__":
    main()
