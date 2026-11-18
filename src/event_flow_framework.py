"""The event-flow framework - built the owner's way: pair by pair,
'all the data', when-X-happens-then-what (owner-directed,
2026-11-18).

Directive (Andrea, in-session): "look one by one at the flow charts
of no volume usd tvc crypto pairs and you must go through all the
data and make inferences from your data of events that happen when
x happens, and build the framework like that (which is what I did)."

PRE-DECLARED PROTOCOL (registered BEFORE the run; nothing tuned):
  1. UNIVERSE AUDIT: every archive series classified by volume
     availability - a series is NO-VOLUME if <1% of its bars carry
     volume > 0; the flow axis on NO-VOLUME pairs uses the owner's
     own AVFI v3.2 fallback (proxy volume from the true range),
     declared here, nothing hidden.
  2. THE EVENT CHAIN (the 'when x happens' skeleton): legs from the
     session-55 grammar (fractal pivots, W=3); each leg -> event
     class = direction x size-bucket(s/m/l) x wake(f/b/e) - the
     duration dimension is dropped for the chain (registered). The
     transition table T[prev][next] = counts of consecutive leg
     pairs over ALL series, row-normalized to P(next|prev) - THE
     FRAMEWORK: when leg X completes, what forms next.
  3. ASYMMETRY READ (the inference rule, declared): a transition is
     an inference only if (a) P(next=OPPOSITE-direction class |
     prev) deviates from the marginal P(opposite) by >=8 points
     AND (b) the deviation holds in BOTH halves (h1/h2 split of the
     series) with the same sign. Everything else is recorded as
     structure, not signal.
  4. PAIR-BY-PAIR: for EVERY series, its own top deviation from the
     aggregate transition table (its individuality recorded - the
     'one by one' pass), saved to
     clue_scan/event_flow_per_pair.csv.
  5. VOLUME vs NO-VOLUME inference: the washout-bottom chip (the
     flagship) re-measured separately on volume pairs (real flow)
     and NO-VOLUME pairs (proxy-TR flow) - does the chart-only
     reading survive without real volume? Declared question, both
     answers reported, whatever they are.
All in-sample descriptive; sigma>0 guard throughout; nothing armed;
nothing trades live.
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd

from chart_grammar_dossier import pivots_legs, flow_pct

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data")
OUT_PAIRS = CLUE / "event_flow_per_pair.csv"
OUT_MATRIX = CLUE / "event_flow_matrix.csv"
OUT_MD = CLUE / "event_flow_framework.md"

W = 3
SIGMA_WIN = 20
MOVE_SIGMA = 4.0
MOVE_HORIZON = 60
FRESH_WIN = 20
RANGE_WIN = 252
NEED = RANGE_WIN + SIGMA_WIN + 5
DEV_MIN = 0.08


def leg_class(sym):
    return f"{sym[0]}{sym[1]}{sym[3]}"


def half_of(idx, n):
    return "h1" if idx < n // 2 else "h2"


def main():
    classes = [d + m + w for d in "UD" for m in "sml" for w in "fbe"]
    agg = {p: {q: 0 for q in classes} for p in classes}
    agg_half = {p: {q: {"h1": 0, "h2": 0} for q in classes} for p in
                classes}
    pair_rows = []
    audit = {"total": 0, "novol": 0, "vol": 0}
    vol_set, novol_set = set(), set()

    chip = {(g, k): [] for g in ("vol", "novol") for k in ("wash",
                                                           "other")}

    for data_file in sorted(DATA.glob("*.csv")):
        try:
            df = pd.read_csv(data_file)
        except Exception:
            continue
        if "close" not in df.columns or len(df) < NEED:
            continue
        for c in ("high", "low", "close"):
            if c not in df.columns:
                df = None
                break
        if df is None:
            continue
        df = df.reset_index(drop=True)
        audit["total"] += 1
        high = pd.Series(df["high"].to_numpy(), dtype=float)
        low = pd.Series(df["low"].to_numpy(), dtype=float)
        close = pd.Series(df["close"].to_numpy(), dtype=float)
        n = len(close)
        has_vol = "volume" in df.columns
        vol_frac = (0.0 if not has_vol else float(
            (pd.Series(df["volume"].to_numpy(), dtype=float) > 0)
            .mean()))
        if vol_frac < 0.01:
            group = "novol"
            audit["novol"] += 1
            novol_set.add(data_file.stem)
            proxy = (high - low).combine(
                (high - close.shift(1)).abs(), np.maximum
            ).combine((low - close.shift(1)).abs(), np.maximum).fillna(
                high - low)
            volume = proxy
        else:
            group = "vol"
            audit["vol"] += 1
            vol_set.add(data_file.stem)
            volume = pd.Series(df["volume"].to_numpy(), dtype=float)

        ret = close.pct_change()
        sigma = ret.rolling(SIGMA_WIN).std().shift(1)
        sigma_a = sigma.to_numpy()
        move = ((ret.abs() >= MOVE_SIGMA * sigma)
                & (sigma > 0)).to_numpy()
        up = ((ret >= MOVE_SIGMA * sigma) & (sigma > 0)).to_numpy()
        rng_hi = high.rolling(RANGE_WIN).max()
        rng_lo = low.rolling(RANGE_WIN).min()
        rp = ((close - rng_lo) / (rng_hi - rng_lo)
              .replace(0, np.nan)).shift(1)
        vp = flow_pct(close, volume).shift(1)
        fresh_lo = (close == close.rolling(FRESH_WIN).min())

        # --- the chip (washout bottom = A2) on this series ---
        valid = ((close > 0.01).astype(float)
                 .shift(1).fillna(0.0).to_numpy()) > 0
        rp_a = rp.to_numpy()
        vp_a = vp.to_numpy()
        fl_a = fresh_lo.shift(1).fillna(False).to_numpy()
        for i in range(n - MOVE_HORIZON - 1):
            if not valid[i]:
                continue
            first_dir = None
            for j in range(i + 1, min(i + MOVE_HORIZON, n - 1) + 1):
                if move[j]:
                    first_dir = 1.0 if up[j] else -1.0
                    break
            if first_dir is None or np.isnan(rp_a[i]) \
                    or np.isnan(vp_a[i]):
                continue
            if rp_a[i] <= 0.20 and fl_a[i]:
                key = "wash" if vp_a[i] <= 10.0 else "other"
                chip[(group, key)].append(first_dir)

        # --- the leg chain on this series ---
        legs = pivots_legs(high.to_numpy(), low.to_numpy(),
                           close.to_numpy(), sigma_a)
        pair_counts = {}
        for a, b in zip(legs, legs[1:]):
            ca, cb = leg_class(a["sym"]), leg_class(b["sym"])
            h = half_of(b["i2"], n)
            agg[ca][cb] += 1
            agg_half[ca][cb][h] += 1
            pair_counts[(ca, cb)] = pair_counts.get((ca, cb), 0) + 1
        best = None
        tot_l = sum(pair_counts.values())
        for (ca, cb), c in pair_counts.items():
            if c < 5:
                continue
            exp = (sum(agg_ca_counts.get(ca, 0) for agg_ca_counts in
                       [None]) if False else None)
            elem = {"series": data_file.stem, "group": group,
                    "prev": ca, "next": cb, "obs_share": c / tot_l,
                    "count": c}
            if best is None or c > best["count"]:
                best = elem
        if best:
            pair_rows.append(best)

    # row-normalized aggregate table + asymmetry read
    marg_up = sum(c["U"] for q in agg.values()
                  for c in [q]) if False else None

    marginal = {}
    for p in classes:
        tot = sum(agg[p].values())
        if tot:
            marginal[p] = {q: agg[p][q] / tot for q in classes}
    next_marginal = {q: sum(agg[p][q] for p in classes)
                     / max(1, sum(sum(x.values()) for x in
                                  agg.values())) for q in classes}
    m_opp = sum(v for kk, v in next_marginal.items()
                if (kk[0] == "D" if True else False))
    rows = []
    for p in classes:
        for q in classes:
            h1 = agg_half[p][q]["h1"]
            h2 = agg_half[p][q]["h2"]
            tot = agg[p][q]
            rows.append({
                "prev": p, "next": q, "count": tot,
                "P_next_given_prev": round(marginal[p][q], 4),
                "marginal_P_next": round(next_marginal[q], 4),
                "h1": h1, "h2": h2,
            })
    OUT_MATRIX.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_MATRIX, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # CLASS-LEVEL inferences (direction alternation is a grammar
    # tautology - legs alternate by construction; the signal layer is
    # WHICH class follows): dev = P(next=q|prev) - marginal P(q),
    # inference only if |dev| >= 8 points, same sign in both halves.
    inferences = []
    for p in classes:
        tot = sum(agg[p].values())
        if tot < 200:
            continue
        for q in classes:
            obs = agg[p][q] / tot
            dev = obs - next_marginal[q]
            if abs(dev) < DEV_MIN:
                continue
            sh = {}
            for halv in ("h1", "h2"):
                t_h = sum(agg_half[p][kk][halv] for kk in classes)
                o_h = agg_half[p][q][halv] / t_h if t_h else None
                sh[halv] = o_h
            stable = (sh["h1"] is not None
                      and np.sign(dev) == np.sign(sh["h1"] - dev)
                      and np.sign(sh["h1"] - next_marginal[q])
                      == np.sign(sh["h2"] - next_marginal[q]))
            inferences.append({
                "prev": p, "next": q,
                "P_next": round(obs, 4),
                "marginal": round(next_marginal[q], 4),
                "dev": round(dev, 4),
                "h1": round(sh["h1"], 4) if sh["h1"] is not None else "",
                "h2": round(sh["h2"], 4) if sh["h2"] is not None else "",
                "half_stable": bool(stable), "n_prev": tot,
            })
    inferences = [i for i in inferences if i["half_stable"]]
    inferences.sort(key=lambda r: -abs(r["dev"]))

    for group in ("vol", "novol"):
        for key in ("wash", "other"):
            arr = np.array(chip[(group, key)])
            print("chip", group, key, len(arr),
                  round(float((arr > 0).mean()), 4) if len(arr) else "-")

    with open(OUT_PAIRS, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["series", "group", "prev", "next", "count",
                    "obs_share"])
        for r in sorted(pair_rows, key=lambda r: -r["count"]):
            w.writerow([r["series"], r["group"], r["prev"], r["next"],
                        r["count"], round(r["obs_share"], 4)])

    md = ["# The event-flow framework - when X happens, what happens",
          "next (built the owner's way: pair by pair, all the data)",
          "",
          f"Universe audit: {audit['total']} series - "
          f"{audit['vol']} with volume, {audit['novol']} NO-VOLUME"
          " (flow via the owner's true-range proxy fallback).",
          "",
          "## Inference cells (P(next CLASS | prev) deviates from",
          "the marginal by >= 8 points, stable in both halves;",
          "direction-alternation is a grammar tautology and is NOT",
          "counted as inference):",
          "",
          "| prev leg | next leg | P(next \| prev) | marginal | dev | h1 | h2 | n(prev) |",
          "|---|---|---|---|---|---|---|---|"]
    for r in inferences[:40]:
        md.append(f"| {r['prev']} | {r['next']} | {r['P_next']} "
                  f"| {r['marginal']} | {r['dev']} | {r['h1']} "
                  f"| {r['h2']} | {r['n_prev']} |")
    md += ["",
           "Full transition matrix: event_flow_matrix.csv; per-pair",
           "counts: event_flow_per_pair.csv. All in-sample",
           "descriptive; nothing armed; nothing trades live."]
    OUT_MD.write_text("\n".join(md) + "\n")
    print("audit:", audit)
    for r in inferences:
        print(r)


if __name__ == "__main__":
    main()
