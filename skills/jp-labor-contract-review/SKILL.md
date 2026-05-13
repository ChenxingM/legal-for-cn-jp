---
name: jp-labor-contract-review
description: Review Japanese labor and outsourcing contracts. **CRITICAL invocation contract: (1) ALWAYS respond in the user's input language — 中文 question → 中文 answer, 日本語 question → 日本語 answer, English → English; statute names and quoted articles stay in original Japanese, but ALL commentary/headings/conclusion follow the user's language. (2) ALWAYS Read `~~/references/laws/労働基準法.md`, `労働契約法.md`, `労働者派遣法.md`, `民法.md` via Read tool before answering. (3) QUOTE the controlling article verbatim; article numbers alone are insufficient. (4) NEVER reference the user's name/employer/role from email or memory. (5) Cases (判例) are out of scope until v0.4.0 — do not cite them.** Decide whether an engagement is 雇用 (employment), 業務委託 (service commission), or 派遣 (dispatch). Flag 偽装請負 risk, illegal overtime clauses, 試用期間 problems, missing 36協定 references, and termination clauses that violate 労働契約法 第16条. Use when the user says "review this 業務委託契約", "check this 雇用契約", "is this an employment or contractor relationship", "原画外注契約 review", "freelancer agreement", "is this 偽装請負", or attaches a Japanese labor / outsourcing contract.
---

# Japanese labor / outsourcing contract review

> **LANGUAGE FIRST — match the user's input language, not the statute's language.**
> 日本語 question → 日本語 answer. 中文 提问 → 中文 回答. English question → English answer.
> Statute names (法令名) and quoted article text stay in their original language. ALL commentary, headings, conclusion, and analysis follow the user's input language. A Chinese question about Japanese law gets a Chinese answer with Japanese article text quoted verbatim.

> **MANDATORY STEPS — DO NOT SKIP.**
>
> 1. **READ via Read tool** before drafting any review (do not paraphrase from training data):
>    - `~~/references/laws/労働基準法.md` → e-Gov [322AC0000000049](https://laws.e-gov.go.jp/law/322AC0000000049)
>    - `~~/references/laws/労働契約法.md` → [419AC0000000128](https://laws.e-gov.go.jp/law/419AC0000000128)
>    - `~~/references/laws/労働者派遣法.md` → [360AC0000000088](https://laws.e-gov.go.jp/law/360AC0000000088)
>    - `~~/references/laws/民法.md` → [129AC0000000089](https://laws.e-gov.go.jp/law/129AC0000000089) (請負/委任 sections)
>
> 2. **ASK FOR THE CONTRACT** if the user has not attached one. An audit without the contract is conjecture.
>
> 3. **QUOTE the controlling article verbatim** from the file before paraphrasing. "第16条" alone is not citation — paste the actual text.
>
> 4. **CITE every legal conclusion** with `法令名 第X条第Y項第Z号` + the e-Gov URL above. For 下請法-adjacent flags: link 公取委 `https://www.jftc.go.jp/shitauke/legislation/` and offer to switch to `jp-subcontract-review`. Never invent article numbers or URLs.
>
> 5. **MATCH user's input language**: 日本語 input → 日本語 output, 中文 input → 中文 output, English input → English output. 条文名・法律名 stay native; translate only commentary.
>
> Skipping any step = invalid response.

**ANTI-PATTERNS — caught 2026-05 in real user feedback. DO NOT REPRODUCE:**

❌ `民法632条以降` — article number alone, no URL, no quoted text. **Fix:** paste the article text verbatim from the .md file you Read.
❌ `ufotable で働かれている前提でのアドバイス` — using user's employer inferred from email domain. **Fix:** never reference employer/role/name. Answer the legal question, not personalize for the person.
❌ `マンナ運輸事件・京都地判H24.7.13` — citing case law (real or invented). Cases are **out of scope until v0.4.0**. **Fix:** stick to statute; if a question fundamentally needs case law, disclose the gap.
❌ `厚労省「副業・兼業の促進に関するガイドライン」によれば...` — paraphrasing administrative guidance without bundled-statute grounding. **Fix:** ground every claim in `~~/references/laws/*.md` first; if 厚労省 guidance is needed, label it as outside-corpus.
❌ Trailing apologies / hedges — `(...は law-index.csv で未確認のため...)`, `申し訳ありません、見落としていました` — apologies don't fix the answer. **Fix:** just produce the correct answer; if you don't have a URL, fetch via `jp-law-lookup`.
❌ **Language mismatch** — user asked in Chinese (`日本就业竞争这边是如何规定的 我能同时接数个公司的业务委托吗`), response opened in Japanese (`日本における兼業・複数業務委託契約について`). Wrong. **Fix:** 中文 question → 中文 answer. Headings, conclusion, analysis ALL in Chinese. Only the quoted 民法/労働基準法 article text stays in Japanese (verbatim).

**REQUIRED PATTERN** (for any statutory claim):

```
**民法 第632条（請負）** [e-Gov: https://laws.e-gov.go.jp/law/129AC0000000089]

> [exact text copied from `~~/references/laws/民法.md`]

このため、〇〇は…
```

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
- Payment terms over 60 days (note: 下請法 may apply if both sides are 事業者 of certain sizes → escalate to `jp-subcontract-review` for the full B2B audit)
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
