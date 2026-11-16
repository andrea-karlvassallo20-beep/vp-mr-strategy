# The Salient Market Hypothesis: a paper draft (null-time, no new results)

Status: DRAFT OUTLINE ONLY, written during null time. It reports only
already-recorded findings; nothing new is measured here, no claim is
evaluated, and every number below is already committed in the repo with its
kill line. The paper is written only if C1-L2 resolves either way - a
falsified hypothesis with three honest deaths is the finding, not a
failure.

## Title (working)

"Compression Is a Costume: Three Deaths of the OHLCV Volatility-Compression
Family, and the Move to the Order Book"

## Abstract (sketch)

We pre-registered, ran, and honestly killed a family of claims that
low-volatility compression states predict significant price events
("coils spring"). The family died three independent times: at daily grain
on the C1 hazard model (all kill lines fired), on the 532-series watchlist
(descriptive, no ranking power), and at 30-minute grain on 78 crypto
perpetuals (C7-30m: +0.00211 mean out-of-sample uplift, CI includes zero,
16,402 eras - a coin flip). The pattern across all three: compression
measured from OHLCV is volatility wearing a costume; the "quiet state"
carries no information beyond quietness itself. We then re-ask the question
where it should have been asked from the start: the order book. We specify
C1-L2, a pre-registered Cox hazard test of book-measured compression
(trailing range in sigma_H units, percentile-ranked per hour-of-day pool)
on gated full-depth Binance futures L2, with five armed kill lines, purge
and embargo on the wall-clock label horizon, and hour-of-day
stratification as a mandatory control. The spec, the harness, and the kill
lines are frozen before the data is unsealed.

## 1. The death of AVFI (Phase 1, closed)

- The AVFI programme (NQ weekly): AVFI is a slow regime descriptor, not a
  weekly timer; the 27-combo grid family fails the White reality check.
- The daily C1 hazard experiment: FAILED, every kill line fired
  (`paper/research/phase1_daily/c1_hazard_report.md`).
- The watchlist interim: no ranking power in the descriptive board.
- The 30m C7-30m verdict: +0.00211, CI includes zero, 50.4% positive -
  the third independent death of the compression family
  (`paper/research/phase1_daily/c7_30m_test_result.md`, taught at
  `docs/ohlcv_verdict.html`).
- What survives: the METHOD, not the claim. Pre-registration, kill lines,
  honest verdicts, and the discipline that a control group must isolate
  the costume from the wearer.

## 2. The birth of the C7 Crypto Edge (Phase 2, active)

- The clue program confined the candidate set to crypto: 37 of 39 deep
  coils are crypto; funding and open-interest positioning give the
  "grievance" a measurable axis that equities lack at retail granularity.
- C7-L2 is the family's second life: the same WHAT question, measured from
  the book itself (compression = trailing realized range in sigma_H units,
  the book's own clock), not from OHLCV bars.
- The C8 Macro-L2 Synthesis is pre-registered behind it (eleven kill
  lines), restated after independent review as a PURE difference-of-
  differences interaction with DML orthogonalization, a shuffled-arrival
  placebo for the Hawkes n_c > 0.8 threshold, a fixed volume-bucket clock
  for VPIN, and a defined market-book factor.

## 3. The transition to L2: the C1-L2 test

- Data: Tardis full-depth binance-futures incremental_book_L2, gated by
  `src/gate_tardis_sample.py` (mid and depth agreement against
  book_snapshot_25; parity anchors recorded for 2026-10-01 and
  2026-10-10). Nothing is evaluated before the gate passes.
- Clock: mid sampled at every BBBA change; trade-touch labels only (a
  barrier is hit on a traded print through the level, never a quote
  flicker); purge/embargo on the wall-clock horizon (CPCV); macro
  censoring of scheduled-event windows BEFORE labeling.
- Estimand: hazard of a K*sigma_H move within H=24h, compression state at
  entry, hour-of-day stratified, five kill lines as binding asserts
  (`src/c1_l2_test.py`, spec `paper/research/c1_l2_test_spec.md`).
- The dry run on 2026-10-01 proved the machinery (57,498 BBBA touch
  events, 19,551 compression events, 74 decision rows; purge empties all
  folds on a 1-day window - correct behavior, documented).

## 4. Methodology: the SMH architecture, reviewed

Null-time review of the KM / Cox / CPCV stack (`strategy/smh_hazard.py`,
`src/cox_diagnostics.py`, `src/event_clock.py`, `src/c1_l2_test.py`).
Findings, all recorded as notes - no code changed, no result affected:

1. Kaplan-Meier (`kaplan_meier`): censoring handled exactly (at-risk set
   decremented by deaths + censorings at each distinct time; survival
   multiplied only at deaths). No defect found.
2. Cox partial likelihood (`cox_fit`): Breslow ties, risk set `T >= T[i]`
   (correct for Breslow), numerically stable shifted-exposure gradient,
   Newton step on the negative-definite Hessian with a small ridge; SEs
   from the observed information. Edge cases worth stating in the paper:
   (a) the loop can exit on a non-finite step with a stale Hessian - the
   SEs of an unconverged fit should not be quoted; (b) the OOF split in
   `_oof_concordance` is "time-ordered" only in list order, and the
   episode list is built per-ticker, so the split is series-grouped, not
   globally chronological - leakage-free (entry covariates are strictly
   causal) but not a chronological split; the L2 harness avoids this by
   splitting on wall-clock CPCV. (c) `t = k + 1` in the episode builder is
   identical on both branches (after an event the remaining compression
   bars are skipped until re-entry) - a frozen-definition quirk to state
   honestly, not a bug.
3. Harrell's concordance: ties at equal event time with censored
   comparators handled the standard way; frozen.
4. CPCV purge/embargo: `assert_no_leakage` is asserted in the harness and
   the tests; embargo equals the label horizon. The known edge case is
   documented behavior, not a bug: on a window shorter than H+embargo the
   folds empty (6/6 folds, train rows 0) - do not shorten the horizon to
   force folds.
5. PH diagnostics (`src/cox_diagnostics.py`): counting-process Cox with
   strata, Grambsch-Therneau Schoenfeld test over three time transforms,
   automatic hour-of-day x regime stratification at p < 0.05, and a
   binding kill at p < 0.01 if the violation persists - reviewed,
   consistent with the pre-registered spec.

## 5. What would falsify the L2 family

The five C1-L2 kill lines (verbatim owners: `src/c1_l2_test.py`): OOF
concordance <= 0.52; vol-tautology (compression HR CI includes 1.0 after
conditioning on sigma alone); constant-hazard null unrejected in >= 30% of
powered folds; the effect dies under hour-of-day stratification; and the
scale-invariance null reproducing the observed gap (whole-layer kill,
demote to a volatility clock). C8's eleven kill lines sit behind them.

## 6. Honesty ledger

Every claim this paper would report is already in the claims ledger
(`docs/ledger.html`) with its status and its kill line. The paper adds
narrative, never evidence. If C1-L2 dies too, the paper's title changes
and its conclusion is the same shape: four deaths, and the question moves
again - this time to the microstructure interaction (C8) or to closure.
