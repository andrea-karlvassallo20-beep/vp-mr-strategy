# Deep-read session 56 — Optimal trade execution and price manipulation in order books with time-varying liquidity

**Authors:** Antje Fruth (Technische Universität Berlin), Torsten
Schöneborn (Deutsche Bank AG, London), Mikhail Urusov (Ulm University).
**Full title:** Optimal trade execution and price manipulation in order
books with time-varying liquidity.
**Venue:** arXiv:1109.2631v1 [q-fin.TR], 12 Sep 2011 stamp, zero
citations recorded in our index (topic tag arxiv-manip). The title page
carries both the 2011 arXiv stamp and an "October 8, 2018" date (PDF
p. 1): the OA copy is a later LaTeX recompile of the 2011 v1. The
GOALS.md front-2 pointer's paraphrase "time-dependent liquidity" and
this note's slug name the same paper, whose actual title word is
"time-varying". A paper that extends the Obizhaeva-Wang block
limit-order-book execution model to deterministic time-varying depth
and resilience, proves that a trading-dependent spread eliminates both
classical and transaction-triggered price manipulation, locates the
exact parameter boundary at which the zero-spread abstraction starts
admitting them, and characterizes optimal liquidation as a
wait-region/buy-region (WR-BR) singular-control structure.

Read 2026-11-20, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(`docs/library/text/x95643a_optimal_trade_execution_and_price_manipulation_in_.txt`,
~42 pp., page-marked). Next UNREAD triage-rank entry (score 28).

## The paper in one paragraph

The model (Section 2, PDF pp. 3-6): a block-shaped limit order book
with time-dependent height q_t (PDF p. 4); a buy market order ξ_t
consumes the ask side from A_t to A_t+ and widens the extra spread
D_t = A_t − A^u_t by ξ_t/q_t, which splits into a permanent part γξ_t
and a temporary part K_tξ_t (γ + K_t = 1/q_t) that decays
exponentially at deterministic rate ρ_t > 0; both sides of the book
carry separate deviations D_t, E_t (Eqs (1)-(2), PDF p. 5), so the
spread is trading-dependent. The risk-neutral investor minimizes
expected execution costs of buying x shares by T (Section 2.2, PDF p.
7); manipulation is defined in the Huberman-Stanzl and
Alfonsi-Schied-Slynko senses (Definitions 3.1-3.2, PDF p. 7). Three
results. First, the spread-bearing model admits neither classical nor
transaction-triggered price manipulation (Proposition 3.4, PDF pp.
9-10): "price manipulation strategies can be severely penalized by a
widening spread" (PDF p. 10), so the problem reduces to deterministic
pure-buying temporary-impact minimization (Proposition 3.3, PDF p. 8;
Section 4, PDF pp. 10-11). Second, optimal strategies scale linearly,
U(t,aδ,ax) = a²U(t,δ,x) (Lemma 5.1, PDF p. 12), collapsing the state to
the dimensionless ratio y = x/δ of remaining order over extra spread;
the value function has wait-region/buy-region structure with a
time-dependent barrier c(t) (Definitions 5.2-5.3, PDF pp. 13-14): always
in discrete time with a unique trade-to-barrier strategy (Theorem 6.1,
PDF p. 18; recursive algorithm, PDF p. 21), and in continuous time
existence needs K continuous (Theorem 7.1, PDF p. 22, with a
Dirichlet-type K counterexample having no optimum, PDF p. 22),
uniqueness needs µ + 2ρK > 0 (Theorem 7.6, PDF p. 26), WR-BR carrying
over (Theorem 7.7, PDF p. 26). Third, in the zero-spread variant (a
single deviation process, Eq (31), PDF p. 28): liquidity growing
faster than resilience manufactures classical price manipulation
(K'_t + 2ρ_tK_t < 0 somewhere, Proposition 8.3, PDF pp. 29-30, with no
optimal strategy at all), and under K'_t + 2ρ_tK_t > 0 the explicit
optimal strategy (35) exists (Theorem 8.4, PDF p. 30) with
transaction-triggered manipulation iff f_0 < 0 or f'_t + ρ_tf_t < 0
somewhere (Corollary 8.5, PDF p. 30; three-regime summary, PDF p. 31);
under condition (44) the dynamic-spread barrier is closed form
(Proposition 9.1, PDF p. 35), recovering the Obizhaeva-Wang "bathtub"
(Example 9.5, PDF p. 37).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The
   initial-state pre-declaration for refutation instruments. Mechanism:
   the zero-spread model's manipulation definitions had to be
   restricted to D^u_0 = 0 precisely because "even in 'sensible' zero
   spread models ... we typically have profitable round trips whenever
   D^u_0 ≠ 0", with the explicit strategy −D^u_0/(2κ)·1_(0,ε](s)
   profitable for any nonzero initial deviation (Remark 8.2, PDF p. 29).
   An initial state is not a market property; it is wiring the analyst
   chooses, and in exactly the abstraction class (single-price,
   zero-spread books) in which a generative null or placebo for the L2
   phase would plausibly be built, an un-pre-declared initial state
   plants the very structure the instrument is deployed to refute.
   Proposed amendment, hardening the dynamics-identification rule for
   generative nulls and the placebo-design precedent behind the queued
   C8 A3 shuffled-arrival placebo: any generative null, placebo,
   simulator, or other refutation instrument used anywhere in C1-L2/C8
   must pre-declare, before the data, its initial-state handling —
   initial book/impact/queue deviations set to zero, or drawn from a
   declared frozen distribution with a stated burn-in — and an
   instrument whose spec omits this fails pre-registration review.
   Harder to pass by construction: a refutation can no longer rest on
   an initial state chosen after seeing the data, and a null whose
   behavior depends on its un-pre-declared warm-up cannot be cited
   against a claim. Killed-if-wrong counterfactual: if the rule is
   wrong, it costs an instrument whose initial states genuinely needed
   post-hoc adjustment — in which case the declaration may be amended
   before the data of the test that uses the instrument, never after
   it. PENDING OWNER RATIFICATION; nothing armed.

