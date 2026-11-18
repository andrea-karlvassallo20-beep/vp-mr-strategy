# The closeness dossier — each criterion's separation from the
# event, in the owner's triad order (price → volume → time)

Status: MEASURED DESCRIPTIVE work, owner-authorized 2026-11-18
("look historically all we saw and start building criteria list by
closeness to actual event starting from price and then volume and
then time"; the "both in parallel" decision — null-time reads
continue). Protocol pre-declared in `src/closeness_dossier.py`
BEFORE the run. No claim is tested, no direction is predicted, no
threshold is chosen: this is the ranked INPUT list for a future
pre-registered instrument (W1's family), not an instrument itself.
The confirm split comes LATER, on data this run never touches.

## 1. Universe and event (declared, honest limits)

- Universe: the cached discovery archive `paper/research/data/`
  (199 daily-OHLCV series — the archive the 1,461-move census was
  built from), every series with >= 781 days of history. The
  misses curriculum's 873-series mega-board kline cache is NOT
  present in this clone, so this run covers the cache-present
  subset; the subset covers 168 of the census's 399 series. The
  difference is declared, not hidden: these numbers describe this
  archive, and the mega-board rerun is a named follow-up.
- Event: a >=4-sigma daily move (|return| >= 4 x trailing-20d
  causal std), identical to the misses curriculum's definition.
- Evaluation: the state the NIGHT BEFORE each series-day, all
  windows causal and NaN-free.
- Closeness: "does a >=4-sigma move occur within K days after the
  evaluation day", K in {5, 10, 20, 60}.
- Statistic: rank AUC (Mann-Whitney) of each criterion between
  event nights and non-event nights, pooled. **AUC > 0.5 = higher
  values closer to the event; AUC < 0.5 = LOWER values closer;
  0.5 = no separation.**

## 2. The ranked dossier (pooled, all 199 series)

| triad | criterion | AUC K=5 | AUC K=10 | AUC K=20 | AUC K=60 |
|---|---|---|---|---|---|
| PRICE | rvol_pct (20d vol percentile, 756d) | **0.323** | 0.345 | 0.376 | 0.411 |
| PRICE | range_pos (position in 252d range) | 0.450 | 0.452 | 0.449 | 0.438 |
| PRICE | stretch_z ((close-252d mean)/252d std) | 0.475 | 0.471 | 0.464 | 0.453 |
| PRICE | ret30 (trailing 30d return) | 0.498 | 0.491 | 0.481 | 0.472 |
| VOLUME | vol_ratio (volume / 20d median) | 0.523 | 0.507 | 0.486 | 0.487 |
| TIME | comp_days (consecutive low-vol days) | **0.544** | 0.542 | 0.538 | 0.533 |
| TIME | days_since_move (nights since last 4-sigma) | 0.438 | 0.474 | 0.483 | 0.473 |

(n_event at K=5 ranges 9,187-18,556 nights and grows with K;
full counts in `closeness_dossier.csv`, crypto-only columns included.)

## 3. The reading (what the list actually says)

1. **The single dominant closeness criterion is PRICE-side
   QUIETNESS: rvol_pct, in the LOW direction.** A night within 5
   days of a >=4-sigma move has a volatility percentile that
   ranks below ~68% of ordinary nights (AUC 0.323 at K=5). The
   separation decays smoothly as the horizon widens (0.411 at
   K=60) — quietness is a NEAR-TERM closeness signal, decaying
   with lead time exactly as a "spark before the move" should.
2. **Position-in-range is the second PRICE criterion, also in the
   low direction** (AUC ~0.44-0.45), consistent with the priming
   rule's range_pos <= 0.35 leg.
3. **comp_days (TIME) is the best of the rest** (AUC ~0.54, mild
   positive): accumulated compression runs add a little separation
   at all horizons.
4. **VOLUME, at this grain, carries almost nothing.** vol_ratio
   is 0.49-0.52 across every horizon — near coin-flip. The
   owner's triad ordering is empirically price-first at the daily
   grain; volume's information, if it exists, lives at finer
   grains in the depth structure (session 21's distance-aware
   depth, session 24-25's passive-impact machinery), not in
   daily volume ratios. This is the daily-grain's own statement
   and licenses nothing about the L2 layer.
5. **stretch_z, ret30, days_since_move: weak (0.44-0.50).**
   Trend-stretch and move-recency are not closeness criteria at
   this grain.

Together with the misses curriculum (daily-grain lift 2.07, tiny
coverage 3.9%) and the sealed C7 measurements (direction is a coin
flip at 0.505; occurrence near-certain inside primed states:
0.940 vs 0.862 within 60 trading days), the dossier's ranked list
is the historical "clue list by closeness" the owner asked for:
**quiet + low-in-range + compressed = close to the event; loud
and stretched = not close; daily volume tells you almost nothing;
and NOTHING here says which way it will go.**

## 4. What this dossier does NOT license

- It ranks criteria; it does not choose thresholds, weights, or a
  trigger. Any combination step happens in a pre-registered
  instrument (W1's family) with kill lines, before confirmation
  data.
- All numbers are DESCRIPTIVE of the sealed discovery archive; the
  same ranking on the confirmation split (W2) is the only thing
  that could ever turn a criterion into evidence, and that data
  does not exist yet.
- Direction is roundly out of scope: the sealed p(up) = 0.505 and
  the census's up-heavy panel (75.9%, a panel property) both say
  the honest product is a WHEN instrument, sized on the posterior
  of MOVE — never a long/short call.
- The subset-versus-mega-board difference is open territory: the
  873-series rerun is a named follow-up, not a silent assumption.
- Nothing here trades live, ever.

## 5. Reproduction

`python3 src/closeness_dossier.py` (pandas/numpy; ~2 minutes for
the 199-series archive). Outputs:
`paper/research/clue_scan/closeness_dossier.csv` ( ranked rows;
this document is `closeness_dossier.md`).
