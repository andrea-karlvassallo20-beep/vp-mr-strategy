# Library deep-read session 83 — Optimal Execution Using Reinforcement Learning

- **Authors:** Cong Zheng, Jiafa He, Can Yang
- **Title:** Optimal execution using reinforcement learning
- **Venue:** arXiv:2306.17178v1 [q-fin.TR], arXiv stamp 19 Jun 2023 (paper
  dated July 3, 2023)
- **What it is:** a reinforcement-learning optimal-execution paper on
  BTC_USDT perpetuals that builds cross-exchange signals (plain sums across
  Binance, OKEx and Bybit of normalized per-venue quantities), regresses
  them on future returns at 100ms-10s horizons, and trains a PPO agent in
  a self-built matching simulator to beat TWAP's implementation shortfall.

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x0fc07a_optimal_execution_using_reinforcement_learning.txt,
~27 pp., page-marked). Next UNREAD triage-rank entry (score 22).

## The paper in one paragraph

The authors collect BTC_USDT perpetual order-book, best-bid-ask and trade
data from Binance, OKEx and Bybit over WebSockets on a single Hong Kong
server, aligning venues by the collector's local timestamps "to avoid
forward-looking bias" and resampling at a fixed 10ms interval (PDF
pp. 5-7). Three cross-exchange signals are built, each a plain sum of
per-exchange normalized quantities: trade-flow imbalance normalized by an
unstated min-max window "over a certain period of time" (Eqs. 1-2, 4,
PDF pp. 7-9), top-five-level order-book imbalance (Eqs. 5-6, PDF
pp. 10-11), and cross-exchange spread with an unparameterized rolling-mean
subtraction (Eqs. 9-10, PDF pp. 13-14). Regressing each on future returns
at 100ms-10s horizons, the cross-exchange sum beats its single-exchange
counterpart in in-sample linear R2 at every horizon, decaying with
horizon (Figs. 2, 5, 7, PDF pp. 9-14), with maximum predictive levels of
about 0.6 bps for the imbalance signals at 5s (Bybit; OKEx weaker at
about 0.4 bps, Figs. 3, 6, PDF pp. 10-13) and about 1.5 bps for the spread
signal, whose advantage persists at longer intervals (Figs. 7-8, PDF
pp. 14-15); one illustrative episode shows price changes leading on
Binance and OKEx while Bybit lags (Fig. 9, PDF p. 15). A PPO agent selling
V = 50 units within T = 50s at H = 10 decision points, market orders only,
is then trained in a self-built order-matching simulator with a 3 bps fee
(Eqs. 11-16, PDF pp. 16-19): it beats TWAP's implementation shortfall by
0.38 bps with single-exchange signals and 0.68 bps with cross-exchange
signals on Bybit against a TWAP IS of -3.10 bps (Table 1, PDF p. 21), by
0.27 bps on OKEx (TWAP IS -1.48 bps, unexplained against the stated fee,
Table 2, PDF p. 22), and still by 0.32 bps under a synthetic linear price
impact and zero-ending penalty (Table 3, PDF p. 23); the 5s prediction
interval dominates both 2s and 10s (Table 4, PDF p. 24), and the
cross-exchange agent pays a variance penalty the authors attribute to
cross-venue network delay (PDF pp. 22-23).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [reinforcing, no new item] Every headline magnitude in this paper is
   earned inside the authors' own simulated matching environment against
   a TWAP baseline, with in-sample-style linear R2 figures and no null
   baseline anywhere: the R2 ladder (Figs. 2, 5, 7, PDF pp. 9-14), the
   bps gains over TWAP (Tables 1-3, PDF pp. 21-23) and the action-space
   maps (Fig. 10, PDF pp. 20-21) are simulator- and venue-indexed
   magnitudes. This is exactly the class the laundering ban exists for:
   no empirical magnitude in this paper may enter the record as support
   for any programme claim, and the execution-engineering content (the
   PPO configuration, the relative-P&L reward of Eq. 14, PDF p. 18) is
   context, never program input — execution-strategy engineering is
   never operationalized under the standing hard invariants. Reinforces
   the no-edge default. No queue change.

2. [candidate sharpening, PENDING OWNER RATIFICATION] The
   feature-normalization pre-declaration, queued as the FORTY-FOURTH
   candidate: BEFORE the L0 gate, any C1-L2/C8-adjacent spec whose signal
   is defined through rolling or windowed normalization statistics — a
   min-max rescaling, a z-score, a rolling-mean subtraction, a rolling
   volatility scale — must pre-declare, in the same frozen signal
   definition, (a) the window length, (b) the estimation convention
   (strictly trailing, with the evaluation point excluded), and (c) the
   warm-up/incomplete-window handling, with the normalization constants
   counted as frozen signal configuration and every deviation a dated
   amendment before any data is touched. A signal whose normalization
   statistics are not pre-declared cannot enter a spec; a number that
   survives only under a post-hoc normalization window fails by rule.
   Earned by the paper's own mechanism: BOTH of its headline signals
   rest on rolling normalizations whose windows are never stated — the
   min-max normalization is over "a certain period of time" (Eq. 2,
   PDF p. 8) and the spread signal subtracts an unparameterized rolling
   mean (Eq. 10, PDF p. 14) — and every predictive-power figure in the
   paper (Figs. 2-8, PDF pp. 9-15) is computed on these signals, so the
   entire evidence layer cannot be audited for lookahead from the text:
   a full-sample min/max window would make the signal forward-looking and
   would inflate precisely the cross-exchange improvement the headline
   rests on. Harder-to-pass because a claim that beats its null only
   under its own post-hoc normalization window, or whose window was
   picked after seeing the result, now fails at the gate instead of
   surviving as preprocessing; it tightens the estimator-configuration
   freeze (deep-read 63) and the noise-model pre-declaration for
   de-noised inputs (deep-read 76) by extending the frozen-configuration
   class from estimators and noise models to signal-side normalization
   statistics, joining the spread-convention declaration rule (deep-read
   56) on the feature axis. Full draft with the killed-if-wrong
   counterfactual below and in the session log.

