"""Tops-and-bottoms detection: divergence and climax detectors.

Two knowledge-grounded detectors for finding turns, both strictly
trailing (Gate 1):

1. RSI DIVERGENCE (Elliott Wave / classic timing layer):
   a bottom when price prints a lower low but RSI prints a higher low
   (momentum refuses to confirm the new price extreme); a top when
   price prints a higher high but RSI prints a lower high.

2. VSA CLIMAX (Master the Markets, "effort vs results"):
   a bottom when volume >= 2x its trailing mean AND the bar's range is
   wide AND the close recovers into the upper half of the bar after a
   decline (effort huge, result reversed = selling exhaustion); a top
   is the mirror after a rally.

Evaluation is an honest event study: for every plain z-score entry
(the production signal), compare forward returns when the entry IS vs
IS NOT confirmed by a detector — and report the standalone detector
hit rates. Negative results are reported.

Usage (nightly):
    python3 tops_bottoms.py --data-dir ./paper/data \
        --research-dir ./paper/research
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from papertrading_runner import load_bars

RSI_WINDOW = 14
DIVERGENCE_LOOKBACK = 20
CLIMAX_VOL_MULT = 2.0
CLIMAX_RANGE_MULT = 1.5
Z_ENTRY = 2.0
LOOKBACK = 100
WARMUP = 110


def rsi(close: np.ndarray, window: int = RSI_WINDOW) -> np.ndarray:
    """Wilder's RSI, strictly trailing."""
    delta = np.diff(close)
    out = np.zeros(len(close))
    gain = np.zeros(len(delta))
    loss = np.zeros(len(delta))
    gain[delta > 0] = delta[delta > 0]
    loss[-delta > 0] = -delta[-delta > 0]
    avg_g = np.zeros(len(delta))
    avg_l = np.zeros(len(delta))
    if len(delta) == 0:
        return out
    avg_g[window - 1] = gain[:window].mean()
    avg_l[window - 1] = loss[:window].mean()
    for t in range(window, len(delta)):
        avg_g[t] = (avg_g[t - 1] * (window - 1) + gain[t]) / window
        avg_l[t] = (avg_l[t - 1] * (window - 1) + loss[t]) / window
    rs = np.where(avg_l > 0, avg_g / np.where(avg_l == 0, 1e-9, avg_l),
                  np.inf)
    val = 100.0 - 100.0 / (1.0 + rs)
    out[window:] = val[window - 1:]
    return out


def detect_divergences(close: np.ndarray, rsi_arr: np.ndarray,
                       lookback: int = DIVERGENCE_LOOKBACK):
    """Bullish/bearish RSI divergences, strictly trailing. Returns
    (bullish_idx, bearish_idx) arrays of bar indices where the
    divergence is confirmed."""
    bull, bear = [], []
    n = len(close)
    for t in range(lookback + 2, n):
        ref = t - lookback
        # bullish: price lower low, RSI higher low
        if close[t] < close[ref] and rsi_arr[t] > rsi_arr[ref] \
                and close[t] == close[max(t - 3, 0):t + 1].min() \
                and rsi_arr[t] < 40:
            bull.append(t)
        # bearish: price higher high, RSI lower high
        elif close[t] > close[ref] and rsi_arr[t] < rsi_arr[ref] \
                and close[t] == close[max(t - 3, 0):t + 1].max() \
                and rsi_arr[t] > 60:
            bear.append(t)
    return np.array(bull, dtype=int), np.array(bear, dtype=int)


