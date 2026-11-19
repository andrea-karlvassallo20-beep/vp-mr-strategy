# Deep-read: Self-exciting price impact via negative resilience (Ackermann, Kruse, Urusov)

Null-time session 63 (log ## 67), deep-read session 53. Julia Ackermann,
Thomas Kruse, Mikhail Urusov, "Self-exciting price impact via negative
resilience in stochastic order books," arXiv:2112.03789v2 (2021 v1; v2
dated 22 Jul 2022, per PDF p. 1). A stochastic-control theory paper
extending the Obizhaeva-Wang transient-impact execution framework to
stochastic market depth AND stochastic resilience where the resilience
is allowed to go NEGATIVE, showing that negative resilience is the exact
switch that makes self-exciting price impact optimal to exploit
(overshooting the liquidation target, closing early, re-entering).

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x77c554_self_exciting_price_impact_via_negative_resilience.txt,
~27 pp., page-marked). Next UNREAD triage-rank entry (score 28).

## The paper in one paragraph

The paper sets up an Obizhaeva-Wang-type block-book execution model
where the price-impact process gamma follows a general SDE (PDF p. 6,
eq. (3)) and the deviation process D driven by a resilience process rho
may REPEL zero instead of reverting to it when rho < 0 (PDF p. 7,
eq. (4) with the sign discussion); the optimal execution problem
(minimizing expected costs over cadlag semimartingale strategies
including block trades and both-direction trading, PDF pp. 6-8,
eqs. (5)-(6)) is solved via a quadratic "characteristic BSDE" whose
existence in the new subsetting (rho, mu, sigma independent of the
Brownian driver) is Theorem 2.1 (PDF pp. 9-11), with the optimal
strategy given as X*_t = (x - d/gamma_0)(1-beta_t)E(Q)_t (Theorem 2.2,
PDF pp. 10-12, eqs. (9)-(13)). The core qualitative results:
Proposition 3.3 — under uniformly positive resilience (rho >= delta >
0) neither "overjumping zero" (the optimal program flipping sign past
the target) nor "premature closure" is ever optimal (PDF pp. 13-15);
Proposition 3.4 — negative resilience persisting in every Lebesgue
neighbourhood of the terminal time T necessitates overjumping zero or
premature closure (PDF pp. 15-17, with the interpretation in
Discussion 3.5). Case studies: with piecewise-constant regimes, a
negative-resilience interval with rho^(2) = -0.05 produces NEITHER
effect (Example 4.2, PDF pp. 19-20); rho^(2) = -0.09/-0.07 produces
both, with the beta-exceedance set strictly INSIDE the negative
resilience interval (Example 4.3 and its stochastic twin, PDF pp. 19-22,
Figures 1-2); and a constructed smooth rho yields an optimal strategy
that closes the position over a whole interval [T1, T2] and reopens
afterward (Section 4.3, PDF pp. 21-23, Figure 3). The authors state
that resilience is difficult to estimate from real data and that they
are "not aware of any empirical study of whether the resilience can be
negative" (PDF p. 3).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING
OWNER RATIFICATION.

1. [reinforcing, no new item] The paper's central structural fact is
   that the SIGN of resilience is a regime switch, not a parameter
   tweak: with rho >= delta > 0 uniformly, sign-flips of the optimal
   program are impossible (Proposition 3.3(iii), PDF pp. 13-15); the
   qualitative effect exists only on the negative side of the sign
   boundary (Proposition 3.4, PDF pp. 15-17). This is the same
   sign-regime discipline the T1 sign-inversion lesson and kill line 6
   (the sign guard) encode: a mechanism family whose qualitative
   behavior flips across a sign boundary must have its sign
   pre-declared or its estimate refused. C1-L2's covariate family
   measures one-sided pressure accumulation; this paper's Proposition
   3.3 is the control-theoretic statement that under reverting
   (positive-resilience) regimes, exploitation-to-overshoot of such
   pressure is suboptimal — i.e., an observed overshoot signature in
   the L2 data would be evidence AGAINST a purely reverting regime.
   Reinforcement of the armed sign guard; nothing added.

