# Library deep-read session 2 — Hardiman & Bouchaud, "Branching ratio
# approximation for the self-exciting Hawkes process" (arXiv:1403.5227v3)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: the legally
acquired, page-marked extracted text
(`docs/library/text/x36082b_branching_ratio_approximation_for_the_self_excitin.txt`);
all page cites are to that PDF.

## The paper in one paragraph

Hardiman & Bouchaud introduce a model-independent branching-ratio
estimator — ñ = 1 − √(μ_W/σ²_W) from the mean and variance of event
counts in a window W (Eq. 7, PDF p. 3) — and use it to re-examine
the Filimonov-Sornette reflexivity results. They reproduce the
flash-crash analysis (PDF p. 5) and the 1998-2013 upward trend at
fixed W (PDF p. 6, Fig. 6), but show that when W is rescaled to
track the market's speeding-up interaction timescale (halving
every 18 months), the trend vanishes: reflexivity is approximately
**scale-invariant**, and as W → ∞ the branching ratio converges to
**criticality (n → 1)** with 1 − ñ ∝ W^−0.37 on 2010 E-mini data
(PDF p. 5, Fig. 5; two regimes with a ~5-minute transition).

## Findings, graded (does any kill line move?)

**NO kill line changes.** All five C1-L2 lines and C8's eleven
stand. But this paper is the most serious qualification yet for
the C8 trigger layer, and it sharpens K7 (the Hawkes
boundary-constraint line) from a convergence check into a
**window-scale question**:

1. **[sharpening, owner must ratify] The 0.8 threshold is an
   estimator-at-scale-W statement, not a true-n statement.** The
   mean-variance estimator is *systematically biased downward* for
   finite W (PDF p. 3: "our approximation systematically
   underestimates the branching ratio since our finite window size
   does not completely cover the region of support of the
   autocorrelation function"), and the MLE estimator's β̂ — hence
   n̂ = α̂/β̂ — is capped by the timestamp randomization scale (PDF
   p. 5: ms randomization gives β̂⁻¹ ≈ 10⁻²; intra-second
   randomization prevents β̂⁻¹ exceeding ~1s). Consequence for C8:
   the pre-declared protocol must fix, BEFORE the data, (a) the
   estimation window W (and ideally a small W-ladder, e.g. 10s /
   30s / 5min, reported together), (b) the timestamp-precision
   handling, and (c) that the 0.8 threshold applies to the
   estimator at the frozen W. A threshold without its W is
   analyst-tunable — the exact sibling of the β-factor bug the
   math verification already caught.
2. **[qualification of Amendment 1, to be recorded honestly]**
   Amendment 1 grounded 0.8 in Filimonov-Sornette's 0.7-0.8 modern
   regime. This paper REPRODUCES those numbers at fixed W (PDF
   p. 6) and simultaneously argues the trend is a fixed-W artifact
   (PDF p. 6, Fig. 7: Moore's-law-rescaled W gives an
   approximately constant branching ratio). Both readings put the
   market near criticality — which is GOOD for the trigger's
   existence — but they disagree about what crossing 0.8 means
   ("unusually endogenous" vs "the window scale moved"). The C8
   file should carry the controversy, not hide it: the F-S numbers
   remain the calibration source; Hardiman-Bouchaud is the
   standing caveat.
3. **[gift, free to take] A model-independent cross-estimator.**
   ñ = 1 − √(μ_W/σ²_W) (Eq. 7, PDF p. 3; sample estimators Eqs. 8-9)
   needs no kernel choice, no MLE, one line of numpy — the paper's
   central point is that kernel choice is the MLE method's main
   pitfall (PDF p. 2). C8 should run it beside the MLE as the
   robustness check: if the two estimators disagree on WHICH bars
   are above 0.8, the trigger is not ready to govern anything.
4. **[gate item] Timestamp bundling corrupts the MLE.** The
   global likelihood minimum can describe packet clustering inside
   the millisecond rather than true dynamics (PDF p. 2). Tardis
   carries microsecond timestamps — no randomization needed —
   but the L0 gate should assert timestamp resolution on arrival
   (the existing `intake_audit.py` timestamp-units assertion is
   exactly this; note it in the C8 execution order).
5. **[interpretive caution] "Critical" does not mean
   "Hawkes-true."** The authors insist the n → 1 conclusion holds
   only if the Hawkes model is the right representation; markets
   may be more complicated, with n = 1 + long-ranged kernel the
   best HAWKES description of non-Hawkes dynamics (PDF pp. 1-2,
   p. 6). For C8: the trigger measures endogeneity AS MODELED;
   the claim language should never say "the market is critical,"
   only "the branching ratio estimator crosses the pre-declared
   line at the pre-declared scale."

## What this paper would have killed if we had done it wrong

If C8 had frozen 0.8 without freezing W, and then chosen W after
seeing which bars light up — that is a tunable trigger, and this
paper is the recipe for tuning it invisibly (Fig. 2, PDF p. 4:
the estimate converges only as W grows; Fig. 3: near-critical
processes give 1 − ñ ∝ W^−ε, so W selection IS n selection). The
sharpening in item 1 closes exactly this hole. Grade: **no kill
line changed; one kill line (K7) materially sharpened, pending the
owner's ratification** — same protocol as session 1's two
sharpenings; nothing is armed by this note.

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The Hardiman-Bouchaud position is itself contested
(Filimonov-Sornette replied in the reflexivity debate); the C8
spec carries both readings and the owner decides what the trigger
layer claims.
