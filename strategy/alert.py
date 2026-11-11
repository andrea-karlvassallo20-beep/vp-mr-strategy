"""Incident alerts: the system files its own anomaly reports.

After each nightly session, check the committed artifacts for alert
conditions — kill-switch trips, SPI degradation, duplicate order fires,
promotion-gate failures — and open (or update) a GitHub issue with the
evidence. In CI, gh issue create uses the workflow token; locally,
--create-issue is a no-op without write access.

Alert conditions:
  - kill_switch_events > 0        (risk gate tripped)
  - SPI < 0.98                    (signal parity degraded)
  - duplicate_fires > 0          (order machine integrity)
  - race PROPOSE_REDEPLOY         (visibility: redeploy proposal pending)

Usage (nightly, after dashboards):
    python3 alert.py --data-dir ./paper/data --state-dir ./paper/state [--create-issue]
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from session_report import build_report

MIN_SPI = 0.98


def check_alerts(data_dir: Path, state_dir: Path) -> list:
    alerts = []
    rep = build_report(data_dir, state_dir)
    if rep["kill_switch_events"] > 0:
        alerts.append({
            "condition": "KILL_SWITCH_TRIPPED",
            "severity": "critical",
            "evidence": f"{rep['kill_switch_events']} kill-switch event(s) "
                        f"in the latest session; max DD "
                        f"{rep['max_dd_pct']}%."})
    if rep["spi"] < MIN_SPI:
        alerts.append({
            "condition": "SPI_DEGRADED",
            "severity": "critical",
            "evidence": f"signal parity index {rep['spi']} < {MIN_SPI}; "
                        "decision-log parity audit failed."})
    if rep["duplicate_fires"] > 0:
        alerts.append({
            "condition": "DUPLICATE_ORDER_FIRES",
            "severity": "critical",
            "evidence": f"{rep['duplicate_fires']} duplicate-fire event(s) "
                        "detected."})
    race_path = state_dir.parent / "challenger_report.md"
    if race_path.exists():
        m = re.search(r"Recommendation: (PROPOSE_REDEPLOY|KEEP_CHAMPION)",
                      race_path.read_text())
        if m and m.group(1) == "PROPOSE_REDEPLOY":
            alerts.append({
                "condition": "REDEPLOY_PROPOSAL_PENDING",
                "severity": "notice",
                "evidence": "the challenger beat the champion on live paper "
                            "data; a redeployment proposal should exist."})
    return alerts


def issue_title(alerts: list) -> str:
    critical = [a for a in alerts if a["severity"] == "critical"]
    if critical:
        return (f"[ALERT] {len(critical)} critical anomaly(ies) in the "
                "paper-trading session")
    return "[NOTICE] redeploy proposal pending"


def issue_body(alerts: list) -> str:
    lines = ["## Session anomalies", ""]
    for a in alerts:
        lines.append(f"- **{a['condition']}** ({a['severity']}): "
                     f"{a['evidence']}")
    lines += ["", "Filed automatically by strategy/alert.py from the "
              "nightly session artifacts. Inspect `paper/` for the full "
              "audit trail."]
    return "\n".join(lines) + "\n"


def create_issue(alerts: list) -> None:
    title = issue_title(alerts)
    body_path = "/tmp/alert_body.md"
    Path(body_path).write_text(issue_body(alerts))
    # idempotency: reuse an open alert issue with the same title
    r = subprocess.run(
        ["gh", "issue", "list", "--state", "open",
         "--search", title, "--json", "number"],
        capture_output=True, text=True)
    existing = json.loads(r.stdout) if r.returncode == 0 else []
    if existing:
        subprocess.run(["gh", "issue", "comment",
                        str(existing[0]["number"]),
                        "--body-file", body_path], capture_output=True)
        print(f"alert appended to issue #{existing[0]['number']}")
        return
    r = subprocess.run(
        ["gh", "issue", "create", "--title", title,
         "--body-file", body_path, "--label", "alert"],
        capture_output=True, text=True)
    if r.returncode == 0:
        print("alert issue opened:", r.stdout.strip())
    else:
        print("issue creation skipped (no write access):", r.stderr.strip())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--state-dir", required=True, type=Path)
    ap.add_argument("--create-issue", action="store_true")
    args = ap.parse_args()
    alerts = check_alerts(args.data_dir, args.state_dir)
    if not alerts:
        print("no alerts: session clean")
        return
    for a in alerts:
        print(f"ALERT {a['severity']}: {a['condition']} — {a['evidence']}")
    if args.create_issue:
        create_issue(alerts)


if __name__ == "__main__":
    main()
