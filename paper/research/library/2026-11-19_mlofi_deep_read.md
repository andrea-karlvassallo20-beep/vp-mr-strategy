# Multi-Level Order-Flow Imbalance in a Limit Order Book — deep-read note

Paper: Ke Xu, Martin D. Gould, and Sam D. Howison (Mathematical Institute,
University of Oxford), "Multi-Level Order-Flow Imbalance in a Limit Order
Book" (arXiv:1907.06230v2 [q-fin.TR], v2 stamped 26 October 2019, dated 29
October 2019; the acknowledgements thank an anonymous reviewer, suggesting a
refereed version may exist; NOT checked at reading — uncertain, flagged for
verification). Triage: score 29, slug
x09d0b5_multi_level_order_flow_imbalance_in_a_limit_order_
(edge_triage_scores.json). Extract: docs/library/text/x09d0b5_multi_level_order_flow_imbalance_in_a_limit_order_.txt,
32 pages, page-marked, complete; read in full.

Read line: Library deep-read session 47, null-time session 51, 2026-11-19.
Selected per the previous session's pointer (score 29, x09d0b5), re-verified
unread against all 47 library notes on main and against the open PR set
(only the closed, superseded PR 219 remains) at read time. Read against the
ONE question: what here would kill C1-L2 or C8 faster, or change their kill
lines?

Session-state note declared before the read: this successor session replaced
an abandoned session that had consumed the x618573 variance-Hawkes target
while a parallel slot-24 session merged the same target onto main
independently (log entry ## 54, note
2026-11-19_variance_hawkes_energy_deep_read.md). Per the standing rule, the
duplicate session was abandoned before merge: PR 219 closed unmerged with a
supersession comment, its branch deep-read-46-variance-hawkes-energy is
dormant and must never be merged, and this session took the queue's next
UNREAD entry (x09d0b5) instead. The initial target (x798515, compound
Hawkes LOB order-size) from a stale state read was detected as already
covered by a prior session before any push; its leftover branch
deep-read-21-compound-hawkes-lob-order-size is likewise dormant and must
never be merged.

## The paper in one paragraph

