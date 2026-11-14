# The night-before score (NBS) — first causal predictability test

**Date:** 12 November 2026 (run on the TVC crypto panel)
**Script:** `src/night_before_test.py` · **Machine-readable:** `night_before_test.json`
**Registry:** `paper/research/night_before_criteria.md`

## The question and the design

The census counted what movers looked like the night before. It could
not test predictability because it had no denominator — no control days
that shared the state and did not move. This study builds the denominator
and asks one question: **does the night-before state raise the measured
probability of a significant move in the next 30 days, versus all other
days?**

The indicator (pre-declared, the registry's composite decomposed into
additive points): **NBS 0–5**, one point per criterion met on the state
day — range bottom (≤0.25), quiet (vol ≤30th pct), coiled (≥10 days),
volume dry-up (<1), down on the year (<0). State computed by the same
causal function the census used. Sampling: one state day per series per
non-overlapping 30-day window (stride 30), ≥300 bars of history.
**156 crypto series, 6,767 state-day samples.** Outcomes strictly
forward from the state day.

## The results

### The headline: the composite does NOT predict the big up-moves

| NBS | n | up-move ≥+100%/30d | short-up ≥+30%/30d |
|---|---|---|---|
| 0 | 207 | 1.93% | 15.46% |
| 1 | 1,166 | 3.77% | 22.38% |
| 2 | 1,283 | 2.81% | 20.58% |
| 3 | 2,002 | 3.35% | 19.98% |
| 4 | 1,022 | 1.96% | 16.73% |
| 5 | 1,087 | 3.13% | 22.36% |
| **all** | **6,767** | **3.03%** | **20.26%** |

Confirmatory comparison (NBS≥4 vs NBS≤1, up-moves): **2.56% vs 3.50%,
z = −1.60, p = 0.11.** The high-score state is *not* associated with more
big up-moves — if anything, slightly fewer. The hazard is flat across the
score, and it is flat in BOTH time halves.

**What this means:** the census's 72.3%-at-range-bottom and 47.2%-quiet
readings were base rates *among movers* — selection on the future. Given
the denominator the census lacked, the forgotten-and-pinned signature
does not raise the 30-day hazard of a +100% move. The descriptive
concentration did not survive being made causal — the same shape as the
region hypothesis and the mid-vol confluence before it.

### The measured finding: the state PROTECTS against short-term crashes

| NBS | short-down ≤−30%/30d |
|---|---|
| 0 | 22.22% |
| 1 | 19.64% |
| 2 | 11.85% |
| 3 | 13.64% |
| 4 | **9.98%** |
| 5 | 12.14% |
| **all** | **13.80%** |

Confirmatory comparison (NBS≥4 vs NBS≤1): **11.10% vs 20.03%,
z = −7.29, p < 0.001.** Days carrying the quiet/coiled/pinned state have
roughly **half** the hazard of a −30% move within 30 days. The direction
holds in both time halves (h1: 9.05% vs 24.53%; h2: 11.70% vs 15.84%).

This is consistent with volatility persistence (Bouchaud, the stylized
facts): quiet regimes persist, and crashes need elevated vol to happen.
It is a **risk-filter reading, not a move-prediction edge** — the state
tells you what is *unlikely*, not what is coming.

## The honest verdict

1. **The composite signature fails its first causal test as an
   up-move predictor.** Descriptive census concentration, given a
   denominator, is null. The registry's composite row now carries this
   verdict.
2. **The state's measured value is on the downside:** coiled/quiet/pinned
   days have about half the short-term crash hazard. As a risk throttle
   ("it is safe to hold through this state") this is the kind of claim
   that must still pass the dual-split gate with a causal rule and the
   forward log — but it is the first composite reading with a
   significant, time-split-stable statistic behind it.
3. **Multiplicity binds:** 6 buckets × 4 outcomes were scanned; the
   confirmatory comparisons were pre-declared, and the short-down result
   is strong enough (z = −7.3) that scan luck is an unlikely
   explanation — but unlikely is not impossible.
4. Limitations: TVC panel only (156 crypto series, 5y); synthetic volume
   (the vol_ratio criterion inherits it); the census's non-crypto
   classes are untested here.

Descriptive until dual-split gated and forward logged. C7 sealed.
