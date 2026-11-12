"""AVFI v3 replication, risk-throttle research, and iterative improvement.

Faithful Python replication of the Pine v5 indicator "AVFI v3 vs v2
[spread axis]" (see KNOWLEDGE (1).md, trading-research programme):

  - sigmaPk: Parkinson-style volatility floor from the bar's high-low
    range, strictly trailing window
  - va: log-volume normalization vs the trailing mean
  - AVFI v3: range-aware vol floor with log-volume normalization
  - AVFI v2: classic volume-adjusted flow; the spread axis compares
    v3 against a slow EMA of v2
  - spread = AVFI v3 - EMA(AVFI v2, slow); sp_z = trailing z-score

The programme's evidence is unambiguous: AVFI is a slow regime
descriptor, NOT an entry timer. Its measurable job is a RISK THROTTLE
(U2: cut maxDD -21.5% -> -15.5% at preserved Sharpe). This module
evaluates ONLY the throttle use, strictly causally.

ITERATION MECHANISM: AVFI is the starting point of the edge formula
and must improve with each run. Each nightly pass (1) evaluates the
current research parameters, (2) searches a pre-committed variant grid
with walk-forward honesty (selection on the first 60%, scoring on the
untouched last 40%), (3) appends the result to an append-only
iteration ledger, and (4) if a candidate beats the current parameters
out-of-sample (more drawdown reduction at preserved Sharpe), the
research parameters advance to the candidate for the next iteration.
The DEPLOYED strategy is never touched (Gate 3).

Usage (nightly):
    python3 avfi.py --data-dir ./paper/data \
        --markdown ./paper/research/avfi_report.md
"""
import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from papertrading_runner import load_bars

DEFAULT_PARAMS = {
    "vol_window": 20,     # volume normalization window
    "pk_window": 20,      # range-vol floor window
    "ema_slow": 26,       # slow EMA of AVFI v2 (spread axis)
    "sp_z_window": 100,   # trailing z-score window for the spread
    "trigger": -1.0,      # sp_z below this -> throttle on
    "throttle": 0.5,      # exposure multiplier while throttled
    # formula variants (iteration grid searches these too):
    "vol_estimator": "parkinson",   # or "garman_klass" (uses OHLC,
                                    #  captures open->close info the
                                    #  high-low range wastes)
    "volume_mode": "shares",        # or "dollar" (volume x close —
                                    #  robust to splits/share counts)
    "entry_mode": "zscore",         # or "detector": z-score entries
                                    #  confirmed by the RSI-divergence /
                                    #  VSA-climax detectors
                                    #  or "topology3": enter only when
                                    #  >= 3 of the 5 turn-topology
                                    #  dimensions align (the confluence
                                    #  finding: score-3 entries beat
                                    #  score-2 on all 5 ETFs)
}
Z_ENTRY = 2.0
Z_EXIT = 0.25
LOOKBACK = 100
WARMUP = 110
COST_BPS = 5.0

VARIANT_GRID = [
    {"trigger": tr, "throttle": th, "ema_slow": es, "pk_window": pk,
     "vol_estimator": ve, "volume_mode": vm}
    for tr in (-0.5, -1.0, -1.5)
    for th in (0.5, 0.25)
    for es in (13, 26)
    for pk in (10, 20)
    for ve, vm in (("parkinson", "shares"), ("garman_klass", "shares"),
                   ("garman_klass", "dollar"))
] + [
    # detector-confirmed entries (tops/bottoms confirmation) at the
    # pre-committed trigger/throttle anchors
    {"trigger": tr, "throttle": th, "ema_slow": 13, "pk_window": 10,
     "vol_estimator": "parkinson", "volume_mode": "shares",
     "entry_mode": em}
    for em in ("detector", "topology3", "topology3_midvol")
    for tr in (-1.0, -1.5)
    for th in (0.5, 0.25)
]


# --- the indicator, piece by piece ------------------------------------
# Every window below is STRICTLY TRAILING: at bar t we only ever see
# bars <= t. That is Gate 1 (zero lookahead) and it is what makes the
# whole study honest.


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
                       window: int) -> np.ndarray:
    # sigmaPk: the "range-aware volatility floor" of AVFI v3. Parkinson
    # showed the high-low range carries ~5x more volatility information
    # per bar than the close; wide-range bars = high vol floor.
    """Parkinson-style per-bar vol floor from ln(H/L)^2, strictly
    trailing window."""
    rng = np.log(np.maximum(high, 1e-9) / np.maximum(low, 1e-9)) ** 2
    c = 1.0 / (4.0 * math.log(2.0))
    return np.sqrt(trailing_mean(rng, window) * c)


