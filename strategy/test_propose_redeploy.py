"""Auto-redeploy proposal tests: report parsing, deterministic patching,
no-op on KEEP_CHAMPION. Patches a COPY of the strategy file. Harness."""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import propose_redeploy as prd

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


tmp = Path(tempfile.mkdtemp())

PROPOSE_REPORT = """# Challenger report — champion vs shadow candidate

Challenger candidate: z=1.5, lookback=60, vol model=garch, VSA filter=False

**Recommendation: PROPOSE_REDEPLOY**

| | Return % | Sharpe | Max DD % |
|---|---|---|---|
| Champion (deployed, frozen) | 0.489 | 0.044 | 3.811 |
| Challenger (shadow) | 0.427 | 0.044 | 5.876 |
"""

KEEP_REPORT = PROPOSE_REPORT.replace("PROPOSE_REDEPLOY", "KEEP_CHAMPION")

# 1. parsing
r = prd.parse_report(Path(__file__).parent / ".." / "paper" /
                     "challenger_report.md")
check("parses KEEP_CHAMPION from the real report",
      r["verdict"] == "KEEP_CHAMPION")

p = tmp / "propose.md"
p.write_text(PROPOSE_REPORT)
r = prd.parse_report(p)
check("parses PROPOSE_REDEPLOY", r["verdict"] == "PROPOSE_REDEPLOY")
check("parses candidate params",
      r["candidate"]["z_entry"] == 1.5 and r["candidate"]["lookback"] == 60
      and r["candidate"]["vol_model"] == "garch"
      and r["candidate"]["volume_filter"] is False)
check("parses evidence rows", len(r["rows"]) == 2)

# 2. deterministic patch on a COPY
copy = tmp / "vp_mr_strategy.py"
shutil.copy(prd.STRATEGY, copy)
prd.STRATEGY = copy
check("patch changes the file", prd.patch_core_params(1.5, 60))
src = copy.read_text()
check("zscore_entry patched", "zscore_entry: float = 1.5" in src)
check("lookback patched", "lookback_zscore: int = 60" in src)
check("other params untouched", "zscore_exit: float = 0.25" in src)
check("re-patch is a no-op when identical", not prd.patch_core_params(1.5, 60))
check("patch back restores", prd.patch_core_params(2.0, 100))

# 3. PR body
body = prd.pr_body(r)
check("PR body carries evidence", "Champion" in body and "Sharpe" in body)
check("PR body carries Gate 3 framing", "human" in body)
check("PR body flags non-core variant dims", "vol model" in body)

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
