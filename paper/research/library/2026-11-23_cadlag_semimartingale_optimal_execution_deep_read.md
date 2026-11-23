# Deep-read session 102 — Ackermann, Kruse & Urusov (2020/2021), "Càdlàg semimartingale strategies for optimal trade execution in stochastic order book models"

Authors: Julia Ackermann (Gießen), Thomas Kruse (Gießen), Mikhail Urusov
(Duisburg-Essen). Venue: arXiv:2006.05863v2 [math.PR], revised 2021-07-26
(PDF p. 1). One clause on what it is: a pure-theory optimal-execution paper
that extends the Alfonsi-Fruth-Schied / Obizhaeva-Wang block-LOB family to
stochastic order-book depth (a stochastic price-impact process γ) and
stochastic resilience (ρ), solves the control problem over càdlàg
semimartingale strategies — infinite variation and two-directional trading
allowed — through a quadratic BSDE, and proves twice in print that the
conventional bookkeeping conventions of the finite-variation literature
become ill-posed (unbounded negative costs) over the wider strategy class.

Read 2026-11-23, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x150a2c_c_dl_g_semimartingale_strategies_for_optimal_trade.txt,
~53 pp., page-marked). Next UNREAD triage-rank entry (score 20, twelfth of
the score-20 tier, verified note-less against the live listing).

## The paper in one paragraph

The paper fixes a horizon [0,T], a continuous local martingale M, and a
price-impact process γ > 0 solving dγ = γ(µ d[M] + σ dM) (eq. 1, PDF p. 2), so
the depth itself is a geometric stochastic process, with a progressively
measurable resilience ρ (PDF p. 6). An execution strategy is any càdlàg
semimartingale X with X_{t-} = x and X_T = 0 (jumps = block trades, both
trade directions allowed), the associated price deviation D solves
dD = −ρD d[M] + γ dX + d[γ,X] (eq. 2, PDF p. 2) — the d[γ,X] covariation term
being the paper's own adjustment — and expected costs are
J = E[∫ D_{s-} dX_s + ∫ (γ/2) d[X]_s] (eq. 3, PDF p. 3), the (γ/2)d[X]
quadratic-variation term being the second adjustment; both adjustments are
derived as continuous-time limits of the discrete-time problem (Appendix A,
PDF pp. 42-44, with the discrete recursion motivating the BSDE in Appendix B,
PDF pp. 44-47). Under the sign condition 2ρ+µ−σ² > 0 (C>0), existence of a
[0,1/2]-valued BSDE solution (CBSDE), and (C[M]), the value function is
V_t(x,d) = (Y_t/γ_t)(d−γ_t x)² − d²/(2γ_t) (Theorem 3.4(i), PDF p. 10), where
Y solves quadratic BSDE (12) with driver (13) (PDF p. 9); an optimal strategy
exists if and only if the process β̃ from (14) admits a càdlàg semimartingale
version β (Theorem 3.4(ii)-(iii), PDF pp. 10-11), in which case it is
explicit (eq. 18). Two counterexamples carry the paper's bite: with constant
γ, ρ > 0, the conventional finite-variation cost functional ~J of (6)/(20)
satisfies ess inf ~J = −∞ over semimartingale strategies — scaled
Brownian-motion strategies X = νW with ν → ∞ give ~J → −∞ whenever
e^{−ρT} − 1 + ρT/2 < 0 (Section 4.1, PDF pp. 13-14) — and, even with the
right cost functional J, the conventional deviation dynamics without the
d[γ,X] term again give J → −∞ when γ is a geometric Brownian motion and the
strategy is a scaled GBM with ν → −∞ (Section 5.1, PDF pp. 15-17); with the
adjusted J and adjusted dynamics both problems become well-posed and the
optimum is explicit (Sections 4.2 and 5.2, PDF pp. 14-15, 18-19). Section 6
gives qualitative effects: optimal strategies can have infinite variation
even when ALL exogenous processes are smooth (Example 6.1, PDF pp. 20-21, the adaptedness failure making Z ≠ 0 being the
mechanism);
a jump only in the drift µ of γ forces a block trade inside (0,T)
(Example 6.2, PDF pp. 21-22 and Figure 2, PDF p. 23); negative resilience ρ < 0
— the paper's explicit reading: "self-exciting behaviour of the price impact,
where trading activities of the large investor stimulate other market
participants to trade in the same direction" (PDF p. 22) — makes it optimal to
sell MORE than the whole position in the initial block and then buy back
(Example 6.3, PDF pp. 23-24, Figure 3, PDF p. 24); and an optimal strategy can
fail to exist while the value function stays finite (Example 6.4/Situation 2,
PDF p. 25, µ of infinite variation, e.g. a Weierstrass function, provably
admits no semimartingale β). Sections 7 and 8 plus Appendix C prove BSDE
existence in two subsettings (Propositions 7.1 and 7.3, PDF pp. 26-29; the
0 ≤ Y ≤ 1/2 comparison, Proposition C.1, PDF pp. 49-50) and the main theorems.

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION. Findings (all graded against the queue as it stands at
fifty-one candidates plus probe E1):

