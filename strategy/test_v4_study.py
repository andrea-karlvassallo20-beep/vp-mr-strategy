"""v4 study suite: causality, confirmation reduces trade count,
structure of the honest verdict, dead-coin exclusion, and ground
truth (synthetic OU series with engineered climax confirmations).
Harness file."""
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from papertrading_runner import load_bars
from v4_study import (causal_z, confirm_sets, run_v4_study,
                      stretch_backtest)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


# --- causality --------------------------------------------------------
rng = np.random.default_rng(7)
c = 100.0 * np.exp(np.cumsum(0.01 * rng.standard_normal(600)))
z = causal_z(c)
z2 = causal_z(np.concatenate([c, [c[-1] * 2.0]]))[:600]
check("causal z untouched by future bars (Gate 1)",
      np.allclose(z, z2, atol=1e-12))

# --- confirmation mechanics -------------------------------------------
h, l, v = c * 1.01, c * 0.99, np.full(600, 1e6)
bull, bear = confirm_sets(h, l, c, v)
check("confirm sets are index sets (causal detector output)",
      isinstance(bull, set) and isinstance(bear, set))
plain, tr_p = stretch_backtest(c, z, bull, bear, False)
v4, tr_v = stretch_backtest(c, z, bull, bear, True)
check("confirmed entries are a subset (fewer or equal trades)",
      tr_v <= tr_p)

# --- ground truth: V-shaped episodes with engineered climax bars ------
# Each episode: a decline into a deep stretch, a textbook VSA
# exhaustion bar (huge volume, wide range, close recovering into
# the upper half) at the bottom, then a recovery. Decline, stretch
# and climax co-occur BY CONSTRUCTION, so confirmation is
# informative by design - if v4 cannot win here, it cannot win.
def v_episodes(seed):
    r = np.random.default_rng(seed)
    n_ep, ep = 24, 40
    p = np.zeros(n_ep * ep)
    vol = np.full(n_ep * ep, 1e6)
    hi = np.zeros(n_ep * ep)
    lo = np.zeros(n_ep * ep)
    lvl = 100.0
    for e in range(n_ep):
        base = e * ep
        for j in range(ep):
            t = base + j
            if j < 28:                      # the decline
                lvl *= (1 - 0.006 + 0.002 * r.standard_normal())
            elif j == 28:                   # the exhaustion bar
                lvl *= (1 - 0.004)
                vol[t] = 5e6
                hi[t] = lvl * 1.03
                lo[t] = lvl * 0.97
                p[t] = lvl
                continue
            else:                            # the recovery
                lvl *= (1 + 0.004 + 0.002 * r.standard_normal())
            p[t] = lvl
            hi[t] = lvl * (1 + abs(0.006 * r.standard_normal()))
            lo[t] = lvl * (1 - abs(0.006 * r.standard_normal()))
    return p, hi, lo, vol


tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()
for i in range(4):
    p, hi, lo, vol = v_episodes(20 + i)
    rows = [(f"2023-{j // 28 % 12 + 1:02d}-{j % 28 + 1:02d}",
             hi[j], hi[j], lo[j], p[j], int(vol[j]))
            for j in range(len(p))]
    write_csv(data / f"eng{i}usd.csv", rows)

r = run_v4_study(data)
check("study structure carries overall, classes, best/worst",
      all(k in r for k in ("overall", "by_class", "best_series",
                           "worst_series", "rows")))
check("engineered confirmations improve the OU series",
      r["overall"]["pooled_premium"] > 0
      and r["overall"]["improves"])
check("every row carries dual-split premium fields",
      all(set(("plain_oos", "v4_oos", "premium_worse_window",
               "plain_trades", "v4_trades")) <= set(x)
          for x in r["rows"]))

# --- dead-coin exclusion -------------------------------------------------
dead = 100.0 * np.exp(
    np.cumsum(0.01 * np.random.default_rng(55).standard_normal(400)))
dead[-1] = dead.max() / 5000.0
rows = [(f"2023-{j // 28 % 12 + 1:02d}-{j % 28 + 1:02d}",
         dead[j] * 1.01, dead[j] * 1.01, dead[j] * 0.99, dead[j],
         1_000_000) for j in range(400)]
write_csv(data / "deadusd.csv", rows)
r2 = run_v4_study(data)
check("dead coin excluded from the study",
      all(x["ticker"] != "DEADUSD" for x in r2["rows"]))

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
