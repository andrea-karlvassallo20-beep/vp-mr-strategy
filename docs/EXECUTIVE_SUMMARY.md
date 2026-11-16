# Executive Summary — the Salient falsification programme

**Final conclusion, owner-confirmed 2026-11-16:**

> **All OHLCV-derived edges are dead. The program now rests entirely
> on the L2 order book data.**

## What died, and how it died

| claim | resolution | kill line that fired |
|---|---|---|
| C1 — compression duration-dependence, daily bars | **tested-fail** | vol-tautology: after conditioning on realized vol, the compression flag's HR CI included 1.0 in 4/4 cells; block-temporal placebo reproduced the entire effect |
| C7-30m — compression priming, 30-minute bars, 78 perps, 6 years | **tested-fail** | vol-tautology: Primed − Quiet-Not-Primed = +0.00211, 95% CI [−0.01059, +0.01454] includes zero; 16,402 eras, 50.4% positive — a coin flip |
| T3 — wall-clock exposure invariance, taker data | **tested-fail** | trade-arrival density survived hour-of-day stratification (HR 0.9998, p = 4.7e-42) — the effect is vol-mediated |
| The watchlist (KAVA, HOLO, GENIUS, SOL) | **observational, window open** | all four primed coils broke downward; direction unclaimed |

The three independent deaths (daily, watchlist, 30m/16k eras) prove the
same mechanism: **OHLCV-derived compression is volatility wearing a
costume.** "Priming" as measured from bars adds nothing beyond
quietness — not timing, not cross-sectional rank, not 4-hour edge.
The C1 death was not a resolution artifact; it reproduced at every
resolution tested.

## What remains untested (and therefore alive, only behind the gate)

- **C1-L2** — compression measured from the BOOK (resting liquidity
  aging), five armed kill lines, blocked on the L0 snapshot-coverage
  decision
- **C5** — 4D Hawkes passive absorption asymmetry (the Tesla-day
  anatomy's buy-share 0.54 in a +10% hour is the motivating
  observation), blocked on verified full-depth L2
- **C6** — multi-depth CKS OFI + Kyle's λ depletion gradient, blocked
  on verified full-depth L2
- **C7-panel** — cross-pair generalization, sealed, gated behind
  BTCUSDT surviving first

## The standing constraints

- The **0.505 direction boundary [0.497, 0.513] is unbroken** — no
  tested mechanism beats a coin on direction. The endpoint is a WHEN
  instrument, sized by the posterior on MOVE, not UP.
- The discovery panel (census, misses profile) is **sealed**; the
  second-generation rule is pre-registered and frozen until a forward
  window that does not yet exists.
- The 30m panel's TEST eras (2025-08 → 2026-06) are **untouched**.
- The L0 gate: 2026-10-01 **PASSED**; 10-02..04 sequence-verified with
  the snapshot audit pending the paid-data decision.

## The one sentence

Three resolutions, one verdict: the coil is not in the candles — if
the WHEN clock exists at all, it lives in the order book, and the
program rests entirely on the L2 data passing the gate.
