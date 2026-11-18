# Deep-read session 16 — Bergault, Bertucci, Bouba, Guéant & Guilbert, "Price-Aware Automated Market Makers: Models Beyond Brownian Prices and Static Liquidity"

Null-time session 18 (deep-read 16, offset honored). Philippe Bergault (Université Paris Dauphine-PSL),
Louis Bertucci (Institut Louis Bachelier), David Bouba (Swaap Labs), Olivier Guéant (Université
Paris 1 Panthéon-Sorbonne) and Julien Guilbert (Swaap Labs); arXiv:2405.03496v3 [q-fin.TR],
18 May 2024 (PDF p. 1). A pure-theory stochastic-control paper deriving Hamilton-Jacobi-Bellman
equations and quadratic-Hamiltonian approximations for the optimal quoting markup of a
price-aware automated market maker, under four price models (Heston-Bates, Stein-Stein with
jumps, a linear Markovian Hawkes jump model, and Z-Hawkes/quadratic Hawkes) and two
liquidity models (Hawkes intensities, rejected for control; Markov-modulated Poisson
processes, adopted as the tractable alternative).

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8 faster, or change
their kill lines? Source: legally acquired OA copy
(docs/library/text/xd1af5a_price_aware_automated_market_makers_models_beyond_.txt, 21 pp.,
page-marked). Triage trace: this is the queue's next UNREAD triage entry (score 39), read
as the standing-pointer read of this session. With the session-9 triage-audit flag on record,
rank is a candidate reading; the owner's library policy governs when rank and quality diverge.

## The paper in one paragraph

The paper extends the price-aware AMM quoting framework of Bergault, Bertucci, Bouba &
Guéant (ref. [6], PDF p. 2) beyond log-normal prices and static liquidity: for each price
model it writes the market maker's expected-excess-PnL-over-Hodl objective (Eqs. 1-2,
PDF pp. 4-5), derives the HJB equation for the value function in the state variables
(spread-to-Hodl y plus the price-model state: instantaneous variance for Heston-Bates,
instantaneous volatility for Stein-Stein, intensity for the Hawkes model, the pair (h, xi)
for Z-Hawkes; PDF pp. 6-15), and shows that a quadratic approximation of the
Hamiltonian functions reduces each to a triangular system of low-dimensional PDEs solvable
by implicit schemes (Eqs. 8, 16, 24, 32; PDF pp. 8, 10, 13, 15). For liquidity, Hawkes-type
intensities driven by the market maker's own transactions are shown to blow up the value
function's dimensionality (three to five state variables) and to break the quadratic
approximation "due to simultaneous jumps in both the y variable and the intensity variables"
(PDF p. 17); the authors adopt instead Markov-modulated Poisson processes with p = 2-3
discrete liquidity states per side and a rate matrix Q (Sec. 4.3, PDF pp. 17-19). "No data
involved in this study" (PDF p. 20): there is no empirical estimation, no calibration, and
no backtest anywhere in the paper.

## Findings, graded (does any kill line move?)

NO kill line changed. NO new candidate sharpening.

1. [reinforcing, no new item] The branching-ratio interpretation is used as a plain input,
   not a finding: the paper's linear Hawkes price model carries the intensity dynamics
   dlambda = -beta(lambda - lambda_inf) dt + beta n J(dt, d eta) with "n in (0, 1)
   corresponding to the percentage of price moves that are purely endogenous" (Sec. 3.4,
   PDF p. 11) — the Filimonov-Sornette endogeneity-share reading, taken as a fixed model
   parameter in an application context. This corroborates that the field reads n as the
   endogeneity share by default, which is exactly why the queued estimator-discipline items
   (the estimator-at-scale-W rule with its mean-variance cross-check, the bootstrap-CI and
   boundary-solution rules, the W-ladder) exist: the interpretation is standard; the
   estimation is where the trigger is won or lost, and this paper contributes nothing there
   (no estimator, no data). Nothing added to any queue.

2. [reinforcing, no new item] The exponential kernel's honest label, from the control
   literature itself: "Power law kernels may be more realistic than exponential ones, but
   they do not lead to Markovian setups" (footnote 8, PDF p. 11). The exponential kernel is
   adopted for tractability, not realism — the paper's own sentence. This is first-principles
   support for the queued ACF-shape kernel-validity gate (deep-read 12): the gate exists
   precisely because the kernel form is a computational convenience that the gated data must
   be given a chance to reject, and it reinforces the deep-read-9 caution (kernel family
   declared with the spec, before data). Nothing added: the gate is already queued, pending
   owner ratification; this citation strengthens its motivation and does not extend it.

3. [reinforcing, no new item] The Z-Hawkes section names the sign-feedback alternative
   family: the quadratic Hawkes model (Blanc, Donier & Bouchaud, ref. [10], PDF pp. 13-14)
   adds an intensity driver xi_t whose increments are proportional to sign(eta) (Eq. on
   PDF p. 13) — the Zumbach channel, i.e. past SIGNED moves raising future intensity —
   which a linear exponential-kernel Hawkes cannot represent by construction. The queued
   kernel-family control (library ritual paper 2, pre-condition 2) already carries this
   scope: the branching reading must survive a pre-declared kernel-family check. This paper
   names the sign-feedback family concretely for that control and provides zero empirical
   grounds to prefer it on our gated data; no new item is earned.

