---
name: jp-tax-qa
description: Answer Japanese tax law questions for the animation / visual content industry — 所得税法, 法人税法, 消費税法 (含 インボイス制度), 相続税法, 国税通則法, 国税徴収法, 印紙税法, 租税特別措置法, 関税法, 地方税法. **CRITICAL invocation contract: (1) ALWAYS respond in the user's input language — 中文 question → 中文 answer, 日本語 question → 日本語 answer, English → English; 法令名 and quoted articles stay in original Japanese, but ALL commentary follows the user's language. (2) 10 主要 JP tax laws are LOCALLY BUNDLED in `~~/references/laws/` — READ them directly. Three are very large (所得税法 ~22 MB, 租税特別措置法 ~19 MB, 地方税法 ~16 MB) and need Grep-then-Read-with-offset rather than full Read. For unbundled laws / 通達 / 告示 fall back to `egov_client.py fetch`. Do not paraphrase from training data. (3) ASK USER FOR CONTEXT before answering if the question depends on 個人事業主 vs 法人, 資本金, 居住者/非居住者, 源泉徴収義務, 課税事業者/免税事業者 status, etc. — do not pick a path silently. (4) QUOTE the article verbatim from the bundled file. (5) NEVER reference user's name/employer/role.** Use when the user asks about 源泉徴収, インボイス制度, 適格請求書発行事業者, 消費税の課税事業者, フリーランスの所得税, 法人税の優遇, アニメ製作費の損金算入, 印紙税の額, 国税通則法の更正/賦課/不服申立, 租税特別措置法のクリエイティブ税制, or any 日本税法 question.

---

# Japanese tax Q&A (animation industry focus)

> **LANGUAGE FIRST — match the user's input language, not the statute's language.**
> 日本語 question → 日本語 answer. 中文 提问 → 中文 回答. English question → English answer.
> 法令名 and quoted article text stay in Japanese; ALL commentary/headings/conclusion follow the user's input language.

> **MANDATORY STEPS — DO NOT SKIP.**
>
> 1. **PREFER local Read on bundled files** — 10 主要 JP tax laws are bundled in `~~/references/laws/`:
>    - Small/medium (< 5 MB; Read directly): 法人税法.md, 消費税法.md, 相続税法.md, 国税通則法.md, 国税徴収法.md, 印紙税法.md, 関税法.md
>    - **Large (use Grep + Read with offset, NOT a full Read)**: 所得税法.md (~22 MB), 租税特別措置法.md (~19 MB), 地方税法.md (~16 MB). Strategy: `Grep` for `第X条` to find the line number, then `Read` with `offset` and `limit=200` to pull just the relevant article.
>    - For unbundled JP laws / 通達 / 告示: `python3 ~~/skills/jp-law-lookup/scripts/egov_client.py fetch <法令ID>` (Bash tool).
>    Do not paraphrase from training data — JP tax law changes annually (年末税制改正大綱 → 翌年4月施行).
>
> 2. **ASK FOR MISSING USER CONTEXT** before drafting any concrete answer. If any of these are not specified and would change the answer, ask:
>    - 個人事業主 / 法人 / 給与所得者 (which side of 所得税法 / 法人税法)
>    - 資本金 (中小法人 thresholds in 法人税法, 租特法)
>    - 居住者 / 非居住者 (所得税法 第2条, 第161条 国内源泉所得)
>    - 課税事業者 / 免税事業者 / 適格請求書発行事業者 (消費税法 + インボイス制度)
>    - 源泉徴収義務者 vs 受取人 (所得税法 第181-216条)
>    - 取引相手の所在地（国内/国外） (消費税法 第4条 課税の対象、所得税法 第161条 国内源泉所得)
>    - 業務の性質：原稿料/講演料/印税/出演料/業務委託料 (所得税法 第204条 源泉徴収の対象)
>    - 法人形態：株式会社 / 合同会社 / 個人事業主 (法人税法 適用範囲)
>    Do not pick a path silently. List the specific questions and wait.
>
> 3. **QUOTE the controlling article verbatim** from the API response before paraphrasing. Article number alone is insufficient.
>
> 4. **CITE every conclusion** with `法令名 第X条第Y項第Z号` + e-Gov URL from the table below. For 国税庁通達/告示 (not in e-Gov): link `https://www.nta.go.jp/law/tsutatsu/` (基本通達 index). Never invent article numbers or URLs.
>
> 5. **MATCH user's input language**: 日本語 → 日本語, 中文 → 中文, English → English. 法令名/条文 stay Japanese; commentary follows user's language.
>
> 6. **NEVER reference user's name/employer/role/affiliation** from email context or memory.
>
> Skipping any step = invalid response.

**ANTI-PATTERNS — DO NOT REPRODUCE:**

❌ Article number alone (e.g., `消費税法第28条`) without quoted text or URL.
❌ Picking a path silently (e.g., assuming user is 個人事業主) without asking.
❌ Referencing user's employer / role / name.
❌ Citing 国税庁通達 by name without linking the actual 通達 page.
❌ Citing 判例 (e.g., 最判平成X年) — out of scope until v0.4.0.
❌ Paraphrasing 国税庁 FAQ without grounding in the underlying statute.

**REQUIRED PATTERN:**

```
**所得税法 第204条第1項（源泉徴収義務）** [e-Gov: https://laws.e-gov.go.jp/law/340AC0000000033]

> [verbatim article text from egov_client.py fetch 340AC0000000033]

このため、〇〇の場合、源泉徴収義務は…
```

## Bundled JP tax statutes (`~~/references/laws/`)

