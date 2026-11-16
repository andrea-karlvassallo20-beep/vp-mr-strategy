# 006 — The Cross-Section of Expected Stock Returns (Fama & French, 1992)

**Venue:** Journal of Finance | **Category:** Backtesting & FML
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
The empirical bombshell: beta (the CAPM's only priced risk) has
essentially no explanatory power in the 1963–1990 cross-section once
size (ME) and book-to-market (BE/ME) are included. Size and value are
strong, monotone, and robust; the relation between beta and return is
flat. This killed the pure CAPM as an empirical description and opened
the modern era of characteristic-based asset pricing — and of
characteristics mistaken for risk.

## The math that matters
Fama-MacBeth cross-sectional regressions: monthly
$\bar R_t = \gamma_0 + \gamma_1 \beta + \gamma_2 \ln(ME) +
\gamma_3 \ln(BE/ME) + e_t$, with $\gamma_1 \approx 0$.

## Why it matters for the L2 project
A canonical case of a "factor" that is really a characteristic. The
project's compression-family deaths (C1, C7) are the same lesson in
microstructure clothing: measured "priming" may be a named variable
that adds nothing beyond a dominant factor. Test the increment, not
the name.

**Caveat:** Verify against library source before production.
