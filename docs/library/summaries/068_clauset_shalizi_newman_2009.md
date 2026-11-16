# 068 — Power-Law Distributions in Empirical Data (Clauset, Shalizi & Newman, 2009)

**Venue:** SIAM Review | **Category:** Volatility & risk
**Status:** Downloaded legally (arXiv:0706.1062); full text: `docs/library/text/068_clauset_shalizi_newman.txt`.

## Summary
The rigorous recipe for power-law claims: the discrete
MLE $\hat\alpha$ for the exponent, the KS goodness-of-fit test
with a parametric bootstrap p-value, and — the paper's most
cited contribution — the likelihood-ratio comparison against
alternative heavy-tailed distributions (lognormal, stretched
exponential), since power-law fits are almost never uniquely
supported. Most published power-law claims do not survive the
recipe.

## The math that matters
$p(x) \propto x^{-\alpha}$ over $x \ge x_{\min}$;
$\hat\alpha = 1 + n\left[\sum_i \ln(x_i/x_{\min-1/2})\right]^{-1}$
(discrete MLE); bootstrap KS p-value; Vuong likelihood-ratio
test between power law and alternatives.

## Why it matters for the L2 project
Two uses: (1) the branching ratio near 1 (C8's Hawkes micro
state) implies critical, power-law-ish event clustering — any
such claim about perps trade data must survive this paper's
recipe, not just a log-log plot; (2) the general lesson: fit
alternatives before naming a distribution; the project applies
the same standard to "the effect is X" claims (fit the null
first).

**Caveat:** Verify page numbers against the extracted text
before production.
