# Simulating and analyzing order book data: The queue-reactive model —
# deep-read note

Paper: Weibing Huang (LPMA, UPMC Paris 6, and Kepler-Cheuvreux),
Charles-Albert Lehalle (Capital Fund Management), and Mathieu Rosenbaum
(LPMA, UPMC Paris 6), "Simulating and analyzing order book data: The
queue-reactive model" (arXiv:1312.0563v2 [q-fin.TR], indexed 2013, v2
stamp 3 Sep 2014). Triage: score 29, slug
x8afb03_simulating_and_analyzing_order_book_data_the_queue
(edge_triage_scores.json), the next UNREAD entry in triage order,
selected per the ## 56 closing pointer. Extract: 29 pp., page-marked,
complete, references included (docs/library/text/
x8afb03_simulating_and_analyzing_order_book_data_the_queue.txt).

Read line: Library deep-read session 49, null-time session 53,
2026-11-19. Selected per the previous session's pointer (score 29,
x8afb03), re-verified unread against all 49 library notes on main and
the log at read time; read-set recomputed by the established
slug-and-normalized-title method; zero open PRs, no branch claims the
slug. Read in full against the ONE question: what here would kill C1-L2
or C8 faster, or change their kill lines?

Operational disclosure: a fresh main tarball was fetched and the
integrity guard run clean before this read; main was found advanced to
log ## 56 (deep-read 48) by successor sessions, so this session's
numbering is deep-read 49 = null-time 53 = log ## 57. No renumber; the
offset mapping is honored.

## The paper in one paragraph

The authors model the limit order book around a fixed reference price
pref (the midprice, with an even-spread tie-break toward the previous
value, PDF p. 6) as a continuous-time Markov jump process in 2K queue
sizes, with all event intensities — limit insertion, cancellation,
market order — functions of the book state only (PDF pp. 4-7), prove
ergodicity under negative individual drift and bounded incoming flow
(Theorem 2.1, Assumptions 1-2, PDF pp. 4-5), and estimate the
intensity functions by maximum likelihood on Cheuvreux 5-limit Euronext
data, January 2010 to March 2012, on two large-tick stocks (France
Telecom, Alcatel-Lucent), first and last trading hours removed (PDF
pp. 5-6). Three nested conditioning sets are estimated: independent
queues (Model I), second-limit intensities conditional on first-limit
emptiness (Model IIa), and first-limit intensities conditional on the
opposite queue's size band (Model IIb), with invariant distributions
computed in product form, by matrix-geometric QBD methods, or by
Monte-Carlo respectively, all closely matching empirical book
distributions (Figs. 3, 5, 7-8, PDF pp. 10-15). Adding a reference-price
jump mechanism with move probability theta and reinitialization
probability theta_reinit (the queue-reactive model, PDF pp. 17-18),
calibrated to 10-minute volatility and a mean-reversion ratio, yields a
market simulator; with theta_reinit = 0 the "maximal mechanical
volatility" of purely book-driven dynamics is 5 bps against 14 bps
empirical, with mean-reversion ratio 0.08 against 0.39 (PDF p. 18),
attributing the gap to exogenous information; calibrated values are
theta = 0.7 and theta_reinit = 0.85 (PDF p. 20). Applications compute
execution probabilities (Fig. 9, PDF p. 16) and simulate order
placement tactic slippage and market impact profiles, which come out
concave in time and volume, square-root-law compatible, with no price
relaxation emerging (Figs. 11-12, PDF pp. 21-22).

## Findings, graded (does any kill line move?)

Verdict: NO kill line changed. ONE new candidate sharpening queued,
PENDING OWNER RATIFICATION: the dynamics-identification rule for
generative nulls.

1. [candidate sharpening, PENDING OWNER RATIFICATION] — the
   dynamics-identification rule. The invariant distribution of this
   model class is determined by the arrival/departure ratios
   rho_i(n) alone, in explicit product form (PDF p. 10), and the
   authors state the consequence plainly: "two assets can have very
   different flow dynamics, but still the same invariant distribution"
   (PDF p. 10). Static book marginals do not identify the generating
   dynamics. Proposed amendment, tightening the placebo and
   generative-null design precedents (the ## 45 synthetic-rebuttal
   precedent and the C8 A3 shuffled-arrival placebo): any generative
   null, placebo, or simulator accepted as a refutation instrument in
   C1-L2 or C8 estimation must pre-declare, next to the static
   marginals it is constructed to match, at least one flow-dynamics
   statistic (event-order, conditional waiting-time, or transition-rate
   statistic) that it must also reproduce; a null validated only on
   invariant or static distributions is inadmissible as a refutation
   instrument. This makes every future test harder to pass: a null can
   no longer be certified faithful by distributional match alone, so a
   refutation or a placebo surviving it carries more force, and a
   future C1-L2 claim cannot be bolstered by a straw null that matches
   the board's shape while carrying arbitrary dynamics.

