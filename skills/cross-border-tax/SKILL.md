---
name: cross-border-tax
description: Cross-border tax issues between Japan and China for the animation / visual content industry — 中日租税条約 (中日税收协定 1983年), 源泉徴収 / 预提所得税 (使用料・配信権・劳务报酬), 移転価格 / 转让定价, インボイス制度 cross-border services, 中国 出口退税, 双重征税抵免, 居住者・非居住者判定. **CRITICAL invocation contract: (1) ALWAYS respond in the user's input language. (2) For each side of the transaction, delegate to the relevant skill (jp-tax-qa for JP rules, cn-tax-qa for PRC rules) — fetch JP from e-Gov API, Read CN from bundled files. (3) ASK USER FOR CONTEXT — direction of payment, who's payer/receiver, residence of each party, type of income, treaty position. (4) QUOTE both sides' controlling articles. (5) NEVER reference user's name/employer/role.** Use when the user asks "中日两边怎么征税", "ライセンス料の二重課税", "中国の動画チームに支払う際の源泉", "源泉徴収と预提所得税の関係", "中日租税条約の使用料条項", "中日税收协定的特许权使用费条款", "アニメの海外配信のクロスボーダー課税", "声優の中国出演料の税務処理", or any JP-CN cross-border tax question.

---

# Japan-China cross-border tax Q&A (animation industry focus)

> **LANGUAGE FIRST — match the user's input language, not either jurisdiction's language.**
> 日本語 question → 日本語 answer. 中文 提问 → 中文 回答. English question → English answer.
> 法令名 (Japanese) / 法律名 (Chinese) and quoted articles stay in their original language; ALL commentary follows the user's input language.

> **MANDATORY STEPS — DO NOT SKIP.**
>
> 1. **DELEGATE TO BOTH SIDES**:
>    - For JP-side rules: use Bash to run `python3 ~~/skills/jp-law-lookup/scripts/egov_client.py fetch <法令ID>` (or delegate to `jp-tax-qa`).
>    - For CN-side rules: use Read tool on `~~/references/cn_laws/<file>.md` (or delegate to `cn-tax-qa`).
>    - For 中日租税条約 (1983-09-06 締結 / 多次议定书 修订): no domestic bundle — link 国税庁協定一覧 https://www.nta.go.jp/publication/pamph/sozei/202206_03.htm and 国家税务总局协定页 https://www.chinatax.gov.cn/。 The treaty text itself: ask the user to provide it or fetch from 国税庁 PDF.
>
> 2. **ASK FOR MISSING USER CONTEXT** before drafting any concrete answer:
>    - **Direction of payment**: JP-side payer → CN-side receiver, or vice versa?
>    - **Type of income**: 使用料/特许权使用费 (license/royalty), 劳务报酬/役務提供, 給与/工资, 配当/股息, 利子/利息, 投資収益 etc.?
>    - **Each party's tax residence**: 日本居住者 / 日本非居住者 / 中国居民 / 中国非居民?
>    - **Each party's legal form**: 個人 / 個人事業主 / 法人 / 制作委員会 / 中国 内资公司 / 外商投资公司 / WFOE / 中外合资?
>    - **Permanent establishment (PE) 常設機関 / 常设机构** in the other jurisdiction?
>    - **Whether 租税条約適用申請書 (JP 様式17) / 享受税收协定待遇申请 has been filed**?
>    - **Currency, transaction amount, frequency** — relevant for 印紙税 (JP) / 印花税 (CN) and PE constitution
>    - **Is there a contract**? — provide it for accurate analysis
>    Do not pick a path silently. List the specific questions and wait.
>
> 3. **QUOTE controlling articles verbatim from BOTH SIDES**:
>    - JP: from egov_client.py output (e.g., 所得税法 第161条 国内源泉所得, 第212条 非居住者の源泉徴収)
>    - CN: from `references/cn_laws/<file>.md` (e.g., 企业所得税法 第3条 居民/非居民, 第19条 非居民企业所得税扣缴义务, 个人所得税法 第7-8条 抵免)
>    - 中日租税条約: cite article (e.g., 第7条 事業所得, 第12条 使用料・特許権使用料, 第14条 給与) and link 国税庁 PDF or 国家税务总局 page.
>
> 4. **CITE every conclusion**:
>    - JP statutes: e-Gov URL `https://laws.e-gov.go.jp/law/<法令ID>` (see jp-tax-qa for table)
>    - PRC statutes: 国家法律法规数据库 `https://flk.npc.gov.cn/` + LawRefBook mirror
>    - 租税条約: 国税庁 / 国家税务总局 official link
>    Never invent article numbers or URLs.
>
> 5. **MATCH user's input language**. Statute citations stay native.
>
> 6. **NEVER reference user's name/employer/role/affiliation** from email or memory.
>
> Skipping any step = invalid response.

**ANTI-PATTERNS — DO NOT REPRODUCE:**

