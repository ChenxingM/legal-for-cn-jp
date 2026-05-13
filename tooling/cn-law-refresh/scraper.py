#!/usr/bin/env python3
"""Scrape latest PRC core statutes from flk.npc.gov.cn.

Designed to run on GitHub Actions runners (US/EU IPs that can reach .cn
even when the user's corporate network cannot).

Usage:
  python3 scraper.py --out-dir /path/to/cn_laws/

What it does:
  1. Bootstraps a session by GET-ing the homepage to receive Set-Cookie.
  2. Queries the unofficial flk.npc.gov.cn API for the latest version of
     each law in CORE_LAWS, with browser-like headers and the session cookie.
  3. Downloads the WORD (.docx) file for each.
  4. Converts to clean Markdown and writes to --out-dir.

The unofficial API was documented by github.com/twang2218/law-datasets.
Endpoints used:
  GET https://flk.npc.gov.cn/api/?type=flsearch&searchType=title%3Bvague&page=1&size=10&...
  GET https://flk.npc.gov.cn/api/?type=detail&id=...
  GET https://wb.flk.npc.gov.cn/... (WORD file CDN)
"""
import argparse
import http.cookiejar
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

HOME = "https://flk.npc.gov.cn/"
API = "https://flk.npc.gov.cn/api/"
CDN = "https://wb.flk.npc.gov.cn"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

# Browser-like headers. flk.npc.gov.cn returns empty 200 to "polite bot" UAs
# without a Referer, so we present as Chrome and always send Referer/Accept-Language.
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
BASE_HEADERS = {
    "User-Agent": UA,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": HOME,
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

# Module-level cookie-aware opener so flsearch/detail calls share session state.
COOKIE_JAR = http.cookiejar.CookieJar()
OPENER = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(COOKIE_JAR))

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
}


def http_get(url, timeout=30, retries=3, extra_headers=None):
    """GET with browser-like headers and cookie session. Returns response bytes."""
    headers = dict(BASE_HEADERS)
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    last = None
    for i in range(retries):
        try:
            with OPENER.open(req, timeout=timeout) as r:
                body = r.read()
                if not body.strip():
                    # Diagnostic: empty body almost always = anti-bot block
                    print(
                        f"  ⚠ empty body. status={r.status} "
                        f"content-type={r.headers.get('Content-Type')!r} "
                        f"content-length={r.headers.get('Content-Length')!r}",
                        flush=True,
                    )
                return body
        except Exception as e:
            last = e
            time.sleep(2 ** i)
    raise last


def bootstrap_session():
    """GET the homepage so the server sets session cookies on COOKIE_JAR."""
    print(f"[bootstrap] GET {HOME}", flush=True)
    headers = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    req = urllib.request.Request(HOME, headers=headers)
    with OPENER.open(req, timeout=30) as r:
        _ = r.read()
        cookies = [c.name for c in COOKIE_JAR]
        print(f"[bootstrap] status={r.status} cookies={cookies}", flush=True)


def _parse_json(body, ctx):
    """Parse JSON or print diagnostic body preview and return None."""
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        print(f"  ✗ JSON parse error in {ctx}: {e}", flush=True)
        preview = body[:500] if isinstance(body, (bytes, bytearray)) else str(body)[:500]
        print(f"    body preview ({len(body)} bytes): {preview!r}", flush=True)
        return None


def search_law(title):
    """Search for a law by exact title. Returns the latest record dict."""
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
    body = http_get(url)
    data = _parse_json(body, "search_law")
    if data is None or data.get("code") != 200:
        return None
    laws = data.get("result", {}).get("data", [])
    for law in laws:
        if law.get("title") == title and law.get("status") == "1" and law.get("type") == "法律":
            return law
    for law in laws:
        if law.get("title") == title:
            return law
    return None


def get_detail(law_id):
    """Fetch detail to get the download links."""
    params = {"type": "detail", "id": law_id, "_": str(int(time.time() * 1000))}
    url = API + "?" + urllib.parse.urlencode(params)
    body = http_get(url)
    data = _parse_json(body, "get_detail")
    if data is None or data.get("code") != 200:
        return None
    items = data.get("result", {}).get("body", [])
    for item in items:
        if item.get("type") == "WORD":
            return CDN + item["path"]
    for item in items:
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

    bootstrap_session()

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
            print(f"  publish: {law.get('publish')}  status: {law.get('status')}", flush=True)
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
            time.sleep(1)
        except Exception as e:
            print(f"  ✗ error: {e}", flush=True)
            failed += 1

    print(f"\nUpdated: {updated}, failed: {failed}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
