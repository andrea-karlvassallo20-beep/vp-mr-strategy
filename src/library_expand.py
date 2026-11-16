#!/usr/bin/env python3
"""Expand the library: find ~100 MORE legally open-access papers.

Searches OpenAlex (open metadata, OA-filtered) and the arXiv API
across the project's topic families, dedupes against the existing
68-paper catalogue and against each other, and downloads only
legally open-access PDFs (publisher OA copies or arXiv preprints).
No paywall circumvention: entries without a legal PDF are skipped.

Outputs:
    docs/library/pdfs/<slug>.pdf          downloaded OA PDFs
    docs/library/text/<slug>.txt          extracted text (pypdf)
    docs/library/expanded_index.json      metadata for every acquired paper
    docs/library/expanded_index.md        human-readable index
"""

import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "vp-mr-strategy-library/1.0"
PDF_DIR = Path("data/library_pdfs")  # git-ignored (weight policy); texts are versioned
LEGACY_PDF_DIR = Path("docs/library/pdfs")  # already-tracked first 186
TEXT_DIR = Path("docs/library/text")
INDEX_JSON = Path("docs/library/expanded_index.json")
INDEX_MD = Path("docs/library/expanded_index.md")
import sys
TARGET = int(sys.argv[sys.argv.index("--target") + 1]) if "--target" in sys.argv else 200
MAX_PDF_BYTES = 20 * 1024 * 1024

QUERIES = [
    ("microstructure", "limit order book price impact microstructure"),
    ("microstructure", "order flow imbalance mid-price prediction"),
    ("microstructure", "queueing limit order book dynamics"),
    ("microstructure", "market maker liquidity provision adverse selection"),
    ("hawkes", "Hawkes process self-exciting financial markets"),
    ("microstructure", "branching ratio endogeneity price jumps trades"),
    ("orderflow", "trade sign autocorrelation order flow persistence"),
    ("orderflow", "VPIN volume synchronized probability informed trading"),
    ("orderflow", "flow toxicity liquidity crashes"),
    ("impact", "square root law market impact execution"),
    ("impact", "optimal execution limit order book Almgren"),
    ("impact", "Kyle lambda insider trading equilibrium"),
    ("backtesting", "backtest overfitting deflated Sharpe ratio"),
    ("backtesting", "purged cross-validation financial machine learning"),
    ("backtesting", "data snooping trading rules evaluation"),
    ("regimes", "Markov switching regime financial returns"),
    ("regimes", "regime switching volatility forecasting"),
    ("changepoint", "change point detection financial time series"),
    ("changepoint", "Wasserstein distance distribution shift detection"),
    ("mlfinance", "deep learning limit order books"),
    ("mlfinance", "machine learning asset pricing cross section"),
    ("mlfinance", "double debiased machine learning treatment effect"),
    ("volatility", "realized volatility high frequency intraday"),
    ("volatility", "rough volatility Hawkes"),
    ("crypto", "cryptocurrency order book microstructure bitcoin"),
    ("crypto", "bitcoin high frequency trading liquidity"),
    ("info", "flash crash liquidity withdrawal"),
    ("info", "Amihud illiquidity asset pricing"),
    ("volatility", "rough volatility model high frequency"),
    ("volatility", "GARCH forecasting cryptocurrency"),
    ("mlfinance", "multiple testing false discovery financial economics"),
    ("mlfinance", "causal inference finance machine learning"),
    ("changepoint", "optimal transport time series comparison"),
    ("microstructure", "deep learning limit order book prediction DeepLOB"),
    ("impact", "meta-order execution hidden impact"),
    ("regimes", "hidden Markov model financial time series"),
    ("marketmaking", "Avellaneda Stoikov market making"),
    ("marketmaking", "market maker inventory risk dealer"),
    ("perps", "perpetual futures funding rate"),
    ("perps", "cryptocurrency basis futures arbitrage"),
    ("defi", "automated market maker decentralized exchange"),
    ("defi", "DeFi liquidity protocol"),
    ("hft", "realized kernels high frequency price noise"),
    ("hft", "synchronization error asynchronous trading Epps"),
    ("pointproc", "autoregressive conditional duration trade arrivals"),
    ("pointproc", "point process financial intraday seasonality"),
    ("network", "financial networks systemic risk"),
    ("network", "lead-lag cross-correlation stock returns"),
    ("text", "text mining news stock returns"),
    ("rl", "reinforcement learning trading market making"),
    ("mlfinance", "transformer attention time series forecasting"),
    ("mlfinance", "generative adversarial network financial time series"),
    ("crypto", "stablecoin design dynamics"),
    ("crypto", "extreme events cryptocurrency jumps"),
    ("info", "price discovery information content trades Hasbrouck"),
    ("info", "informed trading adverse selection spread"),
]

