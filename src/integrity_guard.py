"""Repo integrity guard — born from the 2026-11-16 incident.

That day, `docs/c8_synthesis_spec.md` reached `main` containing a literal
unresolved merge-conflict block (`<<<<<<< HEAD / ======= / >>>>>>>`), and
the corruption survived several merges before anyone noticed. A broken
merge resolution had been pushed. The check that would have caught it is
mechanical, so it belongs in the test suite, not in anyone's memory.

Two invariants, both enforced as raising asserts:

1. MARKER SWEEP — no tracked text file in the repo may contain git
   conflict markers at line start (`<<<<<<< `, `>>>>>>> `, or a bare
   `=======` line). Markdown setext headings use `===`/`---` underlines
   but never exactly seven `=` alone on a line; the sweep was verified
   against the whole tree before it was armed.

2. LIBRARY HONESTY AUDIT — every summary in `docs/library/summaries/`
   carries a Status line. A summary citing extracted text
   ("full text: `path`") must have that file on disk. A "Synthesized
   from LLM internal knowledge" summary must carry the verify-before-
   production caveat. A summary with neither label fails: unlabeled
   provenance is exactly the defect the epistemic contract forbids.

Usage:
    python3 src/integrity_guard.py            # run both checks, exit 1 on any failure
    python3 src/integrity_guard.py --sweep   # markers only
    python3 src/integrity_guard.py --library  # summaries only

The pytest suite runs both via tests/test_integrity_guard.py.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MARKER_RE = re.compile(r"^(<{7} |>{7} |={7}$)")
TEXT_SUFFIXES = {
    ".md", ".py", ".html", ".json", ".csv", ".txt", ".js", ".css",
    ".yml", ".yaml", ".toml", ".cfg", ".ini", ".jsonl", ".sh",
}

# Files that legitimately demonstrate conflict markers (e.g., this
# guard's own documentation) would be listed here. None at arming time.
MARKER_WHITELIST: frozenset[str] = frozenset()


def sweep_markers(root: Path) -> list[str]:
    """Return the list of tracked text files containing conflict markers."""
    offenders = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(root).as_posix()
        if rel in MARKER_WHITELIST or rel.startswith(".git/"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if MARKER_RE.match(line):
                offenders.append(f"{rel}:{lineno}: {line.strip()[:60]}")
                break  # one report per file is enough
    return offenders


def audit_library(root: Path) -> list[str]:
    """Return the list of library-summary provenance violations."""
    problems = []
    summaries = sorted((root / "docs" / "library" / "summaries").glob("*.md"))
    if not summaries:
        return ["docs/library/summaries/ is empty or missing"]
    for path in summaries:
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not re.search(r"\*\*Status:\*\*", text):
            problems.append(f"{rel}: no Status line (unlabeled provenance)")
            continue
        m = re.search(r"full text: `([^`]+)`", text)
        if m:
            cited = root / m.group(1)
            if not cited.exists():
                problems.append(f"{rel}: cites full text `{m.group(1)}` which does not exist")
        elif "synthesized from llm internal knowledge" in text.lower():
            if "Verify against library source" not in text:
                problems.append(f"{rel}: synthesized without the verify-before-production caveat")
        else:
            problems.append(f"{rel}: Status line carries neither a full-text cite nor the synthesized label")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sweep", action="store_true", help="marker sweep only")
    ap.add_argument("--library", action="store_true", help="library audit only")
    args = ap.parse_args(argv)
    root = Path(__file__).resolve().parents[1]

    failures: list[str] = []
    if not args.library:
        failures += [f"CONFLICT MARKER: {o}" for o in sweep_markers(root)]
    if not args.sweep:
        failures += [f"LIBRARY PROVENANCE: {o}" for o in audit_library(root)]

    if failures:
        print("INTEGRITY GUARD FAILED — the repo is not clean:")
        for f in failures:
            print(f"  {f}")
        return 1
    print("Integrity guard: clean — no conflict markers, all library provenance labels honest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
