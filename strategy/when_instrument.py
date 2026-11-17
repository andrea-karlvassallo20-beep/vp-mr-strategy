"""THE W1 WHEN-INSTRUMENT ENGINE (governing spec:
paper/research/when_instrument/w1_when_instrument_spec.md).

The WHEN instrument: straddle-logic sized by the posterior on MOVE,
not UP. This module is the pre-registered DECISION, not an exposure:
it converts measured quantities into a position size or a documented
refusal, and it refuses on any input that has not been measured.

Every rule below is pre-declared in the spec (section 4/5) BEFORE any
trigger measurement exists:

  THE REFUSAL RULE (K1): size is ZERO unless the LOWER bound of the
  CPCV hazard-lift distribution exceeds 1.0. A wide or uninformative
  posterior means no position. The engine refuses to size enthusiasm.

  THE NET-OF-COST LINE (K2): the structure's expected value at the
  lift LOWER bound, net of round-trip cost (fee + half-spread), must
  be positive. The harvestable rule: raw edge is never reported alone.

  THE KELLY-FLAVORED CAP: quarter-Kelly (the repo's standing haircut)
  on the binary-approximation edge, using ONLY the lift lower bound
  and the payoff model's measured R-distribution. Point estimates are
  never sized.

  THE CVaR CONSTRAINT: the expected loss in the worst decile of the
  payoff model's simulated outcomes, at the proposed size, must stay
  inside the declared drawdown budget; otherwise the size scales down
  to the budget (and to zero if even the minimum exposure breaches).

  THE INPUT HONESTY RULE: any input marked UNKNOWN (None) is a
  refusal reason. No defaults, no guesses, no invented numbers.

Usage:
    python3 when_instrument.py --demo      # synthetic both-ways check
    python3 when_instrument.py --input decision_input.json
"""
import argparse
import json
import math
import sys
from pathlib import Path

KELLY_FRACTION = 0.25        # the repo's standing haircut, pre-declared
LIFT_LOWER_Q = 0.10           # CPCV lower decile defines the lower bound
CVAR_DECILE = 0.10            # the worst decile of simulated outcomes
REFUSAL_ZERO = 0.0


def _finite_float(value, name, refusals):
    """Coerce one input to a finite float or record a refusal.

    A NaN in a measured distribution is the most dangerous input a
    falsification engine can receive: every comparison against it is
    False, so it silently passes every kill line. Non-finite and
    non-numeric inputs are therefore REFUSALS, never propagated.
    """
    try:
        f = float(value)
    except (TypeError, ValueError):
        refusals.append(f"{name}: non-numeric value {value!r} - refuse")
        return None
    if not math.isfinite(f):
        refusals.append(
            f"{name}: non-finite value (NaN/inf) - the measurement is "
            "unusable and cannot be sized")
        return None
    return f


def _finite_samples(values, name, refusals):
    """Coerce a sample list to finite floats or record a refusal."""
    out = []
    for v in values:
        f = _finite_float(v, name, refusals)
        if f is None:
            return None
        out.append(f)
    return out


def _quantile(sorted_vals, q):
    """Linear-interpolation quantile of an already-sorted sequence."""
    if not sorted_vals:
        raise ValueError("empty sample")
    if len(sorted_vals) == 1:
        return float(sorted_vals[0])
    pos = q * (len(sorted_vals) - 1)
    lo = int(math.floor(pos))
    hi = min(lo + 1, len(sorted_vals) - 1)
    frac = pos - lo
    return float(sorted_vals[lo]) * (1 - frac) + float(sorted_vals[hi]) * frac


def lift_bounds(cpcv_lift_samples):
    """The CPCV lift distribution's lower and upper decile bounds.

    K1 fires when this interval straddles 1.0 (lower bound <= 1.0).
    """
    s = sorted(float(x) for x in cpcv_lift_samples)
    return _quantile(s, LIFT_LOWER_Q), _quantile(s, 1.0 - LIFT_LOWER_Q)


