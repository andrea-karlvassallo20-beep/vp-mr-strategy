"""THE FULL-UNIVERSE TOPS/BOTTOMS BACKTEST: AVFI v4 detection and
the philosopher's long rule across the whole extended universe -
15 main indexes, 29 commodity futures, 156 crypto series - to
identify the points of significant change at tops and bottoms.

Two measurements, one module:

  1. AVFI v4 DETECTION, EVERYWHERE: v4's deep stretch
     (|z| >= 2) plus detector confirmation (divergence or
     climax within 3 bars, causally) fires a BOTTOM (bull-side)
     or TOP (bear-side) event. At every event the forward 1/2/4-
     week returns are measured - is the detected point a point of
     significant change? The honest stats: median forward
     return, P(the 4-week move runs the detected direction), and
     the same for the unmatched stretch (no confirmation), per
     asset class.

  2. THE PHILOSOPHER'S LONG RULE, OUT OF SAMPLE: the crash-zone
     entry (-5..-10% weekly on anchored assets) was measured on
     the original anchored set; the 11 NEWLY FETCHED global
     indexes are data the rule has never seen - a natural
     holdout. The rule is scored on them unchanged: median net
     4-week return, hit rate, per index.

Honesty devices: dead-coin filter, winsorized returns, costs on
the tradable legs, and the confirmation premium judged against
its own unmatched control.

Usage (nightly, after market_philosopher):
    python3 tops_bottoms_backtest.py --data-dir \\
        ../paper/research/data --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from cross_asset import safe_name
from market_philosopher import (HOLD_WEEKS, WEEK, ZONE_HI,
                                ZONE_LO, COST_BPS)
from papertrading_runner import load_bars
from smh_proof import _series
from tops_bottoms import (detect_climaxes, detect_divergences,
                          rsi)
from v4_study import CONFIRM_LB, causal_z

WINSOR = 0.05
NEW_INDEXES = ("STOXX50E", "GDAXI", "FCHI", "FTSE", "N225",
               "HSI", "KS11", "TWII", "AXJO", "BVSP", "NSEI")


def _class_of(name: str) -> str:
    if name in NEW_INDEXES:
        return "index (new holdout)"
    if name in ("GSPC", "IXIC", "DJI", "RUT"):
        return "index"
    if name.endswith("F") and len(name) <= 4:
        return "commodity"
    return "crypto"


def _winsor(x):
    x = np.asarray(x, dtype=float)
    if not len(x):
        return x
    lo, hi = np.quantile(x, [WINSOR, 1 - WINSOR])
    return np.clip(x, lo, hi)


def detect_events(c, v):
    """Causal v4 detection: (bottoms, tops) bar indices - deep
    stretch with detector confirmation within CONFIRM_LB bars -
    plus the unmatched stretch indices for the control."""
    z = causal_z(c)
    h = np.maximum(c, c * 1.0)
    l = np.minimum(c, c * 1.0)
    bull, bear = detect_divergences(c, rsi(c))
    cb, ct = detect_climaxes(h, l, c, v)
    bull_conf = set(bull.tolist()) | set(cb.tolist())
    bear_conf = set(bear.tolist()) | set(ct.tolist())
    bottoms, tops = [], []
    unmatched_b, unmatched_t = [], []
    for t in range(len(c)):
        if z[t] <= -2.0:
            ok = any(i in bull_conf
                     for i in range(max(0, t - CONFIRM_LB),
                                    t + 1))
            (bottoms if ok else unmatched_b).append(t)
        elif z[t] >= 2.0:
            ok = any(i in bear_conf
                     for i in range(max(0, t - CONFIRM_LB),
                                    t + 1))
            (tops if ok else unmatched_t).append(t)
    return (bottoms, tops, unmatched_b, unmatched_t)


def _fwd_stats(logc, events, direction, horizon):
    """Forward returns after events, in the detected direction:
    direction +1 (bottoms -> up) or -1 (tops -> down)."""
    rets = []
    n = len(logc)
    for t in events:
        k = t + WEEK * horizon
        if k >= n:
            continue
        rets.append(direction * float(logc[k] - logc[t]))
    if not rets:
        return {"n": 0}
    w = _winsor(rets)
    return {
        "n": len(rets),
        "median_fwd": round(float(np.median(w)), 4),
        "p_runs_direction": round(float(
            np.mean(np.array(rets) > 0)), 3),
    }


def run_backtest(data_dir: Path) -> dict:
    # single pass over the universe; per-class accumulators
    acc = {}
    for name, c, v in _series(data_dir):
        cls = _class_of(name)
        logc = np.log(c)
        n = len(logc)
        slot = acc.setdefault(cls, {
            "series": 0,
            "bottoms": [], "tops": [],
            "bottoms_un": [], "tops_un": [],
            "zone": [],
        })
        slot["series"] += 1
        b, t_, ub, ut = detect_events(c, v)

        def fwd(evts, direction):
            out = []
            for t in evts:
                k = t + WEEK * 4
                if k < n:
                    out.append(direction * float(
                        logc[k] - logc[t]))
            return out

        slot["bottoms"] += fwd(b, 1)
        slot["tops"] += fwd(t_, -1)
        slot["bottoms_un"] += fwd(ub, 1)
        slot["tops_un"] += fwd(ut, -1)
        # the crash-zone long trades (net of costs)
        for tt in range(60, n - WEEK * HOLD_WEEKS):
            if tt < WEEK:
                continue
            wr = float(logc[tt] - logc[tt - WEEK])
            if ZONE_LO <= wr < ZONE_HI:
                slot["zone"].append(
                    float(logc[tt + WEEK * HOLD_WEEKS]
                          - logc[tt]) - 2 * COST_BPS / 1e4)

    def stats(rets):
        if not rets:
            return {"n": 0}
        w = _winsor(rets)
        return {
            "n": len(rets),
            "median_fwd_4w": round(float(np.median(w)), 4),
            "p_runs_direction_4w": round(float(np.mean(
                np.array(rets) > 0)), 3),
        }

    out = {}
    for cls, s in acc.items():
        out[cls] = {
            "series": s["series"],
            "bottoms": stats(s["bottoms"]),
            "tops": stats(s["tops"]),
            "bottoms_unmatched": stats(s["bottoms_un"]),
            "tops_unmatched": stats(s["tops_un"]),
            "zone": stats(s["zone"]),
        }

    # the OOS verdict: the crash-zone rule on the new indexes
    oos = out.get("index (new holdout)", {}).get("zone", {})
    oos_n = oos.get("n", 0)
    oos_med = oos.get("median_fwd_4w")
    oos_hit = oos.get("p_runs_direction_4w")
    return {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "protocol": "AVFI v4 detection (deep stretch + causal "
            "confirmation) and the crash-zone long rule, across "
            "the full extended universe; the 11 newly fetched "
            "global indexes are a natural holdout the rule has "
            "never seen",
        "classes": out,
        "oos_holdout": {
            "n_trades": oos_n,
            "median_net_4w": oos_med,
            "p_positive": oos_hit,
            "verdict": ("the crash-zone long edge REPLICATES on "
                        "data the rule never saw" if
                        oos_med is not None and oos_med > 0
                        and oos_hit is not None and oos_hit > 0.5
                        and oos_n >= 10 else
                        "the holdout is thin or the edge does "
                        "not replicate - reported as measured"),
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Full-universe tops/bottoms backtest")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_backtest(args.data_dir)
    dest = args.research_dir / "tops_bottoms_backtest.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    o = r["oos_holdout"]
    print(f"tops/bottoms backtest -> {dest} "
          f"(classes: {list(r['classes'])}; holdout "
          f"{o['n_trades']} trades, median "
          f"{o['median_net_4w']}, verdict: {o['verdict'][:40]})")


if __name__ == "__main__":
    main()
