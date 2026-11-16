# Library deep-read, session 1: Cont, Kukanov & Stoikov (2011/2014), "The Price Impact of Order Book Events"

Read against ONE question: **what here kills C1-L2 (or C8) faster, or
changes a kill line?** Source: the extracted text
(`docs/library/text/018_cont_kukanov_stoikov.txt`, arXiv:1011.6402v3);
page numbers below are the text's page markers.

## What the paper establishes (with pages)

- OFI is the signed net change of the best bid/ask queues: limit adds and
  price improvements raise it; cancels, market orders and price walks
  lower it. A market sell and a cancel buy of the same size are
  **equivalent by construction** (p. 3) - OFI cannot tell them apart.
- On a 10-second uniform grid, 50 NYSE stocks, April 2010: mid-price
  changes (in ticks) are LINEAR in contemporaneous OFI, average R^2 = 65%,
  slope beta significant in ~100% of half-hour subsamples (pp. 3, 11).
- The impact coefficient is inversely proportional to depth:
  beta_i = c / AD_i^lambda with lambda ~= 1 (pp. 6, 12-13). Intraday
  patterns in impact and volatility are explained by observable depth
  alone - no unobservable information-asymmetry parameters.
- Event autocorrelations vanish after ~10 seconds (p. 7). The relation
  is robust across time scales and stocks (abstract, p. 3).
- Their own placebo: re-sampling the mid at trade times instead of the
  uniform grid drops R^2 to 35-60% (p. 8 fn) - the clock choice is a
  first-order effect, not a nuisance.
- The "square-root law" of volume impact is derived as a statistical
  artifact of aggregation; volume-based relations are noisy and less
  robust than OFI-based ones (pp. 3-4, section 4).

## Findings, graded by whether they change a kill line

**Changed no kill line.** All five C1-L2 kill lines and C8's eleven stand
exactly as pre-registered. Four sharpenings:

1. **The 4h/24h clock cannot inherit OFI's power (interpretation, not a
   kill line).** The 65% R^2 is a *contemporaneous 10-second* statement;
   the paper offers no evidence OFI carries information across hours.
   C8's design is consistent with this (extreme OFI is a *trigger* state
   at the moment of decision, not a horizon forecast), but any future
   temptation to "smooth OFI over the horizon" is now pre-condemned: the
   paper's own ACF decay (~10 s) says the smoothed version is mostly
   noise. The 24h-shift book placebo already guards a version of this.

2. **Depth IS the market factor (supports C8 amendment A5).** The
   review's blocking amendment demanded the "market-book common factor"
   be defined before the run. CKS hands us the definition: because
   beta_i = c / AD_i, cross-sectional and intraday depth variation
   creates a common impact factor by construction. Candidate definition
   for the C8 amendment: the market factor is the venue-wide average
   depth AD (or the first principal component of per-level depths),
   enterable as a covariate, exactly the observable the theory names.
   This is a proposal for the owner to ratify in the amendment, not a
   change made here.

3. **The clock placebo is precedented (supports the VPIN clock fix).**
   CKS's own trade-time re-sampling changed R^2 by ~25 points. The C8
   review's demand for ONE fixed VPIN clock (volume buckets per the
   original construction) is the same lesson; the paper is the citation
   for why the two-clock ambiguity is fatal rather than cosmetic.

4. **Unit normalization is a silent degree of freedom (implementation
   note for the harness, sibling of the beta bug).** Our math
   verification already caught one beta-factor bug in the Hawkes
   branching metric. The CKS sibling: OFI is in units of queue SIZE,
   delta-P is in TICKS, so beta carries units (ticks per contract). On
   Binance futures the queue size is in contracts/BTC, the tick is 0.1
   USDT, and the multiplier is not 1 - an OFI threshold pre-registered
   in raw units is unit-dependent and therefore analyst-tunable. The C8
   "extreme OFI" threshold must be pre-declared in normalized units
   (tick-size and depth normalized, e.g. OFI / AD, which the theory
   itself says is the right scaling). To be recorded in the C8
   amendment before arming.

5. **A warning for the control group.** The paper shows volume-based
   variables are the noisy shadow of OFI. Any C8 control built on volume
   (the vol family, one factor wearing six names) would be testing the
   artifact, not the mechanism - consistent with, and reinforcing, the
   existing "L2 vol-tautology asked first" kill line.

## The cancel-blindness caveat (recorded honestly)

OFI treats a market sell and a cancel buy as the same event. The C5
claim (passive cancellation as the mechanism) is therefore NOT testable
through OFI alone - it needs the event-type decomposition the raw
incremental feed provides. This is not new (the programme already knows
it), but the paper states it as a definition, so it is pinned here with
the citation.

## Grade

Session grade: **no kill line changed; one amendment sharpened (the
market factor now has a theory-named candidate definition: depth); one
implementation pre-declaration required before arming C8 (OFI threshold
in depth-normalized units); one reinforcing citation for the clock
discipline.** Read again before the C8 amendment is written.
