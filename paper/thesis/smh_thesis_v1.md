# THE SALIENT MARKET HYPOTHESIS
## A Falsifiable Theory of Liquidity and Time on the Weekly Chart
### Thesis, version 1.0

Written 19 November 2026, session 131, at the owner's directive to write
the salient market hypothesis from scratch to finish. Status: THEORY-CLASS
DOCUMENTATION under autonomy charter v1, class T. ZERO STATUS until the
forward calibration record accrues rows. Every quantitative statement in
this thesis is a frozen design figure produced on unsealed pre-2021 weekly
NQ data and already recorded in the programme bundle; design statistics are
bookkeeping, never proof, and the proof object is the forward calibration
record alone, which is empty by design. The standing consolidation draft
(smh_theory_consolidation_v0.md, session 119) is cited throughout and not
rewritten; where this thesis paraphrases, the frozen source wording
governs. Kill criteria of every claim are stated with the claim.

The two load-bearing sentences of the programme, absolute and permanent:

The default assumption is NO EDGE. The burden of proof is absolute.

---

## Abstract

The salient market hypothesis (SMH) claims that a price series carries a
recurrent, measurable, salience-local timing structure. On the weekly grain
of a liquid equity-index future, one entry condition is measured to raise
the conditional probability of a significant single-week move within twelve
weeks from the unconditional climatology 0.441 [0.411, 0.471] to a measured
0.634 [0.487, 0.782], with disjoint confidence bands: when 8-week realized
volatility crosses DOWN into its compression region (a cross, not a dwell),
the 12-week first-event hazard of a significant week, defined as
|r1| >= 2.5 x sig_w of the decision week, rises materially above the
do-nothing baseline. The content of the signature is DURATION, a clock
anchored at the cross, not the entry conditions themselves. The structure
recurs actuarially, roughly 2.04 triggers and 1.29 anticipated events per
year on the design sample, with the full circle in medians about 29 weeks
end to end; no dated instance is ever inevitable. The public levels and
means of the phenomenon are PRICED: implied volatility tracks the clock
monotonically, and the variance risk premium survives the trigger, so the
hypothesis cannot rest on public-information mispricing. What remains
private, at the weekly grain, is the CALIBRATION RECORD, the act of
pre-registering a dated hazard and scoring it against realized outcomes.
The hypothesis is falsifiable in public by kill lines declared in advance
(3/8/19/31 resolved events at 10/20/40/60 scored forward rows) and by one
positive proof statement: at least 57 of 104 resolved compression 12-week
windows must resolve with the event. Zero forward rows have been scored.
Direction is refused until forward rows earn it. This thesis states the
hypothesis, its every constituent finding, its priced-ness measurements,
its proof protocol, its falsification record, its known defects, and what
it does not claim. It is a standing hypothesis, not a result.

---

# PART I. THE PROBLEM

## Chapter 1. The motivating question

A circus lion goes feral during a show. To the audience there were no
signs moments prior; to whoever assembled the conditions, the escape was
already overdetermined. The motivating intuition of this research
programme is that markets have moments of this shape: a significant move
arrives, and afterwards the crowd insists it was unheralded, while a
measurable state of the market had quietly made it materially more
likely. The question the programme set out to answer, in its owner's own
framing, is whether a set of recurring, effectively inevitable conditions
can be identified, close in time, that mark the beginning of a significant
directional impulse, before it arrives, across markets.

That framing contains three demands: inevitability, timing, and direction.
The programme's first and most consequential finding is a theorem about
that triple, and the entire shape of SMH is a consequence of it. The
present chapter states the problem; the next chapter states the theorem
that shapes it.

The problem, formalized, is four questions at a decision close:

1. WHEN is a big move likely? (the hazard question)
2. HOW CLOSE in time can we get to it? (the timeliness question)
3. WHICH WAY will it go? (the direction question)
4. WHAT DOES IT COST to be there? (the exploitability question)

Everything the programme measured is an answer to one of these four, a
measured refusal to answer one of them, or a measured statement that the
answer is priced and therefore worthless as an edge.

## Chapter 2. The refusal theorem

The certainty-timing-direction triangle, consolidated at sessions 36-37 of
the programme and formalized at session 30 (block 38), states: a PUBLIC
rule claiming all three of certainty, timing, and direction is priced
away. The logic parents recorded at its formalization are the
no-arbitrage and martingale machinery of Björk and Elliott-Kopp, the
no-trade theorems of O'Hara's microstructure canon, and the empirical
publication-decay evidence of McLean-Pontiff: whatever a public rule can
guarantee about a future price is arbitraged into the current price until
it guarantees nothing. Inevitability without timing is true and priced;
inevitability with both timing and direction collapses back into
statistics. There is no third door for a public rule. The refusal is a
theorem, not a mood.

