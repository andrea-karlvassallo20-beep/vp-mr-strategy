"""One-command monitor for the VP-MR paper-trading journal.

Reads the committed paper/ artifacts on any branch and prints the current
state of the forward test: session count, verdict, SPI, performance, and
recent order activity. Harness file.

Usage:
    python3 strategy/monitor.py [--paper-dir ./paper]
"""
import argparse
import json
import re
from pathlib import Path


def summarize(paper_dir: Path) -> dict:
    out = {"paper_dir": str(paper_dir)}
    state_path = paper_dir / "state" / "session_state.json"
    if not state_path.exists():
        out["status"] = "NO_SESSION_YET"
        return out

    state = json.load(open(state_path))
    if "invocations" in state:
        out["sessions_completed"] = state["invocations"]
    else:
        out["sessions_completed"] = 1  # legacy state: at least one session
        out["sessions_note"] = ("legacy state without invocation counter; "
                                "next session will record it")
    out["sessions_required"] = 20
    out["positions"] = {s: q for s, q in state["positions"].items() if q != 0}
    out["equity_internal"] = round(state["equity"], 2)
    out["decisions"] = len(state["decision_log"])
    out["orders"] = len(state["order_log"])
    fills = [o for o in state["order_log"] if o.get("state") == "FILLED"]
    out["fills"] = len(fills)
    out["last_dates"] = dict(state["last_date"])

    verdict_path = paper_dir / "gate_verdict.md"
    if verdict_path.exists():
        text = verdict_path.read_text()
        m = re.search(r"verdict: (PROMOTE|HOLD)", text)
        out["verdict"] = m.group(1) if m else "UNKNOWN"
    else:
        out["verdict"] = "NOT_GENERATED"

    rep_path = paper_dir / "performance_report.md"
    if rep_path.exists():
        text = rep_path.read_text()
        for key, pat in (("sharpe", r"\| sharpe \| ([\d.-]+)"),
                         ("max_dd_pct", r"\| max_dd_pct \| ([\d.-]+)"),
                         ("spi", r"\| spi \| ([\d.-]+)")):
            m = re.search(pat, text)
            if m:
                out[key] = m.group(1)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper-dir", type=Path, default=Path("paper"))
    args = ap.parse_args()
    s = summarize(args.paper_dir)
    if s.get("status") == "NO_SESSION_YET":
        print("no paper-trading state yet - sessions have not run")
        return
    print("=== VP-MR-ETF-D1-001 forward test status ===")
    print(f"  sessions:  {s.get('sessions_completed')} / "
          f"{s.get('sessions_required')} required")
    print(f"  verdict:   {s.get('verdict')}")
    print(f"  SPI:       {s.get('spi', '?')}")
    print(f"  sharpe:    {s.get('sharpe', '?')}   max DD: "
          f"{s.get('max_dd_pct', '?')}%")
    print(f"  decisions: {s.get('decisions')}   orders: {s.get('orders')}   "
          f"fills: {s.get('fills')}")
    print(f"  equity:    {s.get('equity_internal')} (cost-adjusted)")
    print(f"  positions: {s.get('positions') or 'flat'}")
    print(f"  last bar per instrument: {s.get('last_dates')}")


if __name__ == "__main__":
    main()
