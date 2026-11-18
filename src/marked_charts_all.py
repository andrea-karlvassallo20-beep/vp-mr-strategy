"""ALL-UNIVERSE marked charts + notes (owner-directive: "do this for
all 250 charts until you finish, with notes of relative position of
vfi to price, sequentiality of historical vfi across zones below 0
above 0 extremity below extremity above etc and when a trade for a
long or short is best to be made (at extremities with declining
effort or coiled effort)").

Per pair (min 310 bars for the z axis; shorter pairs recorded as
insufficient in the index):
  CHART (144 bars): price panel with grammar leg shading (U-base /
  V-spike / even), fresh-low-at-lows ^, absorption o at lows,
  fresh-high-at-highs v, VFI zero-cross-up blue markers; VFI panel
  bars colored by sign with zone bands: XB (z<=-1.5 extremity
  BELOW), B (-1.5..0), A (0..1.5), XA (z>=1.5 extremity ABOVE).
  NOTES (in the index table):
    pos_rel: price range_pos x vfi zone ("price 4% of range BOTTOM;
      flow A (above zero, mid); flow ABOVE price's extreme read").
    seq: the compressed zone-run sequence of the last 144 bars,
      e.g. "XB:9>B:31>A:58>XA:12>A:34".
    seg_age: days since the current positive-segment opened
      (flow-age axis: young segments carry the first-half 0.720;
      old ones the second-half 0.550).
    coil: rvol percentile at lows (the presence seat's "coiled
      effort"); declining-effort flags at tops (z falling out of XA).
    read: the LONG/SHORT seat observation (NOT advice): LONG-SEAT
      cells = bottom-range + fresh lows + (washout flow OR young
      segment OR recent absorption at lows); SHORT-WATCH = top-range
      + flow fading from extremity above or divTop; else "-".
All observation display; nothing armed; nothing trades live.
"""
import csv
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from chart_grammar_dossier import pivots_legs

FRESH = Path("paper/research/data_fresh")
OUT = Path("paper/research/clue_scan/charts")
IDX = Path("paper/research/clue_scan/charts/CHART_INDEX.md")
BARS = 144
VOL_MA, Z_WIN, PCT_WIN = 23, 252, 756
SIGMA_WIN, FRESH_WIN = 20, 20
MIN = 310


def flow_axis(close, volume):
    v = (volume / volume.shift(1).rolling(VOL_MA).mean()
         .replace(0, np.nan) - 1.0).clip(0, 3.0).fillna(0.0)
    up_g = (close >= close.shift(1) * 1.01).astype(float)
    dn_g = (close <= close.shift(1) * 0.99).astype(float)
    vfi = (v * (up_g - dn_g)).cumsum()
    z = ((vfi - vfi.rolling(Z_WIN).mean())
         / vfi.rolling(Z_WIN).std().replace(0, np.nan)).clip(-10, 10)
    return z


def zone(zv):
    if zv >= 1.5:
        return "XA"
    if zv >= 0:
        return "A"
    if zv > -1.5:
        return "B"
    return "XB"