def kelly_fraction(p_win, odds):
    """Full-Kelly fraction for a binary bet at decimal odds (win pays
    `odds` times the risked amount, loss loses the risked amount)."""
    if odds <= 0:
        raise ValueError("odds must be positive")
    p = min(max(p_win, 0.0), 1.0)
    return (p * (odds + 1.0) - 1.0) / odds


def expected_value_r(p_release, payoff_r_samples, cost_r):
    """Expected value of the structure in R-multiples of defined risk.

    p_release: probability of release within H (the sized quantity).
    payoff_r_samples: measured R-multiples conditional on release
    (the payoff model's CPCV/simulated draws; None/empty = UNKNOWN).
    cost_r: round-trip cost (fee + half-spread) in the same R units.
    """
    if not payoff_r_samples:
        raise ValueError("payoff distribution is UNKNOWN - refuse")
    if cost_r is None or cost_r < 0:
        raise ValueError("cost is UNKNOWN - refuse")
    mean_payoff = sum(float(r) for r in payoff_r_samples) / len(payoff_r_samples)
    return p_release * mean_payoff - (1.0 - p_release) * 1.0 - cost_r


def cvar_worst_decile(r_samples):
    """Mean of the worst CVAR_DECILE of the outcome distribution."""
    s = sorted(float(x) for x in r_samples)
    k = max(1, int(math.ceil(CVAR_DECILE * len(s))))
    return sum(s[:k]) / k


def decide(inputs):
    """The W1 decision: size fraction (of risk budget) or documented refusal.

    Required keys in `inputs`:
      cpcv_lift_samples: the trigger's CPCV hazard-lift draws (list).
      baseline_hazard: P(release <= H | primed), measured (float 0..1).
      payoff_r_samples: R-multiples conditional on release, measured.
      cost_r: round-trip cost in R units, measured (float >= 0).
      drawdown_budget: worst-decile loss tolerance as a fraction (float > 0).

    Returns a dict: {"size_fraction": float, "refusals": [...], "echo": {...}}
    A size of exactly 0.0 with a non-empty refusals list is a REFUSAL.
    """
    refusals = []
    raw_lift = inputs.get("cpcv_lift_samples")
    raw_baseline = inputs.get("baseline_hazard")
    raw_payoff = inputs.get("payoff_r_samples")
    raw_cost = inputs.get("cost_r")
    raw_budget = inputs.get("drawdown_budget")

    lift_samples = None
    payoff = None
    baseline = cost_r = budget = None

    if not raw_lift:
        refusals.append("K1: lift CPCV distribution is UNKNOWN")
    else:
        lift_samples = _finite_samples(raw_lift, "lift samples", refusals)
    if raw_baseline is None:
        refusals.append("baseline hazard is UNKNOWN")
    else:
        baseline = _finite_float(raw_baseline, "baseline hazard", refusals)
        if baseline is not None and not (0.0 < baseline < 1.0):
            refusals.append("baseline hazard is out of range (0, 1)")
            baseline = None
    if not raw_payoff:
        refusals.append("K2: payoff R-distribution is UNKNOWN")
    else:
        payoff = _finite_samples(raw_payoff, "payoff samples", refusals)
    if raw_cost is None:
        refusals.append("K2: round-trip cost is UNKNOWN")
    else:
        cost_r = _finite_float(raw_cost, "round-trip cost", refusals)
        if cost_r is not None and cost_r < 0:
            refusals.append("round-trip cost is negative")
            cost_r = None
    if raw_budget is None:
        refusals.append("drawdown budget is not declared")
    else:
        budget = _finite_float(raw_budget, "drawdown budget", refusals)
        if budget is not None and budget <= 0:
            refusals.append("drawdown budget must be positive")
            budget = None

    lift_lb = lift_ub = None
    if lift_samples:
        lift_lb, lift_ub = lift_bounds(lift_samples)
        if lift_lb <= 1.0:
            refusals.append(
                f"K1: lift CPCV lower bound {lift_lb:.4f} <= 1.0 "
                "(no measurable WHEN; the posterior straddles the baseline)")

    if refusals:
        return {"size_fraction": REFUSAL_ZERO, "refusals": refusals,
                "echo": {"lift_lower_bound": lift_lb,
                         "lift_upper_bound": lift_ub}}

    p_release = min(baseline * lift_lb, 1.0)

    try:
        ev_lb = expected_value_r(p_release, payoff, cost_r)
    except ValueError as exc:
        refusals.append(str(exc))
        return {"size_fraction": REFUSAL_ZERO, "refusals": refusals,
                "echo": {"lift_lower_bound": lift_lb}}
    if ev_lb <= 0.0:
        refusals.append(
            f"K2: net-of-cost expected value at the lift lower bound "
            f"is {ev_lb:.4f} R <= 0 (unharvestable at the prevailing book)")
        return {"size_fraction": REFUSAL_ZERO, "refusals": refusals,
                "echo": {"lift_lower_bound": lift_lb, "ev_lower_r": ev_lb}}

    mean_payoff = sum(float(r) for r in payoff) / len(payoff)
    odds = mean_payoff
    f_kelly = kelly_fraction(p_release, odds)
    if f_kelly <= 0.0:
        refusals.append(
            f"Kelly edge non-positive at the conservative inputs "
            f"(p={p_release:.4f}, odds={odds:.4f})")
        return {"size_fraction": REFUSAL_ZERO, "refusals": refusals,
                "echo": {"lift_lower_bound": lift_lb, "ev_lower_r": ev_lb}}
    size = KELLY_FRACTION * f_kelly

    outcomes = [p_release * r - (1.0 - p_release) * 1.0 - cost_r
                for r in payoff]
    worst = cvar_worst_decile(outcomes)
    if worst < 0:
        max_size = budget / (-worst)
        if max_size <= 0:
            refusals.append("CVaR constraint cannot be satisfied")
            return {"size_fraction": REFUSAL_ZERO, "refusals": refusals,
                    "echo": {"lift_lower_bound": lift_lb}}
        size = min(size, max_size)

    return {"size_fraction": round(size, 6), "refusals": [],
            "echo": {"lift_lower_bound": round(lift_lb, 6),
                     "lift_upper_bound": round(lift_ub, 6),
                     "p_release_sized": round(p_release, 6),
                     "ev_lower_r": round(ev_lb, 6),
                     "quarter_kelly_uncapped": round(
                         KELLY_FRACTION * f_kelly, 6),
                     "cvar_worst_decile_r": round(worst, 6)}}


