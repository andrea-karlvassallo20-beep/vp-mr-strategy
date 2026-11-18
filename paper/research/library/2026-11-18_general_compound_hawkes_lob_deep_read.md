# Deep-read session 13 — Swishchuk & Huffman, "General Compound Hawkes Processes in Limit Order Books"

Null-time session 15 (deep-read 13, offset honored; session number taken fresh from the log
tail at append time — the previous parallel slot landed as log entry 18 / null-time session
14 / deep-read session 12). Anatoliy Swishchuk & Aiden Huffman, University of Calgary;
arXiv:1812.02298v1, 6 Nov 2018 (stamped "Manuscript submitted", Mathematics in Science
and Industry, placeholder pagination). Whether compound Hawkes constructions with
Markovian price-change size states yield diffusion limits whose volatility factorizes into
arrival and size terms, tested against one-day LOBSTER level-1 mid-price data.

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8 faster, or change
their kill lines? Source: legally acquired OA copy
(docs/library/text/xfeb371_general_compound_hawkes_processes_in_limit_order_b.txt, 27 pp.,
page-marked). Assignment trace: PRE-ASSIGNED by the owner in a 24-slot parallel launch (this
slot 6; triage score 36), not read as the queue's top pointer; verified at session start that
no deep-read note for this slug exists in paper/research/library/ and no open or unmerged
closed PR covers it. The queue's next UNREAD triage pointer is unchanged.

## The paper in one paragraph

