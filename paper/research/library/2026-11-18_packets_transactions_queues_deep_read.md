# Deep-read session 23: Maciejewski, "Packets, Transactions and Queues: Design Principles for HFT Systems from a Measurement Study of CME Market Data"

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8 faster, or
change their kill lines? Source: legally acquired OA copy
(docs/library/text/xc5ba34_packets_transactions_and_queues_design_principles_.txt,
~125 pp., page-marked). Next UNREAD triage-rank entry (score 34, xc5ba34).

## The paper in one paragraph

A solo-author measurement study (Maciejewski, arXiv:2609.32848v2, September 2026)
of the CME MDP3 feed for NQ front-month futures: 281 sessions, 2025-01 through
2026-02, RTH, every packet and every matching-engine transaction followed through
the two feed timestamps from engine to publisher to a receiver, cross-checked
against a 53-minute live production capture on ES/NQ/ZN seven months after the
corpus ends (PDF pp. 24, 69). Packet arrivals are near-critical self-exciting
clusters, and the clustering belongs to the matching engine's transactions, not
to packetisation: 98 percent of transactions fit in one packet, the tight gaps
between packets are gaps between different engine events, and an exponential-
kernel Hawkes fit gives branching ratio about 0.8 on packets and on transaction
starts alike, with a kernel decaying over about 160 microseconds (PDF pp. 25-26,
35-38). The publisher behaves as a deterministic-service queue of period about
7.5 microseconds, so a receiver sees an engine burst as a train of packets one
publisher period apart, and the queueing tail of a single-threaded receiver is
produced by the timing of engine transactions - not by packet rate, packet
size, or packetisation (PDF pp. 36-41, 51-59). The paper's design question is
threading architecture; its market content is one page of race signature and a
conjecture that the publisher's capacity is an information-side speed limit
(PDF pp. 63-65).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening. Default grade. The paper is a
feed-and-queueing measurement; its two mechanisms that touch the programme's
questions - a fitted near-critical branching ratio and a hard deterministic
publisher clock - are worked exhibits of rules already standing in the queue,
and the paper itself applies the two cautions those rules encode.

1. [reinforcing, no new item] The fitted branching ratio is explicitly not
   load-bearing, and the paper says why: with an exponential-kernel fit and a
   constant background over a fixed window, the branching ratio is overstated
   when the background intensity varies within the window, per the
   Filimonov-Sornette result the paper cites; the paper declares its own
   n = 0.798 "descriptive and subject to the same caveat, and none of the
   paper's conclusions rests on its value", resting its empirical claims
   instead on model-free diagnostics (short-gap share 73 percent vs Poisson
   9.5, Fano factor growing from about 50 to about 1000 with bin width, Hurst
   about 0.74; PDF pp. 25-26, Table 1). This is a worked exhibit for the two
   rules already queued from the Hardiman-Bouchaud and Markov-modulated reads:
   the estimator-mode register (a bare fitted n from the wrong estimator family
   with the wrong background treatment is not evidence of a regime) and the
   near-critical regime-disclosure rule (only the disclosed estimate chain is
   a regime). It licenses nothing new: the T-H comparison benchmark already
   carries the Hardiman-Bouchaud pre-conditions, and this paper's number is one
   more disclosure exhibit, not a programme input.

2. [reinforcing, no new item] The branching ratio is a function of the event
   definition and the clock, and the paper shows both directions at once:
   packets and transaction starts give the same n (0.798 vs 0.795, PDF p. 38,
   Table 7) only because 98.3 percent of transactions are exactly one packet
   (PDF p. 36, Table 5), so the two event streams coincide; but the same gaps
   measured on the engine clock and on the publisher clock are entirely
   different objects - 17.1 percent of consecutive engine events fall within
   one publisher period, the tightest percentile 0.18 microseconds apart,
   against 1.04 percent on the publisher clock (PDF p. 57, Table 13). A
   worked exhibit for the record's clock discipline: no branching reading from
   one clock may be pooled with or narrated alongside a reading taken on
   another, and the correlation of two event definitions is itself a measured
   fact, not an assumption. It licenses nothing new; it reinforces.