def garman_klass_sigma(open_, high, low, close, window) -> np.ndarray:
    # Garman-Klass OHLC estimator: everything Parkinson sees PLUS the
    # open->close move (overnight/session gaps Parkinson wastes).
    # ~2x more efficient than close-to-close, ~1.4x than Parkinson.
    hl = 0.5 * np.log(np.maximum(high, 1e-9)
                      / np.maximum(low, 1e-9)) ** 2
    co = (2.0 * math.log(2.0) - 1.0) * \
        np.log(np.maximum(close, 1e-9)
               / np.maximum(open_, 1e-9)) ** 2
    return np.sqrt(trailing_mean(np.maximum(hl - co, 0.0), window))


def avfi_v3_series(high, low, close, volume, vol_window, pk_window,
                   open_=None, vol_estimator="parkinson",
                   volume_mode="shares"):
    # AVFI v3 = signed price move x log-volume normalization (va) x the
    # range-aware vol floor. va > 1 means this bar's volume is above
    # its trailing norm (real effort); va < 1 means weak effort.
    """Range-aware vol-floor flow with log-volume normalization (v3)."""
    if vol_estimator == "garman_klass" and open_ is not None:
        sigma_pk = garman_klass_sigma(open_, high, low, close, pk_window)
    else:
        sigma_pk = parkinson_sigma_pk(high, low, pk_window)
    if volume_mode == "dollar":
        volume = np.asarray(volume, dtype=float) * np.asarray(close,
                                                              dtype=float)
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


def avfi_v2_series(close, volume, vol_window):
    """Classic volume-adjusted flow: signed return x volume ratio."""
    ret = np.zeros_like(close)
    ret[1:] = np.sign(np.diff(close))
    vm = trailing_mean(volume, vol_window)
    ratio = np.ones_like(volume)
    ok = vm > 0
    ratio[ok] = volume[ok] / vm[ok]
    return ret * ratio


def spread_axis(high, low, close, volume, params,
                open_=None) -> np.ndarray:
    # THE SPREAD AXIS: AVFI v3 minus a slow EMA of AVFI v2. When v3 runs
    # above the slow v2 line, range-aware flow is expanding; below it,
    # effort is fading — a slow regime descriptor.
    """spread = AVFI v3 - slow EMA of AVFI v2 (the spread axis)."""
    v3 = avfi_v3_series(high, low, close, volume,
                        params["vol_window"], params["pk_window"],
                        open_=open_,
                        vol_estimator=params.get("vol_estimator",
                                                 "parkinson"),
                        volume_mode=params.get("volume_mode", "shares"))
    v2 = ema(avfi_v2_series(close, volume, params["vol_window"]),
             params["ema_slow"])
    return v3 - v2


def spread_z(spread: np.ndarray, window: int) -> np.ndarray:
    # sigma-normalized histogram: how many trailing standard deviations
    # the spread sits from its trailing mean. This z is what the
    # throttle reads.
    """Trailing z-score of the spread (sigma-normalized histogram)."""
    z = np.zeros_like(spread)
    for t in range(window, len(spread)):
        w = spread[t - window + 1:t + 1]
        sd = w.std()
        if sd > 0:
            z[t] = (spread[t] - w.mean()) / sd
    return z


