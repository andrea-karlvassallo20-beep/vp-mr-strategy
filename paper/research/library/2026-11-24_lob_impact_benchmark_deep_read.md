# Deep-read session 106 — Nigmatulin et al. (2026), "LOB-Impact Benchmark: Emergent Market Impact in Generative Limit Order Book Models"

Authors: George Nigmatulin, Valentin Mohl, Sascha Frey, Kang Li, Aramis
Marti-Shahandeh, Mihai Cucuringu, Anisoara Calinescu, Jakob Foerster and
Stefan Zohren. Venue: arXiv:2610.27100v1 [q-fin.TR], 19 Oct 2026;
published version identified on the extract itself: the proceedings of
ICAIF '26 (ACM, DOI 10.1145/3858063.3858909, CC-BY 4.0, PDF p. 1). One
clause on what it is: a benchmark/methods paper that injects
execution-style metaorders into generative limit-order-book message
models and measures the emergent impact response — existence,
attribution, shape and relaxation — through a claim ladder with paired
blind controls and baseline kernels whose physics is written in.

Read 2026-11-24, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x88c3e6_lob_impact_benchmark_emergent_market_impact_in_gen.txt,
9 pp., page-marked). Next UNREAD triage-rank entry (score 19, SECOND of
the SEVENTEEN-entry score-19 tier; consumed per the ## 140 closing
pointer's explicit tier order; verified note-less before this session
against the live library listing).

## The paper in one paragraph