ARXIV_QUERIES = [
    ("arxiv-micro", "cat:q-fin.TR AND abs:order book"),
    ("arxiv-hawkes", "cat:q-fin* AND abs:Hawkes"),
    ("arxiv-impact", "cat:q-fin.TR AND abs:market impact"),
    ("arxiv-ml", "cat:q-fin* AND abs:machine learning"),
    ("arxiv-crypto", "cat:q-fin.TR AND abs:cryptocurrency"),
    ("arxiv-vol", "cat:q-fin.ST AND abs:volatility"),
    ("arxiv-ot", "cat:q-fin* AND abs:optimal transport"),
    ("arxiv-book", "cat:q-fin.TR AND abs:limit order book"),
    ("arxiv-bt", "cat:q-fin.CP AND abs:backtest"),
    ("arxiv-vpin", "cat:q-fin.TR AND abs:order imbalance"),
    ("arxiv-micro2", "cat:q-fin.TR AND abs:microstructure"),
    ("arxiv-hawkes2", "cat:q-fin.ST AND abs:self-exciting"),
    ("arxiv-cp", "cat:q-fin.ST AND abs:regime change"),
    ("arxiv-noise", "cat:q-fin.ST AND abs:microstructure noise"),
    ("arxiv-mm", "cat:q-fin.MF AND abs:Hawkes"),
    ("arxiv-jump", "cat:q-fin.MF AND abs:self-exciting jumps"),
    ("arxiv-manip", "cat:q-fin.TR AND abs:manipulation"),
    ("arxiv-spoof", "cat:q-fin.TR AND abs:spoofing"),
    ("arxiv-exec", "cat:q-fin.TR AND abs:execution"),
    ("arxiv-opt", "cat:q-fin.PR AND abs:order flow"),
    ("arxiv-pm", "cat:q-fin.PM AND abs:momentum"),
    ("arxiv-risk", "cat:q-fin.RM AND abs:extreme"),
    ("arxiv-net", "cat:q-fin.GN AND abs:lead-lag"),
    ("arxiv-lob2", "cat:q-fin.TR AND abs:order book AND abs:prediction"),
    ("arxiv-imb", "cat:q-fin.TR AND abs:imbalance"),
    ("arxiv-liq", "cat:q-fin.TR AND abs:liquidity"),
    ("arxiv-crash", "cat:q-fin.ST AND abs:crash"),
    ("arxiv-vol2", "cat:q-fin.ST AND abs:realized variance"),
    ("arxiv-crypto2", "cat:q-fin.TR AND abs:bitcoin"),
    ("arxiv-stable", "cat:q-fin.TR AND abs:stablecoin"),
    ("arxiv-defi", "cat:q-fin.TR AND abs:DeFi"),
    ("arxiv-hawkes3", "cat:q-fin.ST AND abs:branching"),
    ("arxiv-impact2", "cat:q-fin.TR AND abs:transient impact"),
    ("arxiv-mm2", "cat:q-fin.TR AND abs:market making"),
    ("arxiv-tick", "cat:q-fin.TR AND abs:tick size"),
    ("arxiv-pred", "cat:q-fin.CP AND abs:prediction market"),
    ("arxiv-ml2", "cat:q-fin.CP AND abs:deep learning AND abs:returns"),
]


def http_get(url, timeout=90):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def json_get(url):
    return json.loads(http_get(url))


def slugify(text, paper_id):
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").lower()[:50]
    return f"x{paper_id}_{text}"


def off_topic(title):
    t = title.lower()
    return (("transport" in t and "cost overrun" in t)
            or "income volatility" in t
            or "transport infrastructure" in t)


def clean_title(t):
    return re.sub(r"\s+", " ", (t or "")).strip()


def norm_title(t):
    return re.sub(r"[^a-z0-9]", "", clean_title(t).lower())


