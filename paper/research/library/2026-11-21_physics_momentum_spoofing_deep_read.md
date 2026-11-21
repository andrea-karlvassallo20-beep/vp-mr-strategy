# Deep-read note — library deep-read session 71 (null-time session 82)

**Paper:** Haochen Li, Maria Polukarov, Carmine Ventre (King's College London),
"Detecting Financial Market Manipulation with Statistical Physics Tools"
(arXiv:2308.08683v1 [q-fin.TR], 16 Aug 2023; listed date on the PDF title page
August 21, 2023). A physics-flavoured engineering paper: it re-maps Level-3
order-book events (submissions, cancellations, matches) onto a
particle-momentum metaphor, defines a book-level "momentum" statistic over an
analyst-partitioned active/passive depth window, and uses large deviations of
that statistic in the passive window to locate candidate spoofing and layering
orders, on Coinbase L3 data for LUNA/USD (May 2022 flash crash) and BTC/USD.

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x6aed5b_detecting_financial_market_manipulation_with_stati.txt,
~21 pp., page-marked). Next UNREAD triage-rank entry (score 25).

## The paper in one paragraph

The authors model every limit order as a particle whose "velocity" is its
quoted-price distance from the moving lower/upper bound of an "active area"
[bM-alpha, aM+alpha] divided by the sampling interval (eqs. 1-4, PDF pp. 4-5),
define order momentum m = s*v, book momentum as the sum of momenta in the
active area per delta_t = 0.1 s bucket (eq. 5, PDF p. 6), and a passive-area
variant with doubled window (eq. 6, PDF pp. 8-9). The active-area cumulative
net momentum "closely mirrors the midprice movement" on BTC/USD
(PDF p. 7, Fig. 3a) and, split by order class on LUNA crash day, shows market
orders pushing upward while limit orders sell persistently (PDF pp. 7-8,
Figs. 4-5). Because no labelled manipulation ground truth exists — "neither
spoofing nor layering events are labeled or identified" (PDF p. 12) — the
method is validated by planting synthetic spoofing orders the authors
themselves designed (Tables 1a/1b, PDF p. 13) and showing the passive-area
momentum jumps at them (Figs. 7, 12), then applied to the real LUNA data,
where the top ten-deviation timestamps trace back to limit buys cancelled
minutes later (Tables 2a-2c, PDF pp. 14-15), including a 124-record cluster
of identically sized 29,000-LUNA orders read as layering. The claimed
superiority over Z-score anomaly detection (PDF pp. 14-19) rests on the
Z-score applied to raw order sizes flagging large-but-harmless distant
orders (Tables 3, 4) where the momentum method flags the planted and
suspected patterns. The conclusion (PDF pp. 19-20) advertises the framework
as a foundation for manipulation study across asset classes.

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The active-area depth alpha is a pure analyst
   parameter: "the identification of active and passive areas... is left to
   be determined by the observer" and "to the best of our knowledge there is
   no known automated algorithm that determines this separation"
   (PDF p. 11); it is set as an absolute 100 USD on BTC/USD and an absolute
   0.5 on LUNA/USD (PDF pp. 7-8) — a per-asset absolute money window whose
   scale is never justified. Every headline statistic (the momentum series,
   the deviation list, which timestamps count as anomalies, even which
   planted spoofing orders fall inside or outside the scanned window,
   PDF p. 13) is a function of this undeclared geometry, and the velocity
   anchor bM(T-delta_t) is itself a function of the unexamined
   delta_t = 0.1 s clock choice (PDF pp. 4-6). This is the flow-clock
   scale-constant and the window/level-declaration family (already queued:
   flow-clock scale-constant; already ratified precedents: spread-convention
   declaration, VPIN clock pre-commitment) with a second concrete instance;
   nothing new added.

