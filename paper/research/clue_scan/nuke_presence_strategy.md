# Nuke Presence Long - PAPER STRATEGY v0.1 (draft, owner-directed)

One pre-registered rule, zero variants. Signal: causal nuke_down
night (>=4-sigma down day within 2 days). Entry: next open.
One trade per episode. Take-profit: the first >=4-sigma UP day
(the event the chip measures). Time-stop: 60 trading days.
No stop-loss (the down tail is measured, not insured). Zero
costs, zero slippage, declared. ALL NUMBERS IN-SAMPLE: the chip
was discovered on this same archive; the halves are the only
quasi-independent intra-archive check; W2 fresh-window
confirmation mandatory. Nothing armed; nothing trades live.

Series scanned: 199; episodes: 947.

### ALL (in-sample)

| n | win rate | mean ret | median ret | p5 ret | p25 ret | p75 ret | p95 ret | mean hold days | median hold days | mean mae | p5 mae |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 947 | 0.4372 | -0.0117 | -0.0335 | -0.4256 | -0.1909 | 0.1119 | 0.4781 | 51.1 | 60 | -0.2213 | -0.5749 |


### HALF 1 (earlier, in-sample)

| n | win rate | mean ret | median ret | p5 ret | p25 ret | p75 ret | p95 ret | mean hold days | median hold days | mean mae | p5 mae |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 606 | 0.4703 | 0.0087 | -0.0154 | -0.3987 | -0.1842 | 0.1405 | 0.5388 | 52.6 | 60 | -0.2112 | -0.5388 |


### HALF 2 (later, in-sample)

| n | win rate | mean ret | median ret | p5 ret | p25 ret | p75 ret | p95 ret | mean hold days | median hold days | mean mae | p5 mae |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 341 | 0.3783 | -0.0479 | -0.0573 | -0.4708 | -0.2156 | 0.067 | 0.4136 | 48.4 | 60 | -0.2391 | -0.6469 |


## THE HONEST VERDICT (v0.1: REJECTED as specified)

The paper strategy does NOT convert the direction chip into positive
episode returns, in-sample: 947 episodes, win rate 43.7%, mean -1.17%,
median -3.35%, halves diverging (+0.87% earlier / -4.79% later), MAE
mean -22.1%, p5 -57.5%. The mechanism is now understood: the chip
measures the DIRECTION of the first >=4-sigma move (70-80% up under the
-session-47 construction), but the post-crash sigma is INFLATED, so
take-profit fires early on modest absolute bounces while the 60-day
time-stop accumulates the adverse path (median hold 60 = time-stop
dominated). And under the sigma>0 data-quality guard discovered in this
session, the chip itself deflates (nuke_down to 0.523/0.627 — below
baseline in the earlier half; nuke_up to 0.615/0.689 — modest, still
above baseline in both halves). Lesson internalized end-to-end: a
direction conditional is not a return; a fake 4-sigma-event was hiding
inside flatlined series; entering after crashes without a stop is a
fat-left-tail bet (p5 episode -42.6% on entry-open, MAE p5 -57.5%).
v0.1 is rejected as specified. No variant will be tuned against these
numbers (multiplicity discipline): a v0.2 requires a new dated
amendment with its rules registered BEFORE evaluation. Nothing armed;
nothing trades live.
