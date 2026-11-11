"""Automated redeployment proposal: challenger verdict -> PR.

When the nightly race report says PROPOSE_REDEPLOY, this module:
  1. patches the champion's core parameters (z_entry, lookback) in the
     frozen StrategyParameters defaults — the only auto-applicable subset;
  2. regenerates run_card.json from the new frozen defaults;
  3. prepares a branch and PR body with the full evidence trail.

Everything is deterministic and CI-gated: the PR still requires human
merge (Gate 3). Candidates whose edge comes from the vol model or the
VSA filter require manual implementation and are only flagged.

Usage (nightly, after the challenger step; inside the repo):
    python3 propose_redeploy.py --report ./paper/challenger_report.md [--apply]
    # --apply: actually patch + branch + commit + open the PR (needs git/gh)
"""
import argparse
import re
import subprocess
from pathlib import Path

STRATEGY = Path(__file__).parent / "vp_mr_strategy.py"


def parse_report(report_path: Path) -> dict:
    text = report_path.read_text()
    m = re.search(r"Recommendation: (PROPOSE_REDEPLOY|KEEP_CHAMPION)", text)
    verdict = m.group(1) if m else "KEEP_CHAMPION"
    cand = {}
    mc = re.search(r"z=([\d.]+), lookback=(\d+), vol model=(\w+), "
                   r"VSA filter=(True|False)(?:, exit z=(-?[\d.]+), "
                   r"ATR mult=([\d.]+))?", text)
    if mc:
        cand = {"z_entry": float(mc.group(1)),
                "lookback": int(mc.group(2)),
                "vol_model": mc.group(3),
                "volume_filter": mc.group(4) == "True"}
        if mc.group(5) is not None:
            cand["exit_z"] = float(mc.group(5))
            cand["atr_mult"] = float(mc.group(6))
    rows = re.findall(
        r"\| (Champion[^|]*|Challenger[^|]*)\| ([\d.-]+) \| ([\d.-]+) \| "
        r"([\d.-]+) \|", text)
    return {"verdict": verdict, "candidate": cand, "rows": rows}


def patch_core_params(z_entry: float, lookback: int) -> bool:
    """Deterministically patch the StrategyParameters defaults. Returns
    True if the file changed (i.e., params actually differ)."""
    src = STRATEGY.read_text()
    new = src
    new = re.sub(r"(zscore_entry: float = )[\d.]+", rf"\g<1>{z_entry}", new)
    new = re.sub(r"(lookback_zscore: int = )\d+", rf"\g<1>{lookback}", new)
    if new == src:
        return False
    STRATEGY.write_text(new)
    return True


def pr_body(report: dict) -> str:
    c = report["candidate"]
    rows = "\n".join(
        f"| {a.strip()} | {b}% | {c2} | {d}% |" for a, b, c2, d in report["rows"])
    return f"""## Automated redeployment proposal

The nightly champion/challenger race on live paper data recommends
**PROPOSE_REDEPLOY**. This PR applies the winning candidate's core
parameters and regenerates the run card.

- New z-score entry: **{c.get('z_entry')}** (was 2.0)
- New lookback: **{c.get('lookback')}** (was 100)

### Evidence (live paper window)
| Strategy | Return | Sharpe | Max DD |
|---|---|---|---|
{rows}

### Notes
- Gate 3: this PR is the redeployment mechanism; merging it IS the human
  review. The forward-test session counter continues from the champion's.
- Candidate vol model: {c.get('vol_model')}; VSA filter:
  {c.get('volume_filter')}; exit z: {c.get('exit_z', 0.25)}; ATR mult:
  {c.get('atr_mult', 3.0)}. If these differ from the champion's
  (realized / off / 0.25 / 3.0), they require manual implementation and
  are flagged here only.
- CI runs the full verification program on this PR; merge only if green.

Generated automatically by strategy/propose_redeploy.py from
paper/challenger_report.md.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True, type=Path)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    report = parse_report(args.report)
    if report["verdict"] != "PROPOSE_REDEPLOY":
        print(f"no proposal: verdict is {report['verdict']}")
        return
    c = report["candidate"]
    if not c:
        print("no proposal: candidate unparseable")
        return

    if not args.apply:
        print("proposal ready (dry run):")
        print(pr_body(report))
        return

    changed = patch_core_params(c["z_entry"], c["lookback"])
    if not changed:
        print("no proposal: core params already match the candidate")
        return

    r = subprocess.run(["python3", "strategy/generate_run_card.py"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"run card regeneration failed: {r.stderr}")

    body = "/tmp/redeploy_pr_body.md"
    Path(body).write_text(pr_body(report))
    cmds = [
        ["git", "checkout", "-b", "redeploy/proposal"],
        ["git", "add", "-A"],
        ["git", "commit", "-m",
         f"Automated redeploy proposal: z={c['z_entry']}, "
         f"lookback={c['lookback']} (from challenger race)"],
        ["git", "push", "-u", "origin", "redeploy/proposal"],
        ["gh", "pr", "create", "--title",
         f"Automated redeploy proposal: z={c['z_entry']}, "
         f"lookback={c['lookback']}",
         "--body-file", body],
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 and "already exists" not in r.stderr:
            raise RuntimeError(f"{' '.join(cmd[:3])} failed: {r.stderr}")
        if cmd[0] == "gh" and r.returncode == 0:
            print("proposal PR opened:", r.stdout.strip())


if __name__ == "__main__":
    main()
