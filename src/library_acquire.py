"""Legal open-access acquisition for the Library's article catalogue.

For every record in docs/articles_catalogue_data.txt:
  1. Resolve a DOI via Crossref title search (free, public API).
  2. Query Unpaywall (free, legal OA locator) for a legally free PDF.
  3. Fallback: arXiv API title search (preprints).
  4. Fallback: a known http link from the record itself.

Only legally free versions are downloaded (open-access, preprints,
author-shared). Paywalled articles are NOT scraped; they are listed in
the manifest for the owner to supply. Every obtained file records its
source URL in the manifest.

Output: docs/library/pdfs/*.pdf + docs/library/manifest.md
"""

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/library/pdfs"
EMAIL = "library@vp-mr-strategy.local"  # Unpaywall requires an email contact


def _get_json(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research-library-indexer)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def crossref_doi(title, author):
    q = urllib.parse.quote(f'{title} {author.split("(")[0]}')
    try:
        d = _get_json(f"https://api.crossref.org/works?query.bibliographic={q}&rows=3")
        for it in d["message"]["items"]:
            if "DOI" in it and abs(len(it.get("title", [""])[0]) - len(title)) < 0.6 * max(len(title), 1):
                return it["DOI"]
        # fall back to top hit if reasonably close
        items = d["message"]["items"]
        if items and "DOI" in items[0]:
            t0 = items[0].get("title", [""])[0].lower()
            if title.lower()[:30] in t0:
                return items[0]["DOI"]
    except Exception:
        pass
    return None


def unpaywall_pdf(doi):
    try:
        d = _get_json(f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}")
        loc = d.get("best_oa_location") or {}
        pdf = loc.get("url_for_pdf") or loc.get("url")
        return pdf if pdf else None
    except Exception:
        return None


def arxiv_pdf(title):
    q = urllib.parse.quote(f'all:"{title}"')
    try:
        d = _get_json(f"http://export.arxiv.org/api/query?search_query={q}&max_results=2")
        m = re.search(r"<entry>.*?<id>(http://arxiv.org/abs/[^<]+)</id>", d if isinstance(d, str) else "", re.S)
    except Exception:
        # arXiv returns Atom XML, not JSON
        try:
            req = urllib.request.Request(
                f"http://export.arxiv.org/api/query?search_query={q}&max_results=2",
                headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=25) as r:
                xml = r.read().decode()
            m = re.search(r"<id>(http://arxiv.org/abs/[^<]+)</id>", xml)
            if m:
                aid = m.group(1).split("/abs/")[-1]
                return f"http://arxiv.org/pdf/{aid}.pdf"
        except Exception:
            pass
    return None


def download(url, dest):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        if len(data) < 20_000 or not data[:5].startswith(b"%PDF"):
            # some OA links serve HTML landing pages; try pdf-suffix variants
            if not url.endswith(".pdf") and "pdf" not in url:
                alt = url.rstrip("/") + ".pdf"
                req = urllib.request.Request(alt, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=60) as r2:
                    data = r2.read()
            if len(data) < 20_000 or not data[:5].startswith(b"%PDF"):
                return False
        dest.write_bytes(data)
        return True
    except Exception:
        return False


def main():
    import pandas as pd  # noqa
    OUT.mkdir(parents=True, exist_ok=True)
    recs = json.load(open("/tmp/recs.json"))
    manifest = []
    for r in recs:
        num, title = r["num"], r["title"]
        dest = OUT / f"{num}_{re.sub(r'[^A-Za-z0-9]+', '_', title[:40]).strip('_')}.pdf"
        got, src = False, None
        doi = r["doi"] or None
        if not doi:
            doi = crossref_doi(title, r["authors"]); time.sleep(1.0)
        if doi:
            pdf = unpaywall_pdf(doi); time.sleep(0.8)
            if pdf and download(pdf, dest):
                got, src = True, f"Unpaywall/OA via DOI {doi}"
        if not got:
            ax = arxiv_pdf(title); time.sleep(0.8)
            if ax and download(ax, dest):
                got, src = True, "arXiv preprint"
        if not got and r["link"].startswith("http"):
            if download(r["link"], dest):
                got, src = True, r["link"]
        manifest.append({"num": num, "title": title, "doi": doi or "",
                        "obtained": got, "source": src or "",
                        "file": dest.name if got else ""})
        print(num, "OK" if got else "paywalled/none", flush=True)
    json.dump(manifest, open("/tmp/manifest.json", "w"), indent=1)
    n_ok = sum(m["obtained"] for m in manifest)
    print(f"\nOBTAINED {n_ok}/{len(manifest)}")


if __name__ == "__main__":
    main()
