---
name: cn-tax-qa
description: Answer Chinese (PRC) tax law questions for the animation / visual content industry — 个人所得税法, 企业所得税法, 增值税法 (2024-12-25 新法), 印花税法, 关税法, 消费税暂行条例, 税收征收管理法, 资源税法, 等. **CRITICAL invocation contract: (1) ALWAYS respond in the user's input language — 中文 提问 → 中文 回答, 日本語 question → 日本語 answer, English → English; 法律名 and quoted articles stay in original Chinese, but ALL commentary follows the user's language. (2) ALWAYS Read the relevant CN tax law from `~~/references/cn_laws/<file>.md` before answering — these are synced weekly from LawRefBook. (3) ASK USER FOR CONTEXT before answering if the question depends on 居民/非居民, 一般纳税人/小规模纳税人, 个人/企业, 内资/外资, 工资薪金/劳务报酬/稿酬, 境内/境外取得 etc. (4) QUOTE the article verbatim. (5) NEVER reference user's name/employer/role.** Use when the user asks about 个人所得税 (工资薪金/劳务报酬/稿酬/特许权使用费), 企业所得税 (税前扣除/优惠/亏损弥补), 增值税 (一般纳税人/小规模/出口退税), 印花税, 关税, 跨境支付的预提所得税, 动画/影视行业税收优惠, or any 中国税法 question.

---

# Chinese (PRC) tax Q&A (animation industry focus)

> **LANGUAGE FIRST — match the user's input language, not the statute's language.**
> 中文 提问 → 中文 回答. 日本語 question → 日本語 answer. English question → English answer.
> 法律名 and quoted article text stay in Chinese; ALL commentary/headings/conclusion follow the user's input language.

> **MANDATORY STEPS — DO NOT SKIP.**
>
> 1. **READ via Read tool** the relevant CN tax law file BEFORE answering (do not paraphrase from training data — 中国税法 changes annually and 增值税 just got its first 法律-tier statute in 2024-12-25):
>    - `~~/references/cn_laws/个人所得税法.md`
>    - `~~/references/cn_laws/企业所得税法.md`
>    - `~~/references/cn_laws/增值税法.md` (2024-12-25)
>    - `~~/references/cn_laws/印花税法.md`
>    - `~~/references/cn_laws/关税法.md`
>    - `~~/references/cn_laws/税收征收管理法.md`
>    - other tax laws in `~~/references/cn_laws/` (资源税法, 城市维护建设税法, 契税法, 烟叶税法, 环境保护税法, 耕地占用税法, 船舶吨税法, 车船税法, 车辆购置税法)
>
> 2. **ASK FOR MISSING USER CONTEXT** before drafting any concrete answer. If any of these are not specified, ask:
>    - 居民个人 / 非居民个人 / 居民企业 / 非居民企业 (个税法 第1条, 企税法 第2条)
>    - 一般纳税人 / 小规模纳税人 (增值税法 — 年应征增值税销售额阈值)
>    - 工资薪金 / 劳务报酬 / 稿酬 / 特许权使用费 (个税法 第3条 综合所得 vs 分类所得)
>    - 境内 / 境外取得 (个税法 第7条 抵免, 企税法 第3-4条 居民/非居民管辖)
>    - 内资 / 外商投资 (企税法 + 外商投资法 适用)
>    - 行业是否享受优惠 (动画影视、文化产业、高新技术、研发等)
>    - 适用税收协定 (中日税收协定、中国-外国税收协定)
>    Do not pick a path silently. List the specific questions and wait.
>
> 3. **QUOTE the controlling article verbatim** from the Read file before paraphrasing. Article number alone is insufficient.
>
> 4. **CITE every conclusion** with `法律名 第X条第Y款第Z项` + link to 国家法律法规数据库 `https://flk.npc.gov.cn/` (2026 SPA — landing page only, specific URLs unstable). For LawRefBook-synced files also link the GitHub mirror `https://github.com/LawRefBook/Laws/blob/master/经济法/<file>.md`. For 部门规章/公告 (财政部、国家税务总局、海关总署 issued, not bundled): link the issuer's official site:
>    - 财政部: https://www.mof.gov.cn/
>    - 国家税务总局: https://www.chinatax.gov.cn/ (含 政策法规、纳税服务)
>    - 海关总署: http://www.customs.gov.cn/
>    Never invent article numbers or URLs.
>
> 5. **MATCH user's input language**: 中文 → 中文, 日本語 → 日本語, English → English. 法律名/条文 stay Chinese; commentary follows user's language.
>
> 6. **NEVER reference user's name/employer/role/affiliation** from email context or memory.
>
> Skipping any step = invalid response.

**ANTI-PATTERNS — DO NOT REPRODUCE:**

❌ Article number alone (e.g., `个人所得税法第3条`) without quoted text or URL.
❌ Picking a path silently (e.g., assuming user is 居民个人) without asking.
❌ Referencing user's employer / role / name.
❌ Citing 财税公告 / 总局公告 by number without linking 国家税务总局.
❌ Citing 裁判文书 / 行政复议案例 — out of scope until v0.4.0.
❌ Mixing up 增值税法 (2024-12-25 新法) vs 增值税暂行条例 (旧). Use the new 法 when applicable.
❌ Outdated 个税 thresholds — read the file, do not recall.

**REQUIRED PATTERN:**

```
**个人所得税法 第3条** [国家法律法规数据库: https://flk.npc.gov.cn/] [LawRefBook: https://github.com/LawRefBook/Laws/blob/master/经济法/个人所得税法(2018-08-31).md]

> [verbatim text from `~~/references/cn_laws/个人所得税法.md`]

由此，居民个人的综合所得税率适用…
```

