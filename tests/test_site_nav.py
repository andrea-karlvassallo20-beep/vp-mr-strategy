"""The grouped navigation is the owner's information architecture.

Too many subtitles was the complaint (2026-11-16); the nav collapsed
from 14 flat links to 6 top-level entries via 4 collapsible groups.
These tests freeze that structure and prevent drift between the static
pages and the regenerated ones (heatmap, dormancy, resources).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import site_nav  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
NAV_PAGES = [
    "index.html", "manual.html", "causal.html", "clues.html",
    "criteria.html", "v4_charts.html", "heatmap.html", "dormancy.html",
    "ledger.html", "ohlcv_verdict.html", "math_verification.html",
    "resources.html", "books.html", "instrument.html",
    "program.html",
]


def test_render_six_top_level_entries():
    n = site_nav.render(None)
    assert n.count("<details") == 4          # 4 groups
    assert n.count("<a href") == 16          # all pages still reachable
    assert n.startswith("<nav>") and n.endswith("</nav>")


def test_render_marks_current_and_opens_its_group():
    n = site_nav.render("ledger.html")
    assert 'href="ledger.html" aria-current="page"' in n
    assert '<details class="navgroup" open>' in n  # the Record group opens


def test_all_site_pages_carry_the_grouped_nav():
    for page in NAV_PAGES:
        p = REPO_ROOT / "docs" / page
        assert p.exists(), page
        text = p.read_text(encoding="utf-8", errors="ignore")
        assert 'class="navgroup"' in text, f"{page} lost the grouped nav"
        # no page regressed to the old 14-flat-link nav
        assert 'The working manual</a>\n  <a href="causal.html"' not in text, (
            f"{page} carries the old flat nav"
        )


def test_no_dead_links_in_nav():
    for href, _ in site_nav.DIRECT + site_nav.DIRECT_AFTER:
        assert (REPO_ROOT / "docs" / href).exists(), href
    for _, links in site_nav.GROUPS:
        for href, _ in links:
            assert (REPO_ROOT / "docs" / href).exists(), href
