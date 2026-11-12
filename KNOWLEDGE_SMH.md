# The Salient Market Hypothesis (SMH)

Named by Andrea, 12 November 2026: the framework was drafted as the
State-Clock Framework and adopted its standing name the same day. Same
object, same falsification rules; every future reference says SMH.

A theoretical framework for identifying, in advance, the significant
events in a market. Written as a direct replacement for Elliott Wave:
it keeps what Elliott got right, discards what Elliott got wrong, and
adds the dimension Elliott never had, time. Built from the 20-book
canon and the paper waves (Balan, Williams, Copsey, Hasbrouck, Kyle,
Bouchaud, Tsay, Hamilton, Clark, Sornette, Lo, and the rest), and from
the AVFI programme's own measured results.

## 1. The diagnosis of Elliott Wave

What Elliott Wave got right, and why it survived a century:

- Markets alternate between impulse and correction. TRUE, and now
  measured: returns show horizon-structured autocorrelation,
  persistence at weeks-to-months and reversal at multi-year horizons.
  The alternation is real; the 5-3 cage around it is not.
- The same structure appears at multiple scales. TRUE in the
  volatility sense: volatility is multifractal, correlations aggregate
  across heterogeneous trader horizons (Muller's HARCH, Bouchaud's
  stylized facts). Self-similarity lives in the variance process, not
  in a fixed price geometry.
- Crowd psychology evolves in phases that leave footprints. TRUE:
  herding, order-flow correlation, and the volume-price
  effort-vs-result relation are documented stylized facts. VSA read
  them verbally; order-flow research measures them.

What it got wrong:

- The fixed 5-3 form. Copsey's own finding: every impulse can be
  counted as a three. A form that cannot be counted wrong cannot be
  counted right.
- Fibonacci price ratios as targets. No statistical evidence anywhere
  in the canon. Geometry licenses them as measurement tools only; a
  ratio is a description, not a prediction.
- Unfalsifiability. Any count can be recounted, any correction
  extended. A theory that cannot fail predicts nothing.

What it never had, and correctly identified as the gap: time. Elliott
says where, never when. Every "when" in wave practice is retro-fitted.
This framework makes time a first-class dimension.

## 2. The ontology: what a market is

From Hasbrouck and the microstructure canon. A market is a matching
engine plus participants managing inventory plus informed flow. There
are two prices: a latent efficient price, moved by information and
inventory pressure, and the transaction price, which oscillates around
it. The transaction path equals the efficient path (near a random
walk with drift) plus mean-reverting noise.

From Clark, Mandelbrot, and the VPIN wave: the efficient price does
not evolve in calendar time. It evolves in trading time, clocked by
volume and volatility. All "when" questions must be posed in the right
clock. A week of calendar time can be an hour of trading time, or a
month of it.

From Hamilton and Diebold-Inoue: the process switches regimes slowly,
and what looks like long memory can be a sequence of breaks. Structure
exists, but it is statistical, not geometric.

## 3. The six unconditional laws

These are the inevitables, the axioms of the framework. Each is
documented, each carries its evidence anchor, and each is stated with
its use as a rule.

