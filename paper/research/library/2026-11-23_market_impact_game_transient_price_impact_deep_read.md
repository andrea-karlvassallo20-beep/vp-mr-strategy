# Deep-read note — library session 99 ("A market impact game under transient price impact")

- Session: null-time deep-read session 99 (null-time session 109, log ## 131),
  2026-11-23.
- Authors: Alexander Schied, Tao Zhang.
- Title: "A market impact game under transient price impact".
- Venue/id: arXiv:1305.4013v7 [q-fin.TR] (stamp 8 May 2017; slug xc495e3, per
  docs/library/expanded_index.json).
- What it is, one clause: a pure-theory analysis of the two-agent Nash
  equilibrium between competing high-frequency liquidators in a propagator
  (transient-impact) model, proving the "hot-potato game" equilibrium
  oscillations for small transaction costs and their disappearance above a
  critical cost threshold.

Read 2026-11-23, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xc495e3_a_market_impact_game_under_transient_price_impact.txt,
~26 pp., page-marked). Next UNREAD triage-rank entry (score 20, ninth of the
score-20 tier).

## The paper in one paragraph

Two competing agents must each liquidate an initial inventory by time T in a
market whose unaffected price is a martingale (assumed natural for
short high-frequency horizons, PDF p. 3), with trading on a discrete time
grid and linear transient price impact through a strictly positive-definite
decay kernel G (eqs. 1-2, PDF pp. 3-4); execution realizes the average of
the pre- and post-impact price, execution priority between simultaneous
orders is decided by an independent coin toss (symmetric latency), and each
trade incurs quadratic transaction costs of the form a progressive
transaction tax can reproduce near the origin (Definitions 2.1-2.2, eq. 3,
Proposition 2.6, PDF pp. 3-7). Theorem 2.5 proves existence and uniqueness
of the Nash equilibrium in the class of adapted strategies and gives it
explicitly: equilibrium strategies are deterministic and spanned by two
kernel-only vectors v and w (eqs. 7-8, PDF pp. 5-6). For theta = 0 and
sufficiently fine grids the equilibria oscillate strongly — each agent
passes the position to the other and buys a similar one back, the "hot
potato game", read as protection against predatory trading, which preys on
impact-created price drift and is neutralized by cancelling one's own
earlier impact (Remark 2.10, PDF p. 8). Theorem 2.7, the main result: for
continuous positive-definite log-convex kernels and equidistant grids, all
oscillations disappear exactly at and above the critical threshold of
transaction costs theta* = G(0)/4 (equilibrium strategies become buy-only or
sell-only), proved through triangular-Toeplitz inversion, the Kaluza sign
criterion and M-matrix theory (PDF pp. 7-8, 19-24); below theta*,
Proposition 2.8 proves the last three trades of w alternate signs and
Proposition 2.9 proves all entries of w alternate for exponential kernels on
equidistant grids (PDF pp. 8, 17-18). Numerical simulations, all on invented
parameters (G(t) = e^-t, T = 1; Figures 1-6, PDF pp. 9-13), show expected
equilibrium costs increasing in trading frequency for small theta but
decreasing at theta = theta*, a sawtooth odd/even-N alternation at theta = 0
(Figure 4, PDF pp. 10-11), and costs lower WITH transaction costs than
without, with a minimum at theta of roughly 0.06 (Figures 4-5, PDF
pp. 10-12), interpreted through the tax's asymmetry: a predatory strategy
is a round trip and is penalized more than a one-directional liquidation
(PDF p. 11). A price-of-anarchy comparison against unaware single-trader
strategies is defined (PDF pp. 11-13). Zero empirical content anywhere; the
Flash-Crash hot-potato vignette (27,000 contracts in 14 seconds, 49 percent
of volume, roughly 200 net contracts, from the CFTC-SEC report, PDF pp. 1-2)
is motivating narrative only.

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] Endogenous volume without information, proven
   in print: the model's Nash equilibrium generates strong two-sided volume
   recirculation (single components of v and w exceeding 60 percent of the
   initial position, Figure 1, PDF p. 9) with near-zero net liquidation,
   purely from strategic interaction between two agents — no information
   flow and no exogenous events required (Theorem 2.5 and Remark 2.10, PDF
   pp. 5-8). For C1-L2 and C8 this is the structural-confounder case in
   its cleanest form: high L2 activity, volume and turnover is not per se
   evidence of information-bearing flow. The C8 shuffled-arrival placebo and
   the generative-null pre-declaration families (## 118 lineage; #42, #47)
   already carry exactly this. No queue change.
2. [interpretation caution] The sign structure of simulated endogenous flow
   is decided by the strategic-structure assumption, not by the impact
   kernel: for the same convex, nonincreasing decay kernel, the single-agent
   optimum is buy-only or sell-only (Alfonsi-Fruth-Schied Theorem 1, quoted
   as Remark 2.11, PDF p. 10), while the two-agent equilibrium on the
   identical kernel oscillates (Theorem 2.7, Propositions 2.8-2.9, PDF
   pp. 7-8, 17-18). Game form (one optimizer versus two agents in Nash
   equilibrium) is an assumption no data can identify within the propagator
   family, and it flips the predicted sign structure. Under the
   estimator-configuration freeze and the dynamics-identification and
   generative-null pre-declaration families, the game form of any future
   generative null is one more knob that must be frozen before the data;
   this read records that as standing context for the existing pre-declaration
   discipline, nothing more. No queue change.
3. [interpretation caution] Grain conclusions invert with a cost constant:
   expected equilibrium costs INCREASE with trading frequency for small
   theta, DECREASE at theta = theta* = G(0)/4, and exhibit a pure
   grid-parity sawtooth (odd/even N) at theta = 0 that already disappears
   for theta = 0.01 (Figure 4 and its discussion, PDF pp. 10-11). In this
   model family, sampling-grid parity and the direction of grain-dependence
   are simulation artifacts conditional on an unmeasured cost parameter;
   no claim about "finer grain sees more" can be laundered through such a
   model. Reinforces the grain-association caution family and the
   flow-clock scale-constant frozenness. No queue change.
4. [cost-survival ammunition] "Transaction costs can reduce everyone's
   expected costs" (steep decrease to a minimum near theta of 0.06, then
   slow increase, Figure 5, PDF pp. 11-12; the calming-effect discussion,
   PDF p. 24) is relevant only if a future K7-style cost-survival layer ever
   exists, and that layer must carry the declared assumptions: zero
   bid-ask spread averaged over order types, with rebates, dark pools and
   exotic order types argued away (Remark 2.3, PDF p. 5), quadratic
   temporary impact standing in for slippage (eq. 3, PDF p. 4), symmetric
   latency by coin toss (Definition 2.2, PDF p. 4), and a martingale
   unaffected price (PDF p. 3). A "taxes calm fire sales" reading is
   model-internal on invented parameters; banned from the record as support
   for any programme claim. No queue change.
