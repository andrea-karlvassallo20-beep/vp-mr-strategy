import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from top500_scan import genesis_metrics


def _mk_df(closes):
    n = len(closes)
    return pd.DataFrame({
        "date": [f"2024-01-{i+1:02d}" for i in range(n)],
        "close": closes,
        "volume": np.ones(n),
    })


def test_genesis_ath_inside_first_90_days():
    closes = np.concatenate([np.linspace(1, 10, 90), np.linspace(9.9, 2, 110)])
    g = genesis_metrics(_mk_df(closes))
    assert g["ath_in_genesis"] is True
    assert g["genesis_ret_90d"] == round(float(closes[89] / closes[0] - 1.0), 3)


def test_genesis_ath_after_genesis():
    closes = np.concatenate([np.linspace(10, 1, 90), np.linspace(1, 100, 110)])
    g = genesis_metrics(_mk_df(closes))
    assert g["ath_in_genesis"] is False
    assert g["ath_vs_now"] == 1.0


def test_genesis_short_history():
    g = genesis_metrics(_mk_df(np.linspace(1, 5, 200)))
    assert g["n_days"] == 200
    assert g["first_bar"] == "2024-01-01"
