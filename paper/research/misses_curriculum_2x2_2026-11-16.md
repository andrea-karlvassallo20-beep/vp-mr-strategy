# Task 2 — the misses curriculum, quantified: the 2x2 matrix and the base rates

Status: DESCRIPTIVE, on the SEALED discovery panel (the 1,461-move
census, `paper/research/clue_scan/move_study.csv`). No claim is tested
here; the census has no discovery/confirmation split (W2 of the
methodology review) and every number below is a description of what
the panel contains, not a prediction. The priming rule is the frozen
one (`src/dormancy_tracker.py`): comp_days >= 20 AND rvol_pct <= 33
AND range_pos <= 0.35, evaluated at the pre-move state.

## 1. The 2x2: flagged x move direction (all 1,461 census episodes)

| | move UP | move DOWN | row total |
|---|---|---|---|
| **flagged (primed_before)** | 136 | 7 | **143** |
| **not flagged** | 973 | 345 | 1,318 |
| **column total** | 1,109 | 352 | 1,461 |

## 2. The base rates (the coverage the owner asked for)

- **P(move is UP) = 1,109/1,461 = 75.9%.** The census itself is
  up-heavy — a property of the panel and the move-finding thresholds,
  not a market law. Every direction number below travels with this
  denominator.
- **P(flagged) = 143/1,461 = 9.8%** — the overall detection rate of the
  priming rule over the census.
- **P(flagged | UP move) = 136/1,109 = 12.3%.**
- **P(flagged | DOWN move) = 7/352 = 2.0%.**
- The rule detects UP breakouts at **6.2x** the rate of DOWN
  breakouts. This is a DETECTION asymmetry, not a directional
  probability (see §4).

Per class (flagged / class n):

| class | flagged | class n | detection | P(flagged|up) | P(flagged|down) |
|---|---|---|---|---|---|
| crypto | 135 | 846 | 16.0% | 130/751 = 17.3% | 5/95 = 5.3% |
| commodity | 5 | 253 | 2.0% | 4/143 = 2.8% | 1/110 = 0.9% |
| index | 2 | 87 | 2.3% | 2/42 = 4.8% | 0/45 = 0.0% |
| equity | 1 | 275 | 0.4% | 0/173 = 0.0% | 1/102 = 1.0% |

The coil's detection lives almost entirely in crypto (135 of 143
flags); outside crypto the rule is near-blind (8 of 615). The
grievance-scope caveat of the methodology review (W4) stands.

## 3. Magnitude base rates

- Median |move30d| of flagged episodes: 1.34; of unflagged: 0.92
  (census units). The moves the rule catches are LARGER than the ones
  it misses — consistent with the C7 occurrence record (the coil
  precedes bigger releases), and consistent with the misses' median
  pre-state (no compression, mid-range volatility, no stretch).
- Artifacts: 61 census episodes carry the artifact flag; only 1 of
  them is flagged. The rule is not an artifact machine.

## 4. What the 2x2 does NOT say (read this before citing it)

- **It is NOT a direction signal.** P(flagged | up) > P(flagged | down)
  is a statement about which moves the rule DETECTS, conditioned on a
  move having occurred. The direction question is the reverse
  conditional — P(up | flagged) — and it is answered by the
  coil-conditioned samples: the C7 panel and the watchlist, where 3
  of 4 primed coils broke DOWNWARD. Both facts coexist: among census
  moves, ups were more often preceded by the coil; among primed
  coils, the realized break direction is not claimed (and the
  watchlist's first reading leaned down). The 0.505 boundary is not
  on trial and nothing here touches it.
- **It is NOT out-of-sample.** The census is the discovery panel; the
  detection rates above are its honest description. The
  second-generation rule (pre-registered) validates only on the
  forward window that does not yet exist.
- **It is NOT the C7 record.** C7's sealed +7.9 points are occurrence
  over matched quiet controls on daily data; this census is a
  different denominator (4-sigma episodes) and a different question
  (coverage).

## 5. The curriculum lesson, quantified

The priming rule is a low-coverage, up-detecting, crypto-native,
magnitude-correlated clue: it sees roughly one in eight up-breakouts,
one in fifty down-breakouts, almost nothing outside crypto, and the
moves it misses are systematically smaller and quieter-starting. This
is the base-rate table the misses curriculum needed: the honest
denominators for any future claim about what the coil "predicts" —
and the quantitative case for why the endpoint is a WHEN instrument
with the trigger doing the timing, not a direction call wearing a
coil.
