# 045 — Long Memory in Stock Market Prices and a New Model (Mandelbrot, 1971)

**Venue:** Journal of Business (record to verify) | **Category:** Financial time series
**Status:** Synthesized from LLM internal knowledge (Paywalled paper; catalogue flags title details to verify).

## Summary
Mandelbrot's program: financial series exhibit long-range
dependence (the Hurst phenomenon from Nile-flood hydrology) —
autocorrelations that decay hyperbolically rather than
geometrically, so "the past never washes out". Implication for
statistics: sample means converge far more slowly than
$\sqrt{n}$, and standard inference on long-memory series is
anti-conservative.

## The math that matters
Long memory: $\rho(k) \sim c\, k^{2d-1}$ with $0 < d < 1/2$; the
variance of the sample mean decays like $n^{2d-1}$, not $n^{-1}$;
fractionally integrated processes (later ARFIMA) formalize this:
$(1-L)^d x_t = \epsilon_t$.

## Why it matters for the L2 project
Two-edged: (1) if book/return features have long memory, block
bootstrap block sizes must be large and naive t-stats overstate
significance; (2) Diebold-Inoue (063) warns that regime switching
can masquerade as long memory — the C8 macro state and any long
memory estimate must be disentangled before either is believed.

**Caveat:** Verify against library source before production.
