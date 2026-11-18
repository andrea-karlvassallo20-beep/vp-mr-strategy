# Exploratory probe E1: volume conservation as a depth-reconstruction admissibility rule

[exploratory] Null-time session 21, 2026-11-18. Exploratory probe E1 under
the ratified exploratory channel (docs/exploratory_channel.md). Read against
the programme's ONE question: what here would kill C1-L2 or C8 faster, or
change their kill lines? Anchors: the owner's question about volume-flow
physics and conservation mathematics (chat, 2026-11-18), the
Huang-Rosenbaum moving-frame representation (deep-read 18), and own
derivation (the flux map below). Nothing was measured; no data was touched;
L2 is still awaited.

## The import, honest version: conservation-law bookkeeping

The finite-volume method from computational physics is flux-differencing
bookkeeping on a discretized domain: cells, face fluxes, balance laws,
declared boundary conditions and declared source terms. The limit order book
is exactly such a domain. Cells are price levels on a fixed absolute grid,
storage is the posted depth q_i(t) at level i, and the tape events are the
face fluxes. The discrete conservation identity needs no continuum
idealization and no physics metaphor: the tape IS q-dot, the balance law IS
the exact integral form, and the finite-volume view supplies nothing but
correct bookkeeping and honest boundary discipline.

## The identity (own derivation, pre-registered here)

On a fixed absolute price grid, for any level i and any window
(t1, t2], with reconstruction built only from the event tape:

  q_i(t2) - q_i(t1)
      = sum of signed event volumes at level i in (t1, t2]
        + boundary flux terms (events beyond the tracked K-level window)
        + source terms (venue-attributed liquidity changes: hidden-size
          adds/withdrawals, administrative corrections; declared per venue)

Event-to-flux map, declared once per venue before any run: limit insertion
+v at level i; cancellation -v at level i; execution -v at the resting
side of the fill; modification orders split into cancellation + insertion
per the declared engine convention. Hidden liquidity appear/disappear are
source terms, never silently absorbed into fluxes.

## Why this matters for C1-L2 and C8's L2 arm

OFI, queue-imbalance, and depth-aggregated flow features are computed from
reconstructed depth. The classic fatal bugs are gross reconstruction
failures: double-counted executions, feed gaps, timestamp misalignment
between stream types, wrong-side assignment, silent re-injection of missed
messages. Every one of them shows up as a conservation violation at some
level-window, and none of them is reliably caught by schema checks alone.
The identity is bug-catching machinery for the point-in-time-safe pipeline
layer: any window used in a C1-L2 or C8 L2-arm measurement should have to
prove its depth was internally consistent first.

## Output: ONE candidate sharpening queued, PENDING OWNER RATIFICATION

The volume-conservation reconstruction-admissibility rule: any depth
reconstruction used in a C1-L2 (or C8 L2-arm) measurement must pass the
flux-differencing identity per level per window, within a tolerance and a
source-term budget that are BOTH pre-registered before the first L2 run, and
calibrated on a calibration window DISJOINT from every evaluation window the
features are scored on. Windows that fail are inadmissible, and the log of
which windows failed travels with the measurement. This is harder to pass
than the standing protocol: windows that would today silently enter a
measurement with corrupted depth are excluded before any statistic is
computed. It changes no kill line and defines no signal.

## Caveats

- Venue feed semantics must be encoded per venue in the event-to-flux map;
  an unspecified map makes the rule inapplicable, not lenient.
- The tolerance must never be tuned on evaluation windows; tuning-set
  separation is part of the rule.
- This probe shipped zero data work: it is a proposal for validation
  machinery only. No empirical claim in this note supports any programme
  claim, and none may be cited as confirmatory later.
- Negative-results standard: if, once L2 arrives, the identity passes
  trivially everywhere, that is an honest finding of a weak check, to be
  logged as such, not oversold.

Nothing measured, no kill line moved, nothing armed, nothing trades live.