2. [candidate sharpening, PENDING OWNER RATIFICATION] The
   regime-window pre-declaration rule: Examples 4.2-4.4, with the SAME
   structure and only the magnitude of the negative-resilience interval
   changed, show that a negative-resilience window either produces no
   qualitative effect at all (rho^(2) = -0.05, both deterministic and
   stochastic, PDF pp. 19-21, Figures 1-2 top rows) or both effects at
   once (rho^(2) = -0.09/-0.07, PDF pp. 19-22, middle rows), and
   Proposition 3.4 shows the location of the window — specifically its
   persistence in every neighbourhood of the terminal horizon T — is a
   SUFFICIENT condition (PDF pp. 15-17, Discussion 3.5(a)-(c)), while
   Example 4.2 shows the same-negativity window far from T produces
   nothing. The regime-identification window (where the self-exciting
   regime is declared to start and end) and its distance to the
   barrier horizon are therefore researcher degrees of freedom fully
   capable of manufacturing a qualitative "self-exciting regime"
   finding post hoc: a future report could freeze constants that
   happen to place its mined negative-resilience-looking window at the
   absorbing distance from the barrier. The proposed amendment, in the
   pre-registration-discipline family (same family as the sign
   kill-line template rule and the C1-L2 base-rate confrontation):
   before the L0 gate, any C1-L2 or C8 adjacent spec that proposes to
   identify a self-excitation / negative-resilience regime in the book
   data must carry a pre-declared regime-window rule (how regime
   boundaries are computed from frozen constants, with no post-data
   boundary adjustment) and a pre-declared proximity treatment (the
   distance from any candidate window to the wall-clock barrier
   horizon, stated before the data, with the
   killed-if-wrong-counterfactual recorded: an effect claim whose
   window rule or horizon proximity was chosen after seeing the data is
   the Example-4.2 laundering shape — a manufactured
   near-horizon-window find). It tightens rule 1 of the
   pre-registration discipline the same way the base-rate confrontation
   does: by forcing the spec to deny its future author a free window.
   HARDER TO PASS only: a future positive must survive a window rule it
   did not choose after the fact. PENDING OWNER RATIFICATION; nothing
   is armed and the C1-L2/C8 specs are untouched by this session.

3. [interpretation caution] The beta-exceedance set is strictly
   contained in the negative-resilience set (Example 4.3: "[t: beta_t >
   1] is strictly included in the set where rho_t < 0," PDF p. 20; the
   containment is an identity in Example 4.4 and its stochastic
   analogue, PDF pp. 20-22). Reading rule for future L2 features:
   absence of the downstream self-excitation signature (the overshoot,
   the sign-flip) does NOT license the conclusion "resilience was
   positive" — genuinely negative-resilience time can pass without
   producing the signature (Example 4.2). A future
   regime-classification feature may under-report the negative
   regime; the null result direction is the safe direction to err in
   and the one the burden of proof already demands.

4. [reinforcing, no new item] The authors candidly state that
   resilience "is difficult to estimate from real data" and that no
   empirical study establishes whether resilience can be negative at
   all (PDF p. 3, citing Section 7.3 of Roch). Reinforces, by a second
   source, the estimator-discipline family: a resilience-style
   parameter whose sign is the load-bearing quantity and whose
   empirical identifiability is contested by its own theorists must
   never be estimated post hoc into a claim. The library invariant
   binds doubly here: this paper is ammunition for window-identification
   discipline, never evidence that negative resilience exists in any
   market. Also bound by the standing invariants: the entire
   execution-strategy content (block trades, overjumping zero,
   premature closure, reopen constructions in Section 4.3) is optimal
   execution engineering and is never operationalized — nothing trades
   live.

5. [source-quality note] Zero citations recorded in our index; a
   focused mathematical paper squarely in the Ackermann-Kruse-Urusov
   execution line (its companions [1], [2] of the bibliography, PDF
   pp. 24-25). The published version should be checked before any
   formal citation elsewhere (arXiv v2; the acknowledgement thanks two
   anonymous referees, PDF p. 24, suggesting a refereed version
   may exist).

## What this paper would have killed if we had done it wrong

The window-mining death: a future L2 result declaring a "self-exciting
regime" after having chosen, with data in hand, which negative-looking
window to designate and how close to the barrier it sits — the exact
shape Example 4.2 legitimates within the model (a real
negative-resilience window with zero qualitative consequence) and
Proposition 3.4 makes available as a manufactured find (place the window
at the horizon and the effect appears). Without the queued
window-pre-declaration, the programme's most expensive data phase could
have sold a manipulated-selection artifact as regime discovery. Also
killed in advance: the sign-symmetry assumption — reading this paper as
"impact dynamics are impact dynamics" and letting a future
resilience-signed estimator drift across zero unchecked, which
Proposition 3.3 shows changes the qualitative behavior class
altogether.

## Standing caveat

The model takes the resilience process as exogenously given (the
authors contrast their exogenous self-excitation with the more
endogenous Nash-equilibrium version of Fu-Horst-Xia, PDF p. 3); its
negative-resilience phenomena are proven inside the block-shaped-book
idealization with the structural convexity assumption 2* rho + mu -
sigma^2 >= epsilon > 0 (PDF p. 6, eq. (1)) — i.e., NEGATIVE resilience
only enters the solvable region in combination with compensating
positive mu, so the theory itself never admits an arbitrarily
sign-hostile book. No empirical content exists in the paper at all: no
data, no fit, no calibration; the authors say so themselves (PDF p. 3).
Its applicability to any real market — including whether crypto L2
books exhibit sign-portable resilience at all — is entirely untested.
arXiv v2 caveat: check the published version before formal citation
outside this note.
