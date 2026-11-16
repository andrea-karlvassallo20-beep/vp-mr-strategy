# The road to the endpoint — methodology review and forward plan

Written during null time (owner studying; no L2 environment yet).
Nothing here tests a claim, tunes a parameter, or touches data. It
is the map: where the project is, what the endpoint is, and what
can be improved or done BEFORE the L2 data exists.

## 1. The endpoint, stated plainly

The endpoint of this programme is NOT a profitable strategy. It
is a COMPLETE LEDGER: every claim family either (a) survived its
pre-registered kill lines and is sized by the convexity framework,
or (b) died at a documented kill line and is never wondered about
again. The product is the map of what is real — the OHLCV verdict
page is the model of what an endpoint looks like: a question
closed so hard it stays closed.

Two terminal outcomes, both victories:
- **C8 passes:** the compression family is real at the book, the
  macro x micro interaction multiplies, the sizing framework
  (pre-registered in the C8 spec, section 7) turns it into a
  position-sized, cost-surviving answer.
- **C8 dies (fourth death):** the compression family is measured
  in the book itself — the last place the executive summary said
  it could live — and is not there. The L2 family's other leads
  (WATCH change detection, cross-impact, SPDE impact forms) are
  then the open frontier, with the compression question closed at
  every resolution: daily, watchlist, 30m, and L2.

## 2. Where the project stands (2026-11-16)

| Family | Status | Governing document |
|---|---|---|
| Compression (OHLCV) | DEAD x3 (C1 daily, watchlist, C7-30m) | `docs/ohlcv_verdict.html`, ledger |
| C1-L2 (compression at book resolution) | blocked-on-data | `c1_l2_test_spec.md` |
| C8 (macro x L2 synthesis) | DECLARED, blocked-on-data, math verified | `c8_macro_l2_synthesis_spec.md` |
| Library (evidence base) | 186 PDFs, 68 summaries, 5 formula families verified | `docs/library/manifest.md` |
| Deployment (Codespaces L2) | `CLOUD_DEPLOY.md` written; `.devcontainer` pending | root `CLOUD_DEPLOY.md` |

## 3. The path from here, as a decision tree

1. Owner provisions the codespace, runs the L0 gate
   (`src/gate_tardis_sample.py`). Gate fails -> fix acquisition
   (schema, truncation); no science until it passes.
2. C1-L2 runs on gated data. Its kill lines decide:
   - dies -> the compression family is dead at book resolution;
     C8's base is gone; the L2 leads (WATCH, cross-impact, SPDE)
     inherit the frontier. Record the fourth death with the same
     tabulated honesty as the first three.
   - survives -> C8 runs (eleven kill lines armed, thresholds
     frozen, thresholds' calibration now source-grounded by
     Amendment 1).
3. C8 runs. Interaction CI excludes 1.0 AND joint superiority CI
   excludes 0 -> the synthesis is real -> the convexity sizing
   framework (already pre-registered) converts hazard into size.
   Any kill line fires -> record the death, publish the page,
   close the family.
4. Either way: the ledger is completed, the website tells the
   whole story, and the programme ends with a map, not a hope.

## 4. Methodology review — what works, and seven improvements

What works and should never change: kill lines armed before the
data exists; placebos (era shuffle, 24h-shift book); DSR
multiplicity tax; the claims ledger as the single public record;
math verified against sources (`math_verification_2026-11-16.md`)
rather than trusted from memory or from me.

Improvements, in priority order:

1. **One authoritative spec per C-number (enforced).** This
   session found two live C8 pre-registrations (the
   `docs/c8_synthesis_spec.md` draft and the verified
   `paper/research/c8_macro_l2_synthesis_spec.md`). Duplicates
   are ambiguity defects: after a result, the loser of the two
   would be the one remembered. Fixed today by superseding the
   draft with a pointer; rule going forward: a C-number has
   exactly one governing spec, amendments are appended, dated,
   and marked, and supersession is recorded in both documents
   and the ledger.
2. **Every formula passes the verification harness before it
   enters a spec.** `src/verify_math_library.py` exists now; the
   rule is that no formula enters a pre-registration without a
   machine-checkable test in `tests/test_math_exactness.py`
   (the CKS non-strict-indicator and the beta-factor branching
   defects are the cautionary tales).
3. **Repo weight policy.** The library's raw PDFs are ~313MB in
   git history. Going forward: commit extracted texts and the
   index (small, searchable, useful); new raw PDFs go to a
   git-ignored local folder or LFS. The texts are what the
   project reads; the PDFs are what the owner browses.
4. **A pre-registration template.** Every future C-number spec
   opens with the same six sections: falsifiable core, data and
   label, estimand, kill lines (numbered, armed), what is
   deliberately NOT pre-registered, and the execution order.
   All three existing specs already conform; the template makes
   the next one cheap and the review of it mechanical.
5. **Library triage, not library reading.** 176 expanded papers
   is a haystack. The protocol: topic-priority queue (C8-relevant
   first: Hawkes/branching-ratio, OFI/multi-level, impact), one
   page summaries ONLY for papers that can change a kill line or
   a formula; the rest stay indexed and unread until a spec needs
   them. Reading is justified by a spec's citation, not by
   curiosity.
6. **A null-time playbook** (this document, section 5) so that
   waiting-for-data time is never improvised.
7. **"Harvestable" defined before any pass.** A surviving claim
   is reported raw and net of round-trip cost at the prevailing
   book (fee + half-spread), and the sizing framework's
   convexity math is pre-registered in the C8 spec — so a pass
   goes to sizing, not to celebration.

## 5. The null-time playbook (what can run without L2 data)

Done this session: the 0.8 threshold source-grounded (Amendment
1); the duplicate spec superseded; the acquired library integrated
into the website's library page; this roadmap.

Still open, in order of value, all data-free:
- **`.devcontainer` for the codespace** — the last deployment
  gap; python 3.12, pandas/pyarrow/scipy/lifelines/pypdf, the
  TARDIS_API_KEY secret wiring, a post-create command running
  the repo's test suite (`tests/`) so the environment is verified
  the moment it boots.
- **Pre-write the C1-L2 result pages** (pass and fail variants,
  numbers blank): when data arrives, the verdict is a fill-in,
  not a writing exercise under excitement.
- **Cheatsheet coverage of the WATCH detector** — the exact
  threshold construction from the acquired source text
  (043), formula + tested numpy function, same standard as the
  five existing families.
- **Library triage round 1** — one-page summaries for the ~10
  C8-critical expanded papers (branching-ratio approximation,
  multi-level OFI, high-frequency OFI forecasting), each checked
  against its extracted text.
- **The PDF policy switch** (improvement 3) executed once the
  owner confirms.

## 6. Where I would like this project to move

The programme's center of gravity is already right: falsify
first, pre-register everything, verify math against sources,
publish every death. The one direction I would push: **make the
L2 family's falsification as cheap as the OHLCV family's was.**
Every hour spent on gates, templates, pre-written verdicts, and
verification harnesses is an hour subtracted from the dangerous
gap between "data arrived" and "answer recorded" — the gap where
excitement lives. The endpoint is a complete ledger; the road to
it is paved with things that were ready before they were needed.
