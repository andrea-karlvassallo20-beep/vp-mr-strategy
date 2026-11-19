# The misses curriculum's missing leg: the C1-L2 spec confronts the base-rate
# table — descriptive, nothing measured

Front/goal: null-time session 61 (log ## 65), 2026-11-19, the front-3
completion leg under the goal-autonomy conductor protocol (v2, edition 2).
The null-time queue's own item stated the endpoint this note finishes: the
misses curriculum's 2x2 "becomes the reference the C1-L2 spec must confront."
Verified this session by direct search of `paper/research/c1_l2_test_spec.md`:
zero matches for "misses," "base rate," "base-rate," "coverage," or "lift."
The C8 spec (`paper/research/c8_macro_l2_synthesis_spec.md`) likewise carries
no misses/base-rate reference. The confrontation had never been written. This
note writes it. Mid-flight renumbering, disclosed: this note and its log
entry were first drafted as session 59 / log ## 63 against a main at
56add4c; the push-time race check found a parallel session had landed
deep-read 51 as ## 63 (the Wang-Xu-Zhu Hawkes-IG paper, xf77014,
consuming that pointer), so this session first renumbered to session
60 / log ## 64; while that head's CI ran, PR #232 landed the GOALS.md
status-board and encoding-sanity session as ## 64 / null-time session
60, so this note's entry renumbers AGAIN, to session 61 / log ## 65,
per the main-wins protocol; the queue the landings name was unchanged
by either landing (thirty plus probe E1, zero armed, at this note's
rebuild).
Descriptive only: no experiment, no fit, no data run, no new
numbers computed this session, no claim tested, no kill line touched, C7
stays sealed, nothing armed, nothing trades live.

## What the frozen tables of record say (quoted, not recomputed)

Every number below is the frozen output of the pre-declared protocol run of
2026-11-16, quoted from `paper/research/clue_scan/misses_curriculum.json`.
NOTHING in this session re-ran the protocol: the klines it needs live in the
codespace (verified: `data/raw` in this environment holds only the L2 sample
placeholders), and a re-run would be a new measurement belonging to a session
that declares it, not a quotation. The reference of record is the frozen
output, not a re-computation.

The board-level 2x2 (873 series, 1,765,316 series-days, 14,541 four-sigma
days; priming rule frozen everywhere else: comp_days >= 20 AND rvol_pct <=
33 AND range_pos <= 0.35, evaluated at t-1; move = |daily simple return| >=
4x trailing 20-day std, causal):

- A (primed, moved) = 570; B (primed, silent) = 33,595;
  C (not primed, moved) = 13,971; D (not primed, silent) = 1,717,180.
- Coverage A/(A+C) = 0.0392 — the priming rule sees fewer than one in
  twenty-five of the big daily moves.
- P(move | primed) = 0.01668; P(move | not primed) = 0.00807;
  lift = 2.07. Base priming rate on the board: 0.0194.

The census-level 2x2 (`paper/research/misses_curriculum_2x2_2026-11-16.md`,
the 1,461-move discovery census): detection 143/1,461 = 9.8% overall,
UP-detection 12.3% vs DOWN-detection 2.0% (a detection asymmetry, NOT a
directional probability), the flags almost entirely crypto (135 of 143).
Every one of those caveats travels with the numbers; the census is the
discovery panel; none of this is out-of-sample; the direction boundary
(0.505) is not on trial and nothing here touches it.

## The confrontation, stated plainly

The C1-L2 test asks: was the daily C1 null a resolution artifact, or a real
absence? That question is now unanswerable as posed without the daily
base-rate table beside it, for one mechanical reason: the daily grain is
NOT silent. Daily priming already lifts big moves 2.07x, at 3.9% coverage,
on the same cached universe the L2 phase will draw its regime context from.
A future L2 positive that reported compression-conditioned hazard without
the daily table beside it could sell as book-resolution discovery what the
daily table already delivers for free. That is the laundering channel this
leg exists to close, BEFORE the gate passes and while the spec is still a
draft (the blocking state is a feature here: the spec is DRAFTED, NOT RUN,
blocked on Tardis L2 data behind the L0 gate, so a ratified confrontation
installs with zero risk of post-hoc fit — the numbers it cites were frozen
2026-11-16, the test has not run, and the L2 data does not exist yet).

