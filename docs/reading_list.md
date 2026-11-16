# Reading list: OFI and Hawkes in crypto (null-time scan)

Purpose: the adversarial curriculum for C1-L2 and C8 - every entry is read
against one question: "what here kills C1-L2 (or C8) faster?" Sections:
(A) papers already in the repo library (PDF or extracted text under
`docs/library/`), (B) papers NOT yet in the library, synthesized from
internal knowledge and flagged for legal-OA acquisition and verification
before any production use. Per the programme's rule, paywalled papers are
never scraped; they are acquired legally or summarized with the "verify
against the source" label.

## A. Already in the library

1. **Cont, Kukanov & Stoikov - "The Price Impact of Order Book Events"
   (Journal of Financial Econometrics, 2014).** Defines OFI as the
   signed, tick-size-normalized net size change of the best bid and ask
   and proves a linear relation between OFI and mid-price changes over a
   short horizon. It is the mathematical backbone of C8's OFI leg; our
   formula was verified against the arXiv source
   (`paper/research/phase1_daily/math_verification_2026-11-16.md`).
   Read adversarially: their linear impact is a short-horizon statement -
   if the C8 interaction only exists at horizons beyond the OFI
   half-life, the claim is dead on arrival.

2. **Xu et al. - "Multi-Level Order-Flow Imbalance in a Limit Order
   Book".** Extends OFI to multiple price levels and shows the
   multi-level variant predicts better than top-of-book alone. It matters
   because C8's "extreme OFI absorption" state must survive the question
   of whether depth (levels 2-25, which the Tardis data gives us) carries
   the information that top-of-book OFI misses. If the C8 effect lives
   only in deep levels, the pre-registered top-of-book definition may be
   measuring the wrong costume again.

3. **"Forecasting High Frequency Order Flow Imbalance".** Documents how
   quickly OFI predictability decays with horizon and how it concentrates
   in event time, not wall-clock time. It matters because C1-L2 and C8
   both run hazard clocks in wall-clock with event-time sampling of the
   mid; if the OFI signal is purely event-time-local, the 4h/24h hazard
   clock may be too coarse to ever see it.

4. **Bacry, Delattre, Hoffmann & Muzy - "Modelling microstructure noise
   with mutually exciting point processes".** The canonical bridge from
   Hawkes self-excitation to price dynamics: trades excite trades, and
   the branching ratio measures how much of the activity is endogenous
   feedback. It matters because C8's Hawkes n_c > 0.8 threshold IS the
   branching-ratio "reflexivity" concept; our estimator was already
   corrected once (the metric that overstated n_c by the factor beta).
   Read adversarially: their estimates are on equities with stable
   matching engines; crypto venue outages and fee-tier changes are
   exogenous shocks the branching ratio can mistake for endogeneity.

5. **Filimonov & Sornette - "Quantifying Reflexivity in Financial
   Markets: Towards a Prediction of Flash Crashes".** Uses the Hawkes
   branching ratio as a real-time measure of how close the market is to
   a self-exciting cascade, with flash-crash case studies. It matters
   because the Tesla-day anatomy that motivates C8 is exactly this
   pattern at crypto grain; the paper's main risk to us is the opposite
   of comfort - their n_c estimates are noisy on short windows, which is
   why the C8 amendment demands a shuffled-arrival placebo before the
   0.8 threshold is armed.

6. **Easley, Lopez de Prado & O'Hara - the VPIN / flow-toxicity papers
   (including the volume-clock construction).** VPIN measures
   order-flow toxicity on a volume clock with bulk volume classification.
   It matters because C8's third micro state uses VPIN - and the C8
   review already fixed the clock ambiguity (volume buckets per the
   original construction) that killed T3 on a two-clock trap. Read
   adversarively: the VPIN literature's own critics (anderson/hammid
   style rebuttals) show VPIN can be a volatility proxy in disguise -
   the exact costume check C8's kill lines demand.

7. **"Branching ratio approximation for the self-exciting Hawkes
   process".** The estimator paper behind our n_c code path. It matters
   because C8's placebo design (production threshold must exceed the
   shuffled-arrival 95th percentile) is derived from this paper's bias
   analysis on finite windows; 30 minutes of arrivals is exactly the
   regime where the naive estimator is biased upward.

8. **"The Flash Crash: High-Frequency Trading in an Electronic Market"
   (Kirilenko, Kyle, Samadi, Tuzun).** The forensic anatomy of a
   self-exciting unwind in an electronic book. It matters as the
   motivating picture for what "the grievance coming due" looks like in
   the data we are about to buy: a compressed book, an aggressive
   initiator, and a cascade. Read adversarially: their cascade was
   cross-market and liquidity-provider-driven; a crypto perp cascade
   runs through liquidations and funding, which the 2026 data will show
   differently.

## B. Not yet in the library (acquisition candidates)

*Flagged honestly: synthesized from internal knowledge; each must be
acquired legally (OA/arXiv) and verified before any production use. None
is a claim; each is a question.*

9. **Bacry, Mastromatteo & Muzy - "Hawkes Processes in Finance"
   (Quantitative Finance, 2015).** The survey that unifies the Hawkes
   estimation stack (MLE via the Ozaki/EM recursion, branching ratio,
   multivariate excitation) in one place. It matters because our
   cheatsheet's O(N) Ozaki recursion and the C8 multivariate
   (price/trade) extension both follow its conventions; a mismatch
   between its conventions and our implementation would be a silent
   estimator bug. Acquisition: check arXiv for the preprint version.

10. **Abergel & Jedidi - "A Mathematical Framework for Limit Order
    Books" (and the long-term-behavior companion).** Builds the LOB as
    a Hawkes-driven queueing system and derives stationary depth
    distributions. It matters because C1-L2's compression state is a
    statement about the book's realized range; their framework is the
    cleanest source for what "stationary book" should mean, which our
    5-day percentile pool approximates. If the book is non-stationary
    at exactly the scales we pool over, the percentile ranking is
    noise. Acquisition: check publisher OA status.

11. **"Trade Arrival Dynamics and Quote Imbalance in a Limit Order
    Market" (already downloaded as an OA stray in the expanded
    library - verify and shelve it next to the Hawkes family).** It
    jointly models arrival rates and the quote-imbalance state, which
    is close to C8's interaction before the interaction was written.
    It matters because it is the nearest existing thing to C8's
    estimand, and reading it adversarially will show whether the
    interaction we pre-registered has already been measured (and
    killed) in equities.

12. **Crypto-specific Hawkes/OFI literature (multiple candidates).**
    The expanded library holds crypto microstructure families
    (perps/funding, networks/lead-lag, extreme crypto events), but the
    specific question "does the Hawkes branching ratio of a crypto perp
    predict the 4h/24h hazard of a significant move" appears untested
    in our library index. Candidate searches for the next acquisition
    round: branching-ratio studies on Binance perp trades; OFI on
    crypto venues (several exist on Bitcoin spot); liquidation-cascade
    point-process models. Each matters for the same adversarial
    reason: if someone has already measured the C8 interaction and
    found nothing, that is a pre-registration-relevant fact we want to
    know BEFORE the data is bought, not after.

## Standing rule

One paper per null-time session, read against the killing question - not
for coverage. Summaries of library papers cite the extracted text;
candidates in section B stay labeled until legally acquired and read.