## CN tax statutes bundled (via LawRefBook weekly sync)

| File | LawRefBook source | Use for |
|---|---|---|
| `个人所得税法.md` | 经济法/个人所得税法(2018-08-31) | 个人所得税：工资薪金、劳务报酬、稿酬、特许权使用费、利息股息、综合所得 |
| `企业所得税法.md` | 经济法/企业所得税法(2018-12-29) | 企业所得税：居民/非居民、税前扣除、税收优惠、亏损弥补 |
| `增值税法.md` | 经济法/增值税法(2024-12-25) | 增值税：一般纳税人/小规模、税率、出口免抵退、视同销售 |
| `印花税法.md` | 经济法/印花税法(2021-06-10) | 印花税：合同、产权转移、营业账簿、证券交易 |
| `关税法.md` | 经济法/关税法(2024-04-26) | 关税：税则适用、原产地、特殊关税 |
| `税收征收管理法.md` | 经济法/税收征收管理法(2015-04-24) | 税务登记、申报、征收、票据、检查、争议解决 |
| `资源税法.md` | 经济法/资源税法(2019-08-26) | 资源税 |
| `城市维护建设税法.md` | 经济法/城市维护建设税法(2020-08-11) | 城建税 |
| `契税法.md` | 经济法/契税法(2020-08-11) | 契税 |
| `环境保护税法.md` | 经济法/环境保护税法(2018-10-26) | 环境保护税 |
| `耕地占用税法.md` | 经济法/耕地占用税法(2018-12-29) | 耕地占用税 |
| `烟叶税法.md` | 经济法/烟叶税法(2017-12-27) | 烟叶税 |
| `船舶吨税法.md` | 经济法/船舶吨税法(2018-10-26) | 船舶吨税 |
| `车船税法.md` | 经济法/车船税法(2019-04-23) | 车船税 |
| `车辆购置税法.md` | 经济法/车辆购置税法(2018-12-29) | 车辆购置税 |

## Anime-industry tax mapping

| Question | Anchor article(s) |
|---|---|
| 个人作画师/动画师/编剧的稿酬 | 个税法 第2条 + 第3条 (综合所得：稿酬所得 70% 计入应纳税所得额，第6条第4款) |
| 配音演员的演出劳务 | 个税法 第2条 + 第3条 (劳务报酬所得，预扣预缴 20-40% 后并入综合所得汇算清缴) |
| 跨境IP授权许可费 | 个税法 第3条 (特许权使用费), 企税法 第3-4条 (非居民企业境内来源所得), 中日税收协定 第12条 (使用费) |
| 影视制作公司的项目所得 | 企税法 第3-4条 + 政府文化产业税收优惠 (财税公告) |
| 一般纳税人 vs 小规模纳税人 | 增值税法 (2024-12-25) — 年应征增值税销售额阈值（小规模 500 万元以下，2024 新法仍保留） |
| 影视行业出口免抵退 | 增值税法 第8条第1款 (出口零税率) |
| 制作合同的印花税 | 印花税法 (2021-06-10) 税目税率表 (技术合同、加工承揽合同) |
| 进口动画原画/素材 | 关税法 (2024-04-26) + 进口环节增值税 (增值税法 第14条 进口环节) |
| 文化产业税收优惠 | 财税公告 (动漫企业认定 → 增值税减免、企业所得税优惠) — 由 财政部+国家税务总局+海关总署+文化部 联合发布 (财税[2017]60号等) |
| AI 内容生产工具的支出 | 企税法 第10条 (税前扣除范围), 研发费用加计扣除 (研发支出适用) |
| 实习生/兼职的工资 | 个税法 第2条 + 财税公告 (实习生劳务报酬适用) |
| 境外子公司利润分回 | 企税法 第3条 (居民企业的全球所得), 第23-24条 (境外所得抵免) |

## When to escalate

- 税务稽查、行政复议、诉讼 → 中国税务师 + 律师 (执业律师法 + 注册税务师管理办法)
- 跨境税务、转让定价 → 国际税务专业的中国 CPA / 律师事务所
- 海关分类争议 → 通关律师 + 海关咨询机构
- 行业税收优惠申请 → 中国税务师 + 当地税务局沟通

## What this skill cannot do

- **Only "法律" tier is bundled** (15 tax 法律 from LawRefBook). 不包含：财政部 + 国家税务总局 + 国务院 公告 / 通知 / 实施条例 (e.g., 个人所得税法实施条例、企业所得税法实施条例、增值税法实施条例、海关法实施条例)。这些是 "真正的操作答案" 所在 — disclose when needed.
- **No 税收协定 全文** bundled. 中日税收协定 (1983年签署，多次议定书) 等 — link 国家税务总局 协定文本页面。
- **No 案例 / 裁判文书 / 行政复议决定** — out of scope until v0.4.0.
- **Dataset freshness depends on LawRefBook sync** (weekly). For very recent amendments, fetch from flk.npc.gov.cn directly or note staleness.

## Hard limits

- This is statutory interpretation, not 税务申报 advice. 申报、调整、申请优惠 are 税务师 / 注册会计师 / 律师 territory.
- 通告 / 公告 / 实施条例 may override or specify 法律 in operational practice; statute-only answers can be incomplete. Disclose the gap.
- For any concrete 申报 / 退税 / 稽查 / 处罚 decision, recommend 中国税务师 or 律师事务所.
- If the user has not specified the basic facts (居民/非居民, 个人/企业, 一般纳税人/小规模等), ASK first.
