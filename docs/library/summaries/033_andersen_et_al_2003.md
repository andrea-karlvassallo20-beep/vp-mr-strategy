# 033 — Modeling and Forecasting Realized Volatility (Andersen, Bollerslev, Diebold & Labys, 2003)

**Venue:** Econometrica | **Category:** Volatility & risk
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Realized volatility: sum squared high-frequency returns over a day
gives a nonparametric, ex-post volatility measure that is
approximately Gaussian in logs and better forecastable than
GARCH-filtered estimates. The paper opens the realized-volatility
program: volatility is measurable, not just latent.

## The math that matters
$RV_t = \sum_{j=1}^{M} r_{t,j}^2$; for $M \to \infty$ (infill),
$RV_t \to \int_t \sigma^2(s)ds$ (quadratic variation);
$\log RV_t$ is approximately normal, and HAR-type regressions
forecast it well.

## Why it matters for the L2 project
The project's realized_vol_30 is exactly this estimator. The C7
finding — six vol features are one factor — is anticipated here:
realized vol IS the integrated variance; the other five names are
noisy transforms of it. The L2 extension (realized vol measured
from the book) is the project's actual remaining question.

**Caveat:** Verify against library source before production.
