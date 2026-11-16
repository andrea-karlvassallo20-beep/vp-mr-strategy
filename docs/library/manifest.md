# Library manifest

## PDF acquisition: legal open-access only

PDF scraping of paywalled sources is stopped and was never
attempted. Acquisition runs through legal open-access routes only:
arXiv (known IDs + title search via the arXiv API) and Unpaywall
(DOI-based OA location lookup; requires the owner's email for the
API). The runner is `src/library_acquire.py`; the per-paper status
log is `acquisition_log.json`.

## Acquisition status (68-paper catalogue)

- **7 papers downloaded and text-extracted** (arXiv, legal):
  011, 018 (Cont-Kukanov-Stoikov OFI), 019, 038, 044, 065 (DML),
  068. PDFs in `pdfs/`, plain text with page markers in `text/`.
- **2 papers open-access at the publisher** (SAGE Open 060, AIMS
  Mathematics 061) but not machine-downloadable from this
  environment; to be fetched manually in the codespace.
- **59 papers paywalled or preprint-only**: no legal bulk route
  found in this session; their knowledge is synthesized (below).

## Synthesis status

- **68 one-page summaries** in `summaries/` (one per catalogue
  entry): what the paper does, the math that matters, and why it
  matters for the L2 project.
  - Downloaded papers cite the extracted text and (for 018) exact
    arXiv PDF page numbers for the math.
  - Papers that could not be downloaded are labeled:
    **"Synthesized from LLM internal knowledge (Paywalled
    paper)."** and carry the warning **"Verify against library
    source before production."**
- **The math cheat sheet** (`docs/math_cheatsheet.md`): the exact
  formulas and executable numpy implementations for OFI
  (Cont-Kukanov-Stoikov), Hawkes intensity + MLE
  (Filimonov-Sornette), CPCV (Lopez de Prado), Kyle's lambda, and
  VPIN (Easley-Lopez de Prado-O'Hara). All code blocks are
  executed and tested before commit.

## Non-goals

- No paywalled PDFs, no scraping of publisher sites, no shared
  credentials, no Unpaywall API calls with a fabricated email.
- The paper text is not the deliverable; the formulas and their
  executable equivalents are.

## Where the library is used

`docs/c8_synthesis_spec.md` (the C8 combination test) draws its
micro-state definitions (OFI, Hawkes branching ratio, VPIN), its
estimand (DML), and its kill-line precedents directly from these
summaries and the cheat sheet.

The library task is closed. Active work: the L2 Codespaces
deployment (`CLOUD_DEPLOY.md`, `.devcontainer`).
