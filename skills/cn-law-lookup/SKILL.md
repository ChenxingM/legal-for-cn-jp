---
name: cn-law-lookup
description: Look up Chinese (PRC) statutory law — find the text of a specific article, check what 民法典/著作权法/劳动合同法/个人信息保护法 actually says, identify which law applies to a topic. Use when the user asks "中国法律对XX怎么规定", "民法典第X条", "PRC copyright law on Y", "what does 个人信息保护法 say about Z", "中国劳动法对动画外注的规定", or any question requiring the actual text of a PRC 法律.
---

# Chinese (PRC) statute lookup

Answer questions about Chinese statutory law by retrieving the actual text — not by reciting from training data, which is likely out of date. Chinese law moves fast: 公司法 was rewritten in 2023, 反不正当竞争法 was amended in 2025, 网络安全法 in 2025, and new 部门规章 around AI appear yearly.

## Decision tree

1. **Is the law one of the 21 bundled core statutes?** Check `~~/references/cn_laws/`. If yes, read it directly — fastest path, zero network, latest curated text.
2. **Not in the bundled set?** This version cannot fetch the long tail at runtime. Tell the user the law is outside the bundled corpus, offer to reason from general principles only, and **always** flag the text-unavailable caveat. The roadmap is to extend the LawRefBook sync list in `tooling/cn-law-refresh/scraper.py` to cover more 法律部门 / 行政法规 / 司法解释.
3. **No .cn domain is reached from the user's machine at runtime.** Many corporate networks block .cn domains. 17 of the 21 core statutes are synced weekly on GitHub-hosted runners from `github.com/LawRefBook/Laws` (the community-maintained corpus handles flk.npc.gov.cn's 2026 SPA migration for us). The remaining 4 are maintained by the project owner from authoritative .docx files. Either way, end users never need to hit .cn.

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
| 制作公司与角色作者的归属 | 著作权法 第18条 (职务作品) — 注意中国职务作品规则与日本職務著作不同 |
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

- **Long-tail laws (anything outside the 21 bundled core statutes) cannot be served at runtime in this version.** Future plan: a weekly GitHub Actions job will pull a curated extended set from flk.npc.gov.cn and commit it to the repo, so end users never need .cn access. Until that lands, only the 21 bundled core statutes are queryable; for anything else, reason from general principles and disclose the gap.
- **No 部门规章 (部委级规章)**. Most 部门规章 (e.g., 网信办《生成式人工智能服务管理暂行办法》, 国家版权局规章) are not in the core 21. For these the user needs to fetch from the issuing 部委 website manually. v0.5.0 will bundle the most important ones for animation work.
- **No 判例 (cases)**. PRC case-law search is v0.4.0.
- **No 港澳台 special-region laws** in the bundled set (these are governed by separate frameworks).

## Freshness — read every time before quoting

Single tier: the 21 bundled core statutes in `references/cn_laws/`, currently as of 2026-05.

Refresh paths:

1. **Automated sync from LawRefBook (preferred for 17 of 21)**: `.github/workflows/refresh-cn-laws.yml` runs every Monday 03:00 UTC, `git clones` LawRefBook/Laws, and copies the latest-dated version of each law in `LRB_SOURCED_LAWS` (see `tooling/cn-law-refresh/scraper.py`) into `references/cn_laws/`. Opens a PR if anything changed.
2. **Owner-maintained from authoritative .docx (for 4 of 21)**: 民法典, 反不正当竞争法, 网络安全法, 仲裁法 are not in the auto-sync list because LawRefBook lags their 2025 amendments. Refreshed by the project owner via `python3 ~~/skills/cn-law-lookup/scripts/refresh_cn_corpus.py /path/to/docx/`.

No freshness disclaimer is needed when quoting from the bundled 21 — they are refreshed weekly. For any law outside the 21, no statutory text is available; do not paraphrase from memory without disclosure.

## Hard limits

- This skill returns statutory text. It does not give legal advice.
- PRC law involves significant administrative interpretation. Even when the statute is clear, regulator practice may diverge — always recommend a PRC 律师 for matters of consequence.
- Always note when the statute references implementation rules (例如 "国务院制定" or "由国务院有关部门规定") because the practical answer is in those rules, not the statute itself.
