# 007 — The Deflated Sharpe Ratio (Bailey & Lopez de Prado, 2014)

**Venue:** Journal of Portfolio Management | **Category:** Backtesting & FML
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Corrects a Sharpe ratio for two selection effects: (1) the number of
trials $N$ that produced the strategy, and (2) the non-normality
(skewness, kurtosis) of returns. The expected maximum Sharpe under the
null of no skill grows like $\sqrt{2\ln N}$; a reported Sharpe must be
judged against that bar, not against zero. The DSR is the probability
that the true Sharpe exceeds zero after these corrections.

## The math that matters
Expected max SR: $E[\max_n SR_n] \approx \sqrt{2\ln N}\,(1 - \gamma/(2\ln N))$
with $\gamma$ the Euler-Mascheroni constant; the deflated benchmark
$SR^* = \sqrt{V[SR_n]}\cdot\left((1-\gamma)\Phi^{-1}(1-1/N) +
\gamma\Phi^{-1}(1-1/(Ne))\right)$; then
$DSR = \Phi\left(\frac{(SR - SR^*)\sqrt{T-1}}{\sqrt{1-\hat\gamma_3 SR +
\frac{\hat\gamma_4-1}{4}SR^2}}\right)$ with $\hat\gamma_3,\hat\gamma_4$
skew/kurtosis.

## Why it matters for the L2 project
Kill line K3 of C7 names DSR explicitly. C8 will try multiple L2
thresholds (branching ratio cutoffs, OFI extremes); its TEST reading
must be deflated over that count, using exactly this machinery.

**Caveat:** Verify against library source before production.
