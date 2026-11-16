# Library manifest

## PDF acquisition: ABORTED

PDF scraping of the research library is stopped. No PDFs will be
downloaded, parsed, or stored in this repository. The library is
delivered as synthesized knowledge instead: the mathematical core of
each critical paper is extracted into executable form
(`docs/math_cheatsheet.md`), which is faster and more useful than
reading a PDF.

## Critical papers (extracted, not stored)

| Paper | Core concept | Status |
|---|---|---|
| Cont, Kukanov, Stoikov (2014), "The Price Impact of Order Book Events" | Order Flow Imbalance (OFI) | Extracted to `docs/math_cheatsheet.md`; VERIFIED against the arXiv LaTeX source (arXiv:1011.6402v3, Sec. 2.1) 2026-11-16 — byte-exact, 2 defects fixed (`paper/research/math_verification_2026-11-16.md`) |
| Filimonov, Sornette (2012/2014), Hawkes-process endogeneity of markets | Hawkes intensity, branching ratio | Extracted to `docs/math_cheatsheet.md`; VERIFIED against the `tick` library (v0.8.0.2) on exact simulations 2026-11-16 — 3 defects fixed, branching ratio now the true spectral radius of G |
| Lopez de Prado (2018), "Advances in Financial Machine Learning", ch. 7 | Combinatorial Purged Cross-Validation (CPCV) | Extracted to `docs/math_cheatsheet.md` |

The library is no longer merely extracted: the two load-bearing papers
(CKS, Filimonov-Sornette) are SOURCE-VERIFIED and CROSS-CHECKED, and the
verification is re-runnable (`src/verify_math_library.py`) with hermetic
regression tests (`tests/test_math_exactness.py`). The public page:
`docs/math_verification.html`.

## Non-goals

- No PDF files in the repo (size, licensing, and zero marginal value).
- No scraping infrastructure to maintain.
- The paper text is not needed; the formulas and their executable
  equivalents are the deliverable.

With the cheatsheet written, the library task is closed. Active work
returns to the L2 deployment: `CLOUD_DEPLOY.md` and the
`.devcontainer` for the Codespaces L2 data pipeline.
