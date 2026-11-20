# Deep-read session 57 — Bacry, Muzy, "Hawkes model for price and trades high-frequency dynamics"

- Authors: Emmanuel Bacry (CMAP, École Polytechnique), Jean-François Muzy (SPE, Université de Corse)
- Full title: "Hawkes model for price and trades high-frequency dynamics"
- Venue: arXiv:1301.1135v1 [q-fin.TR], arXiv stamp 7 Jan 2013 (the acquired extract's
  title page carries the date line "November 27, 2024" — see the source-quality note
  below)
- What it is: the founding 4-dimensional Hawkes model coupling anonymous
  market-order arrivals (ask/bid side) with mid-price jumps (up/down) through four
  2×2 kernel blocks (trade self-excitation, trade-to-price impact, price
  self-influence, price-to-trade feedback), with a stability condition, closed-form
  covariances, a labeled-agent market-impact decomposition, a non-parametric
  (Fredholm) kernel estimator, and an application to EuroStoxx and Euro-Bund futures
  tick data.

Read 2026-11-20, against ONE question: what here would kill C1-L2 or C8 faster, or
change their kill lines? Source: legally acquired OA copy
(docs/library/text/x2df250_hawkes_model_for_price_and_trades_high_frequency_d.txt,
~41 pp., page-marked). Next UNREAD triage-rank entry (score 27).

## The paper in one paragraph

The paper embeds price and trades in one stationary multivariate Hawkes process
λt = M + Φ ⋆ dPt with bi-symmetric kernel blocks, so that all four causal channels
(trade clustering, impact, price mean reversion, feedback) live in one norm-bounded
system whose stability is exactly an eigenvalue condition on Φ̂0 (Prop 1, PDF pp.
8-9), equivalent to c+ < (1−a+)(1−b+) with a+, b+ < 1 and implying hard coupling
bounds between the kernel-imbalance norms (eq. 14, PDF p. 9). Price and trade
auto-covariances have closed forms (Props 3-4, PDF pp. 13-14), a labeled-agent
extension yields an analytic market-impact profile (Prop 5, eq. 42, PDF pp. 17-18)
that recovers the concave-then-relaxation meta-order shape from anonymous
order-flow once the kernels are estimated (Cor 1, eqs. 52-53, PDF p. 18; Sec 7.4,
PDF pp. 31-32), and a Fredholm inversion of the conditional-expectation matrix g
estimates all kernels non-parametrically with ~Ne^{-1/2} error (Sec 6, PDF pp.
21-23). On futures data, the trade self-excitation imbalance is a power-law with
norm ~0.9 (near stability saturation), price is mean-reverting (Δφ̂N0 < 0), impact
is impulsive at millisecond scale, and a U-shaped intraday modulation is carried
entirely by the exogenous rate µt while the kernel shapes stay stable across the
day (Sec 7, PDF pp. 23-26). Near-saturation Δφ̂T0 ≃ 1 plus a small cutoff c is then
shown to manufacture trade-sign autocorrelation resembling long-range dependence
over roughly three decades out of a strictly short-range process (Sec 7.3, PDF pp.
26-29), while price efficiency emerges without fine tuning of any parameter (PDF
pp. 30-31).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening. Every mechanism this paper
carries lands on an item already armed in the queue's two reinforcement families;
the near-instability artifact, the calendar separation, and the
response-versus-impact distinction are all pre-empted by standing and already-queued
discipline. That this paper, the founding document of the whole 4-kernel literature,
adds nothing beyond what the queue already holds is itself honest evidence the
standing rules already cover this cluster.

1. [reinforcing, no new item] The apparent-long-memory artifact: with power-law
   kernels ΔφT,t = α(c+t)^{−β}, β ≈ 1.2, cutoff c ≤ 10−2 s, and near-saturated
   norm Δφ̂T0 ≃ 0.9, the model's trade-sign autocorrelation decays as τ^{2ν−1}
   (≈ τ^{−0.6}) over about three decades while remaining strictly integrable —
   the inequality (64) needs ~c^{-1}·10^{-5} scales to break (Sec 7.3, eqs. 62-66,
   PDF pp. 28-29) — so decades of slow decay in flow signs are exactly what a
   stable, short-range, near-unstable Hawkes process produces without any genuine
   long memory. This is second-source reinforcement of the already-queued
   near-instability / apparent-criticality estimator-discipline items: any C1-L2 or
   C8-adjacent claim that leans on persistent flow-sign autocorrelation as a
   "fixed characteristic" must first fail a strictly stable near-saturated Hawkes
   null. No queue change.