5. [source-quality note] Theory preprint by established microstructure
   authors, but: arXiv v7 stamped 8 May 2017 on a 2013 submission id; the
   oscillation assertions for the v vector are simulation-only ("at this
   time not able to prove", PDF p. 8); the oscillation and
   no-oscillation proofs hold only for log-convex kernels on equidistant
   grids, with the authors stating their proofs "cannot be extended beyond
   our stated conditions" and conjecturing the general result (Remark 2.12,
   PDF p. 10); several numerical observations are proven only in the
   companion follow-up paper (ref. [23], PDF pp. 11, 26); zero empirical
   content, no L2 data anywhere. Check for a published version before
   formal citation. No queue change.

## What this paper would have killed if we had done it wrong

Without the library-is-ammunition caveat, the headline that transaction
costs can reduce the expected costs of all market participants and calm
fire sales (PDF pp. 10-12, 24) would have entered the C8 macro-synthesis as
a licensed market property — a policy-flavored structural claim — when it
is a two-agent model-internal statement on an idealized block-shaped book
with a declared zero spread, quadratic slippage and invented parameters.
Without the estimator-configuration freeze, the game-form knob would
launder sign structure after the fact: the very same convex kernel predicts
buy-only behaviour for one agent (Remark 2.11) and oscillating hot-potato
behaviour for two (Theorem 2.7), so any observed L2 oscillation could be
"explained" by assuming two agents and any absence of oscillation by
assuming one, the assumption chosen post hoc — the pre-declaration
discipline exists so the programme can never occupy that position. Without
the grain-association caution, the odd/even-N sawtooth of Figure 4 would
be a reproducible "alternating structure" at fine sampling, elevated to a
market property from a pure simulation artifact. Without the laundering
discipline, the CFTC-SEC hot-potato magnitudes (49 percent of volume on
roughly 200 net contracts in 14 seconds, PDF pp. 1-2) would sit in a claim
as programme evidence, when they are a single-day, single-venue regulatory
quote usable only as motivation, never as support.

## Standing caveat

Everything is single-asset theory: martingale unaffected price (assumed
natural for high-frequency horizons, PDF p. 3), block-shaped-book linear
impact with execution at the average of pre- and post-impact prices, zero
bid-ask spread averaged over order types (Remark 2.3, PDF p. 5), quadratic
transaction costs standing for slippage or a tax, symmetric latency by coin
toss (PDF pp. 4-5). Two agents only; deterministic-equilibrium focus;
finite grids; the displaced notion of costs is liquidation cost against
book value. The oscillation results are proven for log-convex kernels on
equidistant grids (Theorem 2.7, via the Kaluza sign criterion and M-matrix
theory, PDF pp. 19-24) and, for full-vector alternation, for exponential
kernels only (Proposition 2.9, PDF pp. 18-19); the equivalence for general
positive-definite kernels is conjectured, not proven (Remark 2.12, PDF
p. 10); the v-vector oscillation evidence is numerical only (PDF p. 8).
The cost-reduction and frequency-inversion results are numerical on
invented parameters, partially proven in the follow-up [23]. The
Flash-Crash vignette is narrative motivation, not measurement. arXiv v7
preprint; check the published version before formal citation.
