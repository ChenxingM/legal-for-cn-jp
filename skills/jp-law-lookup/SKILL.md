---
name: jp-law-lookup
description: Look up Japanese statutory law — find the text of a specific article, search by keyword across all current laws, list a law's revision history. **CRITICAL invocation contract: (1) ALWAYS respond in the user's input language — 中文 question → 中文 answer, 日本語 question → 日本語 answer, English → English; statute names and quoted articles stay in original Japanese, but ALL commentary/headings/conclusion follow the user's language. (2) Bundled laws (16 in `~~/references/laws/` + 5 下請法系) MUST be Read via Read tool before quoting; for unbundled laws use the e-Gov API client. (3) QUOTE the controlling article verbatim. (4) NEVER reference the user's name/employer/role. (5) NEVER invent 法令ID — use the table in this skill or fetch via e-Gov API.** Use when the user asks "what does Article X of [law] say", "find the rule on [topic] in Japanese law", "show me 著作権法第30条", "search laws for [term]", "is there a Japanese law that covers [topic]", or any question that requires the actual statutory text rather than a general answer.
---

# Japanese statute lookup

> **LANGUAGE FIRST — match the user's input language, not the statute's language.**
> 日本語 question → 日本語 answer. 中文 提问 → 中文 回答. English question → English answer.
> Statute names (法令名) and quoted article text stay in their original language. ALL commentary, headings, conclusion, and analysis follow the user's input language. A Chinese question about a Japanese statute gets a Chinese answer with Japanese article text quoted verbatim.

> **MANDATORY STEPS — DO NOT SKIP, EVEN FOR "SIMPLE" QUESTIONS.**
>
> 1. **READ via Read tool**: if the law is in the bundled table below, read `~~/references/laws/<file>.md` directly before answering. For unbundled laws, use the e-Gov API client (see below). **Do not paraphrase from training data — your knowledge of these statutes is stale.**
> 2. **QUOTE the controlling article verbatim** before paraphrasing it. Citing only "第X条" without the article's actual text is insufficient proof that you read the source — the user can't verify your reasoning without seeing the text.
> 3. **CITE every quoted or paraphrased rule** with `法令名 第X条第Y項第Z号` + the e-Gov URL from the table (format: `https://laws.e-gov.go.jp/law/<法令ID>`). For 下請法系 (not in e-Gov): link 公取委 URLs (see `jp-subcontract-review` skill). **Never invent article numbers or URLs** — if you don't have the ID in the table, fetch via the e-Gov API client below.
> 4. **MATCH user's input language**: 日本語 input → 日本語 output, 中文 input → 中文 output, English input → English output. 条文名・固有名詞・専門用語・法律名 stay native; translate only commentary.

**ANTI-PATTERNS — DO NOT REPRODUCE:**

❌ Article numbers without quoted text or URL — looks like you read but didn't.
❌ Referencing user's employer/role/affiliation from email or memory.
❌ Inventing 法令ID for laws not in the bundled table — fetch via the e-Gov API client below, do not guess.
❌ Trailing apologies about uncertainty — if uncertain, run the API client and check.

**REQUIRED PATTERN:**

```
**民法 第632条（請負）** [e-Gov 129AC0000000089: https://laws.e-gov.go.jp/law/129AC0000000089]

> [exact text from `~~/references/laws/民法.md`]
```

Answer questions about Japanese statutory law by retrieving the actual text — not by reciting from training data, which is likely out of date.

## Decision tree

When the user asks for the text or substance of a Japanese law, follow this order:

1. **Is the law one of the 16 bundled core statutes?** Check `~~/references/laws/` (relative to plugin root). If yes, read it directly — fastest and free of network risk.
2. **If not bundled, is the law name known?** Look it up in `~~/references/law-index.csv` to get the `law_id`, then fetch via the e-Gov API.
3. **If the user asked a topic question** (e.g. "what does Japanese law say about deepfakes"), run a keyword search via the e-Gov API across all 10,000+ laws.

## Bundled core statutes

These 16 laws live in `references/laws/` as cleaned Markdown — full current text. **Read them with the Read tool before fetching anything remote.** Reading them takes one tool call and zero seconds of network latency.

| File | 法令ID (e-Gov) | Use for |
|---|---|---|
| `著作権法.md` | [345AC0000000048](https://laws.e-gov.go.jp/law/345AC0000000048) | Copyright — ownership, 二次利用, 私的複製, 引用, 著作者人格権, 罰則 |
| `著作権等管理事業法.md` | [412AC0000000131](https://laws.e-gov.go.jp/law/412AC0000000131) | JASRAC and other management organizations |
| `民法.md` | [129AC0000000089](https://laws.e-gov.go.jp/law/129AC0000000089) | Contracts, torts, agency, succession — the base civil code |
| `労働基準法.md` | [322AC0000000049](https://laws.e-gov.go.jp/law/322AC0000000049) | Working hours, overtime, wages, leave |
| `労働契約法.md` | [419AC0000000128](https://laws.e-gov.go.jp/law/419AC0000000128) | Employment contract formation, termination, fixed-term rules |
| `労働者派遣法.md` | [360AC0000000088](https://laws.e-gov.go.jp/law/360AC0000000088) | Dispatched workers — distinguish from outsourcing |
| `不正競争防止法.md` | [405AC0000000047](https://laws.e-gov.go.jp/law/405AC0000000047) | Trade secret, slavish imitation, well-known mark abuse |
| `個人情報保護法.md` | [415AC0000000057](https://laws.e-gov.go.jp/law/415AC0000000057) | APPI — personal data handling |
| `商標法.md` | [334AC0000000127](https://laws.e-gov.go.jp/law/334AC0000000127) | Trademark registration and enforcement |
| `意匠法.md` | [334AC0000000125](https://laws.e-gov.go.jp/law/334AC0000000125) | Design rights |
| `特許法.md` | [334AC0000000121](https://laws.e-gov.go.jp/law/334AC0000000121) | Patents |
| `映画盗撮防止法.md` | [419AC1000000065](https://laws.e-gov.go.jp/law/419AC1000000065) | Theatrical recording ban |
| `プロバイダ責任制限法.md` | [413AC0000000137](https://laws.e-gov.go.jp/law/413AC0000000137) | Notice-and-takedown (現「情報流通プラットフォーム対処法」) |
| `消費者契約法.md` | [412AC0000000061](https://laws.e-gov.go.jp/law/412AC0000000061) | Consumer contract rules |
| `独占禁止法.md` | [322AC0000000054](https://laws.e-gov.go.jp/law/322AC0000000054) | Antitrust, 優越的地位の濫用 |
| `景品表示法.md` | [337AC0000000134](https://laws.e-gov.go.jp/law/337AC0000000134) | Advertising rules |

Plus 下請法 系 5 files (not in e-Gov) — see `jp-subcontract-review` for the 公取委 URLs.

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

## Hard limits

- This skill returns statutory text. It does not give legal advice.
- Japanese case law (判例) is not bundled and the API does not provide it. Tell the user that case-law analysis requires the case-lookup skill (coming in v0.2.0) or external research.
- Ministerial guidance (ガイドライン, 通達, 告示) is partially in the index but treat it as secondary — flag where the legal weight is regulatory guidance rather than statute.
- For any question that calls for professional judgment ("can we be sued for", "is this enforceable"), recommend the user consult a bengoshi.
