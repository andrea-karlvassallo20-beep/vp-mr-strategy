# Deep-read session 65 — Çetin & Waelbroeck, "Informed Trading, Limit Order Book and Implementation Shortfall: Equilibrium and Asymptotics"

Null-time session 76 (deep-read 65, offset honored; session number taken fresh
from the log tail at append time — the tail's ## 82 pointer named this paper as
the queue's next UNREAD). Umut Çetin (LSE Statistics) and Henri Waelbroeck
(Baruch College, CUNY and AlgoCortex LLC); arXiv:2003.04425v1 [q-fin.TR],
9 Mar 2020. A static Glosten-equilibrium model of the limit order book with
N profit-maximizing insiders trading through a competitive dealer with random
initial inventory, yielding exact asymptotics for the market impact of large
trades and for the volume tail.

Read 2026-11-20, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xe96c60_informed_trading_limit_order_book_and_implementati.txt,
58 pp., page-marked). Next UNREAD triage-rank entry (score 26).

## The paper in one paragraph

The authors build a one-period Glosten-style model: competitive liquidity
suppliers post the book h, a competitive dealer holds Z ~ N(0, σ2) independent
of the liquidation value V, and N risk-neutral insiders observe V exactly and
route market orders through the dealer, who charges his liquidation cost under
Bertrand competition (Eqs. 2.1-2.3, PDF pp. 6-8); limit prices are Glosten tail
expectations (Eq. 2.4, PDF p. 8). Equilibrium exists if and only if the
integral equation (3.11) has a solution; existence is proven for bounded V
(Theorem 3.2, PDF p. 15) with maximal/minimal solution bounds (Theorem 3.3,
PDF pp. 15-18). F inherits Gaussian scaling (Proposition 3.1, PDF pp. 11-12),
which makes the equilibrium bid-ask spread independent of the noise-trading
variance σ while the book flattens as σ grows (Corollaries 3.2-3.3, PDF pp.
12-13); the same scaling shows the spread widens with the informational
asymmetry (PDF p. 12). With a monopolistic insider the last infinitimal slice
prices at v conditional on V = v (Proposition 2.1(2), PDF p. 9), while N > 1
competitors trade more aggressively, overshoot the last slice, and drive
aggregate profit to 0 as N → ∞ (Propositions 2.1(3), 3.2, PDF pp. 9, 12-13).
The exact large-trade asymptotics are the headline: M − F is regularly varying
of index ρ+ = Ψ+x(M) − 1 / (1 − Ψ+x(M))N, so impact follows a power law if
the signal tail is fat and a (log x)^(1/n) law for lighter tails (Theorems
4.1-4.3, Corollary 4.3, PDF pp. 16-21, 26 Tables 1-2), the equilibrium volume
tail is a power law with exponent ζ+ tied to the signal tail and N (Remark 5,
Eq. 4.25, PDF p. 20), and for unbounded signals the authors conjecture
equilibrium requires N ≥ Ψ+x(∞) — no equilibrium for a monopolist under a
Student-t(3) signal, parabolic impact at N = 2, linear at N = 3, concave at
N ≥ 4 (PDF pp. 25, 28, 32-33; Figure 12, PDF p. 33). Numerically the same
picture holds for log-normal and Gaussian signals with implementation
shortfall fitting a square-root-log form (PDF pp. 27-31, 57-58), and an
alternative "same-price liquidation" desk model behaves similarly but with no
existence proof and an F "not necessarily increasing" (PDF p. 35).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening. Default grade; every
lesson here is a page-cited instance of a discipline the programme already
carries.

1. [reinforcing, no new item] Impact functional form is not a free parameter
   and not universal: within one self-consistent world the large-trade impact
   law is DERIVED from the signal tail plus N — power law iff fat tails, log
   law for lighter tails (PDF pp. 1, 5, 26 Tables 1-2, 38 Theorems 4.1-4.3),
   and the volume tail exponent is equally derived (Remark 5, PDF p. 20).
   This is the standing library-is-ammunition rule sharpened from the other
   side: no impact or volume functional form may be ASSUMED either, without a
   pre-declared tail class; the paper proves the two common practitioner
   forms (sqrt-X and log) are calibrated-similar at small sizes and diverge
   exactly where data is sparse (PDF p. 4), so a fitted functional form near
   the large-trade boundary is an extrapolation, not a reading. No queue
   change.