1. **Volatility persists, then mean-reverts.** High vol weeks follow
   high vol weeks; compressed vol expands. (Tsay's GARCH persistence;
   the clock study's frozen tercile tables.) USE: this is the clock
   itself.
2. **Tails are heavy.** Return distributions are non-Gaussian at
   every horizon. (Bouchaud's stylized facts; Student-t conditional
   tails.) USE: all thresholds, stops, and event definitions live in
   sigma units, never in fixed points.
3. **Autocorrelation has horizon structure.** Momentum at medium
   horizons, reversal at long ones, near-zero at short ones.
   (Jegadeesh-Titman; De Bondt-Thaler; time-series momentum in all 58
   contracts of the Moskowitz-Ooi-Pedersen study; the programme's own
   rule set T, its only replicated effect.) USE: the directional
   prior, valid only inside trend states and only at the right
   horizons.
4. **Impact is concave in volume.** Big moves require big flow, and
   flow leaves footprints. (Kyle's lambda; the square-root law;
   Cont-Kukanov-Stoikov's OFI.) USE: a significant event must be
   confirmed by volume, the formalized version of VSA's
   effort-vs-result. A move without volume is a suspect move.
5. **Events self-excite.** Price changes cluster in time, mostly
   endogenous. (Hawkes processes; Filimonov-Sornette's reflexivity
   measurements.) USE: hazard is state-dependent, so timing
   forecasts are conditional distributions, never constants.
6. **Every exploitable regularity decays.** The market adapts to
   whoever uses it. (Lo's adaptive markets; the programme's own
   holdout lesson.) USE: every rule in this framework carries a
   forward calibration score and a decay watch. Nothing is forever,
   by law.

Not on the list, and provably not on the list: the direction of the
next impulse at a chosen time. That absence is the framework's central
theorem, next.

## 4. The central theorem: the certainty-timing-direction triangle

In a public market, suppose a rule identifies, before it happens, an
event that is all three: certain, timed, and directional. Anyone who
sees the rule trades it; the price moves to the forecast; the event no
longer happens as forecast. Therefore such a rule cannot exist
publicly. It exists only privately: as informed flow (knowing
something others do not) or as speed (seeing it first). Kyle built the
formal version of this; the microstructure canon is its case law.

So the claims must be distributed honestly:

- CERTAINTY lives at the level of the distribution (the six laws).
- PROBABILITY lives at the level of the event (conditional rates by
  state).
- HAZARD lives at the level of timing (the clock).

Elliott Wave implicitly claimed all three and therefore made zero
testable predictions. The State-Clock Framework claims them separated,
and every separated claim is scoreable. That is the replacement in one
sentence: Elliott had anatomy without a clock and without the
possibility of being wrong; this framework gives the market a clock
and a scoreboard.

## 5. The state layer: what replaces wave counting

States are defined by measured quantities, never by counting. Four
states, on the instrument you trade, at the decision horizon:

- COMPRESSION -> TREND: vol expands with directional persistence
- COMPRESSION -> EXPANSION: vol expands, direction unresolved
- TREND -> COMPRESSION: momentum fades, vol contracts
- TREND -> STRESS: tail event against the state
- EXPANSION -> TREND: volume confirms direction
- EXPANSION -> STRESS: volume confirms reversal
- STRESS -> COMPRESSION: vol mean-reverts
- STRESS -> TREND: crash-scale overshoot resolves

COMPRESSION: low volatility tercile. The event-prone state: the clock
study measured a 47 percent rate of a significant 4-week move from
this state, versus 14 percent from high vol.

TREND: persistent directional drift. Law 3's prior is valid here and
only here.

EXPANSION: the event window, active while the significant move is in
progress. Law 4 operates: confirmation requires the volume footprint.

STRESS: the post-event tail regime. Law 2 operates: sizing cuts,
expectations widen.

What wave psychology called phases (optimism, disbelief, euphoria,
denial) are not prophecies here; they are names for measured occupancy
durations and transition rates. That is the entire difference between
description and divination.

## 6. The clock layer: time as a first-class dimension

The primary clock is volatility. At each decision close: sigma_w
(trailing 8-week weekly vol), its tercile, and the frozen conditional
tables give the hazard of a significant event within the next 4
weeks. The secondary clock is volume time (needs finer data than
weekly OHLCV). The tertiary clock is self-excitation (needs intraday
data; out of scope for now, documented as such).

Timing in this framework means: a conditional hazard function, updated
at every decision close, scored against outcomes. Not a date. A date
is what an open system cannot give, because a date would collide with
the central theorem the moment anyone believed it. The hazard IS the
"when", and the clock study is its measurement instrument: probability
logged in advance, Brier-scored, reliability-diagrammed. The 47 versus
14 percent tercile spread is the first measured tick of this clock.

## 7. The event: what you anticipate, identified before it happens

Definition, pre-registered: a significant event is a move of at least
2.5 sigma_w within 4 completed weeks (the clock study's frozen
threshold). Identification before it happens = the pre-event
signature:

- The clock: compression-state vol tercile (hazard elevated, 47
  percent).
- The state layer: which states are legal exits of compression, and
  what the horizon structure says about direction inside each.
- The flow layer: at finer horizons, the volume/OFI footprint that law
  4 requires of any genuine impulse (needs finer data; documented).

The signature raises probability. It never reaches 1, and the framework
says so in its own axioms. The Sornette log-periodic program is the
canon's model of a precursor signature: pre-registered, ex-ante, with
a public record of hits and misses. This framework adopts the pattern
and refuses the certainty.

## 8. What the framework predicts, and what it refuses

Predicts (all scoreable, all forward):

- Conditional event rates by state and tercile (clock study).
- Hazard of expansion from compression, updated weekly.
- State occupancy frequencies and persistence times.
- Direction asymmetry (drift) conditional on trend states (law 3).
- Volume confirmation of genuine impulses (law 4).

Refuses (permanently, by the central theorem):

- Dates. Price targets. Wave counts. Fibonacci projections. Certainty
  about direction at a chosen time.

Anything the framework refuses to output is something no public theory
can output honestly; the ones that claim to are the ones that have
never been scored.

## 9. The falsification protocol

The framework's most important layer, and the one that makes it a
replacement rather than a repeat of Elliott:

1. Every quantitative claim is scored forward: probability forecasts
   logged before outcomes (Brier, log score, reliability diagrams).
2. A claim that cannot be scored is not part of the framework.
3. Supersession happens by recorded, dated amendment only; nothing is
   silently rewritten.
4. The human forecaster is inside the protocol as a component to be
   calibrated, not an oracle outside it.
5. Decay is watched by law 6: every rule's calibration record is its
   life expectancy.

Elliott Wave fails every one of these five. That is the succession.

## 10. Relation to what already exists

This framework is not new machinery; it is the theoretical layer the
AVFI programme discovered empirically, piece by piece:

- The AVFI state machine: retained as the regime descriptor of the
  state layer. Its measured verdict stands: it describes regimes; it
  does not predict direction, and its timing content is weak (the
  clock study: 21-29 percent across the three adequately populated
  states, versus climatology 28.5).
- Rule set T: law 3 in production.
- V and V4h sizing: law 1 in production (vol targeting).
- The clock study: the clock layer's measurement instrument, with its
  frozen tables.
- The validation spine (RC, SPA, single-open holdout, FTEP): the
  falsification layer.
- Elliott Wave itself: retained as lineage and context (Balan's
  discipline, the alternation insight), the theory this framework
  replaces.

## 11. Open problems: where the hunger goes next

- **Hazard estimation.** Regime switching crossed with survival
  analysis: Hamilton's states meet Kaplan-Meier and Cox. Time-to-
  event methodology, identical in spine to clinical research. UPDATE
  12 Nov 2026: the Kaplan-Meier v0 exists (hazard layer v0, bundle
  document); Cox covariates (state, momentum, duration) are the next
  step.
- **The volume clock.** Clark's subordination measured on real NQ
  data. Blocked only by data quality.
- **Precursor signatures beyond volatility.** Can any weekly-
  observable footprint raise the event hazard above the tercile
  table? This is where AVFI returns honestly: not as an
  inevitability, as a testable signature with a calibration score.
- **Self-excitation measurement.** Hawkes estimation needs intraday
  data; documented as out of scope until the data exists.
- **The Bayesian forecaster.** Human prior times measured
  calibration: the formal version of integrating judgment into the
  hazard model once it has a score.

## 12. The honest close

The inevitable, unconditional rules exist: the six laws. They were
found, not invented, and they are the closest thing to market truth
anyone has. What they inevitably produce is a distribution, and the
anticipated event appears inside it with a probability you can state in
advance and a clock you can score. The theory that replaces Elliott
Wave is this: state instead of count, clock instead of prophecy,
calibration instead of belief. It is less romantic than waves, and it
has one property no wave theory ever had: it can be wrong in public,
which is the only way anything in markets can ever be right.