def detect_climaxes(high, low, close, volume,
                   vol_mult: float = CLIMAX_VOL_MULT,
                   range_mult: float = CLIMAX_RANGE_MULT):
    """VSA climax bars: huge effort (volume AND range stretched vs
    their trailing means) with a result that reverses the bar's own
    direction. Returns (bottom_idx, top_idx)."""
    n = len(close)
    rng = (high - low) / np.maximum(close, 1e-9)
    vol_avg = np.zeros(n)
    rng_avg = np.zeros(n)
    csum_v = np.cumsum(volume)
    csum_r = np.cumsum(rng)
    for t in range(n):
        lo = max(0, t - 20)
        cnt = t - lo + 1
        vol_avg[t] = (csum_v[t] - (csum_v[lo - 1] if lo > 0 else 0)) / cnt
        rng_avg[t] = (csum_r[t] - (csum_r[lo - 1] if lo > 0 else 0)) / cnt
    up_half = (close - low) / np.maximum(high - low, 1e-9)
    bottoms, tops = [], []
    for t in range(30, n):
        if volume[t] < vol_mult * vol_avg[t] or \
                rng[t] < range_mult * rng_avg[t]:
            continue
        # the trend INTO the bar (excluding the reversal bar itself)
        declined = close[t - 1] < close[max(t - 10, 0)]
        rallied = close[t - 1] > close[max(t - 10, 0)]
        if declined and up_half[t] >= 0.6:
            bottoms.append(t)
        elif rallied and up_half[t] <= 0.4:
            tops.append(t)
    return np.array(bottoms, dtype=int), np.array(tops, dtype=int)


def turn_topology(high, low, close, volume,
                  lookback: int = LOOKBACK, z_entry: float = Z_ENTRY):
    """MULTI-DIMENSIONAL TURN TOPOLOGY. At every bar, five strictly
    trailing dimensions are evaluated for a BOTTOM and a TOP:

      1. PRICE   — z-score stretch in the turn direction (z <= -2 / >= +2)
      2. MOMENTUM— RSI in turn territory (< 40 / > 60)
      3. DIVERGE — RSI divergence confirmed within the last 3 bars
      4. EFFORT  — VSA climax confirmed within the last 3 bars
      5. REGIME  — the AVFI spread z is exhausted and turning (for a
                   bottom: sp_z < 0 and rising over the last 3 bars —
                   flow already washed out; mirror for tops)

    Returns (bottom_score, top_score) integer arrays, 0..5 each. A turn
    is "tradeable" when several dimensions ALIGN — confluence, not any
    single indicator, is the hypothesis."""
    from avfi import DEFAULT_PARAMS, spread_axis, spread_z
    n = len(close)
    r = rsi(close)
    bull, bear = detect_divergences(close, r)
    cb, ct = detect_climaxes(high, low, close, volume)
    sp_z = spread_z(spread_axis(high, low, close, volume,
                                dict(DEFAULT_PARAMS)),
                    DEFAULT_PARAMS["sp_z_window"])
    near = lambda idxs: {int(i) for i in idxs}

    def recent(idxs, t, span=3):
        return any(t - span <= i <= t for i in idxs)

    bull_s, bear_s = near(bull), near(bear)
    cb_s, ct_s = near(cb), near(ct)
    logp = np.log(close)
    bottom_score = np.zeros(n, dtype=int)
    top_score = np.zeros(n, dtype=int)
    for t_ in range(lookback + 1, n):
        w = logp[t_ - lookback + 1:t_ + 1]
        sd = w.std()
        z = (logp[t_] - w.mean()) / sd if sd > 0 else 0.0
        # dimension 1: price stretch
        b1 = z <= -z_entry
        t1 = z >= z_entry
        # dimension 2: momentum territory
        b2 = r[t_] < 40
        t2 = r[t_] > 60
        # dimension 3: divergence (recent)
        b3 = recent(bull_s, t_)
        t3 = recent(bear_s, t_)
        # dimension 4: climax effort (recent)
        b4 = recent(cb_s, t_)
        t4 = recent(ct_s, t_)
        # dimension 5: AVFI regime exhaustion turning
        regime_turn_up = (sp_z[t_] < 0 and t_ >= 3
                          and sp_z[t_] > sp_z[t_ - 3])
        regime_turn_dn = (sp_z[t_] > 0 and t_ >= 3
                          and sp_z[t_] < sp_z[t_ - 3])
        # numpy bool_ + bool_ is logical OR, not addition — cast to int
        bottom_score[t_] = (int(b1) + int(b2) + int(b3) + int(b4)
                            + int(regime_turn_up))
        top_score[t_] = (int(t1) + int(t2) + int(t3) + int(t4)
                          + int(regime_turn_dn))
    return bottom_score, top_score


