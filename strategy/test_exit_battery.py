"""Exit battery suite: the entry/exit machinery measured against
KNOWN ground truth - a hand-computed exit path, the episode
cooldown, the dual-split gate refusing a decaying edge, and the
battery's structure on a synthetic universe (every cell present,
per-asset breakdown mandatory, fewer trades only when earned).
Harness file."""
import datetime as _dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from exit_battery import (HOLDS, HOLD_WEEKS, V4_WINDOW, WEEK,
                          MAX_CONCURRENT, _cell_stats, _entries,
                          _exit_return, portfolio_sim,
                          run_exit_battery)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


# --- hand-computed exit path -------------------------------------
# entry at t=300; week 1 +5%, weeks 2-4 flat
logc = np.zeros(400)
logc[300] = 0.0
logc[305] = 0.05
logc[310] = logc[315] = logc[320] = 0.05
r, w, took = _exit_return(logc, 300, 4)
check("time exit holds to the full window",
      abs(r - 0.05) < 1e-9 and w == 4 and not took)
r, w, took = _exit_return(logc, 300, 4, profit_take=0.02)
check("profit take exits at the first clearing week",
      abs(r - 0.05) < 1e-9 and w == 1 and took)
r, w, took = _exit_return(logc, 300, 4, profit_take=0.06)
check("a take the path never clears falls back to the time exit",
      abs(r - 0.05) < 1e-9 and w == 4 and not took)
# a DOWN path: week 1 -3%, week 2 cumulative +3%
logc2 = np.zeros(400)
logc2[300] = 0.0
logc2[305] = -0.03
logc2[310] = 0.03
logc2[315] = logc2[320] = 0.03
r, w, took = _exit_return(logc2, 300, 4, profit_take=0.02)
check("profit take reads the CUMULATIVE path, not weekly bars",
      abs(r - 0.03) < 1e-9 and w == 2 and took)

# --- episode entries + cooldown ----------------------------------
# daily increments: quiet, then one crash WEEK (-7.25%)
n = 600
rets3 = np.full(n, 0.001)
for k in range(260, n - 60, 260):
    rets3[k:k + 5] = -0.0145
logc3 = np.cumsum(rets3)
ents = _entries(logc3, n, WEEK * HOLD_WEEKS)
check("entries fire at zone crosses",
      len(ents) > 0 and all(
          -0.10 <= float(logc3[t] - logc3[t - WEEK]) < -0.05
          for t in ents))
check("cooldown forbids re-entry while the hold runs",
      all(b - a >= WEEK * HOLD_WEEKS
          for a, b in zip(ents, ents[1:])))

# --- the dual-split gate refuses a decaying edge ------------------
good = [{"ticker": "X", "t": i, "net": 0.02,
         "exit_week": 4, "profit_take_hit": False}
        for i in range(30)]
bad = good[:15] + [{"ticker": "X", "t": i, "net": -0.02,
                    "exit_week": 4, "profit_take_hit": False}
                   for i in range(15, 30)]
check("gate passes a stable edge",
      _cell_stats(good)["dual_split_gate"])
check("gate refuses an edge that decays in both worse windows",
      not _cell_stats(bad)["dual_split_gate"])
check("thin cells are refused, not flattered",
      _cell_stats(good[:5]).get("verdict")
      == "INSUFFICIENT_TRADES")

# --- the battery on a synthetic universe -------------------------
tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
res = tmp / "research"
data.mkdir(parents=True)
res.mkdir(parents=True)


def _write_series(path, rets, d0=(2015, 1, 1)):
    prices = 100.0 * np.exp(np.cumsum(rets))
    d0 = _dt.date(*d0)
    rows = []
    for i, p in enumerate(prices):
        d = (d0 + _dt.timedelta(days=i)).isoformat()
        rows.append((d, round(float(p), 4),
                     round(float(p) * 1.002, 4),
                     round(float(p) * 0.998, 4),
                     round(float(p), 4), 1_000_000.0))
    write_csv(path, rows)