def _demo():
    """Synthetic both-ways demonstration: separated posterior sizes,
    wide posterior refuses, UNKNOWN input refuses. No real data."""
    separated = {
        "cpcv_lift_samples": [1.9, 2.1, 2.4, 2.6, 3.0, 3.3, 3.8, 4.2, 4.7, 5.1],
        "baseline_hazard": 0.15,
        "payoff_r_samples": [0.0, 0.5, 1.2, 2.0, 3.5, 5.0, 8.0],
        "cost_r": 0.05,
        "drawdown_budget": 0.02,
    }
    wide = dict(separated)
    wide["cpcv_lift_samples"] = [0.6, 0.8, 1.0, 1.2, 1.5, 1.9, 2.4, 3.1]
    unknown = dict(separated)
    unknown["baseline_hazard"] = None
    print(json.dumps({
        "demo_note": "SYNTHETIC inputs only; no W1 quantity is measured",
        "separated_posterior": decide(separated),
        "wide_posterior": decide(wide),
        "unknown_input": decide(unknown),
    }, indent=2))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--demo", action="store_true",
                    help="run the synthetic both-ways demonstration")
    ap.add_argument("--input", type=str,
                    help="path to a decision-input JSON file")
    args = ap.parse_args(argv)
    if args.demo:
        _demo()
        return 0
    if args.input:
        with open(args.input) as fh:
            print(json.dumps(decide(json.load(fh)), indent=2))
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
