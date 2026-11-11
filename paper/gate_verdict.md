# Forward-test gate verdict: HOLD

Sessions: 1 / 20 required

| Criterion | Required | Observed | Pass |
|---|---|---|---|
| min_paper_trading_days | >= 20 | 1 | NO |
| signal_parity_index | >= 0.98 | 1.0 | YES |
| duplicate_fires | = 0 | 0 | YES |
| kill_switch_events | <= 0 | 0 | YES |
| max_daily_drawdown_respected | no uncontrolled drawdown (max_dd within risk model) | 3.811% | YES |

## Session summary

- sharpe: 0.005
- max_dd_pct: 3.811
- fills: 78
- expected_costs_total: 11320.39
- audit_status: PASS

Criteria not yet met: continue paper trading.