def topology_buckets(close, entries, bottom_score, top_score,
                     horizon: int = 10):
    """Forward returns of z-score entries bucketed by how many topology
    dimensions align. Monotonicity across buckets is the honest test."""
    buckets = {}
    for t_, d in entries:
        sc = int(bottom_score[t_]) if d == 1 else int(top_score[t_])
        fr = forward_returns(close, t_, horizon)
        if fr is None:
            continue
        buckets.setdefault(sc, []).append((fr, d))
    out = {}
    for sc, vals in sorted(buckets.items()):
        longs = [fr for fr, dd in vals if dd == 1]
        shorts = [fr for fr, dd in vals if dd == -1]
        out[sc] = {
            "n": len(vals),
            "long_fwd": round(float(np.mean(longs)), 4) if longs else None,
            "short_fwd": round(float(np.mean(shorts)), 4)
            if shorts else None,
            "short_fwd_neg": round(float(-np.mean(shorts)), 4)
            if shorts else None,
        }
    return out


def z_entries(close: np.ndarray, lookback: int = LOOKBACK,
              z_entry: float = Z_ENTRY):
    """Plain z-score bottom-long / top-short signals (production)."""
    logp = np.log(close)
    entries = []
    for t in range(lookback + 1, len(close)):
        w = logp[t - lookback + 1:t + 1]
        sd = w.std()
        if sd <= 0:
            continue
        z = (logp[t] - w.mean()) / sd
        if z <= -z_entry:
            entries.append((t, 1))
        elif z >= z_entry:
            entries.append((t, -1))
    return entries


def forward_returns(close: np.ndarray, idx: int, horizon: int = 10):
    """Forward return over `horizon` bars after idx (None at the end)."""
    if idx + horizon >= len(close):
        return None
    return float(close[idx + horizon] / close[idx] - 1.0)


def event_study(close, entries, confirm_idx) -> dict:
    """Compare forward returns of confirmed vs unconfirmed entries.
    confirm_idx: set of bar indices where ANY detector confirms."""
    conf, unconf = [], []
    for t, d in entries:
        window = range(max(0, t - 3), t + 1)
        r = forward_returns(close, t)
        if r is None:
            continue
        (conf if any(i in confirm_idx for i in window) else
         unconf).append((r, d))
    def mean_side(vals, d):
        side = [r for r, dd in vals if dd == d]
        return float(np.mean(side)) if side else None
    def hit_rate(vals, d):
        side = [r for r, dd in vals if dd == d]
        if not side:
            return None
        return float(np.mean([1.0 if (r > 0) == (d > 0) else 0.0
                               for r in side]))
    return {
        "n_confirmed": len(conf), "n_unconfirmed": len(unconf),
        "long_confirmed_fwd": mean_side(conf, 1),
        "long_unconfirmed_fwd": mean_side(unconf, 1),
        "short_confirmed_fwd": mean_side(conf, -1),
        "short_unconfirmed_fwd": mean_side(unconf, -1),
        "long_confirmed_hit": hit_rate(conf, 1),
        "short_confirmed_hit": hit_rate(conf, -1),
    }