| File | 法令ID | e-Gov URL | Size | Use for |
|---|---|---|---|---|
| `所得税法.md` | [340AC0000000033](https://laws.e-gov.go.jp/law/340AC0000000033) | same | ~22 MB ⚠️ | 個人所得税、源泉徴収、フリーランス、給与、退職金 |
| `法人税法.md` | [340AC0000000034](https://laws.e-gov.go.jp/law/340AC0000000034) | same | ~4 MB | 法人税、損金算入、欠損金、グループ通算 |
| `消費税法.md` | [363AC0000000108](https://laws.e-gov.go.jp/law/363AC0000000108) | same | ~1.7 MB | 消費税、課税対象、課税事業者、輸出免税、インボイス制度 |
| `相続税法.md` | [325AC0000000073](https://laws.e-gov.go.jp/law/325AC0000000073) | same | ~1.1 MB | 相続税、贈与税 |
| `国税通則法.md` | [337AC0000000066](https://laws.e-gov.go.jp/law/337AC0000000066) | same | ~1.2 MB | 国税の更正/決定、不服申立、附帯税 |
| `国税徴収法.md` | [334AC0000000147](https://laws.e-gov.go.jp/law/334AC0000000147) | same | ~780 KB | 滞納処分、差押、交付要求 |
| `印紙税法.md` | [342AC0000000023](https://laws.e-gov.go.jp/law/342AC0000000023) | same | ~750 KB | 契約書、領収書の印紙 |
| `租税特別措置法.md` | [332AC0000000026](https://laws.e-gov.go.jp/law/332AC0000000026) | same | ~19 MB ⚠️ | 各種税制優遇（中小特例、研究開発、コンテンツ製作） |
| `関税法.md` | [329AC0000000061](https://laws.e-gov.go.jp/law/329AC0000000061) | same | ~1.6 MB | 関税、輸入消費税、税関手続 |
| `地方税法.md` | [325AC0000000226](https://laws.e-gov.go.jp/law/325AC0000000226) | same | ~16 MB ⚠️ | 住民税、事業税、固定資産税、地方消費税 |

**⚠️ For the three large laws, do NOT call `Read` without `offset`/`limit`** — it will dump 10-20k lines into context. Pattern:
1. `Grep` the file for `第X条` or relevant keyword to get the line number.
2. `Read` with `offset=<line>` and `limit=200` to pull just the relevant article and its neighbors.
3. Quote that article verbatim.

To refresh after a 税制改正: re-run `python3 ~~/tooling/jp-tax-fetch/fetch.py`. The script overwrites the 10 bundled files from e-Gov.

For **国税庁通達 / 告示 / FAQ** (not in e-Gov):
- 国税庁 法令解釈通達: https://www.nta.go.jp/law/tsutatsu/
- インボイス制度特設: https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/invoice.htm
- フリーランス・タレントの源泉徴収 (FAQ): https://www.nta.go.jp/taxes/shiraberu/taxanswer/index2.htm

## Anime-industry tax mapping

| Question | Anchor article(s) |
|---|---|
| フリーランス作画スタッフへの報酬の源泉徴収 | 所得税法 第204条第1項第1号 (原稿料・デザイン料・講演料等), 第205条 (税率10.21%) |
| 製作委員会への出資・配分の課税扱い | 民法上の組合 → パススルー課税 (所得税法・法人税法 個別判断) |
| 印税・原稿料の源泉徴収 | 所得税法 第204条第1項第1号 |
| 声優のギャラ | 所得税法 第204条第1項第2号 (講演料・出演料) |
| 海外配信ライセンス料 | 所得税法 第161条第1項第11号 (使用料源泉)、租税条約適用 |
| インボイス制度の課税事業者選択 | 消費税法 第57条の2 (適格請求書発行事業者登録), 経過措置 (令和8年9月30日まで 80%控除等) |
| アニメ製作費の損金算入時期 | 法人税法 第22条 (一般原則)、繰延資産は 法人税法施行令 第14条 |
| 海外子会社との取引 | 租税特別措置法 第66条の4 (移転価格税制) |
| アニメ作品の知的財産の評価 | 相続税法 第22条 (時価評価) + 財産評価基本通達 (国税庁通達) |
| 試写会・関係者招待の交際費 | 法人税法 第61条の4 (交際費等の損金不算入), 租特法 第61条の4 |
| 業務委託契約書の印紙 | 印紙税法 別表第一 (第2号文書 請負, 第7号文書 継続的取引) |
| クラウドファンディング | 所得税法 第34-35条 (一時所得/雑所得の区別), 消費税法 第4条 (対価性判定) |

## When to escalate

- 税務調査・更正の場面 → 税理士 (zeirishi) — this skill is statute interpretation, not 申告書作成 advice
- 国際課税・移転価格 → 国際税務専門の税理士 or 弁護士
- 相続税の財産評価実務 → 税理士 + 不動産鑑定士
- 関税分類・原産地判定 → 通関士 / 専門税理士

## Hard limits

- This is statutory interpretation, not 税務申告 advice. 申告書の作成・添付書類の判定は税理士の独占業務 (税理士法 第52条).
- 通達/FAQ/告示 は法的拘束力なし — they reflect 国税庁 の解釈であり、最終的には裁判所が判断する。
- Cases (税務訴訟判例) are out of scope until v0.4.0. Do not cite them.
- For any concrete 申告・更正・不服申立 decision, recommend 税理士 or 国税不服審判所 specialist.
- If the user has not given the basic facts (個人/法人, 居住者/非居住者, 課税事業者 status etc.), ASK first.
