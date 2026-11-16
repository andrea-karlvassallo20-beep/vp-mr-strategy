# The 1-year roadmap (null-time draft, owner to ratify)

Status: a PLANNING DOCUMENT, not a pre-registration. Nothing here arms a
claim, moves a kill line, or spends data. Every test below still requires
its own spec, its own kill lines, and - where multiplicity is involved -
its own pre-declared family, BEFORE any data touches it. Dates are
relative (T0 = the day the Codespaces environment first gates real L2).

## Where we are

- Phase 1 (Daily/AVFI): CLOSED. Three independent deaths of the
  OHLCV-compression family (C1 daily, the watchlist, C7-30m).
- Phase 2 (Crypto L2): ACTIVE. The L2 data acquisition spec, the C1-L2
  test spec, the C7-L2 integration spec, and the C8 synthesis spec are
  all pre-registered; the environment (devcontainer + Makefile) is
  ready; the data is not yet bought and pulled.
- Standing null-time evidence: the nightly sealed-prediction ledger
  (`src/surprise_ledger.py`) accumulates priming-score ranking
  resolution pairs every day at zero data cost.

## Quarter 1 (T0 to T0+3 months): the C1-L2 window

1. Codespace up; `make gate-day` on the verified free day; parity
   anchors reproduced (2026-10-01: 145,203,455 rows, mid 100/100, depth
   100/100; 2026-10-10: 78,904,284 rows, 1 block).
2. Buy and pull the 2-4 week BTCUSDT window, one day at a time:
   gate -> convert (verified row counts) -> next day. Commit every gate
   log with its exit code.
3. Macro censor, label, fit: run C1-L2 per the frozen spec. The five
   kill lines are binding asserts; no re-runs, no horizon shortening, no
   post-hoc rescue.
4. While the data decision is pending: keep the sealed-prediction ledger
   running. At ~100 resolutions, the priming score's ranking at daily
   grain gets its own honest verdict (rho vs zero) - a named, dated
   death if it fails, a sharpened motivation for C1-L2 if it holds.

## Quarter 2: the branch point

### If C1-L2 PASSES (concordance > 0.52, all kill lines silent)

- The finding is recorded with its effect size and CI; nothing is
  promoted to a strategy - the programme never trades live by charter.
- C8 (Macro-L2 Synthesis) arms next, per its own spec, with the five
  review amendments recorded first (pure interaction estimand,
  difference-of-differences with DML, the Hawkes shuffled-arrival
  placebo, the fixed VPIN volume clock, the defined market factor).
- The forward paper test: sealed predictions on rolling fresh L2
  windows (never the training window), resolved by the existing ledger
  machinery. A passing backtest plus a passing sealed forward window
  is the only honest pair.
- Write the paper (`docs/smh_paper_draft.md` is the skeleton): the
  three deaths, the L2 result, the methodology.

### If C1-L2 FAILS (any kill line fires)

- Record the death with the same ceremony as C7-30m: a dated verdict
  page, the ledger row, the kill line that fired, the number.
- The question moves, it does not die: C8's motivating observation (the
  Tesla-day anatomy) survives C1-L2's death by design - C8 is an
  interaction claim, not a main-effect claim. But C8 runs ONLY on gated
  L2 regardless, so the data decision is unchanged; what changes is the
  prior and the paper's title.
- If both C1-L2 and C8 eventually fail: the honest endpoint is closure
  of the compression family at all measurable grains, and the paper
  becomes the falsification record. That is a publishable result and
  the programme's stated purpose - the falsification spine is the
  product.

## Quarter 3-4: portfolio scaling, WITHOUT violating the multiplicity rules

The danger is not finding nothing; it is finding something by asking
78 more questions. The rules, pre-declared here and binding:

1. BTCUSDT is the only asset in the C1-L2 spec. Any expansion to ETH,
   SOL, or the perp universe is a NEW pre-registered amendment with
   its own family declared BEFORE the first new asset's data is pulled.
2. One family, one battery: all assets enter a single pre-declared
   family with a max-t (White reality check / SPA) or DSR deflation
   across the whole family - the same discipline that killed the 27-
   combo AVFI grid. Per-asset "discoveries" that do not survive the
   family-level correction are costume, not edge.
3. The expansion order is fixed ex ante by liquidity (BTC, ETH, then
   the top perps by volume), not by which asset looks best in a scan.
   No asset is added because it "looks promising" - that sentence is
   the definition of the multiple-testing trap.
4. Cross-asset claims (lead-lag, spillover) are a separate family with
   their own spec; they are never evaluated inside the per-asset
   family's budget.
5. Costs and capacity are part of every spec from the start (K7-style
   cost survival): an edge that dies at realistic taker fees is
   dead, and its death is recorded the same hour.

## Standing infrastructure commitments (all quarters)

- The nightly paper-trading session, the board refresh, and the
  sealed-prediction ledger keep running; they are the cheapest
  evidence in the programme.
- Prose rot is a named enemy: the claims ledger and the website status
  are updated with every verdict (the landing page now states: Phase 1
  closed, Phase 2 active).
- Nothing is pre-built beyond the frozen specs: the test is frozen
  before the data; the environment is ready; the discipline is the
  moat.