# a bouncing asset: crash weeks, a recovery that PEAKS at
# week 2 and fades - the shape where a profit take earns its
# keep against the 4-week time exit
rng = np.random.default_rng(7)
n1 = 2600
rets1 = np.full(n1, 0.0004)
for k in range(260, n1 - 60, 260):
    rets1[k + 3:k + 5] = -0.03625   # one crash week (-7.25%)
    rets1[k + 5:k + 15] = 0.0035    # two recovery weeks
    rets1[k + 15:k + 25] = -0.0025  # the fade
rets1 += 0.0002 * rng.standard_normal(n1)
_write_series(data / "SIF.csv", rets1)
# a falling-knife asset: crashes that keep falling
rets2 = np.full(n1, 0.0002)
for k in range(260, n1 - 60, 260):
    rets2[k + 3:k + 5] = -0.03625
    rets2[k + 5:k + 25] = -0.001
rets2 += 0.0002 * rng.standard_normal(n1)
_write_series(data / "CLF.csv", rets2, d0=(2015, 1, 1))

r = run_exit_battery(data)
check("the battery runs and reports every cell",
      r["status"] == "OK"
      and [c["hold_weeks"] for c in r["hold_ladder"]]
      == list(HOLDS)
      and len(r["profit_take_cells"]) == 2
      and len(r["entry_filter_cells"]) == 3
      and len(r["filter_plus_2w_combos"]) == 3)
check("the baseline is the 4-week production hold",
      r["baseline_4w"]["hold_weeks"] == HOLD_WEEKS)
check("exposure is measured from actual exit weeks",
      all(c["exposure_bars"] <= WEEK * HOLD_WEEKS * c["n"]
          for c in r["hold_ladder"]))
check("every cell with trades carries the per-asset "
      "breakdown",
      all("per_asset" in c
          and (c["per_asset"] or c.get("verdict"))
          for c in r["hold_ladder"]
          + r["profit_take_cells"]
          + r["entry_filter_cells"]))
check("the bounce asset is the positive cell and the knife "
      "is negative in the breakdown",
      r["baseline_4w"]["per_asset"]["SIF"]["positive"]
      and not r["baseline_4w"]["per_asset"]["CLF"]["positive"])
check("on the bounce design the profit take must beat the "
      "time exit median",
      any(c.get("median_net", 0)
          > r["baseline_4w"].get("median_net", 0)
          for c in r["profit_take_cells"]))
check("the three verdicts are stated, honestly either way",
      all(isinstance(r[k], str) and r[k]
          for k in ("verdict", "profit_take_verdict",
                    "entry_filter_verdict")))

# --- the portfolio block: same entries, exits differ ----------
pb = r.get("portfolio_block", {})
check("the portfolio block carries both variants and a "
      "verdict",
      pb.get("baseline_4w", {}).get("status") == "OK"
      and pb.get("pt_4pct", {}).get("status") == "OK"
      and isinstance(pb.get("verdict"), str) and pb["verdict"])
check("both portfolio variants trade the same entries",
      pb["baseline_4w"]["n_trades"]
      == pb["pt_4pct"]["n_trades"])
check("the profit take spends LESS time in the market",
      len(pb["pt_4pct"]["equity_curve_monthly"])
      <= len(pb["baseline_4w"]["equity_curve_monthly"]))
check("the portfolio respects the concurrent cap",
      pb["baseline_4w"]["concurrent_cap"] == MAX_CONCURRENT)
ps = portfolio_sim(data, None)
check("portfolio_sim runs standalone on the data dir",
      ps.get("status") == "OK" and ps.get("n_trades", 0) > 0
      and ps.get("equity_curve_monthly"))
res_f = res / "exit_battery.json"
res_f.write_text(json.dumps(r, indent=2))
check("the JSON artifact serializes",
      json.loads(res_f.read_text())["status"] == "OK")

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
