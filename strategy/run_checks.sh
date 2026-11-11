#!/usr/bin/env bash
# Run the full VP-MR-ETF-D1-001 verification program.
# Fast suites always run; the real-engine suites run if nautilus_trader
# is installed (the CI engine job installs it).
set -e
cd "$(dirname "$0")"

echo "=== 1/6 Gate suite (G1-G4 + modules) ==="
python3 test_gates.py

echo "=== 2/6 Adapter wiring (stubbed engine) ==="
python3 test_adapter_wiring.py

echo "=== 3/6 Paper-trading runner (persistence, idempotency, SPI) ==="
python3 test_runner.py

echo "=== 4/6 Session report consistency ==="
python3 test_session_report.py

echo "=== 5/6 Promotion gate (PROMOTE/HOLD verdicts) ==="
python3 test_gate_check.py

echo "=== 6/6 Real-engine suites (skips if nautilus_trader missing) ==="
python3 test_nautilus_engine.py
python3 test_engine_parity.py

echo ""
echo "ALL SUITES GREEN"
