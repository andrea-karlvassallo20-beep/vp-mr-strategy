# Deep-read session 86 — Boltzmann Price (Rola, 2025)

**Library deep-read session 86 (null-time session 96, fourth of the score-22
tier).** Przemysław Rola, "Boltzmann Price: Toward Understanding the Fair
Price in High-Frequency Markets", arXiv:2507.09734v1 [q-fin.TR], 13 Jul 2025
(Cracow University of Economics). One clause on what the paper is: a
parametrized family of "fair" prices derived from the Maximum Entropy
Principle applied to a two-state (bid/ask) system whose state probabilities
depend on top-of-book (TOB) volume imbalance, plus a heuristic price-process
model in which both drift and volatility are driven by that imbalance.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x85b5e3_boltzmann_price_toward_understanding_the_fair_pric.txt,
~28 pp., page-marked). Next UNREAD triage-rank entry (score 22).

## The paper in one paragraph

The author defines the Boltzmann price as the softmax-weighted expectation of
the bid and ask prices with weights from the Boltzmann distribution over TOB
imbalances (Definition 3.2, PDF p. 5), showing it interpolates the mid-price
at β = 0 and approximately the weighted mid-price at β = 2 (Lemma 4.1 and
Eqs. 19-20, PDF pp. 5-6), and that Stoikov's micro-price coincides with the
β-family under a modified large-tick example, P^micro ≈ (1 − β/2)P^mid +
(β/2)P^w with β = 2α (PDF pp. 24-25; Eq. 72, PDF p. 25). A biased-random-walk
construction with step probabilities given by the same Boltzmann weights
yields a heuristic SDE, dP_t = σ(tanh(βθ_t)dt + dW_t cosh(βθ_t)) (Eqs. 25-41,
PDF pp. 7-8; Eq. 45, PDF p. 9), where θ_t is the centered TOB imbalance and
σ is argued to scale with half the spread (PDF p. 9). Simulations with
imbalance drawn from Beta distributions and spread from Gamma distributions
generate elevated kurtosis in price changes (Tables 1-3, PDF pp. 10-12), and a
market-impact section derives the price response to an imbalance change,
dP^boltzmann = β(S/2)cosh²(βθ)dq, bounded by half the spread (Eqs. 55-60, PDF
pp. 18-19). On one month of 1-minute Refinitiv quotes for two stocks (GE,
variable spread; LCID, constant one-tick spread, May 2025, ~8,000
observations each), sampled price differences constructed as in Eqs. 52-53
with hand-chosen β and scaling η are shown to match the mean, standard
deviation and kurtosis of historical mid-price changes (PDF pp. 14-17;
Tables 5-8, PDF pp. 15-16). β is a free parameter of the framework, left
undetermined by it (PDF p. 5), with a heuristic β ~ 1/spread relation
(Eqs. 73-76, PDF pp. 25-26).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The paper is a printed demonstration that a
   two-parameter family with a free scale can match any target moment triple
   by hand: β = 17 and η = 2 for LCID were selected "to produce sampled price
   changes with means and standard deviations similar to those in the
   historical data, while also achieving comparable kurtosis" (PDF p. 16),
   the author notes that "increasing β increases kurtosis but, on the other
   hand, decreases the variance" (PDF p. 16), and the parameter estimation is
   explicitly left to future research (PDF p. 14, note 22). The historical
   "fits" (Figs. 8, 10; Tables 5-8, PDF pp. 15-17) are therefore
   marginal-moment matches between the data's own summary statistics and a
   construction whose free parameters were tuned against those same moments —
   no market null, no costs, no predictive content. This is exactly the class
   the queued dynamics-identification rule for generative nulls forbids
   (static- or invariant-distribution match alone inadmissible), and the
   β/η-tuning degree of freedom is exactly what the estimator-configuration
   freeze (deep-read 63) and primary-metric pre-commitment (deep-read 55)
   already bind. Every magnitudinal claim in the paper is banned from the
   record under the laundering rule; nothing new is licensed. No queue
   change.

2. [reinforcing, no new item] Every price in the paper's comparison set is a
   deterministic transform of the same two quotes and two queue sizes:
   P^boltzmann(0) = P^mid, P^boltzmann(2) ≈ P^w (Eqs. 19-20, PDF p. 6), the
   quasi-equilibrium price ½(P^mid + P^w) (Definition 4.2, PDF p. 6), and
   P^micro ≈ P^boltzmann(β) in the large-tick example (Eq. 72, PDF p. 25). The
   "Boltzmann price (β = 1) offers more informative signals than the
   mid-price changes, while remaining less noisy than the weighted
   mid-price" claim (PDF p. 15) is a within-family self-comparison over
   book conventions with no external null — the paired-family
   self-comparison shape the laundering rule already forbids, and the same
   cross-market control-arm discipline point as the spread-convention
   declaration rule (deep-read 56): the difference between these prices is a
   convention choice (β), not measured information. No queue change.

