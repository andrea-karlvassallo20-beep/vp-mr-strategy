# Deep-read session 22 — Takahashi, "Returns and Order Flow Imbalances: Intraday Dynamics and Macroeconomic News Effects"

Library deep-read session 22 (null-time session 26, log entry ## 30).
Makoto Takahashi (Faculty of Business Administration, Hosei University,
Tokyo; a Northwestern/Kellogg dissertation chapter, committee Torben
Andersen, Viktor Todorov, Robert Korajczyk, Beth Andrews), arXiv:2508.06788v4
[q-fin.TR], 8 Oct 2025, 18 pp.: a bivariate structural VAR of one-second
mid-quote returns and Cont-Kukanov-Stoikov order flow imbalance in the
S&P 500 E-mini futures (CME BBO files, 1,490 trading days, Jan 2008-Dec
2013, 8:30-15:00 Chicago time), identified through heteroskedasticity
(SVAR-ITH, Rigobon 2003; the Deuskar-Johnson 2011 framework), estimated
separately for each 15-minute interval (37,029 valid interval fits out
of 38,740), with the estimated structural parameters regressed on
scheduled macroeconomic announcement dummies and market activity.

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x5459dc_returns_and_order_flow_imbalances_intraday_dynamic.txt,
18 pp., page-marked). Next UNREAD triage-rank entry (score 34).

## The paper in one paragraph

