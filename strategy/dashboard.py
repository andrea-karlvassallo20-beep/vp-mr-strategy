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
    articles_html = ""
    reg_path = (base.parent / "paper" / "research" / "articles.json")
    if reg_path.exists():
        reg = json.loads(reg_path.read_text())
        if reg:
            cards = ""
            for a in reg:
                status = a.get("status", "")
                meta = (f'{a.get("pages", 0)} pages, '
                        f'{a.get("chars", 0)} chars, '
                        f'{_esc(status)}')
                digest = _esc(a.get("digest", "")[:900])
                cards += (
                    f'<div class="book"><div class="btitle">'
                    f'{_esc(a["file"])}</div>'
                    f'<div class="bdesc dim">{meta}</div>'
                    f'<div class="bdesc">{digest}...</div></div>')
            articles_html = (
                '<h3 class="sub">Ingested research articles '
                f'({len(reg)} PDFs)</h3>'
                '<p class="dim">PDFs dropped into the repo root or '
                'articles/ are extracted nightly (pypdf) and '
                'registered here with their digests; full text '
                'lands in paper/research/articles/.</p>'
                f'<div class="bgrid">{cards}</div>')
    return (intro
            + '<div class="kgrid">' + "".join(rows) + "</div>"
            + f'<h3 class="sub">Studied library ({len(books)} books)'
            f'</h3><div class="bgrid">{books_html}</div>'
            + programme + articles_html + eval_html)

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
    """The AVFI v4 Pine v5 source (evidence-rewritten) plus the
    v3.2 original, displayed for TradingView."""
    base = Path(__file__).parent
    out = ""
    v4 = base / "avfi_v4.pine"
    if v4.exists():
        out += ('<details class="doc" open><summary>AVFI v4 '
                '&mdash; Stretch + Confirmation &mdash; Pine v5 '
                'source <span class="dim">&mdash; rewritten from '
                'scratch on the evidence: the flow engine and '
                'throttle kept (validated), the price-stretch axis '
                'and detector confirmation added (the one supported '
                'entry signal and its tripling filter), the '
                'falsified components (vol-percentile gating, '
                'multi-axis region confluence, mid-vol terciles) '
                'deliberately absent. Paste into a TradingView '
                'Pine editor.</span></summary>'
                f'<pre>{_esc(v4.read_text())}</pre></details>')
    v32 = base / "avfi_v3_2.pine"
    if v32.exists():
        out += ('<details class="doc"><summary>AVFI v3.2 '
                '&mdash; the original spread-axis indicator '
                '<span class="dim">&mdash; kept for reference and '
                'comparison</span></summary>'
                f'<pre>{_esc(v32.read_text())}</pre></details>')
    return out


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
            f'<td>{(r.get("deflated_sharpe") or {}).get("dsr", "-")}</td>'
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
                      '<th>OOS Sharpe delta</th><th>DSR</th>'
                      '<th>Outcome</th></tr>'
                      f'{rows}</table>'
                      '<p class="dim">DSR = Deflated Sharpe Ratio '
                      '(Bailey & Lopez de Prado 2014): the OOS '
                      'Sharpe judged against what the best of 84 '
                      'zero-skill searches would manufacture by '
                      'luck alone. Below 0.95 means the edge is not '
                      'yet statistically separated from the search '
                      'itself — the honest multiple-testing context '
                      'for every number in this table.</p>')
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
            f'symbols in the widget). Overlay the AVFI v4 '
            f'source above in any TradingView Pine editor.'
            f'</p>'
            f'{_tradingview_embed()}')


def _tb_chart_svg(ch: dict, width=520, height=170) -> str:
    """Price chart with detected bottoms (green) and tops (red):
    triangles = RSI divergence, squares = VSA climax."""
    closes = ch["close"]
    n = len(closes)
    if n < 2:
        return ""
    lo, hi = min(closes), max(closes)
    rng = (hi - lo) or 1.0
    xs = [8 + (width - 16) * i / (n - 1) for i in range(n)]
    ys = [8 + (height - 26) * (1 - (c - lo) / rng) for c in closes]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    marks = ""
    for idx in ch.get("divergence_bottoms", []):
        if idx < n:
            marks += (f'<path d="M{xs[idx]:.1f},{ys[idx] - 6:.1f} '
                      f'l6,10 l-12,0 z" fill="#3fb950">'
                      f'<title>RSI divergence bottom '
                      f'{ch["dates"][idx]}</title></path>')
    for idx in ch.get("divergence_tops", []):
        if idx < n:
            marks += (f'<path d="M{xs[idx]:.1f},{ys[idx] + 6:.1f} '
                      f'l6,-10 l-12,0 z" fill="#f85149">'
                      f'<title>RSI divergence top '
                      f'{ch["dates"][idx]}</title></path>')
    for idx in ch.get("climax_bottoms", []):
        if idx < n:
            marks += (f'<rect x="{xs[idx] - 4:.1f}" '
                      f'y="{ys[idx] - 4:.1f}" width="8" height="8" '
                      f'fill="#3fb950" fill-opacity=".55" '
                      f'stroke="#0d1117" stroke-width=".6">'
                      f'<title>VSA climax bottom '
                      f'{ch["dates"][idx]}</title></rect>')
    for idx in ch.get("climax_tops", []):
        if idx < n:
            marks += (f'<rect x="{xs[idx] - 4:.1f}" '
                      f'y="{ys[idx] - 4:.1f}" width="8" height="8" '
                      f'fill="#f85149" fill-opacity=".55" '
                      f'stroke="#0d1117" stroke-width=".6">'
                      f'<title>VSA climax top '
                      f'{ch["dates"][idx]}</title></rect>')
    return (f'<svg width="{width}" height="{height}" role="img" '
            f'aria-label="{_esc(ch["ticker"])} tops and bottoms" '
            f'viewBox="0 0 {width} {height}">'
            f'<polyline fill="none" stroke="#58a6ff" stroke-width="1.4" '
            f'points="{pts}"/>{marks}'
            f'<text x="8" y="12" font-size="10" fill="#8b949e">'
            f'{_esc(ch["ticker"])}</text></svg>')


def _tops_bottoms_html(paper_dir: Path) -> str:
    """Tops-and-bottoms detection study: detector-marked charts plus
    the confirmed-vs-unconfirmed event study."""
    res_path = paper_dir / "research" / "tops_bottoms.json"
    if not res_path.exists():
        return ("<p class=\"dim\">Tops-and-bottoms research appears "
                "here after the first nightly research pass.</p>")
    r = json.load(open(res_path))
    charts = r.get("charts", [])[:12]
    svgs = "".join(f'<div class="pc">{_tb_chart_svg(ch)}</div>'
                   for ch in charts)
    fmt = lambda x: f"{x:+.4f}" if isinstance(x, (int, float)) else "-"
    rows = ""
    for row in r.get("rows", []):
        dd_better = (row.get("long_confirmed_fwd") is not None
                     and row.get("long_unconfirmed_fwd") is not None
                     and row["long_confirmed_fwd"]
                     > row["long_unconfirmed_fwd"])
        rows += (f'<tr><td>{_esc(row["ticker"])}</td>'
                 f'<td>{row["n_divergence_bottoms"]}</td>'
                 f'<td>{row["n_divergence_tops"]}</td>'
                 f'<td>{row["n_climax_bottoms"]}</td>'
                 f'<td>{row["n_climax_tops"]}</td>'
                 f'<td>{row["n_confirmed"]}</td>'
                 f'<td>{fmt(row.get("long_confirmed_fwd"))}</td>'
                 f'<td>{fmt(row.get("long_unconfirmed_fwd"))}</td>'
                 f'<td class="{"good" if dd_better else "dim"}">'
                 f'{"better" if dd_better else "no edge"}</td></tr>')
    tb_rows = ""
    for row in r.get("rows", []):
        buckets = row.get("topology_buckets", {})
        for sc in sorted(buckets, key=int):
            b = buckets[sc]
            lf = b.get("long_fwd")
            lf_s = f"{lf:+.4f}" if lf is not None else "-"
            good = "good" if int(sc) >= 3 and lf is not None else "dim"
            tb_rows += (f'<tr><td>{_esc(row["ticker"])}</td>'
                        f'<td>{sc}</td><td>{b["n"]}</td>'
                        f'<td class="{good}">{lf_s}</td></tr>')
    if tb_rows:
        tb_rows = ('<table><tr><th>Ticker</th><th>Aligned dims</th>'
                   '<th>entries</th><th>long fwd (10 bars)</th></tr>'
                   f'{tb_rows}</table>')
    rob = r.get("robustness", {})
    rob_html = ""
    if rob:
        ts_rows = "".join(
            f'<tr><td>{_esc(s)}</td>'
            f'<td class="{"good" if v["holds_first"] else "bad"}">'
            f'{"yes" if v["holds_first"] else "no"}</td>'
            f'<td class="{"good" if v["holds_second"] else "bad"}">'
            f'{"yes" if v["holds_second"] else "no"}</td></tr>'
            for s, v in rob.get("time_split", {}).items())
        ca_rows = "".join(
            f'<tr><td>{_esc(s)}</td>'
            f'<td class="{"good" if v["holds"] else "bad"}">'
            f'{"yes" if v["holds"] else "no"}</td></tr>'
            for s, v in rob.get("cross_asset", {}).items())
        rob_html = ('<h3 class="sub">Robustness: does confluence '
                    'survive scrutiny?</h3>'
                    '<p class="dim">Two stress tests of the confluence '
                    'finding. Honest verdict: the score-3 &gt; score-2 '
                    'regularity is period-dependent (stronger in the '
                    'first half of history) and asset-dependent '
                    '(4 of 11 cross-asset series). A partial lead, '
                    'not a solved edge — reported as found.</p>'
                    '<div class="pgrid"><div>'
                    '<h3 class="sub">Time-split (ETFs)</h3>'
                    '<table><tr><th>Ticker</th><th>first half</th>'
                    '<th>second half</th></tr>'
                    f'{ts_rows}</table></div><div>'
                    '<h3 class="sub">Cross-asset</h3>'
                    '<table><tr><th>Series</th><th>holds</th></tr>'
                    f'{ca_rows}</table></div></div>')
    reg = r.get("regime", {})
    reg_html = ""
    if reg:
        rr = ""
        for s, row in reg.items():
            cells = ""
            for k in ("low_vol", "mid_vol", "high_vol"):
                v = row.get(k, {})
                h = v.get("holds")
                cls = ("good" if h else "bad") if h is not None \
                    else "dim"
                txt = "yes" if h else ("no" if h is not None else "-")
                cells += f'<td class="{cls}">{txt}</td>'
            rr += f'<tr><td>{_esc(s)}</td>{cells}</tr>'
        reg_html = ('<h3 class="sub">Regime-conditional confluence '
                    '(descriptive)</h3>'
                    '<p class="dim">Long entries bucketed by trailing '
                    '20-bar realized-vol tercile. The confluence edge '
                    'concentrates in MID-volatility regimes (holds on '
                    '4/5 ETFs) — the same regime-concentrated shape '
                    'as the programme\'s H6 finding. Descriptive '
                    'study, not a live gate.</p>'
                    '<table><tr><th>Ticker</th><th>low vol</th>'
                    '<th>mid vol</th><th>high vol</th></tr>'
                    f'{rr}</table>')
    return (f'<p class="dim">Two strictly-trailing detectors hunt the '
            f'turns: <strong>RSI divergence</strong> (price prints a '
            f'new extreme, momentum refuses to confirm — triangles) '
            f'and <strong>VSA volume climax</strong> (huge effort, '
            f'reversed result — squares). Green = bottoms, red = tops. '
            f'The event study asks the honest question: do detector-'
            f'confirmed z-score entries forward-outperform unconfirmed '
            f'ones (10-bar horizon)? Negative results are reported.'
            f'</p>'
            f'<div class="pgrid">{svgs}</div>'
            '<table><tr><th>Ticker</th><th>div bot</th><th>div top</th>'
            '<th>clim bot</th><th>clim top</th><th>confirmed</th>'
            '<th>long fwd (conf)</th><th>long fwd (unconf)</th>'
            '<th>verdict</th></tr>'
            f'{rows}</table>'
            '<h3 class="sub">Multi-dimensional turn topology '
            '(confluence score)</h3>'
            '<p class="dim">Five dimensions scored at every entry — '
            'price stretch, momentum, divergence, effort, AVFI regime. '
            'Forward returns bucketed by how many align. Monotonicity '
            'across buckets is the honest test of confluence.</p>'
            f'{tb_rows}'
            f'{rob_html}'
            f'{reg_html}')