The theorem was not accepted on faith; the programme tested the tradition
that claimed otherwise. Elliott Wave as received claimed all three
(certainty, timing, direction) and produced zero testable predictions,
which is why it was refused as theory and retained only as a descriptive
canvas layer for annotation. Volume Spread Analysis, the Wyckoff event
dictionaries, the Copsey cycle ladders: each was studied in full from the
programme's book collection, encoded where encodable, and subjected to the
same registration standard. None bypassed the theorem. The chapter of the
record that tests the AVFI family (Chapters 21-22 of Part VI) is the
demonstration that the programme tests even its owner's standing beliefs
exactly as directed and freezes the nulls.

## Chapter 3. What remains private

The observer corollary (session 32, block 40) is the constructive turn of
the refusal theorem: the only forecast that cannot be priced away is the
private one, existing in exactly three forms:

1. INFORMATION others lack;
2. SPEED others lack;
3. A CALIBRATION RECORD others have not measured.

SMH builds the third. The corollary carries a privacy caveat recorded as
interpretation, not measurement: privacy erodes on publication; the
protective privacy of the record is the pre-registration interval; and
what remains strictly private even after publication is the actuarial
posture the record licenses, sizing in proportion to the measured hazard.
The programme's measured door status, stated fully in Chapter 14:
information is CLOSED at this grain on levels and means (with one
sub-door pending on unsigned data-side drafts), speed is NOT HELD at the
weekly grain (order-flow branches are pre-registration only, blocked on
data), and calibration is UNDER CONSTRUCTION. The forward log, empty by
design, is the proof object.

---

# PART II. THE FORMAL STRUCTURE

## Chapter 4. Objects and layers

A theory of liquidity and time must keep its objects separate. The
programme's five-layer architecture, held everywhere in this thesis:

1. MARKET-STATE MEASUREMENT. Where is the series now? Descriptive,
   bookkeeping, never a claim. (sig_w, the region occupancy, the AVFI
   state.)
2. EVENT PROBABILITY / HAZARD. Given the state, how likely is the
   anticipated event within the observation horizon?
3. POTENTIAL PRECURSOR. Does anything add to the hazard beyond the state
   and the clock? (Tested covariates: null unless forward rows say
   otherwise.)
4. DIRECTIONAL EVIDENCE. Which way is the event signed? Refused until
   forward rows earn it; the anticipated change is a significant MOVE,
   never a signed one.
5. EXECUTION / RISK CONTEXT. What position, if any, does the hazard
   license, at what cost? Descriptive sizing only; paper trading only;
   nothing in this thesis is tradeable advice.

Conflating these layers is how theories launder themselves: a state
measurement dressed as a prediction; a direction guess dressed as a
hazard; a sizing preference dressed as a finding. Every statement in this
thesis names its layer.

## Chapter 5. The frozen definitions

The definitions below are frozen in the programme bundle and are quoted
from their frozen sources. sig_w is the 8-week trailing weekly log-return
standard deviation (ddof=1), including the current week.

THE TRIGGER (smh_hazard_v0.md, session 32). Compression entry at t:
sig_w(t) <= LOW (LOW = 0.01739, the frozen pre-2021 tercile cutpoint) AND
sig_w(t-1) > LOW. A cross, not a dwell. True crosses pre-2021: n = 41.
The load-bearing part is the crossing week: the trigger is the cross into
the compression region, never a residence in it.

THE EVENT (same source). The significant 1-week event: |r1(t+1)| >= 2.5
x sig_w(t), first occurrence within 12 weeks of the entry. The event is
defined as a MOVE, never a signed move; direction is not part of the
event definition. The realized design anatomy (smh_event_anatomy_v0.md,
session 39): the median event overshoots its own bar by 1.41x (maximum
2.63x), so the median significant week is a ~3.5-sigma week. The median
dwell of the compression spell is 4 weeks; the entry-anchored clock and
the spell-anchored abort condition were reconciled by the
competing-risks decomposition.

THE CLOCK (sessions 32-38). The duration machinery: entry-anchored
Kaplan-Meier first-event clocks per region. The clock is anchored at the
entry cross and does NOT require the region to be maintained inside the
window. The measured content verdict, from the Cox v0.1 null
(smh_strategy_v0.md rung 8): the hazard content of the compression
signature is DURATION, honestly the pooled level and not even the slope,
not the entry conditions.

THE ARMED CLOCK (smh_sizing_v0.md, session 52, block 60). ARMED(t) holds
when week t falls in the 12 weeks after any compression entry t' <= t-1.
A new cross re-arms; overlapping windows do not stack; the armed clock
runs the full 12 weeks with no early termination at an event, because
cutting it short would be a second, untested policy. The armed clock is a
locked register in the record. Its measured verdict as a sizing lever is
recorded honestly in Chapter 24: the armed-window reduction policy is
DEAD.

THE REGIONS. The same sig_w axis, cut by the frozen terciles into
compression (LOW), mid, and stress (HIGH): the salience gradient of
Chapter 8 is measured across these three entry regions plus the
any-week climatology.

