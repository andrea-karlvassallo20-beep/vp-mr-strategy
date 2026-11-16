# 047 — The Microstructure of the 'Flash Crash' (Easley, Lopez de Prado & O'Hara, 2011)

**Venue:** Journal of Portfolio Management | **Category:** HF data & intraday
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
The event study of May 6, 2010: flow toxicity (VPIN) on E-mini
futures rose to extreme levels hours before the crash; liquidity
providers who monitor toxicity would have withdrawn before the
spiral. The paper's claim is that the crash was a liquidity
crisis triggered by toxic flow, not purely an algorithmic accident.

## The math that matters
Same VPIN machinery as 046, applied as a time series with
pre-event trend analysis; the empirical claim is a level shift in
VPIN preceding the price collapse.

## Why it matters for the L2 project
The precedent for C8's design: a microstructure state variable
(branching ratio, OFI, VPIN) that LEADS a macro price event is the
whole hypothesis class. Note also the controversy: the leading
claim was disputed — hence C8's insistence on pre-registered kill
lines rather than post-hoc event narratives.

**Caveat:** Verify against library source before production.