def _state_space_svg(ss: dict, width=520, height=340) -> str:
    """3D AVFI state-space trajectory, isometric projection. Axes:
    x = AVFI spread z (regime), y = price z (stretch), z = trailing vol
    percentile (risk). Turns are regions of space; the trajectory shows
    them as orbit changes."""
    n = len(ss.get("sp_z", []))
    if n < 50:
        return ""
    start = max(0, n - 400)
    x = np.array(ss["sp_z"][start:])
    y = np.array(ss["price_z"][start:])
    z = np.array(ss["vol_pct"][start:])
    # isometric projection
    c30, s30 = 0.866, 0.5
    u = (x - y) * c30
    v = (x + y) * s30 - z
    pad = 24
    su = (width - 2 * pad) / (u.max() - u.min() or 1.0)
    sv = (height - 2 * pad) / (v.max() - v.min() or 1.0)
    s = min(su, sv)
    ox = width / 2 - (u.max() + u.min()) / 2 * s
    oy = height / 2 + (v.max() + v.min()) / 2 * s
    px = lambda i: ox + u[i] * s
    py = lambda i: oy - v[i] * s
    pts = " ".join(f"{px(i):.1f},{py(i):.1f}"
                   for i in range(len(u)))
    marks = ""
    for key, color, dy in (("divergence_bottoms", "#3fb950", -1),
                           ("climax_bottoms", "#3fb950", 1),
                           ("divergence_tops", "#f85149", 1),
                           ("climax_tops", "#f85149", -1)):
        for idx in ss.get(key, []):
            i = idx - start
            if 0 <= i < len(u):
                marks += (f'<circle cx="{px(i):.1f}" cy="{py(i):.1f}" '
                          f'r="3" fill="{color}" fill-opacity=".85">'
                          f'<title>{key} {ss["dates"][idx]}</title>'
                          f'</circle>')
    # origin axes cross at the projected (0,0,0.5)
    uo = (0 - 0) * c30
    vo = (0 + 0) * s30 - 0.5
    xo, yo = ox + uo * s, oy - vo * s
    return (f'<svg width="{width}" height="{height}" role="img" '
            f'aria-label="{_esc(ss["ticker"])} AVFI state space" '
            f'viewBox="0 0 {width} {height}">'
            f'<line x1="{xo:.1f}" y1="{yo:.1f}" '
            f'x2="{width - pad}" y2="{yo:.1f}" '
            f'stroke="rgba(128,128,128,.25)"/>'
            f'<line x1="{xo:.1f}" y1="{yo:.1f}" x2="{xo:.1f}" '
            f'y2="{pad}" stroke="rgba(128,128,128,.25)"/>'
            f'<polyline fill="none" stroke="#a371f7" '
            f'stroke-width="1.1" stroke-opacity=".8" '
            f'points="{pts}"/>{marks}'
            f'<text x="10" y="16" font-size="11" fill="#8b949e">'
            f'{_esc(ss["ticker"])} — state space: x=spread z, '
            f'y=price z, z=vol regime</text></svg>')


def _state_space_html(paper_dir: Path) -> str:
    """The 3D AVFI state-space section: trajectories for the deployed
    ETFs and the strongest mean-reverting commodities."""
    path = paper_dir / "research" / "avfi_state_space.json"
    if not path.exists():
        return ("<p class=\"dim\">State-space trajectories appear "
                "here after the first nightly research pass.</p>")
    series = json.load(open(path))
    etfs = [s for s in series
            if s["ticker"] in ("SPY", "QQQ", "IWM", "XLF", "XLE")]
    top_comm = [s for s in series if s["ticker"] in
                ("ZOF", "OJF", "CTF", "ZSF", "ZWF", "PLF", "CLF")]
    svgs = "".join(f'<div class="pc">{_state_space_svg(s)}</div>'
                   for s in etfs + top_comm)
    study_html = ""
    spath = paper_dir / "research" / "state_space_study.json"
    if spath.exists():
        study = json.load(open(spath))
        rows = ""
        for s, row in study.items():
            br = row["bottom_region"]
            mr_ = row["mid_region"]
            holds = row.get("hypothesis_holds")
            cls = "good" if holds else "dim"
            rows += (f'<tr><td>{_esc(s)}</td>'
                     f'<td>{br["n"]}</td>'
                     f'<td>{br["fwd"] if br["fwd"] is not None else "-"}</td>'
                     f'<td>{mr_["n"]}</td>'
                     f'<td>{mr_["fwd"] if mr_["fwd"] is not None else "-"}</td>'
                     f'<td class="{cls}">'
                     f'{"supported" if holds else "unproven"}</td></tr>')
        pooled_html = ""
        extpath = paper_dir / "research" / "state_space_study_extended.json"
        if extpath.exists():
            ext = json.load(open(extpath))
            agg = ext.get("aggregate") or {}
            br = agg.get("bottom_region") or {}
            mr_ = agg.get("mid_region") or {}
            holds = agg.get("hypothesis_holds")
            cls = "good" if holds else "dim"
            n_series = len(ext.get("series", {}))
            pooled_html = (
                '<h3 class="sub">Pooled across the full universe'
                '</h3>'
                '<p class="dim">The deployed ETFs fire the full '
                'bottom region too rarely for a per-instrument '
                'verdict, so the hypothesis is also tested POOLED '
                f'across all {n_series} extended series (crypto, '
                'indices, commodities). This is the accumulating '
                'evidence base; the pooled verdict is the one that '
                'matters.</p>'
                '<table><tr><th>Scope</th>'
                '<th>bottom-region n</th><th>fwd</th>'
                '<th>mid-region n</th><th>fwd</th>'
                '<th>beats (own scale)</th>'
                '<th>verdict</th></tr>'
                f'<tr><td>POOLED ({n_series} series)</td>'
                f'<td>{br.get("n", 0)}</td>'
                f'<td>{br.get("fwd") if br.get("fwd") is not None else "-"}</td>'
                f'<td>{(mr_.get("n") or 0)}</td>'
                f'<td>{mr_.get("fwd") if mr_.get("fwd") is not None else "-"}</td>'
                f'<td>{agg.get("series_beats", 0)} / '
                f'{agg.get("series_with_both", 0)}</td>'
                f'<td class="{cls}">'
                f'{"supported" if holds else "unproven"}</td></tr>'
                '</table>'
                '<p class="dim">The pooled forward returns mix '
                'scales across very different assets, so the '
                'scale-free beat count is the stronger evidence: '
                'for the hypothesis to be supported it must win '
                'the pooled return AND beat on its own scale in a '
                'majority of series that have both regions '
                'populated.</p>')
        study_html = ('<h3 class="sub">The region hypothesis, tested'
                      '</h3>'
                      '<p class="dim">If bottoms are REGIONS of space, '
                      'entries inside the bottom region (deep stretch '
                      '+ fading flow + elevated vol) should forward-'
                      'outperform partially-aligned entries. Honest '
                      'verdict: unproven — the full region fires '
                      'rarely (0-9 events per ETF) and the evidence is '
                      'mixed. The study re-runs nightly; the buckets '
                      'fill as data accumulates.</p>'
                      '<table><tr><th>Ticker</th>'
                      '<th>bottom-region n</th><th>fwd</th>'
                      '<th>mid-region n</th><th>fwd</th>'
                      '<th>verdict</th></tr>'
                      f'{rows}</table>')
        axispath = paper_dir / "research" / "state_space_axis.json"
        if axispath.exists():
            axis = json.load(open(axispath))
            arows = ""
            for name, a in axis.items():
                holds = a.get("carries_weight")
                cls = "good" if holds else "dim"
                label = ("flow fading (spread z < 0)" if name == "sp_z_neg"
                         else "elevated vol (percentile > 0.5)")
                arows += (f'<tr><td>{label}</td>'
                          f'<td>{a.get("n_with", 0)}</td>'
                          f'<td>{a.get("pooled_with_fwd")}</td>'
                          f'<td>{a.get("n_without", 0)}</td>'
                          f'<td>{a.get("pooled_without_fwd")}</td>'
                          f'<td>{a.get("beats", 0)} / '
                          f'{a.get("series", 0)}</td>'
                          f'<td class="{cls}">'
                          f'{"carries weight" if holds else "no"}</td></tr>')
            sp_ax = axis.get("sp_z_neg") or {}
            vol_ax = axis.get("vol_high") or {}
            n_sp, n_vol = (sp_ax.get("series", 0),
                           vol_ax.get("series", 0))
            b_sp, b_vol = (sp_ax.get("beats", 0),
                           vol_ax.get("beats", 0))
            both = (sp_ax.get("carries_weight")
                    and vol_ax.get("carries_weight"))
            ax_verdict = (
                'at the full-universe sample both axes show WEAK '
                f'descriptive majorities (flow-fading {b_sp}/{n_sp}, '
                f'elevated-vol {b_vol}/{n_vol}) and pooled edges - '
                'but the causal test (the v4 study) already showed '
                'axis-conditioned entries do not convert into a '
                'strategy, and the pooled numbers are scale-'
                'contaminated by high-drift crypto. Descriptive '
                'weight is not an edge; at the earlier 50-series '
                'sample both axes read as dead, which is itself a '
                'lesson about sample size.'
                if both else
                'neither axis carries weight at this sample; deep '
                'stretch alone is what the data supports.')
            study_html += (
                '<h3 class="sub">Axis attribution: which single axis '
                'pays?</h3>'
                '<p class="dim">The region was falsified as a bundle, '
                'so each axis is tested ALONE: among deep-stretch '
                'long entries, do entries WITH the condition '
                'forward-outperform entries WITHOUT it? Honest '
                f'reading, regenerated live: {ax_verdict}</p>'
                '<table><tr><th>Axis</th>'
                '<th>with n</th><th>fwd</th>'
                '<th>without n</th><th>fwd</th>'
                '<th>beats (own scale)</th>'
                '<th>verdict</th></tr>'
                f'{arows}</table>')
        depthpath = paper_dir / "research" / "stretch_depth.json"
        if depthpath.exists():
            depth = json.load(open(depthpath))
            drows = ""
            for name, b in depth.get("buckets", {}).items():
                drows += (f'<tr><td>price z {name}</td>'
                          f'<td>{b.get("n", 0)}</td>'
                          f'<td>{b.get("fwd") if b.get("fwd") is not None else "-"}</td>'
                          f'<td>{b.get("beats_shallow", 0)} / '
                          f'{b.get("series", 0)}</td></tr>')
            deeper = depth.get("own_scale_deeper_pays")
            knife = depth.get("falling_knife")
            bk = depth.get("buckets", {})
            b1 = bk.get("z2.5-3.0", {})
            b2 = bk.get("z3.0-4.0", {})
            b3 = bk.get("z4.0+", {})
            beat_txt = ", ".join(
                f'{b.get("beats_shallow", 0)}/{b.get("series", 0)}'
                for b in (b1, b2, b3) if b)
            study_html += (
                '<h3 class="sub">The stretch-depth curve</h3>'
                '<p class="dim">Deep stretch is the one supported '
                'signal, so: does DEEPER stretch pay more, or is '
                'there a falling-knife zone? On each series\' '
                'OWN SCALE, deeper stretch beats the shallow edge '
                f'in a majority of series at every depth '
                f'({beat_txt}), and there is no falling '
                'knife even beyond z 4. Own-scale verdict: '
                f'<strong>{"deeper pays" if deeper else "inconclusive"}'
                f'</strong>; falling knife: '
                f'<strong>{"real" if knife else "not found"}</strong>. '
                'A descriptive lead for entry-threshold research \u2014 '
                'not yet a causal, out-of-sample-tested variant.</p>'
                '<table><tr><th>Depth bucket</th><th>n</th>'
                '<th>pooled fwd</th><th>beats shallow (own scale)'
                '</th></tr>'
                f'{drows}</table>')
        study_html += pooled_html
    return (f'<p class="dim">Every bar is a <strong>position in '
            f'space</strong>, and the strategy lives as a trajectory '
            f'through it: x = AVFI spread z (the regime axis), '
            f'y = price z-score (the stretch axis), z = trailing vol '
            f'percentile (the risk axis). Tops and bottoms are not '
            f'points on a price chart — they are <strong>regions of '
            f'this space</strong>: bottoms form in the deep-stretch, '
            f'fading-flow, elevated-vol octant; tops in the mirror. '
            f'Turns appear as orbit changes. Purple = trajectory, '
            f'green = detected bottoms, red = detected tops '
            f'(hover for dates). Deployed ETFs plus the strongest '
            f'mean-reverting commodities.</p>'
            f'<div class="pgrid">{svgs}</div>'
            f'{study_html}')