3. [interpretation caution] The model's informational universe is Level I
   of the book and nothing else: Assumption 3.1 makes both state
   probabilities functions of the TOB volume imbalance alone (PDF p. 4),
   higher levels are declared out of scope (PDF p. 4; PDF p. 20, note 28),
   and the 1-minute aggregation uses "the last available quote within each
   bin" (PDF p. 14), discarding intra-bin dynamics. Any C1-L2/C8-adjacent
   imbalance feature inherits this boundary: it is blind to depth-beyond-best
   depletion, to hidden liquidity (the paper's own P^b ≈ P^a justification
   assumes liquid assets, PDF p. 4), and to order of events inside an
   aggregation bin. The compression-clock and passive-cancel mechanisms the
   L2 phase cares about live precisely in what this construction cannot see —
   the paper is a caution against TOB-imbalance features being read as
   book-state summaries. No queue change.

4. [interpretation caution] β is not a constant of nature even inside the
   paper's own framework: the heuristic derivation gives β ~ 1/spread
   (Eqs. 73-76, PDF pp. 25-26), so any spec that freezes a single
   imbalance-rescaling constant across days, regimes, or assets embeds an
   untested cross-sectional assumption the paper itself declines to defend
   (parameter estimation left open, PDF p. 14, note 22); the queued
   self-excitation regime-window pre-declaration and the cross-market
   control-arm discipline already forbid exactly this silent
   constant-across-regime choice, and the estimator-configuration freeze
   would count β as frozen configuration. Interpretation discipline only;
   no queue change.

5. [reinforcing, no new item] The market-impact section's boundedness result —
   the Boltzmann price response to a full one-side queue clearance is
   S/2 · tanh(β/2) < S/2 for β = 1 (Eq. 60 and following, PDF pp. 18-19),
   versus the weighted-mid's full S/2 (Eq. 64, PDF p. 19) — is the paper
   itself showing that the same book event produces different "impact"
   magnitudes purely as a function of which within-family price definition is
   used, i.e., that impact magnitudes are convention-limited before they are
   informational. This is more evidence for the standing caveat that
   episode-attributed impact reads need the attribution null family
   (deep-read 82) and never a within-family comparison. Ammunition, not
   evidence. No queue change.

6. [source-quality note] arXiv v1 (July 2025), zero citations at
   cataloguing, single author, no journal counterpart; the price-process
   derivation is heuristic and the formal study of the proposed SDEs is
   explicitly deferred (PDF p. 9; PDF p. 20); parameter estimation deferred
   (PDF p. 14, note 22); the empirical section is two stocks, one month,
   1-minute bars. Read, graded, recorded at its grade: an ammunition-grade
   construction paper whose value to the programme is the tuning demonstration
   in finding 1 and the convention-limits demonstration in finding 5.

## What this paper would have killed if we had done it wrong

If the C1-L2 phase had scored its compression-depletion features against
nulls matched only on marginal moments — mean, standard deviation, kurtosis
of price changes — this paper is a printed constructive counterexample that
such a null is free to pass: β and η are two free knobs, the author tunes
them by hand until the constructed series reproduces the historical moment
triple (PDF p. 16), and the construction carries zero anticipatory
information (the sampled "price changes" are functions of resampled
imbalance draws and Gaussian noise, Eqs. 52-53, PDF pp. 14, 16). A
marginal-match null certified nothing. The program avoided this artifact
because the dynamics-identification rule for generative nulls (null-time
session 58) already refuses static-marginal match as a refutation
instrument, and because the estimator-configuration freeze (deep-read 63)
would refuse a β chosen after the data. The counterfactual kill: a future
"the book anticipates the price" claim laundered through a
moment-matched synthetic null, exactly the shape the queue's two rules were
built against; this paper is now part of the evidence that those rules are
load-bearing.

## Standing caveat

The construction's applicability boundary is stated by the paper itself:
constant-spread or Gamma-spread assumptions (PDF p. 7; PDF p. 10), Level-I
only (PDF p. 4), the heuristic β ~ 1/spread relation never tested against an
estimated β (PDF pp. 25-26), no formal study of the proposed SDEs (PDF p. 9),
and the empirical validation limited to two stocks, one month, 1-minute
quote-bin aggregates with hand-tuned parameters (PDF pp. 14-17). The
historical-fit exhibits are marginal comparisons against the data's own
fitted distributions, not out-of-sample predictions. arXiv-version caution:
v1 of July 2025, no journal version — check for a published counterpart
before any formal citation.
