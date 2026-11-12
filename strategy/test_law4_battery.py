"""Law-4 battery suite: effort vs result at the crash-zone
entry, measured against KNOWN ground truth - a synthetic
universe where high-effort crashes bounce and low-effort
crashes do not must be read as a gate, and one where effort
is irrelevant must be read as no gate. Harness file."""
import datetime as _dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from law4_battery import run_law4

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def _write_series(path, rets, vols, d0=(2015, 1, 1)):
    prices = 100.0 * np.exp(np.cumsum(rets))
    d0 = _dt.date(*d0)
    rows = []
    for i, p in enumerate(prices):
        d = (d0 + _dt.timedelta(days=i)).isoformat()
        rows.append((d, round(float(p), 4),
                     round(float(p) * 1.002, 4),
                     round(float(p) * 0.998, 4),
                     round(float(p), 4),
                     round(float(vols[i]), 2)))
    write_csv(path, rows)


def _crash_universe(n=9000, seed=5, period=130):
    """Periodic crash weeks; the bounce after each crash is
    set per-cell by the caller. Volume at the crash bar
    alternates high/low so the effort split is forced."""
    rng = np.random.default_rng(seed)
    rets = 0.0002 * rng.standard_normal(n)
    vols = np.full(n, 1_000_000.0)
    for k, j in enumerate(range(300, n - 60, period)):
        rets[j + 3:j + 5] = -0.03625          # the crash week
        rets[j + 5:j + 25] = 0.0035           # the bounce
        vols[j + 4] = (4_000_000.0 if k % 2 == 0
                       else 400_000.0)        # effort alternates
    return rets, vols


def _bounce_by_effort(rets, vols, high, low, period=130):
    """Rewrite the bounce depth per effort cell."""
    rets = rets.copy()
    k = 0
    for j in range(300, len(rets) - 60, period):
        eff = vols[j + 4] > 1_000_000.0
        rets[j + 5:j + 25] = (high if eff else low) / 20
        k += 1
    return rets


tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir(parents=True)

# --- ground truth 1: effort GATES the bounce --------------------
r1, v1 = _crash_universe()
r1 = _bounce_by_effort(r1, v1, high=0.05, low=0.0)
_write_series(data / "SIF.csv", r1, v1)
res1 = run_law4(data)
check("a universe where only high-effort crashes bounce "
      "reads as gated",
      "GATES THE ENTRY" in res1["verdict"]
      and res1["high_effort"]["median_net"]
      > res1["low_effort"].get("median_net", 0))

# --- ground truth 2: effort is irrelevant ------------------------
r2, v2 = _crash_universe()
r2 = _bounce_by_effort(r2, v2, high=0.035, low=0.035)
_write_series(data / "SIF.csv", r2, v2)
res2 = run_law4(data)
check("a universe where effort is irrelevant reads as a "
      "tilt or no-gate, never gated",
      "GATES THE ENTRY" not in res2["verdict"])
check("the battery reports every cell with breakdowns",
      all("per_asset" in res2[k]
          for k in ("pooled", "high_effort", "low_effort")
          if "median_net" in res2[k]))
check("the effort quantiles are carried",
      "effort_ratio_quantiles" in res2
      and res2["effort_ratio_quantiles"]["q33"] > 0)
res_f = tmp / "research"
res_f.mkdir()
(res_f / "law4_battery.json").write_text(json.dumps(res2))
check("the JSON artifact serializes",
      json.loads((res_f / "law4_battery.json")
                 .read_text())["status"] == "OK")

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
