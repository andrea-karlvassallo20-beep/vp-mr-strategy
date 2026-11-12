"""The v4 study: stretch+confirmation vs plain stretch, everywhere.

AVFI v4's signal is deep stretch + detector confirmation. The MR-coin
study measured the confirmation premium on forward returns (roughly
3x the median, on MR coins); this study converts it to a CAUSAL
backtest and measures the improvement across the WHOLE universe -
156 crypto and 29 commodity series - plain z-score entries vs v4
confirmed entries, per series, per asset class, pooled and judged
out-of-sample.

Honesty devices, pre-committed:
  - dead coins excluded (priced 1000x below peak); returns winsorized
  - both sides pay 5 bps; entries confirmed within 3 bars, causally
  - dual-split: the premium must hold at BOTH the last-40% and
    last-50% windows, scored at the worse one
  - the verdict requires the pooled premium AND a majority of
    own-scale beats, per asset class and overall

Usage (nightly):
    python3 v4_study.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from cross_asset import safe_name
from papertrading_runner import load_bars
from tops_bottoms import (detect_climaxes, detect_divergences, rsi)

Z_ENTRY = 2.0
Z_EXIT = 0.25
LOOKBACK = 100
WARMUP = 110
COST_BPS = 5.0
CONFIRM_LB = 3
SPLITS = (0.6, 0.5)


def causal_z(close: np.ndarray) -> np.ndarray:
    logp = np.log(close)
    z = np.zeros(len(close))
    for t in range(LOOKBACK, len(close)):
        w = logp[t - LOOKBACK + 1:t + 1]
        sd = w.std()
        if sd > 0:
            z[t] = (logp[t] - w.mean()) / sd
    return z


def confirm_sets(h, l, c, v):
    """Causal detector sets: bull-side and bear-side confirmation
    indices (divergence OR climax, either detector confirms)."""
    bull, bear = detect_divergences(c, rsi(c))
    cb, ct = detect_climaxes(h, l, c, v)
    return (set(bull.tolist()) | set(cb.tolist()),
            set(bear.tolist()) | set(ct.tolist()))


def stretch_backtest(c, z, bull_conf, bear_conf, confirmed_only):
    """Long/short z-score core. Plain: enter at |z| >= 2. v4: same,
    but the entry bar must be detector-confirmed on the correct side
    (within CONFIRM_LB bars). Exit at |z| <= 0.25. Costs both sides."""
    n = len(c)
    pos = np.zeros(n)
    cur = 0.0
    trades = 0
    for t in range(WARMUP, n - 1):
        if cur == 0.0 and abs(z[t]) >= Z_ENTRY:
            side = 1 if z[t] < 0 else -1
            ok = True
            if confirmed_only:
                conf = bull_conf if side > 0 else bear_conf
                ok = any(i in conf
                         for i in range(max(0, t - CONFIRM_LB), t + 1))
            if ok:
                cur = float(side)
                trades += 1
        elif cur != 0.0 and abs(z[t]) <= Z_EXIT:
            cur = 0.0
        pos[t + 1] = cur
    rets = np.diff(np.log(c))
    strat = pos[1:] * rets
    if trades:
        turns = np.abs(np.diff(pos, prepend=0.0))[1:]
        strat = strat - turns * COST_BPS / 1e4
    strat = np.clip(strat, -0.5, 0.5)
    return strat, trades


def _sharpe(rets, lo=None):
    seg = rets[int(len(rets) * lo):] if lo else rets
    if len(seg) < 20 or seg.std() == 0:
        return 0.0
    return float(seg.mean() / seg.std() * np.sqrt(252.0))


def run_v4_study(data_dir: Path) -> dict:
    rows = []
    for f in sorted(data_dir.glob("*.csv")):
        bars = load_bars(f)
        if len(bars) < 400:
            continue
        c = np.array([b["close"] for b in bars], dtype=float)
        mask = np.isfinite(c) & (c > 0)
        c = c[mask]
        if len(c) < 400 or (c.max() > 0 and c[-1] < c.max() / 1000.0):
            continue
        h = np.array([b["high"] for b in bars], dtype=float)[mask]
        l = np.array([b["low"] for b in bars], dtype=float)[mask]
        v = np.array([float(b["volume"]) for b in bars])[mask]
        z = causal_z(c)
        bull, bear = confirm_sets(h, l, c, v)
        plain, tr_p = stretch_backtest(c, z, bull, bear, False)
        v4, tr_v = stretch_backtest(c, z, bull, bear, True)
        # dual-split premium: worse of the two OOS windows
        prem = min(_sharpe(v4, s) - _sharpe(plain, s) for s in SPLITS)
        rows.append({
            "ticker": f.stem.upper(),
            "asset_class": ("crypto" if f.stem.lower().endswith("usd")
                            else "commodity"),
            "plain_full": round(_sharpe(plain), 2),
            "plain_oos": round(_sharpe(plain, SPLITS[0]), 2),
            "v4_full": round(_sharpe(v4), 2),
            "v4_oos": round(_sharpe(v4, SPLITS[0]), 2),
            "premium_worse_window": round(prem, 2),
            "plain_trades": tr_p,
            "v4_trades": tr_v,
            "plain_rets": plain,
            "v4_rets": v4,
        })

    def class_summary(cls):
        grp = [r for r in rows if r["asset_class"] == cls]
        if not grp:
            return None
        n = min(len(r["plain_rets"]) for r in grp)
        out = {}
        for key in ("plain", "v4"):
            arr = np.mean([r[f"{key}_rets"][-n:] for r in grp], axis=0)
            out[key] = round(min(_sharpe(arr, s) for s in SPLITS), 2)
        beats = sum(1 for r in grp
                    if r["premium_worse_window"] > 0)
        return {"series": len(grp),
                "plain_pooled": out["plain"],
                "v4_pooled": out["v4"],
                "pooled_premium": round(out["v4"] - out["plain"], 2),
                "own_scale_beats": f"{beats}/{len(grp)}",
                "improves": bool(out["v4"] > out["plain"]
                                 and beats * 2 > len(grp))}

    classes = {cls: class_summary(cls)
               for cls in ("crypto", "commodity")}
    overall = class_summary("crypto")
    # overall across everything
    n = min(len(r["plain_rets"]) for r in rows)
    pooled = {}
    for key in ("plain", "v4"):
        arr = np.mean([r[f"{key}_rets"][-n:] for r in rows], axis=0)
        pooled[key] = round(min(_sharpe(arr, s) for s in SPLITS), 2)
    beats_all = sum(1 for r in rows if r["premium_worse_window"] > 0)
    overall = {"series": len(rows),
                "plain_pooled": pooled["plain"],
                "v4_pooled": pooled["v4"],
                "pooled_premium": round(pooled["v4"] - pooled["plain"], 2),
                "own_scale_beats": f"{beats_all}/{len(rows)}",
                "improves": bool(pooled["v4"] > pooled["plain"]
                                 and beats_all * 2 > len(rows))}
    for r in rows:
        del r["plain_rets"]
        del r["v4_rets"]
    top = sorted(rows, key=lambda r: -r["premium_worse_window"])[:15]
    bottom = sorted(rows, key=lambda r: r["premium_worse_window"])[:10]
    return {
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "by_class": classes,
        "overall": overall,
        "rows": rows,
        "best_series": top,
        "worst_series": bottom,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="v4 stretch+confirmation vs plain, everywhere")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_v4_study(args.data_dir)
    dest = args.research_dir / "v4_study.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    o = r["overall"]
    print(f"v4 study -> {dest} ({o['series']} series, "
          f"pooled premium {o['pooled_premium']}, "
          f"beats {o['own_scale_beats']}, "
          f"improves {o['improves']})")


if __name__ == "__main__":
    main()
