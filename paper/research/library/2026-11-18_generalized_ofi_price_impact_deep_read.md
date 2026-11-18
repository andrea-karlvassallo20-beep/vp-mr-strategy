# Deep-read session 25: Su, Sun, Li and Yuan, "The Price Impact of Generalized Order Flow Imbalance"

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8 faster, or
change their kill lines? Source: legally acquired OA copy
(docs/library/text/xdb066c_the_price_impact_of_generalized_order_flow_imbalan.txt,
~9 pp., page-marked). Next UNREAD triage-rank entry (score 33, xdb066c).

## The paper in one paragraph

A short applied paper (Su, Sun, Li and Yuan, Xi'an Jiaotong University,
arXiv:2112.02947v1, December 2021) extending the Cont-Kukanov-Stoikov OFI
to Chinese stock snapshot data: with 3-second order-book snapshots, the
best quote routinely moves several ticks inside one observation window,
breaking the one-tick-per-window assumption under which the CKS linear
identity holds, and the classic OFI estimator then drops the depth
changes across the swept levels (PDF pp. 3-4). Their Generalized OFI
weights depth changes across every level swept by the best-quote move,
with a log-stationarized variant (log-GOFI) after Wang et al.; regressed
linearly against mid-price change on 10 CSI 500 constituents at 30
second, 1 minute and 5 minute scales, they report average out-of-sample
R-squared rising from about 33-43 percent (OFI) to about 84-86 percent
(log-GOFI) (PDF p. 1 and Tables 1-3, PDF pp. 5-6). The empirical
protocol's train/test details are not recoverable from the extract, the
10 stocks are disclosed as selected "to facilitate presentation", and
no costs or strategy layer exist in the paper; it is a fit-quality
comparison on one market's snapshot data and nothing more.

## Findings, graded (does any kill line move?)

NO kill line changed. ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION. The paper's mechanism is real and load-bearing even though
its magnitudes are not importable (finding 2), and it exposes a genuine
gap in the standing admissibility family.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The event-grain
   OFI accumulation rule, extending the E1 volume-conservation
   reconstruction-admissibility family. The one-tick assumption is
   load-bearing in the CKS linear identity: the mid-price change equals
   the imbalance times the impact coefficient only up to a truncation
   error that is second-order while the best quote moves at most one
   tick per observation window; under coarse snapshots (3 seconds on
   the Chinese feed, and any windowed aggregation coarser than the
   event tape generally) the best quote crosses multiple ticks inside
   one window, the swept levels' depth changes are misattributed, and
   the truncation becomes first-order (PDF pp. 3-4, with their Figure 2
   showing a two-tick intra-window move). Probe E1's ratified rule
   admissibility-checks the DEPTH reconstruction (conservation identity
   per level per window) but says nothing about the GRANULARITY at which
   accumulated flow features are computed from that depth: a
   conservation-clean depth series can still feed a windowed OFI that
   quietly mixes multi-tick crossings. Pre-declaration: any OFI-type
   flow feature used in a C1-L2 (or C8 L2-arm) measurement must be
   accumulated at event grain, each event contributing at the book
   state it acts on; any window-aggregated fallback must disclose the
   per-window best-quote crossing count and the declared sweeping
   convention, and windows with undisclosed multi-tick crossings are
   inadmissible. Harder to pass: it closes the one route by which a
   measurement could pass the conservation gate and still rest on a
   mispriced flow object - and the mispricing is not neutral, since
   coarse-grain OFI can inflate apparent flow-price correlation and
   make a compression signal easier to "find". It tightens only the
   E1 admissibility family (and through it the future C1-L2 pipeline
   and C8's L2 arm); T-O's taker-print trigger, no C1-L2 spec text, and
   no kill line are touched; nothing is armed.

2. [interpretation caution] The reported R-squared magnitudes shall
   never be imported, for two reasons visible in the paper itself.
   First, the generalized construction weights depth changes by the
   number of ticks the best quote moved, a quantity mechanically tied
   to the mid-price change being regressed: part of the R-squared gain
   may be definitional coupling between feature and target, not
   incremental information, and the paper presents no control for it.
   Second, the train/test protocol is not recoverable from the extract
   and the stock set is a disclosed convenience sample. The numbers are
   recorded as the paper's claims about its own construction on its own
   data, page-cited, and nothing more.

3. [reinforcing, no new item] Beyond-best-quote depth carries
   information: the paper's construction exists only because depth
   changes at the swept levels are informative, and it cites the
   multi-level OFI line (Xu, Gould and Howison 2018) as the
   depth-beyond-BBO precedent (PDF pp. 1-2). This corroborates, at the
   library level, that BBO-only features are a coarsening of the depth
   information available in full L2 - the standing motivation language
   of C1-L2 - and nothing further: no number, weight, or level count
   transfers.

4. [source-quality note] arXiv v1 only, zero citations in the index, no
   published version on the shelf; four authors; the sample is 10 of the
   CSI 500 constituents selected "to facilitate presentation" (selection
   disclosed, not random); the text extract is heavily degraded (formula
   symbols lost), so the construction was reconstructed from the prose
   and figure descriptions rather than verified symbol-by-symbol; the
   published version, if one exists, is to be checked before any formal
   citation. Triage-audit lesson applies: a score of 33 delivered a
   competent but minor preprint; read, graded, recorded.

## What this paper would have killed if we had done it wrong

If the programme had imported the headline ("OFI explains up to 86
percent of price changes") into C1-L2's motivation or expectations, two
failures would have followed. First, laundering a one-market,
snapshot-grain fit comparison into a programme expectation: when the
event-grain L2 OFI then shows a different (lower or higher) association
with the compression endpoint, the gap would be read as a programme
failure rather than a definitional difference of objects. Second, the
deflation risk flows the other way too: if someone later "improved" a
windowed OFI with tick-move weighting inside the programme without
pre-declaring it, the feature would partially embed the outcome's own
units and inflate correlations - exactly the kind of silent
target-into-feature leak the sharpening queued in finding 1 exists to
make inadmissible. The standing discipline (library is ammunition;
admissibility before statistics; no number from any paper enters a
spec) blocked both routes in advance; the new candidate sharpens the
second one against a specific, page-cited mechanism.

## Standing caveat

Chinese CSI 500 constituents, 3-second exchange snapshots, horizons of
30 seconds to 5 minutes, no transaction costs, no strategy, no crypto
market, and a formula text degraded in extraction. Nothing here measures
anything on the programme's instruments, clocks, or feature
definitions; the transferable content is the mechanism (window grain
versus event grain in accumulated flow features), never any magnitude.
arXiv v1: check published version before formal citation. Laundering
directions named: INTO - no coefficient, weight, R-squared, tick-count
convention, or construction detail enters any spec, default, or
calibration, and the generalized construction itself is not adopted
anywhere without its own pre-registration; OUT - the R-squared claims
are never cited as evidence that OFI-family features explain price
changes in any market other than the paper's own sample, and the
86-percent style headline is never repeated as a motivation for
C1-L2.
