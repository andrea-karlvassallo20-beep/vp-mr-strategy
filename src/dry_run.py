"""Dry run (Option c): infrastructure validation on real BTCUSDT aggTrades.

DESCRIPTIVE ONLY. No hazard model, no predictive claims, no C5/C6 proxies.
bookDepth band-OFI is a SYNTAX CHECK only (5s snapshots destroy the update
sequence; the number is not meaningful and is not plotted as if it were).
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from features import vpin_trade_buckets, fit_hawkes, top_of_book_ofi, band_depth_ofi_proxy
from event_clock import trade_clock_rows, purged_cpcv_splits, assert_no_leakage

PROC = Path("data/processed")
PLOTS = PROC / "plots"
PLOT = False
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    PLOT = True
except ImportError:
    pass


def ascii_hist(x, bins=20, width=50, title=""):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    lo, hi = x.min(), x.max()
    counts, edges = np.histogram(x, bins=bins)
    mx = counts.max()
    print(f"\n{title}  n={len(x)}  min={lo:.4g}  max={hi:.4g}  "
          f"mean={x.mean():.4g}  nan={np.isnan(np.asarray(x, dtype=float)).sum()}")
    for c, e0, e1 in zip(counts, edges[:-1], edges[1:]):
        bar = "#" * int(width * c / max(mx, 1))
        print(f"  [{e0:>10.4g},{e1:>10.4g}) {c:>8} {bar}")


def day_stats(trades, label):
    rows = trade_clock_rows(trades)
    per_day = len(rows)
    hours = pd.to_datetime(rows["ts_exchange_us"], unit="us", utc=True).dt.hour
    hc = hours.value_counts().reindex(range(24), fill_value=0)
    kinds = rows["state_change_kind"].value_counts().to_dict()
    print(f"\n[{label}] trades={len(trades):,}  clock_rows={per_day:,}  "
          f"({per_day / len(trades) * 100:.1f}% of trades)  kinds={kinds}")
    print(f"  rows/hour min={hc.min()} (h{int(hc.idxmin())})  "
          f"max={hc.max()} (h{int(hc.idxmax())})  -> self-thinning "
          f"{'CONFIRMED' if hc.max() / max(hc.min(), 1) > 5 else 'weak'}")
    return rows, per_day, hc


def main():
    files = sorted((PROC / "aggtrades").glob("*.parquet"))
    assert files, "no ingested aggTrades parquet found"
    all_rows = []
    per_day_counts = {}
    hourly = pd.Series(0, index=range(24))
    for f in files:
        t = pd.read_parquet(f)
        rows, n, hc = day_stats(t, f.name)
        all_rows.append(rows)
        per_day_counts[f.name] = n
        hourly = hourly.add(hc, fill_value=0)

    print("\n=== KILL LINE 3: event-clock rows per day (>= 10,000 required) ===")
    for k, v in per_day_counts.items():
        print(f"  {k}: {v:,} rows  {'PASS' if v >= 10_000 else 'FAIL'}")

    print("\n=== VPIN (trade-count buckets, genuine aggTrades volume) ===")
    for f in files:
        t = pd.read_parquet(f)
        v = vpin_trade_buckets(t, bucket_size=5000)
        assert not v.isna().any().any(), "NaN in VPIN output"
        ascii_hist(v["vpin"], title=f"VPIN (EWMA50) {f.name}")
        if PLOT:
            PLOTS.mkdir(parents=True, exist_ok=True)
            fig, ax = plt.subplots(figsize=(10, 3))
            ax.plot(pd.to_datetime(v["bucket_end_ts"], unit="us"), v["vpin"],
                    lw=0.5)
            ax.set_title(f"VPIN trade-count buckets - {f.name}")
            fig.tight_layout()
            fig.savefig(PLOTS / f"vpin_{f.stem}.png", dpi=110)
            plt.close(fig)

    print("\n=== Hawkes 2-dim (buy/sell trades): calm window then crash window ===")

    def hawkes_window(parquet, start, end, cap=200_000):
        t = pd.read_parquet(PROC / "aggtrades" / parquet)
        lo = pd.Timestamp(start).value // 1000
        hi = pd.Timestamp(end).value // 1000
        w = t[(t["ts_exchange_us"] >= lo) & (t["ts_exchange_us"] < hi)]
        capped = False
        if len(w) > cap:
            w = w.iloc[:cap]
            capped = True
        fit = fit_hawkes(w["ts_exchange_us"].to_numpy(),
                         w["aggressor_buy"].to_numpy())
        return fit, capped

    for label, pq, s, e in [
        ("CALM  2024-08-04 12:00-12:10 UTC (mandatory: must converge)",
         "BTCUSDT-aggTrades-2024-08-04.parquet",
         "2024-08-04 12:00:00+00:00", "2024-08-04 12:10:00+00:00"),
        ("CRASH 2024-08-05 00:00-00:10 UTC (extreme regime)",
         "BTCUSDT-aggTrades-2024-08-05.parquet",
         "2024-08-05 00:00:00+00:00", "2024-08-05 00:10:00+00:00"),
    ]:
        print(f"\n  [{label}]")
        fit, capped = hawkes_window(pq, s, e)
        if capped:
            print("  window capped at 200,000 events for the sequential recursion")
        if not fit["converged"]:
            print("  MLE FAILED on this window: logged as extreme non-stationarity")
            continue
        assert all(np.isfinite(fit["mu"]))
        assert np.isfinite(fit["branching_ratio"])
        print(f"  n_events={fit['n_events']:,}  window_s={fit['window_s']:.0f}  "
              f"optimizer={fit['optimizer']}")
        print(f"  mu (buy, sell)/s = {[round(x, 3) for x in fit['mu']]}")
        print(f"  alpha = {[[round(v, 4) for v in row] for row in fit['alpha']]}")
        print(f"  branching ratio (spectral radius) = "
              f"{fit['branching_ratio']:.4f}")
        print(f"  excitation half-life = {fit['excitation_half_life_s']:.3f} s "
              f"(ln2/beta, beta fixed at {fit['beta_fixed']})")
        print(f"  loglik = {fit['loglik']:.1f}")

    print("\n=== Top-of-book OFI: synthetic bookTicker logic validation ===")
    rng = np.random.default_rng(7)
    n = 20000
    bid_p = 50000 + np.cumsum(rng.normal(0, 1, n))
    book = pd.DataFrame({
        "ts_exchange_us": np.sort(rng.integers(0, 10**10, n)).astype("int64"),
        "update_id": np.arange(n),
        "bid_price": bid_p,
        "bid_qty": rng.uniform(0.1, 5, n),
        "ask_price": bid_p + 0.1 + rng.integers(0, 4, n) * 0.1,
        "ask_qty": rng.uniform(0.1, 5, n),
    })
    ofi = top_of_book_ofi(book)
    assert not ofi.isna().any().any(), "NaN in OFI output"
    ascii_hist(ofi["ofi"], bins=15, title="OFI (synthetic bookTicker)")

    print("\n=== bookDepth band-OFI: SYNTAX CHECK ONLY (not meaningful, not plotted) ===")
    import zipfile, io
    with zipfile.ZipFile("data/raw/bookTicker/BTCUSDT-bookDepth-2024-08-05.zip") as zf:
        bd = pd.read_csv(zf.open(zf.namelist()[0]))
    p = band_depth_ofi_proxy(bd)
    assert not p.isna().any().any(), "NaN in band-OFI proxy"
    print(f"  bookDepth 2024-08-05: {len(bd):,} snapshot rows, "
          f"{len(p):,} diff rows, no NaN. SYNTAX CHECK PASS. "
          "NOT plotted, NOT meaningful (5s snapshots destroy update sequence).")

    print("\n=== KILL LINE 2: CPCV + embargo dry run on the real event clock ===")
    rows = pd.concat(all_rows, ignore_index=True).sort_values("ts_exchange_us")
    row_ts = rows["ts_exchange_us"].to_numpy()
    H = int(3600 * 1e6)
    E = int(3600 * 1e6)
    rng = np.random.default_rng(11)
    toy_label = rng.integers(0, 2, len(row_ts))
    total_overlaps = 0
    print(f"  rows={len(row_ts):,}  label_horizon=1h  embargo=1h  "
          f"toy labels: {toy_label.sum():,} ones")
    for split in purged_cpcv_splits(row_ts, n_groups=6, label_horizon_us=H,
                                    embargo_us=E, n_test_groups=1):
        assert_no_leakage(split, row_ts, H, E)
        inter = len(set(split["train_idx"]) & set(split["test_idx"]))
        lo_, hi_ = split["test_bounds"]
        print(f"  split {split['test_groups']}: test={len(split['test_idx']):,} "
              f"train={len(split['train_idx']):,} purged={split['purged']:,} "
              f"index-intersection={inter} label-overlaps=0")
        total_overlaps += inter
    print(f"  TOTAL index intersections across splits: {total_overlaps} "
          f"{'PASS' if total_overlaps == 0 else 'FAIL'}")

    if PLOT:
        PLOTS.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.bar(hourly.index, hourly.values)
        ax.set_title("Event-clock rows by UTC hour (3 days, self-thinning)")
        ax.set_xlabel("UTC hour")
        fig.tight_layout()
        fig.savefig(PLOTS / "event_clock_hourly.png", dpi=110)
        plt.close(fig)
        print(f"\nplots written to {PLOTS}/")


if __name__ == "__main__":
    main()
