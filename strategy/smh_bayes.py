"""THE SMH BAYESIAN FORECASTER (charter v3, open problem 5, the
formal completion): human prior times measured calibration.

The charter's form: "human prior times measured calibration: the
formal version of integrating your judgment (the judgment log)
into the hazard model once it has a score." The judgment log
exists; this module is the integration, with every parameter
PRE-DECLARED so nothing is fitted to flatter:

  THE BLEND (pre-declared): for every open forward row that
  carries a judgment, the blended forecast is a logit-space
  weighted average of the model's p and the human's p:

      logit(p_blend) = w * logit(p_human) + (1 - w) * logit(p_model)

  THE WEIGHT (pre-declared, earned by score): the human's weight
  is zero until the calibration record holds at least
  MIN_SCORED scored judgments; beyond that,

      w = clip((B_model - B_human) / B_model, 0, 0.5)

  - the human earns weight only by BEATING the model's Brier,
    at most half the blend, never more. A human who is noise
    gets zero weight; a human who is worse than the model gets
    zero; the shrinkage protects the record while it is young.

  THE SCORED TRACK: the blend is a SEPARATE scored track - the
  forward row's official forecast stays the model's (doctrine
  rule 2: the logged row is never revised). When the row
  resolves, all three Briers land on the record: model, human,
  blend. That three-way scoreboard is the Bayesian forecaster's
  whole existence.

Usage (nightly, after the judgment pass):
    python3 smh_bayes.py --research-dir ../paper/research
"""
import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))

MIN_SCORED = 20          # the human's record earns weight only now
W_CAP = 0.5              # the human never owns more than half


def _logit(p):
    p = min(max(p, 1e-4), 1 - 1e-4)
    return math.log(p / (1 - p))


def _sigmoid(x):
    return 1.0 / (1.0 + math.exp(-np.clip(x, -30, 30)))


def human_weight(scored: list) -> float:
    """The pre-declared earned weight: zero under MIN_SCORED,
    then the Brier advantage, capped at W_CAP."""
    if len(scored) < MIN_SCORED:
        return 0.0
    b_model = float(np.mean([j["brier_model"] for j in scored]))
    b_human = float(np.mean([j["brier_human"] for j in scored]))
    if b_model <= 0:
        return 0.0
    return float(np.clip((b_model - b_human) / b_model,
                          0.0, W_CAP))


def run_bayes(research_dir: Path) -> dict:
    """The nightly pass: blend every open row that carries a
    judgment, score every resolved one, and publish the three-way
    scoreboard."""
    fw = json.loads(
        (research_dir / "smh_forward.json").read_text())
    rows = {(r["ticker"], r["entry_index"]): r
            for r in fw.get("rows", [])}
    jpath = research_dir / "smh_judgment.json"
    log = (json.loads(jpath.read_text())
           if jpath.exists() else {"judgments": []})
    scored = [j for j in log["judgments"]
              if j.get("outcome") is not None]
    w = human_weight(scored)

    blends = []
    for j in log["judgments"]:
        r = rows.get((j["ticker"], j["entry_index"]))
        if r is None:
            continue
        p_b = float(_sigmoid(
            w * _logit(j["human_p"])
            + (1 - w) * _logit(j["model_p"])))
        entry = {
            "ticker": j["ticker"],
            "entry_index": j["entry_index"],
            "model_p": j["model_p"],
            "human_p": j["human_p"],
            "blend_p": round(p_b, 4),
            "weight_human": round(w, 3),
        }
        if r["status"] == "resolved":
            y = float(r["outcome"])
            entry["outcome"] = int(y)
            entry["brier_blend"] = round((p_b - y) ** 2, 4)
        blends.append(entry)

    b_path = research_dir / "smh_bayes.json"
    result = {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "protocol": "pre-declared logit blend; the human's "
            f"weight is zero until {MIN_SCORED} scored "
            "judgments, then the Brier advantage capped at "
            f"{W_CAP}; the logged forward row is never revised "
            "(doctrine rule 2) - the blend is a separate scored "
            "track",
        "human_weight": round(w, 3),
        "n_scored_judgments": len(scored),
        "min_scored": MIN_SCORED,
        "w_cap": W_CAP,
        "blends": blends,
        "scoreboard": {
            "model_brier": (round(float(np.mean(
                [j["brier_model"] for j in scored])), 4)
                if scored else None),
            "human_brier": (round(float(np.mean(
                [j["brier_human"] for j in scored])), 4)
                if scored else None),
            "blend_brier": (round(float(np.mean(
                [b["brier_blend"] for b in blends
                  if "brier_blend" in b])), 4)
                if any("brier_blend" in b for b in blends)
                else None),
            "statement": ("the three-way scoreboard: the model, "
                          "the human, and the blend - the "
                          "Bayesian forecaster's whole "
                          "existence, on the record" if scored
                          else "no judgments scored yet - the "
                          "blend waits with the rows"),
        },
    }
    b_path.write_text(json.dumps(result, indent=2))
    return result


def main() -> None:
    ap = argparse.ArgumentParser(
        description="SMH Bayesian forecaster (the blend)")
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_bayes(args.research_dir)
    sb = r["scoreboard"]
    print(f"smh bayes -> {args.research_dir}/smh_bayes.json "
          f"(human weight {r['human_weight']} at "
          f"{r['n_scored_judgments']} scored judgments; "
          f"model {sb['model_brier']}, human {sb['human_brier']}, "
          f"blend {sb['blend_brier']})")


if __name__ == "__main__":
    main()
