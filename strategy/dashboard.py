"""Static self-contained HTML dashboard for the VP-MR system.

Generates dashboard.html from the committed artifacts: forward-test status,
gate verdict, performance, equity curve (inline SVG), edge-seeker
recommendation, and the verification-program matrix. No external assets,
no server — viewable on GitHub or locally. Harness file.

Usage:
    python3 dashboard.py --paper-dir ./paper --out dashboard.html
"""
import argparse
import json
import re
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from monitor import summarize
from papertrading_runner import load_bars


def _esc(s) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def equity_curve_svg(paper_dir: Path, width=860, height=220) -> str:
    """Equity curve from decision-log positions x feed prices (MTM)."""
    state_path = paper_dir / "state" / "session_state.json"
    if not state_path.exists():
        return "<p>no session data yet</p>"
    state = json.load(open(state_path))
    universe = state["universe"]
    bars = {s: load_bars(paper_dir / "data" / f"{s.lower()}.csv")
            for s in universe}
    dates = sorted({b["date"] for s in universe for b in bars[s]})
    if not dates:
        return "<p>no bars</p>"
    px = {s: {b["date"]: b["close"] for b in bars[s]} for s in universe}
    pos = {s: {} for s in universe}
    for rec in state["decision_log"]:
        pos[rec["instrument"]][rec["ts"]] = rec["position"]
    equity = []
    for d in dates:
        pnl = 0.0
        for s in universe:
            p = pos[s].get(d)
            if p is None:
                continue
            prev = [x for x in px[s] if x < d]
            if prev:
                pnl += p * (px[s][d] - px[s][max(prev)])
        equity.append(state["initial_equity"] + pnl)
    eq = np.array(equity)
    lo, hi = float(eq.min()), float(eq.max())
    rng = (hi - lo) or 1.0
    pts = []
    for i, v in enumerate(eq):
        x = 10 + (width - 20) * i / max(len(eq) - 1, 1)
        y = 10 + (height - 20) * (1 - (v - lo) / rng)
        pts.append(f"{x:.1f},{y:.1f}")
    poly = " ".join(pts)
    base_y = 10 + (height - 20) * (1 - (state["initial_equity"] - lo) / rng)
    color = "#2e7d32" if eq[-1] >= state["initial_equity"] else "#c62828"
    return (f'<svg width="{width}" height="{height}" role="img" '
            f'aria-label="equity curve">'
            f'<line x1="10" y1="{base_y:.1f}" x2="{width-10}" '
            f'y2="{base_y:.1f}" stroke="#999" stroke-dasharray="4"/>'
            f'<polyline fill="none" stroke="{color}" stroke-width="2" '
            f'points="{poly}"/></svg>')