## The proposed confrontation paragraph (draft, PENDING OWNER RATIFICATION)

The text below is queued as a candidate sharpening (the thirty-first), NOT
installed. It would be added to `paper/research/c1_l2_test_spec.md` as a
pre-declared section before the L0 gate passes, if and only if the owner
ratifies. It tightens the spec, harder-to-pass in four named ways:

1. **The daily reference is quoted whole, in the spec, before the gate.**
   The frozen 2026-11-16 table's five numbers (coverage 0.039, P(move|primed)
   0.01668, P(move|not primed) 0.00807, lift 2.07, base priming rate 0.0194,
   over 873 series and 1,765,316 series-days) appear in the spec itself and
   in any report the test ever produces. The reference is the frozen output
   of record; descriptive re-runs never replace it (they may be reported
   beside it, dated, all cells shown).
2. **The novelty statement is pre-declared, not post-hoc.** Before the gate,
   the spec states what a positive must add beyond the daily table: timing
   finer than the daily grain and/or coverage beyond the daily 3.9%. A
   positive that offers neither is a re-discovery of daily priming at finer
   sampling and must be reported as such.
3. **The horizon bridge is pre-declared.** The spec's labels are wall-clock
   (primary H = 24h, secondary H = 72h); the daily table counts >=4-sigma
   days within 10 daily bars. Before the gate, the spec fixes the
   aggregation that maps the L2 hazard onto the daily horizon for the
   comparison, or states explicitly that they are non-comparable and why
   the claim survives without the comparison. The bridge is frozen before
   the data; it is never reconstructed after a result.
4. **The lift travels with every effect size.** Any reported compression-
   conditioned effect at L2 carries the daily lift 2.07 printed beside it
   in the same table row, so no reader — and no future session — can read
   an L2 effect in isolation from what the daily grain already knew.

Killed-if-wrong, stated: without this rule the programme's most expensive
future test could return a positive that daily data trivially reproduces,
and the record would carry it as a book-resolution discovery — the exact
laundering shape the deep-read family keeps catching (the ## 45
synthetic-rebuttal precedent, the ## 61 equilibrium-determinism caution),
this time pre-empted at the spec instead of caught post-hoc.

## Instrument observations recorded (front 8, audit by reference, no action)

Three state observations, verified this session, recorded for the
owner/codespace; front 8 says instrument upkeep is automated and never
re-done by hand, so this session acts on none of them:

- `src/misses_2x2.py` — the per-class lead-lag 2x2 built 2026-11-16, its
  protocol pre-declared and parity-pinned, "wired into the nightly
  board_refresh cycle" per log section 7 — has NO outputs on main. No
  `misses_2x2.csv`, no per-series file, no dated report exists anywhere in
  the tree. The founding record says its first real run "happens in the
  codespace where the klines live"; that run has either never happened or
  its outputs have never been committed. The confrontation paragraph above
  deliberately cites only the frozen board-level table, whose outputs ARE
  on record.
- `paper/research/clue_scan/board_history.csv` holds exactly one snapshot
  row (2026-11-16). Three nights have passed. There is no in-repo evidence
  the nightly cycle has run since founding. If the codespace cycle is
  running but not committing, the surprise ledger — the programme's
  cheapest falsification instrument — may be accumulating off-repo or not
  at all. Observation only.
- `logs/board_surprise_ledger.jsonl` likewise holds the founding nights'
  snapshots. Same observation, same non-action.

None of this blocks front 3's writing leg, which is what this session
executed. All three are named so the owner can check the codespace side in
one look at the next directorate sitting.

## Standing pointers

Ratification queue after this session: THIRTY-ONE candidate sharpenings
plus probe E1, zero armed (the thirty-first is the C1-L2 base-rate
confrontation drafted above; `docs/DECISIONS_PENDING.md` updated per the
rule). No paper was read this session and no pointer was consumed by it;
the live next UNREAD per the landed ## 63 (deep-read 51) is "Application
of Hawkes volatility in the observation of filtered high-frequency
prices" (score 28, xb710f4), then "Self-exciting price impact via
negative resilience in stochastic order books" (score 28, x77c554).
A successor session must re-read the live main tail and the branch/PR set,
consult `docs/goal_autonomy_protocol.md` (v2, edition 2), and record its
work choice and reason in its session-state note. Nothing measured, no kill
line moved, nothing armed, nothing trades live.
