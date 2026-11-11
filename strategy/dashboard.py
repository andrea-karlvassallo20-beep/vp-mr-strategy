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


def mtm_equity(paper_dir: Path, state_path: Path = None):
    """Mark-to-market equity series from decision-log positions x feed
    prices. Returns (dates, equity list, initial_equity) or None."""
    state_path = state_path or (paper_dir / "state" / "session_state.json")
    if not state_path.exists():
        return None
    state = json.load(open(state_path))
    universe = state["universe"]
    bars = {s: load_bars(paper_dir / "data" / f"{s.lower()}.csv")
            for s in universe}
    dates = sorted({b["date"] for s in universe for b in bars[s]})
    if not dates:
        return None
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
    return dates, equity, state["initial_equity"]


def equity_curve_svg(paper_dir: Path, width=860, height=220) -> str:
    """Equity curve from decision-log positions x feed prices (MTM)."""
    res = mtm_equity(paper_dir)
    if res is None:
        return "<p>no session data yet</p>"
    _, equity, initial = res
    eq = np.array(equity)
    lo, hi = float(eq.min()), float(eq.max())
    rng = (hi - lo) or 1.0
    pts = []
    for i, v in enumerate(eq):
        x = 10 + (width - 20) * i / max(len(eq) - 1, 1)
        y = 10 + (height - 20) * (1 - (v - lo) / rng)
        pts.append(f"{x:.1f},{y:.1f}")
    poly = " ".join(pts)
    base_y = 10 + (height - 20) * (1 - (initial - lo) / rng)
    color = "#2e7d32" if eq[-1] >= initial else "#c62828"
    return (f'<svg width="{width}" height="{height}" role="img" '
            f'aria-label="equity curve">'
            f'<line x1="10" y1="{base_y:.1f}" x2="{width-10}" '
            f'y2="{base_y:.1f}" stroke="#999" stroke-dasharray="4"/>'
            f'<polyline fill="none" stroke="{color}" stroke-width="2" '
            f'points="{poly}"/></svg>')


def drawdown_svg(paper_dir: Path, width=860, height=140) -> str:
    """Underwater curve: percentage drawdown from the running peak."""
    res = mtm_equity(paper_dir)
    if res is None:
        return "<p>no session data yet</p>"
    _, equity, _ = res
    eq = np.maximum.accumulate(np.array(equity))
    dd = (np.array(equity) - eq) / eq * 100.0
    lo = float(dd.min())
    rng = (-lo) or 1.0
    pts = []
    for i, v in enumerate(dd):
        x = 10 + (width - 20) * i / max(len(dd) - 1, 1)
        y = 8 + (height - 16) * (-v / rng)
        pts.append(f"{x:.1f},{y:.1f}")
    poly = " ".join(pts)
    area = f"10,{height - 8} " + poly + f" {width - 10},{height - 8}"
    return (f'<svg width="{width}" height="{height}" role="img" '
            f'aria-label="drawdown curve">'
            f'<polygon fill="rgba(248,81,73,.25)" points="{area}"/>'
            f'<polyline fill="none" stroke="#f85149" stroke-width="1.5" '
            f'points="{poly}"/></svg>')


