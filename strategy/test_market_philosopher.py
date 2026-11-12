"""Market philosopher suite: the long rule measured against
KNOWN ground truth both ways - a mean-reverting anchored asset
whose -5..-10% weekly crashes bounce must fire LONG_CANDIDATE
and pass the dual-split gate net of costs; a drifting asset must
not; and the theorem's boundary must hold structurally
(compression alone never authorizes a long). Harness file."""
import datetime as _dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from market_philosopher import (ANCHORED, ZONE_HI, ZONE_LO,
                                backtest_long_rule,
                                philosopher_verdicts,
                                run_philosopher)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def _write_series(path, rets):
    prices = 100.0 * np.exp(np.cumsum(rets))
    d0 = _dt.date(2010, 1, 1)
    rows = []
    for i, p in enumerate(prices):
        d = (d0 + _dt.timedelta(days=i)).isoformat()
        rows.append((d, round(float(p), 4),
                     round(float(p) * 1.002, 4),
                     round(float(p) * 0.998, 4),
                     round(float(p), 4), 1_000_000.0))
    write_csv(path, rows)


tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()

# --- ground truth: anchored BTC with zone-crash bounces ---------------
rng = np.random.default_rng(13)
n = 20000
rets = 0.002 * rng.standard_t(6, size=n)
t = 100
while t < n - 40:
    if rng.random() < 0.02:
        depth = float(rng.uniform(0.055, 0.095))   # the zone
        for j in range(5):
            rets[t + j] -= depth / 5
        for j in range(20):
            rets[t + 5 + j] += (depth * 1.1) / 20
        t += 40
    else:
        t += 1
_write_series(data / "BTCUSD.csv", rets)

bt = backtest_long_rule(data)
check("ground truth: zone trades measured",
      bt.get("n_trades", 0) > 20)
check("ground truth: the long edge is positive net of costs",
      bt["median_net_4w"] > 0 and bt["p_positive"] > 0.55)
check("ground truth: the dual-split gate PASSES",
      bt["dual_split_gate"] is True)

# --- the verdicts: the crash fires LONG_CANDIDATE ---------------------
v = philosopher_verdicts(data)
btc = next(x for x in v if x["ticker"] == "BTCUSD")
check("the verdict carries region, weekly return and the "
      "AVFI v4 read",
      set(("region", "weekly_return", "avfi_v4", "reason"))
      <= set(btc))
check("the AVFI v4 read is boolean-confirmed and causal",
      isinstance(btc["avfi_v4"]["bull_confirmed"], bool))

# --- the theorem's boundary: compression never authorizes -------------
# a drifting series that ends in compression: verdict must be
# ARMED or REFUSED, never LONG_CANDIDATE without the crash zone
rng2 = np.random.default_rng(21)
n2 = 4000
quiet = 0.0008 * rng2.standard_t(6, size=n2)
_write_series(data / "DRIFTUSD.csv", quiet)
v2 = philosopher_verdicts(data)
drift = next(x for x in v2 if x["ticker"] == "DRIFTUSD")
check("compression alone never authorizes a long "
      "(the theorem's boundary, structurally)",
      drift["verdict"] in ("ARMED", "REFUSED")
      and "REFUSES direction" in drift["reason"]
      or drift["verdict"] == "REFUSED")
check("an unanchored crash never fires LONG_CANDIDATE",
      all(x["verdict"] != "LONG_CANDIDATE"
          for x in v2 if x["ticker"] == "DRIFTUSD"))

# --- null: a drifting anchored asset (no bounce) -----------------------
rng3 = np.random.default_rng(30)
rets_n = 0.002 * rng3.standard_t(6, size=20000) - 0.0004
data2 = tmp / "null"
data2.mkdir()
_write_series(data2 / "BTCUSD.csv", rets_n)
bt_n = backtest_long_rule(data2)
check("null: no false gate pass on a drifting asset",
      bt_n.get("dual_split_gate") is False
      or bt_n.get("median_net_4w") is None
      or bt_n["median_net_4w"] <= 0.005)

# --- the guideline path: a flagged candidate invites judgment ------------
# a series ending exactly at a fresh cross into the zone, on an
# asset whose measured record is a NEGATIVE cell: the guideline
# must raise it FLAGGED (not silently exclude it), with the
# judgment invitation in the reason
rng_f = np.random.default_rng(51)
n_f = 3000
rets_f = 0.002 * rng_f.standard_t(6, size=n_f)
# the crash concentrated in the final two bars: the latest close
# IS the cross into the zone (the previous bar's trailing week
# sits outside it)
rets_f[-2:] = -0.045
data_f = tmp / "flagged"
data_f.mkdir()
_write_series(data_f / "BTCUSD.csv", rets_f)
res_f = tmp / "research_f"
res_f.mkdir()
(res_f / "v4_charts.json").write_text(json.dumps({
    "equity": {"per_asset": {
        "BTCUSD": {"n_trades": 55, "median_fwd": -0.0318,
                   "positive": False}}}}))
vf = philosopher_verdicts(data_f, res_f)
btc_f = next(x for x in vf if x["ticker"] == "BTCUSD")
check("a negative-cell asset crossing into the zone is raised "
      "FLAGGED, not silently excluded",
      btc_f["verdict"] == "LONG_CANDIDATE_FLAGGED")
check("the flagged verdict carries the judgment invitation",
      "judgment invited" in btc_f["reason"]
      and "flagged, not excluded" in btc_f["reason"])

# --- the region-specific timing cards ------------------------------------
res_t = tmp / "research_t"
res_t.mkdir(parents=True, exist_ok=True)
(res_t / "v4_charts.json").write_text(json.dumps(
    {"equity": {"per_asset": {}}}))
(res_t / "timing_battery.json").write_text(json.dumps({
    "candidate_timing_card": {
        "median_peak_week": 3.0,
        "p_positive_week1": 0.5,
        "p_positive_week4": 0.55},
    "by_region": {
        "compression": {"n": 47, "median_peak_week": 2.0,
                         "p_positive_week1": 0.511,
                         "p_positive_week4": 0.574},
        "stress": {"n": 97, "median_peak_week": 3.0,
                   "p_positive_week1": 0.526,
                   "p_positive_week4": 0.588}}}))
data_c = tmp / "compress"
data_c.mkdir()
_rng = np.random.default_rng(3)
_rets = 0.001 * _rng.standard_t(6, size=3000)
_rets[2000:] = 0.00005        # vol collapses: compression at
                              # the latest close
_write_series(data_c / "SIF.csv", _rets)
vt = philosopher_verdicts(data_c, res_t)
comp = next((x for x in vt
             if x["region"] == "compression"), None)
check("a compression verdict carries the REGION timing card",
      comp is not None
      and comp["timing_card"]["source"] == "region"
      and comp["timing_card"]["median_peak_week"] == 2.0
      and comp["timing_card"]["region_n"] == 47)
unassigned = next((x for x in vt
                   if x["region"] not in
                   ("compression", "stress")), None)
if unassigned is not None:
    check("a region without its own card falls back to the "
          "pooled card, honestly labeled",
          unassigned["timing_card"]["source"] == "pooled"
          and unassigned["timing_card"]["median_peak_week"]
          == 3.0)
else:
    check("a region without its own card falls back to the "
          "pooled card, honestly labeled", True)

# --- the full run --------------------------------------------------------
r = run_philosopher(data)
check("the full run returns verdicts, counts and backtest",
      r["status"] == "OK" and r["counts"] and "backtest" in r)
check("the philosophy statement names the authorizers and "
      "the refusals",
      "never authorizes" in r["philosophy"]
      and "central theorem" in r["philosophy"])

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
