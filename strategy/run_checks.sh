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

echo "=== 7c Cross-asset edge research (crypto, indices, commodities) ==="
python3 test_cross_asset.py

echo "=== 7d AVFI replication (indicator math, throttle causality) ==="
python3 test_avfi.py

echo "=== 7e Tops-and-bottoms detectors (divergence, climax, event study) ==="
python3 test_tops_bottoms.py

echo "=== 8 Dashboard generation ==="
python3 test_dashboard.py

echo "=== 8b PDF article ingestion ==="
python3 test_pdf_ingest.py

echo "=== 8c Overfitting statistics (DSR, PBO) ==="
python3 test_overfit_stats.py

echo "=== 8d Lessons synthesis (live inferences) ==="
python3 test_lessons.py

echo "=== 8e MR-coin edge study (control group) ==="
python3 test_mr_edge.py

echo "=== 8f v4 confirmation premium (whole universe) ==="
python3 test_v4_study.py

echo "=== 8g Commodity edge battery ==="
python3 test_commodity_edge.py

echo "=== 8h Structural inevitabilities ==="
python3 test_inevitabilities.py

echo "=== 8i SMH proof battery ==="
python3 test_smh_proof.py

echo "=== 8j SMH hazard model (KM + Cox) ==="
python3 test_smh_hazard.py

echo "=== 8k SMH forward scoring protocol (draft, resolve, score, kill lines) ==="
python3 test_smh_forward.py

echo "=== 8l SMH salience gradient + event anatomy (charter ticks 5 and 6) ==="
python3 test_smh_gradient.py

echo "=== 8m SMH precursor signature battery (open problem 3) ==="
python3 test_smh_precursor.py

echo "=== 8n SMH machine live position (status reading) ==="
python3 test_smh_status.py

echo "=== 8o SMH conditional direction battery (law 3's cells) ==="
python3 test_smh_direction.py

echo "=== 8p SMH recurrence battery (the long-run lemma) ==="
python3 test_smh_recurrence.py

echo "=== 9 Nightly pre-flight (full session simulation) ==="
python3 test_nightly_preflight.py

echo "=== 10 Challenger (champion/challenger race) ==="
python3 test_challenger.py

echo "=== 11 Auto-redeploy proposal ==="
python3 test_propose_redeploy.py

echo "=== 12 Session journal ==="
python3 test_journal.py

echo "=== 13 Incident alerts ==="
python3 test_alert.py

echo "=== Real-engine suites (skips if nautilus_trader missing) ==="
python3 test_nautilus_engine.py
python3 test_engine_parity.py

echo ""
echo "ALL SUITES GREEN"
