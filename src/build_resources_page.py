"""The Library page builder: the 100-resource list + the research-articles
catalogue, rendered in the site's style from the two plain-text data files.

Data files (kept as committed, human-editable text):
  docs/resources_data.txt         - 100 resources, 10 categories
  docs/articles_catalogue_data.txt- research articles catalogue

Honesty rules baked into the page: every record carries its verification
status (the catalogues themselves say "verify bibliographic details and
licenses before use" - the page repeats it); research leads and title
variants are flagged, not laundered; the articles catalogue is marked as
received-through-068-of-104 where applicable.
"""

import html
from pathlib import Path

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_nav import render as _render_nav

ROOT = Path(__file__).resolve().parents[1]

NAV = _render_nav("resources.html")

STYLE = """
body{background:#0b0e14;color:#c9d1d9;font-family:Georgia,serif;margin:0;padding:2rem;max-width:1200px;margin:auto}
h1{color:#fff;font-size:2.2rem;letter-spacing:.02em}
h2{color:#35ff9e;border-bottom:1px solid #24304a;padding-bottom:.3rem;margin-top:2.8rem}
h3{color:#fff;margin-bottom:.4rem}
table{border-collapse:collapse;width:100%;font-size:.83rem;margin:1rem 0}
th,td{border:1px solid #24304a;padding:.35rem .55rem;text-align:left;vertical-align:top}
th{background:#161b26;color:#35ff9e}
tr:nth-child(even) td{background:#11151f}
.note{color:#8b949e;font-size:.9rem;font-style:italic}
.tag{font-size:.7rem;padding:.05rem .4rem;border-radius:3px;margin-right:.4rem}
.core{background:#12351f;color:#35ff9e}
.high{background:#2b2313;color:#ffd166}
.lead{background:#3a1414;color:#ff8080}
a{color:#58a6ff}
"""


def esc(s):
    return html.escape(str(s or ""))


def link_of(url):
    if not url or url == "artefact":
        return ""
    if url.startswith("10."):
        return f'<a href="https://doi.org/{esc(url)}">doi</a>'
    return f'<a href="{esc(url)}">link</a>'


def build_resources_section():
    cats, cur = [], None
    for line in (ROOT / "docs/resources_data.txt").read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        if line[0].isalpha() and "." in line[:3]:
            cur = {"name": line, "items": []}
            cats.append(cur)
            continue
        head, why, link = [p.strip() for p in line.split("|")]
        num, _, title = head.partition(". ")
        cur["items"].append((num, title, why, link))
    parts = []
    for c in cats:
        rows = "\n".join(
            f"<tr><td>{n}</td><td><b>{esc(t)}</b><br>"
            f"<span class='note'>{esc(w)}</span></td>"
            f"<td>{link_of(l)}</td></tr>"
            for n, t, w, l in c["items"])
        parts.append(f"<h3>{esc(c['name'])}</h3>\n<table>{rows}</table>")
    return "\n".join(parts)


def build_articles_section():
    rows = []
    for line in (ROOT / "docs/articles_catalogue_data.txt").read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        f = [p.strip() for p in line.split("|")]
        # f0 = "NNN Tag"; f1 title; f2 authors; f3 category; f4 venue;
        # f5 doi (may be empty); optional f6 link; last field = relevance
        num, _, tag = f[0].partition(" ")
        title, authors, cat, venue = f[1], f[2], f[3], f[4]
        if len(f) >= 8:
            doi, rel = (f[5] or f[6]), f[7]
        else:
            doi, rel = f[5], f[6]
        cls = "lead" if "RESEARCH LEAD" in rel else tag.lower()
        rows.append(
            f"<tr><td>{esc(num)}</td>"
            f"<td><span class='tag {cls}'>{esc(tag)}</span>"
            f"<b>{esc(title)}</b><br>{esc(authors)} · {esc(venue)} · {esc(cat)}<br>"
            f"<span class='note'>{esc(rel)}</span></td>"
            f"<td>{link_of(doi)}</td></tr>")
    return f"<table>{''.join(rows)}</table>"


def main():
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Library — vp-mr-strategy</title>
<meta name="description" content="The library: the papers, datasets and tools behind the programme, with legal acquisition status for every one.">
<link rel="stylesheet" href="site.css">
<style>{STYLE}</style>
</head>
<body>
{NAV}

<div class="epigraph"><p>"You will not find the answer in a book. But you will find every wrong answer already tried — and that is most of the work."</p></div>

<main>
<div class="kicker">100 resources &middot; 68 research articles &middot; verified status on every record</div>
<h1>The Library<span class="dot">.</span></h1>

<p class="note">Two catalogues: the hundred resources the programme draws on (data, macro, search, microstructure, state-space, validation, optimal transport, nonlinear dynamics, software, and the Salient artefact checklists), and the research-articles catalogue. Every record carries its verification status — bibliographic details and licenses are to be verified against the publisher before formal use; research leads and title variants are flagged, never laundered. The articles catalogue was received through record 068 of 104; the remainder is pending from the owner.</p>

<h2>1 &middot; The hundred resources</h2>
{build_resources_section()}

<h2>2 &middot; The research-articles catalogue</h2>
<p class="note">Tags: <span class="tag core">Core</span> load-bearing for the programme's claims; <span class="tag high">High</span> high-value context; <span class="tag lead">Lead</span> research lead — citation to be verified before any formal use. All records: verify DOI/venue against the publisher before citing.</p>
{build_articles_section()}

<h2>3 &middot; What this page cannot tell you</h2>
<p class="note">That any listed method works on our data. A library is ammunition, not evidence — every idea here still faces the kill lines before it enters the ledger.</p>
</main>
</body>
</html>"""
    (ROOT / "docs/resources.html").write_text(page)
    print("docs/resources.html:", len(page), "bytes")


if __name__ == "__main__":
    main()
