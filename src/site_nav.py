"""The grouped site navigation — one canonical renderer.

The owner's call (2026-11-16): too many subtitles. The nav had 14 flat
links; it now has 6 top-level entries (3 direct links + 3 collapsible
groups). Every page and every page generator imports THIS module so the
nav can never drift between the static pages and the regenerated ones
(heatmap, dormancy, resources).

Usage:
    from site_nav import render
    html = render("ledger.html")          # aria-current on that page's link
"""

from __future__ import annotations

# (href, label) pairs; groups render as <details class="navgroup">
DIRECT = [
    ("index.html", "Thesis"),
]
GROUPS = [
    ("The Manual", [
        ("manual.html", "The working manual"),
        ("causal.html", "Causal chains"),
        ("clues.html", "The clue dossier"),
        ("criteria.html", "The night-before sauce move"),
    ]),
    ("The Board", [
        ("v4_charts.html", "The board, colored"),
        ("heatmap.html", "The heat map"),
        ("dormancy.html", "The dormancy map"),
    ]),
    ("The Record", [
        ("ledger.html", "The claims ledger"),
        ("ohlcv_verdict.html", "The OHLCV verdict"),
        ("math_verification.html", "The math, verified"),
    ]),
    ("The Library", [
        ("resources.html", "The library"),
        ("books.html", "The books, taught"),
    ]),
]
DIRECT_AFTER = [
    ("instrument.html", "The instrument (live)"),
]

_STYLE = """
nav details.navgroup { display: inline-block; position: relative; }
nav details.navgroup summary { color: var(--dim); font-size: 14px;
  cursor: pointer; list-style: none; display: inline; user-select: none; }
nav details.navgroup summary::after { content: " \\25BE"; font-size: 10px; }
nav details.navgroup[open] summary { color: var(--accent); }
nav details.navgroup .navsub { display: flex; flex-direction: column;
  gap: 8px; position: absolute; left: 0; top: 24px; z-index: 30;
  background: rgba(7, 11, 18, .97); border: 1px solid var(--line);
  border-radius: 10px; padding: 12px 18px; min-width: 200px; }
"""


def style_css() -> str:
    """CSS block for the grouped nav (append to site.css or a page <style>)."""
    return _STYLE


def render(current: str | None = None) -> str:
    """Render the <nav>...</nav> block; `current` gets aria-current."""
    parts = ["<nav>"]
    for href, label in DIRECT:
        cur = ' aria-current="page"' if href == current else ""
        parts.append(f'  <a href="{href}"{cur}>{label}</a>')
    for group, links in GROUPS:
        hrefs = [h for h, _ in links]
        open_attr = ' open' if current in hrefs else ""
        parts.append(f'  <details class="navgroup"{open_attr}>')
        parts.append(f'    <summary>{group}</summary>')
        parts.append('    <div class="navsub">')
        for href, label in links:
            cur = ' aria-current="page"' if href == current else ""
            parts.append(f'      <a href="{href}"{cur}>{label}</a>')
        parts.append("    </div>")
        parts.append("  </details>")
    for href, label in DIRECT_AFTER:
        cur = ' aria-current="page"' if href == current else ""
        parts.append(f'  <a href="{href}"{cur}>{label}</a>')
    parts.append("</nav>")
    return "\n".join(parts)