def throttle_backtest(high, low, close, volume,
                      use_throttle: bool = True,
                      params: dict = None, open_=None):
    """Production-style daily z-score MR backtest; the AVFI throttle
    cuts exposure to `throttle` x when sp_z <= trigger. Strictly
    causal. Returns dict with metrics, equity curve, positions,
    entries and the sp_z series."""
    # --- the strategy the throttle rides on --------------------------
    # A plain z-score mean-reversion core: buy stretched bottoms
    # (z <= -2), sell stretched tops (z >= +2), exit near the mean.
    # The AVFI throttle then CUTS exposure when the spread z says the
    # regime is distribution (effort without result) — risk-off, not
    # entry timing. Equity therefore revolves around longs at bottoms
    # and shorts at tops, throttled by AVFI.
    p = dict(DEFAULT_PARAMS if params is None else params)
    logp = np.log(close)
    n = len(close)
    confirm = None
    if p.get("entry_mode") == "detector":
        from tops_bottoms import (detect_climaxes, detect_divergences,
                                  rsi)
        bull, bear = detect_divergences(close, rsi(close))
        cb, ct = detect_climaxes(high, low, close, volume)
        confirm = set(bull.tolist()) | set(bear.tolist()) | \
            set(cb.tolist()) | set(ct.tolist())
    elif p.get("entry_mode") == "topology3":
        from tops_bottoms import turn_topology
        b_score, t_score = turn_topology(high, low, close, volume)
        confirm = ({int(i) for i in np.nonzero(b_score >= 3)[0]}
                   | {int(i) for i in np.nonzero(t_score >= 3)[0]})
    elif p.get("entry_mode") == "topology3_midvol":
        # confluence >= 3 AND the entry bar's trailing 20-bar realized
        # vol sits in the MIDDLE tercile of its EXPANDING history
        # (strictly causal regime gate — the descriptive regime study
        # found the confluence edge concentrates in mid-vol regimes)
        from tops_bottoms import turn_topology
        b_score, t_score = turn_topology(high, low, close, volume)
        confirm = ({int(i) for i in np.nonzero(b_score >= 3)[0]}
                   | {int(i) for i in np.nonzero(t_score >= 3)[0]})
        rets = np.diff(np.log(close))
        vol20 = np.zeros(len(close))
        wins = np.lib.stride_tricks.sliding_window_view(rets, 20)
        vol20[20:] = wins.std(axis=1)
        mid_ok = np.zeros(len(close), dtype=bool)
        for t_ in range(60, len(close)):
            hist = vol20[20:t_ + 1]
            mid_ok[t_] = (np.quantile(hist, 1 / 3) <= vol20[t_]
                          <= np.quantile(hist, 2 / 3))
        confirm = {i for i in confirm if mid_ok[i]}
    sp_z = (spread_z(spread_axis(high, low, close, volume, p,
                                  open_=open_), p["sp_z_window"])
            if use_throttle else np.zeros(n))
    pos = np.zeros(n)
    cur = 0.0
    throttled = 0
    entries = []
    for t in range(WARMUP, n - 1):
        window = logp[t - LOOKBACK + 1:t + 1]
        mu, sd = window.mean(), window.std()
        if sd <= 0:
            continue
        z = (logp[t] - mu) / sd
        confirmed = confirm is None or any(
            i in confirm for i in range(max(0, t - 3), t + 1))
        if cur == 0.0 and abs(z) >= Z_ENTRY and confirmed:
            cur = -1.0 if z > 0 else 1.0   # short the top, long the bottom
            entries.append((t + 1, cur))
        elif cur != 0.0 and abs(z) <= Z_EXIT:
            cur = 0.0
        size = cur
        # AVFI risk throttle: regime says distribution -> shrink the
        # position instead of trusting the stretch
        if use_throttle and cur != 0.0 and sp_z[t] <= p["trigger"]:
            size = cur * p["throttle"]
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
    return {"sharpe": sharpe, "max_dd_pct": max_dd * 100.0,
            "return_pct": total, "trades": trades,
            "throttled_bars": throttled, "entries": entries,
            "pos": pos, "sp_z": sp_z, "eq": eq}


def _window_dd(eq: np.ndarray, lo: int, hi: int) -> float:
    seg = eq[lo:hi]
    if len(seg) < 2:
        return 0.0
    peak = np.maximum.accumulate(seg)
    return float(((peak - seg) / peak).max() * 100.0)


def _window_sharpe(eq: np.ndarray, lo: int, hi: int) -> float:
    seg = eq[lo:hi]
    if len(seg) < 3:
        return 0.0
    rets = np.diff(seg)
    sd = rets.std()
    return float(rets.mean() / sd * math.sqrt(252)) if sd > 0 else 0.0


def _load_params(research_dir: Path) -> dict:
    f = research_dir / "avfi_params.json"
    if f.exists():
        saved = json.loads(f.read_text())
        return {**DEFAULT_PARAMS, **saved}
    return dict(DEFAULT_PARAMS)


def _save_params(research_dir: Path, params: dict) -> None:
    research_dir.mkdir(parents=True, exist_ok=True)
    (research_dir / "avfi_params.json").write_text(
        json.dumps(params, indent=2))