2. [reinforcing, no new item] Deterministic intraday seasonality is fully
   separated from the excitation structure: the kernel shapes are stable across
   2-hour slices while the U-shape lives entirely in the exogenous µt (Sec 7.2,
   Fig 11, PDF pp. 25-26; Prop 2's mean-intensity decomposition, PDF pp. 8-10).
   Day-varying activity mass is calendar, not endogenous. Reinforces the
   already-queued deterministic-clock null arm and the standing calendar-laundering
   caution; no queue change.

3. [interpretation caution] The response function is not the market-impact
   function: R_t = E(price move | a trade) is polluted by the impact of all other
   orders in the same meta-order, and only the model-decomposed impact (eq. 42
   through Δξ) isolates one agent's contribution (Sec 5.3, PDF pp. 20-21). Any
   "predictiveness" read off a C1-L2 flow feature whose construction is
   response-shaped measures a herding-plus-impact mixture, not bare anticipation.
   On the same footing, trade-to-price causality inside the millisecond resolution
   is an assignment convention, not an observation (impulsive φI,s, Sec 2.1.3, PDF
   pp. 6-7; confirmed mostly impulsive on data, Sec 7.1, PDF p. 25) — precisely
   the convention class the queued spread-convention declaration rule (the
   thirty-fourth, session 56) makes declarable and countable. Reading discipline
   only; no queue change.

4. [cost-survival ammunition] Closed-form meta-order impact from anonymous data:
   MI_t ∼ t^{1−ν} during and t^{−ν} after execution with ν ≈ 0.2 (not a strict
   square root; Sec 7.4, eq. 68, PDF pp. 31-32), plus the permanent-impact formula
   (eq. 56, PDF p. 19) and the three routes (microstructure reversion, cross-side
   feedback, trade-sign autocorrelation at norm ⇒ 1) that shrink it (Sec 5.2, PDF
   pp. 19-20). Declares the assumptions a future K7-style cost layer must carry
   (kernel invocation, exogenous decomposition, labeled-agent determinism);
   ammunition only.

5. [source-quality note] arXiv v1 of a 2013 posting with an anomalous "November
   27, 2024" title-page date line in the acquired extract; volumes are deliberately
   dropped (point events only, Sec 2.1 and fn. 3, PDF pp. 3-4; volume extension
   deferred to "a forthcoming work", Sec 8, PDF pp. 32-33); the empirical claims
   rest on two futures contracts from one vendor (QuantHouse, PDF pp. 23-24) and
   2-hour stationarity slices; the non-parametric estimator's statistical study is
   likewise deferred (Sec 6, PDF p. 23; the Kirchner parallel work, PDF p. 21,
   fn. 5). The published version should be checked before any formal citation
   outside this note.

## What this paper would have killed if we had done it wrong

The near-unstable-long-memory laundering death: observing three decades of slowly
decaying trade-sign autocorrelation in the L2 data, naming it long-range
dependence, and booking a persistence or compression claim on that "fixed
characteristic" — when this paper proves, with exact inequalities (eqs. 62-66, PDF
pp. 28-29), that a strictly stable power-law Hawkes process with a near-saturated
trade kernel manufactures precisely that signature on every lag scale the data can
resolve. Pre-empted by the near-instability estimator-discipline family already in
the queue (apparent-criticality calibration, the branch-norm reporting duties) and
by the frozen-constant regime-window pre-declaration. Alongside it, the calendar
death: attributing the intraday activity modulation to endogenous self-excitation —
pre-empted by the deterministic-clock null arm, exactly as in session 56. Neither
survival licenses any claim about C1-L2 or C8; their kill lines are unchanged.

## Standing caveat

All results live inside a 4-dimensional bi-symmetric Hawkes representation of
anonymous, unmarked (volume-free) market orders and mid-price direction jumps on a
discrete tick grid, with a millisecond-resolution simultaneity convention, an
exact-stationarity assumption per intraday slice, and kernels estimated by a
Fredholm/Nyström inversion whose statistical study sits outside the paper (Sec 6,
PDF pp. 21-23). The empirical application covers two futures contracts over
2009-2012 from a single data vendor (PDF pp. 23-26). This is an arXiv v1 with a
date-line anomaly on the acquired copy; the published version should be checked
before any formal citation outside this note. Nothing here is programme evidence;
under the library invariant it is ammunition, not support.
