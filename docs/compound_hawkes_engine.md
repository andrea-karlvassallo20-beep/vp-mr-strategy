# Compound Hawkes order-flow engine (synthetic)

Owner-ordered engineering build following deep-read session 21 (Jain, Firozye,
Kochems and Treleaven, "Limit Order Book Dynamics and Order Size Modelling
Using Compound Hawkes Process", arXiv:2312.08927v5). This is demonstration
infrastructure, not evidence. Nothing measured with it counts for any
programme claim, no kill line is involved, and it never touches programme
datasets.

## What it is

- `src/ofhawkes.py` - a 12-dimensional compound Hawkes point process driving
  a six-queue top-of-book simulator. Dimensions: limit, cancel and market
  orders at the touch, one tick deep, and inside the spread, on both sides.
  Order sizes are compound marks: geometric body with Dirac masses at 1, 10,
  50, 100, 200 and 500 shares. Intensities carry separable U-shape
  time-of-day factors (13 bins, mean 1 per dimension), spread gating
  (s-1)^0.75 for in-spread dimensions, signed exponential kernels with
  heterogeneous decays, and live inhibition floored at zero intensity.
- `src/ofhawkes_demo.py` - regenerates the synthetic dashboard dataset
  (writes `ofhawkes_demo_data.json` to the working directory; that file is
  gitignored).
- `tests/test_ofhawkes.py` - 20 tests: spread floor invariant, book
  conservation under scripted events, exact-consumption walk, in-spread
  guard, kernel-norm analytic versus numeric, sampler mass and rejects,
  seed reproducibility, Hawkes-versus-Poisson clustering, grid validity.

## Deliberate differences from the paper

Disclosed, not hidden:

1. Exponential kernels instead of the paper's power-law fits. Reason: the
   discrete-time Bernoulli simulator keeps an exact excitation bank this way.
2. Constrained, mechanical book dynamics instead of a fitted LOB: walk-ups on
   queue depletion (including exact consumption), replenishment on widening.
3. A hard hazard guard: peak intensity times dt must stay under the grid
   resolution bound, or the simulator raises rather than producing
   a discretisation artefact.

## The no-silent-capping rule

`stabilize_norm_matrix` either refuses an unstable kernel-norm matrix or
rescales it to a declared target and returns a disclosure record: raw
eigenvalue, scaled eigenvalue, applied factor, action. The demo that produced
the current dashboard ran with raw eigenvalue 0.6349 against a stationary
bound of 0.5261, was rescaled to 0.2630 with a disclosed factor of 0.4143,
and then had excitation amplitudes halved once more for headroom, landing at
a simulated eigenvalue of 0.1315. Every step is inside the emitted metadata.
The programme lesson behind this: fitted parameters pinned at or beyond a
stability cap are a defect to disclose, never a quiet repair.

## Status

Synthetic only. The engine simulates; it does not estimate, test, or claim.
See the deep-read note in `paper/research/library/` for the paper assessment
(2026-11-18). Graded default NO sharpening: the session found no new
trigger-family rule warranted, and none is queued from this build.
