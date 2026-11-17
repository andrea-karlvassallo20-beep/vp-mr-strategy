# T2 addendum: the recommendation re-examined after T1's sign inversion

**Date:** 2026-11-16. **For the owner.** This addendum does not change the
standing recommendation — it hardens it, and it names one thing that must
happen BEFORE T2 is ever run, while it is still legal to do so.

## The standing recommendation (unchanged)

`paper/research/t1_t2_decision_memo_2026-11-16.md` recommended: **run T1,
hold T2** until full L2, because T2's Hawkes channels (cancellations, the
passive side) do not exist in aggTrades. T1 has now run and survived with
its mechanism's sign inverted (see
`paper/research/phase2_l2/t1_second_window_review_2026-11-16.md`). The
inversion STRENGTHENS the hold recommendation: it is direct evidence that
taker-only data can carry real, vol-robust information about the hazard
while pointing the wrong way for the story — the passive side is where
the sign gets resolved, and T2 on aggTrades is blind to it by
construction.

## The gap T2 shares with T1 (named while it is still fixable)

T2's registered mechanism is directional: *"persistent one-sided taker
aggression ... reflects informed sweep accumulation before price
displaces"* — buy-aggression should predict up. But its kill lines test
only **separation from the coin-flip band** [0.497, 0.513] and placebo
reproduction. None of them fires if the skill is real but the direction
is INVERTED (buy-aggression predicting down with skill would "survive").
That is precisely the ambiguity T1 just landed in, and the C1-L2 spec
has since gained its sign guard (kill line 6, PR #140).

**Proposed prospective amendment to T2's contract** — legal now, because
no T2 result exists:

> T2 SIGN GUARD: the directional skill must be on the side the mechanism
> states — P(up | buy-aggression) > 0.513 with the sell-aggression
> mirror < 0.487. A skilled result on the wrong side is booked
> "mechanism-refuted (sign)," exactly as T1 was — informative, not a
> pass for the story.

If the owner accepts the template-level sign-kill-line rule (pending),
this is simply its application to T2; it can be written into
`src/run_taker_falsification.py`'s T2 contract in one commit, before any
run.

## Why T2 on aggTrades, even sign-guarded, is still LOW value

- The passive-withdrawal mechanism — the actual SMH story — is
  invisible in taker prints (CKS's own words, carried in the deep-reads).
- T1's inversion gives a live, concrete precedent for a taker-side
  result that is real but story-inverted.
- Full L2 unlocks the cancellation channels T2's 2D Hawkes design
  actually wants; running it earlier spends a pre-registration on a
  half-blind instrument.

**Recommendation: HOLD T2. If it is ever run on aggTrades anyway, add the
sign guard first. The L2 version of T2 is the one worth its
pre-registration.**