2. [reinforcing, no new item] The authors' own three practical difficulties —
   spread-impact collinearity for small orders, weak signal-to-noise for
   small executions, and endogenous order-size bias for large trades
   (PDF p. 22) — are the base-rate and multiple-comparisons discipline stated
   by the source literature itself; nothing measured on trade-size-scaling
   features is separable from these three without a pre-declared
   identification rule. Reinforces the queued base-rate confrontation family
   and the estimator-discipline queue; no queue change.

3. [interpretation caution] The impact exponent is manufactured by N, the
   number of informed competitors: Table 1's ρ+ = ((N − 1)/(Nα − 1))^(−1)
   (PDF p. 26) and the worked Student-t(3) case (parabolic N = 2, linear
   N = 3, concave N ≥ 4, PDF pp. 28, 32-33) mean any future magnitude-response
   reading of imbalance or flow carries an unstated competition premise. No
   universal concavity or sign of curvature may be read from this shelf and
   none may be assumed in a spec; magnitudes and shapes stay venue- and
   regime-bound. No queue change.

4. [interpretation caution] The equilibrium bid-ask spread is invariant to
   noise-trading volume σ and moves only with informational asymmetry
   (Corollaries 3.2-3.3, PDF pp. 12-13, 38; the book flattens as σ grows, PDF
   pp. 4, 12): a spread magnitude is never a clean liquidity proxy
   independent of the adverse-selection level. Reading discipline only: any
   spread-based normalizer in a future L2 window travels with the
   informational regime. No queue change.

5. [cost-survival ammunition, relevant only if a future K7-style cost-survival
   layer exists] The implementation shortfall IS(x) sits strictly below the
   marginal cost F on the buy side (Proposition 2.2, PDF p. 9) and converges
   to it as N grows (Corollary 4.3, PDF p. 21); the largest trades dominate
   aggregate shortfall precisely where empirical identification is weakest
   (PDF p. 4). Any future cost layer must carry the collinear-spread,
   weak-SNR and endogenous-size caveats (PDF p. 22) as explicit assumptions
   and may not transplant the paper's log-normal-style √log(1 + ax^δ) fit
   (PDF pp. 27, 30) cross-venue. No queue change.

6. [source-quality note] arXiv v1 preprint (9 Mar 2020); existence proof only
   for bounded signals, the unbounded cases numerical with stated conjectures
   (PDF pp. 5, 25); the same-price liquidation variant has NO existence
   proof and a possibly non-monotone F (PDF p. 35, section 6); second author
   industry-affiliated (AlgoCortex LLC, PDF p. 56); Benford-eligible
   practitioner motivation, single-period, no crypto venue, no calibration to
   a real book. Cite with the arXiv-version caution: check the published
   version before formal citation.

## What this paper would have killed if we had done it wrong

Had the power-law-vs-log dichotomy been read as an empirical claim about
crypto limit order books, a "universal impact law" would have entered the
record as ammunition-evidence while the paper itself proves the exponent is
manufactured by two analyst-chosen premises — the signal-tail class and the
competitor count N (PDF pp. 26, 28, 32-33): the exact academic-degree-of-
freedom failure the queue's pre-declaration family exists to kill at the
gate. Had the equilibrium volume-tail power law been cited as measured market
structure, a theorem deduced from unverified assumptions (competitive book,
one period, risk neutrality) would have been laundered into the C8 record —
the library-is-evidence violation. And had the spread's σ-invariance been
read backwards ("spread is pure adverse selection, safe to normalize on"),
a single-period bounded-signal result would have been transplanted onto a
venue and horizon it never modeled, the class of transplant that the
standing magnitudes-never-transfer rule forbids on every page it matters.

## Standing caveat

Ammunition, not evidence: nothing in this note enters any claim as support.
The model is one-period, static, with a competitive-bid idealization the
authors themselves flag as not always the limit of finite-N Nash equilibria
when adverse selection is low (Biais et al., Back-Baruch, PDF p. 3); all
numerics are the authors' own fits to their own model (no real order book is
calibrated anywhere in the paper); the unbounded-signal results are formally
unproven (existence conjectured to require N ≥ Ψ+x(∞), PDF pp. 25, 38); the
same-price desk variant is a numerical study without a maximum principle
(PDF p. 35). What transfers, cautiously and structurally only: impact and
volume-tail functional forms are consequences of declared tail-and-competition
premises, and the bid-ask spread is an adverse-selection object first and a
liquidity object only second. Any port belongs to a gated spec, never to this
citation. Check the published version before formal citation.
