---
name: cn-law-lookup
description: Look up Chinese (PRC) statutory law — find the text of a specific article, check what 民法典/著作权法/劳动合同法/个人信息保护法 actually says, identify which law applies to a topic. Use when the user asks "中国法律对XX怎么规定", "民法典第X条", "PRC copyright law on Y", "what does 个人信息保护法 say about Z", "中国劳动法对动画外注的规定", or any question requiring the actual text of a PRC 法律.
---

# Chinese (PRC) statute lookup

Answer questions about Chinese statutory law by retrieving the actual text — not by reciting from training data, which is likely out of date. Chinese law moves fast: 公司法 was rewritten in 2023, 反不正当竞争法 was amended in 2025, 网络安全法 in 2025, and new 部门规章 around AI appear yearly.

## Decision tree

1. **Is the law one of the 21 bundled core statutes?** Check `~~/references/cn_laws/`. If yes, read it directly — fastest path, zero network, latest manually-curated text.
2. **Is the law not in the bundled set?** Use the HuggingFace fetch client at `scripts/hf_client.py` — works against the bundled 22,552-entry index that covers 法律 / 宪法 / 行政法规 / 司法解释 / 地方性法规 / 监察法规 from the 国家法律法规数据库 as of 2023-09.
3. **Important — flk.npc.gov.cn is NOT used at runtime.** Many corporate networks block .cn domains. This plugin deliberately routes all PRC law fetches through HuggingFace's HTTPS endpoints, which are not blocked in typical corporate environments.

## HuggingFace fetch client

For any PRC law outside the 21 bundled core statutes, use `scripts/hf_client.py`. Run via Bash:

```bash
# Search the bundled 22552-entry index by title fragment (offline, no network)
python3 ~~/skills/cn-law-lookup/scripts/hf_client.py search "信息网络传播权" --limit 5

# Filter by type
python3 ~~/skills/cn-law-lookup/scripts/hf_client.py search "著作权" --law-type "司法解释"

# Filter by issuing body
python3 ~~/skills/cn-law-lookup/scripts/hf_client.py search "数据" --office-level "国务院"

# Fetch by dataset offset (from search results)
python3 ~~/skills/cn-law-lookup/scripts/hf_client.py fetch 934

# One-shot: search by title and fetch the top match
python3 ~~/skills/cn-law-lookup/scripts/hf_client.py fetch-title "信息网络传播权保护条例"
```

`fetch-title` ranks matches as 法律 > 宪法 > 行政法规 > 司法解释 > others, then by most-recent publish date. It always returns the full text plus the top 4 other matches as `other_matches` so you can offer alternatives.

The dataset is `twang2218/chinese-law-and-regulations` — pandoc-converted Markdown of the 国家法律法规数据库, snapshot 2023-09. **For amendments after Sept 2023** (e.g., 公司法 2023-12 修正, 反不正当竞争法 2025-06, 网络安全法 2025-10), the bundled 21 core statutes have been manually refreshed and supersede the HuggingFace text — check `~~/references/cn_laws/` first.

## Bundled core statutes

These 21 laws live in `references/cn_laws/` as cleaned Markdown — top tier (法律), enacted by the 全国人大 or its 常委会.

| File | Topic | Latest version |
|---|---|---|
| `著作权法.md` | Copyright — works, ownership, 邻接权, fair use, 信息网络传播权 | 2020 修正 |
| `商标法.md` | Trademarks | 2019 修正 |
| `专利法.md` | Patents (含设计专利) | 2020 修正 |
| `反不正当竞争法.md` | Unfair competition, trade secrets, 商业混淆 | 2025 修正 |
| `反垄断法.md` | Antitrust, abuse of dominance | 2022 修正 |
| `广告法.md` | Advertising regulation | 2021 修正 |
| `电影产业促进法.md` | Film industry promotion (relevant to cross-border 引进/输出) | 2016 |
| `民法典.md` | Civil Code — contracts (合同编), torts (侵权责任编), personality rights (人格权编), 等 | 2020 |
| `消费者权益保护法.md` | Consumer protection | 2013 修正 |
| `电子签名法.md` | E-signatures | 2019 修正 |
| `电子商务法.md` | E-commerce | 2018 |
| `劳动法.md` | Foundational labor law | 2018 修正 |
| `劳动合同法.md` | Employment contract specifics | 2012 修正 |
| `劳动争议调解仲裁法.md` | Labor dispute arbitration | 2007 |
| `网络安全法.md` | Cybersecurity (operator obligations, CIIO) | 2025 修正 |
| `数据安全法.md` | Data classification, cross-border data | 2021 |
| `个人信息保护法.md` | PIPL — personal information protection | 2021 |
| `公司法.md` | Company law (major 2023 rewrite) | 2023 修正 |
| `外商投资法.md` | Foreign investment | 2019 |
| `民事诉讼法.md` | Civil procedure | 2023 修正 |
| `仲裁法.md` | Arbitration | 2025 修正 |

## Anime industry mapping — which law for which question

