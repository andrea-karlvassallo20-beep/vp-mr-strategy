# SMH Presence Indicator v0.1 — Pine port (declared UNTESTED in
# Pine; the Python core in `src/smh_presence.py` is the
# replication-grade reference and was run clean on the archive)

Written 2026-11-18 at the owner's request ("why not try and make
your own indicator, or improve on mine or try go flip a coin").
This is the program's own indicator: the owner's AVFI/VPVI lineage
composed with the four measured dossiers (closeness 34, coin-chip
37, VFI-extremity 40, fade-layer 42). Every constant below is
REGISTERED from a measured dossier, not tuned: 20d/756d/252d/23d
windows from the dossiers; the base gate rvol_pct <= 33 and
range_pos <= 0.15 (chip .645); the VFI bottom-decile gate pct <= 10
(chip .686) — the session-42 amendment replacing the owner's
median sign gate; the 20-bar fresh-extreme triggers (arrival
1.6-1.8x); the >=4-sigma nuke chips (.748 down / .767 up); the
composed base x vfi-extremity NEAR state (arrival 1.9x, chip
.601). Discipline: INDICATOR, not strategy — no equity curve, no
win rate, no backtest stats; every number is a discovery-panel
conditional, W2 confirmation pending; nothing armed; nothing here
is live advice. Daily bars are the measured grain (the archive);
weekly re-instantiation is a different construction and its
confirmation is a named follow-up. Copy the code below into
TradingView (v5, daily chart).

```pine
//@version=5
indicator("SMH Presence v0.1 [measured constants]", shorttitle="SMH P v0.1", overlay=false, precision=3, max_bars_back=800)

// ═══ Registered constants (measured dossiers 34/37/40/42; do not tune) ═══
SIG_WIN   = 20     // sigma + rvol window (sessions 34/37)
PCT_WIN   = 756    // percentile window
RNG_WIN   = 252    // range window
VOL_MA    = 23     // VFI volume MA (session 40 construction)
Z_WIN     = 252    // VFI z window
PB_N      = 20     // fresh-extreme lookback (session 42)
RVOL_MAX  = 33.0   // quiet + base gate
RPOS_MAX  = 0.15   // base-of-range gate
EXT_PCT   = 10.0   // VFI bottom-decile gate (session 42 amendment)
NLBL      = 2      // nuke lookback (days)

// ── quietness: 20d vol percentile in 756d ─────────────────────
ret = ta.change(close) / close[1]
// (Pine lacks rolling-rank; approximate the percentile by the
// fraction of the prior days whose 20d rvol is below the current
// one — declared approximation; window capped at 200 for load.)
rv20   = ta.stdev(ret, SIG_WIN)
below  = 0.0
for i = 1 to 200 by 1
    below += (rv20[i] < rv20 ? 1.0 : 0.0)
rvol_den = math.min(PCT_WIN, bar_index - 1)
rvol_pct = 100.0 * below / rvol_den

// (full 756-wide percentile loop is heavy in Pine; this v0.1 uses
// a declared 200-bar approximation of the percentile window -
// the Python core is exact and authoritative.)

// ── position in the 252d range ────────────────────────────────
hi = ta.highest(close, RNG_WIN)
lo = ta.lowest(close, RNG_WIN)
range_pos = (close - lo) / math.max(hi - lo, 1e-10)

// ── VFI (session-40 construction) and its bottom-decile gate ──
vol_ok = not na(volume) and volume > 0
vol_ma = ta.sma(volume, VOL_MA)
v_flow = vol_ok ? math.min(volume / math.max(vol_ma[1], 1e-10) - 1.0, 3.0) : 0.0
gate_up = close >= close[1] * 1.01
gate_dn = close <= close[1] * 0.99
vfi_raw = v_flow * (gate_up ? 1.0 : gate_dn ? -1.0 : 0.0)
vfi = ta.cum(vfi_raw)
vfi_z = (vfi - ta.sma(vfi, Z_WIN)) / math.max(ta.stdev(vfi, Z_WIN), 1e-10)
// bottom-decile status of vfi_z within its recent distribution:
belowz = 0.0
for i = 1 to 100 by 1
    belowz += (vfi_z[i] < vfi_z ? 1.0 : 0.0)
belowz_den = rvol_den
vfi_pct = 100.0 * belowz / belowz_den
vfi_ext_low = vfi_pct <= EXT_PCT

// ── presence / near / comp ────────────────────────────────────
quiet = rvol_pct <= RVOL_MAX
base = quiet and range_pos <= RPOS_MAX
low_vol_20 = ta.sum(rvol_pct <= RVOL_MAX ? 1 : 0, SIG_WIN)
comp = low_vol_20 >= 20
presence = base
near = presence and vfi_ext_low

// ── fresh extremes + nukes (sessions 37/42) ───────────────────
fresh_low = close <= ta.lowest(close, PB_N)
fresh_high = close >= ta.highest(close, PB_N)
sig20 = ta.stdev(ret, SIG_WIN)
nuke_dn = ta.barssince(ret <= -4.0 * sig20) <= NLBL
nuke_up = ta.barssince(ret >=  4.0 * sig20) <= NLBL

// ── registered chip (dossiers 37/40/42; P(first 4-sigma move up)) ─
chip = near ? 0.601 : presence ? 0.645 : vfi_ext_low ? 0.686 : nuke_dn ? 0.748 : nuke_up ? 0.767 : 0.576

// ── plots ─────────────────────────────────────────────────────
plot(rvol_pct, "Quietness pct (lower=closer)", color=color.new(color.teal, 0))
plot(range_pos, "Range position", color=color.new(color.gray, 40))
hline(33.0, "quiet gate", color=color.gray, linestyle=hline.style_dashed)
bgcolor(near ? color.new(color.lime, 78) : presence ? color.new(color.green, 90) : na, title="Presence")
bgcolor(nuke_dn and not near ? color.new(color.red, 85) : na, title="Nuke (down)")
plotshape(vfi_ext_low, "flow extremity (bottom decile)", shape.circle, location.bottom, color.new(color.aqua, 20), size=size.tiny)
plotshape(fresh_low, "fresh 20d low", shape.triangleup, location.bottom, color.new(color.lime, 30), size=size.tiny)
plotshape(fresh_high, "fresh 20d high", shape.triangledown, location.top, color.new(color.red, 30), size=size.tiny)

// ── state table (last bar) ────────────────────────────────────
var table t = table.new(position.top_right, 2, 7)
if barstate.islast
    table.cell(t, 0, 0, "SMH PRESENCE v0.1", text_color=color.white, bgcolor=color.black)
    table.cell(t, 1, 0, "paper only", text_color=color.white, bgcolor=color.black)
    table.cell(t, 0, 1, "quiet pct", text_color=color.silver); table.cell(t, 1, 1, str.tostring(rvol_pct, "0.#"), text_color=color.white)
    table.cell(t, 0, 2, "range pos", text_color=color.silver); table.cell(t, 1, 2, str.tostring(range_pos, "0.00"), text_color=color.white)
    table.cell(t, 0, 3, "state", text_color=color.silver)
    table.cell(t, 1, 3, near ? "NEAR (x1.9 arrive)" : presence ? "PRESENCE" : nuke_dn ? "post-nuke down" : nuke_up ? "post-nuke up" : "flat", text_color=color.white, bgcolor=near or presence ? color.new(color.green, 50) : na)
    table.cell(t, 0, 4, "chip (P(first big move up))", text_color=color.silver)
    table.cell(t, 1, 4, str.tostring(chip, "0.000") + "  [W2 pending]", text_color=color.white)
    table.cell(t, 0, 5, "fresh extremity", text_color=color.silver)
    table.cell(t, 1, 5, fresh_low ? "20d LOW" : fresh_high ? "20d HIGH" : "—", text_color=color.white)
    table.cell(t, 0, 6, "reminder", text_color=color.silver)
    table.cell(t, 1, 6, "times the FIRST BIG MOVE; not drift; nothing live", text_color=color.orange)

// W2 confirmation pending; discovery-panel conditionals only; the
// Python core (src/smh_presence.py) is exact and authoritative.
// © Mozilla Public License 2.0; SMH programme, 2026-11-18.
```