The benchmark takes a message-level generator, a stock, a per-stock
calibration from the stock's own LOBSTER data (evaluation month January
2026, held out of training), and runs three phases with two paired
controls (PDF pp. 2-3, Fig. 1 PDF p. 3). Phase 1, free generation, reads
the balance: the trade-sign autocorrelation decay gamma_flow against the
mid-price Hurst exponent H, with persistent flow uncompensated by
transient impact showing up as a super-diffusive price — "a generator
that combines persistent flow with a super-diffusive price (H > 0.5) has
built a free lunch into its own market" (PDF p. 2) — plus free drift and
the single-trade response. Phase 2 injects a 100-child build-up metaorder
(aggro children of the stock's median market-order size, spaced by the
participation identity eta = 10%, Delta_N = 9 phi per day, Eq. 3, PDF
p. 4; child count fixed a priori at the empirical mean metaorder length,
PDF p. 4) and fits I = a*q^delta with existence decided before
magnitude: a least-squares identifiability test whose amplitude has
closed form per delta on a grid, a law counts as identified only when
the misfit curve has a sharp minimum and the amplitude clears a floor,
validated by planted laws recovered with a small downward bias (at most
0.11 at neural amplitudes) and 500 null trials in which not one false
law is returned (PDF pp. 3-4). Phase 3 stops injection after ten
children and reads relaxation over ten silent execution durations,
against real metaorders' decay to one-half to two-thirds of peak and
against kernel baselines with known physics (Propagator, Obizhaeva-
Wang) run under the same schedule, whose closed-form end-over-peak sets
the scale (PDF pp. 2-3). The blind control pairs every visible
build-up: same conditioning windows, same seeds, the injected orders
fill in the simulator's plumbing while neither model input carries
them, so the visible-over-blind ratio attributes the response to the
model itself (PDF p. 2). The verdict ladder C1-C5 uses tolerances fixed
in advance for every model (PDF p. 4). Panel: 13 models on 5 NASDAQ
stocks, one per order-to-trade cohort — four replay baselines (the
Historic negative control, a Heuristic permanent-shift, the Propagator
and OW kernels), four parametric generators (CST, NMZI, Hawkes,
queue-reactive) and five neural SSM message generators (S5-120M, S5-4k,
Mamba3, Mamba3-4k, GDN, 55M-120M parameters, context windows 500-4000
messages) sharing one eight-name corpus that includes four of the five
evaluation stocks (Table 1, PDF p. 5; Table 2, PDF p. 4; JAX-LOB
matching, PDF p. 5). Results, one signature repeated across all 25
neural model-stock cells: a law always exists (C2 pass) and is always
the model's own (C3 pass: visible at least 3x the blind floor in all
25 cells, over 10x in 16, PDF pp. 4, 8) but is never the square-root
law (C4 fail: binned exponents 0.63-1.21, all 25 day-clustered
intervals excluding 0.5, PDF pp. 5, 7-8) and never credibly relaxes
(C5 fail: end-over-peak mostly above 1 — the price keeps moving in the
metaorder's direction after the last child executes — with the three
lowest descents riding the heaviest-drift rows, "the descent is drift,
not resilience", PDF pp. 1, 7-8); every neural generator also fails C1
and drifts freely, from -3 to -879 ticks per rollout (PDF pp. 5, 7).
Amplitudes run Y = 2-50 against the empirical ~0.5, four to a hundred
times what a real metaorder pays per unit of participation (PDF pp. 5,
8); on EA, the one out-of-corpus stock, "the observed OOD result does
not destroy the law; it destroys its calibration" (Y 12-50, PDF p. 8).
Distributional scores (LOB-Bench) do not predict impact fidelity: the
rank correlation between KS and |delta - 0.5| is unstable in sign
(+0.54 on GOOG against -0.71 on MSFT, p = 0.02; MSFT neural rows
-0.90, p = 0.08), "the better mimic can sit farther from the impact
law, so the two properties must be measured separately" (PDF p. 8). The
authors attribute the joint C4/C5 failure to insufficient replenishment
with limited long-horizon memory (short contexts cannot retain the
pre-metaorder reference price), "tentatively" (PDF pp. 1, 8), and warn
that such simulators "can reward schedules that a real book would
punish" and that the repair direction matters: "learn replenishment
rather than unlearn persistence; killing flow memory would restore the
balance vacuously" (PDF p. 8). Everything is measured at one operating
point of one month of one exchange, and "a month atypical by about one
within-month standard deviation would already move the exponent past
its half-width cap" (PDF pp. 8-9). The benchmark is released open
source (PDF p. 9).

## Findings, graded (does any kill line move?)

NO kill line changed. ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The
   intervention-attribution blind-arm pre-declaration: BEFORE the L0
   gate, any C1-L2/C8-adjacent generative-null, placebo, comparator or
   simulator experiment whose readout includes the system's own
   response to an injected or experiment-side intervention (injected
   messages, orders or events; a forced or conditioned perturbation)
   must pre-declare, as frozen configuration counted in the
   multiplicity ledger, a blind attribution arm: runs identical to the
   visible runs in conditioning windows and seeds, in which the
   intervention executes in the simulator's plumbing (book
   reconstruction, matching, level consumption) but does not enter the
   model's inputs, with the response attributed through the
   visible-over-blind ratio under a margin fixed before the data — and
   every response conclusion (shape, magnitude, relaxation,
   reproduction or refutation of any mechanism claim) licensed only
   from runs that clear the declared blind floor; response conclusions
   from visible-only runs are unlicensed at the gate. Harder to pass
   because the attribution is today silent and the benchmark prints
   that it cannot be recovered from the measured quantities themselves:
   the replay kernels, with no model inside, identify at delta =
   0.73-0.81, inside the neural range on the same stock, "so the
   exponent cannot attribute the response, and a large amplitude could
   be purely mechanical impact" (PDF p. 2; Table 3, kernel rows, PDF
   p. 7) — a law's existence, its exponent and its amplitude are all
   consistent with pure book mechanics, and only the paired blind arm
   separates them (C3's at-least-3x criterion, PDF p. 4; measured v/b
   5.0-38 across the neural panel, PDF pp. 7-8). No queued rule asks
   the question: the dynamics-identification rule for generative nulls
   (null-time session 58) demands pre-declared flow-dynamics statistics
   beside the static marginals, not response attribution between
   plumbing and model inside an intervention experiment; the
   residual-flow attribution null (deep-read 82) conditions aggregate
   signed flow out of real-data episode attribution, not plumbing-vs-
   model attribution inside a simulator; the queue-jump-diffusion
   pre-declaration (deep-read 81) freezes null parameters, not the
   experiment arm structure; the generative-null agent information-set
   pre-declaration (deep-read 104, ## 139) declares what simulated
   agents see, not what the model sees of the experimenter's own
   intervention; the impact growth-class pre-declaration (deep-read
   105, ## 140) declares the impact functional's tail, not the
   measurement's attribution. Tightens the dynamics-identification
   rule for generative nulls on the intervention-response axis, and
   joins the residual-flow attribution null in extending the
   attribution family from observational episode attribution to
   experimental response attribution, complementing the agent
   information-set item (whose declaration the blind arm operationalises
   from the experimenter's side).
2. [reinforcing, no new item] Distributional realism licenses nothing
   about response and does not even rank it: the rank correlation
   between the LOB-Bench KS ranking and the |delta - 0.5| ranking is
   unstable in sign across stocks (+0.54 GOOG against -0.71 MSFT,
   p = 0.02) and mostly negative within the neural family (MSFT neural
   rows -0.90, p = 0.08), "the better mimic can sit farther from the
   impact law, so the two properties must be measured separately"
   (PDF p. 8). Reinforces the dynamics-identification rule for
   generative nulls (null-time session 58: static- or
   invariant-distribution match alone inadmissible for any refutation
   instrument) with a printed panel-wide mechanism, and reinforces the
   two-null admission family (log ## 17). No queue change.
3. [reinforcing, no new item] The relaxation failure prints the
   transient-layer premise as a generator failure: persistent flow plus
   insufficient replenishment produces steep, non-relaxing,
   quasi-permanent emergent impact (4 of 5 AMD generators end-over-peak
   above 1 — the price keeps moving after execution stops; no neural
   cell passes C5 anywhere, PDF pp. 1, 7-8), and the C1 balance the
   benchmark enforces is the programme's own: persistent signs must be
   compensated by transient impact, else the uncompensated
   super-diffusive drift is "a free lunch built into its own market"
   (PDF p. 2). Reinforces the impact-viability/transient-layer
   pre-declaration family (deep-read 87): a null missing the
   transient/replenishment component does not merely miss a stylized
   fact — it misprices every counterfactual response it is asked, and
   the failure is invisible to distributional metrics (finding 2). No
   queue change.
4. [interpretation caution] Free drift is a first-class measurement
   confounder in generative nulls: every neural generator drifts when
   left alone (-3 to -879 ticks per rollout, Table 3, PDF p. 7; PDF
   p. 5), and the benchmark carries a three-part discipline —
   antisymmetrisation so direction-independent drift cancels (Eq. 2,
   PDF p. 2), a separate no-injection arm so drift enters the
   accounting exactly once (PDF p. 2), and an explicit drift criterion
   under C5 so a descent cannot masquerade as resilience (PDF p. 4);
   the three lowest end-over-peak cells in the panel sit on the
   heaviest-drift rows, "the descent is drift, not resilience" (PDF
   p. 8). Any future symmetry- or response-based reading on a
   generative null must carry its drift arm; a drifting null can
   manufacture both build-up and decay appearances. No queue change.
5. [interpretation caution] Exponent-type estimates are
   operating-point- and sample-fragile, and only quotable behind an
   identification gate: everything is measured at one participation
   (10%), one child size, one metaorder shape, one month of one
   exchange, aggressive children (PDF pp. 8-9), and "a month atypical
   by about one within-month standard deviation would already move the
   exponent past its half-width cap" (PDF p. 9); the estimator quotes a
   number only where the existence gate identifies a law, validated by
   planted-law recovery with a measured downward bias (at most 0.11,
   so printed exponents are conservative) and 500 null trials with
   zero false laws (PDF pp. 3-4). Existence-before-magnitude reinforces
   the frozen-configuration identifiability axis (the model-inversion
   identifiability pre-declaration family), and the operating-point
   fragility is the standing reading discipline for any exponent- or
   shape-like quantity the L2 phase may estimate from a single window.
   No queue change.
6. [cost-survival ammunition] Calibration survives in corpus and dies
   out of corpus, so cross-instrument null comparisons must declare
   their calibration corpus against the evaluation universe: Y = 2-19
   on the four in-corpus stocks against 12-50 on EA, the one
   out-of-corpus name, where "the OOD result does not destroy the law;
   it destroys its calibration" (PDF p. 8); and a simulator with
   wrong-shape, non-decaying impact "can reward schedules that a real
   book would punish" (PDF p. 8). Relevant only under a future
   K7-style cost-survival layer. No queue change.
7. [source-quality note] arXiv v1 [q-fin.TR] 19 Oct 2026, published
   version stated on the extract: ICAIF '26 proceedings, ACM, DOI
   10.1145/3858063.3858909, CC-BY 4.0 (PDF p. 1) — the standing arXiv
   caution upgrades to "published version identified; cite it". Zero
   citations in the index; the benchmark's authors largely overlap
   with the authors of the evaluated generator family (JAX-LOB,
   LOB-Bench, the S5/Mamba LOB line), an honest self-evaluation printed
   as its own models' failures, mitigated by criteria fixed in advance
   (C1-C5 tolerances, PDF p. 4) and the open-source release (PDF p. 9).
   Pure methodology: the empirical anchors (beta ~ 0.5, Y ~ 0.5,
   two-thirds relaxation) are literature citations, and the paper's own
   measurements are measurements of models, not of markets. No queue
   change.

## What this paper would have killed if we had done it wrong

Without finding 1's blind arm, a future C8 intervention experiment on a
generative null could read a "response" that was entirely matching-engine
plumbing: the benchmark prints the exact failure class — book mechanics
alone identify an impact law at delta = 0.73-0.81, inside the learned
range, so neither existence nor magnitude separates them (PDF pp. 2, 8)
— and a "the null reproduces the mechanism" or "no null reproduces it"
conclusion would carry the artifact with no visible fingerprint in the
outputs. Without finding 2's print, a generator validated
distributionally (LOB-Bench-passing, message-level realistic) could
license null-refutation claims while its response channel was never
measured at all: the paper shows the two channels are nearly
uncorrelated across a whole panel, unstable in sign (PDF p. 8). Without
finding 4's drift discipline, an antisymmetrised or post-event reading
on a freely drifting null could manufacture mechanism claims from drift
(PDF p. 8). Without finding 6's caution, a comparator's calibration
transfer across instruments would be assumed rather than declared
(PDF p. 8). The queued attribution family, extended by finding 1 to
the experimenter's own injection arm, closes each channel before any
L0-gate run may license anything.

## Standing caveat

Everything above is the arXiv v1 text (9 page-marked PDF pages: title
and abstract, methodology with the claim-ladder figure, all model and
stock tables, the AMD results band by band, the full Table 3 for all
five stocks, discussion, limitations, conclusion, references complete;
nothing skipped). Scope: one exchange (NASDAQ via LOBSTER, January
2026), five stocks, one operating point (eta = 10% participation,
median-size aggressive children, N = 100 fixed a priori, one shape per
phase), 13 models of which the five neural generators share one
eight-name training corpus containing four of the five evaluation
stocks (EA the flagged exception); only AMD is read band by band, the
other four stocks live in Table 3 only (PDF p. 8). The authors' own
honesty: the context-length attribution for the missing relaxation is
"tentative" (PDF p. 1), the 4k-context variants "fail the same tests but
remain well short of a metaorder, leaving the attribution untested
rather than refuted" (PDF p. 8), and the month-sensitivity cap bounds
every exponent quoted (PDF p. 9). Nothing measured during this session.
The library is ammunition, not evidence: the paper's empirical
references are literature citations and its own numbers are
measurements of models, so nothing here licenses any C1-L2 or C8
claim. The published version is the ICAIF '26 proceedings (DOI
10.1145/3858063.3858909); cite it for any formal citation.

Nothing measured during this session. No kill line moved. Nothing armed.
Nothing trades live.
