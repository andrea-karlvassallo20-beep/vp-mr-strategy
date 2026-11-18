# Deep-read session 13 — Fabre & Challet, "Learning the Spoofability of Limit Order Books With Interpretable Probabilistic Neural Networks"

Null-time session 15 (deep-read 13, parallel-fire slot, offset honored). Timothée Fabre (MICS, CentraleSupélec / SUN ZU Lab) & Damien Challet (MICS, CentraleSupélec); arXiv:2504.15908v1, 23 April 2025. Whether a Hawkes-inspired limit-order-flow feature set with explicit posting-distance kernels predicts the one-second mid-price move distribution on Coinbase Level-3 data, and whether a spoofer's expected-cost function computed from that model flags manipulative depth in real time.

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8 faster, or change
their kill lines? Source: legally acquired OA copy
(docs/library/text/x2aee07_learning_the_spoofability_of_limit_order_books_wit.txt, 22 pp.,
page-marked). Pre-assigned triage entry (score 34), verified this session to be UNREAD: no
prior note for this slug exists in paper/research/library/ and no open or merged PR covers
it at session start. NB (source-quality, stated up front): the assigned task brief called
this "Probabilistic Logic Programming"; the actual paper, per the extract (PDF p. 1) and the
expanded index, is "Interpretable Probabilistic Neural Networks" — same slug, correct text,
mislabelled title in the assignment only.

## The paper in one paragraph

The authors build order-flow features as exponentially decayed sums over past limit and
marketable order arrivals, with kernels phi_{beta,eta}(t,v,delta) = e^(-beta t) v e^(-eta delta)
and psi_beta(t,v) = e^(-beta t) v (Eqs. 5–12, PDF pp. 4–5): three time scales beta in
{10,100,1000} per second, four distance scales eta in {0.001,0.1,1,10} per bp, both book
sides, giving 30 flow features plus the spread (PDF pp. 6–7). A one-hidden-layer neural
network predicts the parameters of a skewed Gaussian for the one-second mid move, trained
per asset (BTC-USD, ETH-USD; Coinbase Level-3 via SUN ZU Lab, 1M orders train / 1M
validation, time-sorted split, Box-Cox normalization fitted on training only; PDF
pp. 6–7). Partial dependence recovers the spread–volatility linearity of Madhavan/Wyart
(Fig. 1, PDF pp. 7–8) and monotonic responses in log-imbalance features I_LO, I_MO
(Eqs. 22–23, Figs. 2–5, PDF pp. 8–10). Counterfactual insertion experiments (rewriting
the feature vector as if an order of size Q at distance delta had/had not been posted;
Eq. 24, PDF p. 10) show significant positive Sharpe-ratio impact for bid orders, negative
for asks, increasing in Q, decreasing in distance, but statistically nonzero up to ~10 bps
from touch for large BTC-USD asks (Figs. 6–7, PDF pp. 10–11); cross-asset, BTC orders
move ETH more than the reverse (Figs. 8–9, PDF pp. 11–12). Section 3 turns the predicted
price-move distribution into a spoofer's expected cost under first-passage execution
(Eqs. 27–30, Assumptions 1–3, PDF pp. 11–14) and flags as suspicious any large order
(Q >= 4,500 USD) whose insertion improves the spoofer's expected cost; run over 88.3M
orders (2024-12-04..07), 31% of large orders are flagged "could spoof" (PDF pp. 14–15;
Table 1, PDF p. 19).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER RATIFICATION.

1. [reinforcing, no new item] The two-null admission rule's queue-imbalance comparator
   gains mechanistic support. The paper's own detection output shows spoofers almost
   never post at the best queue: 0% of large suspicious orders at top-of-book vs 4.20%
   of large normal orders (Table 1, PDF p. 19), exactly because top-of-book execution
   risk is the highest (PDF pp. 3, 12–13). The Gould–Bonart Eq. 7 comparator (the two-null
   admission rule, joined 2026-11-18) is built from best-queue depths only, so on an
   unregulated venue the manipulable pressure it cannot see is the pressure spoofers do
   not put there. This licenses nothing new; it hardens the existing rule's rationale
   without touching its text.

