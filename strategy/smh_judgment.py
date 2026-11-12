"""THE SMH JUDGMENT LOG (charter v3, section 9 rule 4 and open
problem 5): the human forecaster INSIDE the protocol, as a
component to be calibrated - not an oracle outside it.

The charter's Bayesian forecaster is "human prior times measured
calibration: the formal version of integrating your judgment
into the hazard model once it has a score." The score does not
exist yet (no forward row has resolved), but the LOG can: this
module gives the human a place to record a prior probability
BEFORE the outcome, attached to the same forward rows the model
drafted, under the same doctrine rules:

  rule 2 (advance or not at all): a judgment is accepted only
       against an OPEN forward row, and only before its window
       could have resolved; it is never revised afterward.
  rule 5 (seductive cells carry flags forever): every judgment
       is logged with its reasoning, however short.
  rule 6 (corrections are part of the record): the log is
       append-only.

When the rows resolve, the resolver scores the human's Brier
next to the model's - the calibration record the observer
corollary names as the only private edge this programme can
build.

CLI (the human's entry point):
    python3 smh_judgment.py --ticker BTC-USD --p 0.7 \\
        --note "coiling under resistance since October" \\
        --research-dir ../paper/research

Nightly (integration pass, no CLI):
    python3 smh_judgment.py --data-dir ../paper/research/data \\
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))


def _load_forward(research_dir: Path) -> dict:
    path = research_dir / "smh_forward.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def record_judgment(research_dir: Path, ticker: str, p: float,
                    note: str) -> dict:
    """Append one human prior against an OPEN forward row.
    Rejected (with the reason, on the record) if: the row does
    not exist, the row is not open, a judgment already exists
    for that row, or p is not a probability."""
    fw = _load_forward(research_dir)
    rows = fw.get("rows", [])
    row = next((r for r in rows
                if r["ticker"].upper() == ticker.upper()
                and r["status"] == "open"), None)
    if row is None:
        return {"status": "REJECTED",
                "reason": f"no OPEN forward row for {ticker}"}
    jpath = research_dir / "smh_judgment.json"
    log = (json.loads(jpath.read_text())
           if jpath.exists() else {"judgments": []})
    if any(j["ticker"].upper() == ticker.upper()
           and j["entry_index"] == row["entry_index"]
           for j in log["judgments"]):
        return {"status": "REJECTED",
                "reason": "a judgment already exists for this row "
                          "(never revised after the fact)"}
    if not (0.0 < p < 1.0):
        return {"status": "REJECTED",
                "reason": f"p = {p} is not a probability in (0,1)"}
    log["judgments"].append({
        "ticker": row["ticker"],
        "kind": row["kind"],
        "entry_index": row["entry_index"],
        "model_p": row["forecast_p"],
        "human_p": round(float(p), 4),
        "note": note,
        "logged_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "outcome": None,
        "brier_human": None,
        "brier_model": None,
    })
    jpath.write_text(json.dumps(log, indent=2))
    return {"status": "RECORDED",
            "ticker": row["ticker"],
            "model_p": row["forecast_p"],
            "human_p": round(float(p), 4)}


def resolve_judgments(research_dir: Path) -> dict:
    """The nightly integration pass: score every judgment whose
    forward row has resolved - the human's Brier next to the
    model's, the calibration record the observer corollary
    names. Append-only: outcomes fill in, nothing is rewritten."""
    fw = _load_forward(research_dir)
    rows = {(r["ticker"], r["entry_index"]): r
            for r in fw.get("rows", [])}
    jpath = research_dir / "smh_judgment.json"
    log = (json.loads(jpath.read_text())
           if jpath.exists() else {"judgments": []})
    n_scored = 0
    for j in log["judgments"]:
        if j["outcome"] is not None:
            continue
        r = rows.get((j["ticker"], j["entry_index"]))
        if r is None or r["status"] != "resolved":
            continue
        y = float(r["outcome"])
        j["outcome"] = int(y)
        j["brier_human"] = round(
            (j["human_p"] - y) ** 2, 4)
        j["brier_model"] = round(
            (j["model_p"] - y) ** 2, 4)
        n_scored += 1
    jpath.write_text(json.dumps(log, indent=2))
    scored = [j for j in log["judgments"]
              if j["outcome"] is not None]
    human_brier = (round(float(np.mean(
        [j["brier_human"] for j in scored])), 4)
        if scored else None)
    model_brier = (round(float(np.mean(
        [j["brier_model"] for j in scored])), 4)
        if scored else None)
    return {
        "status": "OK",
        "n_judgments": len(log["judgments"]),
        "n_scored": len(scored),
        "scored_tonight": n_scored,
        "human_brier": human_brier,
        "model_brier": model_brier,
        "statement": ("the human's calibration record, scored "
                      "against the same outcomes as the model - "
                      "the observer corollary's private edge, "
                      "compounding" if scored else
                      "no judgments scored yet - the log waits"),
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="SMH judgment log (the human inside the "
                    "protocol)")
    ap.add_argument("--ticker", type=str, default=None,
                    help="the open forward row to judge")
    ap.add_argument("--p", type=float, default=None,
                    help="the human prior, a probability in (0,1)")
    ap.add_argument("--note", type=str, default="",
                    help="the reasoning, on the record")
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    if args.ticker is not None and args.p is not None:
        r = record_judgment(args.research_dir, args.ticker,
                            args.p, args.note)
        print(f"judgment -> {r['status']}: {r}")
        return
    r = resolve_judgments(args.research_dir)
    print(f"judgment pass: {r['n_scored_tonight']} scored "
          f"tonight, {r['n_scored']} total; "
          f"human Brier {r['human_brier']}, "
          f"model Brier {r['model_brier']}")


if __name__ == "__main__":
    main()
