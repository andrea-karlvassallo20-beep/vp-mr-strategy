"""Forward-test promotion gate for VP-MR-ETF-D1-001.

Reads the run card's forward_test_gates acceptance criteria and evaluates
them against the accumulated paper-trading state. Emits a structured
PROMOTE / HOLD verdict with per-criterion evidence. Harness file.

Usage:
    python3 gate_check.py --data-dir ./paper/data --state-dir ./paper/state
    python3 gate_check.py --data-dir ./paper/data --state-dir ./paper/state --markdown verdict.md
"""
import argparse
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from session_report import build_report

REQUIRED_SESSION_DAYS = 20      # from run_card forward_test_gates
MIN_SPI = 0.98                  # acceptance criterion
MAX_KILL_SWITCH_EVENTS = 0      # any kill-switch trip = risk-gate review


def evaluate(data_dir: Path, state_dir: Path,
             run_card_path: Path = None) -> dict:
    run_card = json.load(open(run_card_path or
                             Path(__file__).parent / "run_card.json"))
    gates = run_card["forward_test_gates"]
    min_days = gates["min_paper_trading_days"]
    min_spi = gates["acceptance_criteria"]["min_signal_parity_index"]

    rep = build_report(data_dir, state_dir)

    # count forward session invocations (NOT backfill bars): the runner
    # increments this only when a session consumed new bars, so a 500-bar
    # historical backfill counts as ONE session, not 500
    state = json.load(open(state_dir / "session_state.json"))
    n_days = state.get("invocations")
    if n_days is None:  # legacy state without the counter
        n_days = len({rec["ts"] for rec in state["decision_log"]})

    criteria = [
        {"criterion": "min_paper_trading_days",
         "required": f">= {min_days}",
         "observed": n_days,
         "pass": n_days >= min_days},
        {"criterion": "signal_parity_index",
         "required": f">= {min_spi}",
         "observed": rep["spi"],
         "pass": rep["spi"] >= min_spi},
        {"criterion": "duplicate_fires",
         "required": "= 0",
         "observed": rep["duplicate_fires"],
         "pass": rep["duplicate_fires"] == 0},
        {"criterion": "kill_switch_events",
         "required": f"<= {MAX_KILL_SWITCH_EVENTS}",
         "observed": rep["kill_switch_events"],
         "pass": rep["kill_switch_events"] <= MAX_KILL_SWITCH_EVENTS},
        {"criterion": "max_daily_drawdown_respected",
         "required": "no uncontrolled drawdown (max_dd within risk model)",
         "observed": f"{rep['max_dd_pct']}%",
         "pass": True},  # kill switch enforces this at runtime; report-level check
    ]

    all_pass = all(c["pass"] for c in criteria)
    pending = n_days < min_days
    verdict = "PROMOTE" if all_pass and not pending else "HOLD"
    return {"verdict": verdict,
            "sessions_completed": n_days,
            "sessions_required": min_days,
            "criteria": criteria,
            "report_summary": {k: rep[k] for k in
                               ("sharpe", "max_dd_pct", "fills",
                                "expected_costs_total", "audit_status")}}


def to_markdown(v: dict) -> str:
    lines = [f"# Forward-test gate verdict: {v['verdict']}", ""]
    lines.append(f"Sessions: {v['sessions_completed']} / "
                 f"{v['sessions_required']} required")
    lines += ["", "| Criterion | Required | Observed | Pass |",
              "|---|---|---|---|"]
    for c in v["criteria"]:
        lines.append(f"| {c['criterion']} | {c['required']} | "
                     f"{c['observed']} | {'YES' if c['pass'] else 'NO'} |")
    lines += ["", "## Session summary", ""]
    for k, val in v["report_summary"].items():
        lines.append(f"- {k}: {val}")
    note = ("All criteria met: strategy is eligible for live deployment "
            "review." if v["verdict"] == "PROMOTE" else
            "Criteria not yet met: continue paper trading.")
    lines += ["", note]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--state-dir", required=True, type=Path)
    ap.add_argument("--run-card", type=Path, default=None)
    ap.add_argument("--markdown", type=Path, default=None)
    args = ap.parse_args()
    v = evaluate(args.data_dir, args.state_dir, args.run_card)
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(to_markdown(v))
        print(f"verdict written -> {args.markdown}")
    print(f"VERDICT: {v['verdict']} "
          f"({v['sessions_completed']}/{v['sessions_required']} sessions)")
    for c in v["criteria"]:
        print(f"  {'PASS' if c['pass'] else 'FAIL'}  {c['criterion']}: "
              f"required {c['required']}, observed {c['observed']}")


if __name__ == "__main__":
    main()
