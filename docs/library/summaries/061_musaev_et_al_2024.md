# 061 — Adaptive Algorithms for Change Point Detection in Financial Time Series (Musaev, Grigoriev & Kolosov, 2024)

**Venue:** AIMS Mathematics | **Category:** Regime switching & state-space
**Status:** Open-access at the publisher (AIMS); not machine-downloadable from this environment — summary synthesized from LLM internal knowledge. Verify against library source before production.

## Summary
A recent survey/methods paper on change-point detection for
financial series: CUSUM and its variants, Bayesian online
change-point detection, kernel-based two-sample tests, and
adaptive thresholding under nonstationarity, with comparative
performance on financial data. Emphasizes algorithms that adapt
their detection threshold to local volatility to control false
alarms.

## The math that matters
The general online detection framework: alarm when a discrepancy
$D(\hat F_{window}, \hat F_{ref})$ exceeds an adaptive threshold
$q_{1-\alpha}(t)$; CUSUM is the likelihood-ratio special case
(see 012), and two-sample kernel tests (MMD) are the
distributional generalization.

## Why it matters for the L2 project
The menu of detectors for the L2 gate: with WATCH (043) as the
Wasserstein option, this supplies the adaptive-threshold
machinery so that a stressed book does not drown the detector in
false alarms.

