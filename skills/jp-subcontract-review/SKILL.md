---
name: jp-subcontract-review
description: Audit a 下請取引 (B2B subcontracting relationship) under Japan's 下請代金支払遅延等防止法 (通称 下請法). Use when the user mentions 下請法, 親事業者, 下請事業者, 60日ルール, 下請代金, アニメ制作の元請-下請関係, 制作協力スタジオへの発注, 個人原画/動画/演出への外注, 書面交付義務, 公取委勧告, 違反通報, or asks "does 下請法 apply to my transaction" / "what's the parent-subcontractor capital threshold" / "are these mandatory written-contract items in our PO". This is distinct from jp-labor-contract-review (which covers 雇用/業務委託/派遣 worker classification) — 下請法 regulates B2B relationships triggered by capital-size thresholds, not worker-status.
---

# 下請取引コンプライアンス監査 (下請代金支払遅延等防止法)

> **MANDATORY STEPS — DO NOT SKIP.**
>
> 1. **READ all five via Read tool** before any audit (do not paraphrase — 規則 was amended through 令和5年):
>    - `~~/references/laws/下請代金支払遅延等防止法.md` → 公取委 https://www.jftc.go.jp/shitauke/legislation/act.html
>    - `~~/references/laws/下請法施行令.md` → 公取委 https://www.jftc.go.jp/shitauke/legislation/co.html
>    - `~~/references/laws/下請法書面規則.md` → 公取委 https://www.jftc.go.jp/shitauke/legislation/article3.html
>    - `~~/references/laws/下請法遅延利息規則.md` → 公取委 https://www.jftc.go.jp/shitauke/legislation/article4_2.html
>    - `~~/references/laws/下請法書類保存規則.md` → 公取委 https://www.jftc.go.jp/shitauke/legislation/article5.html
>
> 2. **QUOTE the controlling article verbatim** before paraphrasing. "第3条" alone is not citation — paste the actual text.
>
> 3. **CITE every legal conclusion** with `法 第X条第Y項第Z号` or `規則 第X条` + the 公取委 URL above. 下請法 is **not in e-Gov**. For adjacent JP statutes use e-Gov `https://laws.e-gov.go.jp/law/<法令ID>` (see `jp-law-lookup` for the bundled 法令ID table). Never invent article numbers or URLs.
>
> 4. **MATCH user's input language**: 日本語 input → 日本語 output, 中文 input → 中文 output, English input → English output. 条文名・法律名 stay native; translate only commentary.
>
> Skipping any step = invalid audit.

**ANTI-PATTERNS — DO NOT REPRODUCE:**

❌ `下請法 第3条` alone — no URL, no quoted text. **Fix:** paste the article from `下請代金支払遅延等防止法.md`.
❌ Referencing user's employer/role/affiliation from email or memory.
❌ Citing 公取委 勧告 examples without verifying — case-style references to enforcement actions are out of scope unless the user provides the case.
❌ Trailing apologies / "未確認" hedges — fix the citation by Reading the file.

**REQUIRED PATTERN:**

```
**下請代金支払遅延等防止法 第2条の2（下請代金の支払期日）** [公取委: https://www.jftc.go.jp/shitauke/legislation/act.html]

> [exact text from `~~/references/laws/下請代金支払遅延等防止法.md`]

このため、貴社の支払サイクルは…
```

下請法 is a thin but unforgiving statute. The 12 articles look small, but the 公正取引委員会規則 attached to them dictate 8 mandatory written-contract items, 11 prohibited parental acts, a 60-day payment ceiling, a 14.6%/year late-interest rate, and 2-year records retention. Animation studios are routinely on the 親事業者 side and trip on the written-document and payment-period rules.

## Always read these first

Before any audit, read the bundled corpus:

1. `~~/references/laws/下請代金支払遅延等防止法.md` — the act (12 articles)
2. `~~/references/laws/下請法施行令.md` — cabinet order (情報成果物 / 役務 definitions for 第2条第7項第1号; electronic-notice consent procedure)
3. `~~/references/laws/下請法書面規則.md` — implementing rule for 第3条 (the 8 mandatory items)
4. `~~/references/laws/下請法遅延利息規則.md` — late-payment interest rate (14.6%/year)
5. `~~/references/laws/下請法書類保存規則.md` — records the 親事業者 must keep, 2-year retention