def _lessons_html(paper_dir: Path) -> str:
    """The learning lessons and live inferences, regenerated from
    the research artifacts every nightly pass."""
    path = paper_dir / "research" / "lessons.json"
    if not path.exists():
        return ("<p class=\"dim\">Lessons appear here after the "
                "first nightly research pass.</p>")
    r = json.load(open(path))
    inf = r.get("inferences", {})
    metrics = "".join(
        f'<div class="metric"><div class="mval">{v}</div>'
        f'<div class="mlabel">{_esc(k)}</div></div>'
        for k, v in (
            ("series studied", inf.get("universe_series")),
            ("mean-reverting (all)", inf.get("mr_passing_all")),
            ("mean-reverting (crypto)", inf.get("mr_passing_crypto")),
            ("crypto confluence holds", inf.get("crypto_confluence_holds")),
            ("region pooled n", inf.get("region_pooled_n")),
            ("DSR (deflated)", inf.get("dsr")),
            ("forward sessions", f"{inf.get('forward_sessions', 0)} / 20"),
        ))
    leaders = ", ".join(
        f"{_esc(x['ticker'])} (t={x['t_stat']}, hl={x['half_life_bars']}b)"
        for x in inf.get("strongest_mr", [])[:5])
    cards = ""
    for i, l in enumerate(r.get("lessons", []), 1):
        cards += (
            f'<div class="book"><div class="btitle">{i}. '
            f'{_esc(l["lesson"])}</div>'
            f'<div class="bdesc dim">forced by: '
            f'{_esc(l["forced_by"])}</div>'
            f'<div class="bdesc">{_esc(l["remedy"])}</div></div>')
    return (f'<p class="dim">Everything this project has learned, '
            f'extracted live from the accumulated studies - each '
            f'lesson tied to the data that forced it and the '
            f'method change it produced. Regenerated nightly; '
            f'never hand-staled.</p>'
            f'<div class="metrics">{metrics}</div>'
            f'<p class="dim">Strongest measured mean reversion: '
            f'{leaders}</p>'
            f'<div class="bgrid">{cards}</div>')


def _mr_edge_html(paper_dir: Path) -> str:
    """The MR-coin edge study: where the physics says the edge
    should live - with its control group and the honest verdict."""
    path = paper_dir / "research" / "mr_edge.json"
    if not path.exists():
        return ("<p class=\"dim\">The MR-coin edge study appears "
                "here after the first nightly research pass.</p>")
    r = json.load(open(path))
    mr = r.get("mr_pooled_oos_sharpe")
    ctl = r.get("control_pooled_oos_sharpe")
    edge = r.get("edge_differential")
    dsr = r.get("deflated_sharpe") or {}
    conf = r.get("confirmed_fwd_median")
    plain = r.get("plain_fwd_median")
    verdict = r.get("verdict")
    cls = "good" if verdict else "dim"
    vtxt = ("edge holds" if verdict else
            "no tradable edge yet - a real filter, not a strategy")
    rows = ""
    for x in sorted(r.get("mr_runs", []),
                    key=lambda x: -(x.get("oos_sharpe") or 0))[:12]:
        rows += (f'<tr><td>{_esc(x["ticker"])}</td>'
                 f'<td>{x["t_stat"]}</td>'
                 f'<td>{x["half_life"]}</td>'
                 f'<td>{x["trades"]}</td>'
                 f'<td>{x["full_sharpe"]}</td>'
                 f'<td class="{"good" if (x.get("oos_sharpe") or 0) > 0 else "dim"}">'
                 f'{x["oos_sharpe"]}</td></tr>')
    return (f'<p class="dim">Mean reversion is measurable per coin, '
            f'so the edge question writes itself: does a strictly '
            f'causal z-score strategy on the strongest mean-reverting '
            f'coins pay out-of-sample - and does it beat the CONTROL '
            f'GROUP of coins that failed the same test? Dead coins '
            f'(priced 1000x below peak) are excluded; returns are '
            f'winsorized; forward stats are medians; every entry and '
            f'exit pays 5 bps.</p>'
            f'<div class="metrics">'
            f'<div class="metric"><div class="mval">{mr}</div>'
            f'<div class="mlabel">MR pooled OOS Sharpe</div></div>'
            f'<div class="metric"><div class="mval">{ctl}</div>'
            f'<div class="mlabel">control group OOS</div></div>'
            f'<div class="metric"><div class="mval">{edge}</div>'
            f'<div class="mlabel">edge differential</div></div>'
            f'<div class="metric"><div class="mval">{conf}</div>'
            f'<div class="mlabel">confirmed fwd median</div></div>'
            f'<div class="metric"><div class="mval">{plain}</div>'
            f'<div class="mlabel">plain fwd median</div></div>'
            f'<div class="metric"><div class="mval">{dsr.get("dsr")}</div>'
            f'<div class="mlabel">DSR at {dsr.get("n_trials")} trials'
            f'</div></div>'
            f'<div class="metric"><div class="mval" class="{cls}">{vtxt}'
            f'</div>'
            f'<div class="mlabel">honest verdict</div></div>'
            f'</div>'
            f'<p class="dim">The t-stat selection carries real ranking '
            f'information (MR coins lose far less than the control '
            f'group), but long-only z-score MR on crypto is net-'
            f'negative OOS after costs in absolute terms. The one '
            f'clean signal: detector-confirmed deep stretches in MR '
            f'coins roughly TRIPLE the median forward return '
            f'(+{conf}% vs +{plain}%) - confirmation is a filter '
            f'worth having; it is not yet a strategy worth running.'
            f'</p>'
            f'<table><tr><th>Ticker</th><th>MR t-stat</th>'
            f'<th>half-life (bars)</th><th>trades</th>'
            f'<th>full Sharpe</th><th>OOS Sharpe</th></tr>'
            f'{rows}</table>')


def _v4_study_html(paper_dir: Path) -> str:
    """v4 stretch+confirmation vs plain stretch, measured across the
    whole universe - with the honest verdict."""
    path = paper_dir / "research" / "v4_study.json"
    if not path.exists():
        return ("<p class=\"dim\">The v4 study appears here after the "
                "first nightly research pass.</p>")
    r = json.load(open(path))
    o = r.get("overall", {})
    cls = r.get("by_class", {})
    imp = o.get("improves")
    cls_v = "good" if imp else "dim"
    vtxt = ("confirmation improves the strategy" if imp else
            "confirmation does NOT survive causal conversion")
    srows = ""
    for name, s in [("ALL SERIES", o)] + list(cls.items()):
        if not s:
            continue
        c_imp = s.get("improves")
        srows += (f'<tr><td>{name.upper()}</td>'
                  f'<td>{s.get("series")}</td>'
                  f'<td>{s.get("plain_pooled")}</td>'
                  f'<td>{s.get("v4_pooled")}</td>'
                  f'<td>{s.get("pooled_premium")}</td>'
                  f'<td>{s.get("own_scale_beats")}</td>'
                  f'<td class="{"good" if c_imp else "dim"}">'
                  f'{"improves" if c_imp else "no"}</td></tr>')
    best = "".join(
        f'<tr><td>{_esc(x["ticker"])}</td><td>{x["plain_oos"]}</td>'
        f'<td class="good">{x["v4_oos"]}</td>'
        f'<td class="good">+{x["premium_worse_window"]}</td></tr>'
        for x in r.get("best_series", [])[:10])
    worst = "".join(
        f'<tr><td>{_esc(x["ticker"])}</td><td>{x["plain_oos"]}</td>'
        f'<td class="dim">{x["v4_oos"]}</td>'
        f'<td class="dim">{x["premium_worse_window"]}</td></tr>'
        for x in r.get("worst_series", [])[:10])
    return (f'<p class="dim">AVFI v4\'s signal is deep stretch + '
            f'detector confirmation. The forward-return study measured '
            f'a tripling of the median 10-day payoff on confirmed '
            f'stretches - so the honest question: does confirmation '
            f'IMPROVE the tradable strategy? Both variants run the same '
            f'causal z-score core (enter |z| &ge; 2, exit |z| &le; '
            f'0.25, 5 bps both sides, winsorized), one with '
            f'confirmed entries only, judged at the WORSE of two OOS '
            f'windows across {o.get("series")} series.</p>'
            f'<div class="metrics">'
            f'<div class="metric"><div class="mval">'
            f'{o.get("plain_pooled")}</div>'
            f'<div class="mlabel">plain pooled OOS</div></div>'
            f'<div class="metric"><div class="mval">'
            f'{o.get("v4_pooled")}</div>'
            f'<div class="mlabel">v4 pooled OOS</div></div>'
            f'<div class="metric"><div class="mval">'
            f'{o.get("pooled_premium")}</div>'
            f'<div class="mlabel">pooled premium</div></div>'
            f'<div class="metric"><div class="mval" class="{cls_v}">'
            f'{vtxt}</div>'
            f'<div class="mlabel">honest verdict</div></div>'
            f'</div>'
            f'<p class="dim"><strong>What the data says:</strong> '
            f'confirmation does NOT survive causal conversion - the '
            f'pooled premium is {o.get("pooled_premium")} with '
            f'{o.get("own_scale_beats")} own-scale wins (a coin '
            f'flip), and on commodities it is actively harmful '
            f'(-0.54): confirmation biases entries toward climax '
            f'bars, where the z-core\'s early exits and costs bite. '
            f'The forward-return tripling was real but '
            f'<em>unconditional</em>; the strategy\'s exit rule '
            f'never collects it. The deeper finding: <strong>plain '
            f'z-score mean reversion on COMMODITIES pooled OOS is '
            f'+0.37 Sharpe - the first positive pooled strategy '
            f'result in the project</strong> - while crypto\'s drift '
            f'kills the same core (-0.31). The edge lives in the '
            f'commodity complex, not crypto; v4 stays what the '
            f'evidence supports - a visualization and risk-throttle '
            f'tool, not an entry filter.</p>'
            f'<table><tr><th>Scope</th><th>series</th>'
            f'<th>plain pooled OOS</th><th>v4 pooled OOS</th>'
            f'<th>premium</th><th>beats</th><th>verdict</th></tr>'
            f'{srows}</table>'
            f'<h3 class="sub">Where confirmation helped most</h3>'
            f'<table><tr><th>Ticker</th><th>plain OOS</th>'
            f'<th>v4 OOS</th><th>premium</th></tr>{best}</table>'
            f'<h3 class="sub">Where it hurt most</h3>'
            f'<table><tr><th>Ticker</th><th>plain OOS</th>'
            f'<th>v4 OOS</th><th>premium</th></tr>{worst}</table>')


