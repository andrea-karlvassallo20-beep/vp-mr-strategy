# 032 — Generalized Autoregressive Conditional Heteroskedasticity (Bollerslev, 1986)

**Venue:** Journal of Econometrics | **Category:** Volatility & risk
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
GARCH adds the lagged conditional variance to ARCH, giving a
parsimonious, persistent volatility process that matches the long
memory of empirical volatility with very few parameters. GARCH(1,1)
became the workhorse of financial econometrics.

## The math that matters
$\sigma_t^2 = \omega + \alpha\,\epsilon_{t-1}^2 + \beta\,\sigma_{t-1}^2$;
stationarity $\alpha + \beta < 1$; unconditional variance
$\omega/(1-\alpha-\beta)$; log-likelihood as in ARCH with the
recursion for $\sigma_t^2$.

## Why it matters for the L2 project
The honest baseline the vol-tautology kill line requires: before
crediting any OHLCV-derived "priming" feature, the K1 check fits the
vol-factor-only model — operationally a GARCH-type filter — and
demands the priming model beat IT out of sample, not beat zero.

**Caveat:** Verify against library source before production.
