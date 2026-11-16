"""Tests for the repo integrity guard (src/integrity_guard.py).

The 2026-11-16 incident: unresolved conflict markers reached main and
survived several merges. These tests make that class of corruption a
red build, not a discovery.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import integrity_guard  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_repo_has_no_conflict_markers():
    offenders = integrity_guard.sweep_markers(REPO_ROOT)
    assert offenders == [], (
        "Conflict markers found in tracked files (a broken merge was "
        f"committed): {offenders}"
    )


def test_library_summaries_provenance_honest():
    problems = integrity_guard.audit_library(REPO_ROOT)
    assert problems == [], f"Library provenance violations: {problems}"


def test_sweep_detects_a_planted_marker(tmp_path):
    (tmp_path / "bad.md").write_text("fine line\n<<<<<<< HEAD\nbad\n")
    offenders = integrity_guard.sweep_markers(tmp_path)
    assert offenders == ["bad.md:2: <<<<<<< HEAD"]


def test_sweep_detects_closing_marker_and_separator(tmp_path):
    (tmp_path / "a.py").write_text("x = 1\n=======\n>>>>>>> abc\n")
    offenders = integrity_guard.sweep_markers(tmp_path)
    assert len(offenders) == 1 and offenders[0].startswith("a.py:2")


def test_sweep_ignores_setext_and_normal_lines(tmp_path):
    (tmp_path / "ok.md").write_text(
        "Title\n======\nnot markers: a >>>>>>> b, <<<<<<< c\n"
    )
    assert integrity_guard.sweep_markers(tmp_path) == []


def test_sweep_ignores_binary_and_untracked_suffixes(tmp_path):
    (tmp_path / "img.png").write_bytes(b"<<<<<<< HEAD\n")
    assert integrity_guard.sweep_markers(tmp_path) == []


def test_audit_flags_missing_full_text(tmp_path):
    s = tmp_path / "docs" / "library" / "summaries"
    s.mkdir(parents=True)
    (s / "001.md").write_text(
        "**Status:** Downloaded; full text: `docs/library/text/001.txt`\n"
    )
    problems = integrity_guard.audit_library(tmp_path)
    assert problems == [
        "docs/library/summaries/001.md: cites full text "
        "`docs/library/text/001.txt` which does not exist"
    ]


def test_audit_flags_unlabeled_summary(tmp_path):
    s = tmp_path / "docs" / "library" / "summaries"
    s.mkdir(parents=True)
    (s / "002.md").write_text("# 002 — Some paper\n\nGreat paper.\n")
    problems = integrity_guard.audit_library(tmp_path)
    assert problems and "no Status line" in problems[0]


def test_audit_accepts_honest_synthesized_label(tmp_path):
    s = tmp_path / "docs" / "library" / "summaries"
    s.mkdir(parents=True)
    (s / "003.md").write_text(
        "**Status:** Synthesized from LLM internal knowledge (Paywalled "
        "paper). Verify against library source before production.\n"
    )
    assert integrity_guard.audit_library(tmp_path) == []
