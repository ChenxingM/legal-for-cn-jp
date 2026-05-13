#!/usr/bin/env python3
"""Sync PRC core statutes from LawRefBook/Laws (https://github.com/LawRefBook/Laws).

Why this approach: flk.npc.gov.cn migrated to a SPA architecture in 2026; the
unofficial JSON API documented by github.com/twang2218/law-datasets no longer
exists at the old endpoints. LawRefBook/Laws is a community-maintained corpus
that handles the upstream complexity. We clone it weekly and cherry-pick the
core statutes we need.

Two lists:
  - LRB_SOURCED_LAWS: synced from LawRefBook each run.
  - OWNER_MAINTAINED_LAWS: never touched by the scraper. Use refresh_cn_corpus.py
    to update these from authoritative .docx files when needed.

A law belongs in OWNER_MAINTAINED when LawRefBook lags behind a known recent
amendment. Move it back into LRB_SOURCED once LawRefBook catches up.

Designed to run on GitHub Actions. Only requires git + python stdlib.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Force UTF-8 stdout so unicode ticks/crosses don't crash on Windows consoles.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8", "cp65001"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

LRB_REPO = "https://github.com/LawRefBook/Laws.git"

# Top-level law-category dirs to search in LawRefBook's tree.
SEARCH_DIRS = [
    "民法商法",
    "经济法",
    "行政法",
    "社会法",
    "刑法",
    "诉讼与非诉讼程序法",
    "宪法",
    "宪法相关法",
    "司法解释",
    "行政法规",
    "部门规章",
    "其他",
]

# Laws synced from LawRefBook on every run.
LRB_SOURCED_LAWS = [
    # Civil / commercial / labor / IP / procedure
    "著作权法",
    "商标法",
    "专利法",
    "反垄断法",
    "广告法",
    "电影产业促进法",
    "消费者权益保护法",
    "电子签名法",
    "电子商务法",
    "劳动法",
    "劳动合同法",
    "劳动争议调解仲裁法",
    "数据安全法",
    "个人信息保护法",
    "公司法",
    "外商投资法",
    "民事诉讼法",
    # Tax (v0.3.0 — for jp-cn-tax skills)
    "个人所得税法",
    "企业所得税法",
    "增值税法",
    "印花税法",
    "关税法",
    "税收征收管理法",
    "资源税法",
    "城市维护建设税法",
    "契税法",
    "环境保护税法",
    "耕地占用税法",
    "烟叶税法",
    "船舶吨税法",
    "车船税法",
    "车辆购置税法",
]

# Laws maintained by the project owner. The scraper does NOT touch these files.
# Refresh them via refresh_cn_corpus.py from authoritative .docx sources.
OWNER_MAINTAINED_LAWS = {
    "民法典": "Owner-maintained from authoritative .docx (1260 articles).",
    "反不正当竞争法": "2025-06-27 第二次修订; LawRefBook stuck at 2019-04-23.",
    "网络安全法": "2025-10-28 修正; LawRefBook stuck at 2016-11-07.",
    "仲裁法": "2025-09-12 修订; LawRefBook stuck at 2017-09-01.",
}


def find_latest(repo_root: Path, stem: str):
    """Find the most recently dated version of {stem}.md across SEARCH_DIRS.

    LawRefBook names files like 反垄断法(2022-06-24).md. We pick the file with
    the largest date. Undated files (just {stem}.md) are treated as oldest.
    Returns (date_str, path) or None.
    """
    dated = re.compile(rf"^{re.escape(stem)}\((\d{{4}}-\d{{2}}-\d{{2}})\)\.md$")
    plain = re.compile(rf"^{re.escape(stem)}\.md$")
    candidates = []
    for d in SEARCH_DIRS:
        sub = repo_root / d
        if not sub.is_dir():
            continue
        for f in sub.iterdir():
            m = dated.match(f.name)
            if m:
                candidates.append((m.group(1), f))
                continue
            if plain.match(f.name):
                candidates.append(("0000-00-00", f))
    if not candidates:
        return None
    candidates.sort(key=lambda c: c[0], reverse=True)
    return candidates[0]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="lrb-") as tmpdir:
        tmp = Path(tmpdir)
        print(f"[clone] {LRB_REPO}", flush=True)
        result = subprocess.run(
            ["git", "clone", "--depth", "1", LRB_REPO, str(tmp)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"  ✗ git clone failed: {result.stderr.strip()}", flush=True)
            sys.exit(1)
        print(f"  ✓ cloned", flush=True)

        updated = 0
        failed = 0
        for stem in LRB_SOURCED_LAWS:
            found = find_latest(tmp, stem)
            if found is None:
                print(f"  ✗ {stem}: not found in LawRefBook", flush=True)
                failed += 1
                continue
            date, src = found
            dest = out_dir / f"{stem}.md"
            shutil.copy2(src, dest)
            rel = src.relative_to(tmp)
            print(f"  ✓ {stem}.md ← {rel} (date {date})", flush=True)
            updated += 1

        print(f"\n[owner-maintained, skipped]")
        for stem, reason in OWNER_MAINTAINED_LAWS.items():
            print(f"  · {stem}.md  ({reason})", flush=True)

        print(f"\nUpdated: {updated}, failed: {failed}")
        if failed:
            sys.exit(1)


if __name__ == "__main__":
    main()
