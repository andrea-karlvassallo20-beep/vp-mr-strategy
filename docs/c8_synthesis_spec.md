# C8 synthesis spec — SUPERSEDED

**This document is superseded by
`paper/research/c8_macro_l2_synthesis_spec.md`** — the authoritative
C8 pre-registration (eleven armed kill lines, hazard-model
estimand, math verified against the arXiv source and the `tick`
library on 2026-11-16:
`paper/research/math_verification_2026-11-16.md`). The claims ledger
(`docs/ledger.html`) points there. Two live pre-registrations for
one test would be an ambiguity defect, so this one stands down.

Kept for the record, not for governance. What this draft
contributed to the final spec, and where it differed:

- The hypothesis shape (C7-Primed macro state x L2 micro state:
  Hawkes branching ratio or extreme OFI or VPIN) and the
  macro-state costume check survived into the authoritative spec's
  kill lines (its L2 vol-tautology line, asked first).
- The estimand here was a DML-orthogonalized interaction uplift
  (`src/dml_orthogonalizer.py`); the authoritative spec uses a
  Cox-hazard interaction term with day-block bootstrap — the
  hazard form is the better instrument for a 4h/24h breakout
  question and is what governs.
- VPIN as a third trigger candidate did NOT survive into the
  authoritative spec's frozen trigger set (Hawkes branching ratio
  and OFI absorption only). VPIN remains documented as a future
  extension in `docs/library/summaries/046` and the cheatsheet
  (Section 5), not as a pre-registered C8 trigger.
- The "micro-state validity" gate (Hawkes fit convergence on >=95%
  of bars, exchange-provided trade side) is folded into the
  authoritative spec's boundary-constraint and proxy-refusal kill
  lines.

Amendments to the governing spec are appended there, dated and
marked — the 0.8 threshold's source-grounding (Filimonov-Sornette,
"Quantifying the Reflexivity of Financial Markets", extracted text
in `docs/library/text/`) is Amendment 1 of that document.
