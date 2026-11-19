#!/usr/bin/env python3
"""gen_thesis_pdf.py - deterministic stdlib-only PDF edition of the SMH thesis.

Reads docs/smh_thesis_v1.md and emits an uncompressed, ASCII-only PDF
(Helvetica / Helvetica-Bold / Helvetica-Oblique) so the file is byte-stable
and transmissible as plain text. No dependencies, no network, double-run
deterministic. Usage:

    python3 gen_thesis_pdf.py [input.md] [output.pdf]

Defaults: docs/smh_thesis_v1.md
       -> docs/The-Salient-Market-Hypothesis-thesis-v1.0.pdf
"""
import os
import sys
import unicodedata

PAGE_W, PAGE_H = 595.28, 841.89
MARG_L, MARG_R, MARG_T, MARG_B = 64.0, 64.0, 72.0, 64.0

F_BODY, F_BOLD, F_ITAL = "F1", "F2", "F3"
SZ_BODY = 9.5
LEAD = 13.2
FOOTER = "SMH thesis v1.0"


def sanitize(s: str) -> str:
    """Force pure ASCII (the PDF bytes must stay 7-bit-clean)."""
    repl = {"ő": "o", "Ő": "O", "—": "-", "–": "-", "’": "'", "‘": "'",
            "“": '"', "”": '"', "×": "x", "·": "."}
    out = []
    for ch in s:
        out.append(repl.get(ch, ch))
    s = unicodedata.normalize("NFKD", "".join(out))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "".join(c if 32 <= ord(c) < 127 or c == "\n" else ""
                   for c in s)


def esc(s: str) -> str:
    return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def strip_md(line: str) -> str:
    return line.replace("**", "").replace("`", "")


def wrap(text: str, width: int, cont_indent: int = 0) -> list:
    lines, cur = [], []
    for w in text.split():
        trial = " ".join(cur + [w])
        limit = width if not lines else width - cont_indent
        if cur and len(trial) > limit:
            lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))
    return lines


class Doc:
    def __init__(self):
        self.page_no = 0
        self.buf = []
        self.y = 0.0
        self.pages = []

    # -- internals --
    def _newpage(self):
        if self.buf:
            self.pages.append("\n".join(self.buf))
        self.buf = []
        self.y = PAGE_H - MARG_T
        self.page_no += 1

    def _room(self, need):
        if self.y - need < MARG_B:
            self._newpage()

    def _text(self, x, y, font, size, s):
        self.buf.append("BT /%s %.1f Tf %.2f %.2f Td (%s) Tj ET"
                        % (font, size, x, y, esc(s)))

    def _footer(self, content, n):
        label = "%s - page %d" % (FOOTER, n)
        width = len(label) * SZ_BODY * 0.50
        x = (PAGE_W - width) / 2.0
        return content + "\nBT /F1 8 Tf %.2f 40 Td (%s) Tj ET" % (
            x, esc(label))

    # -- public --
    def start(self):
        self._newpage()

    def line_at(self, x, dy, font, size, s, newpage_top=False):
        if newpage_top:
            self._newpage()
        self._text(x, self.y - size, font, size, s)
        self.y -= dy

    def para_lines(self, x, lines, font, size, dy):
        for ln in lines:
            self._room(dy + 2)
            self._text(x, self.y - size, font, size, ln)
            self.y -= dy

    def bullet(self, x, text):
        w = wrap(text, 84, 14)
        for k, ln in enumerate(w):
            self._room(LEAD + 2)
            if k == 0:
                self._text(x, self.y - SZ_BODY, F_BODY, SZ_BODY, "-")
            self._text(x + 14, self.y - SZ_BODY, F_BODY, SZ_BODY, ln)
            self.y -= LEAD

    def rule(self):
        self._room(14)
        self.buf.append("%.2f %.2f m %.2f %.2f l 0.5 w S"
                        % (MARG_L, self.y - 6, PAGE_W - MARG_R, self.y - 6))
        self.y -= 16

    def gap(self, pts):
        self.y -= pts

    def heading(self, text, level):
        if level == 0:  # part
            self._newpage()
            self.y = PAGE_H - MARG_T - 30
            self.line_at(MARG_L, 34, F_BOLD, 17, text)
        elif level == 1:  # chapter / major heading
            self._room(50)
            self.gap(8)
            for ln in wrap(text, 66):
                self._text(MARG_L, self.y - 12.5, F_BOLD, 12.5, ln)
                self.y -= 17
            self.y -= 6
        else:  # minor heading
            self._room(34)
            self.gap(3)
            for ln in wrap(text, 70):
                self._text(MARG_L, self.y - 11, F_BOLD, 11, ln)
                self.y -= 15
            self.y -= 4

    def finish(self):
        self.pages.append("\n".join(self.buf))
        self.buf = []
        return [self._footer(p, i + 1) for i, p in enumerate(self.pages)]