## Honest boundaries (read before using)

- Every chip number is a DESCRIPTIVE discovery-panel conditional
  awaiting W2 confirmation — printed to keep them from being read
  as validated probabilities.
- The Pine percentile loops are short-window approximations
  (200-bar) to keep the script light; the Python core is exact.
- The chip is a LEAN; the instrument times the first big move,
  never a drift (medians are negative on the panel).
- Indicator, not strategy: no equity curve, no win rate; nothing
  armed; nothing trades live; no live advice.

---

# SECTION: The SMH presence thesis — one page

## What the Salient Market Hypothesis says, operationally

Big moves are not uniformly distributed in time. They arrive out
of identifiable PRE-STATES — measurable nightly conditions that
concentrate their arrival and tilt their direction — and the
honest instrument refuses direction certainty while timing the
move and riding its measured lean. The thesis is encoded in the
program's own vocabulary: inevitabilities. Be there when the
inevitable arrives; the coin is up-chipped, and the chips are
measurable.

## The four measured dossiers this instrument is made of

1. **Closeness (measured session 34):** quietness ranks distance-
   to-event (AUC 0.323 at 5 days — the dominant criterion);
   position-in-range second (~0.45); compression mild (~0.54);
   daily volume ratios carry ~nothing. LOWER quietness = closer.
2. **The coin's chips (session 37):** P(first big move within 60d
   is UP): baseline .576; after a >=4-sigma DOWN day **.748**;
   after a big UP day **.767**; "a base is built" (quiet + bottom
   of range) **.645** with the largest 60d mean drifts; medians
   NEGATIVE — the chips live in first-move direction, not drift.
3. **The owner's flow extremities (session 40):** VFI bottom-
   decile nights carry a **+10-point** chip (.686) and see moves
   ~34% sooner; the VFI LEVEL is a state marker, NOT a timing
   rank (AUC ~.50). The owner's instinct, quantified.
4. **The fade layer (session 42):** fresh 20-bar lows/highs are
   the arrival accelerators (1.6-1.8x); the median flow gate of
   the owner's H8 subtracts; the bottom-decile gate is the
   registered amendment; their divTop is a measured EXHAUSTION
   (exit) state at .481.

## The verdict ladder (the instrument's whole logic)

| State | What it means | Registered numbers |
|---|---|---|
| **PRESENCE** | quiet + base of range — the timing seat | chip .645, arrival 1.6x |
| **NEAR** | presence x VFI bottom-decile | chip .601, **arrival 1.9x (.094/5d)** |
| **post-nuke** | 4-sigma day within 2 days | chips .748 (down) / .767 (up) |
| no state | flat | baseline .576 / .0497 |

## The one sentence

> Be present in the quiet base; when the flow marks its bottom-
> decile extremity there, the move is roughly twice as near; the
> first big move leans UP 60-65% (74-77% from nukes); the divTop
> fade marks the other end; and the entire structure is a
> discovery-panel conditional awaiting its W2 confirmation — a
> lean, not a promise, timed at the first big move, never a drift.

For the LLM-assessment form of this thesis, see
`smh_longs_prompt.md` (v1) in this directory; for the exact
computation, `src/smh_presence.py`; the live board,
`paper/research/clue_scan/smh_presence_scan.csv`.
