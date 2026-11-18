# The chip stability split — do the measured chips survive a
# temporal split of the archive? (the "works only once" experiment)

Status: MEASURED DESCRIPTIVE work, owner-authorized 2026-11-18,
sixth measured session of the parallel regime. Protocol
pre-declared in `src/chip_stability_split.py`: each series' valid
nights split at its own midpoint; the session-37/40/42 chips
recomputed per half. Descriptive robustness pass — NOT W2; no
kill line moved; nothing armed; nothing trades live.

## 1. The results (P(first big move within 60d is UP), per half)

| state | half 1 | n (h1) | half 2 | n (h2) | verdict |
|---|---|---|---|---|---|
| all nights | 0.556 | 67,917 | 0.599 | 60,733 | up-chip in BOTH halves, GROWING |
| **nuke_down** | **0.703** | 925 | **0.801** | 780 | **STABLE — strengthener** |
| **nuke_up** | **0.738** | 1,098 | **0.802** | 1,002 | **STABLE — strengthener** |
| base | 0.707 | 75 | 0.645 | 14,974 | structurally unsplittable (see §2) |
| vfi_ext_low | — | 0 | 0.686 | 7,304 | structurally unsplittable |
| near | — | 0 | 0.601 | 2,752 | structurally unsplittable |

(P_move5 columns in `chip_stability_split.csv`; see the caution
on nuke-state episode contamination below.)

## 2. The two honest structural findings

1. **The NUKE chips survive the temporal split — the first
   conditional in the program to "work" in two independent
   halves of the archive.** After-crash nights: 70.3% first-move
   UP in the earlier half, 80.1% in the later; after-big-up
   nights: 73.8% / 80.2% — both chips exceed the (growing)
   baseline by double digits in BOTH halves, and both are
   STRONGER in the more recent half. This is the owner's
   "after nukes highest likelihood to go up," now stability-
   passed intra-archive. It remains a descriptive conditional:
   confirmation on fresh data (W2) is still mandatory — but as
   of this run, the nuke chip is the program's best candidate
   for "something that works."
2. **The base / flow-extremity / NEAR states CANNOT be
   temporally split within this archive — their constructions
   have structural burn-in.** The VFI's trailing-756d percentile
   needs its own 252d z-history first, so valid vfi_ext_low
   nights exist only in the later portion of most series (h1
   n = 0-75 vs h2 n = 2,752-14,974): their half-1 cells are
   empty or junk, and this is a STRUCTURAL statement, not a
   stability failure. Honest consequence: the presence/NEAR
   skeleton's confirmation cannot come from this archive at all
   — it must come from FRESH windows (W2), which is already the
   registered requirement.
3. (Caution, declared): the nuke-state P_move5 cells (0.26-0.33)
   include continuation moves of the SAME post-crash episode —
   the arrival concentration is partly the episode itself; the
   direction chips are the stable content, the arrival cells
   carry episode contamination and are not treated as
   independent-event evidence.

## 3. The reading

The owner asked to "find something that works only once." As of
this session: the strongest verified-artifact finding in the
whole program — the nuke chip — now has intra-archive temporal
stability: two independent halves, 70-80% first-move-up after
crash days, growing stronger in recent history, against a
baseline that itself rose from 0.556 to 0.599. The presence/NEAR
skeleton remains the timing instrument but requires fresh-window
confirmation by construction. Nothing is armed. W2 remains
mandatory for everything. Nothing trades live.

## 4. Reproduction

`python3 src/chip_stability_split.py` →
`chip_stability_split.csv` (this document).
