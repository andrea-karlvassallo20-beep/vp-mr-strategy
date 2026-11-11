"""Knowledge-grounded variant tests: trailing-only estimation (G1),
determinism, VSA filter behavior. Harness file."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import numpy as np

from vp_mr_strategy import StrategyParameters
from vol_models import (VariantStrategy, ewma_vol_ann, garch_vol_ann,
                         EWMA_LAMBDA, GARCH_ALPHA, GARCH_BETA,
                         VOLUME_LOOKBACK)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


# --- pure vol estimators ---
rng = np.random.default_rng(1)
closes = 450 + np.cumsum(rng.normal(0, 1.2, 300))
v_ewma = ewma_vol_ann(closes, 252)
v_garch = garch_vol_ann(closes, 252)
v_real = float(np.diff(np.log(closes)).std(ddof=1) * np.sqrt(252))
check("EWMA vol positive and sane", 0 < v_ewma < 1)
check("GARCH vol positive and sane", 0 < v_garch < 1)
check("EWMA deterministic", ewma_vol_ann(closes, 252) == v_ewma)
check("GARCH deterministic", garch_vol_ann(closes, 252) == v_garch)
check("short input returns None (warm-up guard)",
      ewma_vol_ann(closes[:10], 252) is None)
check("GARCH persistence condition (Levy)",
      GARCH_ALPHA + GARCH_BETA < 1)
check("EWMA lambda is the RiskMetrics value", EWMA_LAMBDA == 0.97)

# volatility clustering: EWMA should exceed realized after a vol burst
calm = 450 + np.cumsum(rng.normal(0, 0.5, 100))
burst = np.concatenate([calm, calm[-1] + np.cumsum(rng.normal(0, 4.0, 20))])
check("EWMA reacts to vol clustering (Levy stylized fact)",
      ewma_vol_ann(burst, 252) > ewma_vol_ann(calm, 252))

# --- variant strategy: trailing-only (G1 future-perturbation) ---
def run_variant(vol_model, volume_filter, prices, volumes=None, mutate_from=None):
    p = StrategyParameters(min_history_bars=60, lookback_zscore=40,
                           vol_est_lookback=30)
    s = VariantStrategy(p, ["SPY"], 1_000_000.0, vol_model=vol_model,
                        volume_filter=volume_filter)
    s.deploy()
    sigs = []
    for t in range(len(prices)):
        c = float(prices[t])
        v = float(volumes[t]) if volumes is not None else 1e6
        s.on_bar_close("SPY", t, c, c * 1.002, c * 0.998, c, v)
        sigs.append(s.decision_log[-1]["signal"])
    return s, sigs

prices = 450 + np.cumsum(rng.normal(0, 1.2, 200))
s1, sigs1 = run_variant("garch", True, prices)
s2, sigs2 = run_variant("garch", True, prices)
check("variant deterministic", sigs1 == sigs2)
check("variant warms up and decides", len(s1.decision_log) == 200)

prices_mut = prices.copy()
prices_mut[150:] += rng.normal(50, 10, 50)
s3, sigs3 = run_variant("garch", True, prices_mut)
check("G1: future mutation cannot change past decisions",
      sigs1[:150] == sigs3[:150])

# --- VSA filter: weak-volume stretch allowed, high-volume stretch blocked ---
base = np.full(200, 1e6)
stretch_prices = prices.copy()
stretch_prices[120:140] = stretch_prices[120] - np.arange(20) * 2.0  # sell-off
# high-volume sell-off: filter should block entries
_, sigs_high = run_variant("realized", True, stretch_prices,
                           volumes=base * 5)
# low-volume sell-off: filter should allow entries
_, sigs_low = run_variant("realized", True, stretch_prices,
                          volumes=base * 0.2)
_, sigs_nofilter = run_variant("realized", False, stretch_prices,
                               volumes=base * 5)
check("VSA filter blocks some high-volume entries",
      sum(1 for x in sigs_high if x != 0) <
      sum(1 for x in sigs_nofilter if x != 0))
check("VSA filter admits weak-volume entries",
      sum(1 for x in sigs_low if x != 0) >=
      sum(1 for x in sigs_high if x != 0))

print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
