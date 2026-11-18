# The VFI-extremity dossier — the owner's own method, encoded and
# measured against the program's current best criteria

Status: MEASURED DESCRIPTIVE work, owner-authorized 2026-11-18
("me marking extremities on VFI is the best I could do, you are
here to find even better and the right way to do it, but you
gotta find it"). Third measured session of the parallel regime.
The owner's method was encoded BEFORE the run (Fedenko-style VFI:
gated 23d volume-ratio flow cumulated, z-scored against the prior
252 days, extremities = bottom/top decile of the trailing 756-day
percentile; full declared construction in `src/vfi_extremity_dossier.py`).
Descriptive on the discovery archive; W2 confirmation mandatory
before anything becomes evidence. No kill line moved; nothing
armed; nothing trades live.

## 1. What was asked of the owner's method

- Q1 (closeness): does VFI rank nights by distance-to-move?
- Q2 (chip): does a VFI extremity change which way the first big
  move goes, and how soon it arrives?
- Q3 (additivity): does VFI add information on top of the
  program's best state (quiet + base-of-range)?

## 2. The results

**Q1 — closeness: NO.** AUC of vfi_z against ">=4-sigma move
within K days": 0.499 (K=5), 0.494 (K=20), 0.510 (K=60) — coin
flip at every horizon (context: quietness rvol_pct reads 0.323 at
K=5). On base-state nights it adds nothing either (0.48-0.49).
The owner's read is NOT a continuous timing signal: VFI's level
does not rank nights by distance to the event.

**Q2 — chip: YES, real and specific to the LOW tail.**
| state | P(first big move UP) | P(move within 5d) |
|---|---|---|
| all nights | 0.585 | 0.050 |
| **VFI low extremity** | **0.686** | **0.067** |
| VFI high extremity | 0.558 | 0.041 |
| base (quiet + low range) | 0.644 | 0.082 |
| **low extremity x base** | 0.601 | **0.094** |
| high extremity x base | 0.737 (n=510 — small sample, flagged) | 0.057 |

- The LOW extremity state carries a +10-point chip (68.6% vs
  58.5%, n = 7,304) — a direction chip the HIGH extremity does
  not carry (55.8%). The owner's instinct for marking extremities
  is measurably right on the LOW side.
- Low-extremity nights also see moves arrive sooner (6.7% within
  5 days vs 4.97% baseline, +34 percent) — a state effect, not a
  ranking effect: the extremity TAIL is informative even though
  the VFI LEVEL is not (Q1 and Q2 are both true, different
  objects).

**Q3 — composition, and the "better way" the owner asked for.**
The single best NEAR-TERM arrival state measured on this archive
is the owner's own read COMPOSED with the program's:
**VFI low extremity x quiet-base = 9.43 percent of moves arrive
within 5 days, 1.9x the baseline** — the highest P(move within
5d) of any state measured to date, above base alone (8.17%).
Its direction chip is weaker (0.601 vs base's 0.644), so the
composition trades a little direction for a lot of timeliness.
(The high-extremity-x-base cell reads 0.737 but on n = 510 —
recorded, flagged small, not trusted until confirmation.)

## 3. The honest verdict on "find the better way"

The better way is not a replacement of the owner's read — it is
the owner's read IN THE RIGHT SEAT: VFI extremities are a STATE
marker (they change which nights you are on and tilt direction at
the low tail), while quietness+base remains the TIMING criterion
(it ranks closeness). The composed rule — quiet + base-of-range,
with VFI-low-extremity as a near-term amplifier — is the best
measured instrument skeleton so far:

  be in the base when quiet; when VFI marks a low extremity
  there, the move is ~2x nearer; the first big move leans UP at
  60-65 percent depending on which legs fired.

Descriptive discovery-panel numbers: crypto-heavy archive, the
VFI construction is one declared instantiation (Fedenko gate,
23d/252d/756d windows — a different instantiation is a different
construction, per the estimator-mode rule); the 0.737 cell is
small-sample; W2 confirmation on fresh windows is mandatory
before any of this becomes evidence; no threshold chosen here;
nothing armed; nothing trades live.

## 4. Reproduction

`python3 src/vfi_extremity_dossier.py` →
`vfi_extremity_dossier.csv` (this document:
`vfi_extremity_dossier.md`).