## Chapter 6. The hypothesis, stated formally

H-SMH, the salient market hypothesis, is this specific claim set under
the frozen definitions of Chapter 5:

C1 (OCCURRENCE). At a compression cross t, the conditional probability
that the event occurs within the 12-week window, computed by the
entry-anchored KM clock, exceeds the any-decision-week climatology, with
disjoint confidence bands. Design figures: 0.634 [0.487, 0.782] from 26
of 41 entries, versus 0.441 [0.411, 0.471] from 1050 decision weeks.

C2 (CONTENT). The information content of the signature is duration: the
clock anchored at the cross carries the hazard; the entry conditions
beyond the cross itself carry none measured beyond it.

C3 (LOCALITY). The salience is edge-local: only the compression cross
separates from climatology with disjoint bands; the mid region does not
clearly separate, and the stress region sits below climatology after its
own events pass (the suppression side, Chapter 8).

C4 (RECURRENCE). The structure is actuarial: triggers recur indefinitely
at the design rate (about 2.04 per year; about 1.29 entry-conditioned
events per year); the full circle in medians from cross to next cross is
about 29 weeks end to end. No dated instance is ever inevitable.

C5 (PRICED-NESS). The levels and the mean of the phenomenon are priced
(Chapter 12): the signature is level-cheap but the crowd's calm at
compression entries is still overpriced calm; the variance risk premium
survives the trigger at a thinner level.

C6 (THE PRIVATE RESIDUE). What the hypothesis leaves over, at the weekly
grain, is the calibration record: a pre-registered, dated, scored
forward log whose actuarial value is the measured license it provides
(the posture of readiness at the cross), not a mispricing.

Every clause carries its kill machinery (Chapters 15-19). None of them is
currently proved: the forward log is empty by design, and the design
figures above are bookkeeping on the unsealed pre-2021 sample.

DESIGN-ONLY CROSS-MARKET NOTE. The same rank-transferred rule, zero
re-tuning, measured on the design windows of three further markets
(smh_crossmarket_stageA_v0; descriptive Stage A bookkeeping, sealed
windows untouched): GOLD cum12 0.617 [0.478, 0.756] versus 0.481, gap
+0.136; NIKKEI 0.562 [0.422, 0.703] versus 0.374, gap +0.188; DAX 0.680
[0.551, 0.809] versus 0.465, gap +0.215. The gap sign is positive in
every market tested, each within the NQ grid's own range. These are
bookkeeping figures; the cross-market 2021+ windows are sealed and single
open, only on the owner's dated go.

---

# PART III. THE MEASURED STRUCTURE
### (design sample, unsealed pre-2021 weekly NQ; bookkeeping, never proof)

## Chapter 7. The trigger and the event

The compression cross fired n = 41 times in roughly 20 years of
unsealed pre-2021 weekly data. Of these entries, 26 resolved with the
significant-week event inside the 12-week window: occurrence 0.634,
Greenwood band [0.487, 0.782]. The matched climatology, over 1050
decision weeks, is 0.441 [0.411, 0.471]. The bands are disjoint; the
gap is +0.193. The median lag from the entry to the first event is 5
weeks.

The corrected-table log is part of the frozen provenance: an off-by-one
risk-set bug in the first KM table (343 versus 327 person-weeks) was
caught by the standing consistency check and corrected in the record by
append. This thesis reports the corrected figures.

The event anatomy (session 39): the median event overshoots its own
2.5-sigma threshold by 1.41x (maximum 2.63x). The anticipated "big move"
therefore means, concretely and measurably: a threshold-crossing single
week of central size about 3.5 sigma, not a point target and not a
cluster by construction.

## Chapter 8. The salience gradient

The 12-week first-event cumulative, by entry region (smh_mid_clock_v0.md,
session 38, block 46): compression (n = 41) 0.634; mid (n = 66) 0.470;
any week (n = 1050) 0.441; stress (n = 33) 0.273. The gradient is
monotone, and THE SALIENCE IS EDGE-LOCAL: only the compression cross
separates from climatology with disjoint bands.

The record's compressed form of the finding: above climatology at the
cross, below after the print. The post-print window is suppressed: its
12-week cum is 0.231 [0.069, 0.393] against climatology 0.441,
disjoint-band. This is the salience machine's own shape: the hazard
rises entering compression, realizes at the print, and falls quiet.

## Chapter 9. The capture ladder

Timeliness is a measured margin, not a felt skill
(smh_entry_theorem_v0.md, sessions 37-38):

- Enter at the cross: 0.634.
- Wait 4 quiet weeks, then enter: 0.500.
- Wait 6 quiet weeks: 0.348.

