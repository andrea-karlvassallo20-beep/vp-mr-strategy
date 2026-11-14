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

---

## Appendix — the full computable list, exact daily-OHLCV formulas

Every criterion below is computable from daily OHLCV alone (the data
already in the database — no procurement, no order flow, no on-chain).
Formulas are stated once here so the census extension, the backtests and
the Pine panel all implement the same definitions. W = window length;
all windows trailing, all signals finalized on bar close.

### State (Tier A — measured in the census)

| id | criterion | formula | default W |
|---|---|---|---|
| A1 | range position | `(C - min(L, W)) / (max(H, W) - min(L, W))` | 252 |
| A2 | realized-vol percentile | `percentrank(stdev(ln(C/C[1]), w1), W)` | w1=20, W=252 |
| A3 | coil days | consecutive bars with `H-L <= coilFrac × sma(H-L, W)` | W=50, coilFrac=0.75 |
| A4 | stretch z | `(ln C - sma(ln C, W)) / stdev(ln C, W)` | W=100 |
| A5 | volume ratio | `V / sma(V, W)` (the dry-up reading is < 1) | W=20 |
| A6 | year trend | `C / C[W] - 1` | W=252 |

### Derivatives and durations (Tier B — computable, not yet censused)

| id | criterion | formula | default |
|---|---|---|---|
| B1 | time since last significant move | bars since `|C/C[30] - 1| >= moveThresh` last held | moveThresh: crypto 100%, non-crypto 30% |
| B2 | consecutive quiet days | consecutive bars with `A2 <= quietPct` | quietPct=30 |
| B3 | time from 52w high | bars since `H == max(H, 252)` | 252 |
| B4 | vol-of-vol | `stdev(stdev(ln(C/C[1]), w1), W) / sma(...)` — the stability of the quiet state | w1=20, W=63 |
| B5 | contraction rate | `sma(H-L, w1) / sma(H-L, w2)` — < 1 means the coil is tightening | w1=10, w2=50 |
| B6 | ATR ratio | `atr(w1) / atr(w2)` — cheap redundancy with A2/A3 | w1=10, w2=50 |
| B7 | drawdown from peak | `C / max(H, 252) - 1` (the numeric grievance) | 252 |
| B8 | volume-trend direction | `sma(V, w1) / sma(V, w2)` — is the dry-up getting drier? | w1=10, w2=50 |
| B9 | prior-move magnitude | the largest `|C/C[30] - 1|` in the series' trailing 252d | 252 |
| B10 | board state (cross-sectional rank) | percentile rank of A2 (and A7) across the universe, same night — computable offline, not in a single-symbol Pine | universe |

### The composite signature (the census reading, made computable)

The dossier's forgotten-and-pinned signature, as a boolean state:
`A1 <= 0.25` AND `A2 <= 30` AND `A3 >= 10` AND `A5 < 1` AND `A6 < 0`
(low in range, quiet, coiled, dry, down on the year). The census says
72.3% of crypto up-moves started at the range bottom and 47.2% followed
quiet — the composite's *conditional* hazard versus matched controls is
exactly what C7-style testing must measure. The composite is a state
display and a hypothesis generator; it is NOT an entry signal.

**VERDICT (12 November 2026, the first causal test —
`night_before_test_report.md`):** given the denominator the census
lacked (6,767 matched state days, 156 series), the composite does NOT
raise the 30-day hazard of a +100% up-move (score 4–5: 2.6% vs score
0–1: 3.5%, p=0.11, flat in both time halves). What it measures is
protection: score 4–5 days carry roughly half the short-term crash
hazard (−30%/30d: 11.1% vs 20.0%, z=−7.29, p<0.001, stable in both
halves). The composite's value is on the downside, as a risk filter —
not an up-move predictor.

### Where each is implemented

- Census extension (Python, all of Tier A/B): `src/move_study.py` frame —
  to be extended, not yet run.
- Live nightly-before panel (all single-symbol criteria):
  `strategy/avfi_v5_night_before.pine` — the AVFI v4 engine with the
  full night-before state computed on every bar and shown in the
  dashboard, descriptive only.