3. [interpretation caution] Price changes lead on Binance and OKEx and
   lag on Bybit in the paper's own illustrative episode (Fig. 9, PDF
   p. 15), and Bybit is easier to predict than OKEx for reasons the
   authors offer only speculatively ("may contribute", PDF p. 9).
   Reading discipline for any single-venue C1-L2/C8-adjacent result: a
   compressive or anticipatory association measured on ONE venue
   concerns that venue's price formation, not "the market" — on a
   lagging venue it can be imported co-movement with the leading venues'
   flow — so no single-venue result may be generalized cross-venue
   without the cross-market replication the programme already requires.
   No queue change.

4. [interpretation caution] The cross-exchange signals are plain sums of
   per-exchange normalized quantities (Eqs. 4, 6, PDF pp. 9, 11), not
   fitted weights, and the improvement over single-exchange signals is
   measured on the same unlabeled sample with an in-sample R2 metric and
   no null; two free modelling choices (the summation; the metric) carry
   the headline. Reading discipline: summed-aggregation is a modelling
   choice, not a neutral default; any future multi-venue aggregation
   rule in C8-adjacent work must itself be pre-declared as part of a
   frozen feature definition rather than adopted from the literature,
   and literature R2 figures rank against nothing in this programme
   until they survive a sealed null. No queue change.

5. [reinforcing, no new item] The paper's one honest data-hygiene core:
   venues are aligned on a single collector's local timestamps precisely
   to avoid forward-looking bias (PDF pp. 6-7) — the same failure class
   the L0 gate's timestamp audits exist to catch before any L2
   computation runs. Reinforces the standing gate design on
   arrival-time discipline; nothing new is licensed. No queue change.

6. [cost-survival ammunition] At seconds horizons the 3 bps taker fee
   dominates the entire exercise: TWAP's IS is -3.10 bps on Bybit against
   RL gains of 0.14-0.68 bps (Tables 1, 3, PDF pp. 21, 23), and the
   cross-exchange signals pay a latency-attributed variance penalty
   (PDF pp. 22-23). If a future K7-style cost-survival layer exists, it
   must carry fee assumptions of at least a few bps and latency-derating
   for cross-venue signals, and must never treat a simulated matching
   pass as execution evidence. No queue change now; the assumption
   travels only if that layer ever exists.

7. [reinforcing, no new item] The predictability ladder decays steeply
   from 100ms to 10s (Figs. 2, 5, 7, PDF pp. 9-14), and the agent's gain
   peaks at the 5s prediction interval (Table 4, PDF p. 24): whatever
   this signal family sees, it lives entirely at sub-10s grain. This
   sharpens C1-L2's motivation exactly as the null-time programme framed
   it — the signal, if any, lives where daily scores cannot see — and
   licenses nothing: the magnitudes are ammunition under the laundering
   ban, never evidence. No queue change.

8. [source-quality note] arXiv v1 preprint (stamp 19 Jun 2023) with
   running header "arXiv Template A PREPRINT"; single asset, three
   venues whose data-collection dates are never stated; the fee regime
   is stated as 3 bps for the Bybit results while OKEx's TWAP IS of
   -1.48 bps (Table 2, PDF p. 22) is inconsistent with it and
   unexplained; the matching simulator's fill logic for market orders
   (queue priority, partial fills, depth handling) is undescribed; the
   venue-predictability explanation is offered as speculation; the
   normalization windows are unstated (finding 2). All magnitudes are
   venue-, period- and simulator-indexed, none-of-our-support; the
   laundering ban binds. Check the published version before any formal
   citation.

## What this paper would have killed if we had done it wrong

If the programme had adopted this signal family — summed, rolling-
normalized cross-venue imbalance — as motivation for any C1-L2 feature
without the pre-declaration in finding 2, a compression score whose
normalization window was chosen after seeing the data could have passed
an L2-phase test on lookahead alone, and every later null could have been
argued away by re-choosing the window: the exact post-hoc re-tuning loop
the freeze family exists to close, and the reason the sealed panel freezes
the feature vector at seal time — a signal whose normalization statistics
are not fixed at seal time has no valid seal at all. Equally, had the R2
ladder or the sub-bps gains over TWAP been cited as evidence that
order-flow signals predict anything on the venue the programme will
actually test, a self-benchmarked simulator magnitude would have been
laundered into the record — the failure class the library-is-ammunition
rule forbids, and the reason this note records no empirical claim as
programme support.

## Standing caveat

Everything here is three crypto perpetual venues at one undisclosed
period, with all execution results earned inside the authors' own
matching simulator (market-order-only actions, no queue dynamics, a
synthetic linear price impact, a 3 bps fee) and every predictability
figure an in-sample linear R2 with no null baseline. The rolling-
normalization windows behind the headline signals are unstated, so the
R2 figures cannot be audited for lookahead from the text. The
venue-leadership reading (Fig. 9, PDF p. 15) is a single illustrative
episode, not a systematic lead-lag study. The extract is the arXiv v1
version — check the published version before any formal citation.
Nothing here licenses a measurement, an arming or a kill-line move; it
licenses one harder-to-pass pre-declaration rule, pending the owner's
ratification.