2. [reinforcing, no new item] Whether "manipulation" exists at all is
   a property of the spread abstraction, not of the data: identical
   deterministic liquidity paths (K, ρ) are manipulation-admitting in
   the zero-spread model (K' + 2ρK < 0 → classical, Prop 8.3, PDF pp.
   29-30; f_0 < 0 or f' + ρf < 0 → transaction-triggered, Cor 8.5,
   PDF p. 30) and manipulation-free the moment the spread is allowed to
   widen with trading (Prop 3.4, PDF pp. 9-10, "severely penalized by a
   widening spread", PDF p. 10). A market-level verdict read off a
   stylized single-price book is a verdict about the model class.
   Reinforces the library invariant (ammunition, not evidence) and the
   dynamics-identification rule: no instrument's output may be
   laundered from its abstraction into a market claim. Nothing added.

3. [reinforcing, no new item] The manipulation boundary is a derivation
   boundary, sign-fragile and asymmetric: K'_t + 2ρ_tK_t = 0 separates
   the zero-spread model's three regimes (manipulation /
   transaction-triggered / clean, PDF p. 31), quickly RISING liquidity
   manufactures manipulation while quickly falling liquidity does not
   (PDF p. 30), and in the spread model K'_t + ρ_tK_t < 0 empties the
   buy region, c(t) = ∞, wait-the-whole-window (Prop 9.4, PDF p. 36;
   Prop 5.8, PDF p. 17). Any reading that places a fitted (K, ρ) near
   that boundary is one derivative estimate away from a sign flip —
   the same near-critical fragility as the Hawkes α < βE[ε] boundary
   (deep-read 53 / ## 67; deep-read 55 / ## 69). Reinforces the
   estimator-discipline family and the queued regime-window
   pre-declaration; nothing added.

4. [interpretation caution] The dimension reduction (Lemma 5.1, PDF p.
   12) says that in a block-book exponential-resilience model the
   entire value is determined by one dimensionless ratio y = x/δ
   (remaining order over extra spread), because optimal strategies
   scale linearly; the paper itself notes the scaling "does not
   generalize easily" beyond block shape plus exponential decay (PDF
   p. 11). Reading discipline for the L2 phase: before any future book
   feature is counted as independent information, check it does not
   dimensionally collapse onto a single ratio-like (depth-normalized,
   resilience-discounted) coordinate already spanned by another
   counted feature; in this model class raw depth, spread, and
   order-size levels are redundant coordinates of y. No queue change.

