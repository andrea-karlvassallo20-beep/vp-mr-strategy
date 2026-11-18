# The W2 fresh-window battery - PRE-REGISTERED (do not tune after)

Written 2026-11-18, BEFORE any fresh forward window exists. This
document freezes the confirmation rules for the program's flagship
stack. If any constant below is changed after a W2 evaluation has
been run, the change is invalid (house multiplicity rule); a new
dated amendment is required before any re-evaluation.

## Purpose

Every chip measured to date is an in-sample descriptive conditional
(discovery panel). W2 is the mandatory fresh-window confirmation:
the same registered constructions, evaluated ONLY on windows that
did not exist at discovery time (forward bars accumulated after
2026-11-18, or the sealed one-shot holdout spent only on the
owner's explicit go). No threshold in this document was chosen
after seeing W2 data - none exists yet.

## Data and cadence

- Forward windows: `src/fetch_top250.py` re-run on a weekly
  cadence; new bars beyond 2026-11-18 accumulate the W2 sample.
- Burn-in: constructions need 756+252+20 bars; W2 nights are valid
  only where the full construction history exists (structural
  burn-in, as always).
- Data-quality guards carry over verbatim: sigma>0 guard (session
  49), valid close > 0.01, delisting/zero-volume handling, the
  flat-series exclusions.

## The candidates and their PRE-REGISTERED pass/fail lines

Each candidate gets ONE evaluation when its minimum n accumulates;
one miss kills the chip permanently (it moves to the dead pile with
the nuke_down chip). No re-runs, no threshold edits.

### C1 - THE FLAGSHIP WASHOUT BOTTOM (session 50/55)

- Construction: range_pos <= 0.25 AND fresh 20d close low AND
  vfi_pct <= 10 (session-40 flow); event exit: first >=4-sigma UP
  day (sigma>0-guarded) else 60d stop; one position per 60 days;
  no corrections; zero costs (declared).
- Minimum n: **30 episodes**.
- PASS: win rate >= 0.55 AND mean episode return >= +1%.
- KILL: anything else. Recorded context (not gates): the in-sample
  numbers were win 0.597 / mean +9.8% (n=404).

### C2 - THE AGED DEEP-WASHOUT ZONE (session 63: XB_old_low 0.753)

- Construction: flow z <= -1.5, days-in-zone > 10, range third =
  low. Label: P(first >=4-sigma move within 60d is UP).
- Minimum n: **200 nights**.
- PASS: P_first_up >= (universe baseline over the same fresh
  nights) + 0.05, AND P_first_up >= 0.63 absolute.
- KILL: anything else. Recorded context: in-sample 0.753 vs
  baseline 0.618 (n=1,592).

### C3 - THE TWO-CLOCK AGE LAW (session 60: first-half 0.720 /
  second-half 0.550 with fwd-20d +4.4% / -2.3%)

- Construction: positive flow segments (z >= 0 runs), ex-post
  first half vs second half of each segment.
- Minimum n: **1,000 nights each half**.
- PASS: (P_first_up first half - second half) >= +0.05 AND the
  fwd-20d means keep opposite signs.
- KILL: anything else.

### C4 - ABSORPTION AT LOWS (session 57/64: 0.661/0.662)

- Construction: rho >= 1.5 with |z| <= 0.5 on the day, at range
  thirds; label P_first_up; the pre-flow seat read.
- Minimum n: **150 seat nights**.
- PASS: P_first_up >= baseline + 0.03 at the low third.
- KILL: anything else.

### C5 - YOUNG EUPHORIA MOMENTUM (session 63: XA_young_high 0.743,
  fwd-20d +12.6%)

- Construction: flow z >= 1.5, days-in-zone <= 10, price third =
  high.
- Minimum n: **100 nights**.
- PASS: fwd-20d mean >= +2% AND P_first_up >= baseline + 0.03.
- KILL: anything else. (This cell is the program's only drift-type
  claim; a kill here kills ALL drift language permanently.)

## Multiplicity and process rules

1. One evaluation per candidate when its n is reached; the
   evaluation date and the data vintage are recorded in the
   programme log before the numbers are read.
2. The universe is the top-250 (session 59 rules) at evaluation
   time; membership drift is structural and accepted (recorded,
   not "corrected").
3. Half-split robustness (per-series midpoint of the FRESH window)
   is reported WITH each pass/fail but does not change the gate;
   it adjudicates only if a candidate lands EXACTLY on its line
   (within 1 point), in which case both halves must agree in
   sign - pre-registered now to remove later discretion.
4. Nothing in this battery arms anything, trades anything, or
   changes any registered dossier construction. A pass makes the
   chip "W2-confirmed in-window"; the water decision remains the
   owner's alone, with the sealed one-shot battery as the final
   gate before it.

## Standing queue after this document

Deep-read queue: "State-dependent Hawkes processes and their
application to limit order book modelling" (x947263, score 32).
Ratification queue: fifteen candidates, zero armed. T1 armed
awaiting the owner's word. Nothing trades live.
