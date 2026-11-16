# Case study: the Tesla day — BTCUSD_PERP, 2021-02-08

A teaching case in the dossier's night-before format. One event, no
claims, no census statistics — the census is sealed as a discovery set
and this case predates its window anyway. The value is anatomy: what
the night-before panel could honestly say, and what the tape did.

## The night before (causal state at 2021-02-07 close, strictly earlier data only)

| metric | value | reading |
|---|---|---|
| close | 38,795.69 | — |
| comp_days | **0** | NO coil |
| rvol_pct | **85.8** | volatility at the 86th percentile — loud, not quiet |
| range_pos (1y) | **0.94** | 94% up its one-year range — near highs |
| stretch_z | **+1.59** | stretched ABOVE its 100-day mean |
| ret30 | −4.4% | flat month |
| vol_ratio | 0.99 | normal volume |

**The honest night-before verdict: BTC was NOT primed.** No
compression, high volatility, near range highs, stretched. The primed
coil score would not have flagged this asset on this night. The Tesla
day belongs to the MISSES family — 32% of the census's missed crypto
moves were quiet-not-coiled, and this one is the opposite again:
loud-not-coiled, near-highs. A move can arrive because someone feeds
the lion; the grievance story is not the only story.

## The day (BTCUSD_PERP coin-margined aggTrades, 508,984 prints)

Daily: open 38,795.69 → high 46,794.45 → close 46,374.87, **+19.5%**.
The intraday anatomy, hourly:

- **Hours 00–11 UTC: ordinary churn.** 7–11k trades/hour, returns
  ±1.3%, taker buy-share 0.43–0.58. Nothing on the tape.
- **Hour 12 (13:00–14:00 UTC): the event.** The Tesla 8-K filing hit
  ~13:30 UTC. Trades explode to **54,592 — 6× the prior average** —
  volume 9.3M contracts, and the hour prints **+10.2%**.
- **Hour 13: peak churn, no follow-through.** 86,849 trades (the day's
  maximum), price −0.9% — the market arguing over the new level.
- **Afternoon: elevated activity, slow drift** (20–43k trades/hour),
  closing hours push +3.8% into the close.

## The microstructure observation that matters for the L2 phase

During the +10.2% explosion hour, the taker **buy-share was 0.54** —
barely above balance. A one-directional +10% hour printed with near-
symmetric aggressor flow. The taker imbalance was mild; the price
impact per unit of imbalance was enormous. On taker data alone this is
an observation, not a mechanism — but it is exactly the signature
that **passive liquidity withdrawal** (asks pulled, not buys pushed)
would print, and passive withdrawal is precisely what full-depth L2
measures and taker data cannot see. This is the C5/C6 motivation in
one hour of tape: **the book did the work; the trades only kept the
score.** When the L2 data passes the gate, this hour is a named
candidate for the absorption-asymmetry anatomy — not a test, an
anatomy.

## What this case cannot tell you

That information shocks are predictable, that near-high + high-vol
states precede moves, or that anything generalizes from one day. The
night-before panel said "not primed" and the move came anyway — the
correct lesson is humility about WHAT the priming rule misses, not a
new rule invented from one event. The misses curriculum exists for
that lesson at scale.
