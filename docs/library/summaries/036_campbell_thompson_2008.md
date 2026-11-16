# 036 — Predicting the Equity Premium Out of Sample (Campbell & Thompson, 2008)

**Venue:** Journal of Financial Economics | **Category:** Asset pricing & efficiency
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Return predictability (dividend yield, payout ratio, etc.) looks
weak out of sample — until you impose weak economic restrictions
(the forecast equity premium is never negative; coefficients have
theory-consistent signs). With those priors, OOS predictive
$R^2$ turns modestly positive and economically meaningful for
allocation. The lesson: theory-restricted forecasts beat
unrestricted ones out of sample.

## The math that matters
OOS $R^2_{OOS} = 1 - \frac{\sum (r_{t+1} - \hat r_t)^2}{\sum (r_{t+1}
- \bar r_t)^2}$ vs the historical-mean benchmark; restricted
forecaster: $\hat r_t = \max(0, \hat\beta' x_t)$ with sign
constraints on $\hat\beta$.

## Why it matters for the L2 project
The pre-registration discipline in C7/C8 is the same move: freeze
theory-motivated restrictions BEFORE the test, and the OOS reading
becomes meaningful. Campbell-Thompson is the canonical evidence
that restrictions buy honesty, not just rigidity.

**Caveat:** Verify against library source before production.
