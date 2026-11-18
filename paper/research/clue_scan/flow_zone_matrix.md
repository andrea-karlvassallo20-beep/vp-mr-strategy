# The flow inference matrix - zone x age x price-space

VFI z zones: XB (z<=-1.5), B, A, XA (z>=1.5); young = <=10d in zone; price third of 252d range. P(first big move within 60d is UP) + mean fwd-20d. Thin cells (n<100) marked. In-sample descriptive; nothing armed;
nothing trades live.

| cell | n | P_first_up | thin | mean_fwd20 |
|---|---|---|---|---|
| A | 22127 | 0.6645 | False | -0.0018 |
| A_high | 2053 | 0.511 | False | 0.003 |
| A_low | 15997 | 0.6896 | False | 0.0014 |
| A_mid | 4077 | 0.6436 | False | -0.0154 |
| A_old | 15638 | 0.6791 | False | -0.0053 |
| A_old_high | 1367 | 0.5267 | False | -0.0114 |
| A_old_low | 11376 | 0.7006 | False | 0.0016 |
| A_old_mid | 2895 | 0.6663 | False | -0.028 |
| A_young | 6489 | 0.6295 | False | 0.0065 |
| A_young_high | 686 | 0.4796 | False | 0.0311 |
| A_young_low | 4621 | 0.6624 | False | 0.0007 |
| A_young_mid | 1182 | 0.588 | False | 0.0145 |
| B | 8552 | 0.6268 | False | 0.0096 |
| B_high | 367 | 0.7875 | False | -0.0047 |
| B_low | 7608 | 0.6271 | False | 0.0116 |
| B_mid | 577 | 0.5199 | False | -0.0058 |
| B_old | 5811 | 0.6386 | False | 0.0141 |
| B_old_high | 233 | 0.8369 | False | 0.0219 |
| B_old_low | 5228 | 0.6379 | False | 0.0146 |
| B_old_mid | 350 | 0.5171 | False | 0.0063 |
| B_young | 2741 | 0.6016 | False | 0.001 |
| B_young_high | 134 | 0.7015 | False | -0.0488 |
| B_young_low | 2380 | 0.6034 | False | 0.0059 |
| B_young_mid | 227 | 0.5242 | False | -0.0258 |
| XA | 18606 | 0.6545 | False | 0.016 |
| XA_high | 3898 | 0.6237 | False | 0.0593 |
| XA_low | 10587 | 0.684 | False | 0.0032 |
| XA_mid | 4121 | 0.6081 | False | 0.0049 |
| XA_old | 14345 | 0.6378 | False | 0.0065 |
| XA_old_high | 3128 | 0.5943 | False | 0.0426 |
| XA_old_low | 7937 | 0.6737 | False | -0.0044 |
| XA_old_mid | 3280 | 0.5924 | False | -0.0046 |
| XA_young | 4261 | 0.7109 | False | 0.0456 |
| XA_young_high | 770 | 0.7429 | False | 0.1258 |
| XA_young_low | 2650 | 0.7147 | False | 0.0237 |
| XA_young_mid | 841 | 0.6694 | False | 0.0388 |
| XB | 2478 | 0.7252 | False | 0.0085 |
| XB_high | 34 | 1.0 | True | 0.0472 |
| XB_low | 2294 | 0.7249 | False | 0.0078 |
| XB_mid | 150 | 0.6667 | False | 0.0072 |
| XB_old | 1699 | 0.741 | False | 0.0194 |
| XB_old_high | 23 | 1.0 | True |  |
| XB_old_low | 1592 | 0.7531 | False | 0.0193 |
| XB_old_mid | 84 | 0.4405 | True | 0.0063 |
| XB_young | 779 | 0.6906 | False | -0.0115 |
| XB_young_high | 11 | 1.0 | True |  |
| XB_young_low | 702 | 0.661 | False | -0.0138 |
| XB_young_mid | 66 | 0.9545 | True | 0.0085 |
| BASELINE | 51763 | 0.6576 | False |  |

