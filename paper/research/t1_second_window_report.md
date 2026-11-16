# T1 executed — second aggTrades window (2024-08-01 → 2025-02-28)

Owner-authorized run, 2026-11-16. The pre-registered harness ran UNCHANGED
on a regime it never saw during construction: 212/212 calendar days,
333,527,416 BTCUSDT USDS-M aggTrades rebuilt from public Binance Vision
archives and converted through the normalized parquet schema (int64 UTC
microseconds verified at both ends). 20,351 spells, 12,272 events, 0
macro-censored; 96 first-day startup spells with undefined trailing-sigma
covariates dropped (data-startup exclusion, printed, not silent — the
24h trailing window is incomplete at the window's first day).

## The numbers

- **Out-of-fold concordance (pooled OOF Harrell C): 0.6590** (kill line a:
  ≤ 0.52 → not fired)
- **Stratified (HOD) compression HR: 0.738, CI [0.702, 0.776]** — excludes
  1.0 (kill line d: collapse under stratification → not fired)
- **Vol-tautology (sigma-conditioned) HR: 0.590, CI [0.566, 0.615]** —
  **EXCLUDES 1.0** (kill line b: CI includes 1.0 → NOT fired; the
  compression covariate carries information beyond realized volatility —
  this is NOT quietness wearing a vol costume)
- **Compression-only HR: 0.516, CI [0.496, 0.538]**
- **Constant-hazard null: LR unrejected in 0 of 6 powered folds**
  (all fold p = 0.0; kill line c: ≥30% unrejected → not fired)
- **Scale-invariance (block-shuffled) placebo: observed |log HR| gap
  0.1328; null 95% band [0.1354, 0.2018]** — the null does NOT reproduce
  the observed gap (kill line e → not fired). Margin is thin: the observed
  gap sits 0.0027 below the null band's lower edge. Recorded, not hidden.

**STATUS per the pre-declared kill lines: survives all five.**

## The sign finding — stated plainly, because it matters more than the verdict

The pre-registered MECHANISM says compression aging RAISES the conditional
hazard of a trade-touch excursion. Every measured compression hazard
ratio on this window is **below 1.0**: deeper taker-measured compression
is associated with a LOWER within-spell hazard of a noise-floored
trade-touch excursion. The kill lines were written to detect absence of
information (CIs including 1.0, null-reproduced gaps) — none of them is
sign-guarded, so the claim survives as registered. But the direction
contradicts the coil-exit story at the within-spell hazard scale, and the
programme does not bury direction in a verdict word.

Three readings, recorded, not resolved:
1. **Scale mismatch.** The daily-grain coil-exit story may live at the
   daily-bar scale; the 15-minute spell clock may measure a different
   object (intra-day quiet persistence).
2. **The taker-only constraint, in CKS's own words.** Cont-Kukanov-Stoikov
   find the price-impact information lives in quote events — limit orders
   and cancellations — not in trades; the passive-withdrawal mechanism is
   invisible here by construction. A taker-side compression clock that
   predicts silence is exactly what the C5/C6 no-proxy-substitution rule
   anticipated.
3. **Noise-floor artifact.** Trade-touch barriers floored at 10x the
   median spread proxy are harder to touch from deep quiet by
   construction; the hazard inversion may partly be the barrier geometry,
   not the market.

No pivot, no re-tuning, no surviving-variant search. The result stands
as measured: the covariate is informative, non-tautological, and
inverted relative to the mechanism as stated. The L2 phase inherits this
as a sharper question: if compression carries information but points the
wrong way on taker data, the passive side is where the sign must be
resolved — which is precisely what C1-L2/C5 were designed to see and
aggTrades cannot.

DATA FLAG (binding): aggTrades = taker-side executed prints only; no
resting quote additions/cancellations, no queue depth, no iceberg
visibility. All features in this run are TAKER-ONLY.
