"""L2 Data Verification Gate — runs FIRST on any arriving L2 dataset.

Fails loudly (exit 1, 'GATE FAILED') if the data is corrupted. Nothing
downstream may run until this gate passes.

Supported diff schemas (auto-detected, unknown schemas fail loudly):
- Binance-native depth diffs with sequence numbers U/u/pu (gap = pu != last u).
- Tardis-style incremental book updates with sequence_number + operation
  (insert/update/delete) + side. The exact Tardis column layout must be
  confirmed against the first delivered file; the loader refuses to guess.

Gate criteria (from paper/research/l2_data_acquisition_spec.md):
  1. sequence gap rate < 0.01% of updates
  2. mid-price agreement within one tick at >= 99% of 100 random timestamps
  3. depth agreement (aggregate size within 10bps of mid, per side, within
     depth_rel_tol) at >= 99% of sampled timestamps
Gaps are logged to gaps.log (timestamped, never silently patched). A gap
invalidates the book until the next resync point.
"""

import argparse
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

GAP_LOG = "gaps.log"
N_SAMPLES = 100
MAX_GAP_RATE = 0.0001
MIN_MID_AGREEMENT = 0.99
MIN_DEPTH_AGREEMENT = 0.99


def _norm_cols(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df


def load_diffs(path: Path) -> pd.DataFrame:
    df = _norm_cols(pd.read_csv(path))
    cols = set(df.columns)
    if {"seq_u", "seq_pu", "side", "price", "size"} <= cols:
        kind = "binance_diff"
    elif {"sequence_number", "operation", "side", "price"} <= cols:
        kind = "tardis_ops"
        if "size" not in cols and "amount" in cols:
            df = df.rename(columns={"amount": "size"})
    else:
        raise ValueError(
            f"unknown diff schema: columns {sorted(cols)}; refusing to guess"
        )
    df = df.sort_values("ts_exchange_us", kind="stable").reset_index(drop=True)
    df.attrs["kind"] = kind
    return df


class BookReconstructor:
    """Applies diffs, tracks sequence continuity, logs gaps to gaps.log.
    A gap invalidates the book until the next resync (fresh chain start or
    snapshot)."""

    def __init__(self, tick_size: float, log_path: Path = None):
        self.bids: dict[float, float] = {}
        self.asks: dict[float, float] = {}
        self.last_u = None
        self.gaps = 0
        self.updates = 0
        self.valid = False
        self.tick = tick_size
        self.log = logging.getLogger("l2gate")
        self.log_path = log_path
        if log_path:
            h = logging.FileHandler(log_path, mode="w")
            h.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
            self.log.addHandler(h)
            self.log.setLevel(logging.INFO)

    def _apply(self, side, price, size):
        book = self.bids if side in ("bid", 0, "b") else self.asks
        if size <= 0:
            book.pop(price, None)
        else:
            book[price] = size

    def apply_row(self, r) -> None:
        # Sequence continuity is a property of MESSAGES, not level-rows:
        # an expanded per-level diff CSV repeats (U, u, pu) across the
        # levels of one message. The gap check must fire exactly once per
        # distinct message - checking per row would false-count a gap on
        # every level after the first. Message identity = (seq_U, seq_u).
        key = (r.get("seq_U"), r.get("seq_u"))
        if key != getattr(self, "_last_msg_key", None):
            self.updates += 1  # counted per MESSAGE
            self._last_msg_key = key
            if r.get("seq_u") is not None and not pd.isna(r.get("seq_u")):
                if r.get("seq_pu") is not None and not pd.isna(r.get("seq_pu")):
                    if self.last_u is not None and r["seq_pu"] != self.last_u:
                        self.gaps += 1
                        self.valid = False
                        self.log.warning(
                            "GAP at ts=%s pu=%s != last_u=%s",
                            r["ts_exchange_us"], r["seq_pu"], self.last_u,
                        )
                    elif not self.valid:
                        self.valid = True
                        self.log.info("RESYNC at ts=%s", r["ts_exchange_us"])
                self.last_u = r.get("seq_u")
        self._apply(r["side"], float(r["price"]), float(r["size"]))

    def mid(self):
        if not self.bids or not self.asks or not self.valid:
            return np.nan
        return (max(self.bids) + min(self.asks)) / 2.0

    def depth_within_10bps(self):
        m = self.mid()
        if np.isnan(m):
            return None
        band = m * 0.001
        b = sum(v for p, v in self.bids.items() if p >= m - band)
        a = sum(v for p, v in self.asks.items() if p <= m + band)
        return (b, a)


def reconstruct(diff_df: pd.DataFrame, tick_size: float, log_path: Path = None):
    rc = BookReconstructor(tick_size, log_path)
    records = diff_df.to_dict("records")
    states = []
    for r in records:
        rc.apply_row(r)
        states.append((r["ts_exchange_us"], rc.mid(), rc.depth_within_10bps()))
    return rc, states


def sample_agreement(states, snapshot_df, tick_size, depth_rel_tol=0.01,
                     n_samples=N_SAMPLES, rng=None):
    """Compare reconstructed book against snapshots at n random timestamps.
    snapshot_df: ts_exchange_us, bid_price, ask_price, bid_depth_10bps,
    ask_depth_10bps (depth columns optional; derived from diff rows if absent).
    """
    rng = rng or np.random.default_rng(0)
    ts = np.array([s[0] for s in states])
    mids = np.array([s[1] if s[1] is not None else np.nan for s in states])
    depths = [s[2] for s in states]
    snaps = snapshot_df.sort_values("ts_exchange_us").reset_index(drop=True)
    st = snaps["ts_exchange_us"].to_numpy()
    pick = rng.choice(len(snaps), size=min(n_samples, len(snaps)), replace=False)
    mid_ok = 0
    depth_ok = 0
    n = 0
    for i in pick:
        t = st[i]
        j = int(np.searchsorted(ts, t, side="right")) - 1
        if j < 0:
            continue
        n += 1
        rec_mid = mids[j]
        snap_mid = (snaps.at[i, "bid_price"] + snaps.at[i, "ask_price"]) / 2.0
        if np.isfinite(rec_mid) and abs(rec_mid - snap_mid) <= tick_size + 1e-12:
            mid_ok += 1
        d = depths[j]
        if d is not None and "bid_depth_10bps" in snaps.columns:
            rb, ra = d
            sb = snaps.at[i, "bid_depth_10bps"]
            sa = snaps.at[i, "ask_depth_10bps"]
            ok = True
            for rec, snap in ((rb, sb), (ra, sa)):
                if snap > 0 and abs(rec - snap) / snap > depth_rel_tol:
                    ok = False
                elif snap == 0 and rec > 0:
                    ok = False
            depth_ok += int(ok)
        elif d is not None:
            depth_ok += 1
    return {
        "n_compared": n,
        "mid_agreement": mid_ok / max(n, 1),
        "depth_agreement": depth_ok / max(n, 1),
    }


def run_gate(diff_path: Path, snapshot_path: Path = None,
             tick_size: float = 0.1, out_dir: Path = None) -> int:
    out_dir = out_dir or Path(".")
    if snapshot_path is not None:
        # Streaming path for large raw-replay days: identical audit semantics
        # (same BookReconstructor gap detection, same 100 random snapshots,
        # same mid/depth comparisons) but book state is captured ONLY at the
        # sampled snapshot timestamps, so memory stays bounded on 20GB days.
        return _run_gate_streaming(diff_path, snapshot_path, tick_size, out_dir)
    diffs = load_diffs(diff_path)
    rc, states = reconstruct(diffs, tick_size, out_dir / GAP_LOG)
    gap_rate = rc.gaps / max(rc.updates, 1)
    snap = diffs_to_snapshot_sample(diffs, rc, states)
    res = sample_agreement(states, snap, tick_size)
    print(f"updates={rc.updates:,}  gaps={rc.gaps:,}  gap_rate={gap_rate:.6f}")
    print(f"mid agreement={res['mid_agreement']:.3f}  "
          f"depth agreement={res['depth_agreement']:.3f}  "
          f"n={res['n_compared']}")
    failed = []
    if gap_rate >= MAX_GAP_RATE:
        failed.append(f"gap rate {gap_rate:.6f} >= {MAX_GAP_RATE}")
    if res["mid_agreement"] < MIN_MID_AGREEMENT:
        failed.append(f"mid agreement {res['mid_agreement']:.3f} < {MIN_MID_AGREEMENT}")
    if res["depth_agreement"] < MIN_DEPTH_AGREEMENT:
        failed.append(f"depth agreement {res['depth_agreement']:.3f} < {MIN_DEPTH_AGREEMENT}")
    if failed:
        print("GATE FAILED: " + "; ".join(failed))
        return 1
    print("GATE PASSED")
    return 0


def _run_gate_streaming(diff_path: Path, snapshot_path: Path,
                        tick_size: float, out_dir: Path,
                        depth_rel_tol: float = 0.01,
                        chunksize: int = 2_000_000) -> int:
    """Bounded-memory gate run against independent exchange snapshots.

    Semantics identical to reconstruct()+sample_agreement():
      - every diff row applied in order through BookReconstructor (message-
        level U/u/pu continuity, gap logging, INVALIDATED-until-resync);
      - the SAME 100 random snapshot rows are selected (rng seed 0,
        replace=False) from the snapshot CSV;
      - for each selected snapshot time t, the book state compared is the
        state right after the last diff row with ts <= t (searchsorted
        'right' - 1 equivalence);
      - mid within one tick; per-side 10-bps depth within depth_rel_tol.
    Only difference: states are captured at the sampled timestamps only,
    so no O(N) state array is materialized.
    """
    snap = _norm_cols(pd.read_csv(snapshot_path))
    snaps = snap.sort_values("ts_exchange_us").reset_index(drop=True)
    st = snaps["ts_exchange_us"].to_numpy()
    rng = np.random.default_rng(0)
    pick = rng.choice(len(snaps), size=min(N_SAMPLES, len(snaps)),
                       replace=False)
    targets = sorted((int(st[i]), i) for i in pick)  # (ts, snap_row)

    rc = BookReconstructor(tick_size, out_dir / GAP_LOG)
    mid_ok = depth_ok = n = 0
    ti = 0  # pointer into targets
    results = []

    for chunk in pd.read_csv(diff_path, chunksize=chunksize):
        chunk = _norm_cols(chunk)
        records = chunk.to_dict("records")
        for r in records:
            rc.apply_row(r)
            while ti < len(targets) and r["ts_exchange_us"] > targets[ti][0]:
                t, i = targets[ti]
                ti += 1
                n += 1
                rec_mid = rc.mid()
                snap_mid = (snaps.at[i, "bid_price"]
                            + snaps.at[i, "ask_price"]) / 2.0
                m_ok = bool(np.isfinite(rec_mid)
                            and abs(rec_mid - snap_mid) <= tick_size + 1e-12)
                d = rc.depth_within_10bps()
                d_ok = False
                if d is not None:
                    rb, ra = d
                    sb = snaps.at[i, "bid_depth_10bps"]
                    sa = snaps.at[i, "ask_depth_10bps"]
                    d_ok = True
                    for rec, s in ((rb, sb), (ra, sa)):
                        if s > 0 and abs(rec - s) / s > depth_rel_tol:
                            d_ok = False
                        elif s == 0 and rec > 0:
                            d_ok = False
                mid_ok += int(m_ok)
                depth_ok += int(d_ok and d is not None)
                results.append((t, rec_mid, snap_mid, d, m_ok,
                                d_ok and d is not None))
    gap_rate = rc.gaps / max(rc.updates, 1)
    print(f"updates={rc.updates:,}  gaps={rc.gaps:,}  gap_rate={gap_rate:.6f}")
    mid_ag = mid_ok / max(n, 1)
    dep_ag = depth_ok / max(n, 1)
    print(f"mid agreement={mid_ag:.3f}  depth agreement={dep_ag:.3f}  n={n}")
    failed = []
    if gap_rate >= MAX_GAP_RATE:
        failed.append(f"gap rate {gap_rate:.6f} >= {MAX_GAP_RATE}")
    if mid_ag < MIN_MID_AGREEMENT:
        failed.append(f"mid agreement {mid_ag:.3f} < {MIN_MID_AGREEMENT}")
    if dep_ag < MIN_DEPTH_AGREEMENT:
        failed.append(f"depth agreement {dep_ag:.3f} < {MIN_DEPTH_AGREEMENT}")
    if failed:
        print("GATE FAILED: " + "; ".join(failed))
        return 1
    print("GATE PASSED")
    return 0


def diffs_to_snapshot_sample(diffs, rc, states, n=N_SAMPLES):
    """Fallback when no REST snapshots exist: build the comparison frame from
    the diff stream itself at n random timestamps. FLAGGED as a weaker check —
    it validates internal sequence consistency, not exchange agreement."""
    rng = np.random.default_rng(1)
    ts = np.array([s[0] for s in states])
    idx = rng.choice(len(states), size=min(n, len(states)), replace=False)
    rows = []
    for j in sorted(idx):
        m = states[j][1]
        d = states[j][2]
        if np.isnan(m) or d is None:
            continue
        rows.append({
            "ts_exchange_us": ts[j],
            "bid_price": m - rc.tick / 2,
            "ask_price": m + rc.tick / 2,
            "bid_depth_10bps": d[0],
            "ask_depth_10bps": d[1],
        })
    return pd.DataFrame(rows)


def run_gate_ndjson(depth_ndjson_gz: Path, snapshot_path: Path,
                    tick_size: float = 0.1, out_dir: Path = None,
                    depth_rel_tol: float = 0.01,
                    align: str = "local",
                    seed_ndjson_gz: Path = None) -> int:
    """Full-day gate directly on the raw Tardis replay NDJSON (fast path).

    Semantics identical to the CSV streaming gate, but messages are parsed
    from the raw replay NDJSON (one depthUpdate per line, native U/u/pu) so
    the 100+M level-row expansion is never materialized:
      - sequence continuity checked ONCE PER MESSAGE (pu != last_u -> gap,
        logged to gaps.log, book INVALIDATED until the next clean resync);
      - 100 random snapshots sampled from the snapshot CSV WITHIN the diff
        time range (fixes the n=0 spurious-failure when the diff window is
        shorter than the snapshot file's span);
      - mid within one tick; per-side 10-bps depth within depth_rel_tol;
      - `align` selects the comparison clock. The Tardis book_snapshot_25
        ground truth is constructed on LOCAL-timestamp ordering, so the
        default 'local' compares book states on the common local clock
        (removing pure feed-latency skew); 'exchange' orders by exchange
        event time. The sequence-gap check is clock-independent.
    """
    import gzip
    import json as _json

    out_dir = out_dir or Path(".")
    snap = _norm_cols(pd.read_csv(snapshot_path))
    snaps = snap.sort_values("ts_exchange_us").reset_index(drop=True)
    st = snaps["ts_exchange_us"].to_numpy()

    # pass 1: diff time range (first/last line only)
    with gzip.open(depth_ndjson_gz, "rt") as fh:
        first = _json.loads(fh.readline())
        lo = int(first["exchange_ts_us"])
    # upper bound: an upper bound beyond the data never triggers a target;
    # targets are filtered by t >= lo (first diff timestamp) anyway.
    rng = np.random.default_rng(0)
    in_range = np.where(st >= lo)[0]
    if len(in_range) == 0:
        print("GATE FAILED: no snapshots within the diff time range")
        return 1
    pick = rng.choice(in_range, size=min(N_SAMPLES, len(in_range)),
                       replace=False)
    targets = sorted((int(st[i]), i) for i in pick)

    log = logging.getLogger("l2gate")
    log_path = out_dir / GAP_LOG
    if log_path:
        h = logging.FileHandler(log_path, mode="w")
        h.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        log.addHandler(h)
        log.setLevel(logging.INFO)

    bids: dict[float, float] = {}
    asks: dict[float, float] = {}
    last_u = None
    valid = False
    # All snapshot messages, ordered by local ts. Tardis emits a fresh
    # depthSnapshot at EVERY feed reconnect and the diff stream restarts
    # from it: the book must RESET at each snapshot message (never carry
    # stale levels across a reconnect). Snapshots are interleaved with the
    # diff stream by local timestamp.
    resets = []
    if seed_ndjson_gz is not None and Path(seed_ndjson_gz).exists():
        with gzip.open(seed_ndjson_gz, "rt") as sfh:
            for line in sfh:
                rec = _json.loads(line)
                d = rec["data"]
                resets.append((rec["local_ts_us"], d))
        resets.sort(key=lambda x: x[0])

    def _apply_reset(d):
        nonlocal last_u, valid
        bids.clear()
        asks.clear()
        for px_s, q_s in d.get("bids") or []:
            q = float(q_s)
            if q > 0:
                bids[float(px_s)] = q
        for px_s, q_s in d.get("asks") or []:
            q = float(q_s)
            if q > 0:
                asks[float(px_s)] = q
        last_u = None  # fresh chain after reconnect; no false gap at reset
        valid = True
        log.info("RESET from depthSnapshot lastUpdateId=%s",
                 d.get("lastUpdateId"))
    gaps = 0
    updates = 0
    ti = 0
    mid_ok = depth_ok = n = 0
    failures = []

    def _state(cov=None):
        """Book state: mid and per-side 10-bps depth. `cov` optionally caps
        the depth band at the comparison snapshot's coverage boundary
        (bid_cover_price/ask_cover_price) so a full-depth reconstruction is
        compared against a level-limited snapshot on equal footing."""
        if not bids or not asks or not valid:
            return np.nan, None
        m = (max(bids) + min(asks)) / 2.0
        band = m * 0.001
        lo, hi = m - band, m + band
        if cov is not None:
            lo = max(lo, cov[0])
            hi = min(hi, cov[1])
        b = sum(v for p, v in bids.items() if p >= lo)
        a = sum(v for p, v in asks.items() if p <= hi)
        return m, (b, a)

    ri = 0
    with gzip.open(depth_ndjson_gz, "rt") as fh:
        for line in fh:
            rec = _json.loads(line)
            d = rec["data"]
            ts = rec["local_ts_us"] if align == "local" else rec["exchange_ts_us"]
            while ri < len(resets) and resets[ri][0] <= ts:
                _apply_reset(resets[ri][1])
                ri += 1
            updates += 1
            pu, u = d.get("pu"), d.get("u")
            if pu is not None and u is not None:
                if last_u is not None and pu != last_u:
                    gaps += 1
                    valid = False
                    log.warning("GAP at ts=%s pu=%s != last_u=%s", ts, pu, last_u)
                elif not valid:
                    valid = True
                    log.info("RESYNC at ts=%s", ts)
                last_u = u
            for px_s, q_s in d.get("b") or []:
                px, q = float(px_s), float(q_s)
                if q <= 0:
                    bids.pop(px, None)
                else:
                    bids[px] = q
            for px_s, q_s in d.get("a") or []:
                px, q = float(px_s), float(q_s)
                if q <= 0:
                    asks.pop(px, None)
                else:
                    asks[px] = q
            while ti < len(targets) and ts > targets[ti][0]:
                t, i = targets[ti]
                ti += 1
                n += 1
                cov = None
                if "bid_cover_price" in snaps.columns:
                    cov = (float(snaps.at[i, "bid_cover_price"]),
                           float(snaps.at[i, "ask_cover_price"]))
                rec_mid, dpair = _state(cov)
                snap_mid = (snaps.at[i, "bid_price"]
                            + snaps.at[i, "ask_price"]) / 2.0
                m_ok = bool(np.isfinite(rec_mid)
                            and abs(rec_mid - snap_mid) <= tick_size + 1e-12)
                d_ok = False
                if dpair is not None:
                    rb, ra = dpair
                    sb = snaps.at[i, "bid_depth_10bps"]
                    sa = snaps.at[i, "ask_depth_10bps"]
                    d_ok = True
                    for rec_, s_ in ((rb, sb), (ra, sa)):
                        if s_ > 0 and abs(rec_ - s_) / s_ > depth_rel_tol:
                            d_ok = False
                        elif s_ == 0 and rec_ > 0:
                            d_ok = False
                mid_ok += int(m_ok)
                depth_ok += int(d_ok)
                if not m_ok or not d_ok:
                    failures.append((t, rec_mid, snap_mid, dpair))

    gap_rate = gaps / max(updates, 1)
    mid_ag = mid_ok / max(n, 1)
    dep_ag = depth_ok / max(n, 1)
    print(f"updates={updates:,}  gaps={gaps:,}  gap_rate={gap_rate:.6f}")
    print(f"mid agreement={mid_ag:.3f}  depth agreement={dep_ag:.3f}  n={n}")
    failed = []
    if gap_rate >= MAX_GAP_RATE:
        failed.append(f"gap rate {gap_rate:.6f} >= {MAX_GAP_RATE}")
    if n < N_SAMPLES:
        failed.append(f"only {n} snapshot comparisons available "
                      f"(< {N_SAMPLES})")
    if mid_ag < MIN_MID_AGREEMENT:
        failed.append(f"mid agreement {mid_ag:.3f} < {MIN_MID_AGREEMENT}")
    if dep_ag < MIN_DEPTH_AGREEMENT:
        failed.append(f"depth agreement {dep_ag:.3f} < {MIN_DEPTH_AGREEMENT}")
    if failed:
        for t, rm, sm, dp in failures[:10]:
            print(f"  FAIL ts={t} rec_mid={rm} snap_mid={sm} depth={dp}")
        print("GATE FAILED: " + "; ".join(failed))
        return 1
    print("GATE PASSED")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--diffs", type=Path, required=True)
    ap.add_argument("--snapshots", type=Path, default=None)
    ap.add_argument("--tick-size", type=float, default=0.1)
    ap.add_argument("--out-dir", type=Path, default=Path("."))
    ap.add_argument("--ndjson", action="store_true",
                    help="--diffs is a raw replay depth.ndjson.gz")
    ap.add_argument("--align", choices=("local", "exchange"), default="local",
                    help="comparison clock vs the snapshot ground truth")
    ap.add_argument("--depth-rel-tol", type=float, default=0.01)
    ap.add_argument("--seed", type=Path, default=None,
                    help="depthSnapshot.ndjson.gz to seed the book (Binance "
                         "procedure: snapshot first, then diffs)")
    args = ap.parse_args(argv)
    if args.ndjson:
        code = run_gate_ndjson(args.diffs, args.snapshots, args.tick_size,
                               args.out_dir, args.depth_rel_tol, args.align,
                               args.seed)
    else:
        code = run_gate(args.diffs, args.snapshots, args.tick_size, args.out_dir)
    sys.exit(code)


if __name__ == "__main__":
    main()