## Decision tree

### 1. Does 下請法 apply at all?

Two cumulative tests — **both** must be true.

**(a) Transaction type** — the work commissioned must be one of:

| 委託 | Definition | Anime industry example |
|---|---|---|
| 製造委託 | Manufacture/process tangible goods | 物販グッズ製造、フィギュア原型 |
| 修理委託 | Repair tangible goods | (rare in animation) |
| 情報成果物作成委託 | Create digital/intellectual products | **作画／動画／彩色／3DCG／撮影／音響／脚本／演出**, BGM, 主題歌 |
| 役務提供委託 | Provide services that will be re-provided | (less common; e.g., 制作協力スタジオに丸投げ for resale to keyclient) |

For animation, **情報成果物作成委託** is the relevant category most of the time. 「映画，放送番組その他影像又は音声その他の音響により構成されるもの」(法 第2条第6項第2号) covers anime works directly.

**(b) Capital thresholds** — the parent must exceed and the subcontractor must be at or below the size cutoffs in 法 第2条第7項–8項. The cutoff differs by transaction type:

| Transaction type | 親事業者 capital must be | 下請事業者 capital must be |
|---|---|---|
| 製造／修理委託 (high tier) | > 3億円 | ≤ 3億円 (or 個人事業主) |
| 製造／修理委託 (mid tier) | > 1000万円 and ≤ 3億円 | ≤ 1000万円 (or 個人事業主) |
| 情報成果物／役務提供 (high tier, **excluding programs/transport/storage/info-processing**) | > 5000万円 | ≤ 5000万円 (or 個人事業主) |
| 情報成果物／役務提供 (mid tier, **excluding programs/transport/storage/info-processing**) | > 1000万円 and ≤ 5000万円 | ≤ 1000万円 (or 個人事業主) |
| 情報成果物 = **プログラム** OR 役務 = **運送／倉庫保管／情報処理** | (uses the 製造委託 tiers above per 施行令 第1条) | (uses the 製造委託 tiers above) |

For an animation studio commissioning 個人作画スタッフ (個人事業主): if the studio's 資本金 > 1000万円, **下請法 applies**. Most established anime studios are over the 1000万円 line. Many are below 5000万円 (so the mid tier applies for 作画委託 — which is 情報成果物作成委託 ≠ プログラム).

### 2. みなし規定 (法 第2条第9項)

Even if direct sizes don't hit, **トンネル会社規定**: a controlled sub-entity that re-commissions can be deemed 親事業者 if the chain would have hit thresholds without it. Closing this loophole is why holding-company structures with under-capitalized 制作子会社 don't escape.

### 3. If 下請法 applies — what immediately becomes mandatory

| Obligation | Article | Practical content |
|---|---|---|
| 書面の交付 | 法 第3条 + 書面規則 第1条 | 8 mandatory items (see below). 直ちに at the time of commissioning. |
| 60日支払期日 | 法 第2条の2 | 給付受領日 から **60日以内** に支払期日を定める。it must also be as short as practically possible. |
| 11の遵守事項 | 法 第4条 | 7 prohibited acts (第1項) + 4 prohibited acts harming subcontractor's interest (第2項). |
| 遅延利息 14.6%/年 | 法 第4条の2 + 遅延利息規則 | 受領日 から60日を超えた日から支払日まで、未払額 × 14.6%/年。 |
| 書類等の作成・保存 | 法 第5条 + 書類保存規則 | 12 items per transaction. **2-year retention.** |

## The 8 mandatory written-document items (第3条 + 書面規則 第1条第1項)

書面 (or 法 第3条第2項 によりelectronic equivalent with prior 承諾) must be issued **immediately** when commissioning and must contain:

1. **親事業者と下請事業者の識別** — 商号 or 事業者番号
2. **委託日 + 給付内容 + 受領期日 + 受領場所**
3. **検査をする場合のみ — 検査完了期日**
4. **下請代金の額 + 支払期日**
5. **手形支払のときのみ — 手形金額 + 満期**
6. **債権譲渡担保／ファクタリング／併存的債務引受方式のときのみ — 金融機関名・額・期日**
7. **電子記録債権のときのみ — 額・支払期日**
8. **原材料等を有償支給する場合のみ — 品名・数量・対価・引渡期日・決済期日**

