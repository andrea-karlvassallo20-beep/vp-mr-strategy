# Deep-read session 14 — Petukhina, Reule & Härdle, "Rise of the Machines? Intraday High-Frequency Trading Patterns of Cryptocurrencies"

Null-time session 16 (deep-read 14, offset honored). Alla A. Petukhina, Raphael C. G. Reule,
Wolfgang Karl Härdle, Humboldt-Universität zu Berlin; arXiv:2009.04200v1, 9 Sep 2020
(post-peer-review, pre-copyedit version of an article published in The European Journal of
Finance, DOI 10.1080/1351847X.2020.1789684, PDF p. 2). A descriptive stylized-facts study of
5-minute cryptocurrency data asking whether intraday trading patterns are machine-shaped or
human-shaped, arguing via time-of-day and day-of-week seasonality ("Proof-Of-Human") that
the market of mid-2018 was still predominantly human-driven.

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8 faster, or change
their kill lines? Source: legally acquired OA copy
(docs/library/text/x2a7ad5_rise_of_the_machines_intraday_high_frequency_tradi.txt, 31 pp.,
page-marked). NB: a PARALLEL-FIRE SLOT ASSIGNMENT (slot 12 of 24), declared as such — not the
queue's standing top pointer; that pointer is unchanged (see the read-line's last sentence).
Triage trace: this slug scores 33 in the 500 triage; the queue's next UNREAD triage pointer
remains "Price-Aware Automated Market Makers" (score 39).

## The paper in one paragraph

The authors analyze 5-minute intervals, 1 July – 31 August 2018, over 11 major coins
(BCH, BTC, DASH, ETC, ETH, LTC, REP, STR, XMR, XRP, ZEC; appendix PDF p. 23), with data
from CRIX and dyos solutions GmbH, both Europe-based (+1 GMT; PDF pp. 5–6), i.e. the
post-cooldown 2018 summer chosen deliberately as a corporate-vacation period expected to
favor the algorithmic hypothesis (PDF pp. 6, 15). Method: summary statistics and GAM fits
(generalized additive models with cubic regression splines for daily and P-splines for
weekly seasonality; Eqs. 3–7, PDF pp. 7–8) of absolute returns, volatility and trading
volume against time-of-day and day-of-week (Sec. 3.3, PDF pp. 15–18). Findings: return
distributions are leptokurtic far beyond equity norms (excess kurtosis 8.12–49.44, JB
rejects normality everywhere; Table 1, PDF p. 12); first-order return autocorrelation is
near zero and mostly negative (−0.09 to +0.01) while squared/absolute-return
autocorrelation is positive (0.11–0.27) — quiet periods follow quiet, dynamic follow
dynamic (PDF pp. 12–13); the daily seasonality curves dip at night, rise through the
European morning, flatten around lunch, peak 17:00–20:00, then decline (PDF p. 16); weekly
activity peaks Tue–Thu and drops on weekends in returns, volume and volatility (Figs. 8–10,
PDF pp. 16–18). Against their own expectation band (a machine-dominated market should be
time-independent; the transitional-system argument, PDF p. 15), they conclude the market
was still "firmly in the hands of humans" (closing remarks, PDF pp. 19–20).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The diurnal/weekly seasonality finding independently
   corroborates two items already on record, from a third market and venue type: GAM
   smooth terms are highly significant while their explanatory power is ~1% (PDF p. 15),
   with the human-shaped intraday curve (nighttime trough, 17:00–20:00 peak, PDF p. 16)
   and weekend decline (Figs. 8–10, PDF pp. 16–18). This is venue evidence for session
   9b's hour-of-day stratification and for the MMHP session's seasonality protocol
   (both already queued/on record); nothing is added to any queue, and no existing rule
   is tightened — the paper offers no estimator, no test, and no threshold to import.

2. [interpretation caution] The Proof-of-Human headline is a shape inference, not a
   measured share. "The impact of 24/7 algorithmic trading is rather negligible" (PDF
   pp. 19–20) follows from seasonality CURVES that explain ~1% of variation (PDF p. 15),
   in one two-month European vacation window at 5-minute grain, with no direct
   algorithm-share measurement anywhere in the paper. The reading discipline: agent-mix
   statements about our venue (or any venue) may never be imported from seasonality
   shape alone; at most they are regime hints, and this paper is the page-cited worked
   example of how weak that inference is (a smooth can be significant and carry almost
   nothing). Corollary for session 6's fragility item: the "market running
   homogenized imbalance signals" premise is regime-dated — evidence about 2018 spot
   says nothing about 2024–25 perps' agent mix, in either direction.

3. [interpretation caution] The on-chain/off-chain passage (PDF p. 19) argues that
   market behavior cannot be predicted from on-chain data alone, because exchange order
   books are off-chain and the blockchain's blocktime only bounds settlement visibility.
   Read as: on-chain variables are not admissible substitutes for L2 book state. This
   reinforces the existing proxy-refusal layer (session 3's taker-proxy refusal family);
   no queue change.

4. [reinforcing, no new item] The autocorrelation table (Table 1, PDF p. 12) at 5-minute
   grain on 2018 spot: near-zero, mostly negative first-order return autocorrelation with
   strongly positive absolute/squared-return autocorrelation. Quiet-then-quiet/large-
   then-large clustering is consistent with the compression premise's volatility-clustering
   motivation — but it is a stylized fact at a different grain (5m vs our 30m–4h–24h), a
   different era, and a different instrument class, so it is context for the C1-L2
   motivation, never support for any claim. The library is ammunition, not evidence.

## What this paper would have killed if we had done it wrong

Read without discipline, this paper carries two opposite launderings. (a) Its headline
("machines negligible, humans drive the market") could have been imported as evidence
that high-frequency microstructure does not matter in crypto — which would quietly
undermine the motivation for the entire L2 phase, C1-L2 and C8 included, on the strength
of a seasonality-shape argument whose own R² is ~1%. (b) Its speculative cascade
passage — a false-positive "learning" algorithm dumping an asset and triggering a
waterfall among blockchain-reading algorithms (PDF p. 19) — could have been laundered as
if it were near-criticality evidence for the Hawkes/branching trigger line, when the
paper's own Table 1 shows near-zero first-order return autocorrelation at the grain it
measures. Either direction, a narrative would have been booked as evidence. The
program's existing rule — no empirical claim from any paper enters the record as support
for any program claim — is the discipline that prevented both; this note records the
paper as reinforcement and caution, nothing more.

## Standing caveat

Descriptive, single-window (July–August 2018), 5-minute aggregates only — no order book,
no event data, no trade classification, no LOB reconstruction. The data source is
European (+1 GMT), and the authors themselves flag that time-of-day effects shift with
data-source timezone (PDF p. 6): the human-shaped peak at 17:00–20:00 is a CET reading,
not a universal clock fact. The agent-mix conclusion is an inference from GAM smooths,
not a measurement of algorithmic share. The vacation-period framing was chosen to favor
the algorithmic hypothesis, but the study tests no alternative hypothesis formally.
The copy is post-peer-review, pre-copyedit (PDF p. 2): check the European Journal of
Finance published version before formal citation. Appendix oddity flagged: STR is listed
as "Stalker, staker.network" (PDF p. 23) where Stellar (STR) is the expected asset —
uncertain, marked for verification, bibliographic caution only.