❌ Answering only one side (e.g., explaining JP source-rule without checking CN withholding) — cross-border by definition needs both.
❌ Asserting "treaty applies" without verifying treaty filings (様式17 / 享受待遇申请) have been submitted.
❌ Generic "double taxation can be relieved by treaty" without naming the specific article and rate.
❌ Confusing 使用料 (royalty) vs 役務提供 (services) — they're taxed under different articles. Ask user about substance.
❌ Picking 居住者/非居住者 silently without asking the user.
❌ Referencing user's employer / role / name.
❌ Citing tax cases — out of scope until v0.4.0.

**REQUIRED PATTERN (cross-border requires citing both sides):**

```
## JP-side
**所得税法 第161条第1項第11号（国内源泉所得 — 使用料）** [e-Gov: https://laws.e-gov.go.jp/law/340AC0000000033]
> [verbatim from API]

**所得税法 第212条（非居住者の源泉徴収義務）**
> [verbatim]

## CN-side
**企业所得税法 第3条第3款（非居民企业所得税）** [国家法律法规数据库: https://flk.npc.gov.cn/] [LawRefBook: ...]
> [verbatim from references/cn_laws/企业所得税法.md]

## 中日租税条約
**第12条 使用料** [国税庁: https://www.nta.go.jp/publication/pamph/sozei/202206_03.htm]
（条約限度税率 10% — verify against current 議定書 / 修订版本）

## 結論
[two-jurisdiction integrated answer]
```

## Anime-industry cross-border scenarios

| Scenario | JP-side anchor | CN-side anchor | 租税条約 article |
|---|---|---|---|
| JP studio が 中国スタジオ にライセンス料支払 | 所得税法 第161条第1項第11号 (国内源泉) + 第212条 (源泉20.42%) | 企业所得税法 第3条第3款 (非居民企业, 一般 10%) | 第12条 (使用料 — 10% 限度) |
| JP studio が 中国の個人作画スタッフに業務委託料 | 所得税法 第204条 (源泉徴収) + 第161条 (源泉地判定) | 个税法 第3条 + 第8条 (非居民境内所得) | 第7条 (事業所得 — PE基準) / 第14条 (独立的個人役務) |
| JP声優が 中国出演料を受領 | 所得税法 第161条 + 第204条 — JP居住者なら国外所得は通常課税 | 个税法 (中国 source の場合 預提) | 第17条 (芸能人・スポーツ選手の特則) |
| 中国子会社からの 配当・利息 | 法人税法 第23条 (外国子会社配当益金不算入), 所得税法 第23条 (海外配当) | 企税法 第27条 (居民企业境外所得免征 / 抵免) | 第10条 (配当)、第11条 (利息) |
| アニメ作品の中国配信権ライセンス | 同 1番目 | 同 1番目 | 第12条 |
| 制作協力料 (中国会社へ支払) | 所得税法 第161条 (役務提供地基準) | 企税法 第3条 — PE 構成有無で異なる | 第7条 (事業所得) / 第14条 |
| 移転価格 (関連会社間 license料) | 租税特別措置法 第66条の4 (法人税 移転価格税制) | 企税法 第41-48条 (特别纳税调整) — APA 制度あり | OECD Model TPG 準拠 |
| インボイス制度の cross-border services | 消費税法 第4条 (内外判定) + 第7条 (輸出免税) | 增值税法 第8条 (出口零税率) | N/A (treaty does not address VAT) |
| クラウドファンディング (中国の支援者から JP studio へ) | 所得税法 第34-35条 (区別)、消費税法 第4条 (対価性) | 个税法 (PRC 個人 → JP 受領) | depending on substance |

## What this skill cannot do

- **No 租税条約 全文 bundled**. 中日租税条約 (1983-09-06 / 多次修订) and 議定書 (Protocol) must be fetched from 国税庁 / 国家税务总局 — link only.
- **No 国税庁・国家税务总局 通達/公告 全集**. Operational answers often live in these. Disclose when relevant and link the issuer.
- **No PE 認定の判例** — out of scope until v0.4.0.
- **No transfer-pricing methodology details** beyond statute level. APA / 文書化 (Local File / Master File) は 専門家 領域.
- **Currency hedging / forex tax treatment** — out of scope.

## When to escalate

- 中日 cross-border 取引の課税が現実に発生 → JP-side 税理士 + CN-side 税务师 / CPA + treaty 専門 弁護士
- 移転価格調整・APA → JP/CN 双方の transfer pricing 専門家
- 源泉徴収義務違反の調査 → 国税局 / 国家税务总局 対応の税理士

## Hard limits

- This is treaty + statute analysis, not transactional tax planning. Concrete 申告 / 申請 / 文書 は専門家領域.
- Treaty positions change with 議定書 — verify current text before relying.
- 国内的 通達/公告/告示 may override treaty in some 公租税 areas — case by case.
- If the user hasn't specified direction, residence, income type, and contract substance, ASK first.
