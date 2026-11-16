# 063 — Long Memory and Regime Switching (Diebold & Inoue, 2001)

**Venue:** Journal of Econometrics | **Category:** Regime switching & state-space
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Shows that long memory and regime switching are easily confused:
a regime-switching process with low-frequency persistent states
generates the hyperbolic autocorrelation decay and slow
mean-reversion that define "long memory" in the GPH/spectral
estimators. Conversely, genuine long-memory processes make
regime tests find spurious states. The two are observationally
similar; identification requires structural assumptions.

## The math that matters
Markov chain with persistent states has
$\rho(k) \approx c_1 \lambda^k + c_2 k^{2d-1}$-mixture behavior;
GPH estimator $\hat d$ from the periodogram regression
$\log I(\omega_j) = c + (1-2d)\log\omega_j + u_j$ is biased
toward long memory by switching.

## Why it matters for the L2 project
Critical for the macro state: "quiet" (C7 Primed) is a
persistent regime — any long-memory statistic computed on the
panel (e.g. for block bootstrap sizing) may be measuring the
regime structure, not true fractional integration. C8 must state
which interpretation it assumes and why.

**Caveat:** Verify against library source before production.