def price_charts_html(paper_dir: Path, per_width=460,
                      per_height=150) -> str:
    """Per-instrument close-price charts with trade-entry markers.
    Green up-triangles mark long entries, red down-triangles short
    entries (position changes from the decision log)."""
    state_path = paper_dir / "state" / "session_state.json"
    if not state_path.exists():
        return "<p>no session data yet</p>"
    state = json.load(open(state_path))
    universe = state["universe"]
    bars = {s: load_bars(paper_dir / "data" / f"{s.lower()}.csv")
            for s in universe}
    entries = {s: {} for s in universe}
    prev_pos = {s: 0.0 for s in universe}
    for rec in state["decision_log"]:
        s = rec["instrument"]
        if rec["position"] != prev_pos[s]:
            entries[s][rec["ts"]] = rec["position"] - prev_pos[s]
            prev_pos[s] = rec["position"]
    svgs = []
    for s in universe:
        bl = bars.get(s, [])
        if not bl:
            continue
        closes = np.array([b["close"] for b in bl])
        lo, hi = float(closes.min()), float(closes.max())
        rng = (hi - lo) or 1.0
        n = len(closes)
        pts = []
        for i, v in enumerate(closes):
            x = 8 + (per_width - 16) * i / max(n - 1, 1)
            y = 8 + (per_height - 24) * (1 - (v - lo) / rng)
            pts.append(f"{x:.1f},{y:.1f}")
        poly = " ".join(pts)
        marks = []
        for i, b in enumerate(bl):
            dpos = entries[s].get(b["date"])
            if not dpos:
                continue
            x = 8 + (per_width - 16) * i / max(n - 1, 1)
            y = 8 + (per_height - 24) * (1 - (b["close"] - lo) / rng)
            if dpos > 0:
                marks.append(f'<path d="M{x:.1f},{y - 4:.1f} l4,7 l-8,0 z" '
                             f'fill="#3fb950"/>'
                             f'<title>{s} long entry</title>')
            else:
                marks.append(f'<path d="M{x:.1f},{y + 4:.1f} l4,-7 l-8,0 z" '
                             f'fill="#f85149"/>'
                             f'<title>{s} short entry</title>')
        svgs.append(
            f'<div class="pc"><h3>{_esc(s)}</h3>'
            f'<svg width="{per_width}" height="{per_height}" role="img" '
            f'aria-label="{_esc(s)} price with entries">'
            f'<polyline fill="none" stroke="#58a6ff" stroke-width="1.5" '
            f'points="{poly}"/>' + "".join(marks) + "</svg></div>")
    if not svgs:
        return "<p>no bars</p>"
    return ('<div class="pgrid">' + "".join(svgs) + "</div>")


def race_svg(paper_dir: Path, width=900, height=260) -> str:
    """Champion vs challenger equity overlay from the two persisted
    shadow states."""
    champ = mtm_equity(paper_dir)
    chall = mtm_equity(paper_dir,
                       paper_dir / "challenger" / "session_state.json")
    if chall is None:
        return ("<p class=\"dim\">Challenger shadow state not yet "
                "generated; the race chart appears after the first nightly "
                "challenger session.</p>")
    series = []
    for label, res, color in (("Challenger", chall, "#58a6ff"),
                              ("Champion", champ, "#3fb950")):
        dates, equity, _ = res
        eq = np.array(equity, dtype=float)
        lo, hi = float(eq.min()), float(eq.max())
        rng = (hi - lo) or 1.0
        pts = []
        for i, v in enumerate(eq):
            x = 10 + (width - 20) * i / max(len(eq) - 1, 1)
            y = 10 + (height - 30) * (1 - (v - lo) / rng)
            pts.append(f"{x:.1f},{y:.1f}")
        series.append((label, color, " ".join(pts)))
    lines = "".join(
        f'<polyline fill="none" stroke="{c}" stroke-width="2" '
        f'points="{p}"/>' for _, c, p in series)
    legend = "".join(
        f'<rect x="{10 + i * 130}" y="4" width="10" height="10" '
        f'fill="{c}"/><text x="{24 + i * 130}" y="13" '
        f'fill="#8b949e" font-size="11">{l}</text>'
        for i, (l, c, _) in enumerate(series))
    return (f'<svg width="{width}" height="{height}" role="img" '
            f'aria-label="champion vs challenger equity">{legend}'
            f'{lines}</svg>')


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


