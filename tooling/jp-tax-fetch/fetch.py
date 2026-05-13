#!/usr/bin/env python3
"""Bundle 10 major JP tax laws from e-Gov into references/laws/.

Why bundle these (when other JP laws are fetched dynamically via egov_client.py):
The user explicitly requested local bundling so 中文/英文/日文 commentary skills
have offline access to JP tax statute text without a per-query API round-trip.
Trade-off: ~3-10 MB extra in the repo; refresh is manual (re-run this script
after each tax amendment, typically year-end 税制改正).

Usage:
  python3 tooling/jp-tax-fetch/fetch.py

Run from the repo root. Requires `python` in PATH (egov_client.py is python3).
"""
import json
import os
import pathlib
import subprocess
import sys

# Force UTF-8 stdout for this process and any child Python invocations.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8", "cp65001"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
SUBPROC_ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}

# (法令ID, 出力ファイル名 stem)
LAWS = [
    ("340AC0000000033", "所得税法"),
    ("340AC0000000034", "法人税法"),
    ("363AC0000000108", "消費税法"),
    ("325AC0000000073", "相続税法"),
    ("337AC0000000066", "国税通則法"),
    ("334AC0000000147", "国税徴収法"),
    ("342AC0000000023", "印紙税法"),
    ("332AC0000000026", "租税特別措置法"),
    ("329AC0000000061", "関税法"),
    ("325AC0000000226", "地方税法"),
]

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
CLIENT = REPO_ROOT / "skills" / "jp-law-lookup" / "scripts" / "egov_client.py"
OUT_DIR = REPO_ROOT / "references" / "laws"


def fetch_one(law_id: str, stem: str) -> int:
    """Fetch one law, write to references/laws/<stem>.md. Returns bytes written or 0 on failure."""
    print(f"[{stem}] fetching {law_id}...", flush=True)
    result = subprocess.run(
        [sys.executable, str(CLIENT), "fetch", law_id],
        capture_output=True,
        timeout=120,
        env=SUBPROC_ENV,
    )
    if result.returncode != 0:
        err = result.stderr.decode("utf-8", errors="replace")[:300]
        print(f"  FAIL (exit {result.returncode}): {err}", flush=True)
        return 0
    try:
        # The CLI prints JSON. Parse it; extract `text` (already plain-text-converted XML).
        obj = json.loads(result.stdout.decode("utf-8"))
    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}", flush=True)
        return 0
    if obj.get("error"):
        print(f"  API error: {obj}", flush=True)
        return 0
    text = obj.get("text") or ""
    if not text.strip():
        print(f"  EMPTY text in response", flush=True)
        return 0
    # Prepend a header with metadata
    header = (
        f"# {obj.get('title') or stem}\n\n"
        f"**法令番号**: {obj.get('law_num', 'unknown')}\n"
        f"**法令ID (e-Gov)**: {obj.get('law_id', law_id)}\n"
        f"**公布日**: {obj.get('promulgation_date', 'unknown')}\n"
        f"**最終改正**: {obj.get('amendment_date', 'unknown')}\n"
        f"**出典**: https://laws.e-gov.go.jp/law/{law_id}\n\n"
        f"---\n\n"
    )
    out_path = OUT_DIR / f"{stem}.md"
    out_path.write_text(header + text, encoding="utf-8")
    size = out_path.stat().st_size
    print(f"  ✓ {stem}.md ({size:,} bytes)", flush=True)
    return size


def main():
    if not CLIENT.is_file():
        print(f"ERROR: egov_client.py not found at {CLIENT}", file=sys.stderr)
        sys.exit(1)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    total = 0
    failed = 0
    for law_id, stem in LAWS:
        size = fetch_one(law_id, stem)
        if size == 0:
            failed += 1
        else:
            total += size

    print(f"\nDone. Total {total:,} bytes across {len(LAWS) - failed} laws. Failed: {failed}.")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
