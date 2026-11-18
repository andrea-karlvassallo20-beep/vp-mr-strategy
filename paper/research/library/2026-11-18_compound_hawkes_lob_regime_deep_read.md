# Library deep-read session 26 — Swishchuk, Remillard, Elliott &
# Chavez-Casillas, "Compound Hawkes Processes in Limit Order Books"
# (arXiv:1712.03106v1, 2017; Calgary/HEC/Adelaide; compound and
# regime-switching compound Hawkes price processes, with diffusion
# limits)

Read 2026-11-18, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/xbf2516_compound_hawkes_processes_in_limit_order_books.txt`,
~14 pp., page-marked). Next UNREAD triage-rank entry (score 33;
verified unread by the read-slug mapping). Bibliographic note for
the shelf: this is the 2017 foundational paper of the line the
program already carries — session 16 deep-read the later Swishchuk-
Huffman "General Compound Hawkes Processes in Limit Order Books"
(arXiv:1812.02298, whose first author and program are the same) and
the session-17 simulator read is the 12D descendant; the present
paper is where the CHP/RSCHP diffusion limits were first stated.

## The paper in one paragraph

Two new objects are defined and given LLNs and functional central
limit theorems: the Compound Hawkes Process (CHP) — a one-
dimensional Hawkes process N(t) whose jump times carry marks X_k
from an ergodic two-state continuous-time Markov chain on
{-delta, +delta}, the fixed tick (price changes that are
DEPENDENT, not i.i.d.) — and its Regime-Switching compound
extension (RSCHP), where the Hawkes BACKGROUND intensity itself
switches with an N-state Markov chain Y_t, which the authors
interpret for LOBs as high/normal/low BOOK IMBALANCE states
(PDF pp. 5-7). The headline result is the diffusion limit
(Theorem 1): the tick-time price process satisfies
S_nt - N(nt) s* ~ sqrt(n) -> sigma * sqrt(lambda/(1 - mu-hat)) W(t),
where mu-hat = integral of the excitation kernel, s* = delta(2pi* -
1) is the stationary mean mark, and sigma^2 depends on the mark
chain's transition probabilities (PDF pp. 8-9, eqs. 16-18); the
RSCHP version replaces lambda by the regime-weighted average
lambda-hat = sum p*_i lambda_i (Theorem 2, PDF p. 11). A corollary
extends the FCLT to general point processes, noting the price's
limiting variance splits into a mark-channel term and an
arrival-counting channel term (PDF pp. 10-11).

## Findings, graded (does any kill line move?)

**NO kill line changed. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand:

1. **[reinforcing, no new item] The 1/(1 - mu-hat) amplification
   pre-dates the session-16 citation — and here it is stated in
   its cleanest form.** The diffusion-limit volatility is
   proportional to sqrt(lambda/(1 - mu-hat)): as the excitation
   kernel's integral mu-hat approaches one (near-criticality), the
   long-grain volatility inflates by exactly the branching-
   structure factor (PDF pp. 8-9, eq. 16, Remark 6 for the
   exponential kernel mu-hat = alpha/beta). This is the same
   two-channel decomposition session 16 recorded (arrival-rate
   channel x mark channel) and the same near-critical inflation
   the queue-reactive null's ergodicity warrant (session 13)
   bounds; the citation moves the origin of that structure back to
   this 2017 statement. Nothing queued — the existing
   recordings and the never-read-branching-alone family already
   force the multi-reading format.

2. **[reinforcing, no new item] Regime-switching arrival rates
   with imbalance interpretation — the latent-regime line gains
   its Hawkes-side antecedent.** The RSCHP's switching background
   intensity <lambda, Y_t> is explicitly interpreted as
   high/normal/low imbalance driving the arrival rate, with
   regimes averaging into lambda-hat = sum p*_i lambda_i in the
   limit (PDF pp. 7, 11). The consequence the program already
   carries from the latent-regime read: a FITTED stationary
   background intensity is an ergodic-probability-weighted average
   over unobserved regimes — it is a mixture object, and window
   mixtures across regime compositions silently change its
   meaning. Reinforces the regime-conditional recording
   discipline; the diffusion limit itself is the formal statement
   that the mixture collapses to a single number only under
   stationarity of Y_t.

3. **[interpretation caution] The mark chain's dependence is
   priced into the long-grain volatility — independent-tick
   shortcuts are wrong in a computable direction.** The variance
   formula sigma^2 = 4*delta^2(...(p, p', pi*)) shows the long-grain
   volatility depends on the mark chain's transition probabilities
   through a non-trivial expression that reduces correctly to the
   i.i.d. case only at independence (PDF pp. 8-9, eq. 18).
   Interpretation language only: price-change marks dependent
   through an order-flow mechanism (e.g., runs of same-side
   changes) change the effective variance per event — any future
   variance-per-event or tick-scaling arithmetic on gated windows
   that assumes independent marks is a specification whose bias
   direction this formula makes computable in principle. Recorded
   as a caution; nothing measured, nothing queued.

4. **[source-quality note] Foundational-but-early: definitions
   and limits, thin numerics, LOB aspiration more than LOB
   evaluation.** The numerical section is small and the LOB
   connection is by interpretation (fixed tick, two-valued marks
   — a large-tick equity picture, the mirror image of the
   program's small-tick venue). The marks chain being INDEPENDENT
   of the Hawkes process (Definition 5) is a modeling
   simplification the later literature itself relaxes. arXiv v1,
   December 2017; a published version may exist — check before
   formal citation. Quote for the diffusion-limit structure, not
   as venue facts.

## What this paper would have killed if we had done it wrong

If any future variance-rescaling or tick-scaling arithmetic had
treated per-event price marks as independent and the arrival
process as a free-standing intensity, this paper's two-channel
variance formula is the closed-form demonstration that BOTH
channels — the mark-chain dependence structure AND the
1/(1 - mu-hat) arrival inflation — enter the long-grain
volatility, and omitting either misprices the scaling in a
computable direction. And if a fitted background intensity from
gated windows had ever been read as a venue constant, the
regime-switching half of the paper is the formal statement that it
is an average over hidden regime weights, not a parameter of the
market. Both failures are precluded by the existing
construction-declaration and regime-conditional discipline; the
paper reinforces, changes nothing.

## Standing caveat

Large-tick two-state-mark idealization (Cont-Larrard's fixed-tick
world, not a small-tick perp venue); marks independent of the
Hawkes process by construction; stationarity assumed for the
regime chain (the ergodic probabilities p* are load-bearing);
mu-hat < 1 strictly (subcritical only — the near-critical
amplification is an approach statement, not a criticality claim);
numerical section illustrative only; arXiv v1 2017, check for a
published version before formal citation. No execution content; a
limit-theorem paper; nothing to operationalize; the program never
trades live.
