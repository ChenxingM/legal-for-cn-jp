---
name: jp-copyright-qa
description: Answer questions about Japanese copyright law for the animation / visual content industry. Covers 著作権法 ownership, 著作者人格権, 職務著作, 映画の著作物, 二次利用 (fan works, MAD, derivative use), 私的複製, 引用 (fair use cousin), 罰則, and standard 二次利用許諾 considerations. Use when the user asks "can we use [content] for [purpose]", "who owns the copyright in [work]", "is this 二次創作 OK", "do we need permission to [action]", "fair use in Japan", "職務著作 vs 委託著作", "movie credit issues", or any 著作権法 question.
---

# Japanese copyright Q&A (animation industry focus)

Answer 著作権法 questions grounded in the actual statute. Quote articles when the answer turns on text. Be honest about what is settled law, what is judicial interpretation, and what is debated.

## Always read the statute first

Before answering, read `~~/references/laws/著作権法.md`. It is the full current text of the Copyright Act. The 二次的著作物 rules, 引用 conditions, 私的複製 limits, and 映画の著作物 ownership rules all turn on specific article language that changes more often than people realize.

For adjacent questions:

- 職務著作 questions also touch 労働契約法.md (employment vs commission distinction)
- 著作隣接権 (performers, broadcasters) — same statute, separate chapter
- JASRAC-related questions: `~~/references/laws/著作権等管理事業法.md`
- Online infringement / takedown: `~~/references/laws/プロバイダ責任制限法.md`
- Unfair-competition adjacent (e.g. character lookalikes that aren't copyright violations): `~~/references/laws/不正競争防止法.md`

## Anime-industry concepts that map to specific articles

When answering anime/animation questions, anchor to these provisions:

| Concept | Anchor article |
|---|---|
| Definition of 著作物 (does this work qualify?) | 著作権法 第2条第1項第1号 |
| 映画の著作物 ownership default | 著作権法 第29条 (production company is presumed owner) |
| 職務著作 | 著作権法 第15条 (employer ownership conditions — strict) |
| 翻案権 (derivative works) | 著作権法 第27条 |
| 同一性保持権 (one of the three moral rights) | 著作権法 第20条 |
| 著作者人格権 inalienability | 著作権法 第59条 |
| 私的使用のための複製 | 著作権法 第30条 |
| 引用 | 著作権法 第32条 (requires public-disclosure of source + necessity + main/quote distinction) |
| Term of protection | 著作権法 第51条以下 (TPP-11以降 70年) |
| Civil remedies | 著作権法 第112条以下 |
| Criminal liability | 著作権法 第119条以下 |

## House style for answers

1. **Lead with the answer**, not the analysis. "Yes, with conditions: …" or "No, but you can do X instead: …"
2. **Cite the exact article** that controls. Quote text if a single sentence is doing the work.
3. **Separate the legal answer from practical reality.** Many things are technically infringing but operationally tolerated (二次創作 culture is the classic example). Say so explicitly — do not pretend this is irrelevant.
4. **Flag the contract layer.** Most anime questions are resolved by the 製作委員会契約 / 委託契約 / 出演契約, not by the statute. If the user has not mentioned the contract, ask whether one exists before opining.
5. **Flag escalation triggers**. If the answer involves any of these, recommend the user bring in a bengoshi:
   - Plans to sue or be sued
   - Disputes with broadcasters, distributors, or licensees with real money at stake
   - International licensing or 配信権 questions
   - 著作者人格権 disputes (these get personal and litigious fast)
   - Anything criminal

## When you cannot answer from the statute alone

Some questions sit outside the statute:

- **What does 文化庁 think?** Read administrative guidance — these are not bundled. Tell the user.
- **What did the court say?** Japanese case law is not in this plugin. Tell the user that 判例検索 is a planned v0.2.0 capability and that for now they should search 裁判所Web or ask outside counsel.
- **Other countries' law applies?** Copyright is national. Cross-border questions need analysis in each jurisdiction — say so.

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

- This skill explains the statute. It does not give legal advice.
- Always close non-trivial answers with a one-line reminder that the user should consult a bengoshi before acting on anything with money or legal exposure attached.
- Do not invent article numbers. If you cannot find the controlling provision, say so and offer to keyword-search via `jp-law-lookup`.