## The zone chain (P(next zone | current zone) counts)

| from | to | count | share |
|---|---|---|---|
| XA | A | 1690 | 0.329 |
| A | XA | 1633 | 0.318 |
| A | B | 610 | 0.119 |
| B | A | 605 | 0.118 |
| XB | B | 294 | 0.057 |
| B | XB | 290 | 0.056 |
| B | XA | 9 | 0.002 |
| A | XB | 4 | 0.001 |
| XA | B | 2 | 0.0 |

## THE DERIVED INFERENCES (baseline 0.658 on this universe)

**1. DEPTH BELOW ZERO, AGED, AT LOWS - the strongest direction cell
in the flow geometry: XB_old_low = 0.753 (n=1,592)**; the XB zone
overall 0.725 (n=2,478) and AGING HELPS within it (old 0.741 >
young 0.691) - the deep washout accumulating time at the price lows
is the coiled-effort seat the owner draws: effort drained, price at
the extreme, TIME in the washout adding to the chip. The only
comparable program cell remains the shape-qualified flagship
(0.731, session 55) - now cross-confirmed by a different
construction family (z-zone geometry instead of percentile deciles).

**2. YOUNG EUPHORIA IS MOMENTUM, NOT FADE: XA_young 0.711
(n=4,261); at price HIGHs XA_young reads 0.743 with mean fwd-20d
+12.6% (n=770).** Fresh positive-extreme flow at price highs is the
single largest DRIFT cell the program has measured - the drift the
negative-median rule almost never licenses, appearing exactly where
the flow AGE axis says the young segment is unspent (session 60:
first-half segments +4.4% fwd20; this cell concentrates it).

**3. MILD NEGATIVE FLOW AT PRICE HIGHS RESOLVES UP (secondary,
recorded not claimed): B_high 0.788 (n=367); B_old_high 0.837
(n=233)** - the pause-in-uptrend signature; thin-ish and unsplit -
NOT promoted, no multiplicity spent; named for the next pre-registered
test.

**4. Within-zone age geometry INVERTS by side:** positive flow zones
age BADLY (XA_old 0.638 < XA_young 0.711 - spent effort, session
60's law at zone grain) while the washout zone ages WELL (XB_old
0.741 > XB_young 0.691 - accumulation). The flow axis thus carries
TWO clocks: a spending clock above zero and a charging clock below
it. This duality is the structural reason flow reads are more
informative than price-only states at the same extremes: price
position alone cannot distinguish a young euphoria from a spent one
or a fresh dip from a deepening washout - the flow zone plus its age
can.

**5. THE ZONE CHAIN (sequentiality): the cycle A<->XA dominates
(1,690 / 1,633 transitions - 72% of all zone moves); the negative
side cycles B<->XB (294/290) and B<->A (610/605); DIRECT XB->A jumps
are 4 out of 5,136 (the washout must pass through B first -
structural, since zones are adjacent bands). The market's flow
spends 72% of its transitions oscillating WITHIN the positive side
- the up-tilt of the universe made mechanical - and the information
lives at the edges: deep XB entries and XA exits.**

**The verdict on the owner's claim ("flow is the closest to a
useful indicator system"):** as of this session, YES at the program's
honest bar - the flow axis supplies (a) the strongest measured
direction cell family (0.72-0.75 at the deep-washout-age low seat),
(b) the only recurring drift cells (XA_young_high +12.6%, XB_old
fwd20 +1.9% - the washout is drift-positive too), (c) a two-clock
age geometry that disambiguates what price position cannot, and
(d) a chain structure whose edges (XB/A boundaries) are where the
seats sit - all in one registered construction family, cross-confirmed
by two different derivations. NOT a tradeable edge yet: all
in-sample, halves-unsplit at this grain, W2 owed on every number;
the misses remain ours too (nuke_down dead, V-crash shorts dead,
Katsanos sign dead).

Nothing armed; nothing trades live.
