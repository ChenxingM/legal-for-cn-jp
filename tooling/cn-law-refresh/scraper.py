#!/usr/bin/env python3
"""Scrape latest PRC core statutes from flk.npc.gov.cn.

Designed to run on GitHub Actions runners (US/EU IPs that can reach .cn
even when the user's corporate network cannot).

Usage:
  python3 scraper.py --out-dir /path/to/cn_laws/

What it does:
  1. Queries the unofficial flk.npc.gov.cn API for the latest version of
     each law in CORE_LAWS.
  2. Downloads the WORD (.docx) file for each.
  3. Converts to clean Markdown and writes to --out-dir.

The unofficial API was documented by github.com/twang2218/law-datasets.
Endpoints used:
  GET https://flk.npc.gov.cn/api/?type=flsearch&searchType=title%3Bvague&page=1&size=10&...
  GET https://flk.npc.gov.cn/api/?type=detail&id=...
  GET https://wb.flk.npc.gov.cn/... (WORD file CDN)
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

API = "https://flk.npc.gov.cn/api/"
CDN = "https://wb.flk.npc.gov.cn"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

UA = "Mozilla/5.0 (legal-for-cn-jp scraper; +https://github.com/ChenxingM/legal-for-cn-jp)"

# Mapping: official title → bundled filename stem
CORE_LAWS = {
    "中华人民共和国著作权法": "著作权法",
    "中华人民共和国商标法": "商标法",
    "中华人民共和国专利法": "专利法",
    "中华人民共和国反不正当竞争法": "反不正当竞争法",
    "中华人民共和国反垄断法": "反垄断法",
    "中华人民共和国广告法": "广告法",
    "中华人民共和国电影产业促进法": "电影产业促进法",
    "中华人民共和国民法典": "民法典",
    "中华人民共和国消费者权益保护法": "消费者权益保护法",
    "中华人民共和国电子签名法": "电子签名法",
    "中华人民共和国电子商务法": "电子商务法",
    "中华人民共和国劳动法": "劳动法",
    "中华人民共和国劳动合同法": "劳动合同法",
    "中华人民共和国劳动争议调解仲裁法": "劳动争议调解仲裁法",
    "中华人民共和国网络安全法": "网络安全法",
    "中华人民共和国数据安全法": "数据安全法",
    "中华人民共和国个人信息保护法": "个人信息保护法",
    "中华人民共和国公司法": "公司法",
    "中华人民共和国外商投资法": "外商投资法",
    "中华人民共和国民事诉讼法": "民事诉讼法",
    "中华人民共和国仲裁法": "仲裁法",
    # Add these for v0.2.1 once we confirm scraper works:
    # "信息网络传播权保护条例": "信息网络传播权保护条例",
    # "计算机软件保护条例": "计算机软件保护条例",
}


def http_get(url, timeout=30, retries=3):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json,*/*"})
    last = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(2 ** i)
    raise last


def search_law(title):
    """Search for a law by exact title. Returns the latest record id."""
    params = {
        "type": "flsearch",
        "searchType": "title;vague",
        "sortTr": "f_bbrq_s;desc",
        "page": "1",
        "size": "10",
        "title": title,
        "_": str(int(time.time() * 1000)),
    }
    url = API + "?" + urllib.parse.urlencode(params)
    data = json.loads(http_get(url))
    if data.get("code") != 200:
        return None
    laws = data.get("result", {}).get("data", [])
    # Take the first that is 法律, status=1 (有效), exact title match
    for law in laws:
        if law.get("title") == title and law.get("status") == "1" and law.get("type") == "法律":
            return law
    # Fallback: any with this exact title
    for law in laws:
        if law.get("title") == title:
            return law
    return None


def get_detail(law_id):
    """Fetch detail to get the download links."""
    params = {"type": "detail", "id": law_id, "_": str(int(time.time() * 1000))}
    url = API + "?" + urllib.parse.urlencode(params)
    data = json.loads(http_get(url))
    if data.get("code") != 200:
        return None
    body = data.get("result", {}).get("body", [])
    for item in body:
        if item.get("type") == "WORD":
            return CDN + item["path"]
    # No WORD; try HTML
    for item in body:
        if item.get("type") == "HTML":
            return CDN + item["url"]
    return None


def docx_to_md(docx_bytes, out_path):
    """Convert docx bytes to Markdown."""
    import io
    z = zipfile.ZipFile(io.BytesIO(docx_bytes))
    with z.open("word/document.xml") as f:
        tree = ET.parse(f)
    body = tree.getroot().find("w:body", NS)

    lines = []
    title_set = False
    for p in body.findall("w:p", NS):
        runs = p.findall(".//w:t", NS)
        text = "".join((r.text or "") for r in runs).strip()
        if not text:
            continue
        if re.match(r"^第[一二三四五六七八九十百千]+编[^条]*$", text):
            lines.append(f"\n## {text}\n")
        elif re.match(r"^第[一二三四五六七八九十百千]+章", text) and "条" not in text:
            lines.append(f"\n{'##' if title_set else '#'} {text}\n")
        elif re.match(r"^第[一二三四五六七八九十百千]+节", text) and "条" not in text:
            lines.append(f"\n### {text}\n")
        elif re.match(r"^第[一二三四五六七八九十百千零]+条", text):
            lines.append(f"\n#### {text}")
        elif text.startswith("中华人民共和国") and not title_set and len(text) < 60:
            lines.append(f"# {text}\n")
            title_set = True
        else:
            lines.append(text)

    out = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    return len(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    updated = 0
    failed = 0
    for title, stem in CORE_LAWS.items():
        try:
            print(f"[{title}]", flush=True)
            law = search_law(title)
            if not law:
                print(f"  ✗ not found", flush=True)
                failed += 1
                continue
            print(f"  publish: {law['publish']}  status: {law.get('status')}")
            url = get_detail(law["id"])
            if not url:
                print(f"  ✗ no WORD link", flush=True)
                failed += 1
                continue
            docx_bytes = http_get(url, timeout=60)
            out_path = os.path.join(args.out_dir, f"{stem}.md")
            size = docx_to_md(docx_bytes, out_path)
            print(f"  ✓ {stem}.md ({size/1024:.1f} KB)", flush=True)
            updated += 1
            time.sleep(1)  # be polite
        except Exception as e:
            print(f"  ✗ error: {e}", flush=True)
            failed += 1

    print(f"\nUpdated: {updated}, failed: {failed}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
