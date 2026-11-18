# Library deep-read session 19 — Maciejewski, "Packets, Transactions and
# Queues: Design Principles for HFT Systems from a Measurement Study
# of CME Market Data" (arXiv:2609.32848v2, 2026; M2 Tech Montreal;
# ~110 pp. measurement study of the CME MDP3 feed for NQ, a year of
# sessions, billions of packets)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/xc5ba34_packets_transactions_and_queues_design_principles_.txt`,
page-marked). Next UNREAD triage-rank entry (score 34). This is an
HFT-systems infrastructure paper, not a market-microstructure claim;
the read is for what it implies about RECORDED data's timestamps.

## The paper in one paragraph

Every packet and every matching-engine transaction in a year of CME
NQ front-month market data is followed through the two exchange
timestamps (engine and market-data publisher) to a receiver
(Abstract, PDF p. 1; Part II). Findings: packets arrive in
near-critical self-exciting clusters, and the clustering belongs to
the MATCHING ENGINE'S TRANSACTIONS, not to the exchange's packing
(almost every transaction fits in one packet); the engine often
processes consecutive transactions within a fraction of a
microsecond, with "the signature of a race after trades"; the
market-data publisher behaves as a queue that sends at most one
packet per publisher period (~7.5 microseconds), and when the
engine bursts, its delay grows about tenfold while it drains the
backlog with MORE packets rather than larger ones — so an engine
burst reaches any receiver as a train of single-message packets one
publisher period apart (PDF pp. 1, 56-65). The bulk of the paper is
receiver-design engineering: queueing tails, tandem/threading
analysis (the single-thread rule reverses above the publisher
period), and design recommendations — explicitly scoped by the
author: "why orders reach the engine so close together is a
question about the market and is not addressed here" (PDF p. 1).

## Findings, graded (does any kill line move?)

**NO kill line changes. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand. The program never
trades live, so the paper's engineering content does not touch it;
the read yields one genuinely relevant caution and two smaller
notes:

1. **[interpretation caution for the L2 features] The delivery
   pipeline lives in the timestamps.** The feed between a venue's
   matching engine and any recorded dataset is a QUEUE with its
   own pacing (one packet per ~7.5-microsecond publisher period
   on CME) and its own backlog behavior (more packets, not bigger
   ones, under burst). Recorded interarrival structure at fine
   grains is therefore a SUM of market structure and delivery-
   pipeline structure, and the pipeline term is not negligible by
   construction — it is the transport. For the program's gated
   BTCUSDT windows: any feature that reads fine-grain arrival
   timing (interarrival hazards, arrival clustering) measures
   the PIPE until proven otherwise, and the Layer 0 gate's
   ground-truth comparison (independent book_snapshot_25
   snapshots) is precisely the control that separates the two.
   Recorded as interpretation language for the feature layer:
   arrival-timing features carry a pipeline caveat, and Binance's
   pipeline geometry is its own — the ~7.5-microsecond publisher
   period is CME's number, not a constant.

2. **[reinforcing, no new item] Engine-layer "near-critical"
   clustering is an infrastructure observation, not market
   evidence.** The feed's packet arrivals are near-critical
   self-exciting — but the author is explicit that the origin is
   the racing of transactions at the engine, and that the
   interpretation of that racing belongs to market research, not
   this paper. A near-critical branching reading computed on
   arrival timestamps could therefore carry pipeline/engine
   structure rather than market endogeneity — one more instance
   of the exogenous-absorption caution (session 17), here with
   the absorbing layer being hardware. Goes to the interpretation
   table beside any arrival-clustering reading.

3. **[reinforcing, no new item] Races after trades as the burst
   origin.** The paper's measured "signature of a race after
   trades" sits in the same mechanism family as the quote-race /
   front-of-book interpretation carried by C5 (front-of-queue
   priority) and the intraday OFI read (aggressive submission
   around information): at microsecond scales, competing actors
   respond to the same event nearly simultaneously. Recorded as
   interpretation language; nothing armed.

## What this paper would have killed if we had done it wrong

If a trigger-layer feature had been built on fine-grain arrival
timing without the Layer 0 gate's ground-truth check, the
pipeline's queueing structure (pacing, backlog trains) would have
been laundered into "market clustering" readings — an artifact no
label placebo could catch, because it lives in the TRANSPORT, not
the generating process. The program's gate (independent snapshot
comparison) and its feature discipline already stand between that
error and the record; this read is the citation that the transport
has measured, non-trivial structure worth gating against. Grade:
**no kill line changed; no candidate sharpening; one interpretation
caution (pipeline-in-the-timestamps) and two reinforcing notes;
the ratification queue stands at FOURTEEN candidates, zero armed.**

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launderers. The paper is single-vendor (CME MDP3), single-contract
(NQ front month), with packet captures that are explicitly
non-redistributable and a live check on the author's own production
receiver; the ~7.5-microsecond publisher period and the
more-packets-not-bigger-ones backlog behavior are CME's facts, and
Binance's pipeline geometry must be measured, not assumed from
them. The paper's own scope note — market interpretation excluded —
is respected here: nothing in this note treats its measurements as
evidence about the MARKET. arXiv v2 (Oct 2026), an industry author's
open-systems companion piece (Kaspar-HFT), not peer reviewed —
check before formal citation.