2. [interpretation caution] The "closely mirrors the midprice" result
   (PDF p. 7, Fig. 3a) is close to mechanically built in: a buy order's
   velocity is its positive distance from the active-area floor, a sell's
   the negative distance from the ceiling (eqs. 1-4, PDF pp. 4-5), so
   cumulative net momentum is a signed size-times-distance transform of the
   order flow constructed so that buying activity above the floor adds
   positive momentum in the direction that lifts the midprice. A book-level
   statistic whose construction embeds signed correlation with the target
   is not predictive evidence of anything, and no cross-validated forecast
   is ever run in the paper. Reading discipline for any future C8
   market-book factor or C1-L2 compression statistic: the statistic's
   mechanical correlation with the price path must be stated and, where
   non-trivial, bounded by construction before any attribution to
   microstructure signal is admissible. No queue change.

3. [interpretation caution] The "outperforms Z-score" claim (PDF pp. 14-19)
   confounds detector with representation: the momentum method scores its
   own constructed cumulative time series, while the Z-score baseline scores
   raw per-order sizes — different inputs, different units, different
   populations (36,000 sampling intervals vs 768,270 order records, PDF
   pp. 14-16). No ROC, no labelled positives in the real data (none exist,
   PDF p. 12), no false-positive rate is quantified for either method on
   real data; the real-data detections are the ten largest deviations
   eyeballed and reverse-traced (PDF pp. 14-15), with the layering
   attribution resting on an identical-order-size cluster inference (124
   records of size 29,000, PDF p. 15). If a manipulation-adjacent
   descriptive layer ever exists in this programme, it must carry its own
   labelled ground truth and a same-representation baseline; this paper can
   supply neither. No queue change.

4. [source-quality note] arXiv v1, zero recorded citations in the
   acquisition index, no published version recorded — check before any
   formal citation. The index spells the second author "Polukarova" while
   the PDF title page spells "Polukarov" (PDF p. 1). The v1 shows
   timestamp-format irregularities consistent with a rushed draft
   (e.g. "18:36.13.59", "23:23.22.81", "23:27.43.83" mixed with
   "19/04/2022" vs "20/04/2022" period descriptions for the same BTC
   window on PDF pp. 7 and 17, and figure 12 dated 2023 in its caption,
   PDF p. 18). None of this affects the argument mechanics, but the
   empirical claims carry no evidential weight in this programme
   regardless (the library is ammunition, not evidence).

5. [cost-survival ammunition] The paper's own market-design observation —
   spoofing is profitable mainly in thin books, since liquid markets would
   demand larger, costlier spoof orders, and spoof layers are placed near
   but outside the active window to avoid execution ("spoofers would
   normally tend to place the spoofing orders outside the active area but
   not very far", PDF pp. 11-12) — is recorded only as an assumption class
   a future K7-style cost-survival or manipulation-hygiene layer would have
   to carry (window geometry and its regime dependence); never
   operationalized, nothing armed.

## What this paper would have killed if we had done it wrong

If the programme had no estimator-identity discipline, this is exactly the
paper that launders a constructed statistic into a discovery: "momentum
mirrors the midprice" would have entered the record as evidence that the
book carries price signal, when the correlation is in the construction
(eqs. 1-5, PDF pp. 4-6); "outperforms Z-score across LUNA and Bitcoin"
would have entered as a validation, when the comparison changes both the
statistic and the data population between arms and the positives on real
data are self-labelled by the same procedure that scores them. A C1-L2
compression statistic built on similar ingredients — an analyst-chosen
depth window, an unexamined event clock, a signed size-times-distance
aggregate — would survive its own kill lines for construction reasons and
fail them nowhere, which is the most expensive way a programme can die.
The pre-registration discipline, the already-queued flow-clock
scale-constant and the scale/window declaration family are the existing
immune response; this paper is a second confirmed case of the disease they
were built against, not new medicine.

## Standing caveat

Everything empirical here is one exchange (Coinbase websocket L3), two
crypto pairs, one crash day plus one one-hour BTC window, an unregulated
venue, unvalidated synthetic insertions, and a v1 arXiv draft with the
irregularities noted above. The physics vocabulary adds no identification
power the construction does not already contain. Nothing in this paper is
admissible as support for any programme claim; it is usable only as a map
of failure modes (analyst window geometry, clock choice, mechanical
target correlation, self-labeled detection baselines) that C1-L2 and C8
pre-declarations must continue to fence off.
