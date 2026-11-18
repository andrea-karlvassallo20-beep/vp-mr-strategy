# Deep-read session 26 — Ouazzani Chahdi, Rosenbaum and Szymanski, "Passive Market Impact: A Point Process Approach"

Library deep-read session 26 (null-time session 30, log entry ## 34).
Youssef Ouazzani Chahdi (MICS, CentraleSupélec), Mathieu Rosenbaum
(CMAP, École Polytechnique; Deep Finance and Statistics chair),
Grégoire Szymanski (DMATH, Université du Luxembourg), arXiv:2412.07461v2
[q-fin.MF], v2 stamped 4 Jul 2026 with July 7 2026 on the title page,
39 pp. text extract, page-marked. Read 2026-11-18, against ONE
question: what here would kill C1-L2 or C8 faster, or change their
kill lines? Source: legally acquired OA copy
(docs/library/text/x43a538_passive_market_impact_a_point_process_approach.txt).
Assigned triage-rank entry (score 33, x43a538). Next UNREAD
triage-rank entry (score 33, x28ad86, "Optimal Execution with Passive
Market Impact").

## The paper in one paragraph

A Queue-Reactive-style limit order book where limit and cancel
arrivals depend on the aggregated volume at the touched side, market
orders arrive as a Hawkes process, and each trade carries an
information content kappa(q) that depends on the volume available
there — the "price resistance coefficient", decreasing in available
volume. The price is defined as the conditional expectation of future
volume-weighted trade flow under this kernel (PDF p. 6, eq. (7));
scaling limits are derived for the book and the price (Theorem 2.6),
and closed-form approximations are given for the impact of passive
metaorders (PDF pp. 4-5, eqs. (4)-(5); PDF pp. 14-19). The central
exhibit is a sign paradox (PDF p. 3): a standard propagator model with
constant information content per trade predicts the wrong sign for
the impact of a passive metaorder — a buy executed passively would
push the price down — and the error is repaired only by letting the
information content depend on the book state. Calibration
methodology is proposed (PDF pp. 19-21) but no dataset, fit, or
empirical confrontation appears in this version; Figures 1-2 are
simulations of the model itself.

## Findings, graded

NO kill line changed. ONE new candidate sharpening queued, PENDING
OWNER RATIFICATION.

1. **[candidate sharpening, PENDING OWNER RATIFICATION]** The
   queue-state conditioning disclosure rule for passive-flow features
   in the C1-L2 L2 arm, extending the pending sign-kill-line template
   rule (DECISIONS_PENDING §2). Mechanism, page-cited: with constant
   information content per trade, the classical propagator gives the
   opposite sign for the impact of a passive metaorder (PDF p. 3);
   with kappa(q) decreasing in the available volume at the touched
   side, the sign is correct, and near the stationary state the
   impact of a unit passive order is proportional to
   c_kappa / (c_lambda · mu/(1 - ||phi||_L1)) (PDF p. 4, eq. (4)) —
   i.e. passive-impact size inherits the book's mean-reversion
   strength and the Hawkes stationary intensity. A passive-flow
   feature aggregated without its pre-event queue state is therefore
   definitionally ambiguous in sign under a mechanism that provably
   flips sign when the state dependence is dropped. Pre-declaration:
   any passive-execution or passive-cancel feature pre-registered in
   the C1-L2 L2 arm (or any future pre-registration under the sign
   template) must declare its queue-state conditioning functional —
   the pre-event volume at the touched level, or the declared
   alternative — and passive aggregates whose sign is state-blind
   are inadmissible. Harder to pass: a state-blind passive count
   could correlate with price either way and pass a naive
   association check while the underlying mechanism makes its sign
   unpredictable, exactly the failure the rule forecloses. Scope: the
   sign-kill-line template as it applies to passive features in the
   C1-L2 L2 arm and future pre-registrations; no C1-L2 or C8 spec
   text moves, no kill line moves, T-H and T-O untouched; nothing is
   armed.

2. **[reinforcing, no new item]** The sign paradox is a worked
   exhibit for the standing sign-guard discipline (the T1 lesson,
   log entry ## 5): a mechanically plausible model — a Hawkes
   propagator with constant information content — yields a clean,
   confident, wrong-signed answer for passive flow (PDF p. 3). The
   error is not noise or estimation; it is a specification error
   invisible to any within-model check. This is precisely the class
   of failure the pre-registered sign guard exists to catch, now
   with a concrete page-cited instance from the library. No number
   or formula transfers.

3. **[reinforcing, no new item]** Taker prints cannot recover
   passive impact. The model's price is built from trades weighted
   by the state of the book at the touched side (PDF p. 6, eq. (7);
   PDF pp. 20-21, eq. (15)), and the authors' own remark notes that
   a constant-kappa trade model "only accounts for active trading
   using market orders" and must be extended to see passive effects
   at all (PDF pp. 19-20). Mechanism-level corroboration of the
   standing constraint that aggTrades is taker prints only, that no
   taker proxy may be substituted for passive flow, and of C1-L2's
   premise that full-depth L2 carries what taker prints cannot see.
   Theory corroboration, never evidence; no calibration transfers.

4. **[interpretation caution]** On shape and relaxation: passive
   metaorder impact vanishes identically when kappa is constant
   (PDF pp. 14-15, consistent with the authors' citations [17, 42]);
   under V-shaped liquidity (thin at the touch, linear away) the
   impact grows as sqrt(c·gamma), and a simulated fit lands at
   exponent 0.54 (PDF pp. 14-15, Figure 1) — the square-root law
   line of the record, now for passive flow, and consistent with the
   standing square-root exhibits. But the no-relaxation result —
   impact stops at the metaorder's end with no subsequent decay
   because queues revert to their stationary state immediately in the
   scaling limit (PDF pp. 18-19) — is a consequence of the assumed
   queue mean-reversion, not an empirical claim; the market- and
   limit-order components are separable only under the declared
   approximation that market-order volumes are negligible against
   limit and cancel volumes (PDF p. 18). Read as shape intuition;
   the dissipation claim is never read backwards as an expected
   BTCUSDT property, and no exponent, constant, or curve
   enters any spec.

5. **[source-quality note]** Three authors, affiliations as in the
   header; the arXiv v2 stamp (4 Jul 2026) carries the July 7 2026
   date line. Pure theory paper: the calibration sections propose
   estimators — constant kappa from realised variance with the
   Hawkes-derived xi(0) (PDF pp. 19-20), state dependence from a
   kappa-squared linear-in-q regression on pre-trade queue volumes
   (PDF pp. 20-21) — with the authors' own disclaimer that
   non-parametric estimation is out of scope, and no dataset, fit,
   or empirical confrontation appears; Figures 1-2 are simulations
   of the model itself. Zero indexed citations found. The published
   version is to be checked before any formal citation; kept at
   triage score 33. The extract is mathematically degraded (symbols
   lost in formula regions), so equation numbering follows the
   prose anchors, and all page cites were made against the marked
   pages, but no symbol-by-symbol verification of Theorem 2.6 was
   possible.

## Killed if wrong

If the sign paradox or the state-dependent kappa mechanism is later
shown wrong — for instance if constant-kappa propagators were in
fact found to match passive metaorder impact empirically — the
queued queue-state conditioning rule would lose its mechanism and
should die back: it would impose an unnecessary constraint on
passive features without a failure mode to foreclose. Conversely,
if state-unconditioned passive aggregates are ever allowed into a
C1-L2 pre-registration without disclosure, the route this rule
closes is exactly the one where a wrong-signed feature correlates
with price for state reasons rather than information reasons, and
the sign guard inherits the ambiguity.

## Standing caveat

Pure-theory paper: no market, no sample, no period, no costs.
Transferable content is mechanism only — the sign flip under
state-blindness and the sign of passive impact under state
dependence. Laundering directions named. INTO: the sign-flip
mechanism and the queue-state dependence enter only as
feature-design discipline (the rule above); no constant, exponent,
scaling-limit object, kappa functional, or stationary-state formula
from this paper enters any spec, default, or calibration, and the
model is not adopted anywhere without its own pre-registration.
OUT: the no-relaxation result, the 0.54 exponent, and the
closed-form approximations are never cited as evidence about any
real market, never as expected impact shapes for BTCUSDT, and the
calibration methodology of section 4 is never imported as a
validated estimation procedure.
