# equity-factor-zoo (Month 2: factor library + evaluation instruments)

Price-based cross-sectional factors and the machinery to evaluate them,
built on top of the Month-1 point-in-time pipeline. **Descriptive
infrastructure only — no factor has been evaluated on real data and no
claim is made or implied by anything here.** The instruments are validated
on engineered synthetic ground truth (a "momentum world" and a "null
world"), which tests the measuring devices, not the market.

## The price wing (implemented)

| Factor | Definition | Intuition (declared, unmeasured) |
|---|---|---|
| `momentum` | Total return from t-252 to t-21 (skip-month) | Underreaction / delayed incorporation of news |
| `reversal` | Negative of the past 21-day total return | Liquidity-provision premium, overreaction |
| `volatility` | Trailing 63-day std of daily total returns | Low-vol anomaly (lottery demand) |
| `range_position` | Position of the TR index in its trailing 252-day range, 0..1 | 52-week-high anchoring |
| `amihud` | Mean of \|daily return\| / dollar volume over 21 days | Illiquidity premium |
| `dollar_volume` | Trailing 21-day mean dollar volume | Size/liquidity proxy |

All factors: long format `(sid, date, factor, value)`; the value at date t
uses only information available at the close of t; computed on the
total-return series except the liquidity pair, which correctly uses
unadjusted dollar volume. Factors are returned RAW (no cross-sectional
standardization) — normalization happens once, at evaluation time, under a
declared convention.

## The fundamental wing (deliberately absent)

Value, quality, and profitability factors need point-in-time fundamentals.
They stay blocked until a source passes the
`docs/equity_alpha_lab/data_source_evaluation.md` gate. Writing them
against a survivorship-biased or period-end-keyed source would bake the
sins the whole pipeline exists to prevent into the factor zoo itself.

## Evaluation instruments (`evaluation.py`)

- `ic_series`: per-date Spearman rank IC between factor and forward return.
- `ic_summary`: mean IC, std, naive t-stat, ICIR, hit rate, min names per
  date.
- `quantile_returns`: per-date mean forward return per equal-sized bucket
  (top bucket = highest factor value), plus top-minus-bottom `spread`.
- `top_bucket_turnover`: per-date fraction of top-bucket membership changed.

## Validation (`tests/test_equity_factor_zoo.py`)

- MOMENTUM WORLD: engineered persistent cross-sectional drift ordering —
  momentum IC must be positive, reversal IC negative, quantile means
  broadly monotone, top-bucket turnover < 0.5.
- NULL WORLD: iid returns — IC near zero, naive |t| < 2.5 (the instrument
  must not manufacture signal out of noise).
- Direct hand-computation checks for momentum and reversal; lag discipline
  (no factor value before its window is complete); range_position bounds;
  empty-intersection handling.

## Frozen conventions

- IC horizon: the forward-return horizon passed by the caller (5-day
  default in tests); the production horizon is a spec decision, not a
  tuning knob.
- Quantiles: per-date rank, equal-sized buckets, largest value = top.
- Turnover: changed-membership fraction of the top bucket.

## Limitations (stated before any real-data use)

- The IC t-stat is NAIVE (i.i.d. across dates). Serial dependence in IC,
  cross-sectional dependence, Newey-West/Fama-MacBeth inference, and
  multiple-testing control across the zoo are Month-2 follow-ups and MUST
  precede any claim about a factor.
- Sector/size exposure decomposition is not implemented yet.
- `quantile_returns` uses equal-weighted means; no cost or tradability
  overlay (that is Month 3's job, not the evaluator's).
- All factor windows are defaults, not tuned values; any departure from
  the defaults must be declared as a specification choice.
