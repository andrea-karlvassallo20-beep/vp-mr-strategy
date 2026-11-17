"""CKS average-depth normalization — kill line 7(b) implementation.

Transcribed LITERALLY from the Cont-Kukanov-Stoikov deep-read
(docs/library/cks_ofi_review.md, sibling S1) and pre-declared in
paper/research/c1_l2_test_spec.md kill line 7(b):

    AD_i = (1 / (2 (N(T_i) - N(T_{i-1}) - 1))) * sum(q^B_n + q^A_n)

BOTH sides summed over the interval's events, divided by 2(N-1), NOT 2N.
The -1 is CKS's own and is load-bearing: N-1 consecutive differences exist
between N events. An implementation that divides by the event count N, by
one side only, or by the last snapshot depth silently rescales the impact
coefficient — the exact defect class this module exists to prevent.

KILL LINE 7(b) ENFORCEMENT: an implementation failing the unit test
(tests/test_ck_average_depth.py, hand-built 3-event interval) cannot
run on Tardis data. Single-event intervals have a zero denominator
(undefined average depth) and RAISE here — the caller must merge
intervals explicitly; NaN would silently propagate and that is the
silent-degradation failure mode this repo has already paid for once.
"""

import pandas as pd


def average_depth(events: pd.DataFrame) -> float:
    """CKS average depth over ONE interval of book events.

    events: frame with one row per book event inside the interval
    (T_{i-1}, T_i], columns `bid_depth` and `ask_depth` (sizes at the
    top of each side at the event).

    Returns the literal CKS quantity: sum of BOTH sides across the
    interval's events divided by 2(N-1), where N is the event count.
    Raises ValueError for N < 2 (denominator zero: undefined) or for
    missing/invalid depth columns.
    """
    required = {"bid_depth", "ask_depth"}
    if not required.issubset(events.columns):
        raise ValueError(f"events missing columns: {required - set(events.columns)}")
    n = len(events)
    if n < 2:
        raise ValueError(
            f"average depth undefined for {n} event(s): denominator 2(N-1) is "
            f"zero or negative; merge the interval with a neighbor explicitly"
        )
    both_sides = (events["bid_depth"] + events["ask_depth"]).sum()
    return float(both_sides / (2 * (n - 1)))


def depth_normalized_ofi(ofi: float, events: pd.DataFrame) -> float:
    """OFI for one interval normalized by the literal CKS average depth.

    Any depth-normalized OFI feature used by the C1-L2/C5/C6 layer must
    go through this function (or average_depth directly) so the
    denominator cannot drift from the pre-declared transcription.
    """
    ad = average_depth(events)
    if ad <= 0:
        raise ValueError(f"average depth {ad} is non-positive; OFI normalization undefined")
    return float(ofi) / ad