def openalex_search(query, limit=8):
    url = ("https://api.openalex.org/works?search=" + urllib.parse.quote(query)
           + f"&per-page={limit}&filter=open_access.is_oa:true"
           + "&select=id,doi,title,publication_year,authorships,cited_by_count,"
             "primary_location,best_oa_location,type")
    try:
        data = json_get(url)
    except Exception:
        return []
    out = []
    for w in data.get("results", []):
        title = clean_title(w.get("title"))
        if not title or off_topic(title) or w.get("type") not in ("article", "preprint", "review-article"):
            continue
        oa = w.get("best_oa_location") or {}
        pdf = oa.get("pdf_url")
        if not pdf:
            continue
        authors = [a.get("author", {}).get("display_name") or ""
                   for a in (w.get("authorships") or [])[:4]]
        venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
        out.append({"title": title, "year": w.get("publication_year"),
                    "authors": ", ".join([a for a in authors if a]),
                    "venue": venue, "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                    "pdf": pdf, "cited": w.get("cited_by_count") or 0})
    return out


def arxiv_search(query, limit=25):
    url = ("http://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(query)
           + f"&max_results={limit}&sortBy=relevance")
    try:
        xml = http_get(url).decode("utf-8", "replace")
    except Exception:
        return []
    out = []
    for m in re.finditer(r"<entry>(.*?)</entry>", xml, re.S):
        e = m.group(1)
        t = clean_title(re.search(r"<title>(.*?)</title>", e, re.S).group(1))
        if off_topic(t):
            continue
        arxiv_id = re.search(r"<id>http://arxiv.org/abs/([^<]+)</id>", e).group(1)
        authors = re.findall(r"<name>([^<]+)</name>", e)[:4]
        year = re.search(r"<published>(\d{4})", e).group(1)
        out.append({"title": t, "year": int(year), "authors": ", ".join(authors),
                    "venue": "arXiv:" + arxiv_id, "doi": "",
                    "pdf": f"https://arxiv.org/pdf/{arxiv_id}", "cited": 0})
    return out


def extract_text(pdf_bytes, out_path):
    try:
        from pypdf import PdfReader
    except ImportError:
        out_path.write_text("[pypdf not installed; PDF saved but text not extracted]\n")
        return False
    import io
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        pages = [p.extract_text() or "" for p in reader.pages]
    except Exception:
        out_path.write_text("[text extraction failed; PDF saved]\n")
        return False
    out_path.write_text("\n\n".join(f"=== page {i+1} ===\n{t}"
                                   for i, t in enumerate(pages)))
    return True


def main():
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    TEXT_DIR.mkdir(parents=True, exist_ok=True)

    # existing catalogue + already-acquired papers: skip duplicates
    seen = set()
    for line in Path("docs/articles_catalogue_data.txt").read_text().splitlines():
        m = re.match(r"\d+ \w+ \| (.*?) \|", line)
        if m:
            seen.add(norm_title(m.group(1)))
    for p in (list(PDF_DIR.glob("*.pdf")) + list(PDF_DIR.glob("*.txt"))
              + list(LEGACY_PDF_DIR.glob("*.pdf")) + list(LEGACY_PDF_DIR.glob("*.txt"))):
        seen.add(p.stem)

    # carry over previously acquired expanded-library papers
    acquired = []
    if INDEX_JSON.exists():
        try:
            acquired = json.loads(INDEX_JSON.read_text())
        except Exception:
            acquired = []
        for c in acquired:
            seen.add(c.get("slug") or "")
            seen.add(norm_title(c.get("title", "")))

    candidates, seen_titles = [], set()
    for tag, q in QUERIES:
        for c in openalex_search(q):
            k = norm_title(c["title"])
            if k and k not in seen_titles and k not in seen:
                seen_titles.add(k)
                c["topic"] = tag
                candidates.append(c)
        time.sleep(0.3)
    for tag, q in ARXIV_QUERIES:
        for c in arxiv_search(q):
            k = norm_title(c["title"])
            if k and k not in seen_titles and k not in seen:
                seen_titles.add(k)
                c["topic"] = tag
                candidates.append(c)
        time.sleep(3.1)

    # prioritize by citations within each topic family
    candidates.sort(key=lambda c: -c["cited"])
    print(f"{len(candidates)} unique legal-OA candidates found")

    for c in candidates:
        if len(acquired) >= TARGET:
            break
        pid = hashlib.sha1(c["title"].encode()).hexdigest()[:6]
        slug = slugify(c["title"], pid)
        if slug in seen:
            continue
        try:
            data = http_get(c["pdf"])
        except Exception as e:
            print(f"  skip (download failed {str(e)[:50]}): {c['title'][:60]}")
            continue
        if not data[:5].startswith(b"%PDF"):
            continue
        if len(data) > MAX_PDF_BYTES:
            continue
        (PDF_DIR / f"{slug}.pdf").write_bytes(data)
        extracted = extract_text(data, TEXT_DIR / f"{slug}.txt")
        c.update({"slug": slug, "text_extracted": extracted,
                  "bytes": len(data), "source_pdf": c["pdf"]})
        acquired.append(c)
        print(f"  [{len(acquired):3d}] {c['topic']}: {c['title'][:70]}")

    INDEX_JSON.write_text(json.dumps(acquired, indent=2))
    lines = ["# Expanded library index — additional legally acquired OA papers",
             "",
             f"{len(acquired)} papers beyond the 68-paper core catalogue,",
             "acquired via OpenAlex / arXiv (legal open-access only).",
             "PDFs in `docs/library/pdfs/`, extracted text in `docs/library/text/`.",
             "",
             "| # | Topic | Title | Authors | Year | Venue | File |",
             "|---|---|---|---|---|---|---|"]
    for i, c in enumerate(acquired, 1):
        t = c["title"].replace("|", "/")
        a = (c["authors"] or "").replace("|", "/")
        v = (c["venue"] or "").replace("|", "/")
        lines.append(f"| {i} | {c['topic']} | {t} | {a} | {c['year']} | {v} | `{c['slug']}` |")
    INDEX_MD.write_text("\n".join(lines) + "\n")
    print(f"\nAcquired {len(acquired)} additional papers. Index: {INDEX_MD}")


if __name__ == "__main__":
    main()