4. [interpretation caution] The curse-of-dimensionality verdict on Hawkes liquidity models
   (Sec. 4.2, PDF pp. 16-18) is a CONTROL-THEORETIC statement, not a statistical one: the
   rejection is about the solvability of a quoting-optimization HJB (value functions with
   three to five state variables; the quadratic approximation failing under simultaneous
   jumps in y and the intensities, PDF p. 17), in a problem where the market maker chooses
   markups inside the feedback loop. It licenses NO claim that Hawkes processes are unusable
   for MEASUREMENT — C8's branching-ratio trigger estimates an intensity process and reads
   endogeneity from it; it solves no HJB and never quotes. Reading this paper as
   "the field abandons Hawkes" would import a tractability judgment from a different problem
   class onto the trigger layer. Likewise the MMPP alternative (p typically 2 or 3
   liquidity states, PDF p. 17; footnote 12, PDF p. 16: deterministic intraday patterns
   "can be incorporated without increasing modeling complexity") is a control-side
   discretization convenience, not a regime-measurement result, and the program's
   hour-of-day stratification already stands on its own measurement citations.

5. [interpretation caution] A price-aware AMM manufactures part of its own flow
   endogeneity: the arrival intensities are functions of the markup policy (Eqs. on
   PDF p. 4), and the optimal markups react to the state (inventory y, estimated
   intensity/volatility; Eqs. 25-26, 33-34, 44-45, PDF pp. 13, 15, 19), so on an
   AMM-quoted venue a share of measured clustering is the quoting algorithm's control
   loop, not trader reflexivity. C1-L2 and C8 run on order-book (Tardis LOB) data, so this
   contaminant is NOT in the gated data; the caution binds only if the programme's venue
   scope ever widens to AMM/on-chain pools: a branching-ratio reading on such a venue would
   need the quoting loop separated from trader excitation before it could be read at all.
   Per the standing rule, the quoting machinery itself is execution-strategy engineering:
   recorded as context, never operationalized; nothing trades live.

6. [source-quality note] arXiv v3; "No data involved in this study" (PDF p. 20); two of
   the five authors are members of the Swaap Labs team and the research program is funded
   "in partnership with Swaap Labs" (PDF pp. 1, 20) — an industry-motivated paper whose
   conclusions favor model sophistication for the quoting layer its funder sells; the
   paper's own conclusion honestly states the model choice is a per-pair developer trade-off
   (PDF pp. 15, 19-20). Two typographical defects observed in the equations: the
   Stein-Stein approximate PDE's jump integral carries the state variable nu where sigma is
   meant (Eq. 15, PDF p. 10), and the linear-Hawkes HJB duplicates the Hamiltonian symbol
   H^{1,0}H^{1,0} (Eq. 20, PDF p. 11) — cosmetic, but the equations cannot be transferred
   without re-derivation. Check the published version before formal citation.

## What this paper would have killed if we had done it wrong

Two laundering directions, both named. First: the paper's rejection of Hawkes liquidity
models for control (Sec. 4.2) could have been quoted as an authority to demote C8's Hawkes
trigger machinery — an appeal-from-the-wrong-problem-class that would have weakened a test
on the basis of a solvability result for quoting HJBs the trigger never solves. The
discipline that prevented it: the library is ammunition, not evidence, and a no-data
control paper carries no empirical claim for any program purpose. Second: the paper's
matter-of-fact use of n as "the percentage of price moves that are purely endogenous"
(PDF p. 11) could have been cited as license to read a 0.8-threshold crossing as market
reflexivity, unguarded — when in fact the queued estimator-at-scale-W rule, the
bootstrap-CI and boundary-solution rules, and the W-ladder exist precisely because the
branching reading is estimator- and scale-dependent and the queue has testimony that the
estimator can move the reading across the threshold without any parameter change. A third,
smaller counterfactual: the MMPP liquidity machinery could have tempted a "liquidity-regime
feature" into C1-L2's family straight from the control literature; the no-empirical-import
rule blocks it — a feature with no evidence chain carries no claim.

## Standing caveat

The paper is quoting-strategy engineering: five HJB systems, approximation methods, and
per-pair model-choice guidance for price-aware AMM design. Nothing in it is measured
against data, by its own statement (PDF p. 20). Its Hawkes content is control-side (the
Markovian setup requires the exponential kernel, footnote 8, PDF p. 11 — the same
tractability-forced kernel family as C8's trigger fit, which is why the ACF-shape gate's
motivation gains this citation, no more). Its liquidity content is a tractability verdict
and a discretization choice, not regime evidence. Applicability boundary: two-currency
AMM pools with nonnegative inventory and a Hodl benchmark (PDF pp. 2-3, footnote 1,
PDF p. 2) — not order-book markets; nothing here transfers to the C1-L2 venue except the
abstract point that quoting algorithms inside the flow loop alter what "endogenous" means
on their venues. arXiv-version caution: v3 is not the published record; check before any
formal citation.
