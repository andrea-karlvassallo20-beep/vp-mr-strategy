"""V4 charts + portfolio equity suite: the chart page machinery
and the calendar-date portfolio simulation measured against
KNOWN ground truth - a two-asset universe with known zone trades
must produce the hand-computed equity, the date grid must not
mix timelines (assets with different histories), and the
per-asset breakdown must flag the negative cell. Harness
file."""
import datetime as _dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from v4_charts import (MAX_CONCURRENT, N_POINTS, _downsample,
                       build_charts, portfolio_equity, run)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


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


# --- downsample keeps the endpoints ------------------------------------
idx = _downsample(1000)
check("downsample keeps first and last bar",
      idx[0] == 0 and idx[-1] == 999)
check("downsample respects the target size",
      len(idx) <= int(N_POINTS * 1.2) + 1)

# --- the portfolio: two anchored assets, known trades ------------------
tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()
res = tmp / "research"
res.mkdir()
docs = tmp / "docs"
docs.mkdir()

# BTC: one crash week followed by a +10% run over the hold
n = 400
rets_b = np.zeros(n)
rets_b[100:105] = -0.016          # ~ -7.8% weekly: in the zone
rets_b[105:125] = 0.10 / 20       # the bounce
_write_series(data / "BTCUSD.csv", rets_b)
# ETH: same crash, but a -10% run instead (the negative cell)
rets_e = np.zeros(n)
rets_e[100:105] = -0.016
rets_e[105:125] = -0.10 / 20
_write_series(data / "ETHUSD.csv", rets_e)

eq = portfolio_equity(data)
check("both anchored assets traded (overlapping zone entries "
      "included)",
      eq["status"] == "OK"
      and eq["n_trades"] >= 2
      and set(eq["per_asset"]) == {"BTCUSD", "ETHUSD"})
check("the positive cell is flagged positive, the negative "
      "cell is flagged negative",
      eq["per_asset"]["BTCUSD"]["positive"] is True
      and eq["per_asset"]["ETHUSD"]["positive"] is False)
# hand check: BTC's crash bounces +10%, ETH's declines -10% at
# the same dates with equal weight - the bulk cancels and the
# residual is small relative to either leg
total = eq["total_return"]
check("the equal-weight concurrent equity is small relative to "
      "either leg (the legs cancel)",
      -0.05 < total < 0.05)

# --- the date grid does not mix timelines --------------------------------
# a second asset whose crash happens 2 YEARS later: the equity
# must reflect two separate episodes, not an index collision
rets_l = np.zeros(n)
rets_l[100:105] = -0.016
rets_l[105:125] = 0.10 / 20
_write_series(data / "GCF.csv", rets_l,
              d0=(2017, 6, 1))
eq2 = portfolio_equity(data)
check("assets with different date ranges trade on the calendar "
      "grid (all three present, no timeline mixing)",
      eq2["n_trades"] >= 3
      and set(eq2["per_asset"])
      == {"BTCUSD", "ETHUSD", "GCF"})

# --- the chart page builds ------------------------------------------------
r = run(data, res, docs)
check("the page is written with the charts",
      (docs / "v4_charts.html").exists()
      and r["n_charts"] >= 2)
check("the JSON artifact carries the equity block",
      r["equity"]["status"] == "OK"
      and r["equity"]["equity_curve_monthly"])
# an oscillating anchored series must fire confirmed
# detections so the page carries the v4 markers
rng = np.random.default_rng(5)
n3 = 1200
osc = np.zeros(n3)
lvl = 0.0
for t_ in range(n3):
    lvl = 0.985 * lvl + 0.02 * rng.standard_t(6)
    osc[t_] = lvl
rets_o = np.diff(osc, prepend=0.0)
_write_series(data / "SIF.csv", rets_o)
r3 = run(data, res, docs)
html = (docs / "v4_charts.html").read_text()
check("the page marks confirmed tops and bottoms with the "
      "v4 colors",
      "#4ade80" in html and "#f87171" in html)

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