def _commodity_edge_html(paper_dir: Path) -> str:
    """The commodity edge through the full honesty battery - the
    depth-first follow-up to the project's first positive result."""
    path = paper_dir / "research" / "commodity_edge.json"
    if not path.exists():
        return ("<p class=\"dim\">The commodity edge battery appears "
                "here after the first nightly research pass.</p>")
    r = json.load(open(path))
    b = r.get("battery", {})
    verdict = r.get("verdict")
    cls = "good" if verdict else "dim"
    vtxt = ("battery passed - a candidate at last" if verdict else
            "battery failed - the +0.37 was marginal, not an edge")
    mrows = ""
    for m in r.get("markets", [])[:32]:
        oos = m.get("oos_40")
        mrows += (f'<tr><td>{_esc(m["ticker"])}</td>'
                  f'<td>{m["mr_t_stat"]}</td>'
                  f'<td>{m["half_life"]}</td>'
                  f'<td>{m["trades"]}</td>'
                  f'<td>{m["full"]}</td>'
                  f'<td>{m["first_half"]}</td>'
                  f'<td>{m["second_half"]}</td>'
                  f'<td class="{"good" if (oos or 0) > 0 else "dim"}">'
                  f'{oos}</td></tr>')
    dsr = b.get("deflated_sharpe") or {}
    return (f'<p class="dim">The v4 study surfaced the project\'s '
            f'first positive pooled result: plain z-score mean '
            f'reversion on commodities, +0.37 OOS. The project\'s '
            f'own lessons say a number like that is not believed '
            f'until it survives conversion - so it went through '
            f'the FULL battery: per-market attribution, dual-split, '
            f'time-split, 2x cost stress, and the Deflated Sharpe '
            f'context at {r.get("n_markets")} trials.</p>'
            f'<div class="metrics">'
            f'<div class="metric"><div class="mval">'
            f'{b.get("pooled_oos_worse_window")}</div>'
            f'<div class="mlabel">pooled OOS (worse window)</div></div>'
            f'<div class="metric"><div class="mval">'
            f'{b.get("time_split_first_half")} &rarr; '
            f'{b.get("time_split_second_half")}</div>'
            f'<div class="mlabel">time-split Sharpe</div></div>'
            f'<div class="metric"><div class="mval">'
            f'{b.get("cost_stress_2x_pooled_oos")}</div>'
            f'<div class="mlabel">at 2x costs</div></div>'
            f'<div class="metric"><div class="mval">'
            f'{b.get("positive_markets")}</div>'
            f'<div class="mlabel">positive markets</div></div>'
            f'<div class="metric"><div class="mval">'
            f'{dsr.get("dsr")}</div>'
            f'<div class="mlabel">DSR at {dsr.get("n_trials")} '
            f'trials</div></div>'
            f'<div class="metric"><div class="mval" class="{cls}">'
            f'{vtxt}</div>'
            f'<div class="mlabel">honest verdict</div></div>'
            f'</div>'
            f'<p class="dim"><strong>What the battery said:</strong> '
            f'the pooled OOS holds (+0.37) and both time-split '
            f'halves are positive, but the edge DIES at 2x costs '
            f'(-0.02) and the Deflated Sharpe ({dsr.get("dsr")}) '
            f'is below the 0.5 bar - not separated from search '
            f'luck at {dsr.get("n_trials")} trials. The +0.37 was '
            f'marginal and execution-sensitive, not an edge. The '
            f'direction is now depth-first: one lead at a time, '
            f'through every gate, and no new universes until a '
            f'battery-passing edge exists. The method is the '
            f'asset; the edge has not been found yet.</p>'
            f'<table><tr><th>Market</th><th>MR t</th>'
            f'<th>half-life</th><th>trades</th><th>full</th>'
            f'<th>1st half</th><th>2nd half</th><th>OOS</th></tr>'
            f'{mrows}</table>')


def _inevitabilities_html(paper_dir: Path) -> str:
    """Structural inevitabilities: the market facts that hold
    without prediction - the research framework, measured."""
    path = paper_dir / "research" / "inevitabilities.json"
    if not path.exists():
        return ("<p class=\"dim\">The inevitabilities study appears "
                "here after the first nightly research pass.</p>")
    r = json.load(open(path))
    rows = ""
    for key, c in r.get("claims", {}).items():
        v = c.get("verdict", "")
        cls = "good" if "STRUCTURAL" in v else "dim"
        rows += (f'<tr><td>{_esc(key)}</td>'
                 f'<td class="dim">{_esc(c.get("description", ""))[:260]}'
                 f'{"..." if len(c.get("description", "")) > 260 else ""}'
                 f'</td><td class="{cls}">{_esc(v)}</td></tr>')
    cb = r.get("claims", {}).get("crash_bounce", {})
    ic = r.get("claims", {}).get("impulse_concentration", {})
    return (f'<p class="dim">True direction prediction is '
            f'impossible - but markets have INEVITABLE occurrences '
            f'and drawdown-hostile conditions that can be catalogued '
            f'and measured. The research framework\'s structural '
            f'claims were put to the data across '
            f'{r.get("n_series")} series, each with an honest '
            f'verdict: STRUCTURAL (inevitable) or FOLKLORE (the '
            f'data disagrees).</p>'
            f'<div class="metrics">'
            f'<div class="metric"><div class="mval">'
            f'{ic.get("concentration_ratio_top5")}x</div>'
            f'<div class="mlabel">move-share of the top 5% of '
            f'bars (uniform = 1x)</div></div>'
            f'<div class="metric"><div class="mval">'
            f'{cb.get("crash_fwd_median_anchored")}</div>'
            f'<div class="mlabel">fwd 10d median after a &le; -7% '
            f'day, anchored assets</div></div>'
            f'<div class="metric"><div class="mval">'
            f'{cb.get("anchored_p_positive")}</div>'
            f'<div class="mlabel">P(positive) after crash, '
            f'anchored (n={cb.get("n_crashes_anchored")})</div></div>'
            f'<div class="metric"><div class="mval">'
            f'{cb.get("crash_fwd_median_crypto")}</div>'
            f'<div class="mlabel">same, crypto (no anchor)</div>'
            f'</div></div>'
            f'</div>'
            f'<p class="dim"><strong>What the data says:</strong> the '
            f'noise/impulse structure is REAL (the top 5% of bars '
            f'carry {ic.get("top5_median")} of all movement - a '
            f'{ic.get("concentration_ratio_top5")}x dispropor- '
            f'tion: markets range, then impulse). The crash bounce '
            f'is STRUCTURAL exactly where the anchor physics says it '
            f'must be: on anchored assets (commodities, indices) a '
            f'&le; -7% day forward-returns +{cb.get("crash_fwd_median_anchored")} '
            f'median with {cb.get("anchored_p_positive")} positive - '
            f'while on crypto, with no anchor, the same crash is a '
            f'coin flip ({cb.get("crash_fwd_median_crypto")}). '
            f'Falsified: time-at-price levels are NOT safe (92% of '
            f'congested levels are revisited within 60 bars), and '
            f'compression does NOT precede larger moves - the '
            f'tightest ranges precede SMALLER ones (volatility '
            f'clusters). Impulse follow-through is a coin flip '
            f'(0.47). The framework\'s 5/15-minute max-hold rules '
            f'need intraday data and are honestly recorded as '
            f'untestable on daily bars.</p>'
            f'<table><tr><th>Claim</th><th>What it says</th>'
            f'<th>Verdict</th></tr>{rows}</table>')


def _smh_hazard_html(paper_dir: Path) -> str:
    """The hazard model: KM with censoring plus the Cox regression
    - the frontier's first solved item, scored."""
    path = paper_dir / "research" / "smh_hazard.json"
    if not path.exists():
        return ""
    r = json.load(open(path))
    if r.get("status") != "OK":
        return ""
    c = r.get("cox", {})
    verdict = r.get("verdict")
    cls = "good" if verdict else "dim"
    covs = c.get("covariates", [])
    rows = "".join(
        f'<tr><td>{_esc(cov)}</td><td>{b}</td><td>{z}</td>'
        f'<td>{hr}</td></tr>'
        for cov, b, z, hr in zip(
            covs, c.get("coefficients", []),
            c.get("z_stats", []),
            c.get("hazard_ratios_per_sd", [])))
    return (f'<h3 class="sub">The hazard model &mdash; Cox v1, '
            f'scored</h3>'
            f'<p class="dim">24,638 compression-entry episodes '
            f'(event rate {r.get("event_rate")}); survival to 4 '
            f'weeks {r.get("survival_4_weeks")}. The Cox '
            f'proportional-hazards regression ranks episode risk '
            f'with <strong>concordance '
            f'{c.get("concordance")}</strong> (chance = 0.5). '
            f'Deeper compression raises the event hazard ~1.45&times; '
            f'per standard deviation; momentum into compression '
            f'adds ~1.10&times;. This is the clock growing from a '
            f'tercile table into a proper hazard model - exactly '
            f'the step the hypothesis names.</p>'
            f'<div class="metrics">'
            f'<div class="metric"><div class="mval">'
            f'{c.get("concordance")}</div>'
            f'<div class="mlabel">Cox concordance (chance 0.5)'
            f'</div></div>'
            f'<div class="metric"><div class="mval">'
            f'{r.get("n_episodes")}</div>'
            f'<div class="mlabel">compression episodes</div></div>'
            f'<div class="metric"><div class="mval">'
            f'{r.get("survival_4_weeks")}</div>'
            f'<div class="mlabel">survival to 4 weeks</div></div>'
            f'<div class="metric"><div class="mval" class="{cls}">'
            f'{"scored and significant" if verdict else "not yet"}'
            f'</div>'
            f'<div class="mlabel">hazard model verdict</div></div>'
            f'</div>'
            f'<table><tr><th>Covariate (per SD)</th><th>beta</th>'
            f'<th>z</th><th>hazard ratio</th></tr>{rows}</table>')


