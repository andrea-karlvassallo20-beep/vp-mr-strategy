# The AVFI fade-layer dossier — the owner's H8 tops/bottoms
# construction (AVFI v3.2), encoded and measured on the archive

Status: MEASURED DESCRIPTIVE work, owner-authorized 2026-11-18
(fourth measured session of the parallel regime). The owner
supplied the AVFI v3.2 research indicator (registered draft H8
amendment: fresh 20-bar extreme + flow-fade gate at the median)
and asked for help mining it. The H8 construction was encoded
before the run (protocol in `src/avfi_fade_layer_dossier.py`):
fresh 20-bar closing low/high at the evaluation night, flow axis
= the session-40 declared VFI z as the STAND-IN for the AVFI
spread robust z (the archive has no AVFI series; substitution
DECLARED and dated; a different grain is a different
construction — this run is DAILY, the v3.2 native grain is
weekly NQ). Descriptive on the discovery archive; W2 confirmation
mandatory; no threshold chosen; nothing armed; nothing trades
live.

## 1. The cells (all nights baseline: 57.6% first-move-up,
## 4.97% move-within-5d)

| H8 cell (daily re-instantiation) | P(first big move UP) | P(move ≤5d) | n |
|---|---|---|---|
| fresh 20d LOW alone | 0.596 | **0.081** | 17,660 |
| fresh 20d HIGH alone | 0.610 | **0.090** | 13,230 |
| **bottom fade** (fresh low + flow z ≥ 0) | 0.588 | 0.058 | 11,870 |
| **top fade** (fresh high + flow z ≤ 0) | **0.481** | 0.038 | 1,673 |
| flow sign alone at lows (same as bottom fade) | 0.588 | 0.058 | 11,870 |
| all nights | 0.576 | 0.050 | 129,017 |

## 2. The mining verdict, honestly

1. **The price-extreme triggers are doing the real work.** A fresh
   20-day LOW concentrates arrival (8.1% within 5 days, 1.6x
   baseline) and a fresh 20-day HIGH even more so (9.0%, 1.8x —
   being present at a continuing move, the trend chip). Both
   carry the panel-standard up chip (~0.60).
2. **The H8 median flow gate SUBTRACTS at this grain with this
   proxy.** Bottom-fade dilutes the fresh-low chip (0.588 vs
   0.596) and halves its arrival concentration (0.058 vs 0.081):
   "flow holding up at a low" is the COMMON case (2/3 of fresh
   lows), so the gate mostly removes the sharper tail rather than
   isolating anything.
3. **The owner's TOP FADE is the most informative cell — and it is
   an EXIT marker, not an entry.** Fresh high + flow fading reads
   48.1% first-move-up, BELOW the 57.6% baseline, with arrival
   collapsing to 3.8%: the v3.2 divTop is measurably an
   exhaustion state. Complementary to longs, not a long signal.
4. **The measured better flow read is the flow EXTREMITY, not the
   flow SIGN** (session 40): the chip lives at the bottom DECILE of
   cumulative flow (0.686), gate on the extremity, not on z ≥ 0.
   The suggested v3.2 amendment for the weekly chart, to be
   pre-registered before any evaluation: swap the divBot gate from
   "flow z >= -fadeZ" to "flow z in the bottom decile of its
   trailing distribution" and keep the fresh-low trigger as is.
5. **The presence philosophy, quantified:** the best measured
   instrument skeleton remains session 40's composition (quiet +
   base + flow low extremity, 9.4% five-day arrival, 60-65% lean)
   now PLUS this session's finding that fresh price extremes are
   themselves strong arrival states and that fresh-high-with-flow-
   fade marks the other end. Nothing here is a played threshold:
   W2 confirmation on the weekly grain and fresh windows is
   mandatory before the H8 layer counts as evidence.

## 3. What this does not license

Descriptive discovery-panel numbers on the DAILY re-instantiation
of a WEEKLY-registered rule (grain difference declared); the VFI-z
stand-in for the AVFI spread z is a proxy substitution — the
weekly AVFI re-instantiation on NQ is a named follow-up; no
threshold armed, no kill line moved, nothing trades live.

## 4. Reproduction

`python3 src/avfi_fade_layer_dossier.py` →
`avfi_fade_layer_dossier.csv` (this document:
`avfi_fade_layer_dossier.md`).