5. [reinforcing, no new item] Only the temporary-impact channel
   differentiates strategies: expected costs decompose into the
   martingale term A^u_0 x (martingale orthogonality, Eq (8), PDF p.
   8), the strategy-invariant permanent term γx²/2, and the
   temporary-impact term (Prop 3.3, PDF p. 8; Eq (9), PDF p. 8).
   Whatever order-flow-relevant information this model class carries
   lives in the transient book-displacement channel, never in the
   level or the martingale — second evidence for why C1-L2 targets
   flow-dynamics statistics (resilience, refill, displacement decay)
   rather than levels. Reinforces the queued dynamics-identification
   rule; nothing added.

6. [source-quality note] Purely theoretical: no data, no estimation,
   no calibration anywhere in the paper; deterministic depth and
   resilience only, stochastic liquidity deferred to Fruth (2011)
   (PDF p. 1 fn 1), single large investor, risk-neutral. The OA copy
   is the 2011 v1 text in an "October 8, 2018" recompile (PDF p. 1),
   so both dates travel with the file; zero citations recorded in our
   index. Check for a published version (the Alfonsi-Schied-Slynko and
   Gatheral-Schied-Slynko line it builds on is on the shelf) before
   formal citation outside the note.

## What this paper would have killed if we had done it wrong

The zero-spread-null death: had a future C1-L2/C8 generative null or
placebo been built on a single-price (zero-spread) book abstraction
with its initial deviation state left un-pre-declared, the abstraction
itself manufactures round-trip profitability for any D^u_0 ≠ 0
(Remark 8.2, PDF p. 29) and, for fast-rising liquidity,
unconditionally (Prop 8.3, PDF pp. 29-30) — every verdict such an
instrument returned would be an artifact of its wiring, and a
refutation record built on it would have laundered model-class
structure into market claims. Pre-empted by the queued
dynamics-identification rule, this session's initial-state
pre-declaration, and the library invariant that no paper's model is
evidence. And the boundary-laundering death: calibrating (K, ρ) within
derivative noise of K' + 2ρK = 0 and reading which side of zero a
fitted estimate lands on as a discovered "manipulation regime" — the
same manufactured-boundary laundering the regime-window pre-declaration
(## 67) already forecloses, seen here from the manipulation side rather
than the self-excitation side, by the same senior-author family
(Urusov).

## Standing caveat

The model is a single-investigator, risk-neutral, block-shaped-book,
exponential-resilience abstraction; depth and resilience are
deterministic functions of calendar time (intraday seasonality is the
motivation, PDF pp. 1-2), state-dependence beyond trading impact is
absent, and stochastic liquidity is out of scope by construction (PDF
p. 1 fn 1). Every result in the paper is model-class mathematics with
zero empirical content — the paper's own contribution is precisely
that its "manipulation" objects appear and vanish with modeling
choices (spread on/off, D^u_0 zero/nonzero), which is its ammunition
value and the limit of it. The optimal-execution content (barriers,
trade-to-barrier schedules, the bathtub, the (35) strategies) is
execution engineering, is recorded here as context only, and is never
operationalized; nothing trades live. The published version of the
paper is unchecked on the shelf; check before formal citation outside
this note.
