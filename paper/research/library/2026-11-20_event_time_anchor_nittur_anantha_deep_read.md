# Deep-read session 64 (null-time session 75, log ## 82) — "Event-Time Anchor Selection for Multi-Contract Quoting" (Anantha, Jain, Goyal, Misra, 2025)

Authors: Aditya Nittur Anantha (IISc Bengaluru / SigmaQuant Technologies),
Shashi Jain (IISc Bengaluru), Shivam Goyal (AlgoQuant Technologies),
Dhruv Misra (AlgoQuant Technologies). Full title: "Event-Time Anchor
Selection for Multi-Contract Quoting". arXiv:2507.05749v2 [q-fin.TR], 3
December 2025; per the index a 2025 preprint, zero recorded citations. A
methods/executions paper: in two-leg futures calendar-spread quoting, which
contract to anoint as the reference (anchoring) leg, decided from either
multivariate Hawkes order-flow forecasts or a Composite Liquidity Factor of
instantaneous LOB shape.

Read 2026-11-20, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xd17ea7_event_time_anchor_selection_for_multi_contract_quo.txt,
~29 pp., page-marked). Next UNREAD triage-rank entry (score 26).

## The paper in one paragraph

The quoting design posts a limit order on the quoting leg and fires a
marketable limit order on the reference leg once it fills; slippage is what
the reference price can move during the "critical interval" between the two
executions (PDF pp. 4-6, worked INR example pp. 5-7). The decision problem
is formalized as binary reference-leg choices per 10 ms evaluation window,
scored by agreement with an infeasible hindsight oracle that picks the leg
with the lower realized slippage that window (PDF pp. 7-8, 10, 18). Two
rules are contrasted: a multivariate Hawkes arrival-ratio rule (event types
trades/cancellations/price-downward-modifications per bid/ask side, kernels
fitted by MLE on the past 1000 ms, an SPA test selecting the EM
non-parametric kernel over exponential, sum-of-exponential and
conditional-law variants, forward paths simulated by Ogata thinning over
the next 10 ms, PDF pp. 11-12, 18-19) and a CLF rule (log cross-level price
gap over cumulative depth on the consumed side, EMA-smoothed over 1000 ms,
PDF pp. 14-15, 18). On one day (2022-02-07) of NSE NIFTY futures tick data
(Fig 6.3M and 16.3M tick events, PDF p. 16), the Hawkes rule attains
aggregate agreement 0.6856 and CLF4 0.6358 (Table 8, PDF p. 19); benchmark
regimes are highly persistent (94.1% of windows in runs of 59+ windows,
Fig. 5, PDF p. 17), the Hawkes rule wins in high-persistence regimes
(0.70 vs 0.64), CLF in the low-persistence bins (Fig. 7, PDF pp. 20-21),
and the contract-wise split shows the Hawkes rule agreeing at ~88% when the
oracle picks the current-month leg but only ~18% when it picks the
next-month leg (Fig. 6b, PDF p. 20). The authors' own framing is diagnostic
and illustrative, explicitly not a prescriptive quoting rule (PDF pp. 2,
22).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening. Every relevant lesson in
this paper is a page-cited instance of a rule or caution the queue already
carries; nothing new is earned here.

