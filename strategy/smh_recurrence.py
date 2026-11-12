"""THE SMH RECURRENCE BATTERY (charter v3, section 14, the
long-run lemma): the region chain measured, and the trigger's
actuarial inevitability quantified.

The lemma's claim: the measured region chain is irreducible - all
six directed links between compression, mid and stress observed,
none absorbing - so the compression trigger recurs indefinitely,
and the anticipated event is actuarially inevitable across the
cycle, exactly as a life table makes death inevitable and no death
dated. This battery measures the three quantities the lemma needs:

  THE TRANSITION MATRIX: pooled counts and probabilities for every
  directed region link (the dwell/transition machine's jump
  structure, at this programme's own grain).
  IRREDUCIBILITY: all six directed links observed, no absorbing
  state (a state that, once entered, is never left) - the verdict
  is mechanical, not narrative.
  RECURRENCE: how often the compression trigger fires per market
  per year - the actuarial rate at which the entry condition
  returns, hence the rate at which forward rows accumulate.

Usage (nightly, after smh_direction):
    python3 smh_recurrence.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from smh_gradient import _tercile_states
from smh_proof import WARMUP, _series, _weekly_sigma

REGIONS = (0, 1, 2)
NAMES = {0: "compression", 1: "mid", 2: "stress"}
BARS_PER_YEAR = 252


def run_recurrence(data_dir: Path) -> dict:
    links = {(a, b): 0 for a in REGIONS for b in REGIONS}
    exits = {0: 0, 1: 0, 2: 0}
    n_triggers = 0
    n_market_years = 0.0
    for name, c, v in _series(data_dir):
        sig = _weekly_sigma(np.log(c))
        states = _tercile_states(sig)
        years = len(c) / BARS_PER_YEAR
        n_market_years += years
        prev = None
        for t in range(WARMUP, len(states)):
            s = states[t]
            if s < 0:
                prev = None
                continue
            if prev is not None and s != prev:
                links[(prev, s)] += 1
                exits[prev] += 1
                if s == 0:
                    n_triggers += 1
            prev = s
    trans = {}
    for (a, b), n in links.items():
        trans[f"{NAMES[a]}->{NAMES[b]}"] = {
            "count": int(n),
            "probability": (round(n / exits[a], 3)
                            if exits[a] else None),
        }
    all_links = all(links[(a, b)] > 0
                    for a in REGIONS for b in REGIONS if a != b)
    observed_in = {NAMES[r]: sum(
        links[(a, r)] for a in REGIONS if a != r) for r in REGIONS}
    absorbing = [NAMES[r] for r in REGIONS
                 if exits[r] == 0 and observed_in[NAMES[r]] > 0]
    irreducible = bool(all_links and not absorbing)
    return {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "transition_matrix": trans,
        "irreducibility": {
            "all_six_directed_links_observed": bool(all_links),
            "absorbing_states": absorbing,
            "irreducible": irreducible,
            "statement": ("the region chain is irreducible: every "
                          "region is reachable from every other and "
                          "none is absorbing, so the compression "
                          "trigger recurs indefinitely - the "
                          "anticipated event is actuarially "
                          "inevitable across the cycle, and no "
                          "event is dated" if irreducible else
                          "the chain is NOT irreducible on this "
                          "universe - the lemma's precondition "
                          "fails and is reported as measured"),
        },
        "trigger_recurrence": {
            "n_triggers": int(n_triggers),
            "market_years": round(n_market_years, 1),
            "triggers_per_market_year": (round(
                n_triggers / n_market_years, 2)
                if n_market_years else None),
            "statement": ("the compression cross fires at this "
                          "rate per market per year: the entry "
                          "condition is not a rare event but a "
                          "recurring feature of the cycle, and "
                          "the forward log accumulates at this "
                          "actuarial rate"),
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="SMH recurrence battery (the long-run lemma)")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_recurrence(args.data_dir)
    dest = args.research_dir / "smh_recurrence.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    ir = r["irreducibility"]
    tr = r["trigger_recurrence"]
    print(f"smh recurrence -> {dest} "
          f"(irreducible {ir['irreducible']}, "
          f"triggers/market-year "
          f"{tr['triggers_per_market_year']})")


if __name__ == "__main__":
    main()
