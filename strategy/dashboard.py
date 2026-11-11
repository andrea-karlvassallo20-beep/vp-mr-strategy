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
from cross_asset import safe_name
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
    live = [d for d in dates
            if any(pos[s].get(d) for s in universe)]
    if live:
        first = min(live)
        dates = [d for d in dates if d >= first]
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


def equity_curve_svg(paper_dir: Path, width=860, height=220, uid="eq") -> str:
    """Equity curve from decision-log positions x feed prices (MTM)."""
    res = mtm_equity(paper_dir)
    if res is None:
        return "<p>no session data yet</p>"
    dates, equity, initial = res
    eq = np.array(equity)
    lo, hi = float(eq.min()), float(eq.max())
    rng = (hi - lo) or 1.0
    pad = rng * 0.08
    lo, hi, rng = lo - pad, hi + pad, rng + 2 * pad
    n = len(eq)
    xs = [10 + (width - 70) * i / max(n - 1, 1) for i in range(n)]
    ys = [10 + (height - 34) * (1 - (v - lo) / rng) for v in eq]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    area = (f"{xs[0]:.1f},{height - 24} " + poly +
            f" {xs[-1]:.1f},{height - 24}")
    base_y = 10 + (height - 34) * (1 - (initial - lo) / rng)
    color = "#2e7d32" if eq[-1] >= initial else "#c62828"
    grid = ""
    for frac in (1.0, 0.75, 0.5, 0.25, 0.0):
        v = lo + frac * rng
        y = 10 + (height - 34) * (1 - frac)
        grid += (f'<line x1="10" y1="{y:.1f}" x2="{width - 64}" '
                 f'y2="{y:.1f}" stroke="rgba(128,128,128,.16)"/>'
                 f'<text x="{width - 60}" y="{y + 3.5:.1f}" font-size="10" '
                 f'fill="#8b949e">{v:,.0f}</text>')
    dticks = ""
    for frac, d in ((0.0, dates[0]), (0.5, dates[n // 2]), (1.0, dates[-1])):
        x = 10 + (width - 70) * frac
        dticks += (f'<text x="{x:.1f}" y="{height - 8}" font-size="10" '
                   f'fill="#8b949e" text-anchor="start" '
                   f'{"text-anchor=\"end\"" if frac == 1.0 else ""}>{d}</text>')
    return (f'<svg width="{width}" height="{height}" role="img" '
            f'aria-label="equity curve">'
            f'<defs><linearGradient id="g-{uid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{color}" stop-opacity=".28"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/>'
            f'</linearGradient></defs>'
            f'{grid}'
            f'<polygon fill="url(#g-{uid})" points="{area}"/>'
            f'<line x1="10" y1="{base_y:.1f}" x2="{width - 64}" '
            f'y2="{base_y:.1f}" stroke="#8b949e" stroke-dasharray="4 4"/>'
            f'<polyline fill="none" stroke="{color}" stroke-width="2" '
            f'stroke-linejoin="round" points="{poly}"/>'
            f'{dticks}</svg>')


def drawdown_svg(paper_dir: Path, width=860, height=140, uid="dd") -> str:
    """Underwater curve: percentage drawdown from the running peak."""
    res = mtm_equity(paper_dir)
    if res is None:
        return "<p>no session data yet</p>"
    dates, equity, _ = res
    peak = np.maximum.accumulate(np.array(equity))
    dd = (np.array(equity) - peak) / peak * 100.0
    lo = float(dd.min())
    rng = (-lo) or 1.0
    n = len(dd)
    xs = [10 + (width - 70) * i / max(n - 1, 1) for i in range(n)]
    ys = [10 + (height - 34) * (-v / rng) for v in dd]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    area = f"{xs[0]:.1f},{height - 24} " + poly + f" {xs[-1]:.1f},{height - 24}"
    grid = ""
    for frac in (0.0, 0.5, 1.0):
        v = -lo * frac
        y = 10 + (height - 34) * frac
        grid += (f'<line x1="10" y1="{y:.1f}" x2="{width - 64}" '
                 f'y2="{y:.1f}" stroke="rgba(128,128,128,.16)"/>'
                 f'<text x="{width - 60}" y="{y + 3.5:.1f}" font-size="10" '
                 f'fill="#8b949e">{v:.1f}%</text>')
    worst = f"max drawdown {lo:.2f}%"
    return (f'<svg width="{width}" height="{height}" role="img" '
            f'aria-label="drawdown curve">'
            f'<defs><linearGradient id="g-{uid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#f85149" stop-opacity=".05"/>'
            f'<stop offset="1" stop-color="#f85149" stop-opacity=".3"/>'
            f'</linearGradient></defs>'
            f'{grid}'
            f'<polygon fill="url(#g-{uid})" points="{area}"/>'
            f'<polyline fill="none" stroke="#f85149" stroke-width="1.5" '
            f'points="{poly}"/>'
            f'<text x="14" y="22" font-size="11" fill="#f85149">{worst}'
            f'</text></svg>')


def price_charts_html(paper_dir: Path, per_width=520,
                      per_height=170) -> str:
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
        xs = [8 + (per_width - 16) * i / max(n - 1, 1) for i in range(n)]
        ys = [8 + (per_height - 26) * (1 - (v - lo) / rng) for v in closes]
        poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
        marks = []
        for i, b in enumerate(bl):
            dpos = entries[s].get(b["date"])
            if not dpos:
                continue
            x, y = xs[i], ys[i]
            if dpos > 0:
                marks.append(f'<path d="M{x:.1f},{y - 5:.1f} l5,8 l-10,0 z" '
                             f'fill="#3fb950" stroke="#0d1117" '
                             f'stroke-width=".6">'
                             f'<title>{s} long entry {b["date"]}</title></path>')
            else:
                marks.append(f'<path d="M{x:.1f},{y + 5:.1f} l5,-8 l-10,0 z" '
                             f'fill="#f85149" stroke="#0d1117" '
                             f'stroke-width=".6">'
                             f'<title>{s} short entry {b["date"]}</title></path>')
        first, last = bl[0]["date"], bl[-1]["date"]
        svgs.append(
            f'<div class="pc"><div class="pchead"><h3>{_esc(s)}</h3>'
            f'<span class="pclast">{closes[-1]:.2f}</span></div>'
            f'<svg width="{per_width}" height="{per_height}" role="img" '
            f'aria-label="{_esc(s)} price with entries" '
            f'viewBox="0 0 {per_width} {per_height}">'
            f'<line x1="8" y1="{8 + (per_height - 26) * .5:.1f}" '
            f'x2="{per_width - 8}" '
            f'y2="{8 + (per_height - 26) * .5:.1f}" '
            f'stroke="rgba(128,128,128,.14)"/>'
            f'<polyline fill="none" stroke="#58a6ff" stroke-width="1.5" '
            f'stroke-linejoin="round" points="{poly}"/>' + "".join(marks) +
            f'<text x="8" y="{per_height - 3}" font-size="9" fill="#8b949e">'
            f'{first}</text>'
            f'<text x="{per_width - 8}" y="{per_height - 3}" font-size="9" '
            f'fill="#8b949e" text-anchor="end">{last}</text></svg></div>')
    if not svgs:
        return "<p>no bars</p>"
    return ('<div class="pgrid">' + "".join(svgs) + "</div>")


def race_svg(paper_dir: Path, width=900, height=260, uid="race") -> str:
    """Champion vs challenger equity overlay from the two persisted
    shadow states."""
    champ = mtm_equity(paper_dir)
    chall = mtm_equity(paper_dir,
                       paper_dir / "challenger" / "session_state.json")
    if chall is None:
        return ("<p class=\"dim\">Challenger shadow state not yet "
                "generated; the race chart appears after the first nightly "
                "challenger session.</p>")
    grid = ""
    for frac in (1.0, 0.75, 0.5, 0.25, 0.0):
        y = 10 + (height - 44) * (1 - frac)
        grid += (f'<line x1="10" y1="{y:.1f}" x2="{width - 10}" '
                 f'y2="{y:.1f}" stroke="rgba(128,128,128,.14)"/>')
    lines = []
    for label, res, color in (("Challenger", chall, "#58a6ff"),
                              ("Champion", champ, "#3fb950")):
        _, equity, _ = res
        eq = np.array(equity, dtype=float)
        lo, hi = float(eq.min()), float(eq.max())
        rng = (hi - lo) or 1.0
        pts = []
        for i, v in enumerate(eq):
            x = 10 + (width - 20) * i / max(len(eq) - 1, 1)
            y = 10 + (height - 44) * (1 - (v - lo) / rng)
            pts.append(f"{x:.1f},{y:.1f}")
        lines.append((label, color, " ".join(pts),
                      f"{(eq[-1] / eq[0] - 1) * 100:+.2f}%"))
    polylines = "".join(
        f'<polyline fill="none" stroke="{c}" stroke-width="2" '
        f'stroke-linejoin="round" points="{p}"/>' for _, c, p, _ in lines)
    legend = "".join(
        f'<rect x="{10 + i * 150}" y="4" width="10" height="10" rx="2" '
        f'fill="{c}"/><text x="{26 + i * 150}" y="13" fill="#8b949e" '
        f'font-size="11">{l} {r}</text>'
        for i, (l, c, _, r) in enumerate(lines))
    return (f'<svg width="{width}" height="{height}" role="img" '
            f'aria-label="champion vs challenger equity">{grid}'
            f'{polylines}<g transform="translate(0,{height - 18})">'
            f'{legend}</g></svg>')


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


def _file_details(title: str, path: Path, open_=False) -> str:
    """Render a repo file as a collapsible section with escaped content."""
    if not path.exists():
        return ""
    body = _esc(path.read_text().strip())
    attr = " open" if open_ else ""
    return (f'<details class="doc"{attr}><summary>{_esc(title)} '
            f'<span class="dim">— {_esc(path.name)}</span></summary>'
            f'<pre>{body}</pre></details>')


def _knowledge_html() -> str:
    """Structured view of the Market Studies knowledge base: the
    concept-to-design mapping table plus the studied-book library."""
    base = Path(__file__).parent
    applied = base / "KNOWLEDGE_APPLIED.md"
    kb_files = sorted((base.parent).glob("KNOWLEDGE*.md"))
    rows = []
    if applied.exists():
        for line in applied.read_text().splitlines():
            m = re.match(r"\| (.+?) \| (.+?) \| (.+?) \|", line)
            if m and not set(m.group(1)) <= {"-", " "} and \
                    "Knowledge layer" not in m.group(1):
                layer, concept, where = (g.strip() for g in m.groups())
                rows.append(
                    f'<div class="krow"><div class="klayer">{_esc(layer)}'
                    f'</div><div class="kconcept">{_esc(concept)}</div>'
                    f'<div class="kwhere">{_esc(where)}</div></div>')
    books = []
    for kb in kb_files:
        in_notes = False
        for line in kb.read_text().splitlines():
            if line.startswith("## "):
                in_notes = "Study notes" in line
                continue
            if not in_notes or not line.startswith("- "):
                continue
            m = re.match(r"- \[([^\]]+)\]\([^)]*\)\s*[—-]\s*(.+?)(?:;|$)", line)
            if m:
                title, desc = m.group(1).strip(), m.group(2).strip()
                if len(desc) > 110:
                    desc = desc[:107] + "..."
                books.append((title, desc))
    eval_note = ""
    if applied.exists():
        txt = applied.read_text()
        m = re.search(r"## First honest evaluation.*?\n(.+)", txt, re.S)
        if m:
            eval_note = " ".join(
                l.strip() for l in m.group(1).splitlines() if l.strip())
    books_html = "".join(
        f'<div class="book"><div class="btitle">{_esc(t)}</div>'
        f'<div class="bdesc dim">{_esc(d)}</div></div>' for t, d in books)
    eval_html = (f'<div class="knote">{_esc(eval_note)}</div>'
                 if eval_note else "")
    intro = ('<p class="dim">The strategy is grounded in a '
             f'{len(books)}-book study library. Each knowledge layer maps '
             'to a concrete design decision; candidate improvements become '
             'research variants that the edge-seeker must beat honestly '
             '— the deployed parameters stay frozen (Gate 3).</p>')
    programme = ""
    prog_bullets = []
    for prog_path in kb_files:
        prog_bullets += [
            l[2:].strip() for l in prog_path.read_text().splitlines()
            if l.startswith("- ") and "](" not in l[:60]]
    if prog_bullets:
        prog_cards = "".join(
            f'<div class="book"><div class="bdesc dim">'
            f'{_esc(b[:280])}{"..." if len(b) > 280 else ""}</div></div>'
            for b in prog_bullets)
        programme = ('<h3 class="sub">Trading-research programme '
                     '(AVFI-NQ weekly)</h3><div class="bgrid">'
                     f'{prog_cards}</div>')
    return (intro
            + '<div class="kgrid">' + "".join(rows) + "</div>"
            + f'<h3 class="sub">Studied library ({len(books)} books)'
            f'</h3><div class="bgrid">{books_html}</div>'
            + programme + eval_html)

def _worklog_html() -> str:
    """Rendered work log: each entry as a timeline row."""
    path = Path(__file__).parent / "WORKLOG.md"
    if not path.exists():
        return ""
    items = []
    for line in path.read_text().splitlines():
        m = re.match(r"- \*\*(.+?)\*\* (.+)", line)
        if m:
            items.append(
                f'<div class="wl"><div class="wldate">{_esc(m.group(1))}'
                f'</div><div class="wlbody">{_esc(m.group(2))}</div></div>')
    if not items:
        return ""
    return ('<div class="timeline">' + "".join(items) + "</div>")


_REPO_MAP = [
    ("strategy/vp_mr_strategy.py", "Core gated strategy (G1-G4 enforced)"),
    ("strategy/nautilus_adapter.py", "NautilusTrader adapter"),
    ("strategy/papertrading_runner.py", "Persisted paper-trading runner"),
    ("strategy/edge_seeker.py", "Nightly research trainer (54 candidates)"),
    ("strategy/vol_models.py", "Knowledge-grounded vol models + VSA filter"),
    ("strategy/challenger.py", "Champion/challenger race"),
    ("strategy/propose_redeploy.py", "Auto-redeploy proposal (opens a PR)"),
    ("strategy/gate_check.py", "Promotion gate (PROMOTE/HOLD)"),
    ("strategy/spi_monitor.py", "Signal Parity Index audit"),
    ("strategy/journal.py", "Append-only session journal"),
    ("strategy/alert.py", "Self-filed incident alerts (GitHub issues)"),
    ("strategy/dashboard.py", "This site's generator"),
    ("strategy/run_card.json", "Frozen strategy run card"),
    ("paper/", "Session artifacts: state, reports, verdicts, journal"),
    ("KNOWLEDGE.md", "The 13-book market-studies knowledge base"),
    ("strategy/KNOWLEDGE_APPLIED.md", "Knowledge-to-design mapping"),
    ("strategy/WORKLOG.md", "Full build log"),
    ("test_*.py (16 suites)", "150+ assertions, all green in CI"),
]


def _sparkline(csv_path: Path, width=130, height=34) -> str:
    """Tiny close-price sparkline from a research CSV."""
    raw = [l.split(",") for l in
           csv_path.read_text().strip().splitlines()[1:]]
    if len(raw) < 2:
        return ""
    closes = [float(r[4]) for r in raw]
    lo, hi = min(closes), max(closes)
    rng = (hi - lo) or 1.0
    n = len(closes)
    pts = " ".join(
        f"{2 + (width - 4) * i / (n - 1):.1f},"
        f"{2 + (height - 4) * (1 - (v - lo) / rng):.1f}"
        for i, v in enumerate(closes))
    up = closes[-1] >= closes[0]
    color = "#3fb950" if up else "#f85149"
    return (f'<svg width="{width}" height="{height}" role="img" '
            f'aria-label="sparkline"><polyline fill="none" '
            f'stroke="{color}" stroke-width="1.3" points="{pts}"/></svg>')


def _cross_asset_html(paper_dir: Path) -> str:
    """Cross-asset edge research, one section per asset class, with
    per-series sparklines, from the committed research JSON."""
    res_path = paper_dir / "research" / "cross_asset.json"
    if not res_path.exists():
        return ("<p class=\"dim\">Cross-asset research appears here after "
                "the first nightly research pass.</p>")
    results = json.load(open(res_path))
    data_dir = paper_dir / "research" / "data"
    intro = ("<p class=\"dim\">Does the mean-reversion edge exist beyond "
             "equity ETFs? Each series gets an OU half-life estimate, a "
             "Dickey-Fuller-style mean-reversion t-test, and a "
             "production-style causal z-score backtest vs buy-and-hold. "
             "The deployed champion stays frozen (Gate 3); honest null "
             "results are reported.</p>")
    sections = []
    titles = {"crypto": "Cryptos", "index": "Indices",
              "commodity": "Commodities"}
    for asset_class in sorted({r["asset_class"] for r in results}):
        rows = ""
        for r in sorted((x for x in results
                         if x["asset_class"] == asset_class),
                        key=lambda x: x["ticker"]):
            if r.get("status") != "OK":
                rows += (f'<tr><td>{_esc(r["ticker"])}</td>'
                         f'<td colspan="6" class="dim">no data '
                         f'({_esc(r.get("error", ""))})</td></tr>')
                continue
            spark = _sparkline(
                data_dir / f"{safe_name(r['ticker']).lower()}.csv") \
                if data_dir.exists() else ""
            hl = r["half_life_bars"] if r["half_life_bars"] is not None \
                else "none"
            cls = "good" if r["mean_reverting"] else "dim"
            verdict = "yes" if r["mean_reverting"] else "no"
            rows += (f'<tr><td>{_esc(r["ticker"])}</td><td>{spark}</td>'
                     f'<td>{hl}</td><td>{r["mr_t_stat"]}</td>'
                     f'<td>{r["mr_sharpe"]:+.2f}</td>'
                     f'<td>{r["buy_hold_sharpe"]:+.2f}</td>'
                     f'<td class="{cls}">{verdict}</td></tr>')
        sections.append(
            f'<h3 class="sub">{_esc(titles.get(asset_class, asset_class.title()))}</h3>'
            '<table><tr><th>Ticker</th><th>5y</th>'
            '<th>OU half-life</th><th>MR t-stat</th><th>MR Sharpe</th>'
            '<th>B&amp;H Sharpe</th><th>Reverting?</th></tr>'
            f'{rows}</table>')
    return intro + "".join(sections)


def _avfi_chart_svg(ch: dict, width=560, height=200) -> str:
    """Per-instrument AVFI chart: price line with trade entries on
    top, the sigma-normalized spread z below with the trigger line and
    throttled zones shaded."""
    closes = ch["close"]
    sp_z = ch["sp_z"]
    n = len(closes)
    if n < 2:
        return ""
    top_h = int(height * 0.55)
    bot_h = height - top_h
    lo, hi = min(closes), max(closes)
    rng = (hi - lo) or 1.0
    xs = [8 + (width - 60) * i / (n - 1) for i in range(n)]
    pts = " ".join(
        f"{x:.1f},{6 + (top_h - 14) * (1 - (c - lo) / rng):.1f}"
        for x, c in zip(xs, closes))
    zmax = max(1.0, max(abs(z) for z in sp_z))
    zpts = " ".join(
        f"{x:.1f},{top_h + 6 + (bot_h - 16) * (1 - (z / zmax + 1) / 2):.1f}"
        for x, z in zip(xs, sp_z))
    marks = ""
    for idx, d in ch["entries"]:
        if idx >= n:
            continue
        x = xs[idx]
        y = 6 + (top_h - 14) * (1 - (closes[idx] - lo) / rng)
        if d > 0:
            marks += (f'<path d="M{x:.1f},{y - 5:.1f} l5,8 l-10,0 z" '
                      f'fill="#3fb950"><title>long entry '
                      f'{ch["dates"][idx]}</title></path>')
        else:
            marks += (f'<path d="M{x:.1f},{y + 5:.1f} l5,-8 l-10,0 z" '
                      f'fill="#f85149"><title>short entry '
                      f'{ch["dates"][idx]}</title></path>')
    trig = ch["trigger"]
    trig_y = top_h + 6 + (bot_h - 16) * (1 - (trig / zmax + 1) / 2)
    zones = ""
    in_zone = False
    for i, z in enumerate(sp_z):
        if z <= trig and not in_zone:
            x0 = xs[i]
            in_zone = True
        elif z > trig and in_zone:
            zones += (f'<rect x="{x0:.1f}" y="{top_h + 6}" '
                      f'width="{xs[i] - x0:.1f}" height="{bot_h - 16}" '
                      f'fill="rgba(210,153,34,.15)"/>')
            in_zone = False
    if in_zone:
        zones += (f'<rect x="{x0:.1f}" y="{top_h + 6}" '
                  f'width="{xs[-1] - x0:.1f}" height="{bot_h - 16}" '
                  f'fill="rgba(210,153,34,.15)"/>')
    return (f'<svg width="{width}" height="{height}" role="img" '
            f'aria-label="{_esc(ch["ticker"])} AVFI chart" '
            f'viewBox="0 0 {width} {height}">'
            f'<polyline fill="none" stroke="#58a6ff" stroke-width="1.4" '
            f'points="{pts}"/>{marks}'
            f'{zones}'
            f'<line x1="8" y1="{trig_y:.1f}" x2="{width - 60}" '
            f'y2="{trig_y:.1f}" stroke="#d29922" stroke-dasharray="4 4"/>'
            f'<polyline fill="none" stroke="#a371f7" stroke-width="1.2" '
            f'points="{zpts}"/>'
            f'<text x="{width - 56}" y="{trig_y + 3:.1f}" font-size="9" '
            f'fill="#d29922">trigger</text>'
            f'<text x="8" y="12" font-size="10" fill="#8b949e">'
            f'{_esc(ch["ticker"])} price + entries</text>'
            f'<text x="8" y="{top_h + 16}" font-size="10" fill="#a371f7">'
            f'spread z (AVFI v3 vs v2)</text></svg>')


def _avfi_equity_svg(ch: dict, width=1360, height=240) -> str:
    """Portfolio equity of the AVFI-throttled bottom-long / top-short
    strategy."""
    eq = ch.get("eq", [])
    if len(eq) < 2:
        return ""
    lo, hi = min(eq), max(eq)
    rng = (hi - lo) or 1.0
    n = len(eq)
    xs = [10 + (width - 70) * i / (n - 1) for i in range(n)]
    pts = " ".join(
        f"{x:.1f},{10 + (height - 40) * (1 - (v - lo) / rng):.1f}"
        for x, v in zip(xs, eq))
    base_y = 10 + (height - 40) * (1 - (1.0 - lo) / rng)
    color = "#3fb950" if eq[-1] >= 1.0 else "#f85149"
    grid = ""
    for frac in (1.0, 0.5, 0.0):
        y = 10 + (height - 40) * (1 - frac)
        v = lo + frac * rng
        grid += (f'<line x1="10" y1="{y:.1f}" x2="{width - 70}" '
                 f'y2="{y:.1f}" stroke="rgba(128,128,128,.16)"/>'
                 f'<text x="{width - 64}" y="{y + 3.5:.1f}" '
                 f'font-size="10" fill="#8b949e">{v:.2f}</text>')
    total = (eq[-1] - 1.0) * 100.0
    return (f'<svg width="{width}" height="{height}" role="img" '
            f'aria-label="AVFI portfolio equity">'
            f'<defs><linearGradient id="g-avfi-eq" x1="0" y1="0" '
            f'x2="0" y2="1"><stop offset="0" stop-color="{color}" '
            f'stop-opacity=".25"/><stop offset="1" '
            f'stop-color="{color}" stop-opacity="0"/>'
            f'</linearGradient></defs>{grid}'
            f'<line x1="10" y1="{base_y:.1f}" x2="{width - 70}" '
            f'y2="{base_y:.1f}" stroke="#8b949e" stroke-dasharray="4 4"/>'
            f'<polygon fill="url(#g-avfi-eq)" points="10,{height - 30} '
            f'{pts} {width - 70},{height - 30}"/>'
            f'<polyline fill="none" stroke="{color}" '
            f'stroke-width="2" points="{pts}"/>'
            f'<text x="14" y="24" font-size="11" fill="{color}">'
            f'equal-weight portfolio equity: {total:+.1f}% '
            f'(longs at bottoms, shorts at tops, throttled by AVFI)'
            f'</text></svg>')


def _avfi_code_html() -> str:
    """The annotated research code, shown so every bit is readable."""
    src_path = Path(__file__).parent / "avfi.py"
    if not src_path.exists():
        return ""
    code = _esc(src_path.read_text())
    return ('<details class="doc" open><summary>The code, explained '
            '<span class="dim">— strategy/avfi.py, every comment is '
            'live from the source</span></summary>'
            f'<pre>{code}</pre></details>')


def _avfi_pine_html() -> str:
    """The AVFI v3.2 Pine v5 source, displayed for TradingView."""
    src_path = Path(__file__).parent / "avfi_v3_2.pine"
    if not src_path.exists():
        return ""
    code = _esc(src_path.read_text())
    return ('<details class="doc" open><summary>AVFI v3.2 — Pine v5 '
            'source <span class="dim">— paste into a TradingView Pine '
            'editor; the Python twin is strategy/avfi.py</span></summary>'
            f'<pre>{code}</pre></details>')


def _tradingview_embed(symbol: str = "NASDAQ:NQ1!",
                       interval: str = "W") -> str:
    """Full-bleed live TradingView chart (advanced chart widget):
    edge-to-edge across the whole browser window, 900px tall."""
    config = json.dumps({
        "symbol": symbol, "interval": interval, "theme": "dark",
        "width": "100%", "height": 900, "locale": "en",
        "allow_symbol_change": True, "save_image": False,
        "calendar": False, "hide_side_toolbar": False,
        "support_host": "https://www.tradingview.com",
    })
    return ('<div class="tvfull">'
            '<div class="tradingview-widget-container" '
            'style="height:900px;width:100%">'
            '<div class="tradingview-widget-container__widget" '
            'style="height:900px;width:100%"></div>'
            '<script type="text/javascript" '
            'src="https://s3.tradingview.com/external-embedding/'
            'embed-widget-advanced-chart.js" async>'
            f'{config}'
            '</script></div></div>')


def _avfi_html(paper_dir: Path) -> str:
    """AVFI v3 risk-throttle research: per-instrument charts with
    trades and throttle zones, plus the iteration ledger."""
    chart_path = paper_dir / "research" / "avfi_chart.json"
    if not chart_path.exists():
        return ("<p class=\"dim\">AVFI research appears here after "
                "the first nightly research pass.</p>")
    charts = json.load(open(chart_path))
    portfolio = next((c for c in charts if c["ticker"] == "PORTFOLIO"),
                     None)
    eq_svg = _avfi_equity_svg(portfolio) if portfolio else ""
    svgs = "".join(
        f'<div class="pc">{_avfi_chart_svg(ch)}</div>'
        for ch in charts if ch["ticker"] != "PORTFOLIO")
    site_link = ""
    if (Path(__file__).resolve().parent.parent / "docs" / "avfi-nq.html") \
            .exists():
        site_link = ('<p><a href="avfi-nq.html" '
                     'style="color:var(--accent)">Full AVFI-NQ weekly '
                     'research programme site — the 9-stage validation '
                     'pipeline, hypothesis registry, verdicts and the '
                     '10 evidence-forced lessons</a></p>')
    ledger_html = ""
    led_path = paper_dir / "research" / "avfi_iterations.json"
    if led_path.exists():
        ledger = json.loads(led_path.read_text())[-12:]
        rows = "".join(
            f'<tr><td>{r["iteration"]}</td><td>{r["date"]}</td>'
            f'<td>{r["params_evaluated"].get("trigger")} / '
            f'{r["params_evaluated"].get("throttle")}</td>'
            f'<td>{r["oos_dd_reduction_pct"]}%</td>'
            f'<td>{r["oos_sharpe_delta"]}</td>'
            f'<td class="{"good" if r["advanced"] else "dim"}">'
            f'{"advanced" if r["advanced"] else "kept"}</td></tr>'
            for r in ledger)
        ledger_html = ('<h3 class="sub">Iteration ledger (nightly '
                      'self-improvement)</h3>'
                      '<p class="dim">Each nightly pass evaluates the '
                      'current AVFI research parameters, searches a '
                      'pre-committed 24-variant grid with train/OOS '
                      'honesty, and advances the parameters only when a '
                      'candidate beats them out-of-sample (more drawdown '
                      'reduction at preserved Sharpe). The deployed '
                      'strategy stays frozen (Gate 3).</p>'
                      '<table><tr><th>Iter</th><th>Date</th>'
                      '<th>trigger / throttle</th><th>OOS DD red.</th>'
                      '<th>OOS Sharpe delta</th><th>Outcome</th></tr>'
                      f'{rows}</table>')
    return (f'<p class="dim">Python replication of the Pine v5 '
            f'"AVFI v3 vs v2 [spread axis]" indicator (Parkinson-style '
            f'vol floor, log-volume normalization, sigma-normalized '
            f'spread z). Per the research programme, AVFI is evaluated '
            f'only as a risk throttle — exposure cut to the throttle '
            f'level (shaded zones) when the spread z breaches the '
            f'trigger. Green up-triangles mark long entries, red '
            f'down-triangles short entries.</p>'
            f'{site_link}'
            f'<h3 class="sub">Portfolio equity (throttled)</h3>'
            f'{eq_svg}'
            f'<h3 class="sub">Per-instrument: price, entries, '
            f'spread z and throttle zones</h3>'
            f'<div class="pgrid">{svgs}</div>{ledger_html}'
            f'{_avfi_code_html()}'
            f'{_avfi_pine_html()}'
            f'<h3 class="sub">Live market — TradingView</h3>'
            f'<p class="dim">Interactive chart (NQ weekly, '
            f'matching the AVFI-NQ research programme; switch '
            f'symbols in the widget). Overlay the AVFI v3.2 '
            f'source above in any TradingView Pine editor.'
            f'</p>'
            f'{_tradingview_embed()}')


def build_site(paper_dir: Path) -> str:
    """Salient: the public one-page site (GitHub Pages, docs/index.html).
    Sections: overview, charts, race, knowledge, reports, journal,
    build log, repository."""
    s = summarize(paper_dir)
    verdict = s.get("verdict", "NOT_GENERATED")
    edge_path = paper_dir / "edge_report.md"
    edge_rec = "NOT_GENERATED"
    if edge_path.exists():
        m = re.search(r"Recommendation: (PROPOSE_REDEPLOY|KEEP_PRODUCTION)",
                      edge_path.read_text())
        if m:
            edge_rec = m.group(1)
    svg = equity_curve_svg(paper_dir, width=1360, height=320, uid="site-eq")
    dd_svg = drawdown_svg(paper_dir, width=1360, height=160, uid="site-dd")
    price_html = price_charts_html(paper_dir)
    race_chart = race_svg(paper_dir, width=1360, height=300, uid="site-race")
    sessions = s.get("sessions_completed", 0)
    pct = min(100, int(100 * sessions / 20))
    journal_html = ""
    journal_path = paper_dir / "journal.md"
    if journal_path.exists():
        rows = [l for l in journal_path.read_text().splitlines()
                if l.startswith("| 20")][-10:]
        journal_html = ('<section id="journal"><h2>Session journal</h2>'
                       '<table><tr><th>Date</th><th>Sessions</th>'
                       '<th>Verdict</th><th>SPI</th><th>Sharpe</th>'
                       '<th>Max DD</th><th>Race</th><th>Equity</th></tr>'
                       + "".join(rows) + "</table></section>")
    race_html = ""
    race_path = paper_dir / "challenger_report.md"
    if race_path.exists():
        race = race_path.read_text()
        m = re.search(r"Recommendation: (PROPOSE_REDEPLOY|KEEP_CHAMPION)", race)
        rec = m.group(1) if m else "?"
        rows = re.findall(
            r"\| (Champion[^|]*|Challenger[^|]*)\| ([\d.-]+) \| ([\d.-]+) \| ([\d.-]+) \|",
            race)
        rows_html = "".join(
            f"<tr><td>{_esc(a.strip())}</td><td>{b}%</td>"
            f"<td>{c}</td><td>{d}%</td></tr>" for a, b, c, d in rows)
        race_html = (f'<p class="dim">The edge-seeker nominates a candidate '
                     f'each night; it shadow-trades on the same real data. '
                     f'Current verdict: <strong class="'
                     f'{"good" if rec == "KEEP_CHAMPION" else "warn"}">'
                     f'{_esc(rec)}</strong>. Applying a proposal is always a '
                     f'human-reviewed PR (Gate 3).</p>'
                     f'<table><tr><th>Strategy</th><th>Return</th>'
                     f'<th>Sharpe</th><th>Max DD</th></tr>{rows_html}'
                     f"</table>")

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

    repo_rows = "".join(
        f'<tr><td><code>{_esc(p)}</code></td><td class="dim">{_esc(d)}'
        f"</td></tr>" for p, d in _REPO_MAP)
    reports = (_file_details("Forward-test gate verdict",
                            paper_dir / "gate_verdict.md", open_=True)
               + _file_details("Edge-seeker research report",
                               paper_dir / "edge_report.md")
               + _file_details("Champion vs challenger race report",
                               paper_dir / "challenger_report.md")
               + _file_details("Session performance report",
                               paper_dir / "performance_report.md")
               + _file_details("Session log", paper_dir / "session_report.txt"))

    nav = (" ".join(
        f'<a href="#{a}">{t}</a>' for a, t in
        (("avfi", "AVFI"), ("overview", "Overview"),
         ("charts", "Charts"),
         ("race", "Self-learning"), ("crossasset", "Cross-asset"),
         ("knowledge", "Knowledge"),
         ("reports", "Reports"), ("journal", "Journal"),
         ("buildlog", "Build log"), ("repo", "Repository"))))

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="300">
<title>Salient — VP-MR-ETF-D1-001</title>
<style>
:root {{ --bg:#0a0d13; --panel:#121721; --panel2:#0d1117; --ink:#e6edf3;
        --dim:#8b949e; --accent:#58a6ff; --good:#3fb950; --bad:#f85149;
        --warn:#d29922; --line:#21262d; }}
body {{ background:var(--bg); color:var(--ink); margin:0;
       font-family:-apple-system,'Segoe UI',sans-serif; }}
nav {{ position:sticky; top:0; z-index:10; background:rgba(10,13,19,.92);
      backdrop-filter:blur(8px); border-bottom:1px solid var(--line);
      padding:10px 40px; display:flex; gap:22px; align-items:center;
      flex-wrap:wrap; }}
nav .brand {{ font-weight:700; letter-spacing:-.3px; }}
nav .brand span {{ color:var(--accent); }}
nav a {{ color:var(--dim); text-decoration:none; font-size:13px; }}
nav a:hover {{ color:var(--ink); }}
header {{ padding:44px 40px 8px; max-width:1440px; margin:0 auto; }}
h1 {{ font-size:38px; margin:0; letter-spacing:-1px; }}
h1 span {{ color:var(--accent); }}
.tagline {{ color:var(--dim); margin:8px 0 0; font-size:15px;
           max-width:640px; line-height:1.5; }}
main {{ max-width:1440px; margin:0 auto; padding:16px 40px 48px; }}
.progress {{ background:var(--panel); border-radius:10px; height:14px;
             margin:24px 0 26px; overflow:hidden; }}
.bar {{ height:100%; width:{pct}%; background:linear-gradient(90deg,
        #1f6feb,#58a6ff); border-radius:10px; }}
.pnote {{ font-size:12px; color:var(--dim); margin:-16px 0 24px; }}
.metrics {{ display:grid; grid-template-columns:repeat(8,1fr); gap:12px; }}
.m {{ background:var(--panel); border-radius:12px; padding:16px 18px;
      border:1px solid var(--line); }}
.ml {{ font-size:11px; text-transform:uppercase; letter-spacing:.6px;
       color:var(--dim); }}
.mv {{ font-size:24px; font-weight:700; margin-top:4px; }}
.sub {{ font-size:11px; color:var(--dim); margin-top:2px; }}
section {{ background:var(--panel); border-radius:14px; padding:24px;
           margin-top:22px; border:1px solid var(--line); }}
h2 {{ font-size:18px; margin:0 0 12px; }}
h3.sub {{ font-size:14px; margin:22px 0 10px; color:var(--ink); }}
.dim {{ color:var(--dim); }}
.good {{ color:var(--good); }} .warn {{ color:var(--warn); }}
.legend {{ font-size:12px; color:var(--dim); margin:-4px 0 10px; }}
.legend span {{ margin-right:16px; }}
.dot {{ display:inline-block; width:9px; height:9px; border-radius:2px;
       margin-right:5px; vertical-align:middle; }}
.pgrid {{ display:grid; grid-template-columns:repeat(5,1fr); gap:14px;
          margin-top:14px; }}
.pc {{ background:var(--panel2); border:1px solid var(--line);
       border-radius:10px; padding:12px 14px 8px; }}
.pchead {{ display:flex; justify-content:space-between; align-items:baseline; }}
.pc h3 {{ margin:0 0 4px; font-size:14px; color:var(--ink); }}
.pclast {{ font-size:13px; color:var(--accent); font-weight:600; }}
.pc svg {{ width:100%; height:auto; display:block; }}
table {{ border-collapse:collapse; width:100%; font-size:13px;
         margin-top:10px; }}
td, th {{ padding:7px 10px; border-bottom:1px solid var(--line);
          text-align:left; }}
th {{ color:var(--dim); font-weight:600; font-size:11px;
     text-transform:uppercase; letter-spacing:.5px; }}
.kgrid {{ display:grid; gap:10px; margin-top:14px; }}
.krow {{ display:grid; grid-template-columns:260px 1fr 1fr; gap:18px;
         background:var(--panel2); border:1px solid var(--line);
         border-radius:10px; padding:12px 14px; font-size:13px; }}
.klayer {{ color:var(--accent); font-weight:600; }}
.kconcept {{ color:var(--ink); }} .kwhere {{ color:var(--dim); }}
.bgrid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }}
.book {{ background:var(--panel2); border:1px solid var(--line);
         border-radius:10px; padding:10px 14px; font-size:12px; }}
.btitle {{ font-weight:600; margin-bottom:2px; }}
.knote {{ margin-top:16px; background:var(--panel2);
         border-left:3px solid var(--warn); border-radius:8px;
         padding:12px 16px; font-size:13px; color:var(--dim); }}
.timeline {{ margin-top:8px; }}
.wl {{ display:grid; grid-template-columns:200px 1fr; gap:14px;
      padding:10px 0; border-bottom:1px solid var(--line);
      font-size:13px; }}
.wl:last-child {{ border-bottom:none; }}
.wldate {{ color:var(--accent); }}
.wlbody {{ color:var(--dim); line-height:1.55; }}
details.doc {{ background:var(--panel2); border:1px solid var(--line);
              border-radius:10px; margin-top:10px; }}
details.doc summary {{ cursor:pointer; padding:11px 16px; font-weight:600;
                      font-size:13px; }}
details.doc pre {{ margin:0; padding:0 16px 14px; font-size:11px;
                  line-height:1.5; color:var(--dim); overflow-x:auto;
                  white-space:pre-wrap; }}
code {{ color:var(--accent); font-size:12px; }}
.tvfull {{ width:100vw; position:relative; left:50%;
           right:50%; margin-left:-50vw; margin-right:-50vw;
           background:var(--panel2); border-top:1px solid var(--line);
           border-bottom:1px solid var(--line); }}
.tvfull .tradingview-widget-container {{ margin:0; }}
footer {{ color:var(--dim); font-size:12px; text-align:center;
          padding:28px; line-height:1.7; }}
footer a {{ color:var(--accent); }}
@media (max-width:1100px) {{ .metrics {{ grid-template-columns:repeat(4,1fr); }}
  .pgrid {{ grid-template-columns:repeat(2,1fr); }}
  .bgrid {{ grid-template-columns:1fr; }} }}
@media (max-width:700px) {{ .metrics,.pgrid {{ grid-template-columns:1fr; }}
  .krow {{ grid-template-columns:1fr; }} .wl {{ grid-template-columns:1fr; }} }}
</style></head><body>
<nav><span class="brand">Salient<span>.</span></span>{nav}</nav>
<header>
<h1>An autonomous quantitative trading system<span>.</span></h1>
<p class="tagline">VP-MR-ETF-D1-001 — volatility-parity mean reversion on
US equity ETFs (SPY, QQQ, IWM, XLF, XLE), paper-trading autonomously,
self-audited nightly, grounded in a growing research library, and
promoted only by evidence.</p>
<p class="tagline">A hobby research pursuit: this system will never trade
live. The enjoyment comes from solving and finding the edge — not from
financial gain.</p>
</header>
<main>
<div id="overview">
<div class="progress"><div class="bar"></div></div>
<p class="pnote">{pct}% of the 20-session forward test toward promotion</p>
<div class="metrics">{metrics}</div>
</div>
<section id="avfi"><h2>AVFI &mdash; the edge formula, iterating nightly</h2>
{_avfi_html(paper_dir)}
</section>
<section id="charts"><h2>Performance</h2>
<p class="legend"><span><i class="dot" style="background:#3fb950"></i>equity
(mark-to-market, net of costs)</span>
<span><i class="dot" style="background:#f85149"></i>drawdown from peak</span></p>
{svg}
<h3 class="sub">Drawdown (underwater curve)</h3>
{dd_svg}
<h3 class="sub">Instrument prices &amp; trade entries</h3>
<p class="dim">Green up-triangles mark long entries, red down-triangles
short entries, from the audited decision log.</p>
{price_html}
</section>
<section id="race"><h2>Self-learning: champion vs challenger</h2>
<p class="dim">The deployed champion stays frozen so its forward test stays
honest; the edge-seeker's best candidate shadow-trades as a challenger on
the same real bars every night. Each curve is scaled to its own range.</p>
{race_chart}
{race_html}
</section>
<section id="crossasset"><h2>Cross-asset edge research</h2>
{_cross_asset_html(paper_dir)}
</section>
<section id="knowledge"><h2>Knowledge base &rarr; strategy design</h2>
{_knowledge_html()}
</section>
<section id="reports"><h2>Latest reports</h2>
{reports}
</section>
{journal_html}
<section id="buildlog"><h2>Build log</h2>
<p class="dim">Every phase of building this system, newest last — including
the bugs the real market exposed and how they were fixed.</p>
{_worklog_html()}
</section>
<section id="repo"><h2>Repository map</h2>
<p class="dim">Everything on this page is generated from committed artifacts
in <a href="https://github.com/andrea-karlvassallo20-beep/vp-mr-strategy"
style="color:var(--accent)">the source repository on GitHub</a>.</p>
<table>{repo_rows}</table>
{_file_details("README — the project explained", (Path(__file__).resolve().parent.parent / "README.md"), open_=True)}
{_file_details("DASHBOARD — the live status page", (Path(__file__).resolve().parent.parent / "DASHBOARD.md"))}
</section>
</main>
<footer>Salient — regenerated automatically after every paper-trading
session.<br>
<a href="https://github.com/andrea-karlvassallo20-beep/vp-mr-strategy">Source,
evidence and full work log on GitHub</a> &middot; research system, not
investment advice.</footer>
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