Waiting gains nothing the clock does not already condition on, forfeits
the front-loaded mass, and races the spell's own mortality (median dwell
4 weeks). The compression cross is the measured closest approach to the
event at the weekly grain; the 12-week protocol window is the measured
location of the asymmetry, not arbitrary bookkeeping. Finer timing than
the cross needs intraday data the programme does not hold; the L2
runbook is written and its download is the owner's hands.

## Chapter 10. The cycle

The trigger recurs in about a quarter (smh_aftermath_v0.md, session 41).
The next compression cross follows the event at a median of 15 weeks
(one return censored at the sample end); the return to the trigger is
FASTER than the arrival of a fresh stress spell (median 23.5 weeks). The
full circle, in medians: cross, then the print at 5 weeks; then, within
the quarter (17 of 26 events), the stress region about 3 weeks later;
then the de-stress clock (6 weeks from a stress entry to its cum 0.636
by 12 weeks); then the next cross, 15 weeks from the print. End to end,
about 29 weeks.

The modal episode is a single print against every yardstick: 22 of 26
design windows hold exactly one significant week and no further one.
The clustering intensity is definition-made (the median inter-arrival
gap between clustered prints is about 18.5 weeks against the event's
own drifting endogenous yardstick), and that caveat is frozen beside
the number rather than argued away.

Actuarial rates (smh_strategy_v0.md rungs 7/9; smh_dossier_v0.md):
about 2.04 compression triggers and about 1.29 entry-conditioned events
per year on the design sample; region occupancy 27.5 / 30.6 / 41.9
percent. ROWS ARE STABLE, YEARS ARE NOT: the capture fraction moved
only 0.647 versus 0.625 across decade halves while the trigger RATE
moved by a factor of 4.5 (regime range 0.7-3.2 per year). The proof
schedule in Part V therefore counts rows, never years.

## Chapter 11. Robustness

