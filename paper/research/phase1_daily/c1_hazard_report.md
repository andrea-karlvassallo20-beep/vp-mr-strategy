# C1 Hazard Test — BTC and ETH daily — VERDICT: FAIL (all substantive kill lines)

Spec fixed before running (director's corrections applied). Data: 1,826 daily bars
per instrument, 2021-11-12 to 2026-11-12. Volume NOT used (C1 is price-only; no
proxy issue). Spells: one triple-barrier spell per decision day (n≈1,700 per
instrument per spec), cluster-robust SE by month. Purged 6-fold CV, purge/embargo
= h. Placebo: 100 circular block-temporal shifts (real states, surrogate labels).
Scale-invariance null: 100 block bootstraps of r/sigma, full pipeline re-run.

## Side-by-side: observed vs nulls (both CIs shown together)

| Instrument / spec | Compression HR [95% CI] (pooled) | Vol-tautology HR CI (compression + rvol only) | OOF concordance | Observed gap |log HR| | Placebo gap median [p95] | Placebo reproduces >=50%? | Scale-null gap 95% band | Scale-null reproduces? |
|---|---|---|---|---|---|---|---|---|
| BTC k=1.0 h=28 (n=1738 spells, 1731 events) | 0.832 [0.645, 1.072], p=0.155 | [0.713, 1.092] | 0.557 | 0.184 | 0.194 [0.465] | YES — KILL | [0.004, 0.252] | YES — LAYER KILL |
| BTC k=2.5 h=84 (n=1682, 1665 events) | 1.033 [0.757, 1.409], p=0.837 | [0.813, 1.518] | 0.586 | 0.033 | 0.164 [0.397] | YES — KILL | [0.005, 0.425] | YES — LAYER KILL |
| ETH k=1.0 h=28 (n=1738, 1729 events) | 0.889 [0.690, 1.145], p=0.361 | [0.826, 1.225] | 0.554 | 0.118 | 0.146 [0.417] | YES — KILL | [0.006, 0.230] | YES — LAYER KILL |
| ETH k=2.5 h=84 (n=1682, 1662 events) | 0.981 [0.744, 1.295], p=0.895 | [0.912, 1.484] | 0.602 | 0.019 | 0.193 [0.417] | YES — KILL | [0.006, 0.373] | YES — LAYER KILL |

Constant-hazard LR per fold: rejected in 6/6 folds on all four cells (all folds
>=274 events; the power floor never bound — this failure is not a power failure).
PH test: violations present (tic on BTC k1.0 p<0.001; compression on BTC k2.5
p=0.014) — moot, since the claim died on stronger lines.

## Kill-line accounting

1. OOF concordance <= 0.52: NOT triggered (0.554-0.602) — but concordance is
   carried by the realized-vol covariate (lrvol HR 0.68 on BTC k2.5, p=8e-7),
   not by compression. The model ranks by volatility level; compression adds
   nothing to that ranking.
2. Vol-tautology (compression HR CI includes 1.0 after conditioning on rvol
   alone): TRIGGERED in 4/4 cells.
3. Constant-hazard unrejected in >=30% of powered folds: not triggered.
4. Block-temporal placebo reproduces >=50% of gap: TRIGGERED in 4/4 cells.
5. Scale-invariance null reproduces gap within 95% band: TRIGGERED in 4/4 cells
   on BTC and ETH daily — the pre-declared WHOLE-LAYER kill fires.

## Verdict

C1 is dead on both instruments, and the whole-layer falsification fires:
the daily-resolution hazard layer is falsified as a flow-duration theory and is
demoted to a volatility clock. Per the pre-declared conclusion, a volatility
clock with RR ~1.4 is not a low-drawdown structure; the layer is dead as a
timing edge on this data.

Mechanisms that died (named, not pivoted):
- Liquidity-aging duration dependence: the compression-state/future-event
  alignment is fully reproduced by a vol-clustering-preserving block-temporal
  null (placebo gap median >= observed gap in 3/4 cells).
- Compression as an independent state: carries no hazard information beyond
  realized-vol level (tautology CI includes 1.0 everywhere).
- Scale-invariance: the entire observed gap sits inside the null band produced
  by ATR scaling + vol clustering alone.

Not dead (and not claimed): the descriptive fact that realized-vol level
orders time-to-barrier. That is the volatility clock itself, already bounded by
the pre-declared conclusion; it is not promoted to a claim here.

C3/C4 were never run (they condition on a base hazard that has now failed).
C2 (ETFs) remains queued per the director's instruction; C5/C6 remain blocked.
