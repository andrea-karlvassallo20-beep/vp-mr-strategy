# Library manifest

## PDF acquisition: legal open-access only

PDF scraping of paywalled sources is stopped and was never
attempted. Acquisition runs through legal open-access routes only:
arXiv (known IDs + title search via the arXiv API) and Unpaywall
(DOI-based OA location lookup; requires the owner's email for the
API). The runner is `src/library_acquire.py`; the per-paper status
log is `acquisition_log.json`.

## Acquisition status (68-paper catalogue)

- **10 papers downloaded and text-extracted** (legal OA):
  011, 018 (Cont-Kukanov-Stoikov OFI), 019, 038, 043 (WATCH — the
  research lead, IEEE author version via arXiv:2201.07125), 044,
  061 (AIMS), 064 (Springer OA), 065 (DML), 068. PDFs in `pdfs/`,
  plain text with page markers in `text/`. Sources: arXiv (known
  IDs + title search) and OpenAlex; the Semantic Scholar route was
  tried, returned one wrong paper (034), and was removed.
- **8 papers legally open-access but publisher bot-blocked**
  (004, 007, 009, 015, 016, 026, 059, 060 — Wiley/SAGE/Annual
  Reviews/SIAM direct PDFs return HTTP 403 to non-browser agents):
  to be fetched manually in the codespace browser. Not scraped.
- **50 papers paywalled or preprint-only**: no legal bulk route
  found; their knowledge is synthesized (below).

## Expanded library: 100 additional legal-OA papers

`src/library_expand.py` searched OpenAlex (OA-filtered) and the
arXiv API across the project's topic families (microstructure/LOB,
Hawkes/self-excitation, order flow/VPIN, market impact/execution,
backtesting/overfitting, regime switching, change-point/optimal
transport, ML-finance, volatility, crypto microstructure) and
acquired **100 more legally open-access PDFs** with extracted text:
- PDFs: `pdfs/` (total 110 with the core catalogue)
- Texts: `text/` (page-marked plain text)
- Index: `expanded_index.md` / `expanded_index.json` (topic tag,
  title, authors, year, venue, file)
Duplicates against the 68-paper core catalogue are excluded;
off-topic strays (e.g. literal "transport infrastructure" matches)
are filtered; no paywalled or bot-blocked source is scraped.

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


## Round 3 (PR #132): 29 additional legal-OA PDFs, zero overlap with rounds 1-2

Acquired via Unpaywall (Crossref DOI resolution) + arXiv title search + published OA links. Every file byte-checked as %PDF-. Sources:

- **004** A Test for Superior Predictive Ability — arXiv preprint
- **007** The Deflated Sharpe Ratio — arXiv preprint
- **009** The Probability of Backtest Overfitting — arXiv preprint
- **018** The Price Impact of Order Book Events — Unpaywall/OA via DOI 10.1093/jjfinec/nbt003
- **020** Optimal Execution of Portfolio Transactions — arXiv preprint
- **029** Random Forests — arXiv preprint
- **031** Autoregressive Conditional Heteroscedasticity — arXiv preprint
- **032** Generalized Autoregressive Conditional Heteroskedasticity — arXiv preprint
- **033** Realized Volatility — Unpaywall/OA via DOI 10.3386/w8160
- **034** Do Stock Prices Move Too Much to Be Justified by Subsequent Changes in Dividends? — Unpaywall/OA via DOI 10.3386/w0456
- **035** On the Cross-Section of Expected Returns — arXiv preprint
- **036** On the Predictability of Stock Returns: An Asset-Allocation Perspective — Unpaywall/OA via DOI 10.3386/w4997
- **039** The Cross-Section of Volatility and Expected Returns — Unpaywall/OA via DOI 10.3386/w10852
- **042** The Statistics of Sharpe Ratios — arXiv preprint
- **043** WATCH: Wasserstein Change Point Detection for High-Dimensional Time Series — Unpaywall/OA via DOI 10.1109/BigData52589.2021.9671962
- **044** Wasserstein GAN — arXiv preprint
- **045** Long Memory in Stock Market Prices and a New Model — Unpaywall/OA via DOI 10.3386/w2984
- **049** A Mathematical Framework for Modeling Order Book Dynamics — arXiv preprint
- **052** Commonality in Liquidity — arXiv preprint
- **053** Cross-Impact of Order Flow Imbalance in Equity Markets — arXiv preprint
- **058** Trade Co-occurrence, Trade Flow Decomposition and Conditional Order Imbalance — arXiv preprint
- **059** A Stochastic Partial Differential Equation Model for Limit Order Book Dynamics — arXiv preprint
- **061** Adaptive Algorithms for Change Point Detection in Financial Time Series — Unpaywall/OA via DOI 10.3934/math.20241674
- **062** Can the Markov Switching Model Forecast Exchange Rates? — Unpaywall/OA via DOI 10.3386/w4210
- **063** Long Memory and Regime Switching — Unpaywall/OA via DOI 10.3386/t0264
- **064** Multiple Change Point Detection and Validation in Autoregressive Time Series — Unpaywall/OA via DOI 10.1007/s00362-020-01198-w
- **065** Double/Debiased Machine Learning for Treatment and Structural Parameters — Unpaywall/OA via DOI 10.3386/w23564
- **066** Statistical Modeling: The Two Cultures — arXiv preprint
- **068** A Practical Guide to Heavy Tails — Unpaywall/OA via DOI 10.1137/070710111

The 39 still-missing paywalled articles remain the owner's supply list (DOIs in the round-3 manifest section below).