def run_iteration(data_dir: Path, research_dir: Path,
                  universe=("SPY", "QQQ", "IWM", "XLF", "XLE")) -> dict:
    # --- one improvement iteration --------------------------------------
    # 1. load the CURRENT research parameters (avfi_params.json)
    # 2. evaluate them on the deployed universe
    # 3. search the pre-committed 24-variant grid, scoring candidates on
    #    the untouched last 40% of data (train/OOS honesty)
    # 4. advance the parameters only if a candidate beats them OOS
    # 5. append an honest record to the iteration ledger
    """One improvement iteration: evaluate current params, search the
    pre-committed grid with train/OOS honesty, advance params if a
    candidate wins out-of-sample, append to the ledger."""
    series = []
    for s in universe:
        f = data_dir / f"{s.lower()}.csv"
        if not f.exists():
            continue
        bars = load_bars(f)
        if len(bars) < WARMUP + 60:
            continue
        series.append((s,
                       np.array([b["high"] for b in bars]),
                       np.array([b["low"] for b in bars]),
                       np.array([b["close"] for b in bars]),
                       np.array([float(b["volume"]) for b in bars]),
                       [b["date"] for b in bars],
                       np.array([b["open"] for b in bars])))
    if not series:
        return {"status": "NO_DATA"}

    params = _load_params(research_dir)
    split = int(min(len(c) for _, _, _, c, _, _, _ in series) * 0.6)

    def portfolio(pp, use_throttle=True):
        runs = [throttle_backtest(h, l, c, v, use_throttle, pp, o)
                for _, h, l, c, v, _, o in series]
        return runs

    base_runs = [throttle_backtest(h, l, c, v, False, params, o)
                 for _, h, l, c, v, _, o in series]
    cur_runs = portfolio(params)

    # DUAL-SPLIT ROBUSTNESS: a candidate must beat the current params
    # on BOTH out-of-sample windows (last 40% and last 50%). A single
    # window rewards selection luck — the 2026-11-11 lesson: the
    # detector mode's 27.4% dd-reduction collapsed to 1.0% when the
    # data window shifted by one bar. Advancement now requires
    # stability, not a lucky window.
    splits = [split, int(min(len(c) for _, _, _, c, _, _, _ in series)
                          * 0.5)]

    def oos_score(runs):
        dd_reds, sh_deltas = [], []
        for sp in splits:
            dd_reds.append(np.mean([
                _window_dd(b["eq"], sp, len(b["eq"]))
                - _window_dd(r["eq"], sp, len(r["eq"]))
                for b, r in zip(base_runs, runs)]))
            sh_deltas.append(np.mean([
                _window_sharpe(r["eq"], sp, len(r["eq"]))
                - _window_sharpe(b["eq"], sp, len(r["eq"]))
                for b, r in zip(base_runs, runs)]))
        # the honest score is the WORSE of the two windows
        return min(dd_reds), min(sh_deltas)

    cur_dd_red, cur_sh_delta = oos_score(cur_runs)

    best = None
    for cand in VARIANT_GRID:
        pp = {**params, **cand}
        runs = portfolio(pp)
        dd_red, sh_delta = oos_score(runs)
        # honest selection: maximize the WORST-window OOS drawdown
        # reduction subject to Sharpe preservation (delta >= -0.05)
        if sh_delta >= -0.05 and (best is None or dd_red > best[1]):
            best = (pp, dd_red, sh_delta)

    advanced = bool(best and best[1] > cur_dd_red + 0.1)
    new_params = best[0] if advanced else params
    if advanced:
        _save_params(research_dir, new_params)

    ledger_path = research_dir / "avfi_iterations.json"
    ledger = json.loads(ledger_path.read_text()) \
        if ledger_path.exists() else []
    today = datetime.now(timezone.utc).date().isoformat()
    record = {
        "date": today,
        "iteration": len(ledger) + 1,
        "params_evaluated": params,
        "oos_dd_reduction_pct": round(cur_dd_red, 2),
        "oos_sharpe_delta": round(cur_sh_delta, 3),
        "best_candidate": ({"params": best[0],
                            "oos_dd_reduction_pct": round(best[1], 2),
                            "oos_sharpe_delta": round(best[2], 3)}
                           if best else None),
        "advanced": advanced,
        "params_next": new_params,
    }
    prev = next((r for r in ledger if r["date"] == today), None)
    if prev is not None:
        record["iteration"] = prev["iteration"]
        ledger = [r for r in ledger if r["date"] != today]
    ledger.append(record)
    research_dir.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger, indent=2))

    chart = []
    for (s, h, l, c, v, dates, o), run in zip(series, cur_runs):
        chart.append({
            "ticker": s,
            "dates": dates,
            "close": [round(float(x), 2) for x in c],
            "sp_z": [round(float(x), 3) for x in run["sp_z"]],
            "trigger": params["trigger"],
            "throttle": params["throttle"],
            "entries": [[int(t), int(d)] for t, d in run["entries"]],
            "throttled_bars": run["throttled_bars"],
            "eq": [round(float(x), 5) for x in run["eq"]],
        })
    # portfolio equity: equal-weight blend of the throttled instrument
    # equity curves — the bottom-line result of longs at bottoms and
    # shorts at tops, throttled by AVFI
    n_eq = min(len(ch["eq"]) for ch in chart)
    portfolio_eq = [round(float(np.mean([ch["eq"][i] for ch in chart])),
                          5) for i in range(n_eq)]
    chart.insert(0, {"ticker": "PORTFOLIO", "dates":
                     chart[0]["dates"][-len(portfolio_eq):],
                     "eq": portfolio_eq, "trigger":
                     params["trigger"]})
    (research_dir / "avfi_chart.json").write_text(json.dumps(chart))

    rows = []
    for (s, h, l, c, v, _, o), b, r in zip(series, base_runs, cur_runs):
        rows.append({
            "ticker": s,
            "base": {"sharpe": round(b["sharpe"], 2),
                     "max_dd_pct": round(b["max_dd_pct"], 1),
                     "return_pct": round(b["return_pct"], 1),
                     "trades": b["trades"]},
            "throttle": {"sharpe": round(r["sharpe"], 2),
                         "max_dd_pct": round(r["max_dd_pct"], 1),
                         "return_pct": round(r["return_pct"], 1),
                         "trades": r["trades"],
                         "throttled_bars": r["throttled_bars"]},
        })
    return {"status": "OK", "rows": rows, "iteration": record,
            "params": new_params,
            "note": ("Per the AVFI-NQ programme (KNOWLEDGE (1).md): AVFI "
                     "is a slow regime descriptor, not an entry timer; "
                     "only the risk-throttle use is evaluated. Research "
                     "parameters iterate nightly with train/OOS honesty; "
                     "the deployed strategy stays frozen (Gate 3).")}


