# Deep-read session 90: Calcagnile, Bormetti, Treccani, Marmi, Lillo — "Collective synchronization and high frequency systemic instabilities in financial markets"

**Library deep-read 90** (null-time session 100, log ## 119). Authors: Lucio Maria
Calcagnile, Giacomo Bormetti, Michele Treccani, Stefano Marmi, Fabrizio Lillo.
Venue: arXiv:1505.00704v1 [q-fin.ST], May 5, 2015. One clause: a 2001-2013
US-equities empiricism showing that one-minute extreme moves have become fewer
but dramatically more synchronized across assets, that scheduled macro news
accounts for a minority of the largest synchronized moves, and a parsimonious
Hawkes model of the cojump multiplicity vector in which the memory of systemic
events lives on a ~1.7-minute scale.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8 faster,
or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x9921ac_collective_synchronization_and_high_frequency_syst.txt,
~28 pp., page-marked). Next UNREAD triage-rank entry (score 21).

## The paper in one paragraph

The authors detect one-minute "jumps" in 140 highly liquid Russell 3000 stocks
per year, 2001-2013, as returns exceeding an exponential-moving-average bipower
volatility estimate by a threshold θ = 4 (with sensitivity checks at θ = 6, 8,
10; PDF p. 5), after dividing out the average intraday volatility pattern (PDF
pp. 15-16). Total jumps have decreased secularly across all thresholds, yet
cojumps (simultaneous jumps in M stocks) of high multiplicity are up to ten
times more frequent in 2013 than in 2001, the multiplicity distribution shows a
power-law tail close to M^-1.5 truncated at the finite universe size (PDF pp.
6-8), and the gain is not an artifact of faster markets, verified by repeating
the analysis at one-to-five minute detection scales (PDF pp. 8, 16-17).
Associating systemic cojumps with a database of scheduled macroeconomic
announcements (Econoday, ~150-260 per year, 27 in-session categories; PDF pp.
4-5), they find that well under 40-50% of high-multiplicity cojumps are
preceded by a news release in the previous 15 minutes, and that news-triggered
systemic moves complete essentially within 5 minutes of the release (PDF pp.
2-3, 9-10). They then model the multiplicity vector directly (dropping the
identity of the cojumping stocks) with a three-parameter multivariate Hawkes
process, η = 0.15, β = 0.6 (memory timescale 1/β ≈ 1.67 minutes), γ = 2.65
hyperbolic cross-excitation decay (PDF pp. 10-12, 19), calibrated by moments
(f(1), f(2)) on J = 10 and tested on J = 30, 60 against a shuffling benchmark
(PDF pp. 12-13, 20-21): the more systemic the conditioning cojump, the higher
the probability and the greater the multiplicity of near-future systemic
cojumps, and 85% of intensity is attributed to excitation by construction of
the parametrization (PDF pp. 11-12, 19).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The exogenous fraction of market-wide extreme
   co-movements is a minority: less than 40% of high-multiplicity cojumps are
   preceded by a scheduled macro announcement, consistently across all years
   and even for the largest M (PDF pp. 2-3, 9-10, 14), i.e. systemic structure
   arises endogenously in the majority of cases. What it licenses: no C1-L2/C8
   claim may condition a systemic association on a news/event timeline without
   a null against endogenous clustering, and no news-conditioned comparator
   may attribute to the news what the book does to itself. This reinforces the
   C8 shuffled-arrival placebo (amendment A3, PROPOSED, owner-gated) and the
   deterministic-calendar null (deep-read 73) by the same mechanism the paper
   measures in print. No queue change.

