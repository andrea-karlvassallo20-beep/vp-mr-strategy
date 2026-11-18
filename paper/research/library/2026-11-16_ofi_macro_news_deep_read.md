# Library deep-read session 18 — Takahashi, "Returns and Order Flow
# Imbalances: Intraday Dynamics and Macroeconomic News Effects"
# (arXiv:2508.06788v4, 2025; Hosei/Kellogg dissertation; SVAR-ITH on
# S&P 500 E-mini futures, one-second BBO data, 2008-2013)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x5459dc_returns_and_order_flow_imbalances_intraday_dynamic.txt`,
18 pp., page-marked). Next UNREAD triage-rank entry (score 34).

## The paper in one paragraph

A bivariate structural VAR of mid-quote returns and Cont-Kukanov-
Stoikov order flow imbalance, estimated at ONE-SECOND frequency
per 15-minute interval on 1,490 trading days of S&P 500 E-mini BBO
data (34.5 million second-observations), with simultaneity handled
by identification through heteroskedasticity (Rigobon's ITH, per
Deuskar-Johnson) rather than a recursive ordering (PDF pp. 1-8).
Because price changes trigger price-contingent order submission
within the same interval, plain OLS is inconsistent; the ITH
system identifies BOTH the price impact b_r (flow -> return) and
the flow impact b_f (return -> flow, the aggregation-induced
feedback), plus state-dependent innovation volatilities (PDF
pp. 6-8). Results: b_r mean 0.834 (significant in 64% of
intervals, larger at finer sampling), b_f mean 0.301 (significant
in 71%, smaller at finer sampling — "endogeneity weakens as the
measurement interval approaches the event level," PDF pp. 9, 12);
impulse responses dissipate almost entirely WITHIN A SECOND (PDF
pp. 12-13); macroeconomic announcements RESHAPE the system —
price impact rises, flow impact declines, return innovation
volatility spikes, flow innovation volatility falls (order
submission slows: liquidity withdrawal), PDF pp. 8-11; and the
intraday variation of b_r tracks 1/depth, close to the stylized
LOB benchmark of Cont et al. (PDF pp. 14-16).

## Findings, graded (does any kill line move?)

**NO kill line changes. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand. The program already
deploys the machinery this paper's findings support; the read
supplies three reinforcing citations:

1. **[reinforcing, no new item] The macro censor's existence
   quantified.** Scheduled macro announcements do not merely add
   noise — they CHANGE THE REGIME of the price-flow system (price
   impact up, flow impact down, flow innovation volatility down:
   traders withdraw submission around releases, PDF pp. 8-11).
   The program's deployed macro censor (the ex-ante timeline audit,
   the macro_censor machinery) excludes such windows on principle;
   this read is the venue citation that the principle is right in
   kind: parameters estimated across announcement boundaries are
   mixtures of two systems, not one noisier system. Nothing to
   change — the censor predates the citation.

2. **[reinforcing, no new item] Aggregation endogeneity is
   grain-dependent — a citation for the trigger layer's grain
   discipline.** Their b_f (the feedback term that makes OLS
   inconsistent) SHRINKS as the sampling interval approaches the
   event level (mean 0.301 at one second vs 0.55 at one minute in
   Deuskar-Johnson, PDF p. 12), while b_r GROWS at finer grains.
   Both directions of the simultaneity are grain-dependent. For any
   flow-based feature at the program's 30m-4h-24h grains: the
   measured impact and the measured feedback are functions of the
   aggregation, and readings from different grains are different
   objects — never compared, never mixed. This extends the
   estimator-mode and clock statements by one more dimension
   (grain), already covered in spirit by the specs' fixed grains;
   recorded as interpretation language.

3. **[reinforcing, no new item] The horizon-gap caution's cousin,
   measured.** Their impulse responses die within a second (PDF
   pp. 12-13) — OFI's contemporaneous impact at the event grain is
   real, large, and gone in under a second. This is the same
   horizon-gap discipline flagged in the CKS OFI read (session
   machinery from the null-time programme): a 1-second-horizon
   OFI result licenses nothing about 30m-4h persistence, and the
   citation is now doubly sourced. C8's unexplored cell remains
   exactly that.

## What this paper would have killed if we had done it wrong

If windows spanning macro announcement boundaries had ever been
pooled (or announcement-adjacent observations left in a training
set), the estimated coefficients would have been mixtures of two
regimes with different signs of change — and every downstream
feature built on them would inherit a structural artifact that no
placebo on labels could catch, because the artifact lives in the
WINDOW SELECTION. The program's ex-ante macro censor was already
deployed; this read supplies the measured proof that such windows
are regime boundaries, not noise. Grade: **no kill line changed;
no candidate sharpening; three reinforcing citations (macro-censor
quantified; grain-dependence of aggregation endogeneity;
sub-second dissipation); the ratification queue stands at FOURTEEN
candidates, zero armed.**

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The venue is a single deep liquid equity-index future
with a near-constant one-tick spread (PDF p. 4, Table 1) — the
nearly-always-minimum spread means the depth channel dominates the
impact channel, a property BTCUSDT perps do not share; the ITH
identification assumes impact parameters constant WITHIN each
15-minute window while only volatilities shift (PDF pp. 7, 12) —
exactly the kind of within-window constancy the program's drift
reporting exists to question; and 37,029 of 38,740 intervals passed
the rank condition, meaning ~4% of windows were silently dropped —
a window-selection step the program's pre-registered windows would
have to declare. arXiv v4 (Oct 2025); a dissertation-derived
working paper — check for the published version before formal
citation.
