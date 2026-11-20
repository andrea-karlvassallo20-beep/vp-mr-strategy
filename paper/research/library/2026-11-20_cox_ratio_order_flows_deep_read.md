# Deep-read session 60 (null-time session 71, log ## 77) — the Muni Toke-Yoshida Cox-ratio paper; the sign-persistence admission null

**RECONSTRUCTION NOTE (2026-11-20, null-time session 72, log ## 78):** the
session-71 landing of this note reached the branch corrupted (a single
0x07 control byte). This file is re-earned from the page-marked shelf
extract by the repairing session; every page cite below was re-verified
against `docs/library/text/x0b879c_analyzing_order_flows_in_limit_order_books_with_ra.txt`
in this session; the grading verdict and the queued sharpening text are
those recorded by the original session in the restored log entry ## 77,
which governs. The append-only log carries the honest-error record; this
header is the only newly-authored portion.

Ioane Muni Toke (CentreSupélec, Université Paris-Saclay) and Nakahiro
Yoshida (University of Tokyo), "Analyzing order flows in limit order
books with ratios of Cox-type intensities" (arXiv:1805.06682v3
[q-fin.ST], 22 Aug 2019 stamp). Ratios of Cox-type intensities sharing an
unspecified common baseline λ0, estimated by a quasi-likelihood from
which λ0 cancels exactly (Eq. 1 and rationale, PDF pp. 3-4); consistency
and asymptotic normality (Thms. 3.1-3.2, PDF pp. 6, 10); QCAIC/QBIC and
penalized QMLE selection machinery (Prop. 4.1, PDF pp. 10-11); 36 Paris
Stock Exchange stocks 2015, >1 billion reconstructed events (PDF p. 12);
next-trade-sign, spread and queue-size equilibrium studies (PDF
pp. 13-23); and an out-of-sample sign-prediction comparison against
Hawkes models (PDF pp. 24-27).

