#!/usr/bin/env bash
# Run the full VP-MR-ETF-D1-001 verification program.
set -e
cd "$(dirname "$0")"

echo "=== 1 Gate suite (G1-G4 + modules) ==="
python3 test_gates.py

echo "=== 2 Adapter wiring (stubbed engine) ==="
python3 test_adapter_wiring.py

echo "=== 3 Paper-trading runner (persistence, idempotency, SPI) ==="
python3 test_runner.py

echo "=== 4 Session report consistency ==="
python3 test_session_report.py

echo "=== 5 Promotion gate (PROMOTE/HOLD verdicts) ==="
python3 test_gate_check.py

echo "=== 6 Fetcher hardening ==="
python3 test_fetch.py

echo "=== 7 Edge-seeker (honest walk-forward proposals) ==="
python3 test_edge_seeker.py

echo "=== 7b Knowledge variants (vol models, VSA filter) ==="
python3 test_vol_models.py

echo "=== 8 Dashboard generation ==="
python3 test_dashboard.py

echo "=== 9 Nightly pre-flight (full session simulation) ==="
python3 test_nightly_preflight.py

echo "=== 10 Challenger (champion/challenger race) ==="
python3 test_challenger.py

echo "=== 11 Auto-redeploy proposal ==="
python3 test_propose_redeploy.py

echo "=== 12 Session journal ==="
python3 test_journal.py

echo "=== Real-engine suites (skips if nautilus_trader missing) ==="
python3 test_nautilus_engine.py
python3 test_engine_parity.py

echo ""
echo "ALL SUITES GREEN"
