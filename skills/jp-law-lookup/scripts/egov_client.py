#!/usr/bin/env python3
"""e-Gov 法令API v2 Client

CLI wrapper for https://laws.e-gov.go.jp/api/2/
No API key required.

Subcommands:
  search <title>            Search by partial law title
  keyword <term>            Full-text search across all laws
  fetch <law_id>            Get the full text of a law
  revisions <law_id>        List historical revisions of a law

All output is JSON to stdout for easy parsing.
For fetch, the law_full_text field is returned in plain text form
(stripped of XML tags) suitable for direct context use.
"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

API_BASE = "https://laws.e-gov.go.jp/api/2"
USER_AGENT = "legal-for-cn-jp/0.1 (e-Gov API client)"


def http_get(path: str, params: dict | None = None) -> dict:
    """Issue a GET request to the e-Gov API and return JSON."""
    url = f"{API_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": True, "status": e.code, "body": body[:500]}
    except Exception as e:
        return {"error": True, "message": str(e)}


def cmd_search(args):
    """Search by law title (partial match)."""
    data = http_get("/laws", {
        "law_title": args.title,
        "law_type": args.law_type,
        "limit": args.limit,
    })
    # Trim payload for readability
    if "laws" in data:
        out = []
        for it in data["laws"]:
            info = it.get("law_info", {}) or {}
            rev = it.get("revision_info", {}) or {}
            out.append({
                "law_id": info.get("law_id"),
                "law_num": info.get("law_num"),
                "title": rev.get("law_title") or info.get("law_title"),
                "law_type": info.get("law_type"),
                "promulgation_date": info.get("promulgation_date"),
            })
        print(json.dumps({"hits": len(out), "results": out}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_keyword(args):
    """Full-text keyword search across all laws."""
    data = http_get("/keyword", {
        "keyword": args.keyword,
        "law_type": args.law_type,
        "limit": args.limit,
        "sentences_limit": args.sentences_limit,
        "sentence_text_size": args.sentence_text_size,
        "highlight_tag": "mark",
    })
    if "items" in data:
        out = []
        for it in data["items"]:
            info = it.get("law_info", {}) or {}
            rev = it.get("revision_info", {}) or {}
            snippets = []
            for s in (it.get("sentences") or [])[:args.sentences_limit]:
                txt = s.get("text") or ""
                # Strip our own highlight tag for plain text output
                txt = re.sub(r"</?mark>", "", txt)
                snippets.append({
                    "position": s.get("position"),
                    "text": txt,
                })
            out.append({
                "law_id": info.get("law_id"),
                "title": rev.get("law_title") or info.get("law_title"),
                "law_type": info.get("law_type"),
                "snippets": snippets,
            })
        print(json.dumps({"total_count": data.get("total_count"), "hits": out},
                         ensure_ascii=False, indent=2))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def xml_to_text(xml_str: str) -> str:
    """Convert e-Gov law XML to a plain text dump preserving article structure."""
    try:
        root = ET.fromstring(xml_str)
    except ET.ParseError:
        # Maybe already text; return as-is
        return xml_str
    lines = []
    title_elem = root.find(".//LawTitle")
    law_num_elem = root.find(".//LawNum")
    if title_elem is not None:
        lines.append(f"# {''.join(title_elem.itertext()).strip()}")
    if law_num_elem is not None:
        lines.append(f"法令番号: {''.join(law_num_elem.itertext()).strip()}")
    lines.append("")

    def walk(elem, depth=0):
        tag = elem.tag
        if tag in ("ChapterTitle", "SectionTitle", "SubsectionTitle", "PartTitle", "DivisionTitle"):
            lines.append("\n" + "#" * (depth + 2) + " " + "".join(elem.itertext()).strip())
        elif tag == "ArticleTitle":
            lines.append("\n## " + "".join(elem.itertext()).strip())
        elif tag == "ArticleCaption":
            lines.append("(" + "".join(elem.itertext()).strip().strip("（）()") + ")")
        elif tag == "ParagraphSentence" or tag == "ItemSentence":
            lines.append("".join(elem.itertext()).strip())
        elif tag == "ItemTitle":
            lines.append("\n- " + "".join(elem.itertext()).strip() + " ")
        for child in elem:
            walk(child, depth + 1)

    main = root.find(".//MainProvision")
    if main is not None:
        walk(main)
    text = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", text)


def cmd_fetch(args):
    """Get the full text of a single law."""
    params = {
        "law_full_text_format": "xml",
        "response_format": "json",
    }
    if args.asof:
        params["asof"] = args.asof
    data = http_get(f"/law_data/{urllib.parse.quote(args.law_id)}", params)
    if "law_full_text" in data:
        text = data["law_full_text"]
        if isinstance(text, dict):
            text = json.dumps(text, ensure_ascii=False)
        # If XML, convert to readable text
        if text.lstrip().startswith("<"):
            text = xml_to_text(text)
        info = data.get("law_info", {}) or {}
        rev = data.get("revision_info", {}) or {}
        out = {
            "law_id": info.get("law_id"),
            "law_num": info.get("law_num"),
            "title": rev.get("law_title") or info.get("law_title"),
            "promulgation_date": info.get("promulgation_date"),
            "amendment_date": rev.get("amendment_promulgate_date"),
            "text": text,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_revisions(args):
    """List historical revisions of a law."""
    data = http_get(f"/law_revisions/{urllib.parse.quote(args.law_id)}")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(description="e-Gov 法令API v2 client")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="Search by law title (partial match)")
    s.add_argument("title", help="Law title fragment (Japanese)")
    s.add_argument("--law-type", default=None,
                   help="Filter by type: Act, CabinetOrder, MinisterialOrdinance, Rule, etc.")
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(func=cmd_search)

    k = sub.add_parser("keyword", help="Full-text keyword search across all laws")
    k.add_argument("keyword", help="Keyword (supports AND, OR, NOT, wildcards)")
    k.add_argument("--law-type", default="Act")
    k.add_argument("--limit", type=int, default=10)
    k.add_argument("--sentences-limit", type=int, default=3)
    k.add_argument("--sentence-text-size", type=int, default=120)
    k.set_defaults(func=cmd_keyword)

    f = sub.add_parser("fetch", help="Get the full text of a law")
    f.add_argument("law_id", help="Law ID (e.g. 345AC0000000048) or law number")
    f.add_argument("--asof", default=None, help="Get text as of a specific date (YYYY-MM-DD)")
    f.set_defaults(func=cmd_fetch)

    r = sub.add_parser("revisions", help="List historical revisions of a law")
    r.add_argument("law_id")
    r.set_defaults(func=cmd_revisions)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