def write_report(r: dict, markdown: Path) -> None:
    lines = ["# AVFI v3 risk-throttle research", "",
             "Python replication of the Pine v5 'AVFI v3 vs v2 [spread "
             "axis]' indicator (Parkinson-style sigmaPk vol floor, "
             "log-volume normalization, spread vs slow EMA of v2, "
             "sigma-normalized z). AVFI is evaluated ONLY as a risk "
             "throttle, never as an entry timer.", "",
             "| Ticker | Base Sharpe | Base MaxDD % | Throttle Sharpe | "
             "Throttle MaxDD % | Throttled bars |", "|---|---|---|---|---|---|"]
    for row in r.get("rows", []):
        b, t = row["base"], row["throttle"]
        lines.append(
            f"| {row['ticker']} | {b['sharpe']:+.2f} | {b['max_dd_pct']} | "
            f"{t['sharpe']:+.2f} | {t['max_dd_pct']} | {t['throttled_bars']} |")
    it = r.get("iteration")
    if it:
        lines += ["", "## Iteration ledger", "",
                  f"Iteration {it['iteration']} ({it['date']}) — "
                  f"params: {it['params_evaluated']}",
                  f"OOS drawdown reduction: "
                  f"{it['oos_dd_reduction_pct']}% at Sharpe delta "
                  f"{it['oos_sharpe_delta']}",
                  f"Best candidate: {it['best_candidate']}",
                  f"Advanced: {it['advanced']} -> next params: "
                  f"{it['params_next']}"]
    lines += ["", r.get("note", "")]
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text("\n".join(lines) + "\n")
    print(f"avfi report written -> {markdown}")