At the one-second clock the contemporaneous return-flow pair is a
simultaneous system: order flow imbalance moves the mid (price impact
b_r, liquidity's inverse) and the mid simultaneously triggers
price-contingent order submission (flow impact b_f), so OLS on either
direction is inconsistent whenever the other coefficient is nonzero (PDF
p. 7), and identification comes from heteroskedasticity across nested
five-minute states inside each 15-minute window (PDF pp. 7-8). The
fitted system says both directions are real at one second — b_r mean
0.834, significant in 64 percent of intervals; b_f mean 0.301,
significant in 71 percent (Table 3, PDF p. 12) — with magnitudes ordered
by the sampling clock in the direction Deuskar-Johnson predict: b_r is
larger than their one-minute 0.474 ("shorter sampling intervals capture
stronger contemporaneous impacts", PDF p. 12) and b_f smaller than their
0.55 ("endogeneity weakens as the measurement interval approaches the
event level", PDF p. 12). Impulse responses dissipate almost entirely
within one second (Fig. 3, PDF pp. 12-13; quotes reach new levels after
roughly 20 events, per Hautsch-Huang, and the sample averages 45 events
per second, PDF p. 4), the long-run impact of a unit flow shock is
consistent with the stylized Cont-Kukanov-Stoikov 1/(2D) benchmark (the
depth-reciprocal elasticity of fitted b_r is 0.553, PDF pp. 14-16,
Table 5). Macroeconomic announcements reshape the whole structure: price
impact rises on the interval BEFORE the release (ANN_t-1 = 0.129,
p<0.01) and further under negative surprises (0.136, p<0.1), flow impact
falls on and before the release (-0.033, -0.078, p<0.01), return
innovation volatility spikes at release (0.066, p<0.01) while flow
innovation volatility declines on and before it (-0.039, -0.057,
p<0.01/0.05) — traders withdraw and pause BEFORE the stamp (Table 2,
PDF p. 11; Fig. 2, PDF p. 10) — although the announcement dummies add
little to adjusted R-squared beyond market activity variables (PDF p.
9), most structure being carried by depth, event count, event size,
spread, and the deterministic intraday clock (R-squared 0.54 for b_r,
0.27 for b_f, 0.68 for omega_r, 0.51 for omega_f, Table 5, PDF p. 16).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] **The
   release-calendar component, with a declared pre-release lead, for
   the deterministic-clock null arm of the branching-ratio trigger.**
   The queued arm (deep-read 19, log ## 26) currently enumerates the
   deterministic intensity as "hour-of-day, session segments". This
   paper supplies the missing third component with regression evidence:
   the parameter shifts begin BEFORE the release stamp — price impact
   rises on ANN_t-1 (0.129***, PDF p. 11, Table 2), flow volatility
   declines on ANN_t and ANN_t-1 (-0.039**/-0.057***), and the flow
   responsiveness of submitters collapses around the release — so a
   null whose release handling begins at the stamp misses the very
   interval where liquidity is being withdrawn. Pre-declaration text:
   no branching-ratio trigger window reading is admissible under the
   deterministic-clock null unless the null's deterministic intensity
   also carries the scheduled-release calendar (the owner-curated
   macro timeline), each release entering with a lead window frozen
   from calibration windows disjoint from evaluation and covering the
   pre-release withdrawal interval; release-clock-explained windows
   contribute no firing (neither positive nor negative), and
   release-explained windows are reported separately in every run.
   Harder to pass: release windows are precisely where return
   innovations spike (omega_r, ANN_t = 0.066***), price impact jumps
   and flow responsiveness collapses — an extreme-impact,
   extreme-intensity configuration a branching estimator will read as
   its day's most excited windows; a trigger bar that survives the
   hour-of-day null can still be the release calendar wearing
   excitation's costume, and this component is what separates them.
   It tightens only the queued deterministic-clock null arm (and
   through it the T-H and T-O families); no C1-L2 text moves and no
   armed rule changes; consistent support cited from the same paper's
   lineage (Fleming-Mizrach-Nguyen 2018: announcements amplify
   price-flow impacts, particularly for limit orders, PDF p. 2).

2. Reinforcing, no new item — OFI is constructible from BBO events
   alone, without order-type labels: the paper's OFI follows the CKS
   event construction on best bid/offer price and size changes (PDF
   p. 3), with the order-type decomposition ("summing market, limit,
   and cancellation orders") explicitly reserved for data that carries
   order types (PDF p. 3, footnote 6). A worked exhibit for probe E1's
   volume-conservation reconstruction-admissibility rule: a BBO-derived
   OFI is admissible as a feature, but any decomposition-flavoured
   reading (this share is cancels, this share is market orders) is
   inadmissible on BBO-derived flow; the two constructions coincide
   only under complete book processing, and the claimed provenance of
   every OFI instance must be its construction, stated.

3. Reinforcing, no new item — aggregation manufactures simultaneity,
   and the coefficient is a function of the clock: b_f rises from
   0.301 at one second toward 0.55 at one minute while b_r falls
   (PDF p. 12), the endogeneity traced to stale limit orders and
   price-contingent strategies (Deuskar-Johnson, PDF p. 6; Obizhaeva,
   Obizhaeva-Wang). A worked exhibit for the record's clock
   discipline: no fitted contemporaneous flow-price coefficient from
   one sampling clock may be compared to, pooled with, or narrated
   alongside one from another, and C1-L2's event-clock covariate /
   wall-clock label architecture is the immune design (PDF pp. 3-4
   of the spec family; the paper shows why the pooled-across-clocks
   alternative is biased at every clock where it is measurable).

4. Reinforcing, no new item — fitted structural point estimates are
   unstable across windows and mostly not significant: b_r varies from
   0 to about 5 with standard deviation 0.999 and is significant in
   only 64 percent of 15-minute intervals (Table 3, PDF p. 12); deep
   depth smooths the impact (the D-inverse elasticity 0.553***, PDF
   pp. 14-16). An independent second exhibit, equity-futures this
   time, for the uncertainty-band-not-point-estimate rule already
   queued from Hardiman-Bouchaud: single-window fitted parameters are
   noise-dominated readouts, and any trigger built on one must carry
   its interval-band, not its point.

5. Interpretation caution — the announcement dummies are significant
   but change adjusted R-squared little, because market activity
   variables (depth, event count, event size, spread) already carry
   most of the release-window variation (PDF p. 9, Table 5). The
   honest reading for the funnel: the release calendar acts mostly
   through OBSERVABLE activity, so a null carrying the deterministic
   clock plus the release dummies is not double-counting what the
   activity features already measure — the two overlap, and the null
   arm must declare which carries the release windows, not stack both
   silently.

The killed-if-wrong section stands: had a branching-ratio or absorption
window reading ever been counted inside a release window without the
release-calendar null component, the armed test would have absorbed
public-information repricing and withdrawal-period microstructure into
its interaction claim — it would have fired or died on the calendar,
not the book — and the library-is-ammunition rule plus nothing-measured
are what prevented it. The one-second dissipation finding cuts the other
way and is refused as an OUT laundering below.

Standing caveat recorded: single instrument (S&P 500 E-mini), 2008-2013
(crisis and post-crisis era), 8:30-15:00 Chicago regular hours only —
no Globex/overnight, in a market where the eight selected US releases
are first-order events and mostly land at 9:00 local; the transfer to a
24/7 BTCUSDT tape is mechanism-level only (pre-release withdrawal is
generic microstructure), never numerical; SVAR-ITH assumptions bind
(structural matrix constant within 15 minutes, three nested 5-minute
heteroskedastic states, the rank condition excluding 4.3 percent of
intervals); the announcement set is eight releases at daily grain with
1,490 date clusters; BBO-derived OFI without order types throughout.

Source-quality note — solo-author dissertation chapter, arXiv v4
(8 Oct 2025), advisors and lineage squarely in the
Hasbrouck-Andersen-Todorov tradition; results internally consistent and
the estimator (ITH) is the Rigobon-Deuskar-Johnson standard, but
published version to be checked before formal citation; no replication
package inspected (none offered in the text).

Laundering directions named: INTO — the paper's fitted coefficients
(b_r 0.834, the depth elasticity 0.553, the announcement dummy values,
the one-second dissipation) may never be imported as calibration,
priors, or tolerances for the C8 trigger bars, barrier constants, or
null constructions; they are one instrument, one era, one clock, and
eight announcement types. OUT — the one-second dissipation and the
simultaneity-bias findings may not be read backwards as "L2 flow has no
content at the programme's horizons" or "flow-based triggers are
biased": dissipation is a statement about second-scale contemporaneous
structure in a 2008-2013 equity-index tape, the programme's compression
question is about multi-hour state accumulation the paper does not
test, and the simultaneity finding binds fitted contemporaneous
coefficients, not state-definition triggers (T-O is a state, not an
estimate) — the limits bind what a transferred number may CLAIM, not
whether the longer-horizon content exists.
