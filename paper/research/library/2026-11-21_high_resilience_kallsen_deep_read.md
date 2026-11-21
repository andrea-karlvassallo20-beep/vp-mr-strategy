# Deep-read session 70 (null-time session 81, log ## 90) — the Kallsen–Muhle-Karbe high-resilience limit paper read; the reduced-form quadratic trading cost shown to be a THEOREM'S OUTPUT derived from three book premises (height, resilience, recovery asymmetry) rather than a free primitive; the resilience shown to sit in the transient-cost denominator while the permanent impact is resilience-independent; the equivalence shown to hold only inside an explicitly bounded strategy class; nothing sharpened

Jan Kallsen (Kiel), Johannes Muhle-Karbe (ETH Zürich / Swiss Finance
Institute), "High-Resilience Limits of Block-Shaped Order Books"
(arXiv:1409.7269v1 [q-fin.TR], 25 September 2014; zero recorded
citations in the acquisition index, no published version recorded
there). A pure-mathematics structure paper with no data and no
empirics: it generalizes the Obizhaeva/Wang block-shaped order-book
model (stochastic book heights h↑, h↓, stochastic resilience rates,
permanent-impact fractions α↑, α↓ ∈ [0, 1/2]) with wealth dynamics
(Def. 2.2, eqs. 2.1-2.7, PDF pp. 2-4), and proves as its main result
(Theorem 4.1, PDF pp. 4-5) that as the resilience κ → ∞ the
Obizhaeva/Wang wealth process converges, uniformly on compacts in
probability, to an Almgren/Chriss reduced-form wealth process whose
quadratic temporary cost is λ↑ = (1−α↑)/(κK↑h↑), λ↓ = (1−α↓)/(κK↓h↓)
of exact order O(κ−1), whose permanent linear impact γ↑ = α↑h↑,
γ↓ = α↓h↓ is independent of the resilience, and whose proportional
spread costs ε↑, ε↓ are the book's exogenous baseline. The convergence error is
o(κ−1). Extensions: the κ1/4-scaled active families (Remark 4.2,
PDF p. 6, error o(κ−1/2)), the Lp strengthening under uniform
boundedness (Remark 4.3, PDF pp. 6-7), and Lemma 4.4 (PDF pp. 7-8):
block trades are asymptotically dominated by smoothed absolutely
continuous strategies as resilience grows. Section 5 (PDF pp. 8-11)
applies the limit to portfolio choice: the Moreau–Muhle-Karbe–Soner
small-impact optimizer dϕt = √(κKtht)(σSt)2/(2Rt)·(ϕ∞t − ϕt)dt
(eq. 5.1, PDF p. 9) is asymptotically optimal at leading order
O(κ−1/2) in the Obizhaeva/Wang model too, provided the competing
strategies track a regular frictionless target at rate O(κ1/4)
(Lemma 5.1) and the uniform-integrability classes (5.4)-(5.5) hold
(Theorem 5.2, PDF pp. 9-10), which Corollary 5.3 discharges only under
uniform boundedness of all primitives away from zero (PDF p. 11).

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x475f30_high_resilience_limits_of_block_shaped_order_books.txt,
~12 pp., page-marked, complete, references included). Next UNREAD
triage-rank entry (score 25, x475f30), per the recorded ## 88 pointer
and re-verified against the live file state this session: the score-25
tier order in docs/library/edge_triage_scores.json is x074d5c (read,
## 85), x8f729f (read, ## 87), x6b73c4 (read, ## 88), then x475f30 —
the pointer is correct; x475f30 carries no prior note and no prior log
entry reports reading it.

## The paper in one paragraph

The paper's single claim is a limit theorem: two of the field's
standard price-impact models, the structural block-shaped book of
Obizhaeva/Wang and the reduced-form cost model of Almgren/Chriss, are
the same object in the high-resilience limit, and the connection
identifies the reduced-form cost coefficients in terms of "observable
properties of the order book, namely i) its height, ii) its
resilience, and iii) how symmetrically it recovers on the bid and the
ask sides" (PDF pp. 1-2, Thm 4.1, PDF pp. 4-5): the wealth processes
converge with an O(κ−1) error decomposition that separates the
resilience-independent permanent impact, the O(1) exogenous spreads,
and a transient quadratic cost whose every parameter is a book
quantity divided by the resilience and book height. The authors spell
out the regime boundary themselves: the theorem covers absolutely
continuous strategies with bounded turnover rates (Thm 4.1, PDF
pp. 4-5), families scaled at most as κ1/4 (Remark 4.2, PDF p. 6),
with block trades proved asymptotically suboptimal in this regime
(Lemma 4.4, PDF pp. 7-8); the portfolio-choice transfer carries the
same discipline, holding among regular target-tracking families under
uniform-integrability conditions discharged only by uniform
boundedness of the primitives (Thm 5.2 with (5.4)-(5.5), Cor. 5.3,
PDF pp. 9-11). No dataset appears anywhere; every statement is a
theorem under Assumption 2.1's regularity (PDF p. 3).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening — default grade;
every mechanism found is a page-cited instance of a discipline the
queue already carries.

