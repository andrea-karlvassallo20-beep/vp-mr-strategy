# 024 — Identifying Bull and Bear Markets in Stock Returns (Maheu & McCurdy, 2000)

**Venue:** Journal of Business & Economic Statistics | **Category:** Regime switching & state-space
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
A Markov-switching model of monthly stock returns with a
duration-dependent (Weibull-hazard) state process: the probability
of remaining in a bull/bear market depends on how long the market
has already been in it. The estimated states line up with the
conventional chronology of bull/bear markets, but with hazards that
change with duration, and the classification is done with posterior
probabilities, not ad-hoc drawdown rules.

## The math that matters
Hazard: $\Pr(s_t = j \mid s_{t-1} = j, d_{t-1}) =
1 - \exp(-\lambda_j d_{t-1}^{\rho_j})$ with $d$ the state duration;
returns: $r_t \sim N(\mu_{s_t}, \sigma^2_{s_t})$; estimated by MLE
with the modified Hamilton filter carrying duration.

## Why it matters for the L2 project
Two lessons for the macro state: (1) regime labels should carry
posterior probabilities, not binary verdicts; (2) state duration
matters — "quiet for a long time" and "just turned quiet" may be
different states. If C8's Primed state is duration-blind, that is a
documented simplification, not an oversight.

**Caveat:** Verify against library source before production.
