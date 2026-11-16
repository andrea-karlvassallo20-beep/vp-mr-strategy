# 021 — A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle (Hamilton, 1989)

**Venue:** Econometrica | **Category:** Regime switching & state-space
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Introduces the Markov-switching autoregression: an unobserved
two-state Markov chain (expansion/recession) modulates both the
mean and the variance of GNP growth. Estimated by maximum
likelihood via the Hamilton filter (a Kalman-like recursion over
the state probabilities). The filtered probabilities recover the
NBER business-cycle dates without ever being told them — the
founding demonstration that regimes are statistically real.

## The math that matters
$s_t \in \{0,1\}$ with $P(s_t = j \mid s_{t-1} = i) = p_{ij}$;
$y_t = \mu_{s_t} + \sum_i \phi_i (y_{t-i} - \mu_{s_{t-i}}) +
\epsilon_t$, $\epsilon_t \sim N(0, \sigma^2_{s_t})$; likelihood via
$\Pr(s_t = j \mid y_{1:t}) \propto p_{ij}\Pr(s_{t-1}=i \mid y_{1:t-1})\,
f(y_t \mid s_t = j)$.

## Why it matters for the L2 project
The macro state in C8 (C7 Primed) is a regime label; the
Hawkes branching ratio is another. Hamilton's discipline — estimate
the state, then check it against out-of-sample events, never fit
the state to the answer — is the template for C8's state
definitions, which must be frozen before the test.

**Caveat:** Verify against library source before production.
