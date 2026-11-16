#!/usr/bin/env python3
"""Library acquisition: download legally available open-access papers.

Legal routes only:
  1. arXiv (papers with a known arXiv id, or found via the arXiv API
     by title search).
  2. Unpaywall (papers with a DOI: returns OA locations when the
     publisher version or an accepted manuscript is legally
     open-access). Requires an email address for the API.
  3. OpenAlex (open metadata catalogue; by DOI and by title search,
     returns best_oa_location.pdf_url when a legal OA copy exists).

Semantic Scholar was tried and removed: its fuzzy title match
returned a wrong paper (034), so the route is not used.

No paywall circumvention, no scraping of publisher sites, no shared
credentials. Papers with no legal OA route are reported as
"paywalled" and their summaries are synthesized from internal
knowledge instead (labelled as such in docs/library/summaries/).

Usage:
    export UNPAYWALL_EMAIL="you@example.com"
    python3 src/library_acquire.py [--catalog docs/articles_catalogue_data.txt]

Outputs:
    docs/library/pdfs/<id>_<slug>.pdf     downloaded OA PDFs
    docs/library/text/<id>_<slug>.txt     extracted plain text (pypdf)
    docs/library/acquisition_log.json      per-paper status
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "vp-mr-strategy-library/1.0"

ARXIV_KNOWN = {
    "018": "1011.6402",   # Cont-Kukanov-Stoikov, Price Impact of Order Book Events
    "011": "1803.00567",  # Peyre & Cuturi, Computational Optimal Transport (tutorial basis)
    "019": "1904.03429",  # Peyre & Cuturi, User's Guide to Optimal Transport
    "038": "1502.03562",  # Bailey et al., The Backtest Overfitting Problem
    "044": "1701.07875",  # Arjovsky et al., Wasserstein GAN
    "065": "1608.00060",  # Chernozhukov et al., Double/Debiased ML
    "068": "0706.1062",   # Clauset, Shalizi & Newman, Power-Law Distributions
}

ARXIV_QUERY = "http://export.arxiv.org/api/query?search_type=all&query={q}&max_results=5"
PDF_DIR = Path("docs/library/pdfs")
TEXT_DIR = Path("docs/library/text")
LOG_PATH = Path("docs/library/acquisition_log.json")


def slugify(text):
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    return text[:60].lower()


def http_get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "vp-mr-strategy-library/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_catalog(path):
    """Yield (paper_id, title, authors, year, venue, doi, arxiv_hint)."""
    entries = []
    for line in Path(path).read_text().splitlines():
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 7:
            continue
        pid = parts[0].split()[0]
        title_auth = parts[2]
        m = re.match(r"(.+?)\s*\((\d{4})\)", title_auth)
        title, year = (m.group(1), m.group(2)) if m else (title_auth, "")
        doi = parts[5] if len(parts) > 5 else ""
        if doi and not re.match(r"^10\.\d{4,9}/", doi):
            doi = ""
        entries.append({"id": pid, "title": title, "year": year,
                        "venue": parts[4], "doi": doi, "raw": line})
    return entries


def _json_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def openalex_oa(doi=None, title=None):
    """Legal OA PDF URL via OpenAlex, by DOI or title search."""
    try:
        if doi:
            w = _json_get("https://api.openalex.org/works/doi:" + doi)
        else:
            data = _json_get("https://api.openalex.org/works?search="
                             + urllib.parse.quote(title) + "&per-page=1")
            results = data.get("results") or []
            if not results:
                return None
            w = results[0]
        if not w.get("open_access", {}).get("is_oa"):
            return None
        loc = w.get("best_oa_location") or {}
        return loc.get("pdf_url") or loc.get("landing_page_url")
    except Exception:
        return None


def unpaywall_best_oa(doi, email):
    if not doi or not email:
        return None
    url = f"https://api.unpaywall.org/v2/{doi}?email={urllib.parse.quote(email)}"
    try:
        data = json.loads(http_get(url))
    except Exception:
        return None
    loc = data.get("best_oa_location") or {}
    pdf_url = loc.get("url_for_pdf") or loc.get("url")
    return {"pdf": pdf_url, "license": loc.get("license"),
            "is_oa": data.get("is_oa")}


def arxiv_find(title):
    q = urllib.parse.quote(f'ti:"{title}"')
    try:
        xml = http_get(ARXIV_QUERY.format(q=q)).decode("utf-8", "replace")
    except Exception:
        return None
    m = re.search(r"<id>http://arxiv.org/abs/([0-9.]+)</id>", xml)
    return m.group(1) if m else None


def arxiv_pdf_url(arxiv_id):
    return f"https://arxiv.org/pdf/{arxiv_id}"


def extract_text(pdf_bytes, out_path):
    try:
        from pypdf import PdfReader
    except ImportError:
        out_path.write_text("[pypdf not installed; PDF saved but text not extracted]\n")
        return False
    import io
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = [p.extract_text() or "" for p in reader.pages]
    out_path.write_text("\n\n".join(f"=== page {i+1} ===\n{t}"
                                   for i, t in enumerate(pages)))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", default="docs/articles_catalogue_data.txt")
    ap.add_argument("--email", default=None)
    args = ap.parse_args()
    email = args.email or ""
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    TEXT_DIR.mkdir(parents=True, exist_ok=True)

    log = {}
    for entry in parse_catalog(args.catalog):
        pid, title = entry["id"], entry["title"]
        status = "paywalled"
        source = None
        pdf_url = None

        if pid in ARXIV_KNOWN:
            pdf_url, source, status = arxiv_pdf_url(ARXIV_KNOWN[pid]), f"arXiv:{ARXIV_KNOWN[pid]}", "oa"
        else:
            oa = unpaywall_best_oa(entry["doi"], email)
            if oa and oa.get("pdf"):
                pdf_url, source, status = oa["pdf"], f"Unpaywall ({oa['license']})", "oa"
            else:
                arx = arxiv_find(title)
                if arx:
                    pdf_url, source, status = arxiv_pdf_url(arx), f"arXiv:{arx}", "oa"
                else:
                    oalex = openalex_oa(doi=entry["doi"], title=title)
                    if oalex and (oalex.lower().endswith(".pdf") or "/pdf" in oalex.lower()):
                        pdf_url, source, status = oalex, "OpenAlex", "oa"

        if pdf_url:
            slug = f"{pid}_{slugify(title)}"
            try:
                data = http_get(pdf_url)
                (PDF_DIR / f"{slug}.pdf").write_bytes(data)
                extracted = extract_text(data, TEXT_DIR / f"{slug}.txt")
                status = "downloaded" + ("" if extracted else " (text extraction pending pypdf)")
                print(f"[{pid}] {status}: {source} -> {slug}.pdf")
            except Exception as e:
                status = f"oa-found-download-failed ({e})"
                print(f"[{pid}] {status}", file=sys.stderr)
        else:
            print(f"[{pid}] {status}: no legal OA route; summary will be synthesized")
        log[pid] = {"title": title, "doi": entry["doi"], "venue": entry["venue"],
                    "status": status, "source": source}

    LOG_PATH.write_text(json.dumps(log, indent=2))
    n = sum(1 for v in log.values() if v["status"].startswith(("downloaded", "oa")))
    print(f"\nAcquired {n}/{len(log)} papers. Log: {LOG_PATH}")


if __name__ == "__main__":
    main()