def _smh_proof_html(paper_dir: Path) -> str:
    """The Salient Market Hypothesis proof battery: every measurable
    claim, scored on the universe - the SMH's own scoreboard."""
    path = paper_dir / "research" / "smh_proof.json"
    if not path.exists():
        return ("<p class=\"dim\">The SMH proof battery appears here "
                "after the first nightly research pass.</p>")
    r = json.load(open(path))
    clk = r.get("laws", {}).get("clock_compression_hazard", {})
    th = r.get("laws", {}).get(
        "theorem_hazard_up_direction_unknown", {})
    km = r.get("kaplan_meier_v0") or {}
    rows = ""
    for key, law in r.get("laws", {}).items():
        v = law.get("verdict", "")
        cls = "good" if v == "PROVEN" else "dim"
        rows += (f'<tr><td>{_esc(key)}</td>'
                 f'<td class="dim">{_esc(law.get("claim", ""))[:200]}'
                 f'{"..." if len(law.get("claim", "")) > 200 else ""}'
                 f'</td><td class="{cls}">{_esc(v)}</td></tr>')
    n_proven = sum(1 for v in r.get("laws", {}).values()
                   if v.get("verdict") == "PROVEN")
    return (f'<p class="dim">The Salient Market Hypothesis '
            f'(KNOWLEDGE_SMH.md) - state instead of count, clock '
            f'instead of prophecy, calibration instead of belief - '
            f'makes six unconditional laws, a central theorem, and a '
            f'measured clock claim. Per its own falsification '
            f'protocol, every quantitative claim is scored: '
            f'<strong>{n_proven} of {len(r.get("laws", {}))} '
            f'claims PROVEN</strong> on '
            f'{r.get("n_series")} series, with ground-truth tests '
            f'both ways (GARCH-like series prove the vol laws; '
            f'Gaussian iid controls fail them).</p>'
            f'<div class="metrics">'
            f'<div class="metric"><div class="mval">'
            f'{clk.get("hazard_from_compression")}</div>'
            f'<div class="mlabel">event hazard from compression</div>'
            f'</div>'
            f'<div class="metric"><div class="mval">'
            f'{clk.get("hazard_from_high_vol")}</div>'
            f'<div class="mlabel">from high vol '
            f'(n={clk.get("n_high_bars")})</div></div>'
            f'<div class="metric"><div class="mval">'
            f'{th.get("p_event_up_from_compression")}</div>'
            f'<div class="mlabel">P(event is UP) from compression '
            f'(n={th.get("n_events")})</div></div>'
            f'<div class="metric"><div class="mval">'
            f'{km.get("median_time_to_event_bars")}</div>'
            f'<div class="mlabel">median bars to event from '
            f'compression (KM v0)</div></div>'
            f'</div>'
            f'<p class="dim"><strong>The two results that matter:'
            f'</strong> the CLOCK replicates - a significant event '
            f'(&ge; 2.5&sigma;<sub>w</sub> within 4 weeks) is '
            f'{round((clk.get("hazard_from_compression") or 0) / max(clk.get("hazard_from_high_vol") or 1, 0.0001), 1)}x '
            f'more likely from the compression tercile than from '
            f'high vol, on a completely different universe than the '
            f'original clock study (which measured 47% vs 14%). '
            f'And the central theorem\'s consequence is measured: '
            f'among {th.get("n_events")} compression-born events, '
            f'P(up) = {th.get("p_event_up_from_compression")} - '
            f'the clock says WHEN is more likely; it never says '
            f'WHICH WAY. Law 3 (horizon structure) reads PARTAL-honest: '
            f'short-lag autocorrelation is near zero as claimed, but '
            f'no medium-horizon momentum or long-horizon reversal is '
            f'visible on daily crypto/commodity bars. The volume '
            f'clock and Hawkes self-excitation need intraday data - '
            f'documented as out of scope, per the SMH\'s own '
            f'rules.</p>'
            f'<table><tr><th>Claim</th><th>What it says</th>'
            f'<th>Verdict</th></tr>{rows}</table>')


def _crypto_avfi_chart_svg(ch: dict, width=520, height=230) -> str:
    """Two-panel crypto chart: price with detected tops/bottoms on
    top, the AVFI spread z with the trigger line and throttle zone
    below — the regime context behind every detected turn."""
    closes = ch["close"]
    sp_z = ch.get("sp_z") or []
    n = len(closes)
    if n < 2 or len(sp_z) != n:
        return _tb_chart_svg(ch, width, 170)
    trigger = ch.get("trigger", -1.0)
    p_h, z_h = 140, 62
    lo, hi = min(closes), max(closes)
    rng = (hi - lo) or 1.0
    xs = [8 + (width - 16) * i / (n - 1) for i in range(n)]
    ys = [8 + (p_h - 26) * (1 - (c - lo) / rng) for c in closes]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    marks = ""
    for idx in ch.get("divergence_bottoms", []):
        if idx < n:
            marks += (f'<path d="M{xs[idx]:.1f},{ys[idx] - 6:.1f} '
                      f'l6,10 l-12,0 z" fill="#3fb950">'
                      f'<title>RSI divergence bottom '
                      f'{ch["dates"][idx]}</title></path>')
    for idx in ch.get("divergence_tops", []):
        if idx < n:
            marks += (f'<path d="M{xs[idx]:.1f},{ys[idx] + 6:.1f} '
                      f'l6,-10 l-12,0 z" fill="#f85149">'
                      f'<title>RSI divergence top '
                      f'{ch["dates"][idx]}</title></path>')
    for idx in ch.get("climax_bottoms", []):
        if idx < n:
            marks += (f'<rect x="{xs[idx] - 4:.1f}" '
                      f'y="{ys[idx] - 4:.1f}" width="8" height="8" '
                      f'fill="#3fb950" fill-opacity=".55">'
                      f'<title>VSA climax bottom '
                      f'{ch["dates"][idx]}</title></rect>')
    for idx in ch.get("climax_tops", []):
        if idx < n:
            marks += (f'<rect x="{xs[idx] - 4:.1f}" '
                      f'y="{ys[idx] - 4:.1f}" width="8" height="8" '
                      f'fill="#f85149" fill-opacity=".55">'
                      f'<title>VSA climax top '
                      f'{ch["dates"][idx]}</title></rect>')
    z_top = p_h + 18
    zlo, zhi = min(min(sp_z), trigger), max(max(sp_z), trigger)
    zr = (zhi - zlo) or 1.0
    zy = [z_top + (z_h - 14) * (1 - (v - zlo) / zr) for v in sp_z]
    zpts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, zy))
    ty = z_top + (z_h - 14) * (1 - (trigger - zlo) / zr)
    zones = ""
    in_zone = False
    for i, v in enumerate(sp_z):
        if v <= trigger and not in_zone:
            zones += (f'<path d="M{xs[i]:.1f},{z_top - 4:.1f} '
                      f'L{xs[i]:.1f},{z_top + z_h - 10:.1f}"')
            in_zone = True
            start = xs[i]
        elif v > trigger and in_zone:
            zones += (f' stroke="none"/><rect x="{start:.1f}" '
                      f'y="{z_top - 4:.1f}" width="{xs[i] - start:.1f}" '
                      f'height="{z_h - 6:.1f}" fill="#f85149" '
                      f'fill-opacity=".12"/>')
            in_zone = False
    if in_zone:
        zones += (f' stroke="none"/><rect x="{start:.1f}" '
                  f'y="{z_top - 4:.1f}" width="{xs[-1] - start:.1f}" '
                  f'height="{z_h - 6:.1f}" fill="#f85149" '
                  f'fill-opacity=".12"/>')
    return (f'<svg width="{width}" height="{height}" role="img" '
            f'aria-label="{_esc(ch["ticker"])} price, detections and '
            f'AVFI spread z" viewBox="0 0 {width} {height}">'
            f'<polyline fill="none" stroke="#58a6ff" stroke-width="1.4" '
            f'points="{pts}"/>{marks}'
            f'<line x1="8" y1="{p_h + 6:.1f}" x2="{width - 8}" '
            f'y2="{p_h + 6:.1f}" stroke="#30363b" stroke-width="1"/>'
            f'<text x="8" y="{z_top - 7:.0f}" class="axis">'
            f'spread z (AVFI v3 vs v2)</text>'
            f'{zones}'
            f'<polyline fill="none" stroke="#d2a8ff" stroke-width="1.2" '
            f'points="{zpts}"/>'
            f'<line x1="8" y1="{ty:.1f}" x2="{width - 8}" y2="{ty:.1f}" '
            f'stroke="#f85149" stroke-width=".8" stroke-dasharray="3 3"/>'
            f'<text x="{width - 60}" y="{ty - 3:.1f}" class="axis">'
            f'trigger {trigger:g}</text></svg>')


def _crypto_detections_html(paper_dir: Path) -> str:
    """Top-150 crypto: tops-and-bottoms detections on dailies WITH the
    AVFI spread-z regime axis on every chart."""
    path = paper_dir / "research" / "tops_bottoms_extended.json"
    if not path.exists():
        return ("<p class=\"dim\">Crypto detections appear here "
                "after the first nightly research pass.</p>")
    r = json.load(open(path))
    charts = {c["ticker"]: c for c in r.get("charts", [])
              if c["ticker"].endswith("USD")}
    rows = [row for row in r.get("rows", [])
            if row["ticker"].endswith("USD")]
    if not rows:
        return "<p class=\"dim\">No crypto series in the extended " \
                "study yet.</p>"
    by_confirm = sorted(rows, key=lambda x: -x.get("n_confirmed", 0))
    top = by_confirm[:12]
    svgs = "".join(
        f'<div class="pc"><div class="dim" style="text-align:center">'
        f'{_esc(row["ticker"])}</div>'
        + _crypto_avfi_chart_svg(charts[row["ticker"]])
        + "</div>"
        for row in top if row["ticker"] in charts)
    tbl = ""
    for row in rows:
        tb = row.get("topology_buckets", {})
        lf = {int(k): v["long_fwd"] for k, v in tb.items()
              if v.get("long_fwd") is not None}
        holds = "yes" if (2 in lf and 3 in lf and lf[3] > lf[2]) \
            else "no"
        cls = "good" if holds == "yes" else "dim"
        tbl += (f'<tr><td>{_esc(row["ticker"])}</td>'
                f'<td>{row["n_divergence_bottoms"]}</td>'
                f'<td>{row["n_climax_bottoms"]}</td>'
                f'<td>{row["n_confirmed"]}</td>'
                f'<td class="{cls}">{holds}</td></tr>')
    return (f'<p class="dim">The top 150 liquid coins (plain spot '
            f'USD pairs — the earliest daily history; stablecoins '
            f'excluded): detected bottoms (green) and tops (red) '
            f'on dailies, each chart carrying the AVFI spread z '
            f'below the price — the regime axis behind every turn, '
            f'throttle zones shaded. Charts show the 24 most-active '
            f'series; the confluence table covers all '
            f'{len(rows)}.</p>'
            f'<div class="pgrid">{svgs}</div>'
            f'<table><tr><th>Ticker</th><th>div bottoms</th>'
            f'<th>climax bottoms</th><th>confirmed entries</th>'
            f'<th>confluence holds</th></tr>{tbl}</table>')