2. [reinforcing, no new item] Macro-driven systemic moves complete within about
   5 minutes of the release: the news-attribution fraction is nearly identical
   for τ = 1, 5, 10, 15 minute lookback windows (PDF pp. 9-10). What it
   licenses for the C8 macro limb and any book-plus-event-timeline join: the
   association is insensitive to the tolerance grid, which is exactly what a
   desync-coeval tolerance disclosure must demonstrate, and a join whose
   macro alignment survives only under one post-hoc window would be
   manufacturing the association. Reinforces the cross-stream synchronization
   and single-source-count pre-declaration (#48, queued deep-read 89), whose
   clause (iii) asks precisely for declared tolerance sensitivity. No queue
   change.

3. [reinforcing, no new item] The claim's robustness is earned by pre-emptive
   scale checks, not asserted: detection thresholds θ ∈ {4, 6, 8, 10}, detection
   windows of one-to-five minutes, and a 700-asset universe versus 140 all
   shown to leave the secular synchronization increase intact before any
   headline rests on them (PDF pp. 5, 7-8, 8 inset, 16-17). Reinforces the
   regime-window pre-declaration (deep-read 53), the primary-metric
   pre-commitment (deep-read 55) and the estimator-configuration freeze
   (deep-read 63): the grid of windows, thresholds and universe sizes is
   declared configuration, and a structural claim surviving only one cell of
   that grid is a grid artifact. No queue change.

4. [interpretation caution] The multiplicity-vector Hawkes deliberately
   drops the identity of the cojumping stocks (PDF p. 11): everything it
   licenses lives at the aggregate level. An observed aggregate cojump
   association in C1-L2/C8 data (cross-sectional synchronization depth,
   market-wide burst statistics) cannot be attributed to any individual
   episode, level or asset-specific mechanism; and an aggregate excitation
   (85% endogenous, PDF p. 12; larger conditioning multiplicity raising both
   the probability and the expected multiplicity of future events, PDF pp.
   12-13) is equally consistent with common correlation with the aggregate
   flow, the level-versus-memory confound and pure book-size scaling. Any
   aggregate reading must therefore pass the level-versus-memory
   disambiguation (deep-read 59, queued) and the residual-flow attribution
   null (deep-read 82, queued) before an episode-level interpretation is
   licensed. No queue change.

5. [interpretation caution] The multiplicity power-law tail is explicitly
   truncated by the finite universe: the distribution's bending is attributed
   by the authors to the M ≤ N support (and extends when N = 700; PDF pp. 7-8).
   Any C1-L2/C8 cross-sectional count statistic inherits this: its tail and
   its apparent self-similarity depend on the declared universe size, and a
   tail statement made without the frozen universe definition is ambiguous.
   This is the macro censoring discipline (freeze the censoring rule and the
   support before the data, per the standing base-rate and censoring
   families) applied to cross-sectional counts. No queue change.

6. [reinforcing, no new item] Extremity is defined only after removing the
   intraday (calendar) component: returns are divided by the average
   intraday pattern of absolute returns before any thresholding (PDF pp.
   15-16), i.e. the paper itself normalizes out the time-of-day geometry
   before claiming a state-dependent structure. A future intraday extremity
   or compression-clock feature that thresholds raw magnitudes without
   declaring the calendar normalization would re-import exactly the
   J-shaped-artifact failure the deterministic-calendar null (deep-read 73)
   exists to kill. No queue change.

7. [source-quality note] arXiv v1 preprint (May 5, 2015); Kibot one-minute
   closing prices, 140 stocks per year, 2001-2013, US equities only; no
   peer-reviewed version cited in the extract. The model is calibrated by a
   heuristic weighted-moment fit with an analyst-chosen 0.5 loss weighting on
   the second moment (PDF pp. 20-21), and the "85% endogenous" figure is
   partly imposed rather than freely estimated: the parametrization sets
   µ = ηE[λt] so that the spectral radius of the kernel matrix equals 1 - η
   by construction (PDF pp. 11, 19), with the empirical multiplicity
   frequencies substituted for the expected intensities (PDF pp. 21-22), so
   the branching share is an input restated as a finding; the stationary
   multiplicity distribution is matched by construction (PDF p. 19) and
   cannot count as an independent validation, while the honest
   calibration/test split on J = 10 versus J = 30, 60 (PDF pp. 12, 20-21) is
   genuinely out-of-family for this genre. All magnitudes are venue-,
   sample- and grain-specific and are banned from the record as support for
   any program claim under the laundering rule. Check the published version
   before formal citation.

## What this paper would have killed if we had done it wrong

If the C8 macro limb had been built on the folk assumption that market-wide
extreme events are news events, this paper would have killed it: under 40% of
the largest synchronized moves are news-attributable (PDF pp. 9-10), so a
macro-conditioned comparator would have attributed to announcements what the
book generates endogenously, manufacturing a "macro anticipation" find out of
coincident endogenous clustering. If the cross-stream join discipline (the
book feed plus its macro/event timeline) were handled with a post-hoc
alignment window, the paper's one-to-fifteen-minute insensitivity pattern
(PDF pp. 9-10) shows exactly how much freedom a silent tolerance choice buys:
an analyst could pick the window that maximizes apparent alignment, and the
find would be a tuning artifact. If an aggregate cross-sectional burst or
synchronization statistic had entered a spec without the attribution null,
the multiplicity-vector construction (PDF p. 11) proves by example that an
excitation-looking aggregate can be modeled beautifully while knowing nothing
about which episodes drove it: the spec would have been licensed by a model
that is causally empty at the episode level. The existing disciplines (the
deterministic-calendar null, the #48 join disclosure, the level-versus-memory
and attribution-null queue) are what keep those three roads closed.

## Standing caveat

The paper is one-minute-bar US equity data, 2001-2013, one venue class; it
says nothing about full-depth L2 mechanics, maker behavior or passive
withdrawal, and nothing transfers to the programme's barrier-clock questions
without independent evidence. The multiplicity process is an aggregate with
identity dropped; the model is stationary by parametrization (η fixed, 0 <
η < 1, spectral radius 1 - η; PDF pp. 19, 23) so it cannot speak to
non-stationarity or critical transitions, only to a stationary regime with
strong excitation. The calibration is a moment-matching heuristic, not
likelihood inference, and its loss weighting is an analyst choice. The
macro-news sample is scheduled announcements only; non-scheduled and
idiosyncratic news are outside the design (PDF pp. 4-5, 9). arXiv-version
caution applies: check the published version before any formal citation.