The authors extend the Cont-Kukanov-Stoikov (2014) OFI from the best quotes
to a vector MLOFI over the first M populated price levels on each side of
the book (Eqs. 9-12, PDF pp. 8-9; when M = 1, MLOFI = OFI), computed
exactly on Nasdaq LOBSTER event data (no TAQ estimation), for 6 liquid
stocks spanning relative tick sizes (AMZN, TSLA, NFLX small-tick; ORCL,
CSCO, MU large-tick), all of trading year 2016, 10:00-15:30 only, first and
last 30 minutes excluded, hidden-liquidity events excluded (PDF pp. 10-11).
On a grid of 10-second windows inside 30-minute windows (2772 regressions
per stock), they fit the contemporaneous linear model
deltaP = alpha + sum_m beta_m MLOFI_m + eps (Eq. 16, PDF p. 14) first by OLS
then by Ridge. Under OLS the beta_m are weakly significant and unstable;
the MLOFI components are strongly multicollinear (sample correlations above
0.5 for the small-tick stocks and above 0.7 for the rest; eigenvalue ratios
near 0; Figs. 1-2, PDF pp. 16-18), so OLS "may produce a misleading picture"
(the authors' own words, PDF pp. 16-17). Ridge with lambda chosen by 5-fold
cross-validation over 50 log-spaced candidates (Table 7, PDF p. 19) gives
strongly significant beta_m (Table 9, PDF p. 21), monotonically decreasing
in m for small-tick stocks but roughly flat for large-tick stocks. Goodness
of fit improves with each added level under both adjusted R2 (in-sample,
Fig. 4, PDF p. 22) and out-of-sample RMSE (5-fold, Figs. 5-6, PDF pp.
23-25), with out-of-sample RMSE improving 59-74 percent for large-tick
stocks and 15-31 percent for small-tick stocks at M = 10 versus OFI alone
(Table 10, PDF p. 26); OLS overfits for AMZN/TSLA (out-of-sample RMSE rises
for M above about 5, PDF p. 24), which Ridge counteracts. The authors
discuss mechanisms (informed traders placing limit orders deep in the book
to avoid information-leakage costs; cancellations behind the best quotes
enabling larger mid-price moves) as possible explanations only (PDF pp.
26-27).

## Findings, graded (does any kill line move?)

NO kill line changed. NO new candidate sharpening. Every finding reinforces
standing rules or already-queued sharpening candidates; nothing met the
burden for a new item, and nothing armed.

1. [reinforcing, no new item] The headline relationship is CONTEMPORANEOUS,
   not predictive. MLOFI and the mid-price change are measured over the SAME
   10-second window (Eqs. 16-17, PDF p. 14; PDF pp. 12-13), and mid-price
   changes are, mechanically, consequences of the very order-flow events
   MLOFI aggregates: a fit of this kind is an accounting decomposition of
   same-window book updates, not evidence that order flow at time t
   forecasts price at any later time. For large-tick stocks the adjusted R2
   at M = 10 is "very close to 1" (PDF p. 23) precisely because the
   relationship is close to mechanical once enough levels are included. Any
   future citation of this paper as "deep-book order flow predicts price"
   would launder contemporaneity into prediction, exactly the category the
   standing direction-versus-magnitude and vol-tautology/identity kill
   lines (C1-L2 lines 2/5, C8's K8 battery) exist to catch. No rule moves;
   the identity family already binds.

2. [interpretation caution] The paper is itself a worked specimen of the
   estimator-discipline family (already-queued candidates through deep-read
   43): the SAME data and the SAME declared functional yield
   opposite-looking beta tables under OLS versus Ridge (Tables 5-6 vs
   Tables 8-9, PDF pp. 15, 20-21) purely through the estimator choice, and
   the authors reverse a published conclusion (the Cont et al. 2014
   appendix finding that only near-best-quote flow matters) partly by
   switching from in-sample adjusted R2 to out-of-sample RMSE (PDF pp.
   22-26). Discipline for the programme: any future multi-feature
   microstructure regression on collinear flow features must disclose the
   estimator, the regularization hyperparameter and its selection protocol
   (the queued optimizer-path/estimator-identity candidates cover this),
   and an in-sample goodness-of-fit statistic may never be the reported
   success metric. No new item; the queued estimator-discipline
   sharpenings already encode exactly this failure mode.

3. [interpretation caution] Fitted quantities are venue- and
   regime-specific to a degree the paper itself demonstrates: beta_m decay
   shapes, lambda values (139.0 for AMZN down to 1.3 for CSCO, PDF p. 19),
   R2 levels and RMSE improvements all split by relative tick size (PDF pp.
   21-26), and the same MLOFI vector maps to different mid-price outcomes
   when the spread exceeds one tick (limit order inside the spread vs at
   the best queue; one tick inside vs many ticks inside — the authors' own
   two degenerate-mapping explanations, PDF pp. 27-28). No beta, no
   lambda, no R2, no RMSE improvement transfers to the programme venue; a
   BTCUSDT perp book with a different tick/fee/queue regime is exactly the
   cross-venue import the house rules forbid. The feature itself
   (depth-indexed net flow) remains admissible as a declared input on the
   programme's own data, never on this paper's coefficients.

4. [parameter-sensitivity note] The authors' own sensitivity pass matters:
   for small-tick stocks the adjusted R2 varies by about 10 percent across
   window-length choices and INCREASES with both window lengths (PDF pp.
   12-13), and intraday seasonality shifts beta_1 for the two largest-tick
   stocks (PDF pp. 29-30). A fitted flow-property conclusion that moves
   with the sampling grid is a grid artifact until shown otherwise;
   reinforces the standing parameter-sensitivity rule (conclusions must be
   shown stable across reasonable window and grid choices), and the
   discretized-conditioning/queue-label declaration candidates (deep-read
   sessions 32/33) already cover the analogous disclosure duty.

5. [economic-gate note] The paper's own significance discussion (PDF pp.
   28) concedes the incremental RMSE improvements (down to about 0.002
   ticks between M = 9 and M = 10 for MU) are meaningful only "for a
   trader operating high-frequency trading algorithms" executing "many
   thousands of times per day". Market-making/HFT execution contexts are
   never operationalized by this programme (standing rule); nothing here
   approaches a spread-plus-costs economic gate at any horizon the
   programme measures, and the paper claims nothing at any horizon at
   all — everything is same-window.

6. [source-quality note] Clean, unusually transparent empirical
   microstructure paper: exact event data (LOBSTER, Nasdaq-native, no
   estimation of order flow), OLS-vs-Ridge shown openly, overfitting
   exhibited rather than hidden, limitations stated in the authors' own
   text. Weaknesses for citation purposes: 6 stocks, one venue, one year
   (2016), single-venue flow only (off-Nasdaq flow ignored, PDF pp.
   10-11), hidden-liquidity events excluded (PDF p. 10), M capped at 10
   without an explicit selection rule, and an acknowledgements-only
   review trail. A published version (possibly Quantitative Finance) was
   NOT verified at reading (uncertain, flagged for verification).

## What this paper would have killed if we had done it wrong

Had "out-of-sample RMSE improves with every added depth level (Table 10)"
been cited as evidence that the deep book carries anticipatory information
about future price, a contemporaneous accounting fit — whose inputs and
outputs are measured over the same 10 seconds, and whose near-R2-of-1 for
large-tick stocks is close to bookkeeping — would have been laundered into
a compression-clock claim it never makes; the first horizon-explicit test
would have killed it and the proxy-identity battery exists precisely so
this laundering cannot enter a spec. Had the Ridge beta tables entered any
spec table as if they were stable deep-book loadings, a
multicollinearity-conditioned estimator artifact (the authors' own Tables
5-8 show the OLS version of the same fit is unstable) would have anchored
venue parameters on a tick-regime the programme does not trade; the
cross-venue import ban kills this before it starts. Had the lambda values
or the M = 10 choice been imported as defaults, a CV-tuned, stock-specific
hyperparameter would have traveled as a constant; the estimator-discipline
and discretized-conditioning declaration candidates (both queued, both
PENDING OWNER RATIFICATION) exist to force such choices to be declared on
TRAIN instead of imported. Grade: no kill line changed; no candidate
sharpening; zero armed.

## Standing caveat

A library is ammunition, not evidence. Six Nasdaq equities, one year
(2016), one venue's flow, 10-second same-window contemporaneous fits,
hidden liquidity excluded, first and last 30 minutes of each day excluded,
M capped at 10, lambda CV-tuned per stock, and every headline number
(Q tables 3-10, lambda values, beta shapes) is a function of tick regime,
sampling grid and estimator choice. No crypto, no perps, no
funding-rate mechanics, no L2 replay observables in the programme's sense.
Nothing in this paper enters any spec, default, kill line, threshold, or
calibration; it charges warnings only.
