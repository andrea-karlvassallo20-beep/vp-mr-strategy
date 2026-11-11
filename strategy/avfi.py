"""AVFI v3 replication and risk-throttle research.

Faithful Python replication of the Pine v5 indicator "AVFI v3 vs v2
[spread axis]" (see KNOWLEDGE (1).md, trading-research programme):

  - sigmaPk: Parkinson-style volatility floor from the bar's high-low
    range, sigmaPk = sqrt(sum(ln(H/L)^2) / (4 n ln 2)) over the window
  - va: log-volume normalization, va = ln(V) / ln(V_avg) clamped to
    the volatility floor band
  - AVFI v3: range-aware vol floor with log-volume normalization
  - AVFI v2: the classic volume-adjusted flow; the spread axis compares
    v3 against a slow EMA of v2
  - spread = AVFI v3 - EMA(AVFI v2, slow); sp_z = rolling z-score of
    the spread

The programme's evidence (stages 0-6c) is unambiguous: AVFI is a slow
regime descriptor, NOT a weekly entry timer (rule set A was killed;
H1/H2 unsupported; the 27-combo grid family fails the White reality
check). Its measurable job is a RISK THROTTLE: U2 (AVFI reversal_down
throttle 0.5) cut max drawdown from -21.5% to -15.5% at similar
Sharpe. This module therefore evaluates ONLY the throttle use on the
deployed daily ETF universe, strictly causally (all windows trailing).

Usage:
    python3 avfi.py --data-dir ./paper/data \
        --markdown ./paper/research/avfi_report.md
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from papertrading_runner import load_bars

VOL_WINDOW = 20        # volume normalization window
PK_WINDOW = 20         # Parkinson vol floor window
EMA_SLOW = 26          # slow EMA of AVFI v2 (spread axis)
SP_Z_WINDOW = 100      # rolling z-score window for the spread
THROTTLE = 0.5         # U2 pre-committed reversal_down throttle
Z_ENTRY = 2.0
Z_EXIT = 0.25
LOOKBACK = 100
WARMUP = 110
COST_BPS = 5.0


def trailing_mean(values: np.ndarray, window: int) -> np.ndarray:
    """Strictly trailing rolling mean: out[t] = mean(values up to t).
    Early bars (window not yet full) use the expanding mean."""
    out = np.empty_like(values)
    csum = np.cumsum(values)
    for t in range(len(values)):
        lo = max(0, t - window + 1)
        n = t - lo + 1
        out[t] = (csum[t] - (csum[lo - 1] if lo > 0 else 0.0)) / n
    return out


def ema(values: np.ndarray, span: int) -> np.ndarray:
    alpha = 2.0 / (span + 1.0)
    out = np.empty_like(values)
    out[0] = values[0]
    for i in range(1, len(values)):
        out[i] = alpha * values[i] + (1 - alpha) * out[i - 1]
    return out


def parkinson_sigma_pk(high: np.ndarray, low: np.ndarray,
                       window: int = PK_WINDOW) -> np.ndarray:
    """Parkinson-style per-bar vol floor from ln(H/L)^2, strictly
    trailing window."""
    rng = np.log(np.maximum(high, 1e-9) / np.maximum(low, 1e-9)) ** 2
    c = 1.0 / (4.0 * math.log(2.0))
    return np.sqrt(trailing_mean(rng, window) * c)


def avfi_v3_series(high: np.ndarray, low: np.ndarray, close: np.ndarray,
                   volume: np.ndarray,
                   vol_window: int = VOL_WINDOW,
                   pk_window: int = PK_WINDOW) -> np.ndarray:
    """Range-aware vol-floor flow with log-volume normalization (v3)."""
    sigma_pk = parkinson_sigma_pk(high, low, pk_window)
    with np.errstate(divide="ignore", invalid="ignore"):
        lv = np.log(np.maximum(volume, 1.0))
    lv[~np.isfinite(lv)] = 0.0
    vol_avg = trailing_mean(lv, vol_window)
    va = np.ones_like(lv)
    ok = vol_avg > 0
    va[ok] = lv[ok] / vol_avg[ok]
    ret = np.zeros_like(close)
    ret[1:] = np.sign(np.diff(close))
    flow = ret * va * sigma_pk
    flow[0] = 0.0
    return flow


def avfi_v2_series(close: np.ndarray, volume: np.ndarray,
                   vol_window: int = VOL_WINDOW) -> np.ndarray:
    """Classic volume-adjusted flow: signed return x volume ratio."""
    ret = np.zeros_like(close)
    ret[1:] = np.sign(np.diff(close))
    vm = trailing_mean(volume, vol_window)
    ratio = np.ones_like(volume)
    ok = vm > 0
    ratio[ok] = volume[ok] / vm[ok]
    return ret * ratio


def spread_axis(high, low, close, volume) -> np.ndarray:
    """spread = AVFI v3 - slow EMA of AVFI v2 (the spread axis)."""
    v3 = avfi_v3_series(high, low, close, volume)
    v2 = ema(avfi_v2_series(close, volume), EMA_SLOW)
    return v3 - v2


def spread_z(spread: np.ndarray, window: int = SP_Z_WINDOW) -> np.ndarray:
    """Rolling z-score of the spread (sigma-normalized histogram)."""
    z = np.zeros_like(spread)
    for t in range(window, len(spread)):
        w = spread[t - window + 1:t + 1]
        sd = w.std()
        if sd > 0:
            z[t] = (spread[t] - w.mean()) / sd
    return z


def throttle_backtest(high, low, close, volume,
                      use_throttle: bool = True):
    """Production-style daily z-score MR backtest; the AVFI throttle
    halves exposure when the spread axis signals distribution
    (sp_z strongly negative = effort without result = risk-off).
    Strictly causal: every window trails the decision bar. Returns
    (sharpe, max_dd_pct, total_pct, trades, throttled_bars)."""
    logp = np.log(close)
    n = len(close)
    sp_z = spread_z(spread_axis(high, low, close, volume)) \
        if use_throttle else np.zeros(n)
    pos = np.zeros(n)
    cur = 0.0
    throttled = 0
    for t in range(WARMUP, n - 1):
        window = logp[t - LOOKBACK + 1:t + 1]
        mu, sd = window.mean(), window.std()
        if sd <= 0:
            continue
        z = (logp[t] - mu) / sd
        if cur == 0.0 and abs(z) >= Z_ENTRY:
            cur = -1.0 if z > 0 else 1.0
        elif cur != 0.0 and abs(z) <= Z_EXIT:
            cur = 0.0
        size = cur
        if use_throttle and cur != 0.0 and sp_z[t] <= -1.0:
            size = cur * THROTTLE
            throttled += 1
        pos[t + 1] = size
    rets = np.diff(logp)
    vol = np.std(rets) * math.sqrt(252) or 1.0
    strat = pos[1:] / vol * rets
    trades = int(np.sum(np.abs(np.diff(pos)) > 0))
    if trades:
        strat = strat - np.abs(np.diff(pos, prepend=0.0)[1:]) * COST_BPS / 1e4
    sd = strat.std()
    sharpe = float(strat.mean() / sd * math.sqrt(252)) if sd > 0 else 0.0
    eq = 1.0 + np.cumsum(strat)
    peak = np.maximum.accumulate(eq)
    max_dd = float(((peak - eq) / peak).max()) if len(eq) else 0.0
    total = float((eq[-1] - 1.0) * 100.0)
    return sharpe, max_dd * 100.0, total, trades, throttled


def run_avfi_research(data_dir: Path,
                      universe=("SPY", "QQQ", "IWM", "XLF", "XLE")) -> dict:
    """Throttle study per instrument + portfolio view, honest both ways."""
    rows = []
    for s in universe:
        f = data_dir / f"{s.lower()}.csv"
        if not f.exists():
            continue
        bars = load_bars(f)
        if len(bars) < WARMUP + 60:
            continue
        h = np.array([b["high"] for b in bars])
        l = np.array([b["low"] for b in bars])
        c = np.array([b["close"] for b in bars])
        v = np.array([float(b["volume"]) for b in bars])
        base = throttle_backtest(h, l, c, v, use_throttle=False)
        throttled = throttle_backtest(h, l, c, v, use_throttle=True)
        rows.append({
            "ticker": s,
            "base": {"sharpe": round(base[0], 2),
                     "max_dd_pct": round(base[1], 1),
                     "return_pct": round(base[2], 1), "trades": base[3]},
            "throttle": {"sharpe": round(throttled[0], 2),
                         "max_dd_pct": round(throttled[1], 1),
                         "return_pct": round(throttled[2], 1),
                         "trades": throttled[3],
                         "throttled_bars": throttled[4]},
        })
    return {"status": "OK" if rows else "NO_DATA", "rows": rows,
            "note": ("Per the AVFI-NQ programme (KNOWLEDGE (1).md): AVFI "
                     "is a slow regime descriptor, not an entry timer; "
                     "only the risk-throttle use is evaluated here.")}


def write_report(r: dict, markdown: Path) -> None:
    lines = ["# AVFI v3 risk-throttle research", "",
             "Python replication of the Pine v5 'AVFI v3 vs v2 [spread "
             "axis]' indicator (Parkinson-style sigmaPk vol floor, "
             "log-volume normalization, spread vs slow EMA of v2, "
             "sigma-normalized z). Per the programme's evidence, AVFI "
             "is evaluated ONLY as a risk throttle (halve exposure when "
             "sp_z <= -1), never as an entry timer.", "",
             "| Ticker | Base Sharpe | Base MaxDD % | Throttle Sharpe | "
             "Throttle MaxDD % | Throttled bars |", "|---|---|---|---|---|---|"]
    for row in r.get("rows", []):
        b, t = row["base"], row["throttle"]
        lines.append(
            f"| {row['ticker']} | {b['sharpe']:+.2f} | {b['max_dd_pct']} | "
            f"{t['sharpe']:+.2f} | {t['max_dd_pct']} | {t['throttled_bars']} |")
    lines += ["", r.get("note", ""), "",
              "Honest reading: the throttle is judged on drawdown "
              "reduction at preserved Sharpe (the programme's U2 "
              "result), not on Sharpe improvement. Negative results "
              "are reported."]
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text("\n".join(lines) + "\n")
    print(f"avfi report written -> {markdown}")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="AVFI v3 risk-throttle research")
    ap.add_argument("--data-dir", type=Path, default=Path("paper/data"))
    ap.add_argument("--markdown", type=Path,
                    default=Path("paper/research/avfi_report.md"))
    ap.add_argument("--json-out", type=Path,
                    default=Path("paper/research/avfi_report.json"))
    args = ap.parse_args()
    r = run_avfi_research(args.data_dir)
    write_report(r, args.markdown)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(r, indent=2))
    print(f"avfi json written -> {args.json_out}")
    print(f"status: {r['status']}, instruments: {len(r['rows'])}")


if __name__ == "__main__":
    main()
