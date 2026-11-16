# 025 — Markov Switching Models in Empirical Finance (Guidolin, 2011)

**Venue:** IGIER Working Paper | **Category:** Regime switching & state-space
**Status:** Synthesized from LLM internal knowledge (working paper; may be freely downloadable — script verifies).

## Summary
A survey of Markov-switching applications in empirical finance:
equity returns (bull/bear), interest rates, the term structure,
portfolio allocation under regimes, and the Fisher relation. Its
value is taxonomic: it catalogs which financial series show
regime behavior, which specifications are standard (MS-VAR,
MS-GARCH, MS term-structure), and where regime models improve
forecasting versus single-state benchmarks.

## The math that matters
The general MS framework:
$y_t = \mu_{s_t} + A_{s_t}(L) y_{t-1} + \Sigma_{s_t}^{1/2}\epsilon_t$,
with $s_t$ Markov; forecasts mix regime-conditional forecasts with
predicted state probabilities.

## Why it matters for the L2 project
A checklist before C8: regime interaction claims (macro x micro)
must beat the single-state benchmark on the same split protocol —
the survey documents how often they do not.

**Caveat:** Verify against library source before production.
