---
name: jp-law-lookup
description: Look up Japanese statutory law — find the text of a specific article, search by keyword across all current laws, list a law's revision history. Use when the user asks "what does Article X of [law] say", "find the rule on [topic] in Japanese law", "show me 著作権法第30条", "search laws for [term]", "is there a Japanese law that covers [topic]", or any question that requires the actual statutory text rather than a general answer.
---

# Japanese statute lookup

Answer questions about Japanese statutory law by retrieving the actual text — not by reciting from training data, which is likely out of date.

## Decision tree

When the user asks for the text or substance of a Japanese law, follow this order:

1. **Is the law one of the 16 bundled core statutes?** Check `~~/references/laws/` (relative to plugin root). If yes, read it directly — fastest and free of network risk.
2. **If not bundled, is the law name known?** Look it up in `~~/references/law-index.csv` to get the `law_id`, then fetch via the e-Gov API.
3. **If the user asked a topic question** (e.g. "what does Japanese law say about deepfakes"), run a keyword search via the e-Gov API across all 10,000+ laws.

## Bundled core statutes

These 16 laws live in `references/laws/` as cleaned Markdown — full current text. **Read them with the Read tool before fetching anything remote.** Reading them takes one tool call and zero seconds of network latency.

| File | Use for |
|---|---|
| `著作権法.md` | Copyright — ownership, 二次利用, 私的複製, 引用, 著作者人格権, 罰則 |
| `著作権等管理事業法.md` | JASRAC and other management organizations |
| `民法.md` | Contracts, torts, agency, succession — the base civil code |
| `労働基準法.md` | Working hours, overtime, wages, leave |
| `労働契約法.md` | Employment contract formation, termination, fixed-term rules |
| `労働者派遣法.md` | Dispatched workers — distinguish from outsourcing |
| `不正競争防止法.md` | Trade secret, slavish imitation, well-known mark abuse |
| `個人情報保護法.md` | APPI — personal data handling |
| `商標法.md` | Trademark registration and enforcement |
| `意匠法.md` | Design rights |
| `特許法.md` | Patents |
| `映画盗撮防止法.md` | Theatrical recording ban |
| `プロバイダ責任制限法.md` | Notice-and-takedown for online infringement |
| `消費者契約法.md` | Consumer contract rules |
| `独占禁止法.md` | Antitrust, 優越的地位の濫用 |
| `景品表示法.md` | Advertising rules |

## e-Gov API client

For any law outside the bundled set, use the API client at `scripts/egov_client.py`. Run it via the Bash tool:

```bash
# Search by partial title — returns law_id you can use to fetch
python3 ~~/skills/jp-law-lookup/scripts/egov_client.py search "建築基準" --limit 5

# Full-text keyword search across all Acts
python3 ~~/skills/jp-law-lookup/scripts/egov_client.py keyword "ディープフェイク" --limit 10

# Fetch the full current text of a law by ID
python3 ~~/skills/jp-law-lookup/scripts/egov_client.py fetch 345AC0000000048

# Fetch as it stood on a specific date (for historical research)
python3 ~~/skills/jp-law-lookup/scripts/egov_client.py fetch 345AC0000000048 --asof 2020-04-01

# Get revision history
python3 ~~/skills/jp-law-lookup/scripts/egov_client.py revisions 345AC0000000048
```

The script reads no credentials. No setup needed — the e-Gov API is open. Output is always JSON to stdout.

## How to answer

When citing law:

- Quote the article text verbatim when it matters. Paraphrase when summarizing.
- Always include the article number AND the law name in citations: 「著作権法第30条第1項」not just "Article 30".
- If you fetched from the API, mention the asof date so the user knows when the text was current.
- If the answer involves recent amendments or unsettled interpretation, say so plainly — the bundled corpus is a point-in-time snapshot.

## Output policy

### Citations

Every legal or license conclusion MUST anchor to a specific provision and link to an authoritative source. Never paraphrase a rule without a citation.

- **Japanese statutes**: cite `法令名 第X条第Y項第Z号` and link e-Gov as `https://laws.e-gov.go.jp/law/<法令ID>`. The 法令ID for bundled laws is in `~~/references/law-index.csv`; if unknown, link the e-Gov search home `https://laws.e-gov.go.jp/` instead.
- **下請法系 (not in e-Gov)**: link 公正取引委員会 `https://www.jftc.go.jp/shitauke/legislation/`.
- **PRC statutes**: cite `法律名 第X条第Y款第Z项` and link the 国家法律法规数据库 `https://flk.npc.gov.cn/` (note: 2026 SPA migration — specific URLs are not stable, link the landing page). For LawRefBook-synced files also link the GitHub mirror `https://github.com/LawRefBook/Laws/blob/master/<dir>/<file>(<date>).md`.
- **OSS licenses**: cite the SPDX identifier and link the SPDX page `https://spdx.org/licenses/<SPDX-ID>.html`, plus the upstream project's `LICENSE` file URL when relevant.
- **Cases / 判例 / 裁判文书**: out of scope until v0.4.0 — disclose if asked.

Never invent article numbers or URLs. If you can't cite the controlling provision, say so and offer to look it up via `jp-law-lookup` or `cn-law-lookup`.

### Output language

Match the user's input language:
- 日本語 input → 日本語 output
- 中文 input → 中文 output
- English input → English output
- Mixed input → primary language of the question (the language the user uses to ask, not the language of the statute being asked about)

条文名・固有名詞・専門用語・法律名 / 法律条文 / 法律术语 stay in their original language. Translate only commentary and analysis.

## Hard limits

- This skill returns statutory text. It does not give legal advice.
- Japanese case law (判例) is not bundled and the API does not provide it. Tell the user that case-law analysis requires the case-lookup skill (coming in v0.2.0) or external research.
- Ministerial guidance (ガイドライン, 通達, 告示) is partially in the index but treat it as secondary — flag where the legal weight is regulatory guidance rather than statute.
- For any question that calls for professional judgment ("can we be sued for", "is this enforceable"), recommend the user consult a bengoshi.
