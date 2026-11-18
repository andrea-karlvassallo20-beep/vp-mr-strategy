# Library deep-read session 8 — Bechler & Ludkovski, "Optimal
# Execution with Dynamic Order Flow Imbalance" (arXiv:1409.2618v2,
# 2014; UCSB; stochastic-control execution model, NASDAQ ITCH
# calibration)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/pdfs/`, extracted page-marked text in
`docs/library/text/xc42ba9_optimal_execution_with_dynamic_order_flow_imbalanc.txt`).
Next by triage rank (session 8's pointer): the execution model
whose state variable is the SAME flow imbalance C8's queued VPIN
clock would measure — and whose headline structural move
(endogenous horizon) lands exactly on W1's deferred H.

## The paper in one paragraph

The liquidation trader carries inventory x and the market carries a
signed order-flow imbalance Y, modeled as mean-zero Ornstein-
Uhlenbeck (dY = -beta*Y dt - phi(alpha_t) dt + sigma dW, PDF p. 4);
the trader's own selling drags Y down (phi = eta*alpha, the
informational footprint, PDF pp. 3-4), and total cost is quadratic
instantaneous impact plus kappa*Y^2 (adverse-selection cost of
trading in an unbalanced market, per the VPIN/market-toxicity
theory of Easley-Lopez de Prado-O'Hara, PDF p. 4) plus inventory
risk lambda(x) — over an ENDGENOUS horizon T0 = the first time the
inventory reaches zero (PDF p. 3). Fixed-horizon myopic strategies
(VWAP/TWAP, Almgren-Chriss hyperbolic, quadratic) solve in closed
form (Lemma 2, PDF pp. 9-10); the dynamic feedback strategy solves
a Riccati system (Prop. 2, PDF pp. 13-14); optimizing over the
horizon T* and then rolling it forward (receding-horizon control)
is the recommended implementation (PDF pp. 15-16). Simulations
(Table 1, PDF p. 18): the fully dynamic strategy beats static VWAP
by ~6.8%, and — their own emphasis — the gains from ADAPTING THE
HORIZON dominate the gains from modeling leakage dynamically.
The realized horizon T0 is longest in balanced markets and
shortest when selling into a sell-dominated book, an asymmetry
created by the optimal response even though the cost kappa*Y^2 is
symmetric (PDF pp. 19-20). Calibration: an EWMA volume-time flow
imbalance I_k in [-1,1] with memory scale beta = a/V_daily, the
cited intra-day mesoscopic range a in [10, 100] (PDF p. 23, eq.
30); VPIN is the moving average of |bucket imbalance| over n
buckets (PDF p. 25, eq. 32), i.e. E|I|-type toxicity, the ELO
(2013) linkage.

## Findings, graded (does any kill line move?)

**NO kill line changes.** All five C1-L2 lines and C8's eleven
stand; the A4 conditional pre-commitments stay frozen as written.
One candidate sharpening queued, three reinforcing notes recorded:

1. **[candidate sharpening, PENDING OWNER RATIFICATION] The
   flow-clock scale-constant rule.** Any future flow-state
   estimator (VPIN trigger, EWMA imbalance, or successor) hides a
   memory-scale hyperparameter — and this paper supplies the
   sourced constraint the program lacks: beta = a/V_daily with
   a in [10, 100] (PDF p. 23), V_daily = average daily volume.
   Pre-declaration text: the memory scale of any flow clock is
   declared BEFORE data as a fraction of daily volume, with the
   cited library range as the only legal prior; it is NOT a free
   parameter to be tuned after seeing the gated windows (the same
   anti-freedom discipline as the queued boundary-solution and
   per-branch CI rules).

2. **[reinforcing, no new item] W1's deferred horizon H is the
   literature's endogenous control, worked.** Their realized
   execution horizon T0 varies by up to ~50% of the static optimum
   with the state (x, Y) (PDF pp. 19-20, Figs. 6-7), and the
   adaptive-horizon gains dominate the model-form gains (Table 1,
   PDF p. 18). This is the citable worked example that freezing a
   single horizon constant would pre-register a GUESS of a variable
   the field treats as a control: the deferral already made in the
   W1 spec ("H deferred so no guess smuggles in") is not merely
   cautious, it is the only choice consistent with the literature.
   Nothing is armed; H stays deferred until the owner's word.

3. **[reinforcing, no new item] The flow state from executed trades
   alone is a narrow slice.** Market orders are less than 5% of
   total order flow in the 2010s LOB (Remark 5, PDF p. 24; their
   Table 2: tens of thousands of executed trades against hundreds
   of thousands of LOB messages). This matches the C5 queue-reactive
   sharpening from the library ritual's paper 4 (the passive side
   carries the mechanism) and warns the C8 clock builders: a
   toxicity reading computed only from prints measures the taker
   tip of the flow, not the flow.

4. **[reinforcing, no new item] The wash-trading confound, in
   control form.** The trader's program enters the flow state as a
   DRIFT (phi(alpha) in eq. 3, PDF p. 4) — the model's own statement
   that a participant's activity moves Y, which is exactly what a
   wash trader does to any flow-state feature computed over a
   contaminated window (session 6's evidence that wash accounts
   for roughly a third of one exchange's volume). The queued gate
   audit's "contaminated windows are missing, not zero" language
   gains its control-theory citation: the estimator is measuring
   the manipulator's drift, not the market's state.

## What this paper would have killed if we had done it wrong

If the W1 spec had fixed the horizon constant at pre-registration
(because "something must be declared"), this paper is the
counterexample that would have surfaced at review: the horizon's
optimum MOVES with the state (T* longest at balanced flow, shortest
in adverse flow), so the frozen constant would have been a
pre-registered wrong — kill line K3's calibration machinery could
not have repaired a structural constant. The deferral was the
correct discipline. Separately, had anyone computed a flow state
from executed trades alone and read it as "the market's flow,"
Remark 5's <5% fact would have made it a confident reading of a
narrow tip. Grade: **no kill line changed; one candidate sharpening
queued (the flow-clock scale-constant rule), zero armed** — the
owner's word remains the only trigger.

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The control model is calibrated only in its flow METRIC —
the authors state the exact relation between the EWMA imbalance and
the OU state Y "remains open" (PDF p. 24), so the SDE's parameters
are illustrative, not fitted; the OU choice is their own named
compromise (PDF p. 6); the cost term kappa*Y^2 is symmetric by
tractability while the trader's private leakage is one-sided (PDF p. 4);
and the program NEVER trades live, so the execution-cost content
is ammunition for cost-survival amendments (K7-style) only, never
a strategy candidate. arXiv v2 (2014); a later journal version
exists in the literature — check before formal citation.
