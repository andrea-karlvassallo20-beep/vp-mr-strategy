# Deep-read session 35 — Swishchuk, Remillard, Elliott and Chavez-Casillas, "Compound Hawkes Processes in Limit Order Books"

Library deep-read session 35 (null-time session 39, log entry ## 43).
Session numbers taken fresh from the log tail at append time, per the
founding convention: two parallel slots landed first, after this note
was drafted, as deep-read session 33 (null-time session 37, log entry
## 41, TradeFM) and deep-read session 34 (null-time session 38, log
entry ## 42, the Hawkes liquidity-migration diffusive-limit paper,
which also consumed this note's drafted next-pointer x5db64b), so
this session renumbered from 33/37/## 41 to 35/39/## 43; the note
text below otherwise stands as drafted.
Anatoliy Swishchuk (University of Calgary), Bruno Remillard (HEC
Montreal), Robert Elliott (University of Calgary and University of
South Australia) and Jonathan Chavez-Casillas (University of
Calgary), arXiv:1712.03106v1 [q-fin.MF], 7 December 2017, 24 pp.
text extract, page-marked. A theoretical working paper that defines
a compound Hawkes process (CHP) and a regime-switching compound
Hawkes process (RSCHP) for limit-order-book mid-prices and proves
Laws of Large Numbers and diffusion limits for both, with a small
five-day CISCO calibration.

Read 2026-11-19, against ONE question: what here would kill C1-L2
or C8 faster, or change their kill lines? Source: legally acquired
OA copy
(docs/library/text/xbf2516_compound_hawkes_processes_in_limit_order_books.txt,
24 pp., page-marked). Assigned triage-rank entry (score 33,
xbf2516). Selection note, recorded honestly: this entry sits at
triage rank 22 and carries no prior deep-read note; the session-27
next-pointer (score 32, x947263) and every subsequent pointer
through session 32 (score 31, TradeFM) jumped over it without a
recorded skip, so this session consumed the mechanical rule's next
UNREAD entry and left the session-32 pointer text unedited per the
honest-error protocol; the landed parallel deep-read session 33
consumed the stale session-32 pointer (TradeFM) without recording
the skip either, so this session's correction covers both. Next
UNREAD triage-rank entry (score 30, xd08813, "A Microstructural
Foundation for the Rough Hawkes Heat Kernel"); the liquidity-
migration entry the previous draft named was consumed by the parallel
session that landed as log entry ## 42.

## The paper in one paragraph

The paper introduces two constructions: the CHP, a mid-price
St = S0 + sum over N(t) of per-event price changes Xk drawn from an
ergodic continuous-time two-state Markov chain on {minus-delta,
plus-delta}, with N(t) a one-dimensional Hawkes process
(Definition 5, Eq. (10), PDF p. 5); and the RSCHP, the same compound
sum driven by a regime-switching Hawkes process whose background
intensity lambda_t = <lambda, Y_t> can vary with an N-state ergodic
Markov chain Y_t, motivated by a three-state high/normal/low
imbalance reading (Definition 6, Eqs. (13)-(14), PDF pp. 6, 11,
with the general regime-dependent kernel <mu(t), Y_t> admitted at
Eq. (13)). For the CHP the paper proves a diffusion limit
(S_nt minus N(nt)s-star)/sqrt(n) converging to
sigma*sqrt(lambda/(1-mu-hat))*W(t) with s-star and sigma given by
the Markov chain's ergodic and transition probabilities and the
tick (Theorem 1, Eqs. (16)-(18), PDF pp. 8-9) and a corresponding
LLN (Lemma 1, Eq. (26), PDF pp. 9-10), plus a corollary extending
both to general point processes under stated assumptions C1-c3,
adding a point-process variance term sigma-tilde (PDF pp. 10-11).
Analogous limits hold for the RSCHP with the single change that the
background intensity lambda is replaced by the stationary-weighted
lambda-hat = sum_i p-star_i lambda_i (Theorem 2, Eqs. (31)-(32),
PDF pp. 11-12; Lemma 2, Eq. (40), PDF p. 13). Numerically the
authors estimate the CHP on five days of CISCO (3-7 November 2014)
and present the volatility identity as a way to compute price
volatility from order-flow parameters "without observing the price
at all" (PDF pp. 13-14), reporting an estimation error of
approximately 0.08 comparing the two sides of Eq. (16)
(0.07617229 and 0.07980041 under two sampling choices, PDF pp.
16-17), and a two-state regime implementation splitting lambda
around its mean with a claimed error of at most 0.0055 on
lambda-hat (PDF p. 21).

## Findings, graded

NO kill line changes. NO new candidate sharpening.

1. **[reinforcing, no new item]** The kernel enters every one of
   the four limits only through its integral: mu-hat =
   integral of mu(s) ds strictly below one with finite first
   moment (Eq. (17), PDF p. 8), so the exponential kernel appears
   as mu-hat = alpha/beta (Remarks 5, 6, 8, 9, PDF pp. 9-10, 12-13)
   and every fitted kernel shape is summarized at diffusion scale
   by a single constant. This is the aggregation face of the
   kernel-form interpretation caution recorded through deep-read
   session 32: fitted decay shapes carry no information that
   survives averaging, so no kernel-shape observation from any
   single paper can ever be cited as expected behavior of a
   coarse-scale statistic; the programme's existing rule already
   says it. No parameter, no shape, no constant transfers.

2. **[reinforcing, no new item]** The regime-switching limit differs
   from the plain limit by exactly one substitution: the background
   intensity appears as the stationary-probability-weighted
   lambda-hat = sum_i p-star_i lambda_i (Eq. (32), Theorem 2, PDF
   pp. 11-12), the regime chain's transition dynamics vanish at
   scaling, and the diffusion-limit family is otherwise unchanged.
   Read discipline for the pending queue-state conditioning rule
   (deep-reads 26 through 32, all PENDING OWNER RATIFICATION), and
   it only sharpens how such readings are interpreted, nothing
   else: a conditioning state that merely reweights stationary
   intensities changes a scale constant, while conditioning that
   changes the excitation itself lives in the general
   form <mu(t), Y_t> of Eq. (13) (PDF p. 6), and any future
   regime-conditioned reading must say which of the two it claims
   before it is estimated, precisely because the former is
   invisible in the scaling limit. The paper's three-state
   imbalance interpretation (PDF p. 11) is motivation prose, not
   evidence, and never transfers.

3. **[interpretation caution]** The claim that price volatility may
   be computed from order-flow parameters "without observing the
   price at all" (PDF pp. 13-14) holds only inside the paper's own
   tick-world: fixed tick delta with two-valued Markovian
   increments {minus-delta, plus-delta} (PDF p. 7), a
   one-dimensional event count, and stationarity. It is never
   cited as an expected property of the programme's venue (where
   price jumps span multiple ticks and the mid is not a
   plus-or-minus-one-tick chain), never as a volatility estimator
   candidate for any arm, and never as support for any cost or
   calibration assumption.

4. **[interpretation caution]** The numerical section is five days
   of one stock (CISCO, 3-7 November 2014) with no out-of-sample
   component, and the headline "error approximately 0.08" is a
   descriptive mean of squared standard-deviation gaps between the
   two sides of Eq. (16) under two sampling choices (0.07617229,
   0.07980041), not a hypothesis test, with standard errors
   reported for the sample standard deviations only (PDF pp.
   14-17). The 1000-simulation quantile plots are drawings from
   the fitted model, not forecasts checked against realization
   (PDF pp. 19-21), and the RSCHP check is a two-state split of
   lambda around its average with the claimed error bound stated
   only for lambda-hat (0.02688 against fitted lambdas, error at
   most 0.0055, PDF p. 21). Nothing here is evidence that any
   statistic of any market the programme measures behaves as the
   theorem says, and nothing numerical transfers.

5. **[source-quality note]** arXiv v1, December 2017, in
   working-manuscript condition: a literal unresolved bracketed
   citation "[?]" survives on PDF p. 4, references carry typos
   ("Daley and Vee-Jones, 2010", PDF p. 9; "Fillimonov", PDF
   p. 23), the displayed equation numbering jumps from (4) to (10)
   within Section 2, and the proofs rest on the martingale method
   of Swishchuk and Vadori (2015) invoked without reproducing it
   (PDF pp. 8, 12). Robert Elliott and Bruno Remillard are
   established stochastic-process researchers; the paper is the
   direct precursor of the Swishchuk and Huffman general compound
   Hawkes process read at deep-read session 14, one branch of the
   same Calgary program, and it inherits neither more nor less
   authority than a v1 preprint. No journal record was checked at
   reading; the published version is to be checked before any
   formal citation. Graded as a modest theoretical stepping-stone
   read at exactly that level.

## What this paper would have killed if we had done it wrong

If any future specification had lifted the closed form
sigma*sqrt(lambda/(1-mu-hat)) as an assumed price law on the
programme's venue, the programme would have imported the fixed-tick
plus-or-minus-delta world silently inside a volatility
calculation, exactly the costume failure K1 exists to catch; the
record's venue-specificity rules and the session-14 note on the
sibling paper were already in place to make that inadmissible. If
the regime-switching limit had been read as evidence that regime
conditioning "works", a spec could have smuggled in conditioning
invisible to scaling as if it were structure; finding
3 forecloses that by demanding the stationary-reweight-versus-
excitation-form declaration before estimation. And if the paper's
headline error figure had entered the record as a validation, the
programme would have booked a five-day, one-stock, in-sample
descriptive average as evidence; the checklist's own economic and
statistical validity gates were what kept it out. Nothing was
measured, so nothing needed killing: the session consumed the
pointer-chain error (rank 22, skipped by pointers from deep-read 27
onward and not recorded by the parallel session either) and
corrected the next-read discipline without touching any
past text.

## Standing caveat

Everything is proven inside the fixed tick, two-state
plus-or-minus-delta price-change world with a one-dimensional
Hawkes event count and stationary branching; the data exercise is
five days of CISCO, November 2014, regular-hours NASDAQ trading,
one stock. No crypto, no BTCUSDT, no perpetual futures, no
floating-tick venue appears anywhere. Laundering directions named.
INTO: the stationary-weighting-only substitution of the
regime-switching limit may enter strictly as read discipline for
already-queued conditioning rules (declare stationary reweighting
versus excitation-form change before estimation); the kernel
enters scaling only through mu-hat may enter strictly as an
existing-reinforcing observation; no lambda, alpha, beta, tick,
error figure, volatility coefficient, or quantile-plot property
from the CISCO section enters any spec, default, or calibration.
OUT: the volatility-without-price claim, the error of
approximately 0.08, the lambda-hat of 0.02688, the imbalance
three-state interpretation and every closed form in Eqs. (16),
(26), (31), (40) are never cited as expected behavior of any
market the programme measures, never as expected BTCUSDT
behavior, and never as support for any edge, cost, or volatility
assumption in any arm.
