# SMH Methodology Review — thinking time, 2026-11-15

Written while the L2 environment is being set up. This is the programme
stepping back and asking: is the method sound, where can it fool itself,
what is the endpoint, and what can move *now* while the paid data is
pending. Nothing here tests a claim. It is the map.

---

## 1. The endpoint — what this programme terminates into

The Salient Market Hypothesis says: knowing WHAT will move outranks
knowing WHEN, and both outrank knowing WHICH WAY. The falsification
programme exists to convert that sentence into one of exactly two
terminal states:

1. **A verified WHEN clock.** At least one timing mechanism (daily
   coil, event-clock compression, queue-geometry) that survives its
   pre-declared kill lines out-of-sample, on data it never saw, with
   the multiplicity tax paid (DSR) — then Layer 4 shadow, then capital
   sized by posterior on MOVE, not on UP.
2. **A clean falsification record.** Every claim in the ledger dead
   with its kill line named, and the honest product is the record
   itself: what was tried, what was measured, what refused to survive.

Both are successes. The only failure state is drift: untested claims
accumulating, "promising" features never facing kill lines. The
registry has prevented that so far; this review exists to keep it that
way.

**The direction result is already in, and it is an asset.** The 0.505
boundary [0.497, 0.513] has survived every test thrown at it. The
watchlist's first forward reading — three of four coiled assets broke
DOWNWARD within two days — is the same lesson in the field: the coil
predicts *movement*, not *sign*. The endpoint should therefore be
re-framed, explicitly and in writing: **we are building a WHEN
instrument, straddle-logic, sized by the posterior probability of
MOVE.** Any Layer 4 design that quietly re-introduces directional
sizing is smuggling a dead claim back in.

## 2. Where the method can fool itself — five honest weaknesses

**W1 — The priming rule was born on its own test set.** The
comp_days/rvol_pct/range_pos rule was derived from the same panel it
now decorates. The watchlist (ends 2027-01-11) is the first true
out-of-sample reading. The misses table quantifies the risk already:
of 1,461 census moves, the rule flagged 143 (16% in crypto, ~2% in
equities). *Improvement:* freeze the current rule (no re-tuning on the
discovery panel); pre-register a second-generation rule from the
misses' signatures; validate it ONLY on a forward window that does not
yet exist (2027 data). Until then, the rule is a clue with a measured
detection rate, published as such.

**W2 — The census has no discovery/confirmation split.** 1,461
episodes, all examined, no holdout. Any pattern "found" in the census
today is fit to the whole sample. *Improvement:* declare the census
SEALED as a discovery set. All new descriptive statistics must be
computed on a designated confirmation window (e.g., 2026-12 → 2027-06
episodes) and reported side-by-side. The miss decomposition should be
re-run there first.

**W3 — Two clocks, one hypothesis.** The coil is a wall-clock
phenomenon on daily bars. The L2 tests (compression duration, queue
drain) are event-clock phenomena. T3 exists precisely because if the
two clocks disagree, the SMH is really two hypotheses wearing one
name. *Improvement:* T3 must run BEFORE C1-L2 is interpreted, not
after — otherwise we will explain L2 results with a clock the L2 data
cannot see. The multi-month aggTrades download for T3 has started
today (free Binance Vision archives, 2024-08 → 2025-02, BTCUSDT).

**W4 — The grievance column was empty outside crypto.** The
frustration machinery (funding trap, OI divergence, basis extreme)
found scores of 7–20 on commodities/equities vs 72.3 for storjusd.
The SMH's "grievance" language currently has one operational
definition, and it is crypto-native. *Improvement:* before claiming
the hypothesis generalizes, define non-crypto grievances in
measurable terms: COT positioning extremes and inventory builds for
commodities; buyback-blackout windows and short-interest squeezes for
equities. Until then, the honest scope statement is: the grievance
clause is tested only where funding/OI/basis exist.

**W5 — The heat map is a coincidence machine at scale.** 1,325
series scanned for silence finds silence by construction; blue cells
will "predict" moves at the base rate and some will look prophetic.
*Improvement:* the dormancy table must never be read as a call list.
Its formal role is one: the sampling frame for the forward
confirmation window in W2 — every asset that moves gets logged, and
the detection-rate table gets its honest denominator.

## 3. What moves NOW (the unblocked queue, in value order)

1. **T3 on aggTrades (in progress).** Free, registry-directed, and the
   methodological hinge (W3). Kill line: trade-arrival density stays
   significant (p<0.01) after hour-of-day stratification on the
   event-clock Cox. Data downloading; harness next.
2. **The misses study (descriptive, legal).** Cluster the 1,258
   missed moves by pre-move signature: is there a common second-order
   clue (vol-of-vol collapse, volume drought, consecutive
   lower-highs) that separates them from random base-rate moves?
   Output feeds the W1 second-generation rule — but the rule is only
   pre-registered, never validated, on the discovery panel.
3. **Board-refresh automation.** One command (`src/board_refresh.py`,
   to be written) that re-pulls klines, recomputes the dormancy table,
   and appends a dated row to a board history CSV. The 2026-11-14
   refresh was done by hand; the next one should be `make board`. This
   compounds: every future session starts from a fresh board for free.
4. **Reading, reprioritized.** The queue stays as published, but the
   L2 chapters are now load-bearing, not background: Bouchaud's
   Hawkes and queue chapters, and the limit-order-book sections of
   the algorithmic/HFT books, move to the front — they are the
   literature for C5/C6 and the exact models we are about to fit.
5. **A public claims-ledger page.** The falsification record exists
   in the repo; the site shows the epistemics but not the live ledger
   state (C1 dead, L0 partial-pass, C5/C6/C7 blocked-on-data, T1–T3
   pending-free). One page, one table, updated with every PR. The
   programme's credibility is its honesty; the ledger is the honesty
   made visible.

## 4. What I deliberately did NOT put on the list

- No new features for the board. The feature factory is closed until
  the forward confirmation window exists (W2).
- No directional anything. The boundary held; the endpoint is WHEN.
- No multi-pair expansion. BTCUSDT survives first or nothing does —
  the C7 gate clause stands.
- No re-tuning of the priming rule on the discovery panel, however
  tempting the misses table makes it.

## 5. The one-sentence version

While the L2 environment is being set up: download the free data T3
needs (started), freeze the discovery panel, pre-register the
second-generation rule from the misses, automate the board, read the
chapters the next tests will quote — and keep every untested sentence
out of the ledger until its kill line is written first.