Item 4 (額) can be deferred via **「算定方法」** if there's a 「やむを得ない事情」, but the algorithm must be specific enough to compute the actual figure. Item 4 cannot be a placeholder like 「別途協議」.

If any item is genuinely 未定 at commission time → it goes into the 当初書面 as a **特定事項** with (a) reason for non-fixing and (b) the date by which it will be fixed. A **補充書面** must then be issued the moment it's fixed.

## The 11 prohibited 親事業者 acts (第4条)

### 第1項 — 7 acts the 親事業者 **must not do**

1. **受領拒否** without subcontractor fault
2. **支払期日経過後の不払い**
3. **減額** without subcontractor fault
4. **返品** (受領後の引取り強要) without subcontractor fault
5. **買いたたき** — abnormally low 代金 vs. ordinary market price
6. **物品強制購入／役務強制利用** without legitimate quality-control / improvement need
7. **報復措置** — retaliation against subcontractor reporting violations to 公取委 or 中小企業庁

### 第2項 — 4 acts that "harm the subcontractor's interest"

1. **早期決済** — deducting raw-material 対価 from 代金 earlier than the 代金 payment date
2. **割引困難な手形** — issuing 手形 the bank won't discount before the payment date
3. **不当な経済上の利益の提供要請** — demanding kickbacks, free labor, free goods
4. **やり直し・内容変更** without subcontractor fault

役務提供委託 has narrower applicability: 第1項では 第1号 (受領拒否) and 第4号 (返品) are excluded; 第2項では 第1号 (早期決済) is excluded.

## 60-day payment ceiling (法 第2条の2)

- Period starts: 給付受領日 (役務提供委託 → 役務提供完了日)
- Maximum: 60 days
- Required: 「できる限り短い期間」, so 60 days is a ceiling, not a target
- If a 支払期日 is not set or is set in violation → 60日経過日の前日 がみなし支払期日
- After this date, **14.6%/年の遅延利息** applies (法 第4条の2)

## Records (法 第5条 + 書類保存規則)

For each transaction, the 親事業者 must record **12 items** (書類保存規則 第1条第1項各号) including:
- Subcontractor ID
- Commission/receipt/inspection dates and outcomes
- Yarinaoshi reasons (if any)
- 代金額 + 支払期日 + actual payment date + payment method
- 手形 details if applicable
- 電子記録債権 details if applicable
- 原材料等有償支給 details if applicable
- Partial-payment / 控除 balance
- 遅延利息 paid if applicable

**Retention period: 2 years** from the day the recording is complete (書類保存規則 第3条).

Electronic records are allowed but must support (i) revision tracking, (ii) display/print, (iii) searchable by subcontractor ID and date range (書類保存規則 第2条第3項).

## Penalties (法 第10-12条)

- 第3条 書面不交付 → **50万円以下の罰金** (個人の行為者本人)
- 第5条 書類不作成／不保存／虚偽記載 → **50万円以下の罰金**
- 第9条 報告／検査拒否・虚偽 → **50万円以下の罰金**
- **第12条 両罰規定** — same fine applied to the corporate entity

These are criminal fines. The bigger commercial risk is the **公取委 勧告 + 公表** (第7条) — publication of the parent's name as a 下請法違反者. For anime production it's a reputational hit; for IPO companies it can drag into 内部統制 disclosures.

## 親事業者 ↔ 下請事業者 enforcement map

| Trigger | Who acts | Authority article |
|---|---|---|
| 下請事業者 が 公取委 に違反通報 | 公取委 が立入検査 → 勧告 → 公表 | 第6条, 第7条, 第9条 |
| 中小企業庁長官 routes via 第6条 | 公取委 へ要請 | 第6条 |
| 反復違反 | 独占禁止法 第19条 (優越的地位の濫用) も併用可能 | 独禁法 |

The 公取委 publishes 勧告 details. Searchable list: https://www.jftc.go.jp/shitauke/index.html. Anime-industry parents have appeared — these are findable precedent.

## Anime industry mapping

