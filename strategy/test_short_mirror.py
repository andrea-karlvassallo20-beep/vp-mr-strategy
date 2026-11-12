"""Short mirror suite: the euphoria-zone short measured
against KNOWN ground truth - a universe where euphoria
reverses must read as a short edge, and the drift-up universe
(the real markets' shape) must read the mirror as negative.
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
from short_mirror import (EUPH_HI, EUPH_LO, NUC_HI, run_short_mirror)

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


def _euphoria_universe(n=9000, seed=3, period=130,
                       fade=0.0):
    """Periodic euphoria weeks (the +5..10% cross) followed
    by a fade whose depth the caller sets: fade > 0 means the
    move reverses (a short edge exists); fade = 0 means it
    drifts on (no short edge)."""
    rng = np.random.default_rng(seed)
    rets = 0.0002 * rng.standard_normal(n)
    for j in range(300, n - 60, period):
        rets[j + 3:j + 5] = 0.03625          # the euphoria week
        rets[j + 5:j + 25] = -fade / 20      # the fade
    return rets


tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir(parents=True)

# --- ground truth 1: euphoria REVERSES -> the short earns ------
r1 = _euphoria_universe(fade=0.06)
_write_series(data / "SIF.csv", r1)
res1 = run_short_mirror(data)
check("a universe where euphoria reverses reads as a short "
      "edge",
      "MEASURED SHORT EDGE EXISTS" in res1["verdict"]
      and res1["moderate_euphoria_short"]["median_net"] > 0)

# --- ground truth 2: euphoria drifts on -> the mirror is dead ---
r2 = _euphoria_universe(fade=0.0)
_write_series(data / "SIF.csv", r2)
res2 = run_short_mirror(data)
check("a drifting universe reads the mirror as negative",
      "MIRROR IS NEGATIVE" in res2["verdict"]
      and res2["moderate_euphoria_short"]["median_net"] <= 0)
check("the cells carry the mandatory per-asset breakdown",
      "per_asset" in res2["moderate_euphoria_short"]
      and res2["moderate_euphoria_short"]["per_asset"])
check("the seductive nuclear cell is flagged, never hidden",
      ("seductive cell is flagged" in res2["verdict"])
      == bool(res2["nuclear_euphoria_short"].get(
          "dual_split_gate")))
res_f = tmp / "research"
res_f.mkdir()
(res_f / "short_mirror.json").write_text(json.dumps(res2))
check("the JSON artifact serializes",
      json.loads((res_f / "short_mirror.json")
                 .read_text())["status"] == "OK")
check("the zones are the mirror of the measured best-buy",
      (EUPH_LO, EUPH_HI, NUC_HI)
      == (0.05, 0.10, 0.15))

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
