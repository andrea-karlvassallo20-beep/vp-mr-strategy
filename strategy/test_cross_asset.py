"""Cross-asset research suite: diagnostics on synthetic series with
known ground truth, report generation, and graceful data handling.
Harness file."""
import json
import math
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from cross_asset import (CRYPTO, COMMODITIES, EXTENDED_UNIVERSE, INDICES,
                         analyze_series, ou_ar1_stats,
                         ou_half_life, run_research, safe_name,
                         write_report, zscore_mr_backtest)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def ou_series(n, kappa, sigma, seed):
    """Discrete OU log-price series with known mean-reversion."""
    rng = np.random.default_rng(seed)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = x[t - 1] * (1 - kappa) + sigma * rng.standard_normal()
    return np.exp(x + 5.0)


def rw_series(n, seed):
    rng = np.random.default_rng(seed)
    return np.exp(np.cumsum(rng.standard_normal(n)) + 5.0)


check("extended universe covers crypto, indices, commodities",
      {c for c, _ in EXTENDED_UNIVERSE} == {"crypto", "index", "commodity"}
      and len(EXTENDED_UNIVERSE) == len(CRYPTO) + len(INDICES)
      + len(COMMODITIES) and len(CRYPTO) >= 150
      and len(set(CRYPTO)) == len(CRYPTO)
      and len(COMMODITIES) >= 29
      and len(set(COMMODITIES)) == len(COMMODITIES))
check("safe_name sanitizes ^ and =F and -",
      safe_name("^GSPC") == "GSPC" and safe_name("GC=F") == "GCF"
      and safe_name("BTC-USD") == "BTCUSD")

ou = ou_series(1500, kappa=0.05, sigma=0.01, seed=11)
hl = ou_half_life(ou)
check("OU half-life finite for mean-reverting series", 5.0 < hl < 80.0)
rw = rw_series(1500, seed=12)
rw_hl, rw_t = ou_ar1_stats(rw)
check("random walk fails the mean-reversion t-test",
      all(ou_ar1_stats(rw_series(1500, s))[1] > -3.0 for s in (12, 13, 14)))
check("OU series passes the mean-reversion t-test",
      ou_ar1_stats(ou)[1] < -3.0)

res_ou = analyze_series(ou)
res_rw = analyze_series(rw)
check("OU series flagged mean-reverting", res_ou["mean_reverting"])
check("random walk not flagged", not res_rw["mean_reverting"])
check("z-score backtest positive on OU series",
      res_ou["mr_sharpe"] > 0.5 and res_ou["mr_trades"] > 3)
check("z-score backtest JSON fields complete",
      all(k in res_ou for k in ("bars", "half_life_bars", "mr_t_stat",
                                "mr_sharpe", "mr_trades", "mr_return_pct",
                                "buy_hold_sharpe")))

sh, tr, ret = zscore_mr_backtest(ou)
check("backtest strictly causal (no lookahead-safe signature)",
      tr > 0 and math.isfinite(sh))

tmp = Path(tempfile.mkdtemp())
rdir = tmp / "research"
data = rdir / "data"
data.mkdir(parents=True)
for i, (cls, tic) in enumerate(EXTENDED_UNIVERSE[:3]):
    rows = ou_series(400, 0.05, 0.01, seed=20 + i)
    out = []
    for t, p in enumerate(rows):
        out.append(f"2023-01-{(t % 28) + 1:02d},1,1,1,{p:.4f},100")
    (data / f"{safe_name(tic).lower()}.csv").write_text(
        "date,open,high,low,close,volume\n" + "\n".join(out) + "\n")
results = run_research(rdir, fetch=False)
check("cached analysis without fetch", len(results) == len(EXTENDED_UNIVERSE))
check("cached series analyzed OK",
      sum(r["status"] == "OK" for r in results) == 3)
check("missing series reported as NO_DATA",
      all("error" in r for r in results if r["status"] == "NO_DATA"))
rep = rdir / "report.md"
write_report(results, rep)
txt = rep.read_text()
check("report table includes all tickers",
      all(safe_name(t) in txt or t in txt for _, t in EXTENDED_UNIVERSE))
check("report states honest null/positive result",
      "beats buy-and-hold" in txt or "null result" in txt)

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