1. [candidate sharpening, PENDING OWNER RATIFICATION] The
   strategy-class/convention well-posedness pre-declaration. BEFORE the L0
   gate, any C1-L2/C8-adjacent comparator, null, cost model, simulator or
   refutation instrument that defines a cost, objective or "optimality"
   statement must pre-declare, as frozen configuration counted in the
   multiplicity ledger: (i) the admissible process/strategy class over which
   the written definition is posed (finite-variation only, càdlàg
   semimartingales, general adapted), and (ii) a recorded well-posedness
   statement for the pairing of that class with the chosen bookkeeping
   convention — a boundedness-below argument for the objective over the
   declared class, or the dated limiting derivation (e.g. a discrete-time
   limit) that produced the convention, with every deviation a dated
   amendment before the data is touched. An objective computed under a
   convention whose well-posedness over the declared class was never
   established — with a divergent infimum known to exist in that class —
   fails at the gate, and any comparison resting on it is dead by rule.
   The paper proves the failure class is real twice in print with NO
   empirical content: with constant γ > 0 and constant ρ ∈ (0,1/T) — a
   parameterization that satisfies every pointwise sign condition in the
   impact-viability family (the Alfonsi-Infante Acevedo conditions and any
   analogue) — the finite-variation cost functional ~J of (20) satisfies
   ess inf ~J = −∞ the moment the strategy class widens to càdlàg
   semimartingales, since X = νW drives ~J = γν²/ρ(e^{−ρT} − 1 + ρT/2) → −∞
   (Section 4.1, PDF pp. 13-14); and even with the corrected J, the
   conventional dynamics (24) without the d[γ,X] term again yield J → −∞
   over scaled-GBM strategies once γ itself is stochastic (Section 5.1,
   PDF pp. 15-17) — while both problems are well-posed under the corrected
   pairings ((3) and (2)), each correction derived from the discrete-time
   limit (Appendix A, PDF pp. 42-44). So the failure is a property of the
   (convention × admissible class) PAIR, invisible in any single finite
   computed number, and not caught by any queued rule: the
   estimator-implementation concordance rule (deep-read 85) audits code
   against the written definition and passes a wrong-pairing definition
   cleanly; the impact-viability pre-declaration for generative nulls
   (deep-read 87) checks pointwise sign conditions of the impact
   parameterization and passes both counterexamples (γ, ρ positive
   constants); the transform-domain rule (#50) covers existence domains of
   transforms, not bookkeeping conventions. Harder-to-pass because a
   comparator or null whose cost bookkeeping is inherited from a
   narrower class than the one it will actually simulate or optimize over —
   today survivable as a silent convention, producing perfectly finite
   numbers while the infimum of its own objective diverges — now fails at
   the gate BEFORE any data is touched, where today no queued rule asks the
   question; tightens the estimator-implementation concordance rule
   (deep-read 85) by extending the audit from implementation-vs-definition
   to definition-vs-admissible-class well-posedness, and joins the
   impact-viability pre-declaration (deep-read 87) and the
   dynamics-identification rule for generative nulls (null-time session 58)
   in the generative-null pre-declaration family. Full text with the
   killed-if-wrong counterfactual below.

2. [reinforcing, no new item] The paper's own governance of its
   corrections is the estimator-discipline precedent already standing: the
   two adjustment terms (γ/2)d[X] and d[γ,X] are not choices, they are
   forced by the discrete-time limit (Appendix A, PDF pp. 42-44), and the
   paper states in print that preserving the conventional forms "can result
   in an ill-posed optimization problem" (PDF p. 4) with the conventional
   forms recovering exactly in the finite-variation special case (PDF p. 4,
   X^c = 0). This is the estimator-implementation concordance rule's
   (deep-read 85) class in reverse — a convention valid for one admissible
   class silently invalid for another — and it supports the queued rule's
   premise that written definitions, not just code, carry load-bearing
   conventions. The queued rule already carries this case given finding 1's
   extension. No further queue change.

3. [interpretation caution] Existence is not guaranteed by finiteness: the
   value function can be finite while NO optimal strategy exists, provably
   (Example 6.4, PDF p. 25 — a deterministic infinite-variation µ blocks any
   semimartingale β, Situation 2), and the paper's characterization routes
   existence through the semimartingale-version property of β̃ (Theorem
   3.4(ii), PDF pp. 10-11). The analogue for the programme: any future
   comparator or null that references "optimal" behavior of a model — the
   class a K7-style cost-survival layer or an execution-adjacent baseline
   would borrow from — must carry an existence statement for that optimum,
   or it references a vacuous object; a simulated "we behave optimally
   against X" pipeline over a model whose optimum does not exist is
   simulating nothing. Recorded as context. No queue change.

4. [interpretation caution] Negative resilience self-excitation
   re-encodes sign-alternation as OPTIMAL design, not artifact: the paper's
   explicit reading of ρ < 0 is self-exciting behaviour where the large
   investor's trading stimulates others to trade the same direction (PDF
   p. 22), and inside that assumed law the optimal liquidation of a long
   position sells MORE than x in the initial block, flips into a
   buy-program, and buys back — β > 1 makes 1−β negative, the strategy is
   non-monotone by construction, monotone only on (0,T] (Example 6.3, PDF
   pp. 23-24, Figure 3, PDF p. 24). Reads against the queued
   level-versus-memory disambiguation and the sign-persistence admission
   null family as a standing caution: a measured sign-alternating or
   round-trip-shaped flow pattern in book data is not itself diagnostic of
   manipulation, front-running or of any mechanism, if the assumed
   impact/resilience law can make it optimal — the interpretation of the
   sign pattern is conditional on the law, the same conditional-on-the-law
   shape as the price-process-family invariance rule (deep-read 66). No
   queue change.