| Question | Trigger / risk |
|---|---|
| 個人作画スタッフ (個人事業主) に作画委託 | スタジオ資本金 > 1000万円 → 下請法上の **情報成果物作成委託**。書面交付義務 + 60日ルール 適用。 |
| 「作監修正」依頼の追加発注 | 当初の書面に予定金額／受領期日無し → **第3条 書面不交付** の典型。当初書面の特定事項として処理する必要。 |
| 制作協力スタジオ (法人, 資本金 1000万円以下) への一括外注 | スタジオ資本金 > 1000万円 で外注先 ≤ 1000万円 → 下請法適用。 |
| 制作費 が「完成払い」(納品から60日超) | **法 第2条の2違反**。完成払い でも 60日 を超えると みなし支払期日が動き、14.6% 遅延利息が発生する。 |
| 「リテイク」「リテイク」「もう一度」 を作画担当者の責任で求める | **法 第4条第2項第4号 やり直し**。下請事業者の責に帰すべき理由が無いと違反。 |
| 動画用品 (用紙、データ) を有償支給 | 第3条書面の8号 + 第4条第2項第1号 (早期決済) 注意 |
| 「キャラデザ参考のためにグッズも作って」 with 強制購入 | **法 第4条第1項第6号 物品強制購入** |
| 通報した個人スタッフを次回作で外す | **法 第4条第1項第7号 報復措置** — 重い |
| 演出家への報酬を完パケ後の TV 放送後 まで持ち越し | **法 第2条の2違反** 高確率 |
| キャラデザの著作権譲渡条項 | これは 下請法 ではなく **著作権法 第27条/第28条** の問題。jp-copyright-qa と併用。 |
| 「業務委託」と名乗っているが指揮監督が強い個人作画 | これは 下請法 + **偽装請負** の両面。jp-labor-contract-review と併用。 |

## House-style audit output

```
# 下請法コンプライアンス監査：[案件名]

## 適用判定
- 委託類型: [製造／修理／情報成果物作成／役務提供]
- 親事業者 資本金: [X円]
- 下請事業者 形態: [個人事業主／法人 Y円]
- 結論: 下請法 [適用／適用外／みなし規定該当]
- 根拠条文: 法 第2条第7項第[X]号 + 第8項第[X]号

## 義務充足度

### 🔴 違反（直ちに是正）
- [条文] [事実] [是正策]

### 🟡 リスク（運用見直し）
- ...

### ⚪ 確認できず（書面提供を要請）
- ...

## 法 第3条 書面チェック (8項目)
| # | 項目 | 該当書面に有無 | 備考 |
|---|---|---|---|
| 1 | 親-下請識別 | ✓/✗ | |
| 2 | 委託日・給付内容・受領期日・場所 | | |
| ... | | | |

## 法 第4条 11禁止行為チェック
| # | 行為 | 該当 | 備考 |
|---|---|---|---|
| 1項1号 | 受領拒否 | ✓/✗ | |
| ... | | | |

## 支払期日 (法 第2条の2)
- 給付受領想定日: [日付]
- 設定支払期日: [日付]
- 期間: [X日] (上限 60 日)
- 評価: [Pass / 接近 / 違反]

## 改訂提案文
[Specific Japanese redline language for each Red]

## 次のアクション
- [何を 弁護士 が見るべきか]
- [社内：書類保存規則 第3条の 2年保存体制 確認]
```

## Cross-references

- `jp-labor-contract-review` — when the engagement is closer to 偽装請負 (working-reality test) than to clean B2B subcontracting
- `jp-copyright-qa` — when the audit raises 著作権 issues (assignment, 翻案権, 二次的著作物利用権)
- `jp-law-lookup` — for related statutes not bundled (建設業法、政府契約の支払遅延防止法)

## Hard limits

- This is a compliance audit, not legal advice. State this in every memo.
- Recommend 弁護士／公取委対応経験のある法律事務所 review for: ongoing 公取委 調査, 勧告対応, criminal investigation under 法 第10条, or recharacterization disputes worth more than nominal amounts.
- The bundled corpus reflects act amendments through 平成21年法律第51号 (2009) and 書面規則 改正 through 令和5年公正取引委員会規則第3号 (2023). Any later amendments are not reflected. Before relying on this for a live dispute, check the [公取委 legislation page](https://www.jftc.go.jp/shitauke/legislation/) for newer amendments, and recommend external counsel.
- If the user has not provided the actual 書面 (the alleged 第3条 document, the PO, the email chain, the contract), ask for it before running this skill. An audit without the document is conjecture.