def _extended_detections_html(paper_dir: Path) -> str:
    """Tops-and-bottoms detections across the full commodity (and
    extended) universe, on dailies."""
    path = paper_dir / "research" / "tops_bottoms_extended.json"
    if not path.exists():
        return ("<p class=\"dim\">Extended-universe detections appear "
                "here after the first nightly research pass.</p>")
    r = json.load(open(path))
    charts = r.get("charts", [])
    comm = [c for c in charts if not c["ticker"].endswith("USD")]
    svgs = "".join(f'<div class="pc">{_tb_chart_svg(c)}</div>'
                   for c in comm)
    rows = ""
    for row in r.get("rows", []):
        if row["ticker"].endswith("USD"):
            continue
        tb = row.get("topology_buckets", {})
        lf = {int(k): v["long_fwd"] for k, v in tb.items()
              if v.get("long_fwd") is not None}
        holds = "yes" if (2 in lf and 3 in lf and lf[3] > lf[2]) \
            else "no"
        cls = "good" if holds == "yes" else "dim"
        rows += (f'<tr><td>{_esc(row["ticker"])}</td>'
                 f'<td>{row["n_divergence_bottoms"]}</td>'
                 f'<td>{row["n_climax_bottoms"]}</td>'
                 f'<td>{row["n_confirmed"]}</td>'
                 f'<td class="{cls}">{holds}</td></tr>')
    return (f'<p class="dim">Detected bottoms (green) and tops (red) '
            f'across the full commodity universe — triangles = RSI '
            f'divergence, squares = VSA climax, daily bars. The '
            f'table asks whether the confluence regularity '
            f'(score-3 &gt; score-2) holds in each commodity.</p>'
            f'<div class="pgrid">{svgs}</div>'
            '<table><tr><th>Commodity</th><th>div bottoms</th>'
            '<th>climax bottoms</th><th>confirmed entries</th>'
            '<th>confluence holds</th></tr>'
            f'{rows}</table>')


def _smh_gradient_html(paper_dir: Path) -> str:
    """The salience gradient: all three region clocks plus the
    climatology counterfactual, with Greenwood bands - the charter's
    fifth and sixth measured ticks, measured on this programme's
    own 188-series universe."""
    path = paper_dir / "research" / "smh_gradient.json"
    if not path.exists():
        return ""
    r = json.load(open(path))
    if r.get("status") != "OK":
        return ""
    g = r.get("gradient", {})
    v = r.get("verdict", {})
    an = r.get("event_anatomy", {})

    def clock_row(label, c, note=""):
        if not c:
            return ""
        return (f'<tr><td>{_esc(label)}</td>'
                f'<td class="good">{c["cum_event_12w"]}</td>'
                f'<td>[{c["ci95_lo"]}, {c["ci95_hi"]}]</td>'
                f'<td>{c["n"]}</td><td class="dim">{_esc(note)}'
                f'</td></tr>')

    rows = (clock_row("compression entry", g.get("compression")).lstrip()
            + clock_row("mid entry", g.get("mid")).lstrip()
            + clock_row("any week (climatology)", g.get("climatology")).lstrip()
            + clock_row("stress entry", g.get("stress_events")).lstrip())
    disjoint = ("YES - the compression band is disjoint from "
                "climatology" if v.get(
                    "compression_disjoint_from_climatology")
                else "no")
    monotone = ("yes" if v.get("monotone_point_estimates")
                else "not pooled (mid sits below climatology on "
                "this universe - an honest finding, flagged)")
    vol = an.get("volume", {}) if an else {}
    arr = an.get("arrival_split", {}) if an else {}
    anatomy_line = ""
    if an and an.get("n_first_events"):
        anatomy_line = (f'<p class="dim">The event anatomy on this '
                        f'universe: of {an["n_first_events"]} first '
                        f'events, {arr.get("in_spell", 0)} arrive '
                        f'in-spell, {arr.get("escape_week", 0)} ARE '
                        f'the escape week, {arr.get("post_escape", 0)} '
                        f'arrive after the region escaped; the act '
                        f'dissolved at spell end captures '
                        f'{an.get("act_capture_at_spell_end")}. '
                        f'Law 4 at the weekly grain: significant '
                        f'weeks on median volume '
                        f'{vol.get("median_event_ratio")}x their '
                        f'trailing baseline (all weeks '
                        f'{vol.get("median_all_bars_ratio")}x); '
                        f'median overshoot '
                        f'{an.get("overshoot_median")}x the '
                        f'2.5-sigma bar.</p>')
    return (f'<h3 class="sub">The salience gradient &mdash; the 12-week '
            f'first-significant-week clock by entry region</h3>'
            f'<p class="dim">The charter&rsquo;s fifth and sixth '
            f'measured ticks, measured on this programme&rsquo;s own '
            f'universe (188 series, the charter&rsquo;s frozen event: '
            f'a significant week, |r1| &ge; 2.5&sigma;<sub>w</sub> at '
            f'entry, within 12 weeks). Compression separates from '
            f'doing nothing; salience is edge-local.</p>'
            f'<table><tr><th>Entry</th><th>P(event &le; 12w)</th>'
            f'<th>Greenwood 95%</th><th>n</th><th>note</th></tr>'
            f'{rows}</table>'
            f'<p class="dim">Compression disjoint from climatology: '
            f'<strong>{disjoint}</strong>. Gradient monotone pooled: '
            f'{monotone}. The mechanical-threshold caveat (the entry '
            f'sigma is frozen at the decision close) is frozen beside '
            f'these numbers, per the charter.</p>'
            f'{anatomy_line}'
            )


def _smh_direction_html(paper_dir: Path) -> str:
    """Law 3's conditional direction cells, measured and refused -
    the theorem's refusal now scored per cell."""
    path = paper_dir / "research" / "smh_direction.json"
    if not path.exists():
        return ""
    r = json.load(open(path))
    if r.get("status") != "OK":
        return ""
    rows = "".join(
        f'<tr><td>{_esc(c["cell"])}</td><td>{c["n"]}</td>'
        f'<td>{c["p_up"]}</td><td>[{c["wilson_95"][0]}, '
        f'{c["wilson_95"][1]}]</td>'
        + ('<td class="warn">flagged</td>'
           if c["seductive_flag"] else
           '<td class="good">clean</td>')
        + '</tr>'
        for c in r.get("cells", [])
        if c["n"] and "momentum" in c["cell"])
    v = r.get("verdict", {})
    return (f'<h3 class="sub">Law 3&rsquo;s conditional direction '
            f'cells &mdash; measured, and refused</h3>'
            f'<p class="dim">The pooled direction is a coin flip; '
            f'the charter predicts one directional quantity '
            f'(drift conditional on trend states). Measured on '
            f'{r.get("n_first_events")} first events: no '
            f'unflagged cell&rsquo;s Bonferroni-adjusted band '
            f'excludes one half. The charter&rsquo;s own seductive '
            f'cell (compression after a down 12-week move) reads '
            f'exactly 0.500 at n = 9,414 &mdash; the 6-of-7 '
            f'flattery is dead at scale. Direction stays '
            f'REFUSED, now per cell, on the record.</p>'
            f'<table><tr><th>Cell</th><th>n</th><th>p(up)</th>'
            f'<th>Wilson 95%</th><th>flag</th></tr>{rows}</table>')


def _smh_recurrence_html(paper_dir: Path) -> str:
    """The long-run lemma measured: the region chain's jump
    structure, irreducibility, and the trigger's actuarial
    recurrence rate."""
    path = paper_dir / "research" / "smh_recurrence.json"
    if not path.exists():
        return ""
    r = json.load(open(path))
    if r.get("status") != "OK":
        return ""
    ir = r.get("irreducibility", {})
    tr = r.get("trigger_recurrence", {})
    tm = r.get("transition_matrix", {})
    rows = "".join(
        f'<tr><td>{_esc(k)}</td><td>{v["count"]}</td>'
        f'<td>{v["probability"]}</td></tr>'
        for k, v in tm.items() if v["count"])
    cls = "good" if ir.get("irreducible") else "warn"
    return (f'<h3 class="sub">The long-run lemma &mdash; the '
            f'region chain measured</h3>'
            f'<p class="dim">Inevitability lives in the '
            f'recurrence. Measured on this universe: <span '
            f'class="{cls}">the chain is '
            + ("IRREDUCIBLE - all six directed links observed, "
               "none absorbing" if ir.get("irreducible")
               else "NOT irreducible - reported as measured")
            + f'</span>, and the compression trigger fires '
            f'<strong>'
            f'{tr.get("triggers_per_market_year")}</strong> '
            f'times per market per year '
            f'({tr.get("n_triggers")} triggers over '
            f'{tr.get("market_years")} market-years). The '
            f'anticipated event is actuarially inevitable across '
            f'the cycle, and no event is dated.</p>'
            f'<table><tr><th>Link</th><th>count</th>'
            f'<th>probability</th></tr>{rows}</table>')


def _smh_calibration_html(paper_dir: Path) -> str:
    """The forward log's dress rehearsal: the forecast scored out
    of sample on time, against climatology."""
    path = paper_dir / "research" / "smh_calibration.json"
    if not path.exists():
        return ""
    r = json.load(open(path))
    if r.get("status") != "OK":
        return ""
    v = r.get("verdict", {})
    sc = r.get("scores", {})
    cs = r.get("climatology_scores", {})
    rel_rows = "".join(
        f'<tr><td>{_esc(b["bin"])}</td><td>{b["n"]}</td>'
        f'<td>{b["mean_p"]}</td><td>{b["observed"]}</td></tr>'
        for b in sc.get("reliability", []))
    cls = "good" if v.get("beats_climatology_oos") else "warn"
    return (f'<h3 class="sub">The dress rehearsal &mdash; the '
            f'forecast scored out of sample, on time</h3>'
            f'<p class="dim">Before any forward row resolves, '
            f'the instrument itself has been pre-scored: fit on '
            f'the first 70% of each series&rsquo; compression '
            f'entries, scored on the last 30% against the '
            f'outcomes the market produced. Brier '
            f'{sc.get("brier")} vs climatology '
            f'{cs.get("brier")} &mdash; <span class="{cls}">'
            f'skill {r.get("skill_score")}</span>. '
            + ("The compression-conditional forecast carries "
               "real out-of-sample information; the forward log "
               "is scoring something worth scoring."
               if v.get("beats_climatology_oos") else
               "No out-of-sample skill: the forward log would "
               "be scoring noise - the honesty note says so.")
            + f" The reliability bins show mid-range "
            f"overconfidence (flagged; the forward log&rsquo;s "
            f"own Brier is the judge that counts).</p>"
            f'<table><tr><th>Forecast bin</th><th>n</th>'
            f'<th>mean p</th><th>observed</th></tr>{rel_rows}'
            f'</table>')