1. [reinforcing, no new item] The headline "trading cost" is a
   DERIVED object, not a primitive: the quadratic reduced-form cost's
   functional form λ = (1−α)/(κKh) is the output of Theorem 4.1, a
   consequence of the block-shape premise, the exponential-resilience
   premise and the recovery-asymmetry parameter α (Thm 4.1, PDF
   pp. 4-5; the decomposition statement PDF p. 5 — permanent impact
   independent of resilience, transient cost of order O(κ−1), spreads
   O(1)). This is the cost-side sibling of the ## 84 Çetin–Waelbroeck
   exhibit (impact functional form derived from two analyst premises)
   and one structural level deeper than the ## 85 and ## 88
   price-process exhibits: there the assumed family moved an estimated
   LEVEL, here the assumed book family manufactures the cost
   functional's FORM itself, and the same three inputs in a different
   book family would produce a different reduced-form cost object.
   Reinforces the spread-convention declaration rule, the
   price-process-family invariance rule (#38) and the
   estimator-identity family; no new item.
2. [interpretation caution] The resilience sits in the transient
   cost's DENOMINATOR while the permanent component is untouched by it
   (λ = O(κ−1)K−1h−1, γ = αh independent of κ, PDF p. 5): a
   mis-estimated recovery rate silently rescales the transient-impact
   cost by its exact reciprocal and leaves the permanent impact
   alone, so a cost decomposition quoted without its resilience,
   height and asymmetry inputs is not yet a defined quantity, and a
   permanent-versus-transient attribution made under one resilience
   estimate does not survive a different one. Any C1-L2/C8
   cost-adjacent figure falls under the estimator-identity and
   cost-convention disciplines as recorded; no queue change.
3. [interpretation caution] The two models' equivalence is explicitly
   class-bounded, by the authors' own statements: absolutely
   continuous bounded-rate strategies (Thm 4.1, PDF pp. 4-5),
   κ1/4-limited families with the convergence rate degrading to
   o(κ−1/2) beyond the basic theorem (Remark 4.2, PDF p. 6), and a
   portfolio-choice optimality transfer that holds only among
   target-tracking families satisfying the uniform-integrability
   classes (5.4)-(5.5), discharged by boundedness away from zero
   (Thm 5.2, Cor. 5.3, PDF pp. 9-11). A limit-theorem premise cited
   outside its class carries no evidential weight toward anything;
   reading-discipline only, no queue change.
4. [cost-survival ammunition] Lemma 4.4 (PDF pp. 7-8): in the
   high-resilience regime block trades are asymptotically dominated
   by smoothed continuous trading, and the leading correction to
   frictionless performance is O(κ−1/2) with the optimal turnover
   scale √(κKh) in the tracking-rate's numerator (eq. 5.1, PDF
   p. 9). Execution-strategy engineering is context, never content:
   recorded only as the class of assumptions a future K7-style
   cost-survival layer would have to carry (block-shape benchmark,
   resilience-scaled turnover, O(κ−1/2) leading order) if such a
   layer ever exists. No operationalization, nothing armed.
5. [source-quality note] arXiv v1, 2014, indexed venue is the arXiv
   id itself; the acquisition index records zero citations and no
   published version, though the authors are established and a
   published version may exist — check before any formal citation. A
   theorem-only paper: no data, no simulation, no empirical
   validation of any kind, so nothing in it can serve as empirical
   support for any programme claim even if the invariants allowed it
   (they do not: the library is ammunition, not evidence).

## What this paper would have killed if we had done it wrong

If the programme had ever taken the Almgren/Chriss quadratic-cost form
as a free primitive — a cost model chosen because it is "standard" —
then any C1-L2 or C8 cost figure would silently encode three
unexamined book premises (block shape, exponential resilience,
recovery asymmetry), and a book-family change would have rewritten the
cost functional under the programme's feet without any instrument
noticing; the derived-cost exhibit is the structural argument for why
the cost-convention declaration rule and the family-invariance rule
are load-bearing. And if a session had ever read Section 5's
optimality transfer without its integrability premises, a
limit theorem proved for a bounded strategy class would have been
cited as if it licensed choosing execution behavior — exactly the
operationalization the hard invariants forbid by construction; the
paper itself names the class boundary in every statement, and the
counterfactual programme would have had to invent it.

## Standing caveat

The result lives entirely inside the block-shaped-book family with
exponential resilience and linear permanent impact — the linearity of
permanent impact adopted to avoid price-manipulation quasi-arbitrage
(Huberman–Stanzl, PDF p. 2, fn. 5) — and the analytic fine print
(Assumption 2.1's continuity and boundedness, the localization steps
in both proofs, the integrability classes) is the actual price of the
clean statement. Nothing in the paper bears on low-resilience or
sparse books, where the two models are simply different models. The
shelf copy is arXiv v1; check for a published version before any
formal citation.
