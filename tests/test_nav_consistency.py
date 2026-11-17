"""Nav rot is a named enemy of this site: three separate nav-rewrite
PRs (the manual/dormancy/library/ledger wave, the OHLCV/math wave, and
once before that) each rebuilt every page's nav from a stale list and
silently dropped a page — the heat map vanished from the sections
three times. This test makes the rot structurally impossible to merge:

  1. every docs/*.html that carries a <nav> must carry the SAME set of
     nav hrefs (the canonical nav); and
  2. every nav href must point at a page that exists; and
  3. the heat map generator's own NAV constant must match the pages.

A new page that adds itself to one nav but not the others fails here.
"""

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def _nav_hrefs(html):
    m = re.search(r"<nav>(.*?)</nav>", html, re.S)
    if not m:
        return None
    return frozenset(re.findall(r'href="([^"#]+)"', m.group(1)))


def test_every_nav_is_the_canonical_nav():
    pages = {}
    for f in sorted(DOCS.glob("*.html")):
        hrefs = _nav_hrefs(f.read_text())
        if hrefs is not None:
            pages[f.name] = hrefs
    assert pages, "no nav-bearing pages found"
    canonical = None
    for name, hrefs in pages.items():
        if canonical is None:
            canonical = hrefs
        assert hrefs == canonical, (
            f"{name} nav differs from the canonical set.\n"
            f"  missing: {sorted(canonical - hrefs)}\n"
            f"  extra:   {sorted(hrefs - canonical)}\n"
            "Every nav-bearing page must carry the same nav — a page "
            "dropped from one nav is a page vanished from the site.")


def test_nav_links_point_at_existing_pages():
    for f in sorted(DOCS.glob("*.html")):
        hrefs = _nav_hrefs(f.read_text())
        if hrefs is None:
            continue
        for h in hrefs:
            assert (DOCS / h).exists(), (
                f"{f.name} nav links to {h}, which does not exist")


def test_heatmap_generator_nav_matches_pages():
    import heatmap_page
    gen = frozenset(re.findall(r'href="([^"#]+)"', heatmap_page.NAV))
    for f in sorted(DOCS.glob("*.html")):
        hrefs = _nav_hrefs(f.read_text())
        if hrefs is None:
            continue
        assert gen == hrefs, (
            f"{f.name} nav differs from heatmap_page.NAV — the generated "
            "page would drop or add entries against the site's nav")
        break
