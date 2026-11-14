# The night-before criteria registry — what a prior day can and cannot tell us

A complete, tiered list of what can be derived and learned from the prior
day (the last quiet day) of significant move episodes, for prediction
research. Built from the move census (1,461 episodes, `move_study.csv`),
the night-before gallery (92 panels, `night_before.csv`) and the
hundredfold board (`hundred_moves.csv`). Dated 12 November 2026.

The framing rule, stated once and binding: **"predict" means conditional
hazard — does state X on day D raise the measured probability of a
significant move within a stated window, versus matched controls that
shared the state and did not move?** The census alone cannot answer this
(it has no controls); it supplies the base rates and the candidate
variables. Only the matched-quiet comparison (the C7 method, +7.9 points)
and the dual-split gate convert any criterion below into a belief.

---

## Tier A — already measured on the night before (in the record)

These have census base rates right now. Each row: what it is, what the
census says, and what a causal test would need.

| # | criterion | census reading (crypto UP, n=714) | what a test needs |
|---|---|---|---|
| A1 | **Range position** — where price sits in its 52-week range on the last quiet day | 72.3% of up-moves start at the range bottom | matched controls at the range bottom that did NOT move; the base rate of "at range bottom" on a random day is the missing denominator |
| A2 | **Quiet** — realized vol at or near its own low percentile (`rvol_pct`) | 47.2% preceded by quiet | matched-quiet hazard vs matched-loud hazard, same window (the C7 form) |
| A3 | **Coil depth** — days in compression (`comp_days`) and the depth of the coil | 20.9% preceded by a deep coil; crown jewel LSK at 170 days | hazard as a function of coil days (a curve, not a threshold); KMD's no-coil +2,094% already caps "coil is necessary" |
| A4 | **Stretch** — z-score versus own recent trend (`stretch_z`) | measured per episode in `move_study.csv` | stretch-conditioned hazard; the stretch-depth curve already exists for the bottom side (deeper pays, no falling knife) |
| A5 | **Volume dry-up** — volume vs own median (`vol_ratio`) | the dry-up reading is in every night-before panel | dry-up-conditioned hazard vs matched-volume controls |
| A6 | **Year trend** — 52-week trend at the night before (`trend_52w`) | down-on-the-year is the common mover picture | trend-conditioned hazard; interacts with A1 (low in range AND down on the year is the forgotten-and-pinned signature) |

What Tier A has already **derived**: the composite signature. Individually
each criterion is weak; jointly (low in range + quiet + coiled + dry +
forgotten) they describe the pre-move state of crypto's up-moves. Whether
the composite beats its parts is itself a testable claim.

## Tier B — derivable from data already in the database (not yet measured)

Computable today from the existing daily OHLCV panel; each is a candidate
extension of the census, not a new finding until run:

| # | criterion | what it would add |
|---|---|---|
| B1 | **Time since last significant move** | does recency of a prior move suppress or raise hazard? (the "no two lions from the same bush" question) |
| B2 | **Consecutive quiet days** (not just quiet level) | duration of the quiet state, not merely its depth — hazard may live in the spell age, exactly as the SMH clock claims |
| B3 | **Distance from 52w high / low in time**, not just price | how long has it been forgotten? |
| B4 | **Vol-of-vol** — stability of the low-vol state | a single quiet day is noise; a stable quiet regime is a state |
| B5 | **Range contraction rate** — is the coil tightening, static, or loosening? | the derivative of compression, not its level |
| B6 | **ATR ratio** (short ATR vs long ATR) | a second, cheaper compression measure; redundancy with A2/A3 is a feature to be measured, not assumed |
| B7 | **Drawdown from peak at the night before** | how deep is the grievance? (the dossier's grievance column, made numeric) |
| B8 | **Volume trend direction** — is the dry-up getting drier? | the derivative of A5 |
| B9 | **Prior-move magnitude in the same series' history** | does a series that has moved big before move big again? (LSK had; is that typical?) |
| B10 | **Cross-sectional rank** — the state of the whole board that night | the 2026-11-12 board state (bleeding while coiling) is exactly this; hazard may be board-conditional, not just asset-conditional |

## Tier C — plausibly predictive but blocked (data does not exist yet)

Named so nobody rediscovers them as if new; none may enter testing until
its data passes the acquisition gate (see `l2_data_acquisition_spec.md`):

| # | criterion | blocked on |
|---|---|---|
| C1 | Order-book imbalance / liquidity withdrawal at the night before | L2 data (Tardis procurement) |
| C2 | Funding rates and open interest (perp positioning of the crowd) | derivatives data |
| C3 | Options skew / term structure (priced expectations of the move) | options data — already flagged in the SMH charter as the unseen-ness test |
| C4 | Attention proxies (search, social, listing announcements) | external data; also the strongest contamination risk — attention is how the lion gets spotted, and spotting it may kill it |
| C5 | Stablecoin flows / exchange inflows (dry powder) | on-chain data |

## What the prior day can NEVER tell us

On the record, so the registry is not oversold:

1. **Direction at a chosen time.** The SMH refuses it; the census supports
   the refusal (the up and down signatures are near-mirror images of the
   same state — the state conditions hazard, not sign).
2. **The move's size.** LSK's 170-day coil did not encode +895%; nothing
   in the night-before panel scales with the outcome.
3. **Which specific asset.** Base rates are fractions per class; picking
   the one mover out of a hundred quiet assets is a different problem
   (the watchlist problem) and is only answerable forward.
4. **Timing to the day.** The census windows are 30 days; nothing measured
   distinguishes day 3 from day 27.

## How a criterion becomes predictive — the only path

For every row above, the identical conversion rule applies:

1. **Base rate** from the census (what fraction of movers showed it).
2. **Control rate** from matched non-movers that shared the state — the
   step the census cannot do alone.
3. **Causal rule** declared in advance (entry, window, exit).
4. **Dual-split gate** — beat the current parameters on BOTH out-of-sample
   windows, scored at the worse one.
5. **Forward log** — pre-logged candidates, read when the window closes,
   whatever it says.

The four pre-logged forward candidates (KAVA, HOLO, GENIUS, SOL, window
closing 2027-01-11) are the first live pass through this path.

Descriptive registry; multiplicity binds; C7 sealed. A registry lists what
can be asked — the gates decide what is true.