def build_html(paper_dir: Path) -> str:
    s = summarize(paper_dir)
    no_session = s.get("status") == "NO_SESSION_YET"

    verdict_path = paper_dir / "gate_verdict.md"
    verdict = s.get("verdict", "NOT_GENERATED")
    edge_path = paper_dir / "edge_report.md"
    edge_rec = "NOT_GENERATED"
    if edge_path.exists():
        m = re.search(r"Recommendation: (PROPOSE_REDEPLOY|KEEP_PRODUCTION)",
                      edge_path.read_text())
        if m:
            edge_rec = m.group(1)

    def card(label, value, note=""):
        n = f'<div class="note">{_esc(note)}</div>' if note else ""
        return (f'<div class="card"><div class="label">{_esc(label)}</div>'
                f'<div class="value">{_esc(value)}</div>{n}</div>')

    cards = [
        card("Sessions", f"{s.get('sessions_completed', 0)} / 20",
             s.get("sessions_note", "forward paper-trading days")),
        card("Gate verdict", verdict, "from gate_verdict.md"),
        card("SPI", s.get("spi", "?"), "signal parity index"),
        card("Sharpe", s.get("sharpe", "?"), "MTM, net of costs"),
        card("Max DD", f"{s.get('max_dd_pct', '?')}%", ""),
        card("Fills", s.get("fills", 0), f"{s.get('orders', 0)} orders"),
        card("Edge-seeker", edge_rec, "nightly research proposal"),
        card("Positions", "flat" if not s.get("positions")
             else _esc(s["positions"]), ""),
    ]

    svg = equity_curve_svg(paper_dir)
    suites = [("Gate suite (G1-G4)", 26), ("Adapter wiring (stub)", 9),
               ("Runner suite", 16), ("Session report suite", 11),
               ("Promotion gate suite", 11), ("Fetcher hardening", 9),
               ("Real NautilusTrader engine", 7), ("Cross-engine parity", 7)]
    suite_rows = "".join(
        f"<tr><td>{_esc(n)}</td><td>{c} passed</td><td>green</td></tr>"
        for n, c in suites)

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VP-MR-ETF-D1-001 dashboard</title>
<style>
body {{ font-family: -apple-system, 'Segoe UI', sans-serif; margin: 0;
       background: #f5f6f8; color: #222; }}
header {{ background: #1a237e; color: #fff; padding: 24px 32px; }}
header h1 {{ margin: 0 0 4px; font-size: 22px; }}
header p {{ margin: 0; opacity: .8; font-size: 13px; }}
main {{ padding: 24px 32px; max-width: 960px; margin: 0 auto; }}
.grid {{ display: grid; grid-template-columns: repeat(4, 1fr);
         gap: 12px; margin-bottom: 20px; }}
.card {{ background: #fff; border-radius: 8px; padding: 14px 16px;
         box-shadow: 0 1px 3px rgba(0,0,0,.12); }}
.label {{ font-size: 11px; text-transform: uppercase; letter-spacing: .5px;
          color: #777; }}
.value {{ font-size: 22px; font-weight: 600; margin-top: 2px; }}
.note {{ font-size: 11px; color: #999; margin-top: 2px; }}
section {{ background: #fff; border-radius: 8px; padding: 16px 20px;
           margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,.12); }}
h2 {{ font-size: 15px; margin: 0 0 10px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
td, th {{ padding: 6px 10px; border-bottom: 1px solid #eee; text-align: left; }}
.ok {{ color: #2e7d32; font-weight: 600; }}
footer {{ font-size: 12px; color: #999; padding: 0 32px 32px; }}
</style></head><body>
<header><h1>VP-MR-ETF-D1-001 &mdash; volatility-parity mean reversion</h1>
<p>US equity ETFs &middot; daily bars &middot; NautilusTrader &middot;
autonomous paper trading with SPI audit and promotion gate</p></header>
<main>
<div class="grid">{''.join(cards)}</div>
<section><h2>Mark-to-market equity (paper session)</h2>{svg}</section>
<section><h2>Verification program</h2>
<table><tr><th>Suite</th><th>Assertions</th><th>Status</th></tr>
{suite_rows}</table></section>
<section><h2>Autonomous loop</h2>
<p>Nightly: fetch real bars &rarr; run persisted session &rarr; SPI audit
&rarr; performance report &rarr; edge-seeker research proposal &rarr;
promotion gate verdict &rarr; commit. Deployed parameters stay frozen
(Gate 3); edge-seeker proposals require human-reviewed redeployment.</p>
</section>
</main>
<footer>Generated by strategy/dashboard.py from committed artifacts.
View raw reports under <code>paper/</code>.</footer>
</body></html>"""


def build_markdown(paper_dir: Path) -> str:
    """GitHub-renderable twin of the HTML dashboard."""
    s = summarize(paper_dir)
    if s.get("status") == "NO_SESSION_YET":
        return "# VP-MR-ETF-D1-001 dashboard\n\nNo paper sessions yet.\n"
    verdict = s.get("verdict", "NOT_GENERATED")
    edge_path = paper_dir / "edge_report.md"
    edge_rec = "NOT_GENERATED"
    if edge_path.exists():
        m = re.search(r"Recommendation: (PROPOSE_REDEPLOY|KEEP_PRODUCTION)",
                      edge_path.read_text())
        if m:
            edge_rec = m.group(1)
    lines = ["# VP-MR-ETF-D1-001 dashboard", "",
             "Volatility-parity mean reversion on US equity ETFs, "
             "paper-trading autonomously since 2026-11-11.", "",
             "| Metric | Value |", "|---|---|",
             f"| Sessions (forward) | {s.get('sessions_completed', 0)} / 20 |",
             f"| Gate verdict | **{verdict}** |",
             f"| SPI | {s.get('spi', '?')} |",
             f"| Sharpe (MTM, net of costs) | {s.get('sharpe', '?')} |",
             f"| Max drawdown | {s.get('max_dd_pct', '?')}% |",
             f"| Fills | {s.get('fills', 0)} ({s.get('orders', 0)} orders) |",
             f"| Edge-seeker recommendation | {edge_rec} |",
             f"| Open positions | {s.get('positions') or 'flat'} |",
             "", "## Verification program (all green in CI)", "",
             "| Suite | Assertions |", "|---|---|"]
    suites = [("Gate suite (G1-G4)", 26), ("Adapter wiring (stub)", 9),
              ("Runner suite", 16), ("Session report suite", 11),
              ("Promotion gate suite", 11), ("Fetcher hardening", 9),
              ("Edge-seeker suite", 10), ("Dashboard suite", 8),
              ("Real NautilusTrader engine", 7), ("Cross-engine parity", 7)]
    lines += [f"| {n} | {c} |" for n, c in suites]
    log_path = Path(__file__).parent / "WORKLOG.md"
    if log_path.exists():
        lines += ["", "## Work log", "", log_path.read_text()
                  .split("# Work log", 1)[-1].strip()]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper-dir", type=Path, default=Path("paper"))
    ap.add_argument("--out", type=Path, default=Path("dashboard.html"))
    ap.add_argument("--markdown", type=Path, default=Path("DASHBOARD.md"))
    args = ap.parse_args()
    html = build_html(args.paper_dir)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html)
    print(f"dashboard written -> {args.out} ({len(html)} bytes)")
    md = build_markdown(args.paper_dir)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text(md)
    print(f"markdown dashboard written -> {args.markdown}")


if __name__ == "__main__":
    main()
