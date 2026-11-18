# Robust-sigma amendment comparison - what the library taught

Filimonov-Sornette (session 48): moment-based scale estimators
are outlier-fragile on fat-tailed returns; robust median/quartile
scale is the remedy (their pp. 8, 34) - the same lesson as the
owner's AVFI v3.2 robust-z IQR layer. Registered moment sigma
vs candidate robust MAD sigma (1.4826 x median absolute
deviation, trailing 20d, prior-night). sigma>0 guard on both.
Construction COMPARISON only; the amendment is QUEUED PENDING
OWNER RATIFICATION; nothing swapped; nothing armed; nothing
trades live.

| scale | block | n | value |
|---|---|---|---|
| moment_std_registered | all_h1 | 69336 | 0.56 |
| moment_std_registered | all_h2 | 58891 | 0.5896 |
| moment_std_registered | nuke_down_h1 | 575 | 0.5252 |
| moment_std_registered | nuke_down_h2 | 417 | 0.6235 |
| moment_std_registered | nuke_up_h1 | 785 | 0.628 |
| moment_std_registered | nuke_up_h2 | 612 | 0.6732 |
| moment_std_registered | move_density_nextday_h1 | 148575 | 0.0103 |
| moment_std_registered | move_density_nextday_h2 | 131687 | 0.0097 |
| moment_std_registered | A2_all_win_rate | 404 | 0.5965 |
| moment_std_registered | A2_all_mean | 404 | 0.0984 |
| moment_std_registered | A2_h1_win_rate | 306 | 0.634 |
| moment_std_registered | A2_h1_mean | 306 | 0.1077 |
| moment_std_registered | A2_h2_win_rate | 98 | 0.4796 |
| moment_std_registered | A2_h2_mean | 98 | 0.0695 |
| robust_mad_candidate | all_h1 | 94927 | 0.5379 |
| robust_mad_candidate | all_h2 | 81814 | 0.5528 |
| robust_mad_candidate | nuke_down_h1 | 2037 | 0.5351 |
| robust_mad_candidate | nuke_down_h2 | 1678 | 0.5584 |
| robust_mad_candidate | nuke_up_h1 | 2596 | 0.6029 |
| robust_mad_candidate | nuke_up_h2 | 2183 | 0.6303 |
| robust_mad_candidate | move_density_nextday_h1 | 148575 | 0.0231 |
| robust_mad_candidate | move_density_nextday_h2 | 131687 | 0.0223 |
| robust_mad_candidate | A2_all_win_rate | 434 | 0.6106 |
| robust_mad_candidate | A2_all_mean | 434 | 0.0911 |
| robust_mad_candidate | A2_h1_win_rate | 318 | 0.6384 |
| robust_mad_candidate | A2_h1_mean | 318 | 0.1016 |
| robust_mad_candidate | A2_h2_win_rate | 116 | 0.5345 |
| robust_mad_candidate | A2_h2_mean | 116 | 0.0625 |

## THE HONEST READING

1. **The two edge candidates SURVIVE the scale change** (the point of
   the run): the A2 washout bottom (moment: win 59.7% / mean +9.8%;
   robust: win 61.1% / mean +9.1%; positive in both halves under BOTH
   scales: h1 +10.8%/+10.2%, h2 +7.0%/+6.3%) and the nuke_up chip
   (moment 0.628/0.673 vs baseline 0.560/0.590; robust 0.603/0.630 vs
   baseline 0.538/0.553 - above baseline in both halves under BOTH
   scales). The nuke_down chip shows no edge under either scale
   (confirming session 49's deflation).
2. **The robust scale materially changes the EVENT SET, not the
   edges**: the next-day >=4-sigma move density roughly doubles
   (1.03%/0.97% -> 2.31%/2.23%) because MAD on fat-tailed returns is
   smaller than the stdev - the candidate construction finds TWICE as
   many "big moves", which makes its 4-sigma threshold effectively
   easier. This is why the amendment is QUEUED PENDING OWNER
   RATIFICATION, not swapped: the registered moment sigma stays the
   construction of record until the owner's word, and if ratified the
   robust scale re-registers every dependent threshold (the archive
   dossiers' labels included).
3. **What the library taught the formula, ported so far** (the ledger
   the owner asked for): Poisson-reshuffling placebo (session 44) ->
   the label-placebo battery; seasonality-does-not-touch-structure
   splits -> the calendar discipline; near-criticality construction
   conditionality (sessions 48/36) -> the estimator-mode rule; the
   Fedenko VFI form -> the session-40 flow axis; the owner's own AVFI
   H8/H9 draft -> the session-42 fade layer; and now the outlier
   fragility of moment scales (session 48 PDF pp. 8, 34) -> THIS
   queued robust-scale amendment, matching the owner's AVFI v3.2
   robust-z IQR layer they already installed on their own side.

Nothing swapped; nothing armed; nothing trades live.
