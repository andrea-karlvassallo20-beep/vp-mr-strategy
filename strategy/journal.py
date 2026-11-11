"""Session journal: append-only history of paper-trading sessions.

Each nightly session appends one dated entry to paper/journal.md —
sessions completed, gate verdict, SPI, Sharpe, max drawdown, challenger
race verdict — so the forward test has a visible day-by-day history
instead of overwritten reports. Idempotent per date: a re-run on the
same day updates that day's row rather than duplicating it.

Usage (nightly, after the gate and race reports):
    python3 journal.py --data-dir ./paper/data --state-dir ./paper/state \
        --journal ./paper/journal.md
"""
import argparse
import datetime
import re
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from session_report import build_report
from monitor import summarize

HEADER = ("| Date | Sessions | Verdict | SPI | Sharpe | Max DD % | "
          "Race | Equity (MTM) |\n|---|---|---|---|---|---|---|---|\n")


def journal_entry(data_dir: Path, state_dir: Path,
                  date: str = None) -> str:
    rep = build_report(data_dir, state_dir)
    s = summarize(state_dir and state_dir.parent)
    race = "n/a"
    race_path = state_dir.parent / "challenger_report.md"
    if race_path.exists():
        m = re.search(
            r"Recommendation: (PROPOSE_REDEPLOY|KEEP_CHAMPION)",
            race_path.read_text())
        if m:
            race = m.group(1)
    if date is None:
        state = state_dir / "session_state.json"
        import json
        dates = [rec["ts"] for rec in
                 json.load(open(state))["decision_log"]]
        date = max(dates) if dates else (
            datetime.date.today().isoformat())
    return (f"| {date} | {s.get('sessions_completed', '?')}/20 "
            f"| {s.get('verdict', '?')} | {rep['spi']} "
            f"| {rep['sharpe']} | {rep['max_dd_pct']} | {race} "
            f"| {rep['final_equity_mtm']} |")


def update_journal(journal_path: Path, entry: str) -> bool:
    """Insert or replace the row for this date. Returns True if changed."""
    date = entry.split("|")[1].strip()
    if not journal_path.exists():
        journal_path.write_text("# Paper-trading session journal\n\n"
                                + HEADER + entry + "\n")
        return True
    text = journal_path.read_text()
    if not text.endswith("\n"):
        text += "\n"
    pattern = re.compile(rf"^\| {re.escape(date)} \|.*$", re.M)
    if pattern.search(text):
        new = pattern.sub(entry, text, count=1)
        if new == text:
            return False
        journal_path.write_text(new)
        return True
    journal_path.write_text(text + entry + "\n")
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--state-dir", required=True, type=Path)
    ap.add_argument("--journal", required=True, type=Path)
    args = ap.parse_args()
    entry = journal_entry(args.data_dir, args.state_dir)
    if update_journal(args.journal, entry):
        print(f"journal updated -> {args.journal}")
    else:
        print("journal unchanged")


if __name__ == "__main__":
    main()
