# Library deep-read session 5 — Kang, "The Physics of Price Discovery:
# Deconvolving Information, Volatility, and the Critical Breakdown of
# Signal during Retail Herding" (arXiv:2601.11602v2, 2026)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: the legally
acquired, page-marked extracted text
(`docs/library/text/x6698e9_the_physics_of_price_discovery_deconvolving_inform.txt`);
page cites are to that PDF. Rank 3 of the 500-paper edge triage
(`docs/library/edge_triage_500.md`). Korean equity market,
Jan 2020 - Feb 2025.

## The paper in one paragraph

Combines Tikhonov-regularized deconvolution of investor-flow
impulse responses with Hawkes self-excitation analysis of trading
surges. Findings: foreign/institutional flows drive permanent
price discovery while individual (retail) flows provide contrarian
liquidity; retail surges are panic-driven and near-explosively
self-exciting; during herding episodes institutional impact
deteriorates in small caps while large caps stay resilient. The
paper's own headline: market efficiency is a STATE VARIABLE —
conditional on herding intensity and firm size — not a constant.

## Findings, graded (does any kill line move?)

**NO kill line changes.** All five C1-L2 lines and C8's eleven
stand. One candidate sharpening (owner ratification required) and
strong reinforcing evidence for two queued sharpenings:

1. **[sharpening, owner must ratify] The boundary-solution rule,
   documented in the wild.** Their branching-ratio point estimate
   is 0.998 with a 95% bootstrap CI of **[0.050, 0.660]** (PDF
   pp. 13-14, appendix p. 30-31) — and their own appendix says the
   quiet part out loud: the 0.998 "represents the optimizer
   'hitting the wall' of the stability constraint," the bootstrap
   distribution is positively skewed, and the point estimate "is
   likely a constrained boundary solution rather than the true
   underlying value" (PDF p. 31). This is C8's K7 pathology with
   a worked example: an MLE pinned at the n < 1 constraint
   produces n-hat ~= 0.998 that means NOTHING about criticality.
   Candidate pre-declaration for the trigger layer: every
   branching-ratio reading in a trigger window carries its
   bootstrap CI; a window whose estimate is a boundary solution
   (n-hat within optimizer tolerance of the constraint) is
   MISSING, not high. This sharpens K7 (which already demands the
   boundary-constraint majority) from "count them" to "do not let
   them fire the trigger."
2. **[reinforcing, session 3's normalized-units sharpening]**
   Normalization choice changes the signal's regime-dependence:
   volume normalization (STV) is "contaminated by volatility
   artifacts" (PDF p. 8) — under herding, the signal breakdown is
   Herding/Normal = 0.37 with STV vs 0.91 with market-cap
   normalization (PDF p. 39). The cousin of session 3's finding
   (raw-queue-size OFI thresholds are unit-dependent): the
   normalization must be pre-declared because it determines how
   much of the "signal" is really volatility wearing a costume.
   The C8 layer's depth/tick-normalized OFI (session 3, queued)
   gains independent supporting evidence.
3. **[reinforcing, the trigger's meaning] Retail herding is the
   near-critical population.** Individual-investor surges are
   "predominantly panic-driven and exhibit near-explosive
   self-excitation" (PDF p. 1); their branching ratios sit at
   0.98-0.999 across surge thresholds (PDF p. 33). For C8 on
   crypto perps (a retail-heavy venue): the branching-ratio
   trigger likely measures RETAIL PANIC self-excitation — which is
   precisely the endogenous-release mechanism the interaction
   hypothesis wants, but the interpretation language should say
   "the trigger fires on self-excited flow," not "the market is
   critical." Also a warning: a trigger dominated by one
   population's panic is regime-fragile (their impact breakdown
   in small caps during herding).
4. **[philosophical support]** "Market efficiency as a state
   variable — conditional on herding intensity and firm size"
   (PDF p. 1) is the C8 premise stated in another market: the
   hazard is conditional on state. Citable support for the
   interaction hypothesis's framing; tests nothing of ours.
5. **[honest methodological caution, adopted by reference]**
   Their data is non-stationary (ADF p = 0.998, KPSS p = 0.01)
   with a trending branching ratio (+0.0145/year, PDF pp. 13-14),
   and they warn that on trending data historical training
   mis-calibrates (PDF p. 37) and that out-of-sample monitoring
   of the branching ratio "will be crucial" (PDF p. 26). The C8
   trigger's calibration window and its drift reporting are
   already queued items (session 4/4b's W-ladder); this is the
   same warning from an independent market.

## What this paper would have killed if we had done it wrong

If C8's trigger had read n-hat = 0.998 as "near-critical, fire,"
on a perps window where the optimizer had merely hit the
constraint wall, the trigger would fire on an ARTIFACT of the
estimator — and the placebo (era-shuffled labels) would not catch
it, because the artifact is in the FEATURE, not the label. The
boundary-solution rule in item 1 closes exactly this hole. Grade:
**no kill line changed; K7 gains a candidate boundary-solution
rule (bootstrap CI per window; boundary solutions are missing,
not high), pending the owner's ratification** — same protocol as
every session; nothing is armed by this note.

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The paper is single-author, Korean equities (not
crypto), 126 baseline surge events (small-sample caveats are the
paper's own), and its "Kang (2025)" self-citation for the
market-cap normalization claim was not independently checked.
The boundary-solution pathology, however, is a property of the
ESTIMATOR, not the market — which is why it transfers.
