# Library deep-read session 7 — Lee & Seo, "Modeling microstructure
# price dynamics with symmetric Hawkes and diffusion model using
# ultra-high-frequency stock data" (arXiv:1908.05089v1, 2019; S&P 500
# tick data, 10 NYSE names, 2007-2011)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/pdfs/`, extracted page-marked text in
`docs/library/text/x5eb309_modeling_microstructure_price_dynamics_with_symmet.txt`).
Next by triage rank (session 8's pointer): the symmetric Hawkes
tick model — the branching matrix AT the exact grain the trigger
layer would measure it.

## The paper in one paragraph

The authors model the tick price as the difference of two symmetric
Hawkes processes (up moves N1, down moves N2, common baseline mu,
common decay beta, self-excitation alpha_s, cross-excitation
alpha_c, PDF pp. 4-5), derive a closed-form return-variance formula
(Prop. 1 / Remark 2, PDF p. 5:
Var ~ 2*delta^2*mu*t/S0^2 * (1-q_s+q_c)^2 * (1-q_s-q_c), with
q_s = alpha_s/beta, q_c = alpha_c/beta the branching matrix
entries), and estimate daily and intraday on 1-second NYSE
mid-price data. A diffusion analogy (square-root processes for drift
and instantaneous variance, mapped onto the Hawkes parameters) is
proposed — explicitly NOT a rigorous limit (PDF p. 14), but close
in distribution and analytically convenient. Empirics: the Hawkes
volatility estimates from as little as ten minutes of data (PDF
pp. 17-18), beat TSRV on efficiency in simulation (Table 1, PDF
p. 6), run 15-25% ABOVE TSRV on real data with the gap unexplained
(Table 6, PDF p. 18), and the baseline intensity mu — not the
excitation parameters — is the parameter that carries the day's
volatility state (PDF p. 17).

## Findings, graded (does any kill line move?)

**NO kill line changes.** All five C1-L2 lines and C8's eleven
stand. One candidate sharpening is queued for the trigger layer,
one reinforcing note recorded:

1. **[candidate sharpening, PENDING OWNER RATIFICATION] The
   branching matrix is read PER BRANCH, never by its spectral
   radius alone.** The symmetric structure makes the object
   explicit: Q = [[q_s, q_c], [q_c, q_s]], eigenvalues
   xi_1 = -beta - alpha_c + alpha_s and xi_2 = -beta + alpha_c +
   alpha_s (PDF pp. 4-5), and the two branches are different
   MECHANISMS: q_s is the cascade branch (up excites up), q_c is
   the mechanical-mean-reversion branch (up excites down, Bacry et
   al. 2013's microscopic noise). Their own S&P 500 estimates show
   cross-excitation DOMINATING on many ordinary days — GE January
   2011: alpha_c = 1.3576 vs alpha_s = 0.4661 on 0103, alpha_c =
   1.3941 vs alpha_s = 0.4853 on 0104 (Table 4, PDF p. 16); the
   GE monthly average has alpha_c > alpha_s (Table 5, PDF p. 17).
   Consequence for the trigger: a total-branching or spectral-
   radius reading near one can be produced by saturated MEAN
   REVERSION with no cascade at all. Pre-declaration text: every
   branching reading in the trigger layer carries q_s and q_c
   separately with their bootstrap CIs (extending the queued CI and
   boundary-solution rules from sessions 5 and 7), and ONLY the
   self-excited branch q_s can fire the cascade interpretation —
   the cross branch cannot, by construction. This makes the
   trigger harder to fire, which is the only legal direction.

2. **[reinforcing, no new item] The moving parameter is mu, not
   the branching structure.** Day-over-day, mu tracks the
   volatility state with GARCH-like persistence while alpha_s,
   alpha_c, beta "do not appear to be meaningful" movers (PDF
   p. 17); in 2008 the crisis moved mu (and alpha_s, beta), with
   alpha_c "rather stable" (PDF p. 17). This is field evidence for
   the queued drift-reporting item (sessions 4/4b): a window whose
   volatility rose is a window whose MU drifted, and a branching
   reading taken over such a window must report the mu path beside
   it, or it launders a vol change into an endogeneity story.

3. **[interpretation language for the vol-tautology family] The
   SIGN of the microstructure bias is itself an excitation
   fingerprint.** Their mean signature plot rises toward small
   tau with mutual excitation dominant and falls with self
   excitation dominant (Prop. 5 area, PDF p. 12, Fig. 5) — i.e.
   the direction of the realized-variance bias at fine grains is
   determined by WHICH excitation dominates, not by a fixed
   "microstructure noise always biases up" constant. Any C1-family
   variance check that assumes a fixed bias sign would have
   imported this paper's Figure 5 as a counterexample. (Their own
   text on p. 12 misprints "a_s < a_c" into BOTH clauses; the
   figure and the formulas carry the correct reading — cite the
   figure, not the sentence.)

## What this paper would have killed if we had done it wrong

If the trigger layer had used a single pooled branching ratio or
the spectral radius of Q as its endogeneity reading (the natural
implementation, and the one the Hardiman-Bouchaud approximations
invite), then ordinary tick-grain S&P 500 data — where the GE daily
estimates sit at q_c roughly double q_s — would have read
"near-critical" on quiet days that were merely fast mechanical mean
reversion. A false trigger, and worse, one whose placebo battery
on labels could not catch it, because the artifact lives in the
FEATURE decomposition, the same boundary as session 7's
boundary-solution rule. The per-branch rule in item 1 closes
exactly this hole. Grade: **no kill line changed; one candidate
sharpening queued (per-branch branching readings, cascade
interpretation reserved to q_s), zero armed** — the owner's word
remains the only trigger.

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The estimates are one venue class (NYSE mid-quotes, 10
liquid S&P 500 names, 2007-2011), the timestamps are 1-second with
same-second events redistributed (PDF p. 15) — a coarser grid than
the L2 replay, so the q_c dominance reading transfers as a caution,
not a constant; the Hawkes-vs-TSRV gap (15-25%, cause unknown, PDF
pp. 17-18) means any volatility computed from Hawkes parameters
carries an unexplained level bias; and the diffusion analogy is
explicitly heuristic (PDF p. 14) — its leverage-parameter estimation
needs samples their own simulation flags as often insufficient
(PDF p. 13). arXiv v1 only; check for a published version before
formal citation.
