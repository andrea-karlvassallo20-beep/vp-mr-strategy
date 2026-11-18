# The coin-chip dossier — conditional DIRECTION tilts, measured
# (the owner's "which way is the coin chipped" question, answered)

Status: MEASURED DESCRIPTIVE work, owner-authorized 2026-11-18
("everyone gets to flip a coin, but you wanna make sure you know
which way it has been chipped... after nukes highest likelihood to
go up, or after a base is built"). Second measured session of the
parallel regime. Protocol pre-declared in `src/coin_chip_dossier.py`
BEFORE the run, with two data-quality fixes declared and dated in
the file's preamble (dead-coin sub-cent closes invalidate the
night; forward returns outside [-0.95, +10] dropped as delisting
artifacts; up-share recomputed as up-days / move-days after the
first pass measured the wrong denominator — the corrected third
run produced every number below). No claim is tested, no threshold
is chosen, no instrument is armed: descriptive on the discovery
archive, whose confirm split remains mandatory. No kill line
moved; nothing trades live.

## 1. Protocol (declared)

- Universe: the cached 199-series discovery archive (as session
  34's closeness dossier), every series >= 781 days.
- States, causal at the evaluation night:
  - **post_nuke_down**: a >=4-sigma NEGATIVE day within the last 2
    days — the owner's "nuke" (a capitulation-style crash day);
  - **post_nuke_up**: a >=4-sigma POSITIVE day within the last 2
    days — the owner's "trend" momentum case;
  - **primed**: the frozen rule (comp_days >= 20, rvol_pct <= 33,
    range_pos <= 0.35);
  - **base**: quiet (rvol_pct <= 33) AND near the bottom of the
    252-day range (range_pos <= 0.15), no compression requirement —
    the owner's "base is built";
  - **all**: every valid night (the baseline coin).
- Labels: direction of the FIRST >=4-sigma move within 60 days;
  up-share of all moves in the 60-day window (up-days / move-days);
  K-day forward drift, K in {5, 20, 60}, mean and median and
  P(>0).

## 2. The chip table (the answer)

| state | n nights | **P(first big move is UP)** | up-share of moves (60d) | mean / median 20d drift | mean 60d drift |
|---|---|---|---|---|---|
| post_nuke_down | 1,705-3,108 | **0.748** | 0.555 | +0.9% / 0.0% | -0.6% |
| post_nuke_up | 2,112-4,173 | **0.767** | 0.599 | **+2.3%** / 0.0% | +0.2% |
| primed | 8,571-14,246 | 0.635 | **0.654** | +0.9% / -1.4% | **+4.0%** |
| base | 15,049-26,607 | **0.645** | **0.668** | +0.4% / -2.0% | **+1.8%** |
| **all (the coin)** | 129,017-289,262 | **0.576** | 0.585 | -0.1% / -2.3% | +0.0% |

## 3. The reading (which way the coin is chipped)

1. **The panel's coin is ALREADY up-chipped at baseline: 57.6%**
   of first big moves go UP. Nothing in this archive is a 50/50
   coin — every conditional below must be read against 0.576, not
   against 0.500.
2. **The owner's "after nukes" chip is REAL and the largest one
   measured: 74.8%** of first big moves after a >=4-sigma CRASH
   day go UP — an 17-point chip over the panel baseline, on
   n = 1,705 nights. The owner's instinct survives contact with
   the archive, quantified.
3. **The momentum chip is even stronger: 76.7% after big UP days**
   — the "trend" side. Post-nuke-up nights also carry the largest
   clean 20-day mean drift of any state (+2.3%, vs -0.1% baseline).
4. **The "base built" chips: 64.5% first-move up, 66.8%
   up-share** — the conditional the program already owned through
   the priming rule (6.2x detection asymmetry), now stated as a
   direction probability; and primed/base states carry the largest
   60-day mean drifts (+4.0% / +1.8% vs +0.0% baseline).
5. **The honest boundary: medians stay negative almost everywhere
   (the panel's drift is decaying; crypto through bear years).**
   The chips live in the FIRST-MOVE DIRECTION and the up-share-of-
   moves, NOT in median K-day drift: "which way the first big move
   goes" is chipped; "is the next K-day return positive" is not.
   Any instrument built on these numbers times and sizes the first
   big move; it does NOT hold direction.
6. **These are descriptive discovery-panel numbers.** The archive
   is crypto-heavy, spans bear-biased years, and the >=4-sigma
   construction is absolute-return-based (cheap/meme series move
   more); the confirmation split (fresh windows, pre-registered
   thresholds) is mandatory before any conditional here becomes
   evidence, per the W2 rule and the label-placebo discipline.

## 4. What this does not license

No threshold, no instrument, no arming; no direction claim at any
grain other than the first-move object measured here; no
portability to Binance perps L2 windows; nothing trades live.
The chip table is the owner's requested "which way is it chipped"
input — the unifying clue dossier (quietness/order/time from the
closeness dossier) now has its direction column.

## 5. Reproduction

`python3 src/coin_chip_dossier.py` → `coin_chip_dossier.csv`
(this document: `coin_chip_dossier.md`).