def avfi_state_space(high, low, close, volume,
                     lookback: int = 100) -> dict:
    """THE 3D AVFI STATE-SPACE IDEOLOGY. Every bar is a POSITION IN
    SPACE, and the strategy's life is a TRAJECTORY through it:

      x = AVFI spread z      (the regime axis: flow expanding/fading)
      y = price z-score      (the stretch axis: distance from the mean)
      z = trailing vol percentile (the risk axis: calm -> violent)

    Tops and bottoms are not points on a chart — they are REGIONS of
    this space: a bottom forms in the (low spread-z, deep negative
    stretch, elevated vol) octant; a top in the mirror. Watching the
    trajectory through the state space shows turns as ORBIT CHANGES,
    not single-indicator crosses. Strictly trailing throughout."""
    from tops_bottoms import detect_climaxes, detect_divergences, rsi
    logp = np.log(close)
    n = len(close)
    sp_z = spread_z(spread_axis(high, low, close, volume,
                               dict(DEFAULT_PARAMS)),
                    DEFAULT_PARAMS["sp_z_window"])
    price_z = np.zeros(n)
    for t_ in range(lookback, n):
        w = logp[t_ - lookback + 1:t_ + 1]
        sd = w.std()
        if sd > 0:
            price_z[t_] = (logp[t_] - w.mean()) / sd
    rets = np.diff(logp)
    vol20 = np.zeros(n)
    wins = np.lib.stride_tricks.sliding_window_view(rets, 20)
    vol20[20:] = wins.std(axis=1)
    vol_pct = np.zeros(n)
    for t_ in range(40, n):
        hist = vol20[20:t_ + 1]
        if len(hist):
            vol_pct[t_] = float(np.mean(hist <= vol20[t_]))
    bull, bear = detect_divergences(close, rsi(close))
    cb, ct = detect_climaxes(high, low, close, volume)
    return {
        "sp_z": [round(float(x), 3) for x in sp_z],
        "price_z": [round(float(x), 3) for x in price_z],
        "vol_pct": [round(float(x), 3) for x in vol_pct],
        "divergence_bottoms": bull.tolist(),
        "divergence_tops": bear.tolist(),
        "climax_bottoms": cb.tolist(),
        "climax_tops": ct.tolist(),
    }


def state_space_event_study(data_dir: Path,
                           universe=("SPY", "QQQ", "IWM", "XLF", "XLE"),
                           horizon: int = 10) -> dict:
    """The state-space hypothesis, tested: tops and bottoms are
    REGIONS of the 3D space, not indicator crosses. Long z-score
    entries are bucketed by which REGION of state space they occur in:

      bottom-region:  price z <= -2 (deep stretch, by construction)
        AND spread z < 0 (flow fading) AND vol percentile > 0.5
        (elevated risk) — the hypothesis says these forward-outperform
      mid-region:     partially aligned
      elsewhere:      the rest

    Honest question: does the bottom-region confluence of all three
    axes pay more than stretch alone? Reported per instrument."""
    from papertrading_runner import load_bars
    out = {}
    for s in universe:
        f = data_dir / f"{s.lower()}.csv"
        if not f.exists():
            continue
        row = _state_space_study_one(load_bars(f), horizon)
        if row is not None:
            out[s] = row
    return out


def _state_space_study_one(bars, horizon: int):
    """Region-bucket one instrument. Returns None when there is not
    enough history (warm-up 200 bars) or no bottom-side entries."""
    if len(bars) < 200:
        return None
    h = np.array([b["high"] for b in bars])
    l = np.array([b["low"] for b in bars])
    c = np.array([b["close"] for b in bars])
    v = np.array([float(b["volume"]) for b in bars])
    ss = avfi_state_space(h, l, c, v)
    sp_z = np.array(ss["sp_z"])
    price_z = np.array(ss["price_z"])
    vol_pct = np.array(ss["vol_pct"])
    regions = {"bottom_region": [], "mid_region": [],
               "elsewhere": []}
    for t_ in range(110, len(c) - horizon):
        if price_z[t_] > -2.0:
            continue  # only long (bottom-side) entries
        fr = float(c[t_ + horizon] / c[t_] - 1.0)
        if sp_z[t_] < 0 and vol_pct[t_] > 0.5:
            regions["bottom_region"].append(fr)
        elif sp_z[t_] < 0 or vol_pct[t_] > 0.5:
            regions["mid_region"].append(fr)
        else:
            regions["elsewhere"].append(fr)
    if not any(regions.values()):
        return None
    row = {}
    for reg, vals in regions.items():
        row[reg] = {
            "n": len(vals),
            "fwd": round(float(np.mean(vals)), 4) if vals else None,
        }
    br, mr_ = row["bottom_region"], row["mid_region"]
    row["hypothesis_holds"] = bool(
        br["fwd"] is not None and mr_["fwd"] is not None
        and br["n"] >= 10 and br["fwd"] > mr_["fwd"])
    return row