2. [candidate sharpening, PENDING OWNER RATIFICATION] The distance-grid sign-invariance
   rule. The paper's central empirical claim is that models blind to the posting
   distance of limit orders are "not suitable to describe the data" (PDF p. 10): impact
   is monotone in distance and remains significant several bps deep (Figs. 6–7,
   PDF pp. 10–11), and flagged-manipulative depth sits at ~6.9 bps average distance vs
   ~1.0 bp for normal flow (Table 1, PDF p. 19). Pre-declaration text, tightening the
   sign-register and flow-clock scale-constant rules: any C1-L2/C8 feature computed from
   limit-order flow aggregated over book depth must (a) pre-declare its distance
   weighting (equivalently a hard depth cutoff), and (b) have its registered sign shown
   stable across a pre-registered distance grid before admission; a sign that appears,
   flips, or dies only under one distance weighting is a depth-blindness artifact, not a
   signal. Harder to pass because a depth-aggregated flow feature can no longer inherit
   significance from one arbitrary aggregation radius: it must survive perturbation of
   that radius, and a manipulative-depth confound (non-bona fide pressure several bps
   from touch) now has a named, pre-registered test it must fail. Reading-side
   amendment only; nothing is measured during null time and the owner ratifies or
   kills it.

3. [interpretation caution] The paper's market order flow M_b counts sell marketable
   orders hitting the bid (definition, PDF p. 4), so its I_MO partial dependence —
   "a higher market order flow imbalance leads to a smaller expected price movement"
   (Figs. 4–5, PDF pp. 8–10) — is a sign-convention statement (aggressive SELLING
   drives the mid down), not "buy flow predicts down". Any port of marketable-flow
   imbalance into C1-L2 must fix the initiator-side sign map in the pre-registration,
   before estimation, or a sign error here would fabricate a reversal where there is
   none. Extends the sign-register rule (session 12) to this feature family.

4. [cost-survival ammunition] If a K7-style cost-survival layer ever exists, it must
   carry the assumption that on venues without surveillance some fraction of apparent
   book-depth pressure is non-bona fide: orders flagged spoofable are followed by
   significantly larger realized one-second moves (avg 0.11 bp, skew 0.45, vs 0.02/0.02
   for normal orders; Table 1, PDF p. 19), i.e. apparent pressure that executes the
   spoofer's bona fide opposite side and then unwinds. A cost model that treats all
   displayed depth as real liquidity understates adverse execution. Relevant only if
   that layer is ever built; nothing queued.

5. [source-quality note] Grade plainly. Strengths: normalized inputs fitted on
   training only, time-sorted validation split, closed-form cost with semi-analytic
   fill moments (PDF pp. 6–7, 21–22). Weaknesses: the price-response t-statistics are
   computed over N = 10 sampled points per (Q, distance) cell (PDF p. 10); the model is
   trained on one week of December 2022 and applied without drift test to December
   2024 detection data (PDF pp. 7, 15); the 31% headline (PDF p. 15) is an
   expected-gain-conditioned label, not observed or prosecuted manipulation — the
   authors themselves say it flags "suspicious", not spoofing (PDF p. 14); no ground
   truth, no trader IDs (PDF p. 14); Assumption 1 (no partial fills) is acknowledged
   false for the large non-bona fide order (PDF pp. 11–12). arXiv v1 (23 April 2025);
   the text labels itself the first study of the distance kernel's shape — treat all
   magnitudes as single-venue, single-week evidence and check the published version
   before formal citation.

## What this paper would have killed if we had done it wrong

Three artifacts the existing discipline avoided. (a) Depth-blind flow features: had
C1-L2 been specified with limit-order flow summed over depth at an arbitrary cutoff, the
paper's Figs. 6–7 and Table 1 show that cutoff silently decides how much manipulable
pressure the feature drinks in; finding 2 exists precisely because the party would have
been undetectable at any single radius. (b) The 31% headline: read as evidence that
manipulation is rampant rather than as "31% of large orders improve a modelled
manipulator's expected cost under assumptions we did not ratify", it could have imported
an unscaled fear into C8's manipulation arm and moved a contamination threshold on mood.
(c) The sign trap in finding 3: a rushed port of "market order flow imbalance predicts
down" would have handed C1-L2 a sign-inverted feature that then "fails" its sign guard
and burns a kill line on a transcription error, not a market fact. The library is
ammunition, not evidence: nothing measured here.

## Standing caveat

Coinbase BTC-USD/ETH-USD only (unregulated CEX, Level-3, two weeks of data across two
years); execution modeled as mid-price first passage over the limit price, a
simplification the authors adopt for tractability (Assumption 2, PDF p. 12); fees set to
Coinbase's highest tier; the detection rule is unsupervised and its false-positive rate
is unquantified against any ground truth; the paper is arXiv v1 with zero citations on
record at acquisition. None of its magnitudes transfers to regulated equities or to a
maximal-small-tick perp without re-earning; the direction of its lesson (distance is a
first-class variable of limit-order flow) is the only thing carried forward, as a
candidate rule that is harder to pass and that the owner alone can ratify.