def main():
    notes = []
    short = []
    for f in sorted(FRESH.glob("*.csv")):
        df = pd.read_csv(f).reset_index(drop=True)
        if len(df) < MIN:
            short.append(f.stem)
            continue
        for c in ("open", "high", "low", "close", "volume"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
        close = pd.Series(df["close"].to_numpy(), dtype=float)
        volume = pd.Series(df["volume"].to_numpy(), dtype=float)
        ret = close.pct_change()
        sigma = ret.rolling(SIGMA_WIN).std().shift(1)
        rho = volume / volume.shift(1).rolling(VOL_MA).mean()
        zres = (ret / sigma).abs()
        absorbing = (rho >= 1.5) & (zres <= 0.5)
        rng_hi = close.rolling(252).max()
        rng_lo = close.rolling(252).min()
        rp = ((close - rng_lo) / (rng_hi - rng_lo)
              .replace(0, np.nan))
        fresh_lo = close == close.rolling(FRESH_WIN).min()
        fresh_hi = close == close.rolling(FRESH_WIN).max()
        rvol = ret.rolling(SIGMA_WIN).std()
        rvol_pct = rvol.rolling(PCT_WIN).rank(pct=True) * 100.0
        z = flow_axis(close, volume)
        v_pct = z.rolling(PCT_WIN).rank(pct=True) * 100.0

        n = len(df)
        i0 = n - min(BARS, n)
        x = np.arange(n - i0)
        z_a = z.to_numpy()
        cl = close.to_numpy()
        dn = df["date"].to_numpy()
        rp_a = rp.to_numpy()
        fl = fresh_lo.to_numpy()

        # sequence string (zone runs over the plotted window)
        seq = []
        last = None
        run = 0
        for i in range(i0, n):
            zv = z_a[i]
            if not np.isfinite(zv):
                continue
            g = zone(zv)
            if g == last:
                run += 1
            else:
                if last is not None:
                    seq.append(f"{last}:{run}")
                last, run = g, 1
        if last is not None:
            seq.append(f"{last}:{run}")
        seq_str = ">".join(seq)

        # segment age: days since last zero-cross up
        seg_age = ""
        for i in range(n - 1, max(n - 400, 1), -1):
            if np.isfinite(z_a[i]) and z_a[i] >= 0 > z_a[i - 1]:
                seg_age = n - 1 - i
                break
        # effort notes
        rp_end = rp_a[-1] if np.isfinite(rp_a[-1]) else np.nan
        z_end = z_a[-1] if np.isfinite(z_a[-1]) else np.nan
        vp_end = v_pct.iloc[-1]
        rv_end = rvol_pct.iloc[-1]
        abs_low_recent = bool(absorbing.iloc[-5:].any()
                              and rp_end <= 1 / 3)
        # declining effort from extremity above within last 10 bars
        decl_top = False
        for i in range(n - 1, max(n - 11, 1), -1):
            if (np.isfinite(z_a[i]) and z_a[i] < z_a[i - 1]
                    and z_a[i - 1] >= 1.5 and rp_end >= 2 / 3):
                decl_top = True
                break
        coil = (np.isfinite(rv_end) and rv_end <= 33
                and rp_end <= 0.33)
        young_seg = (isinstance(seg_age, int) and seg_age <= 30)
        reads = []
        if (np.isfinite(rp_end) and rp_end <= 0.25
                and (fl[-1]
                     or (np.isfinite(vp_end)
                         and vp_end <= 10.0) or abs_low_recent
                     or young_seg and fl[-1])):
            reads.append("LONG-SEAT (bottom-extreme flow read)")
        if decl_top or (np.isfinite(rp_end) and rp_end >= 0.80
                        and np.isfinite(vp_end) and vp_end >= 90):
            reads.append("SHORT-WATCH (top, flow fading from"
                         " extremity)")
        read = " + ".join(reads) if reads else "-"

        pos_rel = (f"price {round(float(rp_end) * 100)}% of range"
                   f" at {zone_lo_hi(rp_end)}; flow {zone(z_end)}"
                   f" ({round(z_end, 2) if np.isfinite(z_end) else 'na'}"
                   f" z)")

        # chart
        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(13, 7.5), sharex=True,
            gridspec_kw={"height_ratios": [2.4, 1]})
        ax1.plot(x, cl[i0:], color="#1b1b1b", lw=1.4)
        legs = pivots_legs(df["high"].to_numpy(),
                           df["low"].to_numpy(), cl,
                           sigma.to_numpy())
        for lg in legs:
            a, b = lg["i1"], lg["i2"]
            if b < i0:
                continue
            col = {"b": "#2e9e4f", "f": "#d1493a",
                   "e": "#b9b9b9"}[lg["sym"][3]]
            ax1.axvspan(max(a, i0) - i0, b - i0, color=col,
                        alpha=0.12, lw=0)
        for i in range(i0, n):
            k = i - i0
            rp_i = rp_a[i] if i < len(rp_a) else np.nan
            if fl[i] and np.isfinite(rp_i) and rp_i < 0.35:
                ax1.scatter(k, cl[i] * 0.97, marker="^", s=42,
                             color="#1a7a34", zorder=5)
            if absorbing.iloc[i] and np.isfinite(rp_i) \
                    and rp_i <= 1 / 3:
                ax1.scatter(k, cl[i] * 0.94, marker="o", s=34,
                            color="#7a3fd1", zorder=5)
            fh = fresh_hi.to_numpy()
            if fh[i] and np.isfinite(rp_i) and rp_i > 0.8:
                ax1.scatter(k, cl[i] * 1.03, marker="v", s=42,
                            color="#a01414", zorder=5)
            if np.isfinite(z_a[i]) and i > 0 and z_a[i] >= 0 > z_a[i - 1]:
                ax2.scatter(k, 0.15, marker="o", s=38,
                             color="#1454c4", zorder=6)
                ax1.axvline(k, color="#1454c4", lw=0.7, alpha=0.5)
        zz = np.nan_to_num(z_a[i0:], nan=0.0)
        cols = ["#1a7a34" if zz[k] >= 0 else "#a01414"
                for k in range(len(zz))]
        ax2.bar(x, zz, color=cols, alpha=0.75, width=1.0)
        ax2.axhline(0, color="#1b1b1b", lw=1)
        for lvl in (1.5, -1.5):
            ax2.axhline(lvl, color="#7a3fd1", lw=0.8, ls="--")
        # zone bands on vfi panel
        for i in range(i0, n):
            zv = z_a[i] if np.isfinite(z_a[i]) else 0.0
            g = zone(zv)
            if g in ("XB", "XA"):
                ax2.axvspan(i - i0, i - i0 + 1,
                            color="#1454c4", alpha=0.15, lw=0)
        step = max(len(x) // 8, 1)
        ticks = np.arange(0, len(x), step)
        ax2.set_xticks(ticks)
        ax2.set_xticklabels([str(dn[j]) for j in ticks + i0],
                            rotation=35, fontsize=7)
        ax1.set_ylabel("price")
        ax2.set_ylabel("VFI z")
        ax1.set_title(
            f"{f.stem[:-3].upper()} | legs: green=U-base, red=V-"
            f"spike | ^ fresh low @ lows, o absorption, v fresh high "
            f"@ highs | blue = zero-cross up | VFI zones XB/B/A/XA"
            f" (shaded blue = extremity)", fontsize=8)
        ax1.grid(alpha=0.18)
        ax2.grid(alpha=0.18)
        plt.tight_layout()
        plt.savefig(OUT / f"{f.stem}.png", dpi=100)
        plt.close(fig)

        notes.append({
            "pair": f.stem, "date": dn[-1],
            "pos_rel": pos_rel,
            "seq(144d)": seq_str,
            "seg_age_d": seg_age if seg_age != "" else "n/a",
            "coil_at_low": "yes" if coil else "-",
            "absorb_low_5d": "yes" if abs_low_recent else "-",
            "decl_effort_top": "yes" if decl_top else "-",
            "read": read,
        })
        print("chart:", f.stem)

    md = ["# The all-universe marked-chart index (all fetched pairs)",
          "",
          f"Charts rendered: {len(notes)}; insufficient history"
          f" ({MIN} bars min for the flow z axis): {len(short)}"
          " - recorded at the bottom. Markers/zones per chart header."
          " All observation display; nothing armed; nothing trades"
          " live; every seat chip remains W2-owing.", "",
          "| pair | date | position x flow | zone seq (144d) |"
          " seg age | coil | absorb | decl-top | read |",
          "|---|---|---|---|---|---|---|---|---|"]
    for n_row in notes:
        md.append(f"| {n_row['pair']} | {n_row['date']} "
                  f"| {n_row['pos_rel']} | {n_row['seq(144d)']} "
                  f"| {n_row['seg_age_d']} | {n_row['coil_at_low']} "
                  f"| {n_row['absorb_low_5d']} "
                  f"| {n_row['decl_effort_top']} | {n_row['read']} |")
    if short:
        md += ["", "Insufficient history for the z axis: "
               + ", ".join(short)]
    OUT.mkdir(parents=True, exist_ok=True)
    IDX.write_text("\n".join(md) + "\n")
    with open(OUT / "chart_notes.csv", "w", newline="") as fcsv:
        w = csv.DictWriter(fcsv, fieldnames=list(notes[0].keys()))
        w.writeheader()
        w.writerows(notes)
    print(f"done: {len(notes)} charts, {len(short)} short-history")


def zone_lo_hi(rp_end):
    if not np.isfinite(rp_end):
        return "n/a"
    if rp_end <= 1 / 3:
        return "LOW third"
    if rp_end >= 2 / 3:
        return "HIGH third"
    return "MID third"


if __name__ == "__main__":
    main()
