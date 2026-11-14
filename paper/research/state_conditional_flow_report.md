# State-conditional flow: the composite denominator, built and tested

**Date:** 12 November 2026 · **Script:** `src/state_conditional_flow.py` · **Machine-readable:** `state_conditional_flow.json`

## The mathematics, stated honestly

Dividing flow F by any positive measurable denominator D is a monotone
reparametrization — no new information, and boundedness alone is
cosmetic (a tanh bounds anything). The version that can add
information is a **conditional** denominator: D = E[|F| | NBS], the
effort this state usually produces, so the ratio becomes a
state-relative surprise:

    z_cond = (effort − μ_NBS) / σ_NBS

Estimated causally (trailing expanding window), with shrinkage toward
the pooled estimate for buckets under 50 observations, and squashed
to (−1, 1) by tanh so the measure is bounded by construction, as
directed. 156 series, 193,568 daily samples.

## The pre-declared test

The denominator earns its place only if quintile separation of
forward hazards improves versus the unconditional effort z. Both
time halves recorded in the JSON.

**Crash side (−30%/30d):** z_cond separation **2.0 points** vs
unconditional **3.3 points** — conditioning does NOT improve the
crash separation. The crash reading lives in the effort level, not in
its state-relative surprise.

**Up side (+30%/30d):** z_cond separation **5.2 points** vs
unconditional **4.0 points** — and the conditional version is
**monotone across all five quintiles** (18.6% → 23.9%) where the
unconditional is not. The state-relative surprise sharpens the up
reading: effort high *for a coiled, quiet, forgotten asset* carries
more up-hazard than effort high in general.

## The verdict

The composite denominator is mathematically sound and measurably
useful in one place: it converts raw effort into state-relative
surprise, which grades the up-side hazard monotonically and slightly
better than the raw measure. It does not improve the crash side, and
both separations are modest (5 points on a ~20% base). What it buys
is *interpretation discipline* — "high effort, relative to what this
state produces" — which is exactly the matched-control logic the
program already validated, now embedded in the measure itself.

Next candidates this opens (descriptive until gated): the
tanh-bounded z_cond as a Pine input row; a causal rule on
z_cond-quintile-5 as an up-side hazard flag through the dual-split
gate. Multiplicity binds; C7 sealed.
