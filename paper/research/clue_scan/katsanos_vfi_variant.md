# K-VFI: Katsanos original (moment scale) vs the program
variant (robust MAD scale, prior-bar, z->percentile states,
sigma>0 guards) - head to head on the program's own criteria.
Registered constants; nothing tuned; in-sample descriptive;
nothing armed; nothing trades live.

| scale | block | n | value |
|---|---|---|---|
| katsanos_original_moment | A2_mean_ret | 153 | -0.0791 |
| katsanos_original_moment | A2_mean_win | 153 | 0.3137 |
| katsanos_original_moment | A2_h1_mean_ret | 142 | -0.0882 |
| katsanos_original_moment | A2_h1_mean_win | 142 | 0.2958 |
| katsanos_original_moment | A2_h2_mean_ret | 11 | 0.0377 |
| katsanos_original_moment | A2_h2_mean_win | 11 | 0.5455 |
| katsanos_original_moment | P_first_up[fresh_low_h1] | 8693 | 0.5433 |
| katsanos_original_moment | P_first_up[flow_ext_low_h2] | 3085 | 0.5572 |
| katsanos_original_moment | P_first_up[fresh_low_h2] | 8219 | 0.6138 |
| katsanos_original_moment | P_first_up[washout_h2] | 666 | 0.515 |
| program_variant_mad | A2_mean_ret | 155 | -0.0613 |
| program_variant_mad | A2_mean_win | 155 | 0.3419 |
| program_variant_mad | A2_h1_mean_ret | 144 | -0.0816 |
| program_variant_mad | A2_h1_mean_win | 144 | 0.3125 |
| program_variant_mad | A2_h2_mean_ret | 11 | 0.2039 |
| program_variant_mad | A2_h2_mean_win | 11 | 0.7273 |
| program_variant_mad | P_first_up[fresh_low_h1] | 8693 | 0.5433 |
| program_variant_mad | P_first_up[flow_ext_low_h2] | 3093 | 0.5435 |
| program_variant_mad | P_first_up[fresh_low_h2] | 8219 | 0.6138 |
| program_variant_mad | P_first_up[washout_h2] | 708 | 0.5099 |
| andrea_gate_hybrid | A2_mean_ret | 171 | 0.0761 |
| andrea_gate_hybrid | A2_mean_win | 171 | 0.4737 |
| andrea_gate_hybrid | A2_h1_mean_ret | 145 | 0.0627 |
| andrea_gate_hybrid | A2_h1_mean_win | 145 | 0.4552 |
| andrea_gate_hybrid | A2_h2_mean_ret | 26 | 0.1504 |
| andrea_gate_hybrid | A2_h2_mean_win | 26 | 0.5769 |
| andrea_gate_hybrid | P_first_up[fresh_low_h1] | 8693 | 0.5433 |
| andrea_gate_hybrid | P_first_up[flow_ext_low_h2] | 3538 | 0.662 |
| andrea_gate_hybrid | P_first_up[fresh_low_h2] | 8219 | 0.6138 |
| andrea_gate_hybrid | P_first_up[washout_h2] | 632 | 0.5997 |

## ADDENDUM (same session block): the Andrea-gate hybrid

Owner directive (immediately after): "what about taking midpoint
close prior relative price like the 'Andrea' formula" - the Andrea
VPVI script's sign is PRIOR-CLOSE-RELATIVE (volume weighed by whether
the bar acted above or below the PREVIOUS close:
|high-prevClose| vs |prevClose-low| over the zone), not
close-to-close. Built as a third arm: the session-40 bounded-ratio
flow pipeline with ONLY the sign gate swapped to the Andrea form
(v_ratio x w, cumsum, same z(252)->pct(756) states) - the comparison
isolates the sign gate.

| flow construction | A2 n | win rate | mean | h1 / h2 mean |
|---|---|---|---|---|
| session-40 Fedenko-style flow (of record) | 404 | 59.7% | +9.8% | +10.8% / +7.0% |
| Katsanos original (moment scale) | 153 | 31.4% | -7.9% | -8.8% / +3.8% |
| K-VFI variant (MAD + all library lessons) | 155 | 34.2% | -6.1% | -8.2% / +20.4% |
| **Andrea-gate hybrid (this session)** | 171 | 47.4% | **+7.6%** | **+6.3% / +15.0%** |

Chip cells: Andrea-gate flow_ext_low_h2 = **0.662** (vs Katsanos-flow
0.557/0.544 - no edge) and washout_h2 = 0.5997, both against the
h2 baseline 0.553. (h1 cells empty for the flow states: the known
252+756 burn-in, unchanged.)

**Reading:** the owner's PRIOR-CLOSE-RELATIVE gate carries real signal
at lows on this archive - FAR better than the published original's
close-change gate (the difference between -8% and +8% episode returns
is the sign gate alone), positive in both halves, though the
session-40 flow of record still wins the A2 criterion (+9.8% / 59.7%
vs +7.6% / 47.4%). Recorded as a measured POSITIVE result for the
Andrea lineage; the flow of record does NOT change (the owner's word
would be needed to swap gates, and the session-40 gate is still
ahead). Nothing armed; nothing trades live.
