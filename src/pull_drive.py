"""Pull a large file from Google Drive into data/raw/ and audit it.

Usage:
  python3 src/pull_drive.py --url "https://drive.google.com/file/d/FILE_ID/view"
  python3 src/pull_drive.py --file-id FILE_ID --out data/raw/upload.parquet

Uses gdown (handles Google's virus-scan confirmation page for large
files). After the pull, the file goes through src/intake_audit.py and -
if it looks like order-book data - the standing rule prints: the Layer 0
gate runs FIRST; nothing downstream touches it until the gate exits 0.
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--url", default=None,
                    help="the shared Drive link (anyone-with-link)")
    ap.add_argument("--file-id", default=None)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--skip-audit", action="store_true")
    args = ap.parse_args(argv)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    target = args.url or (f"https://drive.google.com/uc?id={args.file_id}")
    cmd = [sys.executable, "-m", "gdown", "-f", "-O", str(args.out), target]
    print(" ".join(cmd))
    r = subprocess.run(cmd)
    if r.returncode != 0 or not args.out.exists():
        print("[fail] download did not complete")
        return 1
    print(f"downloaded: {args.out} "
          f"({args.out.stat().st_size / 1e6:.1f} MB)")
    if args.skip_audit:
        return 0
    audit_out = ROOT / "paper/research/intake_audit.json"
    r2 = subprocess.run([sys.executable, "src/intake_audit.py",
                         str(args.out), "--out", str(audit_out)])
    return r2.returncode


if __name__ == "__main__":
    sys.exit(main())
