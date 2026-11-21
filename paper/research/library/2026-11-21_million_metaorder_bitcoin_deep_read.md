# Deep-read session 82 — "A million metaorder analysis of market impact on the Bitcoin" (Donier, Bonart)

**Session:** library deep-read 82, null-time session 93 (log ## 108).
**Authors:** J. Donier (UPMC Paris 6), J. Bonart (CFM-Imperial Institute of Quantitative Finance).
**Venue/id:** arXiv:1412.4503v3 [q-fin.TR], dated 22 September 2015. A complete-tape
empirical study of market impact on the MtGox Bitcoin/USD exchange reconstructing
over one million metaorders from 13M trader-identified trades, confirming the
square-root impact law and decomposing it into mechanical and informational parts.

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xfcaaa2_a_million_metaorder_analysis_of_market_impact_on_t.txt,
~18 pp., page-marked). Next UNREAD triage-rank entry (score 23).

## The paper in one paragraph

Using the complete August 2011 to November 2013 MtGox Bitcoin/USD trade
record with anonymized but persistent trader IDs (PDF pp. 1, 4), the
authors segment over 14M aggressive trades into more than 1M metaorders
(inactivity threshold about one hour, endpoint at direction change, PDF
pp. 5-7) and measure: peak impact follows the square-root law I ≈
±Yσ(Q/VD)^δ over four decades with δ ≈ 0.5 and Y ≈ 0.9, despite a venue
with 60 bps fees that hobbles arbitrage and market making (PDF pp. 2,
8-9); the law holds trajectory-wise, I_path(r,Q,µ) = I(rQ,µ), the market
not distinguishing a continuing from a stopping metaorder (PDF pp. 9,
eq. 5); the prefactor's non-stationarity is absorbed by σD/√VD, the
residual Y-ratio being approximately Gaussian at 0.9 ± 0.35 and staying
stable through the April 10 2013 crash (PDF pp. 10-11, Figs. 7-8); slow
executions show LARGER measured impact, I_exec ~ Q^δ/µV^δ' with δ' ≈ 0.4,
because the informed component realizes during execution (PDF pp. 13-14,
Fig. 11); the market reacts to the TOTAL order flow, not to individual
metaorders, so impacts do not add linearly and metaorders are not detected
(PDF pp. 14-16, summary point 5); and for "isolated" metaorders (those
accounting for ≥ 75% of net market imbalance over [t0, t0+10T], about 3%
of the sample) the mechanical permanent impact decays to approximately
zero, permanent impact being the correlation between the metaorder and
future order flow rather than information about any fundamental price
(PDF pp. 15-16, Fig. 12). The authors conclude equilibrium/fair-pricing
and martingale arguments cannot be the origin of the square-root law and
promote heterogeneous-agent (supply-demand) models (PDF pp. 2, 16-17).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The square-root law holds on a crypto
   venue at 2011-2013 MtGox microstructure (60 bps fees, ~0.6% spread,
   no market making, 30-40% of daily volume visible in the morning book
   against <1% on stocks, PDF pp. 2, 4, 8-9): ammunition that a generic
   flow-impact mechanism exists across microstructure regimes and
   motivates C1-L2's premise, but it supports nothing — the launder-support
   ban binds, and the paper's universality claim is its own, venue-limited
   (cf. finding 6).

2. [interpretation caution] Impact is trajectory-flat in expectations:
   during execution the market makes no difference between a metaorder
   that will stop and one that will continue (I_path(r,Q,µ) = I(rQ,µ),
   PDF p. 9). Reading discipline for C1-L2: the instantaneous flow state
   does not encode the episode's future; any flow-compression feature
   must not be read as if book/flow snapshots carry metaorder-boundary
   information. No queue change.

3. [interpretation caution] The impact prefactor is regime-state unless
   normalized: raw ~Y varies wildly (including through the April 10 2013
   crash) and is absorbed by σD/√VD, residual Y ≈ 0.9 ± 0.35 (PDF
   pp. 10-11). Reading discipline: any future flow-intensity or
   impact-like statistic must pre-declare its normalization (raw vs
   σ/√V-normalized) — the estimator-configuration freeze (#37, B7)
   already forbids post-hoc estimator choices; this is the
   normalization axis of that owned ground. No queue change.

4. [interpretation caution] Permanent impact is a correlation artifact:
   the informed/uninformed selection (isolated metaorders ≥ 75% of net
   imbalance over [t0, t0+10T], about 3% of the sample) moves the
   measured long-run impact from the ~2/3-of-peak level down to
   approximately zero, and the paper reads permanent impact as
   correlation with future order flow, not information content (PDF
   pp. 15-16). Reading discipline: an apparent persistent component in
   any flow-price statistic may be a residual-flow correlation, and its
   removal is a conditioning protocol with analyst-chosen thresholds —
   the same degree-of-freedom class the queued estimator items fence.
   No queue change.

5. [reinforcing, no new item] The market reacts to total order flow,
   not to individual metaorders; impacts of different metaorders are
   dependent and do not add linearly; metaorders are not detected by
   other participants (PDF pp. 14-16). Reinforces aggregated-flow
   feature design (C1-L2's compression features summarize collective
   flow, which is the right object per this paper) and undercuts any
   detection-based narrative. Nothing new licensed.

6. [source-quality note] MtGox 2011-2013: a 60 bps-fee, no-HFT,
   single-venue, pre-modern crypto microstructure; data from an
   anonymous source with only partial consistency checks and the
   authors' own "no insurance is given that all data is accurate"
   (PDF p. 4); the venue later collapsed outside the paper's record;
   the segmentation scale (one-hour inactivity) is analyst-chosen (PDF
   pp. 5-7); arXiv v3 lineage — a published version must be checked
   before formal citation. No transfer to a modern crypto perp L2 tape
   is established or claimed; this one is ammunition with an expiry
   regime label attached.

## What this paper would have killed if we had done it wrong

Two failure modes this read exhibits openly. First, had the C1-L2 spec
not been frozen before data, this is the paper most likely to have been
laundered into "the square-root law is universal, build impact features
on it": the claim is real on its tape, but its tape is a venue whose fee
structure suppressed the exact mechanisms (arbitrage, market making)
present on any modern perp exchange — the regime label is the whole
lesson. Second, the informed/uninformed result shows a headline
conclusion (permanent impact ≈ 0) produced by a conditioning choice two
thresholds and one window wide, on the same data that shows 2/3
persistence unconditioned: without the estimator-configuration freeze
and the pre-declared-conditioning discipline the queued items already
carry, the same threshold-shopping would be available to any future
impact- or decay-style statistic in the programme. The programme's
pre-declaration spine is what keeps this paper ammunition instead of a
recipe.

## Standing caveat

Everything here is 2011-2013 MtGox, a single-asset economy with no
market-making/HFT presence and 60 bps fees; universality of the
square-root law beyond it is the authors' claim, argued by absence of
mechanisms (fees, arbitrage) rather than by cross-venue evidence given
here. The metaorder reconstruction is a declared convention whose
sensitivity is asserted, not measured across the parameter (PDF pp.
5-7). The impact-surface fits (δ' ≈ 0.4) are the authors' own and noisy
(PDF pp. 13-15). arXiv-version caution applies before formal citation.
