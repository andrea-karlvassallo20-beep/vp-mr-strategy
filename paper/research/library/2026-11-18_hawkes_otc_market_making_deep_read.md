# Deep-read session 20 — Barzykin, "Hawkes-Driven OTC Market Making: Volterra–Riccati Approximation"

Library deep-read session 20 (null-time session 23, log entry ## 27).
Alexander Barzykin (HSBC, London; views declared his own, PDF p. 23),
arXiv:2608.02002v2 [q-fin.RM], 25 Aug 2026: an OTC request-for-quote
market-making control problem in which RFQ arrivals follow general Hawkes
kernels, fills are controlled thinnings of the request flow, and the
path-dependent HJB is approximated by a three-level Volterra–Riccati
hierarchy validated against an exact lifted benchmark.

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xa868e3_hawkes_driven_otc_market_making_volterra_riccati_a.txt,
24 pp., page-marked). Next UNREAD triage-rank entry (score 37); also the
burst slot 05 assignment.

## The paper in one paragraph

An OTC dealer quotes RFQs whose arrivals follow Hawkes processes with
general kernels; the exact control problem is path-dependent because the
relevant state is the order-flow history, or equivalently the forward
curve of conditional future RFQ intensities (PDF pp. 7-9). Exponential
kernels admit a Markovian lift but the dimension explodes for mixtures
and long-memory kernels (PDF p. 8), so the author builds a hierarchy of
Volterra–Riccati approximations: a conditional-mean policy, a covariance
correction, and a state-feedback rule that updates the forecast curve with
the realized post-request memory (PDF pp. 9-12). In an exponential-Hawkes
benchmark with an exact lifted HJB, the state-feedback rule tracks the
exact policy closely (relative paired regret 0.08-0.17% across three
regimes), while a memory-free Poisson policy, solved exactly within its
own misspecified model, suffers up to 27.3% regret in the directional
regime (Table 3, PDF p. 16); the mechanism is that the realized Hawkes
memory carries signed-flow information a deterministic forecast cannot
(Fig. 4, PDF p. 17). Applied to a power-law-like memory kernel, a one-sided
RFQ burst converts into a persistent quote skew whose decay inherits the
kernel tail (Eqs. 51-54, PDF pp. 17-18), improving inventory and P&L risk
control (PDF pp. 19-20). The empirical motivation fits seasonality-adjusted
two-way spot-FX RFQ activity (HSBC data, three pairs, three years, >5*10^5
events each) and finds branching ratios 0.86-0.90 with multi-scale kernels
(Table 1, PDF pp. 3-5), while explicitly refusing any structural contagion
reading of the fitted branching representation (PDF pp. 2, 4-5, 21-22).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] **The
   latent-common-cause (Markov-modulated-baseline) robustness arm for the
   branching-ratio trigger.** The paper states the confound precisely:
   correlated requests "may be reactions to a common unobserved cause —
   public market activity, volatility, a client execution programme or
   another latent liquidity factor — rather than consequences of earlier
   RFQs. If such exogenous variation is omitted from the baseline
   intensity, a fitted Hawkes model may absorb part of it into the
   excitation kernel and thereby produce a large branching ratio" (PDF
   p. 2), and the conclusion names the discriminating test: "compare pure
   Hawkes dynamics with latent-factor or Cox specifications, and
   potentially retain Hawkes excitation only for residual event-to-event
   dependence after persistent common drivers have been modelled" (PDF
   pp. 21-22). The paper's own Table 1 makes the stakes concrete: fitted
   branching 0.86-0.90 in major pairs, on three years and >5*10^5 events,
   AFTER deterministic seasonality is designed out — exactly the
   magnitude range a naive reading would celebrate as near-critical
   reflexivity, from an author who explicitly refuses that reading (PDF
   p. 4). This confound is NOT the deterministic-clock confound queued at
   deep-read 19 (an observed calendar profile is not a stochastic latent
   driver), and none of the standing gates (bootstrap-band, kernel-family,
   ACF-shape, wash-audit, clock null, near-critical disclosure)
   addresses it. Pre-declaration text: every window whose fitted
   branching ratio fires the trigger bar must be re-estimated under a
   registered latent-baseline enrichment — the two-state Markov-modulated
   background already built into C8's MMHP structure — with the baseline
   form pre-registered before the first L2 run; if the excitation mass
   attributed to endogenous branching drops below the bar once the latent
   state is modelled, the window contributes no firing (neither positive
   nor negative); both readings (unconditional and latent-adjusted
   branching) are reported in the register and replace any single-number
   narration. Harder to pass: a window that survives every standing gate
   can still die here, because apparent self-excitation absorbed from an
   omitted common driver is not reflexivity. Tightens only the
   branching-ratio trigger family; no C1-L2 text moves.