2. [reinforcing, no new item] — the maximal mechanical volatility
   bound. Purely book-driven dynamics (theta_reinit = 0, theta = 1)
   generate 5 bps of 10-minute volatility against 14 bps empirical,
   with mean-reversion ratio 0.08 against 0.39 empirical on France
   Telecom (PDF p. 18): endogenous queue mechanics alone UNDER-produce
   price volatility and over-produce mean reversion. This is the
   opposite signed direction from the Hawkes-line artifacts that
   inflate endogeneity, so it reinforces the ## 51 signed-bias
   conjunction caution as a worked exhibit: endogeneity quantifications
   are model-relative, no signed endogeneity bias is quotable in
   either direction, books-versus-flow definitions do not commute, and
   the register stands. For C1-L2 this is context with teeth: whatever
   the compression layer reads lives inside a mechanical ceiling this
   class of model bounds from above — on this venue, by a factor near
   three — but the bound itself is venue- and model-relative and
   enters no spec.

3. [reinforcing, no new item] — state-dependence of all three flow
   intensities in the book state is measured, shaped, and economically
   mechanized: first-limit insertion near-constant in queue size with
   a dip at the empty queue, second- and third-limit insertion
   decreasing in queue size (queue-priority pre-positioning),
   cancellation increasing-concave in queue size against the classical
   linear assumption (queue-priority value), market-order intensity
   exponentially DECREASING in available volume ("rushing for liquidity
   when liquidity is rare"), second-limit intensities conditional on
   first-limit emptiness, first-limit intensities decreasing in the
   opposite queue's size (PDF pp. 8-9, 11-14). These are
   economic-mechanism exhibits for the state-conditioned flow-modulation
   premise family behind C1-L2's hunting license; the paper predicts
   FLOW intensities, never price direction, and licenses no
   return-predictive claim.

4. [interpretation caution] — the parameters are estimated ONLY during
   constant-reference-price periods, with the recording process
   restarted at every pref change (PDF pp. 4, 7), and the honest
   consequence is visible in Model IIb: the joint distribution of the
   two best queues mismatches empirics at exactly the states adjacent
   to price moves, and is repaired only by adding the price-move
   mechanism itself (PDF p. 15). The intensity estimates describe the
   book BETWEEN price moves; they are not licensed at the transition
   moments where C1-L2 trigger readings fire. An instance of the ##
   51 selection-of-windows reading mode, in its sharpest form:
   conditioning on the inter-move regime censors the transitions by
   construction. No queue change.

5. [interpretation caution] — theta_reinit = 0.85, read as "the
   percentage of price changes due to exogenous information" (PDF
   p. 17), and the mechanical-volatility gap express one venue-and-
   model-relative decomposition of moves into mechanical and exogenous
   parts. Neither number may be cited as a market property; any future
   C8 decomposition of a move into mechanical and informational
   components must treat the boundary as estimated, venue-specific,
   model-relative, and pre-declared, and the crypto-perp venue has no
   Euronext session structure behind these calibrations at all.

6. [interpretation caution] — the paper's own estimation conventions
   carry consequences and must be disclosed if ever imitated: the
   bid-ask symmetry assumption (identical intensity functions on both
   sides, PDF p. 7) erases side asymmetry by construction — on any
   venue where taker-side imbalance carries the signal, a
   symmetric-parameter model kills it before estimation begins; the
   closed-form QBD route further requires a level-independence
   assumption of constant Poisson rates at the first limits
   (Assumption 5, PDF p. 25); queue values are rescaled by
   average-event-size ratios across limits when pref moves (PDF p. 17;
   AES versus ATS, PDF p. 28, Table 2). Reading conventions, not
   universal properties; none enters any spec.