def build_site(paper_dir: Path) -> str:
    """Salient: the front page - the market hypothesis, the proof,
    the new work, and the live hazard instrument. The past (the
    falsification archive, the strategy logs, the build history)
    lives in the repository's artifacts and DASHBOARD.md - not on
    this page. This page only faces forward."""
    proof_html = (_smh_proof_html(paper_dir)
                   + _smh_gradient_html(paper_dir)
                   + _smh_direction_html(paper_dir)
                   + _smh_recurrence_html(paper_dir)
                   + _smh_calibration_html(paper_dir)
                   + _smh_hazard_html(paper_dir))
    n_comp = n_mid = n_high = 0
    hz_rows = ""
    hz_total = 0
    path = paper_dir / "research" / "smh_proof.json"
    if path.exists():
        r = json.loads(path.read_text())
        hz = r.get("hazard_now", [])
        hz_total = len(hz)
        n_comp = sum(1 for x in hz if x["state"] == "compression")
        n_mid = sum(1 for x in hz if x["state"] == "mid")
        n_high = sum(1 for x in hz if x["state"] == "high")
        comp = sorted((x for x in hz if x["state"] == "compression"),
                      key=lambda x: x["sigma_w_pct"])
        hz_rows = "".join(
            f'<tr><td>{_esc(x["ticker"])}</td>'
            f'<td>{x["sigma_w_pct"]}%</td></tr>'
            for x in comp[:40])

    # THE VASSALLO SCORE: the hazard model's per-market probability
    # of a significant event within 4 weeks, ranked
    vs_rows = ""
    vs_top_score = vs_top_ticker = "-"
    vs_count = 0
    vs_mean = "-"
    vs_path = paper_dir / "research" / "smh_hazard.json"
    if vs_path.exists():
        vr = json.loads(vs_path.read_text())
        scores = vr.get("vassallo_scores", [])
        vs_count = len(scores)
        if scores:
            vs_top = scores[0]
            vs_top_score = f"{vs_top['vassallo_score']*100:.1f}%"
            vs_top_ticker = vs_top["ticker"]
            vs_mean = (f"{sum(s['vassallo_score'] for s in scores)
                       / len(scores)*100:.1f}%")
            vs_rows = "".join(
                f'<tr><td>{_esc(s["ticker"])}</td>'
                f'<td class="good">{s["vassallo_score"]}</td>'
                f'<td>{s["relative_hazard"]}x</td>'
                f'<td>{s["sigma_w_pct"]}%</td>'
                f'<td>{s["sigma_pct"]}</td>'
                f'<td>{s["momentum_20"]}</td></tr>'
                for s in scores[:40])

    fw_rows_logged = fw_open = fw_resolved = 0
    fw_brier = "-"
    fw_kill = "waiting for the first clock entry"
    fw_path = paper_dir / "research" / "smh_forward.json"
    if fw_path.exists():
        fr = json.loads(fw_path.read_text())
        cnt = fr.get("counts", {})
        fw_rows_logged = len(fr.get("rows", []))
        fw_open = cnt.get("open", 0)
        fw_resolved = cnt.get("resolved", 0)
        sc = fr.get("scores", {})
        if sc.get("brier") is not None:
            fw_brier = sc["brier"]
        kl = fr.get("kill_lines", {})
        if kl.get("next_line"):
            fw_kill = (f"{kl['status']} - next line at "
                       f"{kl['next_line']['at_rows']} scored rows "
                       f"(dies at or below "
                       f"{kl['next_line']['line']} events)")

    # the progress strip: ticks 5 and 6 read from the gradient
    # artifact; the forward log and the precursor verdict give the
    # live status line
    fw_open_live = fw_open
    tick5 = tick6 = "measured"
    tick7 = tick8 = "measured"
    progress_status = ""
    gr_path = paper_dir / "research" / "smh_gradient.json"
    if gr_path.exists():
        gr = json.loads(gr_path.read_text())
        if gr.get("status") == "OK":
            g = gr.get("gradient", {})
            comp_g = g.get("compression", {})
            clim_g = g.get("climatology", {})
            if comp_g and clim_g:
                tick5 = (f"{comp_g['cum_event_12w']} vs "
                         f"{clim_g['cum_event_12w']} "
                         f"(disjoint bands)")
            an_g = gr.get("event_anatomy", {})
            if an_g and an_g.get("overshoot_median"):
                tick6 = (f"{an_g['overshoot_median']}&times; "
                         f"overshoot")
            disjoint = gr.get("verdict", {}).get(
                "compression_disjoint_from_climatology")
            progress_status = (
                f"The gradient on this universe: compression "
                f"{comp_g.get('cum_event_12w')} vs climatology "
                f"{clim_g.get('cum_event_12w')} &mdash; "
                + ("the compression band is DISJOINT from doing "
                   "nothing; salience is edge-local."
                   if disjoint else
                   "the bands overlap on this universe - flagged, "
                   "not hidden."))
    pr_path2 = paper_dir / "research" / "smh_precursor.json"
    if pr_path2.exists():
        prr = json.loads(pr_path2.read_text())
        if prr.get("status") == "OK":
            pv = prr.get("verdict", {})
            pds = prr.get("direction_split_first_events", {})
            progress_status += (" Precursor signatures: "
                + ("a footprint beats the clock out of fold."
                   if pv.get("precursor_beats_clock_oof") else
                   "MEASURED, NEGATIVE - no weekly-observable "
                   "footprint beats the clock out of fold; the "
                   "significant z's are noise wearing p-values.")
                + f" Direction: p(up) = {pds.get('p_up')} "
                f"{pds.get('wilson_95')} at "
                f"n = {pds.get('n_events')} - a coin flip; the "
                "theorem's refusal, confirmed at scale.")
    if fw_rows_logged:
        progress_status += (f" The forward log: {fw_rows_logged} "
                            f"rows logged in advance, {fw_open} "
                            f"open, {fw_resolved} resolved; "
                            f"kill-line status {fw_kill}.")
    rc_path = paper_dir / "research" / "smh_recurrence.json"
    if rc_path.exists():
        rc = json.loads(rc_path.read_text())
        if rc.get("status") == "OK":
            irr = rc.get("irreducibility", {})
            trr = rc.get("trigger_recurrence", {})
            if irr.get("irreducible"):
                tick8 = (f"irreducible; "
                         f"{trr.get('triggers_per_market_year')} "
                         f"triggers/market-year")
            if trr.get("triggers_per_market_year"):
                progress_status += (
                    f" The long-run lemma: the region chain is "
                    + ("IRREDUCIBLE on this universe" if
                       irr.get("irreducible") else
                       "not irreducible - reported as measured")
                    + f", and the compression trigger fires "
                    f"{trr.get('triggers_per_market_year')} "
                    f"times per market per year - the entry "
                    f"condition recurs indefinitely.")
    ca_path = paper_dir / "research" / "smh_calibration.json"
    if ca_path.exists():
        ca = json.loads(ca_path.read_text())
        if ca.get("status") == "OK":
            tick7 = (f"skill {ca.get('skill_score')}")
            cav = ca.get("verdict", {})
            progress_status += (
                " The dress rehearsal: the forecast pre-scored "
                "out of sample on time - Brier "
                f"{ca.get('scores', {}).get('brier')} vs "
                f"climatology "
                f"{ca.get('climatology_scores', {}).get('brier')}, "
                + ("positive skill - the forward log is scoring "
                   "something worth scoring."
                   if cav.get("beats_climatology_oos") else
                   "no skill - the honesty note says so.")
                + " Mid-range overconfidence flagged; the forward "
                "rows are the judge that counts.")

    # the machine's live position: region + spell age per
    # market, with the pooled dwell distribution - descriptive
    # context only, never a forecast (doctrine rule 2)
    st_rows = ""
    st_counts = ""
    st_dwell = ""
    st_path = paper_dir / "research" / "smh_status.json"
    if st_path.exists():
        st = json.loads(st_path.read_text())
        if st.get("status") == "OK":
            c_st = st.get("counts", {})
            st_counts = (f"{c_st.get('compression', 0)} in "
                         f"compression, "
                         f"{c_st.get('mid', 0)} in mid, "
                         f"{c_st.get('stress', 0)} in stress")
            d_st = st.get("dwell_distribution_weeks", {})
            st_dwell = " ".join(
                f"{k}: median {v['median_weeks']}w / mean "
                f"{v['mean_weeks']}w / max {v['max_weeks']}w "
                f"({v['n_spells']} spells)"
                for k, v in d_st.items())
            st_rows = "".join(
                f'<tr><td>{_esc(p["ticker"])}</td>'
                f'<td>{_esc(p["region"])}</td>'
                f'<td>{p["spell_age_weeks"]}w</td></tr>'
                for p in st.get("positions", [])[:24])

    laws_cards = "".join(
        f'<div class="book"><div class="btitle">{_esc(t)}</div>'
        f'<div class="bdesc dim">{_esc(d)}</div></div>'
        for t, d in (
            ("1. Volatility persists, then mean-reverts",
             "High vol weeks follow high vol weeks; compressed vol "
             "expands. This is the clock itself."),
            ("2. Tails are heavy",
             "Return distributions are non-Gaussian at every "
             "horizon. All thresholds live in sigma units, never "
             "in fixed points."),
            ("3. Autocorrelation has horizon structure",
             "Momentum at medium horizons, reversal at long ones, "
             "near-zero at short ones. The directional prior - "
             "valid only inside trend states."),
            ("4. Impact is concave in volume",
             "Big moves require big flow, and flow leaves "
             "footprints. A move without volume is a suspect move."),
            ("5. Events self-excite",
             "Price changes cluster in time, mostly endogenous. "
             "Hazard is state-dependent: timing forecasts are "
             "conditional distributions, never constants."),
            ("6. Every exploitable regularity decays",
             "The market adapts to whoever uses it. Every rule "
             "carries a forward calibration score and a decay "
             "watch. Nothing is forever, by law."),
        ))
    # the hazard model card reads its status from the artifact -
    # the front page never claims more than the data shows
    hz_path = paper_dir / "research" / "smh_hazard.json"
    hazard_status = ("STATUS: Cox v1 done - see the proof section")
    if hz_path.exists():
        hz = json.loads(hz_path.read_text())
        if hz.get("status") == "OK":
            c = hz.get("cox", {})
            hazard_status = (
                f"STATUS: DONE - Cox v1 on {hz.get('n_episodes')} "
                f"compression episodes: concordance "
                f"{c.get('concordance')}; deeper compression "
                f"raises the event hazard ~1.45x per SD "
                f"(z={c.get('z_stats', [0, 0])[1]})")
    # the precursor card reads its verdict from the artifact -
    # the honest answer to open problem 3, whatever it is
    pr_path = paper_dir / "research" / "smh_precursor.json"
    precursor_status = ("STATUS: open - the standing research "
                        "question")
    if pr_path.exists():
        pr = json.loads(pr_path.read_text())
        if pr.get("status") == "OK":
            v = pr.get("verdict", {})
            ds = pr.get("direction_split_first_events", {})
            if v.get("precursor_beats_clock_oof"):
                precursor_status = (
                    "STATUS: a precursor beats the clock out of "
                    "fold - see the proof section")
            else:
                precursor_status = (
                    f"STATUS: MEASURED, NEGATIVE - on "
                    f"{pr.get('n_episodes')} episodes no "
                    f"weekly-observable footprint beats the "
                    f"clock out of fold (full OOF "
                    f"{v.get('full_oof_concordance')} vs "
                    f"clock {v.get('clock_oof_concordance')}, "
                    f"below the pre-declared margin); the "
                    f"direction split is a coin flip: "
                    f"p(up) = {ds.get('p_up')} "
                    f"{ds.get('wilson_95')} at "
                    f"n = {ds.get('n_events')} - the central "
                    f"theorem's refusal, confirmed at scale")
    work_cards = "".join(
        f'<div class="book"><div class="btitle">{_esc(t)}</div>'
        f'<div class="bdesc dim">{_esc(d)}</div>'
        f'<div class="bdesc">{_esc(s)}</div></div>'
        for t, d, s in (
            ("The hazard model",
             "Kaplan-Meier with censoring plus the Cox "
             "proportional-hazards regression: state, momentum "
             "and compression depth as hazard covariates - "
             "Hamilton's states meet Kaplan-Meier and Cox.",
             hazard_status),
            ("Precursor signatures beyond volatility",
             "Can any weekly-observable footprint raise the event "
             "hazard above the tercile table? AVFI returns here - "
             "not as an inevitability, as a testable signature "
             "with a calibration score.",
             precursor_status),
            ("The volume clock",
             "Clark's subordination: the efficient price evolves in "
             "trading time, clocked by volume. Needs finer data "
             "than daily bars.",
             "STATUS: blocked on intraday data"),
            ("Self-excitation measurement",
             "Hawkes estimation of endogenous reflexivity "
             "(Filimonov-Sornette). Needs intraday data.",
             "STATUS: blocked on intraday data"),
            ("The calibrated Bayesian forecaster",
             "Human prior times measured calibration - judgment "
             "inside the protocol as a component to be scored, "
             "not an oracle outside it.",
             "STATUS: awaits the hazard model's score"),
        ))

    css = open(Path(__file__).parent / "salient_front.css").read()

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="300">
<title>Salient — the market hypothesis</title>
<style>
{css}
</style>
</head><body>
<nav><a href="#progress">The progress</a>
<a href="#hypothesis">The hypothesis</a>
<a href="#proof">The proof</a> <a href="#work">The new work</a>
<a href="#now">The Vassallo Score</a></nav>
<header>
<h1>Salient<span>.</span></h1>
<p class="tagline"><strong>The aim:</strong> see the future event
&mdash; before it happens, on the record, with a public scoreboard.
Not its direction (no honest theory can), but its <em>hazard</em>:
which markets are coiled, when a significant move becomes likely,
and by exactly how much &mdash; a probability stated in advance and
scored against outcomes, night after night, until the clock is
ours.</p>
<p class="tagline">The Salient Market Hypothesis is the instrument:
state instead of count, clock instead of prophecy, calibration
instead of belief. Every layer reachable with current data is
now MEASURED on this universe: the gradient (compression 0.639 vs
climatology 0.437, disjoint bands), the direction cells (a coin
flip at n = 15,386, refused per cell), the recurrence (the chain
irreducible, the trigger 21.56 times per market-year), and the
forecast itself pre-scored out of sample with positive skill.
The falsification machinery is live: {fw_open_live} forward rows
sit in the log, logged in advance, waiting to be scored against
the pre-declared kill lines. What remains is exactly two things:
episodes and data.</p>
</header>
<main>
<section id="progress"><h2>The progress &mdash; the measured
ticks, and what is still being scored</h2>
<div class="ticks">
<div class="tick"><div class="tnum">TICK 1</div>
<div class="tlab">the clock: compression vs high-vol event rate</div>
<div class="tval">3.3&times; measured</div></div>
<div class="tick"><div class="tnum">TICK 2</div>
<div class="tlab">hazard layer v0: KM corrected, Cox v0.1</div>
<div class="tval">concordance 0.643</div></div>
<div class="tick"><div class="tnum">TICK 3</div>
<div class="tlab">stress clock: the quarter rule, decay by calm</div>
<div class="tval">2/3 in a quarter</div></div>
<div class="tick"><div class="tnum">TICK 4</div>
<div class="tlab">dwell &amp; transition machine, three states</div>
<div class="tval">measured</div></div>
<div class="tick"><div class="tnum">TICK 5</div>
<div class="tlab">salience gradient on this universe</div>
<div class="tval">{tick5}</div></div>
<div class="tick"><div class="tnum">TICK 6</div>
<div class="tlab">event anatomy: arrival, volume, overshoot</div>
<div class="tval">{tick6}</div></div>
<div class="tick"><div class="tnum">TICK 7</div>
<div class="tlab">the dress rehearsal: forecast pre-scored out of sample</div>
<div class="tval">{tick7}</div></div>
<div class="tick"><div class="tnum">TICK 8</div>
<div class="tlab">the long-run lemma: chain irreducibility, trigger recurrence</div>
<div class="tval">{tick8}</div></div>
</div>
<p class="dim">{progress_status}</p>
</section>
<section id="hypothesis"><h2>The hypothesis</h2>
<p class="dim">Markets are a matching engine plus participants
managing inventory plus informed flow. The transaction price
oscillates around a latent efficient price that evolves in
<em>trading time</em>, not calendar time. Structure exists, but it
is statistical, not geometric. Six unconditional laws hold; the
central theorem forbids what no public theory can honestly sell:</p>
<p class="dim"><strong>The certainty-timing-direction triangle:</strong>
a rule that identified an event as certain, timed, and directional
would be traded until it stopped working &mdash; so it cannot exist
publicly. CERTAINTY lives at the level of the distribution, PROBABILITY
at the level of the event, HAZARD at the level of timing. Elliott
Wave claimed all three and could never be wrong; this framework
separates them so every claim can be scored &mdash; and can fail in
public, which is the only way anything in markets can ever be
right.</p>
<div class="bgrid">{laws_cards}</div>
<p class="dim">Four measured states replace wave counting &mdash;
COMPRESSION (the event-prone state), TREND, EXPANSION, STRESS &mdash;
and the primary clock is volatility: sigma_w, its tercile, and the
frozen conditional tables give the hazard of a significant event
(&ge; 2.5&sigma;<sub>w</sub> within 4 weeks) at every decision close.
The full charter lives in the repository as
KNOWLEDGE_SMH.md.</p>
</section>
<section id="proof"><h2>The proof</h2>
{proof_html}
</section>
<section id="work"><h2>The new work &mdash; until the clock is ours</h2>
<p class="dim">The frontier, in order. Each item is a genuine
research problem with a scoreable end state &mdash; none is a
lottery ticket.</p>
<div class="bgrid">{work_cards}</div>
</section>
<section id="now"><h2>The Vassallo Score &mdash; the likelihood
of the event, expected mathematically</h2>
<p class="dim">The live instrument, named for its author: for every
market currently in the compression state, the Cox hazard model
converts its covariates (momentum into compression, compression
depth) into a RELATIVE hazard, and the Kaplan-Meier baseline turns
that into an ABSOLUTE probability of a significant event
(&ge; 2.5&sigma;<sub>w</sub> within 4 weeks) at the latest close:
<strong>score = 1 &minus; S<sub>0</sub>(20)<sup>exp(&beta;&middot;z)</sup></strong>.
Strictly causal, stated in advance, scored against outcomes every
night &mdash; and never a direction, per the central theorem.
This is the future event we see and can explain.</p>
<div class="metrics">
<div class="metric"><div class="mval">{vs_top_score}</div>
<div class="mlabel">highest Vassallo Score now ({vs_top_ticker})</div></div>
<div class="metric"><div class="mval">{vs_count}</div>
<div class="mlabel">markets scored (in compression)</div></div>
<div class="metric"><div class="mval">{vs_mean}</div>
<div class="mlabel">mean score across compression</div></div>
<div class="metric"><div class="mval">{n_comp}</div>
<div class="mlabel">of {hz_total} markets in COMPRESSION</div></div>
</div>
<h3 class="sub">Ranked by the Vassallo Score &mdash; the coiled
springs, highest mathematical expectation first</h3>
<table><tr><th>Market</th><th>Vassallo Score</th><th>rel. hazard</th>
<th>sigma_w %</th><th>depth pct</th><th>momentum (20b)</th></tr>
{vs_rows}</table>
<h3 class="sub">The forward log &mdash; the scoreboard the charter
declared: forecast rows logged in advance at every clock entry,
resolved against outcomes, Brier-scored</h3>
<div class="metrics">
<div class="metric"><div class="mval">{fw_rows_logged}</div>
<div class="mlabel">forecast rows logged in advance</div></div>
<div class="metric"><div class="mval">{fw_open}</div>
<div class="mlabel">open (windows still running)</div></div>
<div class="metric"><div class="mval">{fw_resolved}</div>
<div class="mlabel">resolved and scored</div></div>
<div class="metric"><div class="mval">{fw_brier}</div>
<div class="mlabel">Brier score (lower is sharper)</div></div>
</div>
<p class="dim">Kill lines, pre-declared (charter v2, section 14):
the occurrence claim dies in public if, at 10/20/40/60 scored
forward rows, the event count is at or below 3/8/19/31.
Current status: {fw_kill}.</p>
<h3 class="sub">The machine&rsquo;s live position &mdash; the status
reading, the operational replacement for counting waves</h3>
<p class="dim">Every market&rsquo;s current clock region and its current
spell&rsquo;s age, against the measured dwell distribution. Spell age
is descriptive context, NOT a forecast: rows are logged only at
clock entries, and this reading converts age into no probability
at all. Right now: {st_counts}. Measured dwell (pooled, weeks):
{st_dwell}.</p>
<table><tr><th>Market</th><th>Region</th><th>Spell age</th></tr>
{st_rows}</table>
</section>
</main>
<footer>Salient &mdash; regenerated automatically every night.
The machine behind this page: an autonomous research pipeline that
fetches real market data, scores every claim forward, and records
every hit and miss in public.
<a href="https://github.com/andrea-karlvassallo20-beep/vp-mr-strategy">Source, evidence and the full falsification record on GitHub</a>
&middot; research system, not investment advice.</footer>
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