2. [reinforcing, no new item] Independent practitioner corroboration of
   the deterministic-clock null arm queued at deep-read 19: a working
   FX dealer-model author finds that "estimating a Hawkes kernel
   directly in calendar time would ... confound deterministic
   seasonality with residual serial dependence" and therefore
   transforms to a
   seasonality-adjusted activity clock BEFORE fitting (PDF pp. 3-4), with
   the explicit discipline that all rates entering a control problem must
   be expressed in one declared clock, variance rates included (PDF
   pp. 4-5). The activity-time transformation is an alternative
   implementation of the same lesson; it reinforces the queued clock null
   and the flow-clock scale-constant rule, and changes nothing in either.

3. [reinforcing, no new item] High branching fits are commonplace and
   specification-sensitive: fitted 0.86-0.90 in data (Table 1, PDF p. 4)
   and 0.92 used as a synthetic stress regime (Table 2, PDF p. 14). A
   trigger bar fired in the 0.86-0.92 range is therefore not an
   extraordinary event by itself; this supports the near-critical
   regime-disclosure rule's requirement that fired bars state their
   limit regime rather than trade on the number alone. Nothing added.

4. [interpretation caution] Fitted excitation is event-set-relative.
   The empirical section filters aggressively before fitting (sizes at
   least 0.25 million, clients with at least 1% historical fill ratio,
   roll windows and holiday periods removed, PDF p. 3) and the model
   convention separates information events (requests) from conversion
   events (fills), so "the branching ratio of the flow" is undefined
   until the event stream and its filters are fixed (PDF pp. 4-6). For
   C8: the trigger's event-stream definition and its filters must be
   pre-registered before the first L2 run; changing stream or filters
   afterwards is a new test under the multiple-testing discipline, not
   a re-estimate.

5. [source-quality note] Single-author practitioner paper (HSBC), arXiv v2
   [q-fin.RM], August 2026; no published version found this session.
   Empirics use proprietary HSBC RFQ data, not independently
   reproducible; the control theory states openly that no general
   well-posedness theorem is pursued, validation is numerical only
   (PDF pp. 14-15), and the theory section's no-arbitrage/impact
   citations are motivation, not derivation, for our purposes. The
   market-making results are execution-strategy engineering and are
   outside programme scope (the programme never trades live). Check for a
   published version before formal citation.

## What this paper would have killed if we had done it wrong

Two deaths invited themselves. First, Table 1 would have been imported as
calibration: "major FX pairs sit at branching 0.86-0.90, three years,
half a million events, a bank's own data" is exactly the kind of authority
a trigger specification would have latched onto, pre-loading the C8 bar
with a number whose own author refuses the structural reading. The
no-empirical-claim-from-papers rule bars that import; the paper instead
earns one robustness pre-declaration that makes the trigger harder to
fire. Second, the market-making results would have smuggled execution
strategy into a programme that arms nothing and trades nothing: the
regret tables, quote-skew formulas, and inventory-risk improvements are a
dealer's control problem, never programme input. The counterfactual is
symmetric: had we read only the confound disclaimer and concluded fitted
branching is meaningless, we would have forgotten that the paper's
validation hierarchy shows the fitted memory to be the economically
relevant state — the confound reading limits WHAT a fired bar may claim,
not WHETHER the forecast content exists.

## Standing caveat

The setting is an OTC RFQ market, not an exchange LOB: requests are
predominantly two-way, so directionality is latent and the author flags
signed-flow filtering as an unsolved statistical problem (PDF p. 22);
fills deliberately do not feed back into request intensity (PDF p. 6, a
baseline separation the author relaxes in discussion); win probabilities
are assumed state-independent; the horizon is one day. Nothing in the
paper transfers to an exchange-tape trigger beyond the estimation
discipline: fitted branching conflates excitation with whatever
conditioning information the baseline omits, deterministic or stochastic,
and the discriminating evidence survives only as the paired readings a
registered specification set produces.