1. [reinforcing, no new item] The aggregate agreement scores are below the
   constant-class baseline, and the authors' own decomposition shows it. The
   oracle selects the near leg in about 72% of windows (PDF pp. 17-18); the
   Hawkes arrival ratio's headline agreement is 0.6856 and CLF4's is 0.6358
   (Table 8, PDF p. 19) — both below the "always pick the current-month leg"
   constant decision, i.e. the reported rules are aggregate-negative-skill
   in this sample, and the contract-wise panels expose the mechanism (Hawkes
   88.18% agreement on Fc-oracle windows vs 17.76% on Fn-oracle windows,
   PDF p. 20). This is a textbook instance of what the already-queued
   base-rate confrontation (C1-L2, log ## 65) exists to force: a
   classification score is not skill until it is confronted with the
   constant-majority-class decision on the same windows. Page-cited
   general-form backing; nothing added.

2. [reinforcing, no new item] Kernel/model selection for any C8-adjacent
   trigger must survive a multiple-testing-controlled comparison under a
   walk-forward, out-of-sample protocol, decided BEFORE the evaluation data
   is touched. The paper's selection layer is exactly that shape: four
   kernel specifications compared by Hansen's SPA test with the
   data-snooping caveat stated ("higher p-values do not establish
   optimality", PDF p. 19), walk-forward estimation on a trailing window
   with decisions formed only from information strictly before each
   interval (PDF pp. 11-12, 18-19), and the White reality check cited as
   the second leg of the protection (PDF p. 22). Reinforces the
   named-estimator-identity family and the just-queued
   estimator-configuration freeze (the EM kernel was chosen by rule on
   declared candidates, not retuned until the score improved); nothing
   added.

3. [reinforcing, no new item] Intraday non-stationarity of excitation
   structure, inside a single venue-day, on display in the authors' own
   diagnostics: PDM (downward price modification) self-excitation dominates
   the 10:05-10:25 block, trades/cancellations excitation grows by
   midday, and cancellations dominate with PDM faded by the 14:10-14:30
   block (Appendix Figs. 8, PDF pp. 25-26), with the time-of-day dependence
   cited, not denied (PDF p. 19). Page-cited general-form backing for the
   standing regime-window pre-declaration and the seasonality-sensitive
   branching-ratio cautions (the regime a kernel-trigger is estimated and
   fired in must be declared before the data is touched, not inferred from
   which block produced the flattering kernel). No queue change.

4. [interpretation caution] Every number in the paper is scoped to the
   conventions of one day, one venue, one instrument pair: a 10 ms decision
   horizon, 1000 ms estimation window, 10 ms shift step (PDF pp. 18-19), a
   top-5-depth CLF grid at depths 1-4 (PDF pp. 14-16, 18), EMA smoothing
   with tie-breaks toward the next-month leg in the CLF majority vote
   (deterministic tie-break toward c elsewhere, PDF p. 18 — an internal
   inconsistency worth remembering as a grading detail of this paper only),
   and an oracle built only from executed passive-aggressive trade pairs at
   minimum tradable quantity (PDF pp. 9-10). Nothing here licenses any
   magnitude, window length, or feature for the programme's own L2 windows;
   any comparison against the Tardis feed would first reconcile horizon
   (10 ms vs the programme's windows), aggregation and event-type
   conventions. Reading discipline only; no queue change.

5. [cost-survival ammunition, relevant only if a future K7-style
   cost-survival layer exists] The paper's own remark that fees, rebates
   and longer-horizon opportunity costs are "invariant to the
   reference-leg choice" holds ONLY because its setup is a single venue
   with identical contract multipliers; the authors say so and name the
   cross-venue, asymmetric-fee conditions under which it breaks (PDF p. 8).
   Any future cost-survival layer must carry that as an explicit assumption
   and may not import the invariance; single-venue slippage accounting is
   not a cost model. No queue change.

6. [source-quality note] arXiv-only preprint (v2), zero recorded citations,
   three of four authors at industry affiliates (SigmaQuant, AlgoQuant,
   PDF p. 1), methods imported from the first author's own prior work
   (ref. [37], PDF p. 12), and the empirical layer is one day of NIFTY
   futures of one Indian venue, framed by the authors themselves as
   "illustrative" and "diagnostic in scope" (PDF pp. 1, 13, 22). The SPA /
   walk-forward laundering controls are genuinely present, but the
   content is a score-26 access-value read, not an evidence source. Cite
   with the arXiv-version caution; check for a published version before
   any formal citation. Honest grade: grade C+, methodologically cleaner
   than the tier average, empirically thinner (one day, and the headline
   score sits below the constant baseline).

## What this paper would have killed if we had done it wrong

Had the headline agreement scores (0.6856, 0.6358) been read as forecast
skill — the exact instinct a compressed summary rewards — the programme
would have booked a 69%-agreement "capability" into the cross-market or C8
front while the authors' own persistence table shows an inert constant
decision (always anchor the current-month leg) agreeing in ~72% of the
same windows: negative skill laundered as evidence, precisely the failure
the queued base-rate confrontation (## 65) exists to kill before it
reaches any spec. Had the SPA-selected EM kernel been treated as an
objectively correct kernel rather than a selection under controlled
snooping on the same sample's declared candidates, the
estimator-identity laundering would have returned through the
model-selection door, which is exactly why the SPA layer is recorded here
as reinforcing, not new. And had the 10 ms quoting mechanics — reference
legs, marketable limit orders, critical intervals — been read as anything
the programme could operationalize, an execution-strategy artifact would
have entered a research record whose standing rule is that the library is
ammunition, not evidence, and nothing in it trades live.

## Standing caveat

The paper's own boundaries, stated plainly: diagnostic, not prescriptive
(the Remark on PDF p. 2 and the conclusion on PDF p. 22); one day, one
venue, one instrument pair; no transaction-cost asymmetry, no
cross-venue routing, no role-dependent fills (the invariance remark,
PDF p. 8); the CLF's internal tie-break inconsistency between sections
(next-month in the majority-vote construction, PDF p. 18, versus
toward-c determinism elsewhere, PDF p. 18); arXiv-version caution
throughout — check the published version before formal citation; and the
agreement scores must never be quoted without the constant-baseline
context or the persistence decomposition, because every one of the four
aggregate numbers in Table 8 is regime-dependent (Fig. 7, PDF pp. 20-21).
