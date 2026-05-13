#!/usr/bin/env python3
"""Refresh the bundled PRC core statutes from a directory of .docx files.

Use case: the bundled core statutes are point-in-time. When a law gets
amended (反不正当竞争法 2025-06, 网络安全法 2025-10, etc.), the user
downloads the latest .docx from 国家法律法规数据库 (flk.npc.gov.cn) on a
network that can reach .cn, drops the docx in an input directory, and
runs this script. The script converts to Markdown and overwrites the
bundled file — no plugin reinstall needed.

Usage:
  python3 refresh_cn_corpus.py /path/to/dir/of/new/docx
  python3 refresh_cn_corpus.py /path/to/single/file.docx
  python3 refresh_cn_corpus.py /path/to/dir/ --add  # add new laws, don't overwrite

The script preserves the existing references/cn_laws/ directory layout.
"""
import argparse
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

# Names mapping: 国家法律法规数据库 official title → bundled filename stem
DEFAULT_NAME_MAP = {
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


def extract_paragraphs(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        with z.open("word/document.xml") as f:
            tree = ET.parse(f)
    body = tree.getroot().find("w:body", NS)
    for p in body.findall("w:p", NS):
        runs = p.findall(".//w:t", NS)
        text = "".join((r.text or "") for r in runs).strip()
        yield text


def classify(text):
    if not text:
        return "blank"
    if re.match(r"^第[一二三四五六七八九十百千]+编[^条]*$", text):
        return "book"
    if re.match(r"^第[一二三四五六七八九十百千]+章", text) and "条" not in text:
        return "chapter"
    if re.match(r"^第[一二三四五六七八九十百千]+节", text) and "条" not in text:
        return "section"
    if re.match(r"^第[一二三四五六七八九十百千零]+条", text):
        return "article"
    if text.startswith("中华人民共和国") and len(text) < 60:
        return "title"
    return "body"


def convert_docx(docx_path, out_path):
    lines = []
    title_set = False
    for text in extract_paragraphs(docx_path):
        if not text:
            continue
        kind = classify(text)
        if kind == "title" and not title_set:
            lines.append(f"# {text}")
            lines.append("")
            title_set = True
        elif kind == "book":
            lines.append(f"\n## {text}\n")
        elif kind == "chapter":
            level = "##" if title_set else "#"
            lines.append(f"\n{level} {text}\n")
        elif kind == "section":
            lines.append(f"\n### {text}\n")
        elif kind == "article":
            lines.append(f"\n#### {text}")
        else:
            lines.append(text)
    out = "\n".join(lines)
    out = re.sub(r"\n{3,}", "\n\n", out)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    return len(out)


def title_of(docx_path):
    """Infer law title from the docx file content (look at first non-blank line that starts with 中华人民共和国)."""
    for text in extract_paragraphs(docx_path):
        if text.startswith("中华人民共和国") and "_" not in text and len(text) < 60:
            return text
    # Fall back to filename
    base = os.path.basename(docx_path).replace(".docx", "")
    return re.sub(r"_\d{8}$", "", base)


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("source", help="docx file, or directory containing docx files")
    p.add_argument("--add", action="store_true",
                   help="Add new laws (not just overwrite existing). New filename = title.md")
    p.add_argument("--out-dir", default=None,
                   help="Override output directory (default: ../../../references/cn_laws/)")
    args = p.parse_args()

    if args.out_dir:
        out_dir = args.out_dir
    else:
        out_dir = os.path.normpath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "..", "..", "references", "cn_laws"
        ))
    os.makedirs(out_dir, exist_ok=True)

    # Collect input docx files
    if os.path.isfile(args.source):
        sources = [args.source]
    elif os.path.isdir(args.source):
        sources = sorted(
            os.path.join(args.source, f)
            for f in os.listdir(args.source)
            if f.endswith(".docx") and not f.startswith("~$")
        )
    else:
        print(f"Source not found: {args.source}", file=sys.stderr)
        sys.exit(1)

    updated, added, skipped = 0, 0, 0
    for src in sources:
        try:
            title = title_of(src)
        except Exception as e:
            print(f"  ✗ {os.path.basename(src)} — could not parse: {e}")
            skipped += 1
            continue

        stem = DEFAULT_NAME_MAP.get(title)
        if stem is None:
            if not args.add:
                print(f"  - {title} — not in core map, skipping (use --add to include)")
                skipped += 1
                continue
            # Use the official title as the filename
            stem = title.replace("中华人民共和国", "").strip()

        out_path = os.path.join(out_dir, f"{stem}.md")
        existed = os.path.exists(out_path)
        size = convert_docx(src, out_path)
        if existed:
            print(f"  ✓ {title}  →  {stem}.md  (updated, {size/1024:.1f} KB)")
            updated += 1
        else:
            print(f"  + {title}  →  {stem}.md  (added, {size/1024:.1f} KB)")
            added += 1

    print(f"\nUpdated: {updated}, added: {added}, skipped: {skipped}")
    print(f"Out dir: {out_dir}")


if __name__ == "__main__":
    main()
