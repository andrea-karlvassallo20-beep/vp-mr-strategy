# Library deep-read session 14 — Bergault & Cognéville, "Simulating
# and analyzing a sparse order book: an application to intraday
# electricity markets" (arXiv:2410.06839v1, 2024; Dauphine/EDF R&D;
# inhomogeneous-Poisson sparse LOB model on EPEX Spot data)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x3ff3a4_simulating_and_analyzing_a_sparse_order_book_an_ap.txt`,
~20 pp., page-marked). Next UNREAD triage-rank entry (score 37).

## The paper in one paragraph

A sparse limit order book model built for markets where the gaps
between price levels are measured in EUROS, not ticks: the European
intraday electricity market (EPEX Spot, 2021 German/French data),
where limits sit tens to hundreds of ticks apart and there is
typically ONE order per limit (PDF pp. 1-5, 9). Order arrival,
insertion, and cancellation are modeled as marked inhomogeneous
Poisson processes with time-varying intensities: market-order
intensity falls EXPONENTIALLY with the spread (lambda_M(t,S) =
lambda-bar_M * e^{-kappa_M(T-t)} * e^{-beta_M*S}, beta_M = 0.5
per euro, PDF p. 15); all activity intensities grow exponentially
toward delivery maturity (the Samuelson effect, verified in the
data, PDF pp. 3-4); cancellation intensity showed NO significant
state dependence in this venue and was left a pure function of
time (PDF p. 9); consumed or cancelled limits are replaced by
randomly drawn new K-th limits (a boundary condition, PDF pp. 9-10).
Least-squares calibration and simulations reproduce the book's
shape and spread behavior near maturity (PDF pp. 15-17).

## Findings, graded (does any kill line move?)

**NO kill line changes. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four feature pre-conditions
stand. The paper's contribution to THIS program is a boundary
statement — where the already-armed machinery does and does not
transfer:

1. **[reinforcing, no new item] The queue machinery is
   book-SHAPE-specific, and the venue freeze has independent
   citation.** C5's feature pre-conditions (front-vs-rear cancel
   separation, queue-conditioned intensities) presuppose a DENSE
   book: many orders sharing a price level, queue priority worth
   defending. In a sparse book there is ONE order per limit — the
   authors state there is "no particular reason" to stack at an
   existing price when you can place a tick closer (PDF p. 9), and
   their cancellation intensity showed no significant state
   dependence (PDF p. 9), the OPPOSITE of the saturated
   queue-conditioning of the dense-book line (Huang-Lehalle-
   Rosenbaum Fig. 2, session 4's concave-then-saturating cancel
   intensity). Nothing in the program is weakened by this — the
   program's L2 phase is BTCUSDT perps, a dense book, and the
   roadmap already fixes venue/asset expansion as a NEW
   pre-registered family (roadmap Q3-4 rules 1-3). This read is
   the independent citation that the feature set itself (not just
   the multiplicity budget) fails to transfer across book shapes.

2. **[reinforcing, no new item] The maturity clock is a confound
   the program's venue does not have.** In hourly electricity
   products, ALL activity intensities grow exponentially as
   delivery approaches (PDF pp. 3-4) — any "priming/compression"
   reading on a finite-maturity contract is entangled with
   time-to-maturity, and a reader cannot separate them without
   modeling the maturity drift. BTCUSDT perps have no maturity;
   this confound is structurally absent from the program's L2
   phase — and this is one more reason the roadmap's
   "expansion is a new family with its own spec" rule exists
   BEFORE any futures/term-structure expansion is ever priced.
   Recorded as interpretation language for whenever that decision
   comes up.

3. **[interpretation language] Spread-gated aggression.** Their
   market-order intensity falls exponentially with the spread
   (PDF p. 15) — takers pay for width, session 15's
   cost-gated-waiting logic observed in a second venue family
   and a second mechanism (arrival gating rather than horizon
   choice). Goes to the interpretation table only.

## What this paper would have killed if we had done it wrong

If the queue-reactive null and C5's front-vs-rear separation had
been assumed VENUE-PORTABLE — carried to a sparse venue and read
as a failed mechanism there — this paper is the counterexample:
in a one-order-per-limit book the mechanism those features encode
(queue position, priority value) does not exist to be measured.
The failure would have been the spec's, not the market's. The
program's discipline (BTCUSDT-only, all expansion is a new
pre-registered family) was already correct before this read; the
citation closes the gap between the rule and its warrant.
Grade: **no kill line changed; no candidate sharpening; three
reinforcing/interpretation notes; the ratification queue stands
at FOURTEEN candidates, zero armed.**

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The model is deliberately simplified (full cancels only,
independent marks, no state-dependent cancel intensity — the
authors' own parsimony choices, PDF p. 9), the venue is a
regulated hourly-delivery commodity market with cross-border
coupling quirks (XBID decoupling one hour pre-delivery, excluded,
PDF pp. 3, 15-16), and the calibration is least-squares eyeballed
against marginal statistics, not a likelihood fit with CIs. The
sparse-book claims transfer as STRUCTURE (one order per limit,
no stacking incentive) and should never be cited as magnitudes
for any venue. arXiv v1 (Oct 2024); check for a published
version before formal citation.
