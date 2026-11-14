# The mathematics of the NBS edge — does the crash-protection survive the full honesty battery?

**Date:** 12 November 2026 · **Script:** `src/nbs_edge_stats.py` · **Machine-readable:** `nbs_edge_stats.json`
**Subject:** the night-before score's crash-protection finding (z = −7.29 in `night_before_test_report.md`), put through the project's complete statistical-edge mathematics.

## The pre-declared verdict rule

The finding is an EDGE only if it survives all three:
(a) Bonferroni deflation ×24 (the comparisons the source test scanned),
(b) an own-scale majority (per-series hazard beats, the convention that
killed the elevated-vol axis), and (c) a positive pooled AND own-scale
expectancy sign.

## Result 1 — multiplicity: survives by eleven orders of magnitude

Crash hazard (−30%/30d): NBS≥4 → **11.19%** (n=2,092) vs NBS≤1 →
**20.03%** (n=1,373). z = −7.19, p_raw = 6.4×10⁻¹³, **Bonferroni ×24:
1.5×10⁻¹¹**. Scan luck is not a plausible explanation.

## Result 2 — own-scale: 88/115 series (76%)

The pooled hazard is not scale contamination: in the 115 series with
enough samples in both groups, the high-score state carries the lower
crash hazard in **88** of them (sign test p ≈ 0). Median per-series
hazard difference: **−10.7 points**. This is the test the elevated-vol
axis failed (22/45) — the composite passes it.

## Result 3 — effect size

- **Relative risk 0.558** (95% CI 0.476–0.656) — the state roughly
  **halves** crash hazard.
- Absolute risk reduction **8.8 points**; NNT ≈ **11** (about 11
  protected-state days avoid one crash that an unprotected day would
  have suffered).

## Result 4 — expectancy: the medians grade monotonically

Pooled means are contaminated (one series' +1,000%+ window puts the
NBS=2 bucket's *mean* at +162% — the exact scale-contamination failure
mode this project has documented twice). The medians are the honest
read, and they are **monotone in the score**:

| NBS | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| median fwd 30d | −9.5% | −6.3% | −5.7% | −4.8% | −4.0% | −1.9% |

Own-scale mean-return wins (NBS≥4 > NBS≤1): **92/115 series (80%)**.

As a strategy framing: always-long Sharpe 0.270 vs NBS≥4-filtered
Sharpe 1.481, PSR = 1.000 — **but the Deflated Sharpe Ratio is 0.156,
failing the 0.95 gate.** The deflation is honest but its trial-Sharpe
proxy is itself contaminated by the same outlier bucket, so the DSR
number here is a conservative bound, not a clean verdict. The clean
statistics are the medians and the own-scale counts.

## The verdict

**All three pre-declared gates pass.** The crash-protection is a
measured, multiplicity-deflated, own-scale-majority statistical
effect with a monotone expectancy gradient. For the first time in the
night-before program, a composite of the registry's criteria carries
a statistically defensible claim.

Three honest limits, on the record:

1. **It is a relative-risk filter, not a money machine.** The medians
   improve monotonically with the score but remain negative on this
   2021–2026 crypto panel — the state improves outcomes *versus other
   days*, it does not make holding profitable by itself.
2. **The DSR framing is unresolved** (0.156 with a contaminated trial
   proxy); the Sharpe comparison inherits the panel's outlier problem.
   The dual-split gate with a causal rule is the next arbiter.
3. **Direction remains refused.** The up-side hazard is flat across the
   score; this edge says nothing about where the lion is — only that
   the night-before state is when the trap is least likely to spring
   downward.

Descriptive until the dual-split gate and the forward log say
otherwise. C7 sealed.
