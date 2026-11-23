# Deep-read session 104 — Taranto, Bormetti & Lillo (2014), "The adaptive nature of liquidity taking in limit order books"

Authors: Damian Eduardo Taranto, Giacomo Bormetti, Fabrizio Lillo. Venue:
arXiv:1403.0842v2 [q-fin.ST], 11 Apr 2014, submitted to JSTAT (PDF p. 1). One
clause on what it is: an empirical-mechanistic microstructure paper that
dissects asymmetric liquidity (a more probable trade sign impacts less)
into taker-side and provider-side components on four mega-liquid stocks,
then builds a statistical order book model in which the liquidity taker's
volume rule adapts to the local predictability of order flow, restoring
diffusive prices at all time scales without parameter fine tuning.

Read 2026-11-24, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x1e5f02_the_adaptive_nature_of_liquidity_taking_in_limit_o.txt,
~40 pp., page-marked). Next UNREAD triage-rank entry (score 20, fourteenth
of the score-20 tier, its LAST entry).

## The paper in one paragraph

The empirical half dissects asymmetric liquidity on AZN and VOD (LSE,
all of 2004, full order book events) and AAPL and MSFT (NASDAQ,
July-August 2009), spanning small-tick and large-tick stocks (Table 1,
PDF p. 7). The order sign process is modeled as DAR(p), p fixed at 500
after MSE insensitivity checks (Table 2, PDF p. 8; predictor and
forecast formulas in Appendix A, PDF pp. 37-39), giving the sign
predictor ℇ̂_n; trade returns are split into a mechanical component
(order penetrates the opposite best) and a quote-revision component
(all limit orders and cancellations between trades), r = r^M + r^Q
(PDF p. 13). The printed mechanism: the mechanical impact is
approximately the penetration probability times half the gap,
r^M(ℇ̂) ≈ (w/2)·δ·g(ℇ·ℇ̂) — eq. 3's empirically validated approximation
(PDF pp. 14, 17-18, Figure 8) — and when predictability-correctness
ℇ·ℇ̂ rises, the probability that a trade moves the mid drops: takers
shrink market order volumes to the outstanding opposite liquidity,
the opposite-best volume first erodes then refills very close to
ℇ̂ = ±1 (Figures 4, 6, 7; PDF pp. 10-17), the quote revision acts in
the SAME direction as the mechanical impact at moderate correctness but
shrinks toward zero at extreme correctness (so providers reinforce, not
restore, efficiency there; PDF pp. 17-19). The efficiency-recovery
measure: the transaction-level inefficiency condition eq. 4 holds in
regions for the NASDAQ stocks (MSFT "clearly inconsistent with market
efficiency", PDF p. 19) and vanishes after s trades: AAPL 5 lags
(5.5 s), MSFT 11 lags (18.7 s), AZN 1 lag (23.1 s), VOD 5 lags
(114.5 s) — the 2009 NASDAQ stocks need MORE trade lags but LESS
physical time than the 2004 LSE stocks to restore efficiency: "high
frequency trading decreases the physical time needed to restore
efficiency in the market, but it might increase the trade time"
(PDF p. 22). The modeling half: the Toth et al. (2011) model recovers
diffusivity only below the limit-order lifetime ν^-1 and only under
unrealistically low cancellation rates (latent-book), where the
conditional volume profile takes the WRONG sign versus data (PDF
pp. 23-26, Figure 11); the authors' fix keeps the zero-intelligence
book but draws market order volume as a fraction f of the opposite-best
volume from a beta law whose exponent depends on the predictability,
g(ℇ·ℇ̂), chosen so the penetration probability is α(1−ℇ·ℇ̂), which
makes the reduced return model r = A(ℇ−ℇ̂)+η exactly
martingale-efficient and diffusive at ALL lags (eqs. 5-6 and the
variance computation, PDF pp. 26-29), with equivalence to the
propagator model under the AR predictor (PDF pp. 28-29). Under the
PUBLIC DAR(p) predictor diffusivity holds only for lags below the
predictor window (σ(ℓ) constant for ℓ < p; Figure 13, PDF p. 34),
while under the PRIVATE metaorder-aware predictor (the LMF
continuation probability ℇ̂ = s_n·π·P_m, eq. 9; PDF pp. 30-33)
diffusivity holds at all scales, insensitive to parameters (Figure 12,
PDF p. 33). Model outputs reproduce the measured conditional volumes,
penetration, fraction, and impact profiles (Figure 14; PDF pp. 34-36).

## Findings, graded (does any kill line move?)

NO kill line changed. ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The generative-null
   agent information-set pre-declaration: BEFORE the L0 gate, any
   C1-L2/C8-adjacent generative null, placebo, comparator or simulator
   whose simulated participants (takers, makers, adversarial responders,
   strategies) act on a decision rule fed by any input — signs,
   predictors, flow histories, metaorder or participant state — must
   pre-declare, as frozen configuration counted in the multiplicity
   ledger, for each simulated agent class: (i) the information set its
   rule consumes, with every input marked PUBLIC (derivable from the
   public observables the null itself simulates) or PRIVATE (not so
   derivable: agent-internal state, metaorder continuation knowledge,
   the knowing-taker assumption), and (ii) which macro-level outputs of
   the simulation are claimed invariant to that marking and which are
   information-set-dependent, with every deviation a dated amendment
   before any data is touched — harder-to-pass because a generative
   null whose agents silently consume private information today passes
   as an ordinary null while its produced macro properties are
   artifacts of the choice, and the claim-refutation pair rides on it:
   the Taranto-Bormetti-Lillo model proves the failure class in print
   on itself with nothing changed but the takers' predictor — the
   public DAR(p) predictor bounds the simulated price's diffusivity to
   lags below the predictor window (σ(ℓ) constant for ℓ < p, shown at
   p = 500 and p = 10000, Figure 13, PDF p. 34) while the private
   metaorder-aware predictor gives diffusivity and informational
   efficiency at all scales, "by construction", insensitive to
   participation π and δ (Figure 12 with the text at PDF p. 33) — the
   same simulator, same rates λ, µ, ν, same grid, different agent
   information set, qualitatively different macro property, and the
   authors themselves mark the private predictor as "not typically of
   public domain" (PDF p. 32). No queued rule asks the question: the
   impact-viability pre-declaration for generative nulls (deep-read
   87) audits the impact parameterization's pointwise sign conditions
   and says nothing about what its agents know; the
   dynamics-identification rule for generative nulls (null-time
   session 58) demands the dynamics be identified, not the agents'
   inputs declared; the queue-jump-diffusion generative-null
   pre-declaration (queued ## 107) freezes null parameters, not
   agent inputs. Tightens the impact-viability pre-declaration
   (deep-read 87) by extending the generative-null pre-declaration
   family from parameterization viability to agent information sets,
   and joins the estimator-discipline queue (B17, deep-read 103) in
   closing a researcher degree of freedom that alone can manufacture a
   macro-level conclusion.
2. [reinforcing, no new item] The impact decomposition is ammunition
   for the C8 covariate/mechanism shortlist, never program evidence:
   mechanical impact ≈ penetration probability × gap/2 (eq. 3,
   validated, PDF pp. 14, 17-18) separates the mechanical from the
   provider-revision channel at transaction grain, and the paper
   prints which stocks' regimes violate the transaction-level
   efficiency condition with recovery horizons in both trade lags and
   physical seconds (PDF pp. 19-22). The trade-time-versus-physical-time
   inversion (the 2009 NASDAQ stocks restore efficiency in less
   physical time but MORE trade lags, PDF p. 22) is temporal-theory
   context for the flow-clock scale-constant discipline already queued:
   efficiency restoration is measured at trade-count grain, so any
   future cross-era comparison must state its clock. No queue change.
3. [interpretation caution] The efficiency-restoring role is assigned
   by the measurements to the TAKER adaptation, not to providers: the
   quote-revision component moves in the same direction as the
   mechanical impact for moderate correctness (reinforcing the price
   move, not counteracting it), vanishing only at extreme correctness
   (PDF pp. 17-19), and the model restores efficiency wholly inside
   the market-order rule (PDF p. 26). Any future C1-L2/C8 narrative
   that assigns efficiency restoration to market makers or to
   stimulated refill must trace to a measured component, not an
   assumed law — the same "markets respond as if" discipline recorded
   at deep-read 101. No queue change.
4. [interpretation caution] The private predictor at the model's core
   lets the simulated taker consume structurally defined but
   non-public knowledge (her own metaorder's continuation probability,
   PDF pp. 31-33) — exactly the class of assumed information the
   information-set pre-declaration of finding 1 would force any future
   simulator to declare. Read jointly with finding 1: the finding is
   not that private information is illegitimate, but that the choice
   is a load-bearing configuration that cannot be silent. No queue
   change.
5. [source-quality note] arXiv v2 [q-fin.ST], 11 Apr 2014, "Submitted
   to: JSTAT" (PDF p. 1), 40 pages, zero citations recorded in the
   index; four mega-liquid stocks across two venues and eras — a
   construction whose breadth is real but whose n is four; the NASDAQ
   inefficiency regions are flagged by the authors themselves as
   regime-dependent with deviations "in a region scarcely populated"
   (PDF p. 15); the DAR(p) estimation smooths negative fitted
   coefficients with a ten-point moving average before zeroing them
   (Appendix A, PDF p. 39), an estimator-side preprocessing any reuse
   must carry. Check the published JSTAT version before formal
   citation. No queue change.

## What this paper would have killed if we had done it wrong

Without finding 1's pre-declaration, a future C8 generative null could
claim "no null reproduces the measured compression signal" while its
simulated takers silently ran on a private-information rule, or
conversely claim "a null reproduces everything" while its agents ran on
a truncated public predictor — either conclusion manufactured by an
undeclared agent information set, with no visible fingerprint in the
outputs and the refutation carrying the artifact. The matched-control
and pre-declaration discipline avoids precisely this. Without the
impact-decomposition caution the paper's taker-side efficiency
narrative would enter the record as a market fact about who restores
efficiency, when it is a four-stock conditional association whose
provider-side model extension the authors themselves leave as future
work (PDF p. 37). And without the clock discipline already queued, the
paper's cross-era efficiency-recovery comparison (2004 LSE vs 2009
NASDAQ) would read as a measured improvement in market quality rather
than what it is: the same restoration measured in two different clocks
with opposite orderings.

## Standing caveat

Everything above is the arXiv v2 text (40 page-marked PDF pages: header,
body, all fourteen figures, the DAR(p) appendix, references complete;
nothing skipped; Figure 3's raw axis text partially garbled in the
extract but its content is stated in the accompanying text, PDF
pp. 8-9). The empirics are four mega-liquid stocks; the model is a
large-tick construction whose small-tick extension is asserted, not
built; the metaorder-aware predictor assumes the simulated taker knows
her continuation law exactly, a modeling convenience rather than a
measured behavior. Nothing here licenses any C1-L2 or C8 claim: the
paper is ammunition for mechanism decomposition and null design, not
evidence. Check the published JSTAT version before formal citation.

Nothing measured during this session. No kill line moved. Nothing armed.
Nothing trades live.
