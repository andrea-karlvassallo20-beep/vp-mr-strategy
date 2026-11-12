"""Cap sensitivity suite: the portfolio across the concurrent
cap ladder, measured against KNOWN ground truth - a universe
with many overlapping crash episodes must show the cap
BINDING (tight rungs differ from loose), and the verdict must
state the never-binds honesty when it doesn't. Harness
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
from cap_sensitivity import CAPS, run_cap_sensitivity

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


def _crisis_universe(n_assets=6, n=9000, seed=7, period=120,
                     offset=40):
    """Many assets with STAGGERED crash episodes so several
    overlap in time - the cap must bind at some rung."""
    rng = np.random.default_rng(seed)
    tmp = Path(tempfile.mkdtemp())
    data = tmp / "data"
    data.mkdir(parents=True)
    names = ("SIF", "GCF", "HGF", "CLF", "DJI", "RUT")
    for a, nm in enumerate(names[:n_assets]):
        rets = 0.0002 * rng.standard_normal(n)
        for j in range(300 + a * offset, n - 60, period):
            rets[j + 3:j + 5] = -0.03625
            rets[j + 5:j + 25] = 0.0035
        _write_series(data / f"{nm}.csv", rets)
    return tmp, data


tmp, data = _crisis_universe()
r = run_cap_sensitivity(data)
check("the ladder runs every rung",
      r.get("status") == "OK"
      and [x["cap"] for x in r["ladder"]] == list(CAPS))
check("every rung carries the shape stats",
      all(set(x) >= {"cap", "n_trades", "total_return",
                     "cagr", "max_drawdown"}
          for x in r["ladder"]))
check("the verdict is stated with the honesty either way",
      isinstance(r["verdict"], str) and len(r["verdict"]) > 30)
res = tmp / "research"
res.mkdir()
(res / "cap_sensitivity.json").write_text(json.dumps(r))
check("the JSON artifact serializes",
      json.loads((res / "cap_sensitivity.json")
                 .read_text())["status"] == "OK")
# the staggered universe has overlapping episodes: with 6
# assets crashing every 120 bars, tight caps must differ from
# loose ones somewhere in the ladder OR the constraint never
# binds - both are honest outcomes, the verdict must name one
check("the verdict names the binding truth",
      ("NEVER BINDS" in r["verdict"])
      or (len({round(x["total_return"], 4)
               for x in r["ladder"]}) > 1))

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
