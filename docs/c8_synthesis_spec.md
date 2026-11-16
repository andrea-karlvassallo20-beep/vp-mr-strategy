# C8 synthesis spec — SUPERSEDED

<<<<<<< HEAD
Status: DRAFT for owner review. Nothing in this document has been
computed on data; no model has been trained; the TEST eras are
untouched. Kill lines below are armed BEFORE any C8 measurement,
following the C7 pre-registration discipline
(`paper/research/phase1_daily/c7_30m_preregistration.md`).
=======
**This document is superseded by
`paper/research/c8_macro_l2_synthesis_spec.md`** — the authoritative
C8 pre-registration (eleven armed kill lines, hazard-model
estimand, math verified against the arXiv source and the `tick`
library on 2026-11-16:
`paper/research/math_verification_2026-11-16.md`). The claims ledger
(`docs/ledger.html`) points there. Two live pre-registrations for
one test would be an ambiguity defect, so this one stands down.
>>>>>>> cf3d47b (Null-time block: methodology hardening, C8 threshold source-grounded, devcontainer, website library page. (1) Duplicate pre-registration fixed: docs/c8_synthesis_spec.md superseded by pointer to the authoritative paper/research/c8_macro_l2_synthesis_spec.md - one governing spec per C-number, both histories preserved, differences itemized (DML estimand stood down for the hazard estimand; VPIN not a frozen trigger). (2) Amendment 1 appended to the authoritative C8 spec: the 0.8 branching-ratio threshold grounded in the acquired Filimonov-Sornette source with exact page cites (modern regime 0.7-0.8 with spikes at 0.9, pp.13-14; May 6 2010 precursory rise toward n=1 vs April 27 exogenous flat n, p.17; 194 events/sec peak, p.9); no threshold changed, no new line armed - if the perp regime baseline differs, that is a K7 finding, not a re-tune. (3) paper/research/roadmap_to_endpoint.md: the endpoint defined (a complete ledger, not a profitable strategy), decision tree from L0 gate to C8 to sizing, seven methodology improvements (single-spec rule, verification-harness rule, repo-weight policy, pre-registration template, library triage protocol, null-time playbook, harvestable-defined), and the null-time backlog. (4) .devcontainer: python 3.12 image, postCreateCommand installs the pipeline stack (incl. scikit-learn, found missing via the test suite) and runs all 121 tests - a codespace that boots red is a broken environment; TARDIS_API_KEY via Codespaces secret. Test suite verified green locally (121 passed). (5) Website: resources.html gains section 3, the acquired library (186 papers, acquisition policy, topic-family table), kicker updated.)

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
