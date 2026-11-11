"""Challenger: shadow paper-trading for the edge-seeker's winning candidate.

Champion/challenger architecture:
- The CHAMPION is the deployed strategy, frozen (Gate 3). Its 20-session
  forward test must remain honest — it is never silently modified.
- The CHALLENGER is the edge-seeker's selected candidate, running in
  shadow on the same real bars each night, with its own persisted state.
- When the challenger's live paper equity beats the champion's by the
  promotion margin over the evaluation window, a redeployment proposal
  is written with the full evidence trail. Applying it stays a
  human-reviewed PR.

Usage (nightly, after the champion session):
    python3 challenger.py --data-dir ./paper/data \
        --champion-state ./paper/state --challenger-state ./paper/challenger \
        --markdown ./paper/challenger_report.md
"""
import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from edge_seeker import seek, CANDIDATES, MARGIN
from papertrading_runner import PaperTradingRunner
from vol_models import VariantStrategy
from vp_mr_strategy import StrategyParameters


def run_challenger_session(data_dir: Path, state_dir: Path,
                           candidate: dict,
                           universe: List[str] = None) -> int:
    """Advance the challenger's shadow paper state by any new bars.
    Universe defaults to instruments that actually have feed CSVs."""
    if universe is None:
        universe = [p.stem.upper() for p in sorted(data_dir.glob("*.csv"))]
    z = candidate["z_entry"]
    lb = candidate["lookback"]
    vm = candidate["vol_model"]
    vf = candidate["volume_filter"]
    params = StrategyParameters(zscore_entry=z, lookback_zscore=lb)

    class ChallengerRunner(PaperTradingRunner):
        def _load_state(self):
            super()._load_state()
            # re-wrap the restored strategy in the variant shell
            base = self.strat
            variant = VariantStrategy.__new__(VariantStrategy)
            variant.__dict__.update(base.__dict__)
            variant.vol_model = vm
            variant.volume_filter = vf
            from collections import deque
            from vol_models import VOLUME_LOOKBACK
            variant._vol_buf = {s: deque(maxlen=VOLUME_LOOKBACK + 5)
                               for s in self.universe}
            self.strat = variant

    runner = ChallengerRunner(data_dir, state_dir, params=params,
                              universe=universe)
    processed = runner.run_session()
    return runner


def challenger_equity(data_dir: Path, state_dir: Path) -> np.ndarray:
    """MTM equity of the challenger from its persisted decision log."""
    state = json.load(open(state_dir / "session_state.json"))
    universe = state["universe"]
    from papertrading_runner import load_bars
    bars = {s: load_bars(data_dir / f"{s.lower()}.csv") for s in universe}
    dates = sorted({b["date"] for s in universe for b in bars[s]})
    px = {s: {b["date"]: b["close"] for b in bars[s]} for s in universe}
    pos = {s: {} for s in universe}
    for rec in state["decision_log"]:
        pos[rec["instrument"]][rec["ts"]] = rec["position"]
    equity = []
    for d in dates:
        pnl = 0.0
        for s in universe:
            p = pos[s].get(d)
            if p is None:
                continue
            prev = [x for x in px[s] if x < d]
            if prev:
                pnl += p * (px[s][d] - px[s][max(prev)])
        equity.append(state["initial_equity"] + pnl)
    return np.array(equity)


def evaluate_race(data_dir: Path, champion_state: Path,
                  challenger_state: Path, candidate: dict) -> dict:
    """Compare challenger vs champion paper equity on the common window."""
    champ_eq = challenger_equity(data_dir, champion_state)
    chall_eq = challenger_equity(data_dir, challenger_state)
    n = min(len(champ_eq), len(chall_eq))
    if n < 2:
        return {"status": "WARMING_UP", "bars": n}
    champ_ret = float(champ_eq[-1] / champ_eq[0] - 1)
    chall_ret = float(chall_eq[-1] / chall_eq[0] - 1)
    champ_dd = float(((np.maximum.accumulate(champ_eq) - champ_eq)
                      / np.maximum.accumulate(champ_eq)).max())
    chall_dd = float(((np.maximum.accumulate(chall_eq) - chall_eq)
                      / np.maximum.accumulate(chall_eq)).max())
    champ_sharpe = _sharpe(champ_eq)
    chall_sharpe = _sharpe(chall_eq)
    propose = chall_sharpe - champ_sharpe > MARGIN
    return {"status": "OK", "bars": n,
            "champion": {"ret_pct": round(champ_ret * 100, 3),
                         "sharpe": champ_sharpe,
                         "max_dd_pct": round(champ_dd * 100, 3)},
            "challenger": {"ret_pct": round(chall_ret * 100, 3),
                           "sharpe": chall_sharpe,
                           "max_dd_pct": round(chall_dd * 100, 3)},
            "candidate": candidate,
            "recommendation": ("PROPOSE_REDEPLOY" if propose
                               else "KEEP_CHAMPION"),
            "gate3_note": ("Champion parameters remain frozen; applying a "
                           "proposal is a human-reviewed PR.")}


def _sharpe(eq: np.ndarray) -> float:
    rets = np.diff(eq) / eq[:-1]
    if len(rets) < 2 or rets.std(ddof=1) == 0:
        return 0.0
    return round(float(rets.mean() / rets.std(ddof=1) * np.sqrt(252)), 3)


def to_markdown(r: dict) -> str:
    if r.get("status") != "OK":
        return ("# Challenger report\n\n"
                f"Status: {r.get('status')} ({r.get('bars', 0)} bars)\n")
    c = r["candidate"]
    lines = ["# Challenger report — champion vs shadow candidate", "",
             f"Challenger candidate: z={c['z_entry']}, lookback="
             f"{c['lookback']}, vol model={c['vol_model']}, VSA filter="
             f"{c['volume_filter']}", "",
             f"**Recommendation: {r['recommendation']}**", "",
             "| | Return % | Sharpe | Max DD % |", "|---|---|---|---|"]
    ch, cl = r["champion"], r["challenger"]
    lines.append(f"| Champion (deployed, frozen) | {ch['ret_pct']} | "
                 f"{ch['sharpe']} | {ch['max_dd_pct']} |")
    lines.append(f"| Challenger (shadow) | {cl['ret_pct']} | "
                 f"{cl['sharpe']} | {cl['max_dd_pct']} |")
    lines += ["", f"Window: {r['bars']} bars of live paper data.", "",
              f"## Gate 3", "", r["gate3_note"]]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--champion-state", required=True, type=Path)
    ap.add_argument("--challenger-state", required=True, type=Path)
    ap.add_argument("--markdown", type=Path, default=None)
    args = ap.parse_args()

    research = seek(args.data_dir, ["SPY", "QQQ", "IWM", "XLF", "XLE"])
    if research.get("status") != "OK":
        print("no data for research pass; challenger unchanged")
        return
    candidate = research["selected_candidate"]

    universe = [p.stem.upper() for p in sorted(args.data_dir.glob("*.csv"))]
    run_challenger_session(args.data_dir, args.challenger_state, candidate,
                           universe=universe)
    race = evaluate_race(args.data_dir, args.champion_state,
                         args.challenger_state, candidate)
    md = to_markdown(race)
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(md)
        print(f"challenger report written -> {args.markdown}")
    print(f"challenger recommendation: {race.get('recommendation', race.get('status'))}")


if __name__ == "__main__":
    main()
