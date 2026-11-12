"""PDF research-article ingestion: the alternative knowledge-input path.

KNOWLEDGE*.md and *.html uploads are the existing knowledge inputs;
this module adds PDFs. Drop research papers into the repo root or
an `articles/` directory and each nightly pass extracts their text
(pypdf), stores a per-article full-text digest under
paper/research/articles/, and registers them in
paper/research/articles.json for the Salient knowledge section.

This is research INFRASTRUCTURE (like fetch_data.py), not the
sandboxed strategy core: it never touches trading logic, parameters
or order state. It only reads documents the user committed and
writes research artifacts.

Usage (nightly):
    python3 pdf_ingest.py --repo-root .. \
        --research-dir ../paper/research
"""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DIGEST_CHARS = 2400


def _clean(text: str) -> str:
    """Collapse PDF extraction artifacts: repeated whitespace, lone
    form feeds, and hyphenated line breaks."""
    text = text.replace("\x0c", "\n")
    text = re.sub(r"-\n(?=[a-z])", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def ingest_pdf(path: Path) -> dict:
    """Extract one PDF: per-page text, cleaned, with a digest and
    honest stats. Never raises on extraction: a corrupt PDF becomes
    a status row, not a failed nightly run."""
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages):
        try:
            pages.append(_clean(page.extract_text() or ""))
        except Exception as exc:  # extraction is best-effort per page
            pages.append(f"[page {i + 1} extraction failed: {exc}]")
    full = "\n\n".join(f"--- page {i + 1} ---\n{p}"
                       for i, p in enumerate(pages) if p)
    chars = sum(len(p) for p in pages)
    return {
        "file": path.name,
        "pages": len(pages),
        "chars": chars,
        "status": "OK" if chars > 0 else "EMPTY",
        "digest": _clean(full)[:DIGEST_CHARS],
        "full_text": full,
    }


def scan_pdfs(repo_root: Path) -> list:
    """Find committed PDFs: the repo root and an articles/ folder.
    Sorted for deterministic runs."""
    roots = [repo_root, repo_root / "articles"]
    seen = {}
    for root in roots:
        if not root.exists():
            continue
        for f in sorted(root.glob("*.pdf")):
            if f.is_file():
                seen[f.name] = f
    return [seen[k] for k in sorted(seen)]


def run_ingest(repo_root: Path, research_dir: Path) -> dict:
    """Ingest every committed PDF into research artifacts. The
    registry is rebuilt fresh each run (PDFs are inputs, not
    append-only history)."""
    pdfs = scan_pdfs(repo_root)
    out_dir = research_dir / "articles"
    out_dir.mkdir(parents=True, exist_ok=True)
    registry = []
    for f in pdfs:
        try:
            rec = ingest_pdf(f)
        except Exception as exc:
            rec = {"file": f.name, "pages": 0, "chars": 0,
                   "status": f"FAILED: {exc}", "digest": "",
                   "full_text": ""}
        slug = re.sub(r"[^a-z0-9]+", "-",
                      f.stem.lower()).strip("-") or "article"
        (out_dir / f"{slug}.md").write_text(
            f"# {f.name}\n\n{rec['full_text']}\n")
        registry.append({
            "file": rec["file"],
            "pages": rec["pages"],
            "chars": rec["chars"],
            "status": rec["status"],
            "digest": rec["digest"],
            "ingested_utc": datetime.now(timezone.utc).isoformat(
                timespec="seconds"),
        })
        print(f"ingested {f.name} -> {out_dir / (slug + '.md')} "
              f"({rec['pages']} pages, {rec['chars']} chars)")
    research_dir.mkdir(parents=True, exist_ok=True)
    (research_dir / "articles.json").write_text(
        json.dumps(registry, indent=2))
    print(f"article registry -> "
          f"{research_dir / 'articles.json'} ({len(registry)} articles)")
    return {"status": "OK", "articles": registry}


def main() -> None:
    ap = argparse.ArgumentParser(
        description="PDF research-article ingestion")
    ap.add_argument("--repo-root", type=Path, default=Path(".."))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    try:
        run_ingest(args.repo_root, args.research_dir)
    except ImportError:
        print("pypdf not installed - PDF ingestion skipped "
              "(research infra only, nothing failed)")


if __name__ == "__main__":
    main()
