# Deep-read session 48 — Baldacci and Bergault, "Optimal incentives in a limit order book: a SPDE control approach"

Library deep-read note, null-time ritual. Deep-read session 48, logged
under its null-time session number (52) in
`paper/research/null_time_programme.md`. Authors: Bastien Baldacci
(Quantitative Advisory Solutions) and Philippe Bergault (CMAP, École
Polytechnique). Published record: arXiv:2112.00375v2 [math.OC], 14
October 2022 (v1 December 2021); a venue-side mechanism-design paper:
the exchange chooses a make-take-style incentive schedule (a rebate
paid at execution, indexed by the limit order's distance from the
mid-price) to reshape the book, with the Cont-Müller SPDE limit order
book model as the plant and a Feynman-Kac-solvable control problem as
the machinery.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or
C8 faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xc937ca_optimal_incentives_in_a_limit_order_book_a_spde_co.txt,
19 pp., page-marked, read in full). Next UNREAD triage-rank entry
(score 29, xc937ca, the pointer named in the landed ## 55 closing
block), re-verified unread against all 48 library notes on main, with
the live main tail and the branch/PR set re-read before consuming.

## The paper in one paragraph

The authors model the LOB as the Cont-Müller SPDE density of rescaled
bid/ask volume in signed distance x from the mid-price, with diffusion
(replacement), convection (re-pricing toward the mid), proportional
cancellation, a multiplicative HFT noise term, and a controllable
order-submission source term f(x,Z) boosted by the exchange's incentive
process Z (Eqs. 1-3, PDF pp. 3-4); the exchange maximizes cumulative
book volume minus a convex penalty g(x,Z) on the incentives paid
(Eq. 4, PDF pp. 4-5), and the paper's main results are that the
associated BSPDE admits a deterministic adjoint solution reducing to a
linear parabolic PDE with a Feynman-Kac representation (Theorem 1,
Eqs. 7-11, PDF pp. 5-7), that in the long-term stationary limit the
adjoint solves a second-order ODE in closed form (Eqs. 12-15,
PDF p. 7), and that with the exponential-penalty / concave-incentive
family the stationary optimal incentive is closed-form, declining
super-exponentially with limit number (Eq. 16, Table 1, PDF pp. 7-10);
a fully fictitious symmetric parameterization (no market data,
10 limits each side, 30-minute horizon; PDF pp. 8-9) then simulates the
controlled book to show incentives lift first-limit volume (Fig. 2,
PDF p. 10), and a sensitivity section shows the optimal incentives
move by orders of magnitude when the diffusion, convection, or
cancellation parameters are perturbed (Figs. 3-8, Tables 2-4,
PDF pp. 11-15).

## Findings, graded (does any kill line move?)

Verdict: NO kill line changes. NO new candidate sharpening. Default
grade. The paper is venue-side mechanism design — it optimizes the
exchange's fee schedule, not any market participant's anticipation,
and its only measurable object is a simulated fictitious book. Under
the one question it is context, not content: nothing here would kill
C1-L2 or C8 faster and nothing licenses a spec change.

1. [reinforcing, no new item] — arrival intensities and book shape
   are partly policy variables, which the library-is-ammunition and
   OUT-direction rules already fence: the paper's entire premise is
   that a venue can move the order-submission intensity and the
   first-limit volume by paying for them (Eqs. 3-4, PDF pp. 4-5;
   Fig. 2, PDF p. 10; Section 6, PDF p. 16). No empirical figure in
   this paper ever enters the record as expected behavior of any
   venue the programme measures — the rule already standing.

