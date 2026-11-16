# 005 — Common Risk Factors in the Returns on Stocks and Bonds (Fama & French, 1993)

**Venue:** Journal of Financial Economics | **Category:** Backtesting & FML
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Constructs the three-factor model: market excess return, SMB (small
minus big), HML (high minus low book-to-market). Monthly factor
returns are built from 2x3 size/BM sorted portfolios, rebalanced
annually. Time-series regressions of portfolio returns on the three
factors absorb most pricing anomalies of the era; the intercept (alpha)
is the test of the model.

## The math that matters
$R_{it} - R_{ft} = a_i + b_i(R_{Mt}-R_{ft}) + s_i\,\text{SMB}_t +
h_i\,\text{HML}_t + e_{it}$; the model predicts $a_i = 0$ for all $i$.

## Why it matters for the L2 project
Not directly actionable for L2, but two habits transfer: (1) factors
are *constructed, documented portfolios*, not latent claims — the
project's features should be reproducible from raw data alone; (2)
testing is done on the residual (alpha), i.e. after removing known
common variation — the C7 vol-factor conditioning (K1) is exactly this
habit applied to "priming".

**Caveat:** Verify against library source before production.