| Question | Anchor |
|---|---|
| 角色形象、剧情、画面的著作权 | 著作权法 第3条以下 + 民法典 人格权编 (姓名权、肖像权 for 真人 reference) |
| 二次创作、同人作品 | 著作权法 第10条(权利) + 第24条(合理使用 — narrow!) — PRC 合理使用比 Japan/US 都窄 |
| 改编权 | 著作权法 第10条第14项 |
| 信息网络传播权 (online distribution) | 著作权法 第10条第12项 |
| 制作公司与角色作者的归属 | 著作权法 第18条 (职务作品) — 注意中国职务作品规则与日本职務著作不同 |
| 影视作品著作权归属 | 著作权法 第17条 (制片人享有著作权，原作者保留署名权和获得报酬权) |
| 跨境授权合同 | 民法典 合同编 第464条以下 + 涉外民事关系法律适用法 |
| 委外加工合同 (外注) | 民法典 承揽合同 第770条以下 |
| 员工vs外包 | 劳动合同法 第7条 (劳动关系成立要件) + 民法典 承揽 |
| 处理用户/角色资料 | 个人信息保护法 全篇 + 数据安全法 跨境 |
| 商标抢注、角色名/作品名 | 商标法 第13条(驰名商标) + 反不正当竞争法 第6条 (有一定影响) |
| 在中国发行电影 | 电影产业促进法 + 国务院《电影管理条例》(行政法规, 不在本插件) |
| AI 生成内容 | 著作权法 第3条(独创性要求) + 部门规章《生成式人工智能服务管理暂行办法》(行政法规, 不在本插件) |

## House style for answers

1. **Lead with the article**, then the conclusion. "民法典第533条规定[文]，因此……"
2. **Always cite the version year** when relevant ("民法典 2020 版", "公司法 2023 修订").
3. **Flag the gap with Japan**. Cross-border anime work often assumes things that hold under 著作権法 but not under 著作权法 — example: PRC 合理使用 is narrower than Japan's 引用, and there is no clear PRC equivalent to Japan's 私的複製.
4. **Identify the regulatory layer**. If the answer depends on 行政法规 (国务院条例) or 部门规章 (省部级 办法), say so plainly — these are not in this plugin's corpus.
5. **Flag escalation triggers**:
   - PRC litigation strategy → 中国律师
   - Cross-border licensing — get both PRC and Japan counsel
   - Network security review (CIIO) — 网信办 territory
   - Anything involving export control or data export — 数据出境安全评估

## What this skill cannot do

- **No 部门规章 (部委级规章)**. The HuggingFace dataset covers laws issued by 全国人大, 国务院, 最高法, 最高检 — but not most 部门规章 (e.g., 网信办《生成式人工智能服务管理暂行办法》, 国家版权局规章). For these, the user needs to fetch from the issuing 部委 website manually. v0.5.0 will bundle the most important ones for animation work.
- **No 判例 (cases)**. PRC case-law search is v0.4.0.
- **Dataset is 2023-09 snapshot**. For amendments after that date, prefer the manually-refreshed 21 core statutes in `references/cn_laws/`. The bundled index does mark `status` (有效 / 已修改 / 已废止) but this status reflects the 2023-09 state, not current state, for older amendments.
- **No 港澳台 special-region laws** in the bundled set (these are governed by separate frameworks).

## Freshness — read every time before quoting

Two-tier freshness:

- **`references/cn_laws/` (21 core statutes)**: manually curated, currently as of 2026-05. Refreshed when the user runs `scripts/refresh_cn_corpus.py` on a directory of newer docx downloads from 国家法律法规数据库.
- **HuggingFace dataset (via `hf_client.py`)**: snapshot dated 2023-09. Anything amended after 2023-09 (公司法 2023-12 修正, 反不正当竞争法 2025-06 修正, 网络安全法 2025-10 修正, 仲裁法 2025-09 修正, 民事诉讼法 2023-09 修正) is **stale** in the HF data.

**When you pull from HuggingFace, always tell the user**:

> ⚠️ 该法律全文来自 2023-09 快照。如果你需要的条文涉及 2023-09 之后的修正，请核验当前版本（或让用户重新下载 docx 并运行 refresh_cn_corpus.py）。

For the 21 bundled core statutes, no freshness disclaimer is needed — they were rebuilt from the user's 2026-05 download.

## Refresh workflow

If a law in the core set gets amended (or the user wants to add a new core law):

1. User downloads the latest .docx from flk.npc.gov.cn on any network that can reach .cn (home, mobile hotspot, etc.)
2. User runs: `python3 ~~/skills/cn-law-lookup/scripts/refresh_cn_corpus.py /path/to/downloaded/docx/`
3. The script auto-detects the law title, converts docx → Markdown, and overwrites the corresponding file in `references/cn_laws/`
4. No plugin reinstall required — the next Claude session picks up the new text

Use `--add` to add a law that is not in the default core mapping (creates a new file in `cn_laws/`).

## Hard limits

- This skill returns statutory text. It does not give legal advice.
- PRC law involves significant administrative interpretation. Even when the statute is clear, regulator practice may diverge — always recommend a PRC 律师 for matters of consequence.
- Always note when the statute references implementation rules (例如 "国务院制定" or "由国务院有关部门规定") because the practical answer is in those rules, not the statute itself.