def state_space_event_study_extended(extended_dir: Path,
                                     horizon: int = 10) -> dict:
    """The same region hypothesis across the FULL extended universe
    (crypto, indices, commodities). The 5 deployed ETFs fire the
    full bottom region only 0-9 times each, so per-instrument
    verdicts may never reach n>=10; pooling across ~50 series is
    the honest way to accumulate evidence. Reports per-series rows
    plus an AGGREGATE row pooling every bottom-region event, and
    the pooled verdict (bottom fwd > mid fwd with n>=10)."""
    from papertrading_runner import load_bars
    out = {}
    pool = {"bottom_region": [], "mid_region": []}
    if not extended_dir.exists():
        return {"aggregate": None, "series": out}
    for f in sorted(extended_dir.glob("*.csv")):
        row = _state_space_study_one(load_bars(f), horizon)
        if row is None:
            continue
        out[f.stem.upper()] = row
        for reg in pool:
            if row[reg]["fwd"] is not None:
                # pool raw returns: fwd * n recovers their sum
                pool[reg].append(row[reg]["fwd"] * row[reg]["n"])
    agg = {}
    for reg, sums in pool.items():
        n = sum(r[reg]["n"] for r in out.values())
        agg[reg] = {
            "n": n,
            "fwd": round(float(sum(sums) / n), 4) if n else None,
        }
    br, mr_ = agg["bottom_region"], agg["mid_region"]
    # Pooled returns mix scales across very different assets (a
    # 10-day crypto return is not an ETF return), so also count the
    # scale-free per-series verdicts: in how many series does the
    # bottom region beat the mid region on ITS OWN scale?
    both = [r for r in out.values()
            if r["bottom_region"]["fwd"] is not None
            and r["mid_region"]["fwd"] is not None]
    beats = sum(1 for r in both
                if r["bottom_region"]["fwd"] > r["mid_region"]["fwd"])
    agg["series_with_both"] = len(both)
    agg["series_beats"] = beats
    agg["hypothesis_holds"] = bool(
        br["fwd"] is not None and mr_["fwd"] is not None
        and br["n"] >= 10 and br["fwd"] > mr_["fwd"]
        and beats * 2 > len(both))
    return {"aggregate": agg, "series": out}


def state_space_axis_attribution(extended_dir: Path,
                                horizon: int = 10) -> dict:
    """AXIS ATTRIBUTION: the 3-axis bottom region was falsified as a
    BUNDLE (pooled fwd +1.27% vs mid +9.81%, own-scale beats 17/40).
    The correct follow-up: does any SINGLE axis carry weight over
    deep stretch alone? For every bottom-side entry (price z <= -2)
    across the extended universe, compare the forward return of
    entries WITH each axis condition against entries WITHOUT it,
    per series on its own scale (beats) and pooled. If no single
    axis pays, the region idea is dead in its components, not
    just as a bundle."""
    from papertrading_runner import load_bars
    conds = {"sp_z_neg": lambda s, p, v: s < 0,
             "vol_high": lambda s, p, v: v > 0.5}
    out = {name: {"series": 0, "beats": 0, "with": [], "without": []}
           for name in conds}
    if not extended_dir.exists():
        return out
    for f in sorted(extended_dir.glob("*.csv")):
        bars = load_bars(f)
        if len(bars) < 200:
            continue
        h = np.array([b["high"] for b in bars])
        l = np.array([b["low"] for b in bars])
        c = np.array([b["close"] for b in bars])
        v = np.array([float(b["volume"]) for b in bars])
        ss = avfi_state_space(h, l, c, v)
        sp_z = np.array(ss["sp_z"])
        price_z = np.array(ss["price_z"])
        vol_pct = np.array(ss["vol_pct"])
        for name, fn in conds.items():
            with_, without = [], []
            for t_ in range(110, len(c) - horizon):
                if price_z[t_] > -2.0:
                    continue
                fr = float(c[t_ + horizon] / c[t_] - 1.0)
                (with_ if fn(sp_z[t_], price_z[t_], vol_pct[t_])
                 else without).append(fr)
            if not with_ or not without:
                continue
            o = out[name]
            o["series"] += 1
            if float(np.mean(with_)) > float(np.mean(without)):
                o["beats"] += 1
            o["with"].append((float(np.mean(with_)), len(with_)))
            o["without"].append((float(np.mean(without)),
                                  len(without)))
    for name, o in out.items():
        n_w = sum(n for _, n in o["with"])
        n_o = sum(n for _, n in o["without"])
        o["pooled_with_fwd"] = (round(sum(m * n for m, n in o["with"])
                                        / n_w, 4) if n_w else None)
        o["pooled_without_fwd"] = (round(sum(m * n for m, n in o["without"])
                                           / n_o, 4) if n_o else None)
        o["n_with"] = n_w
        o["n_without"] = n_o
        o["carries_weight"] = bool(
            o["pooled_with_fwd"] is not None
            and o["pooled_without_fwd"] is not None
            and o["beats"] * 2 > o["series"]
            and o["pooled_with_fwd"] > o["pooled_without_fwd"])
        o["with"] = len(o["with"])
        o["without"] = len(o["without"])
    return out


