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
| Cont, Kukanov, Stoikov (2014), "The Price Impact of Order Book Events" | Order Flow Imbalance (OFI) | Extracted to `docs/math_cheatsheet.md` |
| Filimonov, Sornette (2012/2014), Hawkes-process endogeneity of markets | Hawkes intensity, branching ratio | Extracted to `docs/math_cheatsheet.md` |
| Lopez de Prado (2018), "Advances in Financial Machine Learning", ch. 7 | Combinatorial Purged Cross-Validation (CPCV) | Extracted to `docs/math_cheatsheet.md` |

## Non-goals

- No PDF files in the repo (size, licensing, and zero marginal value).
- No scraping infrastructure to maintain.
- The paper text is not needed; the formulas and their executable
  equivalents are the deliverable.

With the cheatsheet written, the library task is closed. Active work
returns to the L2 deployment: `CLOUD_DEPLOY.md` and the
`.devcontainer` for the Codespaces L2 data pipeline.
