# 037 — Backtest Overfitting in the Machine Learning Era (Arian, Mobarekeh & Seco, 2024)

**Venue:** Knowledge-Based Systems | **Category:** Backtesting & FML
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
A modern restatement of the overfitting problem for nonstationary,
ML-driven strategies: with flexible models and nonstationary data,
in-sample/OOS gaps widen and standard CV misleads. Reviews
validation schemes (purged CV, adversarial CV, combinatorial
splits) and argues for performance evaluation robust to
distribution shift, not just to parameter search.

## The math that matters
Overfitting under nonstationarity: the OOS degradation
$\Delta = \text{IS} - \text{OOS}$ has two components — selection
(classic data snooping) and shift (the joint law of data changing
between train and test); purged/embargoed splits address leakage,
not shift, so regime-stratified reporting is also required.

## Why it matters for the L2 project
Directly the C8 design problem: C8 splits must both purge leakage
(CPCV) and report per-regime (2024 validation vs 2025-26 test,
kill line K4). A single pooled number would hide a shift artifact.

**Caveat:** Verify against library source before production.
