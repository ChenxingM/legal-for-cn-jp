#!/usr/bin/env python3
"""HuggingFace client for the `twang2218/chinese-law-and-regulations` dataset.

Provides PRC law lookup that works even when flk.npc.gov.cn is blocked at
the corporate-network level. The dataset is a pandoc-converted Markdown
dump of the 国家法律法规数据库 as of 2023-09 (22,552 records).

Subcommands:
  search <query>          Search the bundled index by title fragment
  fetch <offset>          Get the full text of a law by its index offset
  fetch-title <title>     Search by title, fetch the top hit

Network requirement: HTTPS to huggingface.co and datasets-server.huggingface.co.
"""
import argparse
import csv
import json
import os
import sys
import urllib.parse
import urllib.request

DATASET = "twang2218/chinese-law-and-regulations"
API_BASE = "https://datasets-server.huggingface.co"

# Index file is bundled alongside the plugin
DEFAULT_INDEX = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", "references", "cn-law-index.csv"
)

USER_AGENT = "legal-for-cn-jp/0.2 (HuggingFace dataset client)"


def http_get_json(url: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_index(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cmd_search(args):
    """Search the bundled index by title fragment. No network needed."""
    rows = load_index(args.index)
    q = args.query
    hits = []
    for r in rows:
        if q in r["title"]:
            if args.law_type and args.law_type not in r["type"]:
                continue
            if args.office_level and args.office_level not in r["office_level"]:
                continue
            hits.append(r)
            if len(hits) >= args.limit:
                break
    out = {
        "query": q,
        "hits": len(hits),
        "results": [
            {
                "offset": int(r["offset"]),
                "title": r["title"],
                "type": r["type"],
                "office": r["office"],
                "publish_date": r["publish_date"],
                "effective_date": r["effective_date"],
                "status": r["status"],
            }
            for r in hits
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def fetch_offset(offset: int) -> dict:
    """Fetch one law's full record from the HuggingFace rows API."""
    url = f"{API_BASE}/rows?" + urllib.parse.urlencode({
        "dataset": DATASET,
        "config": "default",
        "split": "train",
        "offset": offset,
        "length": 1,
    })
    data = http_get_json(url)
    if "rows" not in data or not data["rows"]:
        return {"error": True, "message": data.get("error", "no rows")}
    return data["rows"][0]["row"]


def cmd_fetch(args):
    """Fetch a law by its dataset offset."""
    row = fetch_offset(args.offset)
    if row.get("error"):
        print(json.dumps(row, ensure_ascii=False, indent=2))
        return
    out = {
        "offset": args.offset,
        "title": row.get("title"),
        "type": row.get("type"),
        "office": row.get("office"),
        "office_level": row.get("office_level"),
        "publish_date": str(row.get("publish_date") or "")[:10],
        "effective_date": str(row.get("effective_date") or "")[:10],
        "status": row.get("status"),
        "content": row.get("content") or "",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_fetch_title(args):
    """Search index for title, fetch the best hit's full text."""
    rows = load_index(args.index)
    candidates = [r for r in rows if args.title in r["title"]]
    if not candidates:
        print(json.dumps({"error": True, "message": f"No law matching '{args.title}'"},
                         ensure_ascii=False, indent=2))
        return
    # Prefer 法律 over 行政法规 over others, then most recent publish_date
    type_rank = {"法律": 0, "宪法": 1, "行政法规": 2, "司法解释": 3, "监察法规": 4}
    candidates.sort(key=lambda r: (type_rank.get(r["type"], 99), -int(r["publish_date"].replace("-", "") or "0")))
    pick = candidates[0]
    row = fetch_offset(int(pick["offset"]))
    if row.get("error"):
        print(json.dumps(row, ensure_ascii=False, indent=2))
        return
    out = {
        "offset": int(pick["offset"]),
        "title": row.get("title"),
        "type": row.get("type"),
        "office": row.get("office"),
        "publish_date": str(row.get("publish_date") or "")[:10],
        "effective_date": str(row.get("effective_date") or "")[:10],
        "content": row.get("content") or "",
        "other_matches": [
            {"offset": int(r["offset"]), "title": r["title"], "type": r["type"], "publish_date": r["publish_date"]}
            for r in candidates[1:5]
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(
        description="HuggingFace client for twang2218/chinese-law-and-regulations"
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="Search bundled index by title fragment (no network)")
    s.add_argument("query")
    s.add_argument("--law-type", default=None, help='Filter by type: 法律, 行政法规, 司法解释, etc.')
    s.add_argument("--office-level", default=None, help="Filter by issuing body: 全国人民代表大会, 国务院, etc.")
    s.add_argument("--index", default=DEFAULT_INDEX)
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(func=cmd_search)

    f = sub.add_parser("fetch", help="Fetch a law's full text by dataset offset")
    f.add_argument("offset", type=int)
    f.set_defaults(func=cmd_fetch)

    ft = sub.add_parser("fetch-title", help="Search by title, return full text of top match")
    ft.add_argument("title")
    ft.add_argument("--index", default=DEFAULT_INDEX)
    ft.set_defaults(func=cmd_fetch_title)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
