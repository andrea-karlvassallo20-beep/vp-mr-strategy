"""PDF ingestion suite: extraction, cleaning, registry, and
empty-state grace. Harness file."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    import pypdf
    HAVE_PYPDF = True
except ImportError:
    HAVE_PYPDF = False

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def make_pdf(path: Path, text: str) -> None:
    """Handcraft a minimal one-page PDF with a single text object -
    enough for pypdf's extractor, no external writer needed."""
    content = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET"
    objs = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        "/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        f"<< /Length {len(content)} >>\nstream\n{content}\nendstream",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = ["%PDF-1.4"]
    offsets = []
    for i, o in enumerate(objs, 1):
        offsets.append(sum(len(x) + 1 for x in out))
        out.append(f"{i} 0 obj\n{o}\nendobj")
    xref_pos = sum(len(x) + 1 for x in out)
    xref = f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n"
    for off in offsets:
        xref += f"{off:010d} 00000 n \n"
    xref += (f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\n"
             f"startxref\n{xref_pos}\n%%EOF")
    path.write_text("\n".join(out) + "\n" + xref)


from pdf_ingest import _clean, scan_pdfs, run_ingest

check("cleaner collapses whitespace and dehyphenates",
      _clean("volatil-\nity   spread\x0c\n\n\n\nz") ==
      "volatility spread\n\nz")

tmp = Path(tempfile.mkdtemp())
root = tmp / "repo"
root.mkdir()

check("scan finds no PDFs in an empty repo",
      scan_pdfs(root) == [])

if not HAVE_PYPDF:
    print("  NOTE pypdf not installed - core extraction checks skipped")
else:
    from pdf_ingest import ingest_pdf
    make_pdf(root / "mean-reversion-study.pdf",
             "MEAN REVERTS AT DEEP STRETCH")
    (root / "articles").mkdir()
    make_pdf(root / "articles" / "avfi-paper.pdf",
             "VOLUME FLOW SPREAD AXIS")
    bad = root / "articles" / "corrupt.pdf"
    bad.write_text("this is not a pdf at all")

    pdfs = scan_pdfs(root)
    check("scan finds root and articles PDFs, sorted",
          [p.name for p in pdfs] ==
          ["avfi-paper.pdf", "corrupt.pdf", "mean-reversion-study.pdf"])

    rec = ingest_pdf(root / "mean-reversion-study.pdf")
    check("extraction pulls the text object",
          "MEAN REVERTS" in rec["digest"] and rec["pages"] == 1
          and rec["chars"] > 0 and rec["status"] == "OK")

    r = run_ingest(root, tmp / "research")
    reg = json.loads((tmp / "research" / "articles.json")
                     .read_text())
    check("registry lists all three with honest statuses",
          len(reg) == 3
          and {a["status"].split(":")[0] for a in reg} ==
          {"OK", "FAILED"})
    ok = next(a for a in reg if a["file"] == "mean-reversion-study.pdf")
    check("registry carries pages, chars, digest, timestamp",
          ok["pages"] == 1 and ok["chars"] > 0 and ok["digest"]
          and "ingested_utc" in ok)
    md = (tmp / "research" / "articles" /
          "mean-reversion-study.md")
    check("full-text markdown written per article",
          md.exists() and "MEAN REVERTS" in md.read_text())
    check("corrupt PDF fails gracefully without killing the run",
          r["status"] == "OK"
          and any(a["file"] == "corrupt.pdf" and
                  a["status"].startswith("FAILED") for a in reg))

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