2. [interpretation caution] — first-limit depth is partly fee-induced,
   not purely information-bearing: the closed-form incentives
   concentrate overwhelmingly on the first limits (order 10^-3 dollars
   at limit 1 versus 10^-29 at limit 10, Table 1, PDF p. 9), and the
   simulated with-incentives book moves the first limit from the 5th
   to the 3rd most filled (Fig. 2, PDF p. 10; on real venues the
   standing make-take mechanism is the same lever, PDF pp. 1-2). Any
   future C1-L2 interpretation of first-limit depth, queue-imbalance,
   or book-shape asymmetry must wear the standing caveat that part of
   that depth is manufactured by the venue's fee schedule rather than
   by the flow the programme models; no queue change, a reading
   discipline only.

3. [reinforcing, no new item] — closed-form "optimality" that is a
   hostage to calibration: halving the diffusion parameter multiplies
   the first-limit incentive by roughly 18 (1.90e-3 → 3.51e-2,
   Tables 1-2, PDF pp. 9, 11-12), doubling the cancellation rate
   multiplies it by roughly 9 (→ 1.64e-2, Table 4, PDF p. 15), and the
   incentive schedule inherits the super-exponential e^((a+bar)x)
   geometry of the assumed penalty and intensity forms (Eq. 16,
   PDF p. 8). This is a worked exhibit for the programme's parameter-
   sensitivity discipline: quantities that move by orders of magnitude
   under small model-parameter perturbations are calibration artifacts
   until shown otherwise. The existing sensitivity screens need no
   amendment.

4. [source-quality note] — pure theory on a fictitious book: every
   number is simulated from hand-set parameters with no market data
   anywhere (PDF pp. 8-9); the authors state the incentive-response
   parameters (lambda, kappa) can only be calibrated if the exchange
   already has historical data at different incentive levels,
   "otherwise, some tests and heuristics should be used" (Remark 5,
   PDF p. 9); the Cont-Müller model's own calibration validity is the
   programme's problem, not this paper's. arXiv v2, published version
   not checked at reading (uncertain, flagged for verification). Minor
   copyediting slip: Section 5.3.3 is captioned "Cancellation rate" but
   its comment sentence says "an increase in the convection rate"
   (PDF p. 15) — flagged so no later citation borrows the wrong label.
   Read it, graded plainly, not promoted.

## What this paper would have killed if we had done it wrong

Had the paper's SPDE plant been read as a description of the venue the
programme measures, a fictitious-book simulation with hand-set
parameters and an order-of-magnitude-sensitive "optimum" would have
been laundered into a structural prior on the very book whose
compression signal C1-L2 hunts — precisely the calibration-hostage
failure the parameter-sensitivity discipline exists to prevent. Had the
multiplicative noise term (sigma*u*dW, glossed as high-frequency
submission/cancellation noise, PDF p. 4) been cited as a modelling
warrant that "HFT noise" is a book-level multiplicative shock, a modelling
convenience convenient for solvability would have entered the record as
an empirical claim no data in the paper supports. Had the first-limit
concentration result been read as "first-limit depth is where
incentives live, therefore first-limit depth is informative", the
venue-fee artifact would have been inverted into an information
statement — the exact laundering the OUT-direction rule forbids.
Nothing-measured, library-is-ammunition, and the pre-declared
venue-explicit reading discipline prevented all of it.

## Standing caveat

All quantitative content is a fictitious symmetric limit order book,
hand-set parameters, 10 limits per side, 30-minute horizon, no market
data, no costs, no participants' response modeled beyond the assumed
concave intensity boost, exchange perspective only. Nothing transfers
to any venue the programme measures; nothing enters any spec, default,
kill line, threshold, or generative null. Laundering directions named:
INTO — the fee-engineered-depth reading caveat (as an interpretation
discipline for first-limit book-shape features) and the
calibration-hostage sensitivity exhibit enter as standing-rule
reinforcement only; OUT — no eta, beta, alpha, sigma, or incentive
value, no closed-form Eq. 16, no Table 1-4 figure, no Cont-Müller
parameterization, and no "exchanges can shape the book" sentence is
ever cited as expected behavior of any venue the programme measures,
or as evidence that any programme feature carries information.
Nothing measured, no kill line moved, nothing armed, nothing trades
live.