3. [reinforcing, no new item] A hard deterministic infrastructure clock hides
   inside the event process and must live in the null, not in the signal. The
   publisher sends at most one packet per period of about 7.5 microseconds; two
   packets never arrive closer, engine bursts surface as evenly spaced trains
   at exactly that period, and the receiver's tail threshold is that constant,
   not a market-state quantity (PDF pp. 59, 62; tail onset independent of packet
   rate and branching quintiles at short service times, PDF pp. 51-52). A null
   that ignored this clock would read the publisher's pacing as excitation.
   This is the same class of rule as the queued deterministic-clock null arm
   (hour-of-day, session segments, release calendar): at the programme's
   multi-hour taker-flow horizons the enumerated components are already the
   declared ones, and this paper adds no component that could exist at that
   scale; it corroborates the arm and licenses no extension of it. The 5.8
   conjecture also carries its own reading discipline, stated as a
   qualification by the author: the publisher's delay bounds the speed of an
   information cascade, not its size - "delaying feedback does not reduce the
   branching ratio" (PDF p. 65) - so the conjecture must never be cited as a
   mechanism that tames criticality.

4. [interpretation caution] The race signature bounds what a fine-scale flow
   reading can mean. Transactions across tight engine gaps are ordinary quote
   traffic in about the same mix as across loose gaps; but after a trade, the
   next transaction within microseconds is another trade about five times as
   often and a delete about half again as often as across a loose gap - the
   pattern a race leaves - while race losers never appear on the public feed,
   so the share of racing is unmeasurable in principle (PDF pp. 63-64,
   Table 19). Any future narrative in which microsecond-scale post-trade flow
   is read as informed directional activity is therefore unsupported on feed
   data of this kind: the tight post-trade cluster is compatible with a race to
   take or cancel, and the visible mix is dominated by placements and
   cancellations. This is a reading discipline for interpretation only; no
   feature, threshold, or kill line moves.

5. [source-quality note] Solo-author, arXiv v2, September 2026, zero citations
   recorded in the index, no published version located; the paper itself
   discloses substantial AI assistance (Claude Code for code, analysis,
   drafting, and figures) with the author taking sole responsibility after
   independent review of the mathematics and results (PDF p. 11, section 1.6).
   The disclosed division of labour is exactly the kind that demands the
   published version be checked before any formal citation, and the corpus is
   one instrument (NQ front month), 14 months, RTH, with a live
   cross-validation of 53 minutes on three book streams (PDF pp. 24, 69). The
   transaction-level identification is corpus-only; the live data cannot
   repeat it (PDF p. 69).

## What this paper would have killed if we had done it wrong

If the programme had read a paper reporting "branching ratio about 0.8 on CME
NQ, parallel to the literature's about 0.9" as corroboration that T-H's
threshold sits on a measured market regularity, it would have committed two
errors the standing discipline exists to block. First, importation: the number
belongs to packet and engine-event arrivals on a microsecond clock, not to the
taker-flow, multi-hour object T-H scores; the equality of packet and
transaction branching here is a property of a feed where almost every
transaction is one packet, and says nothing about coarse-aggregated flow.
Second, estimator blindness: the paper itself declares its fitted n overstated
under within-window background variation, which is precisely the failure mode
the queued estimator-mode register and the Hardiman-Bouchaud pre-conditions in
the T-H spec encode. A third error was available too: citing the publisher
speed-limit conjecture as "the exchange caps reflexivity, so cascades are
tamed" - the paper's own qualification forbids that reading, since the delay
moves the follow-on events later without reducing their number. The programme
avoided all three by keeping library numbers out of the trigger definitions
and by demanding the disclosed estimate chain.

## Standing caveat

The study is a single instrument (NQ front-month CME futures), 2025-01 to
2026-02, RTH only, pcap-reconstructed plus one 53-minute live window; the
market-facing content is one page of race signature and one conjecture, and
the author leaves open why orders reach the engine within a microsecond of
each other (PDF pp. 63, 65). Nothing here measures anything at the
programme's horizons, on the programme's instruments, or on the programme's
feature definitions; any transfer to BTCUSDT multi-hour compression windows is
mechanism-level at most and cannot carry any number from this corpus. The
fitted branching estimates carry the author's own estimator caveat and are
descriptive by declaration. arXiv v2: check published version before formal
citation. Laundering directions: INTO - no coefficient, period, decay time, or
quantile from this paper enters any spec, default, calibration, or cost
assumption, and its fitted n does not join the T-H benchmark's evidence chain;
OUT - no future reading of this paper may state that microsecond-scale
post-trade clusters are informed directional flow (the race reading is
unmeasurable against it), that near-criticality at feed granularity implies
anything at the programme's aggregation, or that publisher pacing tames
cascade size.