The authors build compound Hawkes mid-price models S_t = S_0 + Σ_{k≤N(t)} a(X_k) where N(t)
is a (possibly non-linear) Hawkes process counting mid-price changes and X_k is an
ergodic Markov chain on the size/state of each change (Defs. 3.1–3.4, PDF pp. 6–7), and
prove LLN and FCLT/diffusion limits for the family (Thm 4.1 nonlinear, Thm 4.3 n-state,
Cor. 1 two-state, Cor. 3 fixed-tick; PDF pp. 7–13). The diffusion limit factors mid-price
volatility: (S_nt − N(nt)â*)/√n → σ*√(λ/(1−μ̂))W(t), with the arrival term λ/(1−μ̂), the
kernel mass μ̂, and the size-state term σ* built from the chain's transition matrix and
ergodic probabilities (Eq. 34, PDF p. 9; Eq. 36, PDF p. 10; for exponential kernels
λ/(1−α/β) in Eq. 59, PDF p. 14). Empirically, on LOBSTER level-1 data for AAPL, AMZN, GOOG,
MSFT, INTC on a single day (June 21, 2012, first/last 15 minutes dropped; PDF p. 13),
inter-arrivals are non-Poisson and clustered (Figs. 1–2, PDF pp. 21–22), exponential-kernel
MLE fits reproduce expected arrival counts (Tables 2–3, PDF p. 13 with values on PDF
p. 14), and the fixed-tick CHPDO model severely underestimates mid-price variability on the
multi-tick names because 61%/53%/71% of their mid-price changes exceed half a tick (PDF
p. 15; Fig. 4, PDF p. 24), while quantile-built n-state chains on change sizes recover most
of it (AAPL mean residual 0.0050→0.0036, GOOG 0.0115→0.0046 relative to the 2-state
version; Table 8, PDF p. 18) with theoretical-vs-regression coefficient percent errors near
or under 5% for four of five names and 20.8% for AMZN (Table 9, PDF p. 18).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The size-state persistence comparator
   — a third null for the C1-L2/C8 admission family. The paper's own construction is the
   mechanism: a Markov chain whose states are quantile bins of past mid-move sizes, whose
   transition matrix is estimated by simple relative frequency counting (pdd/puu, PDF p. 14),
   and whose stationary spread â*, π* — with no order flow, no events, no depth, nothing but
   the tape's own sequence of move sizes — captures the variance that the intensity-only
   fixed-tick model missed (28–60% mean-residual reductions, AAPL 0.0050→0.0036, GOOG
   0.0115→0.0046; Table 8, PDF p. 18). Candidate pre-declaration: any short-horizon C1-L2/C8
   flow feature earns an incremental-claim comparison only if it adds value beyond (a) the
   top-of-book OFI benchmark (CKS kill line 7), (b) the pre-registered Eq.-7 queue-imbalance
   comparator (session 11's two-null rule), AND (c) a pre-registered own-price size-state
   persistence comparator built exactly as the paper's Sec. 5.3 quantile chain (PDF pp. 16–17)
   on the venue's realized mid-move size distribution. Harder to pass than the standing
   two-null rule because the third comparator never touches the book or the event stream: a
   flow feature beaten by the tape's own size persistence carries no incremental
   microstructure claim, and this null is immune to both event-flow laundering and depth
   laundering. The owner ratifies; nobody else arms anything.

2. [interpretation caution] Fixed-tick constructions are structurally biased on multi-tick
   venues, and the C1-L2 venue is one. The paper's CHPDO fits collapsed on AAPL/AMZN/GOOG
   precisely because their mid-price moves are usually larger than half a tick (61%/53%/71%,
   PDF p. 15; Fig. 4, PDF p. 24); a maximal-small-tick perp is in that regime, so any
   feature, normalizer, effect-size band, or null that embeds a one-tick mid convention must
   be declared alongside the venue's actual move-size distribution. Corollary caution: even
   the size-chain never fully captured AMZN (20.8% coefficient error vs ≤6.4% for the other
   four; Table 9, PDF p. 18) — no parametric state model on this shelf "explains" mid-price
   variance fully, so a residual is not evidence of a flow channel.

3. [reinforcing, no new item] Implied branching ratios α/β from the MLE fits (Table 2,
   PDF p. 14: AAPL 0.409, AMZN 0.420, GOOG 0.437, MSFT 0.527, INTC 0.526) all sit far below
   criticality, and the diffusion limit requires μ̂<1 with a finite first moment (Eq. 35,
   PDF p. 9) — per-branch estimation is the only legal shape, exactly the standing per-branch
   rule. Direction persistence itself flips across names (pdd/puu > 0.5 for MSFT/INTC,
   < 0.5 for AAPL/AMZN/GOOG; Table 4, PDF p. 15), reinforcing the sign-register rule for
   excitation features: persistence is a signed regime property, never a magnitude to be
   averaged across instruments.

4. [reinforcing, no new item] Non-Poisson inter-arrival times and visible one-minute
   clustering of mid-price changes (Figs. 1–2, PDF pp. 21–22) support the clustering
   warrant already on record from the earlier Hawkes reads; nothing new, no queue change.

5. [source-quality note] arXiv:1812.02298v1, 6 Nov 2018; single trading day (June 21, 2012),
   five US equities, level-1 LOBSTER data only, no parameter-stability tests across days;
   the shelf knows no published version of this manuscript (venue stamp is placeholder
   pagination, PDF p. 1) — check before formal citation. Note N(t) counts mid-price changes,
   not order arrivals, despite the title's "in limit order books"; one typographical error
   in the running text ("earier", PDF p. 14), and Corollary 1's condition (Eq. 51, PDF p. 12)
   restates the first-moment bound where Theorem 4.3 (Eq. 35, PDF p. 9) correctly requires
   the second moment ∫sμ(s)ds < ∞ — cite Eq. 35, not Eq. 51, should the condition ever
   matter.

## What this paper would have killed if we had done it wrong

If the C1-L2 admission family had contained only event-flow and depth nulls, a size-state
persistence chain — a few lines of frequency counting on the price tape, the cheapest
computable object in this entire literature — could have absorbed the registered flow
feature's apparent value after the fact, and the claim would have died in post-hoc review
instead of at a pre-declared gate. And if kill-line magnitudes or expectation bands had been
transplanted from this paper's single-day 2012 equity fits (e.g., treating its ≤5%
theoretical-vs-empirical diffusion-coefficient errors as a transferable tolerance), a
genuine signal on a structurally different venue could have been judged against a
miscalibrated band — the false-kill that the programme treats as the worst failure mode.
Pre-declaring the third null AND its quantile construction before the L2 data closes both
traps.

## Standing caveat

Ammunition, not evidence: nothing in this note enters any claim as support. The magnitudes
are one-day, five-name, 2012-Nasdaq, level-1 specific; the "order flow" modeled is the
mid-change stream; the fits carry no cross-day stability evidence; AMZN's unexplained
variance is the paper's own admission that the model class is incomplete (Sec. 5.5,
PDF p. 19). What transfers, cautiously, is structure only: mid-price volatility factorizes
into an arrival term and a size-persistence term, and the size term is computable from the
tape alone. The port of any comparator to the C1-L2 venue belongs to that gated spec, not to
this citation. arXiv-version caution applies: check the published version before formal
citation.