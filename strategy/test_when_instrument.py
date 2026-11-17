"""W1 WHEN-instrument engine suite: the decision measured against
KNOWN ground truth both ways - a separated lift posterior must produce
a positive, capped, CVaR-bounded size; a wide posterior must refuse
(K1); an UNKNOWN input must refuse (the input honesty rule); a
positive lift with negative net-of-cost expectancy must refuse (K2);
and the Kelly cap must be exactly the quarter haircut. Harness file,
pytest-compatible."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from when_instrument import (CVAR_DECILE, KELLY_FRACTION, cvar_worst_decile,
                             decide, expected_value_r, kelly_fraction,
                             lift_bounds)

PASS = FAIL = 0


def check(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}")


# --- the quantile bounds, hand-computed -------------------------------
lifts = [1.9, 2.1, 2.4, 2.6, 3.0, 3.3, 3.8, 4.2, 4.7, 5.1]
lb, ub = lift_bounds(lifts)
check("lift lower decile hand-checked (10 samples, q=0.1 -> index 0.9)",
      abs(lb - (1.9 * 0.1 + 2.1 * 0.9)) < 1e-12)
check("lift upper decile hand-checked",
      abs(ub - (4.7 * 0.9 + 5.1 * 0.1)) < 1e-12)

# --- K1: a wide posterior that straddles 1.0 must refuse ---------------
wide = {
    "cpcv_lift_samples": [0.6, 0.8, 1.0, 1.2, 1.5, 1.9, 2.4, 3.1],
    "baseline_hazard": 0.15,
    "payoff_r_samples": [0.0, 0.5, 1.2, 2.0, 3.5, 5.0, 8.0],
    "cost_r": 0.05,
    "drawdown_budget": 0.02,
}
r = decide(wide)
check("K1 refusal: wide posterior -> size 0", r["size_fraction"] == 0.0)
check("K1 refusal names the kill line",
      any(x.startswith("K1:") for x in r["refusals"]))

# --- the input honesty rule: any UNKNOWN input refuses -----------------
for missing in ("baseline_hazard", "payoff_r_samples", "cost_r",
                "drawdown_budget"):
    poisoned = dict(wide)
    poisoned["cpcv_lift_samples"] = lifts
    poisoned[missing] = None
    r = decide(poisoned)
    check(f"UNKNOWN {missing} -> refusal",
          r["size_fraction"] == 0.0 and len(r["refusals"]) >= 1)
empty = dict(wide)
empty["cpcv_lift_samples"] = []
r = decide(empty)
check("missing lift distribution -> K1 refusal", r["size_fraction"] == 0.0)

# --- K2: positive lift but unharvestable cost must refuse --------------
costly = dict(wide)
costly["cpcv_lift_samples"] = lifts
costly["cost_r"] = 5.0
r = decide(costly)
check("K2 refusal: net-of-cost EV <= 0 at the lift lower bound",
      r["size_fraction"] == 0.0
      and any(x.startswith("K2:") for x in r["refusals"]))

# --- the separated posterior sizes, and the math is hand-checked -------
good = dict(wide)
good["cpcv_lift_samples"] = lifts
r = decide(good)
check("separated posterior -> positive size", r["size_fraction"] > 0.0)
check("separated posterior -> no refusals", r["refusals"] == [])
p = min(0.15 * lb, 1.0)
mean_payoff = (0.0 + 0.5 + 1.2 + 2.0 + 3.5 + 5.0 + 8.0) / 7.0
f_full = (p * (mean_payoff + 1.0) - 1.0) / mean_payoff
check("quarter-Kelly hand-checked",
      abs(r["echo"]["quarter_kelly_uncapped"]
          - KELLY_FRACTION * f_full) < 1e-6)
check("EV at the lift lower bound hand-checked",
      abs(r["echo"]["ev_lower_r"]
          - (p * mean_payoff - (1 - p) - 0.05)) < 1e-6)

# --- the CVaR constraint binds: a tiny budget shrinks the size ----------
tight = dict(good)
tight["drawdown_budget"] = 1e-6
r_tight = decide(tight)
check("CVaR constraint caps the size under a tiny budget",
      0.0 < r_tight["size_fraction"] <= r["size_fraction"])

# --- the Kelly formula, ground truth both ways --------------------------
check("Kelly: fair coin at even odds -> zero edge",
      abs(kelly_fraction(0.5, 1.0)) < 1e-12)
check("Kelly: p=0.6, odds=1 -> 0.2",
      abs(kelly_fraction(0.6, 1.0) - 0.2) < 1e-12)
check("Kelly: a sucker bet is negative",
      kelly_fraction(0.3, 1.0) < 0.0)

# --- the CVaR helper, hand-computed -------------------------------------
vals = [-4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
check("CVaR worst decile hand-checked (10 samples)",
      abs(cvar_worst_decile(vals) - (-4.0)) < 1e-12)
check("CVaR decile is the pre-declared 0.10", CVAR_DECILE == 0.10)

# --- EV refuses on UNKNOWN payoff ---------------------------------------
try:
    expected_value_r(0.1, [], 0.05)
    check("EV on UNKNOWN payoff raises", False)
except ValueError:
    check("EV on UNKNOWN payoff raises", True)

print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
