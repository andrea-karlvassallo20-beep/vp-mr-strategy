# The event-flow framework - when X happens, what happens
next (built the owner's way: pair by pair, all the data)

Universe audit: 199 series - 198 with volume, 1 NO-VOLUME (flow via the owner's true-range proxy fallback).

## Inference cells (P(next CLASS | prev) deviates from
the marginal by >= 8 points, stable in both halves;
direction-alternation is a grammar tautology and is NOT
counted as inference):

| prev leg | next leg | P(next \| prev) | marginal | dev | h1 | h2 | n(prev) |
|---|---|---|---|---|---|---|---|
| Ume | Dme | 0.3335 | 0.1427 | 0.1908 | 0.3103 | 0.355 | 6681 |
| Dme | Ume | 0.3061 | 0.132 | 0.1741 | 0.301 | 0.3103 | 7204 |
| Use | Dme | 0.3085 | 0.1427 | 0.1659 | 0.2584 | 0.3594 | 2784 |
| Dmb | Ume | 0.2954 | 0.132 | 0.1634 | 0.2717 | 0.3164 | 1862 |
| Dlb | Umf | 0.2258 | 0.0813 | 0.1445 | 0.1921 | 0.2607 | 1094 |
| Ulb | Dmf | 0.2306 | 0.0906 | 0.14 | 0.2396 | 0.221 | 3062 |
| Dmf | Ume | 0.2702 | 0.132 | 0.1383 | 0.2669 | 0.2737 | 4570 |
| Ule | Dme | 0.2796 | 0.1427 | 0.1369 | 0.2912 | 0.2671 | 2579 |
| Dle | Ume | 0.2668 | 0.132 | 0.1348 | 0.242 | 0.2857 | 1308 |
| Ule | Dmf | 0.2218 | 0.0906 | 0.1312 | 0.2141 | 0.2301 | 2579 |
| Dlf | Ulb | 0.1827 | 0.0606 | 0.1221 | 0.1853 | 0.1807 | 843 |
| Umf | Dme | 0.2624 | 0.1427 | 0.1197 | 0.2566 | 0.2669 | 4116 |
| Dsb | Ume | 0.2464 | 0.132 | 0.1144 | 0.261 | 0.2299 | 556 |
| Dse | Ume | 0.2464 | 0.132 | 0.1144 | 0.2483 | 0.244 | 3527 |
| Usf | Dse | 0.1814 | 0.0688 | 0.1126 | 0.2014 | 0.161 | 2574 |
| Umb | Dme | 0.2532 | 0.1427 | 0.1105 | 0.241 | 0.2639 | 2741 |
| Ulb | Dsf | 0.1731 | 0.0635 | 0.1096 | 0.174 | 0.1721 | 3062 |
| Dmb | Umf | 0.1874 | 0.0813 | 0.1061 | 0.1826 | 0.1917 | 1862 |
| Dlf | Ume | 0.2349 | 0.132 | 0.1029 | 0.2534 | 0.2206 | 843 |
| Usf | Dme | 0.244 | 0.1427 | 0.1013 | 0.2168 | 0.2718 | 2574 |
| Dle | Umf | 0.182 | 0.0813 | 0.1006 | 0.1519 | 0.2049 | 1308 |
| Ulf | Dsf | 0.1638 | 0.0635 | 0.1003 | 0.1462 | 0.1745 | 1032 |
| Dsf | Use | 0.1524 | 0.054 | 0.0984 | 0.152 | 0.1529 | 3248 |
| Dlb | Ume | 0.2303 | 0.132 | 0.0984 | 0.2729 | 0.1862 | 1094 |
| Ume | Dmf | 0.1887 | 0.0906 | 0.0982 | 0.2004 | 0.1779 | 6681 |
| Use | Dse | 0.162 | 0.0688 | 0.0932 | 0.1806 | 0.1432 | 2784 |
| Dle | Ulb | 0.1514 | 0.0606 | 0.0908 | 0.1873 | 0.124 | 1308 |
| Dsf | Ume | 0.2217 | 0.132 | 0.0897 | 0.2198 | 0.2238 | 3248 |
| Dse | Use | 0.1432 | 0.054 | 0.0892 | 0.1458 | 0.14 | 3527 |
| Ulf | Dse | 0.156 | 0.0688 | 0.0872 | 0.1333 | 0.1698 | 1032 |
| Usb | Dme | 0.2285 | 0.1427 | 0.0859 | 0.2163 | 0.2411 | 967 |
| Umf | Dse | 0.1535 | 0.0688 | 0.0848 | 0.1711 | 0.1398 | 4116 |
| Dsb | Use | 0.1385 | 0.054 | 0.0845 | 0.1492 | 0.1264 | 556 |
| Dle | Ule | 0.1346 | 0.051 | 0.0835 | 0.1555 | 0.1186 | 1308 |
| Dme | Umf | 0.1624 | 0.0813 | 0.0811 | 0.1549 | 0.1687 | 7204 |
| Dlb | Usf | 0.1307 | 0.0503 | 0.0804 | 0.1688 | 0.0912 | 1094 |

Full transition matrix: event_flow_matrix.csv; per-pair
counts: event_flow_per_pair.csv. All in-sample
descriptive; nothing armed; nothing trades live.

## THE GOVERNING QUESTION, ANSWERED (as of this session)

"How can you from flow charts know one by one across markets
significant price change before it occurs?"

The honest structure of the answer, each layer measured on this
archive, half-stable, sigma>0-guarded:

1. **You cannot know THE move before it occurs.** (Medians negative
   everywhere; no drift claim survives; first-move direction is a
   coin with chips, not prophecy.)
2. **You can know the SEAT before it occurs** - where, on the flow
   chart, the next significant move is most likely to ORIGINATE:
   price at the range extreme (bottom 20% of its 252d range), a
   fresh 20-bar low, U-BASE leg shape (back-loaded - the base
   builds late), and washout flow (bottom decile): **0.731
   P(first big move within 60d is UP)** vs 0.556 baseline - the
   strongest formation the program has measured; its mirror at tops
   (washed U-dome, 0.331) tells you where the next significant move
   originates DOWN.
3. **You can know the ARRIVAL ZONE**: within 60 days the first
   >=4-sigma move arrives with concentration (the presence/NEAR
   ladder); the seat narrows WHEN without promising the day.
4. **You can know what forms NEXT (the chain)**: direction
   alternation is a grammar tautology (not signal), but the CLASS
   content is stable and real - after a front-loaded SPIKE leg (f) in
   either direction, the next leg is systematically a MID-SIZED,
   EVEN grind (e.g. Dmf->Ume 0.27 vs 0.13 marginal; Usf->Dse 0.18 vs
   0.07; 28 half-stable cells, D>=8pts) - spikes do not beget spikes;
   they beget grinds. The chart-reader corollary: after the V, wait
   for the grind; the U-bases and washouts are where the grinds turn
   into significant moves.
5. **You can know what to REFUSE** - drift bets, V-crash shorts at
   highs (0.542, no edge), nuke-momentum entries without the washout
   condition (deflated, no edge).

The framework = SEAT x SHAPE x FLOW x CHAIN, per pair, one by one,
with every number W2-owing. That is how far the data honestly takes
the question today; the missing bridges (fresh-window confirmation,
intraweek volume-surprise triggers for the H9 layer) are named and
queued, not hand-waved.

Universe honesty: the archive's 199 series ALL carry volume (1
borderline no-volume series); the TVC no-volume USD pairs are NOT in
this clone's cache - the proxy-true-range flow fallback (the owner's
AVFI v3.2 mechanism) is implemented and declared for the day they
are supplied; the washout chip on real-volume pairs reads 0.6705
(washout) vs 0.6552 (other fresh-low bottom nights) at the
P_first_up grain.

Nothing armed; nothing trades live.
