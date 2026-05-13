---
name: jp-labor-contract-review
description: Review Japanese labor and outsourcing contracts. Decide whether an engagement is 雇用 (employment), 業務委託 (service commission), or 派遣 (dispatch). Flag 偽装請負 risk, illegal overtime clauses, 試用期間 problems, missing 36協定 references, and termination clauses that violate 労働契約法 第16条. Use when the user says "review this 業務委託契約", "check this 雇用契約", "is this an employment or contractor relationship", "原画外注契約 review", "freelancer agreement", "is this 偽装請負", or attaches a Japanese labor / outsourcing contract.
---

# Japanese labor / outsourcing contract review

Review a contract against Japanese labor law and flag deviations from baseline. The output is a memo for the user — not advice for the counterparty.

## Always read these first

Before any review, read:

1. `~~/references/laws/労働基準法.md` — overtime, breaks, wages, leave
2. `~~/references/laws/労働契約法.md` — formation, termination, fixed-term rules
3. `~~/references/laws/労働者派遣法.md` — for any agreement near the dispatch line
4. `~~/references/laws/民法.md` — section on 請負 (Articles 632以降) and 委任 (643以降)

For anime-industry contracts (原画外注、声優出演、演出委託), 99% of the time the agreement is structured as `業務委託` (請負 or 準委任) under 民法 — not as 雇用 under 労働基準法. The risk is when the working reality looks like employment even though the paper says contractor.

## The 雇用 vs 業務委託 vs 派遣 test

The classification is not determined by the contract title. Apply the 労働者性判断基準 (1985 Ministerial guidance, codified in subsequent interpretation):

| Factor | Pushes toward 雇用 | Pushes toward 業務委託 |
|---|---|---|
| 仕事の依頼に対する諾否の自由 | None (cannot refuse) | Free to refuse |
| 業務遂行上の指揮監督 | Directed in detail | Methods left to worker |
| 勤務時間・場所の拘束 | Fixed hours, fixed place | Flexible |
| 代替性 | Cannot delegate to a third party | Can substitute |
| 報酬の性格 | Time-based wage | Outcome-based fee |
| 機材・経費負担 | Provided by company | Worker's own |
| 専属性 | Exclusive | Free to work for others |
| 給与所得処理 | Source withholding | 確定申告 |

If the working reality scores employment-leaning but the contract says 業務委託, flag it as **偽装請負 risk** — both labor law and tax authorities can recharacterize, and Articles 4 and 26 of the 派遣法 add criminal liability if it's structured as multi-tier.

## What to flag in any review

Run through this checklist and surface every hit:

### Hard violations (red)

- Fixed-term `業務委託` exceeding 5 years (`労働契約法` 第18条 applies if recharacterized)
- Hourly rate below 最低賃金 if recharacterized as employment
- Termination clause permitting at-will dismissal with no cause — `労働契約法` 第16条 voids this
- 試用期間 longer than typical (3-6 months max; 1 year+ is presumptively invalid)
- Overtime without 36協定 reference
- 36協定 with caps exceeding `労働基準法` 第36条 limits (45h/month, 360h/year baseline)
- Non-compete clauses without consideration or geographic/temporal scope
- Forfeiture of 著作者人格権 (these are inalienable per `著作権法` 第59条 — cite this in the comment)

### Soft flags (yellow)

- Vague scope of work — common in 原画外注 but creates 偽装請負 exposure
- IP assignment without explicit 著作権法 第27条 (翻案権) and 第28条 (二次的著作物の利用) language — these don't transfer by default
- Payment terms over 60 days (note: 下請法 may apply if both sides are 事業者 of certain sizes)
- Confidentiality with no time limit on post-termination
- Audit / inspection rights that are one-way only
- Mandatory exclusivity without compensation

### Missing-but-should-be-there

- ハラスメント complaint channel (required by `労働施策総合推進法` for employees; recommended even for contractors)
- 個人情報 handling for contractor processing of personal data
- Force majeure / 不可抗力 clause
- Governing law and jurisdiction (絶対に日本法 + 東京地裁 if you're the production side)

## House-style review output

Structure the memo as:

```
# 契約レビュー：[契約名]

## 全体判定
[緑 / 黄 / 赤] — one-paragraph summary

## 法的分類
雇用 / 業務委託（請負 or 準委任）/ 派遣 — and why

## 偽装請負リスク
[High / Medium / Low] with the specific factors pulling each way

## 条文別フラグ
### 🔴 Red — must fix
- [Clause X] [problem] [reference to 労基法 第〇条 / 労契法 第〇条]

### 🟡 Yellow — recommend changes
- ...

### ⚪ Missing — should add
- ...

## 改訂提案文
[Specific Japanese redline language for each Red and the most important Yellows]

## 次のアクション
- [What to do before signing]
- [Whether outside counsel review is recommended — be honest]
```

## Hard limits

- This is a contract review, not legal advice. State this in every memo.
- Recommend bengoshi review for any contract that involves: termination of a specific named employee, multi-jurisdictional engagement, restrictive covenants with significant scope, or contractor recharacterization disputes already in progress.
- If the contract is in English or Chinese, translate the operative clauses first and review against the translation — note any ambiguity introduced by translation.
- If the user has not attached a contract, ask for it before running this skill.
