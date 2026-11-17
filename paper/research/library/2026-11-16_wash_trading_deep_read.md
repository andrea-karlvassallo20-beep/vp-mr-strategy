# Library deep-read session 6 — Aloosh & Li, "Direct Evidence of
# Bitcoin Wash Trading" (Management Science; working-paper version
# via DCU institutional repository, 84 pp.)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally
acquired OA copy (DCU DORAS repository;
`docs/library/text/xaloosh_wash_trading.txt`, page-marked).
Companion evidence for session 5's wash-trading gate audit.

## The paper in one paragraph

Using the internal trading records of a major Bitcoin exchange
leaked by hackers, the authors directly identify wash trading
(a trader clearing her own limit orders): 2,887 wash trader IDs
out of 98,391 (about 2.9% of traders), whose transactions account
for roughly a THIRD of all trades and volume in the sample (PDF
p. 57); self-self trades are only 3.35% of an average wash
trader's activity — wash traders also trade with everyone else
(PDF p. 15). They then evaluate the INDIRECT detection techniques
the literature uses, against their ground truth: Benford's law,
trade-size clustering at round numbers, lognormality, and
structural breaks are USEFUL; power-law tail fits give OPPOSITE
conclusions (PDF pp. 1, 5).

## Findings, graded (does any kill line move?)

**NO kill line changes.** All five C1-L2 lines and C8's eleven
stand. The queued wash-trading audit (session 5, pending owner
ratification) gains a validated, sourced toolkit:

1. **[toolkit for the queued audit, owner ratifies the audit
   itself] The four statistics that survived ground truth:**
   - **Benford's law**: wash trades deviate (chi-squared 69.71,
     reject), non-wash conform (chi-squared 7.91) (PDF p. 17);
     computable per window from trade sizes alone.
   - **Round-number clustering**: wash trades cluster at rounded
     sizes (PDF pp. 5, 16); the unrounded-trade percentage per
     window is the statistic (PDF p. 27).
   - **Lognormality**: deviations from lognormal size
     distributions are indicative (PDF p. 5).
   - **Structural breaks**: wash-heavy months show more EDM
     structural breaks in 10-minute volume series, and the method
     works better on LOG-TRANSFORMED volumes (PDF pp. 23-25) —
     the only one of the four that operates at our 30m-bar
     grain.
2. **[the trap avoided] Power-law detection gives OPPOSITE
   conclusions** (PDF pp. 1, 5): fits of trade-size tails to a
   power law would classify wash-trading activity as CLEAN. This
   matters doubly here: the library's own cheatsheet carries the
   Clauset-Shalizi-Newman power-law machinery (Section source
   068), and an analyst reaching for it in the gate audit would
   be misled in the documented direction. The audit's statistics
   are now named, and power-law tails are explicitly NOT among
   them.
3. **[scale context, honest]** The direct evidence is from a
   2011-2013 leaked exchange — old, small, and not Binance
   futures. The modern perps feed is a different market; the
   finding that transfers is the EXISTENCE and the TOOLKIT, not
   the fraction. The audit's job on our data is to measure the
   fraction, not assume it.
4. **[mechanism note, refines the audit's signature]** Wash
   trading is not only "bursts without price change" (session 5's
   Fabre-Muni Toke signature): self-self trades are a small
   fraction of wash-trader activity — most of it is trading WITH
   everyone else (PDF p. 15), which DOES move price. So the
   audit should not rely on the no-price-change signature alone;
   the four ground-truthed statistics catch the broader
   phenomenon.
5. **[interpretation boundary for the trigger]** If some trigger
   windows are contaminated, the branching ratio measures the
   manipulator's self-excitation — the session 5 concern, now
   with direct evidence that wash trading generates concentrated,
   clustered, round-sized, structurally-breaking volume. The
   C8 file's claim language already queued the fix: contaminated
   windows are missing, not zero.

## What this paper would have killed if we had done it wrong

If the gate audit had used power-law tail fits (the library's own
heavy-tail recipe) as its wash-trading detector, it would have
produced OPPOSITE conclusions on ground-truthed data — a
confidently wrong audit. The toolkit in item 1 plus the
exclusion in item 2 close exactly this hole. Grade: **no kill
line changed; the queued wash-trading audit gains its sourced,
ground-truth-validated statistics (Benford chi-squared, unrounded
fraction, lognormality deviation, EDM structural breaks on
log-volumes; NOT power-law tails)** — the audit itself still
waits for the owner's ratification, per protocol.

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The leaked-records sample is one old exchange; the
authors' own robustness sections flag definitional sensitivity
(alternative wash-trading definitions, PDF pp. 67-79); and the
working-paper pagination differs from the Management Science
published version — page cites here refer to the DORAS copy in
`docs/library/text/`, and the published version should be checked
before formal citation.