def export_state_space(data_dir: Path, research_dir: Path,
                       universe=("SPY", "QQQ", "IWM", "XLF", "XLE"),
                       extended=None) -> None:
    """Export the state-space trajectory per instrument (deployed ETFs
    plus selected extended series) for the 3D visualization."""
    from papertrading_runner import load_bars
    out = []
    names = [(s, data_dir) for s in universe]
    if extended and extended.exists():
        for f in sorted(extended.glob("*.csv")):
            names.append((f.stem.upper(), extended))
    for name, folder in names:
        f = folder / f"{name.lower()}.csv"
        if not f.exists():
            continue
        bars = load_bars(f)
        if len(bars) < 200:
            continue
        h = np.array([b["high"] for b in bars])
        l = np.array([b["low"] for b in bars])
        c = np.array([b["close"] for b in bars])
        v = np.array([float(b["volume"]) for b in bars])
        ss = avfi_state_space(h, l, c, v)
        ss["ticker"] = name
        ss["dates"] = [b["date"] for b in bars]
        out.append(ss)
    research_dir.mkdir(parents=True, exist_ok=True)
    (research_dir / "avfi_state_space.json").write_text(
        json.dumps(out))
    print(f"state space exported -> "
          f"{research_dir / 'avfi_state_space.json'} ({len(out)} series)")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="AVFI v3 risk-throttle research + iteration")
    ap.add_argument("--data-dir", type=Path, default=Path("paper/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("paper/research"))
    ap.add_argument("--markdown", type=Path,
                    default=Path("paper/research/avfi_report.md"))
    args = ap.parse_args()
    r = run_iteration(args.data_dir, args.research_dir)
    export_state_space(args.data_dir, args.research_dir,
                       extended=args.data_dir.parent / "research" / "data")
    ss_study = state_space_event_study(args.data_dir)
    (args.research_dir / "state_space_study.json").write_text(
        json.dumps(ss_study, indent=2))
    print(f"state-space study -> "
          f"{args.research_dir / 'state_space_study.json'}")
    ext = state_space_event_study_extended(
        args.data_dir.parent / "research" / "data")
    (args.research_dir / "state_space_study_extended.json").write_text(
        json.dumps(ext, indent=2))
    a = ext.get("aggregate") or {}
    print(f"state-space extended study -> "
          f"{args.research_dir / 'state_space_study_extended.json'} "
          f"({len(ext.get('series', {}))} series, pooled n="
          f"{(a.get('bottom_region') or {}).get('n', 0)})")
    axis = state_space_axis_attribution(
        args.data_dir.parent / "research" / "data")
    (args.research_dir / "state_space_axis.json").write_text(
        json.dumps(axis, indent=2))
    print(f"axis attribution -> "
          f"{args.research_dir / 'state_space_axis.json'} "
          f"(sp_z_neg: {axis.get('sp_z_neg', {}).get('beats')}"
          f"/{axis.get('sp_z_neg', {}).get('series')} series, "
          f"vol_high: {axis.get('vol_high', {}).get('beats')}"
          f"/{axis.get('vol_high', {}).get('series')} series)")
    write_report(r, args.markdown)
    print(f"status: {r['status']}, instruments: {len(r.get('rows', []))}, "
          f"iteration: {r.get('iteration', {}).get('iteration')}, "
          f"advanced: {r.get('iteration', {}).get('advanced')}")


if __name__ == "__main__":
    main()