Read 2026-11-20, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x0b879c_analyzing_order_flows_in_limit_order_books_with_ra.txt,
~38 pp., page-marked). Next UNREAD triage-rank entry (score 27 in the raw
file; the ## 74 pointer had recorded 26 — raw file governs).

## The paper in one paragraph

A quasi-likelihood framework in which the intensities of several order
flows are proportional to one common (possibly random) baseline λ0 that
the estimation cancels exactly (PDF pp. 3-4): covariates act
multiplicatively on the baseline, so only relative intensities are
identifiable. Consistency and asymptotic normality of the QMLE are
proven (Thms. 3.1-3.2, PDF pp. 6, 10), with QAIC/QCAIC/QBIC model
selection (Prop. 4.1, PDF pp. 10-11). Applied to 36 Paris large caps
(2015, reconstructed flows, PDF p. 12), the framework reads how imbalance,
spread and queue sizes condition relative buy/sell activity (PDF
pp. 13-23) and competes with Hawkes models on next-trade-sign
prediction (PDF pp. 24-27): pooled sign accuracy is dominated by the
mechanical persistence of the last sign — the zero-parameter repeat rule
signs more than 80% of trades (PDF pp. 25-26) — while the state-only
ratio model reaches ~85% pooled but collapses to ~40% on the sign-change
subsample (PDF pp. 26-27).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION — the sign-persistence admission null (the thirty-sixth):
the zero-parameter "next sign repeats the last sign" rule correctly signs
MORE THAN 80% of ~54 million trades across all 36 stocks (PDF
pp. 25-26), and the imbalance-only model is NEVER selected by consistent
criteria among 390 monthly fits (Table 2, PDF pp. 16-17) — so pooled
next-sign accuracy is dominated by mechanical persistence before any
book state enters. Pre-declaration text: any C1-L2/C8 short-horizon sign
or aggressive-flow feature is admitted only if it adds value beyond a
PRE-REGISTERED sign-persistence null (the last-sign repeat, zero
parameters), with the survival shown in the sign-CHANGE subsample — the
paper proves that is where the separation lives (the state-only ratio
model signs ~85% pooled but only ~40% of sign changes, PDF pp. 26-27) —
so a pooled win admits nothing. Harder to pass because the feature must
beat a free null in the exact subsample where its claimed information
lives; tightens the two-null admission rule (deep-read session 11, log
## 17) by joining the Gould-Bonart Eq.-7 comparator and the
tautology-controlled OFI benchmark with a third null that needs no
estimator at all; harder-to-pass only, reading-side only, the owner's
word alone ratifies. [candidate sharpening, PENDING OWNER RATIFICATION]

1. [reinforcing, no new item] Parsimony over cross-excitation for
   prediction: the no-cross Hawkes beats the full cross-excited model,
   75-80% vs 73-78% (PDF p. 26), and QAIC overfits while QCAIC/QBIC
   select smaller structures (PDF pp. 16-18) — same-day-class evidence
   for the per-branch rule (deep-read session 7) and the
   pre-registration family; model form stays declared with the spec.
2. [reinforcing, no new item] Only level-1 imbalance is significant;
   levels 2-10 corrective terms are not (Fig. 5, PDF pp. 18-19) —
   reinforces the distance-grid sign-invariance rule (session 13) and
   the top-of-book comparator's standing.
3. [reinforcing, no new item] Limit-vs-cancel probability crossing at
   the equilibrium queue size recovers the humped book (PDF pp. 20-23)
   — the queue-reactive state-conditioning discipline (library ritual
   paper 4, C5's family) gains another page-cited demonstration that
   unconditioned rates read the queue-size distribution, not the
   mechanism; queue sizes in median-trade-size units (PDF p. 22)
   reinforce the unit pre-declaration sharpening.
4. [interpretation caution] The common-baseline identification axiom:
   ratios cancel λ0, so any flow-type-specific activity sensitivity
   CONFOUNDS the covariate reading; relative-intensity readings must
   pre-declare the common-baseline assumption and carry the confound
   statement beside every estimate (Eq. 1 and rationale, PDF pp. 3-4;
   the paper's own remedy, PDF p. 16).
5. [interpretation caution] Relative is not absolute: this framework
   can never carry an absolute-excitation or criticality reading and
   can never replace or re-tune the branching-ratio trigger layer; the
   two-stage HA/HB covariate pipeline (parameters fixed by the
   independently fitted NoCross Hawkes, PDF pp. 24-25) must be declared
   the same way by any port that reuses fitted parameters inside a
   covariate.
6. [interpretation caution] Bundling immunity does not transfer: the
   ratio likelihood counts events and tolerates tied timestamps (PDF
   p. 13), but that immunity is a property of THIS likelihood — the
   timestamp-bundling trap for the Hawkes MLE (deep-read session 2 and
   the queued clock pre-declaration) stands unchanged for the trigger
   layer.
7. [cost-survival ammunition] The prediction exercise ignores latency,
   delays and reaction times by the authors' own statement (PDF p. 24);
   day-ahead recalibration adds operational cost (PDF p. 25); ~85% sign
   accuracy carries no execution meaning without a latency model —
   relevant only if a K7-style cost layer ever exists.
8. [source-quality note] arXiv v3, published-version line to check
   before formal citation; reconstructed (not raw-feed) order flows via
   the Muni Toke (2016) aggregation (PDF p. 12); one venue class (Paris,
   36 large caps, 2015), no crypto perps; the 390/8052 fits are
   in-sample descriptions with quantile-selected display panels (PDF
   pp. 14-16, 20-21) — identification structure transfers, magnitudes
   never.

## What this paper would have killed if we had done it wrong

Had the programme admitted any short-horizon flow feature on pooled
next-sign accuracy, this paper's own numbers show the pooled statistic
is 80%+ owned by a free dumb null (mechanical sign persistence, PDF
pp. 25-26): a feature beating a Hawkes benchmark by points on the pooled
figure could still carry NO incremental information about sign changes —
exactly the laundering the two-null admission rule (log ## 17) exists to
prevent, now closed on the third side by a null that costs nothing to
run. The pre-registration family gains its hardest free comparator, and
the record gains another worked example (with the Kaj-Caglar
level-versus-memory item, log ## 74) of a headline number that is a
base-rate statement in disguise.

## Standing caveat

Relative-intensity framework: no absolute rates, no criticality, no
branching ratio; identification requires the common-baseline axiom
(equal multiplicative sensitivity of compared flows to global activity,
PDF pp. 3-4), which buy/sell market flows on a single instrument
plausibly satisfy and cross-venue or cross-event-type comparisons may
not. One venue class (Paris equities, 2015), reconstructed flows, and
every quantitative panel in-sample; arXiv v3 — check the published
version before any formal citation.