5. [source-quality note] arXiv v2 [math.PR] revised 2021-07-26, 53 PDF
   pages in the extract, zero citations recorded in the index, pure theory
   with no data anywhere (the only simulations are Figures 1-3 of the
   paper's own theorems, PDF pp. 19, 23, 24), the acknowledgement thanks
   Alexander Schied and two anonymous referees (PDF p. 50), and the
   companion discrete-time study is self-cited as arXiv:2006.05843 (ref.
   [1], PDF p. 50) — a refereed published version likely exists; check it
   before formal citation. Ammunition only: no empirical claim in the
   paper, so nothing can leak into the record as evidence. No queue change.

## What this paper would have killed if we had done it wrong

Without finding 1's pre-declaration, a future C8 comparator or generative
null that borrows a cost/objective convention from the finite-variation
execution literature — the Obizhaeva-Wang/Alfonsi-Fruth-Schied family the
programme's own queue already cites for the impact-viability conditions —
and then optimizes or simulates over a wider process class (any
infinite-variation flow process, any stochastic-depth book) would produce
perfectly finite single numbers while its own objective's infimum is −∞
over that class, exactly the §4.1/§5.1 mechanisms with constant positive
parameters that pass every sign condition; a claimed refutation or
cost-comparison resting on such a number would be manufactured by the
convention with no visible fingerprint, since the divergence lives only in
the infimum, not in any computed value. Without the concordance rule
already queued, the wrong pairing would look like a modeling choice, not
a defect: the conventions reduce to the standard textbook forms in the
finite-variation case, so a spot-check against the inherited literature
would confirm rather than refute them. And for the self-excitation
interpretation: without the queued disambiguation family, a
sign-alternating optimal-looking flow pattern observed in a model with a
negative-resilience component would read as detected manipulation-type
behaviour when Example 6.3 proves it is simply optimal INSIDE the assumed
law — the programme avoids both deaths only because the conventions and
the admissible class are declared and frozen before the data is touched.

## Standing caveat

The paper is pure theory over one Wiener-driven block-LOB abstraction: no
empirical estimation, one-security single-horizon formulation, resilience
and impact entering as exogenously given processes with no story for where
γ and ρ come from, and all qualitative effects (infinite-variation optima,
interior block trades, oversell-flip behaviour, non-existence) constructed
in designed examples rather than calibrated markets — the examples prove
possibility, not prevalence, and say nothing about whether any of these
regimes occur in a crypto CLOB. The i.i.d.-free abstract results
(Propositions 7.1/7.3, PDF pp. 26-29) impose boundedness/continuity
conditions the measured book would have to be argued or frozen into
before any use. arXiv-version caution: v2 revised 2021-07-26 with referee
acknowledgement; check the published version before formal citation.