7. [cost-survival ammunition] — the execution machinery hands any
   future cost layer named, author-signed bias axes: execution
   probabilities are overestimated under Poisson flows (Fig. 9,
   PDF p. 16); Assumptions 3-4 (uniform cancellation within the queue,
   the tracked order never canceled) are declared contrary to evidence,
   biasing execution probabilities upward (PDF p. 16, citing Gareche
   et al.); slippage distributions invert their tactic ranking with
   the scheduling-benchmark pairing (Fig. 11, PDF p. 21); impact
   profiles are concave in time and volume with NO price relaxation
   emerging in the Markovian framework (PDF p. 22). "No relaxation"
   is a model property of this simulator class, not a market verdict;
   any future execution-cost layer for L2-grain backtests must carry
   its impact-relaxation stance as an explicit pre-declared input and
   may not cite this class as evidence for it.

8. [source-quality note] — two Euronext Paris large-tick stocks
   (average spreads 1.43 and 1.99 ticks, Table 1, PDF p. 6), one
   brokerage 5-limit database, January 2010 to March 2012, auction
   hours removed; the framework is claimed applicable where the
   average spread is under roughly 2.5 ticks (PDF pp. 2, 6); no number
   transfers to the crypto-perp venue without re-estimation. The
   conclusion names the boundary honestly: historical order flows and
   their autocorrelation are NOT considered, the model conditions only
   on the current book state (PDF p. 22) — the entire flow-memory line
   (Hawkes, OFI) lives outside this model, so "state explains X" versus
   "memory explains X" comparisons across these model classes are
   comparisons across different conditioning sets and are confounded
   unless the conditioning sets are aligned. arXiv v2 read as-is; the
   published version NOT checked at reading, flagged for verification.

## What this paper would have killed if we had done it wrong

Had the mechanical-volatility bound been laundered INTO the record as
"a third of realized volatility is exogenous news," a single-venue,
two-stock, model-relative ceiling calibrated on auction-trimmed
Euronext session data would have hardened into a market law
constraining every future C8 decomposition. Had the close match between
modeled and empirical invariant distributions (Figs. 3, 5, 7-8) been
read as model validation, the paper's own identification statement
(PDF p. 10) — identical statics, arbitrary dynamics — would have been
contradicted by the citation itself, and a future C1-L2 placebo
certified on shape match alone would have been a refutation instrument
that cannot refute. Had the state-dependence exhibits been imported as
"the book predicts price," a paper that predicts flow intensities and
bounds its own mechanical volatility well below empirical would have
been converted into return-predictive support for a compression signal
it never tested. Had the constant-pref estimation windows been
imitated without disclosure, the transition-censoring consequence the
authors themselves exhibit in Model IIb (PDF p. 15) would have biased
C1-L2 trigger readings at exactly the firing moments. Had the
execution-probability and no-relaxation results been imported into a
cost layer as market facts, author-declared upward-bias assumptions
(PDF p. 16) and a Markovian model property (PDF p. 22) would have
become backtest parameters. Library-is-ammunition, the INTO/OUT
laundering rules, and the placebo-precedent family prevented all five.

Laundering directions named: INTO — nothing; no intensity function or
its shape, no rho ratio, no theta or theta_reinit value, no mechanical
volatility ceiling, no execution probability, no impact profile, no
AES normalization, no symmetric-intensity convention, and no
invariant-distribution exhibit from this paper enters any spec,
default, calibration, tolerance, cost assumption, or generative null;
the one thing this paper licenses into the pending state is the
dynamics-identification rule, queued as PENDING OWNER RATIFICATION and
inert until ratified. OUT — never read backwards as "order flow is
state-driven, memory is irrelevant" (the conditioning set excludes
flow history by construction, PDF p. 22), "only a third of volatility
is mechanical" (venue-, grain-, and model-relative ceiling), "the
book's shape validates queue models" (statics do not identify
dynamics, PDF p. 10), or "impact has no relaxation" (model property of
the Markovian class, PDF p. 22).

## Standing caveat

Two large-tick Euronext equities, one brokerage's 5-limit feed, 27
months, auction hours trimmed; K = 3 limits with the fourth and fifth
assumed similar to the third; order sizes collapsed to
average-event-size units; all intensities functions of current state
only, formally memoryless; the reference price itself an estimate with
a tie-break convention; theta and theta_reinit calibrated on two
10-minute statistics of a single stock; the exogenous-information
mechanism a reinitialization lottery, not a modeled news process;
market orders at non-best limits admitted as rare; cross-limit market
orders decomposed into sequential pseudo-events; Assumptions 3-4 known
false in one direction. arXiv v2, 2013 index year; published version
and any journal-revision differences NOT checked at reading, uncertain
until verified.