The design definition is deliberately NOT the grid optimum. The 11-cell
definition-elasticity audit (smh_robustness_v0.md, family_registry_v0.md)
found the compression gap positive in every cell (gaps 0.106-0.222),
so the frozen definition survives its own perturbation neighborhood
without being the best cell in it; the standing rule against post-null
re-tuning is what keeps this audit honest. The cross-market transfer of
Chapter 6, with zero re-tuning, is the second robustness leg. The
third leg is negative: the second trigger family (stress-side entry)
was measured weaker (Chapter 15's honest reading) and its null risks
refused re-tuning exactly as the AVFI nulls were.

---

# PART IV. PRICED-NESS
### (what the market already sees; smh_unseen_v0.md, session 40, block 48)

## Chapter 12. Level-cheap, mean-priced

THE LEVEL. The compression signature sits in cheap volatility territory:
the median VXN at compression entries is 16.47 versus 20.14 across all
pre-2021 weeks; entries sit at the 25.8th percentile of VXN's own
distribution (mid entries the 46.3rd, stress entries the 67.4th; by
region occupancy, compression weeks the 22.5th, mid 42.4th, stress
77.7th). Implied volatility follows the clock, monotonically. The
market is not blind to the state.

THE MEAN. The strong unseen-ness claim, that the market fails to price
the coming expansion, is REFUTED at the mean in the design sample: the
variance risk premium survives the trigger, +3.71 vol points at entries
(positive at 73.2 percent of entries) versus +4.55 across all weeks
(76.7 percent); forward 12-week realized volatility at entries is 13.96
versus 17.22 all weeks. The crowd's calm is still overpriced calm,
thinner premium, no inversion. Frozen consequence: unseen is the wrong
word for cheap. The edge claim, if any, cannot rest on options
mispricing at this grain; it rests on the unmeasured event-structure
sub-door (whether the specific DATED hazard priced by the options term
structure differs from the clock; pending unsigned data-side drafts and
the owner's data-source choice) and on the forward calibration record.

## Chapter 13. The priced-calm covariate split

One covariate split was measured at the owner's direction and is
registered, flagged, untrusted (smh_priced_calm_v0.md, session 43): at
the frozen cutpoint VXN 16.47 (the pre-2021 entry median, which makes
forward classification deterministic), the residual-fear half of
compression entries (VXN above the cut) shows 0.800 [0.625, 0.975]
against the deep-calm half's 0.476 [0.263, 0.690]. The split is
era-confounded (the halves separate the high-VXN decades from the
low-VXN decades) and is carried in the record as a seductive cell, not
a finding: it becomes examinable only at the forward milestones, under
the cell protocol of Chapter 19, and never before.

## Chapter 14. The three doors, measured

Door 1, INFORMATION: CLOSED at this grain on levels and means. The
event-structure sub-door is unmeasured and rides the owner's unsigned
data-source decision. Door 2, SPEED: NOT HELD. The weekly OHLCV
programme holds no order flow; the L2 and order-flow branches are
pre-registration-only and blocked on the download; a separate judgment
verdict (block 36) refused any speed claim on proxy data. Door 3,
CALIBRATION: UNDER CONSTRUCTION. The empty forward log is the proof
object. The hypothesis's private content is door 3, and it is
epistemic before it is economic: a verifiable record of conditional
mastery whose economic content exists only if the block-93 gaps close
(direction, event-structure priced-ness, post-cost exploitability, and
the forward rows themselves).

---

# PART V. THE PROOF PROTOCOL
### (smh_gates_v0.md, smh_proof_criteria_v0.md, sessions 43-46)

## Chapter 15. The kill lines

The occurrence claim C1 (design p0 = 0.634, 26 of 41) dies in public if
the forward record shows K resolved-event rows at or below its kill
line at a milestone: K <= 3 at n = 10 scored rows; K <= 8 at n = 20;
K <= 19 at n = 40; K <= 31 at n = 60. The rules are sticky,
milestone-exact: rows of the other kind never leak in, unresolved rows
never count. Per-gate false-kill (a true 0.634 machine dying at that
gate): 0.0335 / 0.0282 / 0.0290 / 0.0415. Power against the
climatology-measured world: 0.2855 / 0.4465 / 0.7243 / 0.9046. The
falsificationist's fee is roughly 3-4 percent per gate; that price is
the point, not the defect.

The stress-side de-stress claim (p0 = 0.636, 21 of 33 design) lands on
the SAME thresholds, honestly weaker against a coin (power 0.1719 /
0.2517 / 0.4373 / 0.6506), with no asymmetric tuning applied: the
second trigger family is recorded as the weaker clue and never
re-tuned to look better.

## Chapter 16. Cumulative honesty

Two frozen statements prevent the programme from celebrating either
survival or death without the schedule's own arithmetic. First, a TRUE
machine following this gate schedule dies somewhere in the four gates
roughly one run in eight (about 0.126, independence approximation; the
gates share rows). Second, the design battery of claims was expected,
by its own composition, to produce roughly one chance survivor. The
nulls of Part VI are the working half of this honesty: they are the
record of the battery's other members dying where they fell.

## Chapter 17. Calibration expectations, declared in advance

If the design is right, SMH-forecast rows should cost 0.6568 nats per
resolved window (Brier 0.2320) against climatology-forecast rows' 0.7319
(Brier 0.2693), an expected log-score edge of 0.0751 nats per row. If
climatology is right, the SMH rows lose 0.0766 (0.7628 versus 0.6862),
symmetric by construction: the scoring rule cannot favour the
hypothesis on expectation unless the outcomes actually do. Readouts are
judged at 26, 52, and 104 resolved windows.

## Chapter 18. The positive proof, and the four outcomes

The positive proof is exactly one statement: at least 57 of 104
resolved compression 12-week windows resolve with the event (the
stricter of the two registered rules). Power 0.971; false-pass 0.018.
Nothing less counts; no intermediate readout is over-read; nothing in
the design sample counts at all.

Four outcomes are kept distinct, so that no result can be argued
around after the fact.

1. FALSIFIED: a kill line fires. The claim dies; the obituary is
   written; nothing is re-tuned.
2. REDUCED: the direction peeks fail. Door 3 stays timing-only; the
   residue is actuarial sizing posture.
3. HOLLOWED (economically, not predictively): the event-structure test
   shows the dated hazard fully priced. The residue is
   knowing-your-own-scoreboard: calibration as process quality, not
   income.
4. PROVED: 57 of 104. Nothing above, below, or around that number.

## Chapter 19. Direction peeks and the seductive-cell register

Direction is refused until forward rows earn it. Two peeks are
pre-declared, counted in resolved forward first EVENTS (not rows):
promotion only at up >= 27/40 at 40 events (Clopper-Pearson 95 percent
lower bound above one half) or up >= 39/60 at 60 events; a down-bias
annotation at up <= 13/40 or <= 21/60; otherwise direction stays
refused. The refusal's design basis: 17 of 26 first events were up,
CP95 [0.443, 0.828], the lower bound below one half. A significant
MOVE, never a signed one.

Three seductive cells are registered with frozen definitions, flagged,
untrusted: momentum12 <= 0 at entry (design 6/7);
reversal_down macro state at entry (design 9/12); the priced-calm
residual-fear half (VXN > 16.47 at entry, design 16/20). Cells are
examined only at n >= 10 forward rows, promoted only on a CP95 lower
bound exceeding the unconditional forward event share, never automated,
counted silently below the floor. The critique that keeps this rule in
its place is Chapter 23's second defect: the promotion rule is coherent
as an anti-seduction filter and not coherent as a pre-registered test
(a proposal to repair it, R-1, sits in the ratification queue at zero
status and dies whole on the owner's one word of refusal). The main
proof of Chapter 18 is untouched by any cell verdict by construction.

## Chapter 20. Timing honesty

At the design trigger rate (2.04 triggers, 1.29 entry-conditioned
events per year), the occurrence gates arrive in roughly 5, 10, 20, and
29 YEARS, and the 104-window readout in roughly half a century,
halved if both row windows count. The readout schedule is roughly 13,
25, and 51 years for the intermediate calibration judgments. The
schedule counts rows, never years, precisely because of Chapter 10's
regime instability: a hot regime opens the first gate in about 3
years, a cold one nearer 15. The cross-market forward stream (Amendment
9, signed and first-firing after this thesis's date) is the only
instrument that can open gates before NQ's own clock, and it runs
under its own registered protocol. The thesis states this horizon
plainly because hiding it would turn the protocol into theatre.

---

# PART VI. THE FALSIFICATION RECORD
### (what died, and why that is the asset)

## Chapter 21. The nulls before SMH

The hypothesis of Part II was built only after a full programme of
candidate edges had been tested honestly and killed. The record, in
brief:

- RULE SET A (AVFI state system): killed. In-sample Sharpe -0.115,
  worse than the random-entry control; validation 0.420, equal to
  random, at one-eighth of buy-and-hold upside. The registered
  |sp_z|>=1 variant was structurally vacuous: zero trades ever.
- H1/H2 (AVFI conditional structures): not supported.
- STAGE 6A FAMILY (27-combination AVFI grid): fails White's Reality
  Check. Family best 0.58, RC p = 0.11. Every AVFI variant fails
  individually. The only variant significant in both windows was the
  12-week momentum control, consistent with the generic
  trend-following prior, not with AVFI.
- H8 (AVFI flow-fade divergence at tops, Amendment 3, signed and
  executed exactly as directed): n = 32, WRONG-SIGNED, p 0.79 at the
  primary 4-week horizon. Volume divergence does not call tops in the
  future tense. H8 bottom arm: 0 events, vacuous.
- H9 (effort-vs-result climax): n = 3 events in 26 years; p 0.082 at
  the primary horizon, right direction, fails alpha, no support
  claimed. Family max-t 0.089. The frozen defaults are never re-tuned
  post-null.
- AMENDMENTS 4 AND 5 (regime-quality and terminal-detector confirmatory
  tests): WITHDRAWN UNEXECUTED after their pre-sign-off power readouts.
  The H10a test as drafted was invalid (measured false-positive 7-16
  percent against nominal 5: the predictors are near-integrated, and
  within-sample resampling cannot size them); the validated
  circular-shift revision reaches only 21-29 percent power at
  plausible effects. The H11a test is correctly sized but only detects
  a ~1.25-sigma effect at 80 percent power; meaningful 0.1-0.3 sigma
  effects are detected 7-13 percent of the time. Both withdrawn rather
  than run underpowered.
- THE SPZ COVARIATE NULL: at-entry sp_z adds nothing to the hazard, as
  pre-declared.
- THE HOLDOUT BATTERY (Amendment 1/2, the single open of the sealed
  2021+ window, run once on the owner's explicit go): NOTHING PASSES.
  Rule set T (12-week momentum long/flat): Sharpe 0.575, bootstrap p
  0.069 against the pre-committed 0.05; false at the margin. Rule set
  U3: 0.418, p 0.116; false. H7 (bear-capitulation bounce):
  UNTESTABLE, its state extinct in the modern era (occupancy 0 against
  a gate of 10). The holdout is now SPENT and is never evaluated again
  under any circumstance, even descriptively.

## Chapter 22. The lessons the nulls taught

Three of the record's fifteen-plus lessons carry the theory's technical
spine. Lesson 11/13: near-integrated weekly series (lag-1 of order
0.92+) make within-sample resampling invalid; persistence-preserving
nulls (the Theiler circular-shift family) or validated event-study
machinery are the only lawful tests, and the H10a withdrawal is the
worked demonstration. Lo's Sharpe statistics: annualized headline
Sharpe is banned programme-wide; per-period statistics only. DSR and
PBO: holdout repetition spends holdouts; N = 1 at the moment of
specification is what the signed-dated-amendment rule guarantees; the
~1,000-observation holdout minimum frames the weekly grain honestly.
The battery taught two more: magnitude can replicate while
significance fails (T's 0.575 holdout against 0.571 unsealed, missing
at exactly the 43-percent-power-predicted rate), and insurance is
only worth its premium in the insured regime (U3's drawdown control
underperformed exactly when the crisis regime it hedged against was
absent).

## Chapter 23. Why the record is the asset

A theory's credibility is the set of claims it refused to make cheaply.
SMH arrives holding: a validation spine adopted before its own tests
(family max-t for variants, SPA with all three bounds for family
searches, BH with the BY correction for independent shortlists, DSR
with honest trial counts for final picks); a spent holdout that will
never be re-spent; nulls frozen rather than re-tuned; two underpowered
amendments withdrawn unexecuted rather than run for the record; and an
owner standing belief (AVFI tops/bottoms) tested exactly as directed
and recorded as a belief, not a finding. The default assumption that
there is no edge, and the burden of proof, are the two load-bearing
sentences precisely because everything in this Part was built under
them. The falsification record IS the asset; the hypothesis is the
instrument that keeps the record growing.

---

# PART VII. KNOWN DEFECTS
### (stated inside the theory, not in footnotes)

## Chapter 24. The defects

1. THE SMALL-N SPINE. 41 compression entries in about 20 years; every
   design cell is small; the direction splits doubly so; the
   single-print intensity is definition-made with its caveat frozen
   beside it; the lone-print grid's exact provenance is a stated
   session-window rather than a single session. The forward machinery
   exists precisely because the design sample cannot be its own
   proof.

2. THE CELL-PROMOTION CRITIQUE. The seductive-cell promotion rule is
   coherent as an anti-seduction filter (per-look false-promotion at a
   true-null cell 0.007-0.024, at or below the nominal 2.5 percent)
   and NOT coherent as a pre-registered test on four counts: its
   denominator is ambiguous between three readings that move the
   promotion floor by a factor of 3-4 in required rows; its motivating
   example is not the comparison the rule performs; it lacks declared
   operating characteristics; and its re-examination schedule is
   uncorrected repeated looking. Proposal R-1 (pin the denominator,
   declare the table) sits in the ratification queue at zero status.
   The main proof is untouched by any cell verdict by construction.

3. THE SIZING LAYER'S VERDICTS. The armed-window reduction policy is
   DEAD: the 0.634-class hazard does not cut the measured drawdown,
   because the clock's event is SIGMA-RELATIVE while equity drawdown
   mass is SIGMA-LEVEL (lesson 15). The lever that worked
   descriptively on the same sample, with no decision attached, is
   volatility targeting (max drawdown -0.384 versus -0.695, a 45
   percent reduction, with total return higher, +4.59 versus +3.92, at
   mean exposure 0.79; Calmar 0.233 versus 0.119; in-sample for its
   conventions). The sizing bridge is measured, descriptive,
   pre-decision. No statement in this thesis licenses a live position.

4. NOVELTY IS NOT SELF-CERTIFIABLE. The programme cannot verify that
   no prior literature states this structure; the record's own
   knowledge base, deep in microstructure, econometrics, and
   falsification methodology, is evidence of coverage, not of
   novelty. What the programme CAN say is structural: the hypothesis
   is stated with pre-declared kill lines, a single positive-proof
   statement, refused direction, and priced-ness measurements
   integrated into the statement itself, which is a stronger
   falsifiable structure than the descriptive frameworks it refused.
   A "first of market" claim, if it is ever earned, is earned by the
   forward record, not declared by a document.

---

# PART VIII. WHAT SMH DOES NOT CLAIM

Not direction. The anticipated change is a significant MOVE, never a
signed one; the CP95 lower bound 0.443 on the design split is below one
half; direction arrives only through a promoting peek (Chapter 19).

Not edge. Zero forward rows have been scored. Per the one-in-eight
honesty statement, an edge, if one appears, is indistinguishable from
an unfalsified hypothesis with good hygiene until the forward log
separates it (Chapter 16).

Not profit. Paper trading only. No live claim exists or is claimed.

Not certainty. No dated instance is ever inevitable. Inevitability is
actuarial: the trigger recurs; the event follows more often than
climatology; no weekend is promised.

Not entry rules beyond the cross. The compression cross is the measured
closest approach at the weekly grain; the covariate nulls of Part VI
are the record of every attempted refinement that failed.

Not a completed theory. The forward log is empty by design and is the
proof object. This thesis is the standing hypothesis, not the result.

---

# PART IX. THE ROAD

The proof object fills at the Sunday cadence: forward rows are scored
as decision weeks resolve, the occurrence gates open at 10, 20, 40, and
60 scored rows, the first gate is the binding next milestone, and the
cross-market macro stream (Amendment 9, first firing scheduled after
this thesis's date) is the only instrument that can open gates before
NQ's own clock. What the owner's hands can compress: the options
term-structure data-source decision (the event-structure sub-door of
Chapter 12); the broker/CME 1999-2000 export (the volume/Hawkes layer);
the L2 download (the speed door's pre-registration branch and the
intraday timing that Chapter 9 proves the weekly grain cannot give);
the unsigned drafts on the signature stack; the shelfed amendments.
What no hands can compress: the rows themselves. They arrive as the
market resolves them, or the theory dies at its kill lines first, and
either outcome is recorded.

The programme's definition of what it would mean for the owner's goal
to be met is precisely this: a theory stated so it can fail in public,
a record that scores it in public, and the refusal to claim anything
the record has not earned. The default assumption is NO EDGE. The
burden of proof is absolute.

---

# APPENDIX A. THE FROZEN LEXICON (the ten terms)

The programme's ten frozen terms, with definitions and origin sessions
(smh_lexicon_v0.md, session 117, block 120):

1. TRIGGER: the compression cross. sig_w(t) <= 0.01739 AND
   sig_w(t-1) > 0.01739. A cross, not a dwell. (session 32)
2. EVENT: |r1| >= 2.5 x sig_w of the decision week, first occurrence
   within 12 weeks. A MOVE, never a signed one. (session 32)
3. CLOCK: entry-anchored Kaplan-Meier first-event clocks per region;
   the clock does not require the region to persist. Content verdict:
   DURATION, the pooled level, not the slope. (sessions 32-38)
4. SALIENCE GRADIENT: compression 0.634 > mid 0.470 > any 0.441 >
   stress 0.273, monotone, edge-local. (session 38, block 46)
5. QUARTER RULE: the next cross follows the print at a median 15
   weeks; the return is faster than a fresh stress spell. (session 41)
6. ARMED CLOCK: the 12 weeks after any compression entry; re-arms on a
   new cross; no stacking; no early termination. Sizing verdict: the
   armed-window reduction is DEAD. (session 52, block 60)
7. LONE PRINT: the modal episode is a single significant week against
   every yardstick; the clustering intensity is definition-made, with
   the endogenous-yardstick caveat frozen beside it. (sessions 57-71
   window; exact session honestly not re-derived)
8. KILL LINES: 3/8/19/31 resolved events at 10/20/40/60 scored rows;
   sticky, milestone-exact; the one-in-eight statement rides with
   them. (sessions 43-44)
9. CAPTURE LADDER: 0.634 at the cross, 0.500 after 4 quiet weeks,
   0.348 after 6. Timeliness is a measured margin. (sessions 37-38)
10. PRICED-CALM: level-cheap (median VXN 16.47 at entries versus 20.14
    all weeks) and mean-priced (VRP +3.71 at entries versus +4.55);
    unseen is the wrong word for cheap. (sessions 40-43)

# APPENDIX B. SOURCE MAP

Every constant in this thesis maps to a frozen bundle document, itself
citation-audited at sessions 113-114 and re-verified at session 119:
the trigger cut, the event definition, and n = 41 to
smh_hazard_v0.md; the event anatomy to smh_event_anatomy_v0.md; the
KM bands, salience gradient, and edge-local statement to
smh_mid_clock_v0.md; the Cox duration verdict and the capture ladder
to smh_strategy_v0.md rung 8 and the entry-theorem cards
(smh_entry_theorem_v0.md); the quarter rule, the circle, the
suppression figure, and the lone-print statement to
smh_aftermath_v0.md and smh_strategy_v0.md rung 7; the priced-ness
figures to smh_unseen_v0.md; the priced-calm split to
smh_priced_calm_v0.md; the kill lines, calibration expectations,
positive proof, peeks, and cells to smh_proof_criteria_v0.md and
smh_gates_v0.md; the cell critique to smh_cell_promotion_critique_v0.md
(session 116); the sizing verdicts to smh_sizing_v0.md; the actuarial
rates to smh_strategy_v0.md and smh_dossier_v0.md; the cross-market
gaps to smh_crossmarket_stageA_v0.md; the AVFI and battery nulls of
Part VI to the amendment documents and the programme record
(amendments 1-3; the stage6b battery report; the 4/5 power readout
and withdrawals); the methodology spine to the validation and
regime papers studied as waves 1-2 (White, Hansen, Benjamini-Hochberg,
Lo, Bailey/Lopez de Prado; Hamilton, Diebold-Inoue, Maheu-McCurdy,
Bai-Perron); the refusal layer to smh_observer_corollary_v0.md
(sessions 30/32 lineage); the standing consolidation to
smh_theory_consolidation_v0.md (session 119), whose section 10 is this
appendix's parent. Where this thesis paraphrases, the frozen source
wording governs; on any conflict the source document, not this
thesis, is authoritative.

# APPENDIX C. COMPUTATION LOG

No computation was performed in the writing of this thesis. No market
data was read or evaluated; no sealed or spent window was touched (the
NQ 2021+ holdout is SPENT and remains untouched; cross-market and BTC
2021+ windows remain sealed); nothing was registered, evaluated,
booked, or scored; no frozen constant, rule, kill line, protocol, or
verdict was changed; no closed verdict was relitigated. Every figure
is a frozen design-bookkeeping number quoted from its bundle source
(appendix B). The risk of a thesis is that unification smuggles
reinterpretation; the guards, all carried in place: the abstract
states ZERO STATUS; Part III carries its bookkeeping-never-proof
header on the cover of the Part; Part IV separates measured fact from
registered-flagged-untrusted cells; Part V declares the proof,
falsified, reduced, and hollowed outcomes in advance; Part VII states
the defects; Part VIII recites what is not claimed; and the roadmap
rests on rows the record does not yet hold. Paper trading only.

*End of thesis, version 1.0.*