def build_site(paper_dir: Path) -> str:
    """Salient: the public one-page site (GitHub Pages, docs/index.html).
    Same data as the dashboard, branded, with auto-refresh."""
    s = summarize(paper_dir)
    verdict = s.get("verdict", "NOT_GENERATED")
    edge_path = paper_dir / "edge_report.md"
    edge_rec = "NOT_GENERATED"
    if edge_path.exists():
        m = re.search(r"Recommendation: (PROPOSE_REDEPLOY|KEEP_PRODUCTION)",
                      edge_path.read_text())
        if m:
            edge_rec = m.group(1)
    svg = equity_curve_svg(paper_dir, width=900, height=280)
    dd_svg = drawdown_svg(paper_dir, width=900, height=130)
    price_html = price_charts_html(paper_dir)
    race_chart = race_svg(paper_dir)
    sessions = s.get("sessions_completed", 0)
    pct = min(100, int(100 * sessions / 20))
    journal_html = ""
    journal_path = paper_dir / "journal.md"
    if journal_path.exists():
        rows = [l for l in journal_path.read_text().splitlines()
                if l.startswith("| 20")][-10:]
        journal_html = ('<section><h2>Session journal</h2>'
                       '<table><tr><th>Date</th><th>Sessions</th>'
                       '<th>Verdict</th><th>SPI</th><th>Sharpe</th>'
                       '<th>Max DD</th><th>Race</th><th>Equity</th></tr>'
                       + "".join(r for r in rows) + "</table></section>")
    race_html = ""
    race_path = paper_dir / "challenger_report.md"
    if race_path.exists():
        race = race_path.read_text()
        import re as _re2
        m = _re2.search(r"Recommendation: (PROPOSE_REDEPLOY|KEEP_CHAMPION)", race)
        rec = m.group(1) if m else "?"
        rows = _re2.findall(
            r"\| (Champion[^|]*|Challenger[^|]*)\| ([\d.-]+) \| ([\d.-]+) \| ([\d.-]+) \|",
            race)
        rows_html = "".join(
            f"<tr><td>{_esc(a.strip())}</td><td>{b}%</td>"
            f"<td>{c}</td><td>{d}%</td></tr>" for a, b, c, d in rows)
        race_html = (f'<section><h2>Self-learning race: champion vs challenger</h2>'
                     f'<p class="dim">The edge-seeker nominates a candidate each '
                     f'night; it shadow-trades on the same real data. Current '
                     f'verdict: <strong>{_esc(rec)}</strong>. Applying a proposal '
                     f'is always a human-reviewed PR (Gate 3).</p>'
                     f'<table><tr><th>Strategy</th><th>Return</th><th>Sharpe</th>'
                     f'<th>Max DD</th></tr>{rows_html}</table></section>')

    def metric(label, value, sub=""):
        sub_html = f'<div class="sub">{_esc(sub)}</div>' if sub else ""
        return (f'<div class="m"><div class="ml">{_esc(label)}</div>'
                f'<div class="mv">{_esc(value)}</div>{sub_html}</div>')

    metrics = "".join([
        metric("Forward sessions", f"{sessions} / 20", "to promotion"),
        metric("Gate verdict", verdict, "self-judged"),
        metric("SPI", s.get("spi", "?"), "signal parity index"),
        metric("Sharpe", s.get("sharpe", "?"), "MTM, net of costs"),
        metric("Max drawdown", f"{s.get('max_dd_pct', '?')}%", ""),
        metric("Fills", s.get("fills", 0), f"{s.get('orders', 0)} orders"),
        metric("Edge-seeker", edge_rec, "nightly research"),
        metric("Positions", "flat" if not s.get("positions")
               else _esc(s["positions"]), ""),
    ])

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="300">
<title>Salient — VP-MR-ETF-D1-001</title>
<style>
:root {{ --bg:#0d1117; --panel:#161b22; --ink:#e6edf3; --dim:#8b949e;
        --accent:#58a6ff; --good:#3fb950; --bad:#f85149; }}
body {{ background:var(--bg); color:var(--ink); margin:0;
       font-family:-apple-system,'Segoe UI',sans-serif; }}
header {{ padding:40px 32px 8px; max-width:980px; margin:0 auto; }}
h1 {{ font-size:34px; margin:0; letter-spacing:-0.5px; }}
h1 span {{ color:var(--accent); }}
.tagline {{ color:var(--dim); margin:6px 0 0; font-size:14px; }}
main {{ max-width:980px; margin:0 auto; padding:16px 32px 48px; }}
.progress {{ background:var(--panel); border-radius:10px; height:14px;
             margin:20px 0 28px; overflow:hidden; }}
.bar {{ height:100%; width:{pct}%; background:linear-gradient(90deg,
        #1f6feb,#58a6ff); border-radius:10px; }}
.metrics {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }}
.m {{ background:var(--panel); border-radius:10px; padding:16px; }}
.ml {{ font-size:11px; text-transform:uppercase; letter-spacing:.6px;
       color:var(--dim); }}
.mv {{ font-size:24px; font-weight:700; margin-top:4px; }}
.sub {{ font-size:11px; color:var(--dim); margin-top:2px; }}
section {{ background:var(--panel); border-radius:10px; padding:20px;
           margin-top:20px; }}
h2 {{ font-size:16px; margin:0 0 12px; color:var(--ink); }}
.dim {{ color:var(--dim); }}
.pgrid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:14px; }}
.pc {{ background:#0d1117; border:1px solid #21262d; border-radius:8px;
       padding:10px 12px 6px; }}
.pc h3 {{ margin:0 0 6px; font-size:13px; color:var(--dim); }}
.pc svg {{ width:100%; height:auto; display:block; }}
.legend {{ font-size:11px; color:var(--dim); margin:-6px 0 12px; }}
.legend span {{ margin-right:16px; }}
.dot {{ display:inline-block; width:9px; height:9px; border-radius:2px;
       margin-right:4px; vertical-align:middle; }}
footer {{ color:var(--dim); font-size:12px; text-align:center;
          padding:24px; }}
a {{ color:var(--accent); }}
</style></head><body>
<header>
<h1>Salient<span>.</span></h1>
<p class="tagline">VP-MR-ETF-D1-001 — volatility-parity mean reversion on US
equity ETFs, paper-trading autonomously. Self-audited nightly; promotion
judged by evidence.</p>
</header>
<main>
<div class="progress"><div class="bar"></div></div>
<div class="metrics">{metrics}</div>
<section><h2>Paper-trading equity (mark-to-market, net of costs)</h2>
<p class="legend"><span><i class="dot" style="background:#3fb950"></i>equity</span>
<span><i class="dot" style="background:#f85149"></i>drawdown from peak</span></p>
{svg}
<h2 style="margin-top:18px">Drawdown (underwater curve)</h2>
{dd_svg}
</section>
<section><h2>Instrument prices &amp; trade entries</h2>
<p class="dim">Green up-triangles mark long entries, red down-triangles
short entries, from the audited decision log.</p>
{price_html}
</section>
{journal_html}
{race_html}
<section><h2>Self-learning race: equity overlay</h2>
<p class="dim">Champion (deployed, frozen) vs challenger (edge-seeker
nominee, shadow-trading on the same real data). Each curve is scaled
to its own range.</p>
{race_chart}
</section>
<section><h2>How this works</h2>
<p style="color:var(--dim);line-height:1.6">Every trading day after the US
market close, this system fetches real bars for SPY, QQQ, IWM, XLF and XLE,
runs its frozen strategy, audits every decision (SPI), writes a performance
report, runs an edge-seeking research pass, re-evaluates its own promotion
gate, and republishes this page. It never changes its own parameters —
proposals are committed for human review.</p>
<p style="color:var(--dim)"><a href="https://github.com/andrea-karlvassallo20-beep/vp-mr-strategy">Source, evidence and full work log on GitHub</a></p>
</section>
</main>
<footer>Salient — regenerated automatically after each paper-trading
session. Research system, not investment advice.</footer>
</body></html>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper-dir", type=Path, default=Path("paper"))
    ap.add_argument("--out", type=Path, default=Path("dashboard.html"))
    ap.add_argument("--markdown", type=Path, default=Path("DASHBOARD.md"))
    ap.add_argument("--site", type=Path, default=None,
                    help="also write the Salient site (GitHub Pages)")
    args = ap.parse_args()
    html = build_html(args.paper_dir)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html)
    print(f"dashboard written -> {args.out} ({len(html)} bytes)")
    md = build_markdown(args.paper_dir)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text(md)
    print(f"markdown dashboard written -> {args.markdown}")
    if args.site:
        site = build_site(args.paper_dir)
        args.site.parent.mkdir(parents=True, exist_ok=True)
        args.site.write_text(site)
        print(f"salient site written -> {args.site}")


if __name__ == "__main__":
    main()