def build_pdf(page_contents) -> bytes:
    objects = {}
    objects[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
    resources = b"<< /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R >> >>"
    kids = []
    num = 6
    for pc in page_contents:
        payload = pc.encode("ascii")
        objects[num] = (b"<< /Length " + str(len(payload)).encode()
                        + b" >>\nstream\n" + payload + b"\nendstream")
        sid = num
        num += 1
        objects[num] = (b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 "
                        + ("%.2f %.2f" % (PAGE_W, PAGE_H)).encode()
                        + b"] /Resources " + resources + b" /Contents "
                        + str(sid).encode() + b" 0 R >>")
        kids.append(str(num) + " 0 R")
        num += 1
    objects[2] = (b"<< /Type /Pages /Kids [ " + " ".join(kids).encode()
                  + b" ] /Count " + str(len(page_contents)).encode() + b" >>")
    objects[3] = (b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
                  b"/Encoding /StandardEncoding >>")
    objects[4] = (b"<< /Type /Font /Subtype /Type1 /BaseFont "
                  b"/Helvetica-Bold /Encoding /StandardEncoding >>")
    objects[5] = (b"<< /Type /Font /Subtype /Type1 /BaseFont "
                  b"/Helvetica-Oblique /Encoding /StandardEncoding >>")

    out = bytearray(b"%PDF-1.4\n")
    offsets = {}
    for k in sorted(objects):
        offsets[k] = len(out)
        out += (str(k) + " 0 obj\n").encode() + objects[k] + b"\nendobj\n"
    xref_pos = len(out)
    maxnum = max(objects)
    out += b"xref\n0 " + str(maxnum + 1).encode() + b"\n"
    out += b"0000000000 65535 f \n"
    for k in range(1, maxnum + 1):
        out += ("%010d 00000 n \n" % offsets[k]).encode()
    out += (b"trailer\n<< /Size " + str(maxnum + 1).encode()
            + b" /Root 1 0 R >>\nstartxref\n" + str(xref_pos).encode()
            + b"\n%%EOF\n")
    assert all(b < 128 for b in out), "PDF is not ASCII-clean"
    return bytes(out)


COVER_STATUS = (
    "Status at freezing (19 November 2026, the Board's directive): every "
    "quantitative statement in this thesis is a frozen design figure "
    "produced on unsealed pre-2021 weekly NQ data; design statistics are "
    "bookkeeping, never proof. The proof object is the forward calibration "
    "record. The NQ weekly track is archived by the Board's directive with "
    "the forward log empty, so the hypothesis stands published, unfalsified, "
    "and unproved. The active research front is the L2 order-book track "
    "(C1-L2 -> C8 -> convexity sizing), testing the same hypothesis at book "
    "resolution. Kill criteria of every claim are stated with the claim.")


def cover(doc: Doc):
    doc.y = PAGE_H - 140
    doc.line_at(MARG_L, 36, F_BOLD, 26, "THE SALIENT MARKET HYPOTHESIS")
    doc.line_at(MARG_L, 32, F_BODY, 13,
                "A Falsifiable Theory of Liquidity and Time on the Weekly "
                "Chart")
    doc.line_at(MARG_L, 26, F_BOLD, 12, "Thesis, version 1.0")
    for s in ["Written 19 November 2026.",
              "Accepted and frozen by the Board's directive, 19 November 2026."]:
        doc.line_at(MARG_L, 15, F_BODY, 10, s)
    doc.gap(10)
    doc.rule()
    doc.para_lines(MARG_L, wrap("The two load-bearing sentences, absolute "
                                "and permanent:", 78), F_BOLD, 10, 14)
    doc.para_lines(MARG_L, wrap("The default assumption is NO EDGE. The "
                                "burden of proof is absolute.", 78),
                   F_ITAL, 10.5, 15)
    doc.gap(12)
    doc.rule()
    doc.gap(4)
    doc.para_lines(MARG_L, wrap(COVER_STATUS, 88), F_BODY, SZ_BODY, LEAD)


def body(md: str, doc: Doc):
    lines = [sanitize(strip_md(l.rstrip())) for l in md.split("\n")]
    start = next((i for i, l in enumerate(lines)
                  if l.startswith("## Abstract")), 0)
    i = start
    while i < len(lines):
        s = lines[i].strip()
        if s == "":
            i += 1
            continue
        if s.startswith("# "):
            doc.heading(s[2:].strip(), 0)
        elif s.startswith("## "):
            t = s[3:].strip()
            is_part = t.startswith("PART ") or t.startswith("APPENDIX") \
                or t == "Abstract"
            doc.heading(t, 0 if is_part else 1)
        elif s.startswith("### "):
            doc.heading(s[4:].strip(), 2)
        elif s == "---":
            doc.gap(8)
            doc.rule()
        elif s.startswith("- "):
            doc.bullet(MARG_L, s[2:])
            doc.gap(2)
        else:
            para = [s]
            j = i + 1
            while j < len(lines):
                nxt = lines[j].strip()
                if nxt == "" or nxt.startswith(("## ", "### ", "# ", "- ",
                                                "---")):
                    break
                para.append(nxt)
                j += 1
            doc.para_lines(MARG_L, wrap(" ".join(para), 88),
                           F_BODY, SZ_BODY, LEAD)
            doc.gap(6)
            i = j
            continue
        i += 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    inp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        here, "..", "docs", "smh_thesis_v1.md")
    outp = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        here, "..", "docs", "The-Salient-Market-Hypothesis-thesis-v1.0.pdf")
    with open(inp, "r", encoding="utf-8") as f:
        md = f.read()
    doc = Doc()
    doc.start()
    cover(doc)
    body(md, doc)
    pages = doc.finish()
    pdf = build_pdf(pages)
    with open(outp, "wb") as f:
        f.write(pdf)
    print("pages=%d bytes=%d file=%s" % (len(pages), len(pdf), outp))


if __name__ == "__main__":
    main()
