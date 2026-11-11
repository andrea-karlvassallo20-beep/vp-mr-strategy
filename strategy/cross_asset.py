"""Cross-asset edge research: crypto, indices, commodities.

The deployed champion (VP-MR-ETF-D1-001) stays frozen (Gate 3). This
module explores whether the mean-reversion edge exists in OTHER asset
classes: crypto (BTC, ETH), main indices (S&P 500, Nasdaq, Dow), and
commodities (gold, crude, silver). For each series it estimates the
 Ornstein-Uhlenbeck mean-reversion half-life and runs a quick
production-style z-score strategy, compared against buy-and-hold.
Honest by design: results are reported even when they are negative.

Usage:
    python3 cross_asset.py --research-dir ./paper/research \
        --markdown ./paper/research/cross_asset_report.md
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import fetch_yfinance, write_csv

EXTENDED_UNIVERSE = [
    ("crypto", "BTC-USD"),
    ("crypto", "ETH-USD"),
    ("index", "^GSPC"),
    ("index", "^IXIC"),
    ("index", "^DJI"),
    ("commodity", "GC=F"),
    ("commodity", "CL=F"),
    ("commodity", "SI=F"),
]

WARMUP = 60
Z_ENTRY = 2.0
Z_EXIT = 0.5
COST_BPS = 5.0


def safe_name(ticker: str) -> str:
    return ticker.replace("^", "").replace("=F", "F").replace("-", "")


def ou_ar1_stats(prices: np.ndarray):
    """AR(1) fit on log prices. Returns (half_life_bars, t_stat) where
    t_stat tests the mean-reversion coefficient (Dickey-Fuller style;
    random walks have finite-sample downward bias, so the t-statistic —
    not the half-life alone — decides if a series genuinely reverts)."""
    lg = np.log(prices)
    lag, delta = lg[:-1], np.diff(lg)
    x = lag - lag.mean()
    denom = float(np.dot(x, x))
    if denom <= 0:
        return math.inf, 0.0
    phi_ar = float(np.dot(x, delta - delta.mean())) / denom
    resid = delta - delta.mean() - phi_ar * x
    se = math.sqrt(float(np.dot(resid, resid)) / (len(x) - 2) / denom)
    t = phi_ar / se if se > 0 else 0.0
    phi = 1.0 + phi_ar
    if 0.0 < phi < 1.0:
        return -math.log(2.0) / math.log(phi), t
    return math.inf, t


def ou_half_life(prices: np.ndarray) -> float:
    """Discrete OU half-life (bars) from an AR(1) fit on log prices.
    Returns float('inf') when the series is not mean-reverting
    (phi <= 0 or phi >= 1)."""
    return ou_ar1_stats(prices)[0]


def zscore_mr_backtest(prices: np.ndarray, warmup: int = WARMUP,
                       z_entry: float = Z_ENTRY, z_exit: float = Z_EXIT,
                       cost_bps: float = COST_BPS):
    """Production-style z-score mean reversion, vol-scaled unit sizing.
    Strictly causal: rolling stats on data up to t, position held from
    t+1. Returns (sharpe, n_trades, total_return_pct)."""
    logp = np.log(prices)
    rets = np.diff(logp)
    n = len(prices)
    pos = np.zeros(n)
    cur = 0.0
    for t in range(warmup, n - 1):
        window = logp[t - warmup + 1:t + 1]
        mu = window.mean()
        sd = window.std()
        if sd <= 0:
            continue
        z = (logp[t] - mu) / sd
        if cur == 0.0 and abs(z) >= z_entry:
            cur = -1.0 if z > 0 else 1.0
        elif cur != 0.0 and abs(z) <= z_exit:
            cur = 0.0
        pos[t + 1] = cur
    volatility = np.std(rets) * math.sqrt(252) or 1.0
    sized = pos[1:] / volatility
    strat = sized * rets
    trades = int(np.sum(np.abs(np.diff(pos)) > 0))
    if trades:
        strat = strat - np.abs(np.diff(pos, prepend=0.0)[1:]) * cost_bps / 1e4
    mean = strat.mean()
    sd = strat.std()
    sharpe = float(mean / sd * math.sqrt(252)) if sd > 0 else 0.0
    total = float((np.exp(np.sum(strat)) - 1.0) * 100.0)
    return sharpe, trades, total


def buy_hold_sharpe(prices: np.ndarray) -> float:
    rets = np.diff(np.log(prices))
    sd = rets.std()
    if sd <= 0:
        return 0.0
    return float(rets.mean() / sd * math.sqrt(252))


def analyze_series(prices: np.ndarray) -> dict:
    hl, t_stat = ou_ar1_stats(prices)
    mr_sharpe, trades, mr_ret = zscore_mr_backtest(prices)
    bh = buy_hold_sharpe(prices)
    return {
        "bars": int(len(prices)),
        "half_life_bars": None if math.isinf(hl) else round(hl, 1),
        "mr_t_stat": round(t_stat, 2),
        "mean_reverting": bool(t_stat < -3.0 and math.isfinite(hl)),
        "mr_sharpe": round(mr_sharpe, 2),
        "mr_trades": trades,
        "mr_return_pct": round(mr_ret, 2),
        "buy_hold_sharpe": round(bh, 2),
    }


def run_research(research_dir: Path, fetch: bool = True,
                 period: str = "5y") -> list:
    """Fetch (or reuse cached) extended-universe bars and analyze each."""
    data_dir = research_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for asset_class, ticker in EXTENDED_UNIVERSE:
        name = safe_name(ticker)
        csv_path = data_dir / f"{name.lower()}.csv"
        prices = None
        fetch_error = None
        if fetch:
            try:
                rows = fetch_yfinance(ticker, period=period)
                write_csv(csv_path, rows)
            except Exception as e:
                fetch_error = str(e)
        if csv_path.exists():
            raw = [l.split(",") for l in
                   csv_path.read_text().strip().splitlines()[1:]]
            if raw:
                prices = np.array([float(r[4]) for r in raw])
        if prices is None or len(prices) < WARMUP + 60:
            results.append({
                "asset_class": asset_class, "ticker": ticker,
                "status": "NO_DATA",
                "error": fetch_error or "insufficient bars",
            })
            continue
        res = analyze_series(prices)
        res.update({"asset_class": asset_class, "ticker": ticker,
                    "status": "OK"})
        results.append(res)
    return results


def write_report(results: list, markdown: Path) -> None:
    ok = [r for r in results if r["status"] == "OK"]
    lines = ["# Cross-asset edge research", "",
             "Does the mean-reversion edge exist outside the deployed",
             "universe? Each series: OU half-life estimate and a",
             "production-style z-score backtest vs buy-and-hold.",
             "The deployed champion stays frozen (Gate 3); this is",
             "research toward future challenger candidates.", "",
             "| Class | Ticker | Bars | OU half-life | MR Sharpe | "
             "MR trades | MR return | B&H Sharpe | Mean-reverting? |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(results, key=lambda x: (x["asset_class"], x["ticker"])):
        if r["status"] != "OK":
            lines.append(f"| {r['asset_class']} | {r['ticker']} | - | - | "
                          f"- | - | - | - | NO DATA ({r['error']}) |")
            continue
        hl = r["half_life_bars"] if r["half_life_bars"] is not None \
            else "none"
        lines.append(
            f"| {r['asset_class']} | {r['ticker']} | {r['bars']} | {hl} | "
            f"{r['mr_sharpe']:+.2f} | {r['mr_trades']} | "
            f"{r['mr_return_pct']:+.1f}% | {r['buy_hold_sharpe']:+.2f} | "
            f"{'yes' if r['mean_reverting'] else 'no'} |")
    if ok:
        best = max(ok, key=lambda r: r["mr_sharpe"])
        lines += ["", f"Best mean-reversion candidate: **{best['ticker']}** "
                  f"({best['asset_class']}) with MR Sharpe "
                  f"{best['mr_sharpe']:+.2f} vs buy-and-hold "
                  f"{best['buy_hold_sharpe']:+.2f}.", ""]
        mr_positive = [r for r in ok if r["mr_sharpe"] > 0
                       and r["mr_sharpe"] > r["buy_hold_sharpe"]]
        if mr_positive:
            lines.append("Series where mean reversion beats buy-and-hold: "
                         + ", ".join(r["ticker"] for r in mr_positive) + ".")
        else:
            lines.append("No series currently shows a mean-reversion edge "
                         "over buy-and-hold — an honest null result.")
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text("\n".join(lines) + "\n")
    print(f"cross-asset report written -> {markdown}")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Cross-asset mean-reversion edge research")
    ap.add_argument("--research-dir", type=Path,
                    default=Path("paper/research"))
    ap.add_argument("--markdown", type=Path,
                    default=Path("paper/research/cross_asset_report.md"))
    ap.add_argument("--no-fetch", action="store_true",
                    help="analyze cached CSVs only")
    ap.add_argument("--period", default="5y")
    args = ap.parse_args()
    results = run_research(args.research_dir, fetch=not args.no_fetch,
                          period=args.period)
    json_path = args.research_dir / "cross_asset.json"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(results, indent=2))
    print(f"results written -> {json_path}")
    write_report(results, args.markdown)


if __name__ == "__main__":
    main()
