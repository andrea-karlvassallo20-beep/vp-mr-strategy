# Deep-read note — session 73: "Optimal execution with deterministically time varying liquidity" (Palmari–Lillo–Eisler, arXiv:2410.04867v2)

**Deep-read session 73** (null-time session 84). Gianluca Palmari, Fabrizio
Lillo, Zoltan Eisler, "Optimal execution in a time-varying environment:
well-posedness and price manipulation" (indexed as "Optimal execution with
deterministically time varying liquidity: well posedness and price
manipulation"), arXiv:2410.04867v2 [math.OC], October 2024, v2 stamped
19 March 2026. A pure-theory paper on when the Almgren-Chriss optimal
execution problem with deterministically time-varying impact coefficients
stays well posed, and when it admits transaction-triggered price
manipulation.

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x217e71_optimal_execution_with_deterministically_time_vary.txt,
~49 pp., page-marked). Next UNREAD triage-rank entry (score 25, x217e71),
closing the score-25 tier.

## The paper in one paragraph

The paper puts deterministic time-dependence into the Almgren-Chriss
temporary and permanent impact coefficients (θt, ηt) and asks when the
liquidation problem is well posed (PDF pp. 1-12). In discrete time the
problem reduces to a quadratic form in an impact-encoding matrix A (Eq. 6,
PDF p. 7); strong well-posedness (unique solution, monotone liquidation, no
transaction-triggered manipulation) is guaranteed when A is a B-matrix
(Prop. 4, PDF pp. 9-10), yielding a checkable sufficient condition on the
sampled coefficients (Prop. 5, PDF p. 10) and, on refined grids, a
continuous-time admissibility inequality bounding the remaining-horizon-
weighted cumulative decay of permanent impact by the minimal temporary
impact (Props. 6 and 13-14, PDF pp. 11, 18-19). In continuous time the
extremal solves a non-autonomous Euler-Lagrange boundary-value problem
(Eq. 20, PDF p. 14); a second-order condition γT² < π² with
γ = θ̄/2η̄ (θ̄ the maximal decay rate of permanent impact, η̄ the minimal
temporary impact) guarantees the unique maximum and non-negativity
(Props. 9-12, PDF pp. 14-18), and the monotonicity table (Table 1, PDF p.
22) classifies solution shapes by the signs of impact dynamics. Numerics on
exponential and power-law decaying impacts (PDF pp. 22-26, 45-48) confirm
that rapidly decaying permanent impact relative to minimal temporary impact
produces buy-first "manipulation-type" optima inside the admissible region,
though with positive expected costs, and Example 6 shows a linear-decay
setting with genuinely negative costs (PDF pp. 16-17). The motivating
empirical anchor is a J-shaped deterministic intraday impact trajectory
estimated on one month of Microsoft (Fig. 1, PDF pp. 2-3).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION (the deterministic-calendar null, below). Nothing measured,
nothing armed, nothing trades live.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The
   deterministic-calendar null: before the L0 gate, any C1-L2/C8-adjacent
   spec interpreting an intraday anticipatory, reversal, impact-decay or
   buy-before-sell-type structure as conditioned on book state or flow
   must pre-declare a deterministic-calendar null — a time-of-day
   surrogate built only from frozen constants (calendar position, e.g.
   the J-shaped intraday impact/liquidity profile as a pre-declared
   generic default), carrying zero book-state input — and must show the
   structure survives that null before it may enter any spec as support.
   The paper proves the mechanism is real and needs literally no
   information: with permanent impact decaying linearly in time and
   temporary impact constant, the OPTIMAL liquidation of a long position
   begins by BUYING (ζ̇0 > 0, Example 6, PDF pp. 16-17), and for
   T = 1, a = 5, η = 0.25, b < −4.09 the excess cash is genuinely
   negative-cost — proper price manipulation (PDF p. 17) — with no
   self-excitation, no stochastic state, no news, nothing but the
   calendar. The empirical anchor is exactly such a deterministic
   J-shaped trajectory, estimated intraday on MSFT June 2021 (Fig. 1,
   PDF pp. 2-3). An apparent "anticipatory" intraday shape in L2 data
   that is a pure time-of-day geometry artifact would otherwise sail
   through a state-conditioned test. Harder-to-pass because a feature
   whose intraday shape survives only before removing the calendar
   component now fails at the gate instead of surviving as
   state-conditioned. Tightens the two-null admission family (log ## 17),
   joining the Gould-Bonart Eq.-7 comparator, the tautology-controlled
   OFI benchmark and the sign-persistence admission null with a fourth
   null that needs no state input at all; same tightening shape as the
   self-excitation regime-window pre-declaration and the
   level-versus-memory disambiguation. Ratified by nobody; queued only.

2. [reinforcing, no new item] Pointwise parameter bounds do not certify
   global well-posedness once coefficients vary: the paper's own Example
   2 exhibits a configuration satisfying ηi > θi/2 for every i that is
   nevertheless ill-posed (det(A) < 0, saddle, unbounded cost) when
   permanent impact is time-varying (PDF pp. 8-9); the sufficient
   condition changes character entirely (diagonal dominance, B-matrix,
   PDF pp. 9-10). The lesson mirrors the window-geometry items already
   in the queue (self-excitation regime-window pre-declaration, estimator
   window/level declarations): a validity statement proved per-window
   does not compose into a validity statement over the whole time-varying
   path. Reinforces that family; no new item.

3. [interpretation caution] Nothing in the optimal solution is
   anticipation of the market: by construction the optimal strategy is
   static — fixed at time zero from the deterministic impact calendar
   (PDF pp. 27, 4-5) — and every "manipulation" the paper exhibits is
   exploitation of the impact model's own geometry, not information about
   future prices. Any C8-adjacent exhibit citing execution-optimality
   results as evidence of predictive content would be laundering an
   engineering property into a forecast; reading discipline only, no
   queue change.

4. [reinforcing, no new item] The J-shaped deterministic intraday impact
   trajectory that motivates the whole paper rests on one name, one
   month, one venue (MSFT June 2021, Fig. 1, PDF pp. 2-3), estimated by
   two separate methodologies for the two impact components; the paper
   itself flags testing whether markets ever sit in the manipulation
   region as future work (PDF pp. 27). Importing the J-shape as a
   market-wide calendar prior would launder one month of one stock into
   a property of markets — the base-rate audit family; no new item.

5. [cost-survival ammunition] The paper's admissibility hierarchy
   (B-matrix on every refined grid, sampling-robust √γT ≤ √2, versus the
   weaker continuous-time √γT < π; PDF pp. 18-19, Remark 3) defines the
   constraint class a future K7-style cost-survival or execution layer
   must carry: impact coefficients with bounded decay rates, grid-
   consistent admissibility checks, and the θ̄/(2η̄) ratio as a named
   survival quantity. Recorded only as assumptions that layer must
   declare; never operationalized, nothing armed.

6. [source-quality note] arXiv v2 (math.OC), zero recorded citations in
   the index, no published version recorded; the index title ("Optimal
   execution with deterministically time varying liquidity") differs
   from the extract's printed title ("Optimal execution in a
   time-varying environment: well-posedness and price manipulation") —
   check the published version and the title history before any formal
   citation; whatever the version, no empirical claim here can serve as
   support for any programme claim.

## What this paper would have killed if we had done it wrong

Without the two-null admission discipline and the spread-convention
declaration, a calendar-driven shape is exactly what a hungry L2 scan
would find first: the paper proves that a deterministic, information-free
liquidity decay alone makes the optimal behavior of a plain sell program
start with buys and, at one parameter point, generate negative costs
(Example 6, PDF pp. 16-17) — the same "buy-then-sell before the move"
signature that a naive reading would file as anticipatory flow. Had a
C1-L2 feature entered the record on the strength of such a shape, with
the time-of-day component never named as a null, the sealed-prediction
record would have spent weeks resolving a calendar artifact against
cached klines, and the falsification record — the only asset the
programme owns — would have been spent on a structure that carries no
state information at all. The pointwise-bound lesson (finding 2) is the
second counterfactual: a per-window validity certificate would have been
accepted as a global one, the exact composition error Example 2 exhibits.

## Standing caveat

Deterministic-only impact, by design — stochastic liquidity models are
cited, not analyzed (PDF pp. 3, 2); linear Almgren-Chriss impacts, no
cross-impact (named as future work, PDF p. 27); all conditions sufficient,
not necessary, with an acknowledged gap between the sampling-robust
strong criterion and the weaker continuous one (PDF p. 19); the one
empirical exhibit (Fig. 1) is a single name, single month, estimated
purely to motivate, never tested against market conditions; and the
numerics are parametric exercises in two families (exponential and
power-law decay), not fits to data. arXiv-version caution: v2 dated 19
March 2026, nearly eighteen months after v1 — check the published version
and its title before formal citation. Nothing here validates any model on
real data, and the paper claims no predictive content anywhere.