def run_study(data_dir: Path,
              universe=("SPY", "QQQ", "IWM", "XLF", "XLE")) -> dict:
    rows = []
    charts = []
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
        r = rsi(c)
        bull, bear = detect_divergences(c, r)
        cb, ct = detect_climaxes(h, l, c, v)
        entries = z_entries(c)
        confirm = set(bull.tolist()) | set(cb.tolist()) | \
            set(bear.tolist()) | set(ct.tolist())
        study = event_study(c, entries, confirm)
        b_score, t_score = turn_topology(h, l, c, v)
        buckets = topology_buckets(c, entries, b_score, t_score)
        rows.append({
            "ticker": s,
            "n_divergence_bottoms": int(len(bull)),
            "n_divergence_tops": int(len(bear)),
            "n_climax_bottoms": int(len(cb)),
            "n_climax_tops": int(len(ct)),
            "n_z_entries": len(entries),
            **{k: (round(x, 4) if isinstance(x, float) else x)
               for k, x in study.items()},
            "topology_buckets": {str(k): v for k, v in buckets.items()},
        })
        charts.append({
            "ticker": s,
            "dates": [b["date"] for b in bars],
            "close": [round(float(x), 2) for x in c],
            "divergence_bottoms": bull.tolist(),
            "divergence_tops": bear.tolist(),
            "climax_bottoms": cb.tolist(),
            "climax_tops": ct.tolist(),
        })
    return {"status": "OK" if rows else "NO_DATA", "rows": rows,
            "charts": charts}


def write_report(r: dict, markdown: Path) -> None:
    lines = ["# Tops-and-bottoms detection study", "",
             "Two strictly-trailing detectors — RSI divergence and VSA "
             "volume climax — checked against the plain z-score entries: "
             "do confirmed entries forward-perform better than "
             "unconfirmed ones? Honest by design.", "",
             "| Ticker | div bot | div top | clim bot | clim top | z "
             "entries | confirmed | unconfirmed | long fwd (conf) | "
             "long fwd (unconf) | short fwd (conf) | short fwd "
             "(unconf) |", "|---|---|---|---|---|---|---|---|---|---|"
             "---|---|"]
    for row in r.get("rows", []):
        fmt = lambda x: f"{x:+.4f}" if isinstance(x, float) else "-"
        lines.append(
            f"| {row['ticker']} | {row['n_divergence_bottoms']} | "
            f"{row['n_divergence_tops']} | {row['n_climax_bottoms']} | "
            f"{row['n_climax_tops']} | {row['n_z_entries']} | "
            f"{row['n_confirmed']} | {row['n_unconfirmed']} | "
            f"{fmt(row['long_confirmed_fwd'])} | "
            f"{fmt(row['long_unconfirmed_fwd'])} | "
            f"{fmt(row['short_confirmed_fwd'])} | "
            f"{fmt(row['short_unconfirmed_fwd'])} |")
    lines += ["", "## Multi-dimensional turn topology (confluence score)",
              "",
              "Forward returns by number of aligned dimensions "
              "(price stretch, momentum, divergence, effort, AVFI regime)",
              "at the entry bar. Monotonicity across buckets is the "
              "honest test.", "",
              "| Ticker | score | n | long fwd | short fwd (neg) |",
              "|---|---|---|---|---|"]
    for row in r.get("rows", []):
        for sc, b in sorted(row.get("topology_buckets", {}).items(),
                            key=lambda kv: int(kv[0])):
            lf = b["long_fwd"]
            sf = b["short_fwd_neg"]
            lf_s = f"{lf:+.4f}" if lf is not None else "-"
            sf_s = f"{sf:+.4f}" if sf is not None else "-"
            lines.append(f"| {row['ticker']} | {sc} | {b['n']} | "
                         f"{lf_s} | {sf_s} |")
    lines += ["", "Reading: a detector helps only if confirmed entries "
              "forward-outperform unconfirmed ones on the correct side. "
              "Anything else is reported as a null result."]
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text("\n".join(lines) + "\n")
    print(f"tops/bottoms report written -> {markdown}")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Tops-and-bottoms detector study")
    ap.add_argument("--data-dir", type=Path, default=Path("paper/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("paper/research"))
    args = ap.parse_args()
    r = run_study(args.data_dir)
    write_report(r, args.research_dir / "tops_bottoms_report.md")
    args.research_dir.mkdir(parents=True, exist_ok=True)
    (args.research_dir / "tops_bottoms.json").write_text(
        json.dumps(r, indent=2))
    print(f"results written -> {args.research_dir / 'tops_bottoms.json'}")


if __name__ == "__main__":
    main()
