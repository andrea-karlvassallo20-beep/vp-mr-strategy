"""Marked charts for the owner: price panel + grammar legs + seat
markers, VFI(z) panel with the zero line and decile bands. 144
daily bars per chart (owner: "if 1356 is too long go for 144").
Output: paper/research/clue_scan/charts/<pair>.png. Observation
display only; nothing armed; nothing trades live."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from chart_grammar_dossier import pivots_legs

FRESH = Path("paper/research/data_fresh")
OUT = Path("paper/research/clue_scan/charts")
PAIRS = ["btcusd", "ethusd", "wbtcusd", "bonkusd", "jtousd",
         "atmusd", "apeusd", "crvusd"]
BARS = 144
VOL_MA, Z_WIN, PCT_WIN = 23, 252, 756
SIGMA_WIN, MOVE_SIGMA = 20, 4.0
FRESH_WIN = 20


def flow_axis(close, volume):
    v = (volume / volume.shift(1).rolling(VOL_MA).mean()
         .replace(0, np.nan) - 1.0).clip(0, 3.0).fillna(0.0)
    up_g = (close >= close.shift(1) * 1.01).astype(float)
    dn_g = (close <= close.shift(1) * 0.99).astype(float)
    vfi = (v * (up_g - dn_g)).cumsum()
    z = ((vfi - vfi.rolling(Z_WIN).mean())
         / vfi.rolling(Z_WIN).std().replace(0, np.nan)).clip(-10, 10)
    return z


def main():
    OUT.mkdir(exist_ok=True)
    for pair in PAIRS:
        f = FRESH / f"{pair}.csv"
        if not f.exists():
            continue
        df = pd.read_csv(f).reset_index(drop=True)
        if len(df) < PCT_WIN + 300:
            continue
        close = pd.Series(df["close"].to_numpy(), dtype=float)
        volume = pd.Series(df["volume"].to_numpy(), dtype=float)
        ret = close.pct_change()
        sigma = ret.rolling(SIGMA_WIN).std().shift(1)
        rho = volume / volume.shift(1).rolling(VOL_MA).mean()
        zres = (ret / sigma).abs()
        rng_hi = close.rolling(252).max()
        rng_lo = close.rolling(252).min()
        rp = (close - rng_lo) / (rng_hi - rng_lo).replace(0, np.nan)
        fresh_lo = close == close.rolling(FRESH_WIN).min()
        fresh_hi = close == close.rolling(FRESH_WIN).max()
        z = flow_axis(close, volume)
        absorbing = (rho >= 1.5) & (zres <= 0.5)

        legs = pivots_legs(df["high"].to_numpy(), df["low"]
                           .to_numpy(), df["close"].to_numpy(),
                           sigma.to_numpy())

        i0 = len(df) - BARS
        x = np.arange(BARS)
        cl = close.to_numpy()
        dn = df["date"].to_numpy()

        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(13, 7.5), sharex=True,
            gridspec_kw={"height_ratios": [2.4, 1]})
        ax1.plot(x, cl[i0:], color="#1b1b1b", lw=1.4,
                 label="close")
        # legs shading: back-loaded (U) bases green, front spikes red
        for lg in legs:
            a, b = lg["i1"], lg["i2"]
            if b < i0:
                continue
            aa, bb = max(a, i0) - i0, b - i0
            wake = lg["sym"][3]
            col = {"b": "#2e9e4f", "f": "#d1493a",
                   "e": "#b9b9b9"}[wake]
            ax1.axvspan(aa, bb, color=col, alpha=0.12, lw=0)
        for i in range(i0, len(df)):
            k = i - i0
            if fresh_lo.iloc[i] and (rp.iloc[i] < 0.35):
                ax1.scatter(k, cl[i] * 0.97, marker="^", s=42,
                            color="#1a7a34", zorder=5,
                            label="_")
            if absorbing.iloc[i] and (rp.iloc[i] <= 1 / 3):
                ax1.scatter(k, cl[i] * 0.94, marker="o", s=34,
                            color="#7a3fd1", zorder=5)
            if fresh_hi.iloc[i] and (rp.iloc[i] > 0.8):
                ax1.scatter(k, cl[i] * 1.03, marker="v", s=42,
                            color="#a01414", zorder=5)
        # VFI panel
        z_arr = z.to_numpy()
        zz = np.nan_to_num(z_arr[i0:], nan=0.0)
        colors = ["#1a7a34" if zz[k] >= 0 else "#a01414"
                  for k in range(BARS)]
        ax2.bar(x, zz, color=colors, alpha=0.75, width=1.0)
        ax2.axhline(0, color="#1b1b1b", lw=1)
        ax2.axhline(-1.5, color="#7a3fd1", lw=0.8, ls="--")
        ax2.axhline(1.5, color="#7a3fd1", lw=0.8, ls="--")
        # zero cross markers on both panels
        for i in range(i0 + 1, len(df)):
            if (np.isfinite(z_arr[i]) and z_arr[i] >= 0
                    > z_arr[i - 1]):
                k = i - i0
                ax2.scatter(k, 0.15, marker="o", s=38,
                            color="#1454c4", zorder=6)
                ax1.axvline(k, color="#1454c4", lw=0.7, alpha=0.5)
        step = max(BARS // 8, 1)
        ticks = np.arange(0, BARS, step)
        ax2.set_xticks(ticks)
        ax2.set_xticklabels([str(dn[j]) for j in
                             (ticks + i0)], rotation=35,
                            fontsize=7)
        ax1.set_ylabel("price")
        ax2.set_ylabel("VFI z")
        ax1.set_title(
            f"{pair[:-3].upper()} - last {BARS} daily bars | "
            f"green span = U-base leg (back-loaded), red = V-spike, "
            f"gray = even | ^ green = fresh 20d low at lows, purple "
            f"o = absorption (effort>result at lows), v red = fresh "
            f"high at highs | blue line/dot = VFI zero-cross up",
            fontsize=8)
        ax1.grid(alpha=0.18)
        ax2.grid(alpha=0.18)
        plt.tight_layout()
        p = OUT / f"{pair}.png"
        plt.savefig(p, dpi=110)
        plt.close(fig)
        print("chart:", p)


if __name__ == "__main__":
    main()
