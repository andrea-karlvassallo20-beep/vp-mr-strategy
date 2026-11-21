# Deep-read: Detecting Financial Market Manipulation with Statistical Physics Tools

Library deep-read session 71 (null-time session 82; log entry ## 91).
Haochen Li, Maria Polukarov, Carmine Ventre (King's College London), "Detecting
Financial Market Manipulation with Statistical Physics Tools" (arXiv:2308.08683v1
[q-fin.TR], 2023; zero recorded citations in the acquisition index, no published
version recorded there): a physics-flavoured spoofing/layering detector that models
Level-3 orders as particles, defines per-order momentum relative to an
analyst-chosen "active area" depth, and detects manipulation as top-k deviations
of the passive-area cumulative net momentum.

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8 faster,
or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x6aed5b_detecting_financial_market_manipulation_with_stati.txt,
~20 pp., page-marked). Next UNREAD triage-rank entry (score 25).

Session-state note, per the goal-autonomy conductor protocol (edition 6, ## 89):
the declared work choice is the standing deep-read ritual, the protocol's default
(section 3 point 1); the ## 90 pointer named this paper as next UNREAD and the
tier order was re-verified against the live file state (x475f30 read ## 90, then
x6aed5b). The edition-6 cadence counter stands at ONE of five before this session
(deep-read 70 counted at the ## 89 reset); this read makes it TWO of five, so no
synthesis pass is due.

## The paper in one paragraph

The authors model Level-3 (message-level) order-book records — opens, matches,
cancellations — as particles entering, exiting or annihilating in a 1-D "fluid"
(p. 2, p. 6). Each order's velocity is its price displacement from the boundary of
an "active area" [bM − α, aM + α] centered on the touch, per Δt (eqs. 1-4, pp. 4-5);
momentum m = size × velocity; the active-area cumulative net momentum M (eq. 5,
p. 6) is summed over events per 0.1 s bucket, and a passive-area analogue
M_passive (eq. 6, pp. 8-9) tracks the band one to two depths beyond. On Coinbase
websocket data (BTC/USD 20/04/2022 23:00-00:00, ~2.7M records; LUNA/USD
11/05/2022 crash hours, 800k records, pp. 5-7) the cumulative net momentum is
claimed to mirror midprice movement (pp. 6-8), to separate limit-selling from
market-buying pressure during the LUNA collapse (p. 8), and — in the passive
area — to expose spoofing as momentum jumps that "soon bounce back"
(pp. 9-10). Detection is by inspection of the largest standardised deviations of
M_passive per hour (pp. 13-15), validated by INSERTING the authors' own synthetic
spoofing orders into the real stream (Tables 1a/1b, 5; pp. 11-13, 17-18), and
compared against Z-scores computed on raw order sizes, which the paper reports
flagging large far-from-touch uncancelled orders instead (Tables 3-4, pp. 15-18).
The conclusion claims widespread spoofing in LUNA and method superiority over
Z-score detection (pp. 18-19).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening — default grade; every
mechanism found is a page-cited instance of a discipline the queue already
carries, and this note is another session-9-audit exhibit: a score-ranked entry
that is a proof-of-concept preprint, graded plainly below.

1. [reinforcing, no new item] The headline statistic is a function of an analyst
   constant the authors themselves declare unautomatable: every velocity (eqs.
   1-4, pp. 4-5) is measured against the active-area boundary whose depth α is
   "left to be determined by the observer" with "no known automated algorithm
   that determines this separation" (p. 10), set to α = 100 for BTC/USD and
   α = 0.5 for LUNA/USD (pp. 6-8). The passive-area measure — the detection
   instrument itself — substitutes 2α for α (p. 8), so the magnitudes whose
   top-k values are called spoofing move with a free parameter chosen per market
   per hour by hand. This is the estimator-configuration freeze (#37) in a
   fourth costume: WHICH statistic, in WHICH exact configuration — here the
   analyst must pre-freeze the area-depth convention before the data is touched,
   and a "jump" that appears under one α and dissolves under another is a
   property of the convention. No new item.

2. [reinforcing, no new item] The comparative verdict over "conventional
   anomaly detection" is a comparator-choice artefact: the Z-score baseline is
   computed on RAW ORDER SIZES (pp. 15-17, Tables 3-4), i.e., on a different
   summary of the same stream than the momentum measure it is compared against,
   so the reported "outperforms Z-score" claim (pp. 17-19) is the primary-metric
   pre-commitment rule (#33) exhibited in the wild — the loss/metric choice
   alone decides the ranking, exactly as the Lee duration-paper's loss
   reversal did, and the paper reports no decision threshold, ROC, or
   false-positive rate anywhere ("largest ten deviation values" lists, pp. 13-15,
   are the whole decision procedure). Reinforces the primary-metric
   pre-commitment family; no queue change.

3. [interpretation caution] The paper's performance evidence is self-poisoned
   by construction: validation is done by inserting the authors' own synthetic
   spoofing orders (Tables 1a/1b, 5; pp. 11-13, 17-18) into the live stream and
   observing that the detector finds them — a detector calibrated on events its
   own designers injected cannot fail to find them; the original-data detections
   (Tables 2a-c, p. 15) carry NO ground-truth labels (the paper says plainly
   that manipulation events are neither labelled nor identified, p. 11 — the
   reason synthetic data was needed), and the spoofing attribution is made by
   inspection ("it is reasonable to infer", p. 15). Reading discipline: any
   "detection rate", "accuracy", or "false positive" figure quoted from this
   class of literature is a label-provenance claim first and a number second;
   synthetic-insertion validation licenses nothing about real-data performance.
   No queue change — the library-is-ammunition invariant already bars every
   such figure from entering the record as support.

4. [interpretation caution] The in-window standardisation itself is
   non-stationarity-blind: deviation = (net momentum − mean)/standard variance is
   computed over each one-hour window (p. 13), including the LUNA collapse —
   a window whose mean and variance are themselves moving with the crash — and
   the top-k rule then flags whatever the window's own tails contain. An
   anomaly statistic normalised inside the regime it claims to detect is the
   self-excitation regime-window pre-declaration's (#32) reading-discipline
   cousin: the windowing convention must be pre-declared or the "anomaly"
   content is partly manufactured by the choice. No queue change.

5. [cost-survival ammunition] The paper's spoofing economics — spoof orders
   are placed just OUTSIDE the active area, near enough to mislead, far enough
   to avoid execution, and "normally spoofing and layering happen in markets
   with relatively poor liquidity" (pp. 9-11) — is recorded only as the class
   of assumptions any future K7-style cost-survival layer would have to carry
   (placement-band definition, execution-avoidance premise, per-liquidity
   variation). If a C8 manipulation-adjacent control arm is ever proposed, this
   is the shape of the declaration it owes: never operationalized, nothing
   armed.

6. [source-quality note] arXiv v1, zero recorded citations, no published
   version recorded in the index; the extract header shows the same author as
   "Polukarov" while the index records "Polukarova" (check before formal
   citation); internal date inconsistencies (the BTC dataset is described as
   20/04/2022 on p. 6 but figures are labelled 19/04/2022, and the synthetic
   BTC figure caption reads "19/04/2023", p. 17); no formal statistical test
   anywhere, qualitative visual comparison only. Grade plainly: a
   proof-of-concept preprint by an author team using an interesting
   physicalist lens, not a validated detection methodology; the score-25 rank
   promised more than the text delivers, which is exactly what the session-9
   triage audit said to expect.

## What this paper would have killed if we had done it wrong

If the programme had no estimator-configuration freeze, this paper shows what
would have happened: a C1-L2-adjacent "compression" or "manipulation" statistic
defined relative to an analyst-chosen book-depth band, with the band re-chosen
per market and per hour by hand, whose flagged "events" then travel into a spec
as if they were properties of the market rather than of α. And if the
library-is-ammunition invariant were absent, the synthetic-insertion
"validation" would have entered the record as evidence of detection capability —
the programme would own a claimed detector whose performance was measured
against events its own authors planted. The existing disciplines (config
freeze #37, primary-metric pre-commitment #33, ammunition-not-evidence) are
each page-cited here by this paper's own text; this read is a counterfactual
photograph of the programme with those rules deleted.

## Standing caveat

Everything here is one exchange (Coinbase), two pairs, a few hours including a
flash crash; the "momentum mirrors the midprice" claim (pp. 6-8) is visual and
window-specific (the authors themselves note the LUNA mirror is "somehow more
loose" than BTC's, p. 8); the active/passive separation is explicitly manual and
market-dependent (p. 10); detection thresholds are top-k by inspection (pp.
13-15); validation is self-inserted synthetic events (pp. 11-13); no statistical
significance, no out-of-sample design, no labels. arXiv-version caution: check
for a published version before any formal citation; the acquisition index
records zero citations and no published version.
