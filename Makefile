PYTHON ?= python3
DAY ?= 2026-10-01
SYMBOL ?= BTCUSDT
RAW := data/raw
PARQ := data/processed
DIFFS := $(RAW)/incremental_book_L2_$(SYMBOL)_$(DAY).csv.gz
SNAPS := $(RAW)/book_snapshot_25_$(SYMBOL)_$(DAY).csv.gz
PARQP := $(PARQ)/incremental_book_L2_$(SYMBOL)_$(DAY).parquet
BASE := https://datasets.tardis.dev/v1/binance-futures
DIFFS_BYTES := 796135847
SNAPS_BYTES := 90294106

.PHONY: help env pull-free pull gate verify-bytes convert censor harness-check board test guard gate-day

help:
	@echo "One-command L2 gate process (run from the codespace, repo root)."
	@echo "  make env                 install the Python stack (also done automatically by the devcontainer)"
	@echo "  make pull-free DAY=...   download a free first-of-month day (no key)"
	@echo "  make pull DAY=...        download a paid day (needs $$TARDIS_API_KEY)"
	@echo "  make verify-bytes        check the downloaded day against the frozen 2026-10-01 byte anchors"
	@echo "                           (incremental_book_L2 796135847, book_snapshot_25 90294106)"
	@echo "  make gate DAY=...        run the Tardis L2 gate (mid + depth vs book_snapshot_25)"
	@echo "  make convert DAY=...     csv.gz -> parquet with verified row counts"
	@echo "  make censor             print the ex-ante macro timeline audit"
	@echo "  make harness-check      C1-L2 harness compile check (no data, no results)"
	@echo "  make gate-day            pull-free + verify-bytes + gate for the verified free day 2026-10-01"
	@echo "  make board              nightly descriptive board refresh (seal -> resolve -> study)"
	@echo "  make test               the repo's pytest suite"

env:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install numpy pandas pyarrow scipy lifelines scikit-learn pytest

pull-free:
	mkdir -p $(RAW)
	curl -o $(DIFFS) "$(BASE)/incremental_book_L2/$(SYMBOL)/$(DAY).csv.gz"
	curl -o $(SNAPS) "$(BASE)/book_snapshot_25/$(SYMBOL)/$(DAY).csv.gz"
	@echo "byte sizes checked by make verify-bytes before the gate runs"

pull:
	@test -n "$$TARDIS_API_KEY" || { echo "TARDIS_API_KEY is not set (add it as a Codespaces secret)"; exit 1; }
	mkdir -p $(RAW)
	curl -H "Authorization: Bearer $$TARDIS_API_KEY" -o $(DIFFS) "$(BASE)/incremental_book_L2/$(SYMBOL)/$(DAY).csv.gz"
	curl -H "Authorization: Bearer $$TARDIS_API_KEY" -o $(SNAPS) "$(BASE)/book_snapshot_25/$(SYMBOL)/$(DAY).csv.gz"

verify-bytes:
	@d=$$(wc -c < $(DIFFS) 2>/dev/null || echo 0); \
	if [ "$$d" != "$(DIFFS_BYTES)" ]; then \
	  echo "BYTE CHECK FAILED: $(DIFFS) is $$d bytes, expected $(DIFFS_BYTES) (frozen 2026-10-01 anchor)"; exit 1; \
	fi
	@s=$$(wc -c < $(SNAPS) 2>/dev/null || echo 0); \
	if [ "$$s" != "$(SNAPS_BYTES)" ]; then \
	  echo "BYTE CHECK FAILED: $(SNAPS) is $$s bytes, expected $(SNAPS_BYTES) (frozen 2026-10-01 anchor)"; exit 1; \
	fi
	@echo "BYTE CHECK PASSED: incremental_book_L2 $(DIFFS_BYTES) bytes, book_snapshot_25 $(SNAPS_BYTES) bytes"

gate:
	$(PYTHON) src/gate_tardis_sample.py --diffs $(DIFFS) --snapshots $(SNAPS)

convert:
	$(PYTHON) src/convert_to_parquet.py $(DIFFS) $(PARQP)

censor:
	$(PYTHON) src/macro_censor.py --timeline data/macro_timeline.csv

harness-check:
	$(PYTHON) src/c1_l2_test.py

gate-day: pull-free verify-bytes gate

board:
	$(PYTHON) src/board_refresh.py

guard:
	$(PYTHON) src/integrity_guard.py

test: guard
	$(PYTHON) -m pytest tests -q
