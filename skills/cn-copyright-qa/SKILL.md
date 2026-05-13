---
name: cn-copyright-qa
description: Answer questions about Chinese (PRC) copyright law for the animation / visual content industry. Covers 著作权法 ownership rules, 职务作品 vs 委托作品 vs 法人作品 (the three "who owns" categories — different from Japan's 職務著作), 视听作品 (the renamed 电影作品 post-2020), 信息网络传播权, 合理使用 (narrower than US fair use), 邻接权 (录像制作者, 表演者, 广播组织), and AI 生成内容 独创性问题. Use when the user asks "中国著作权法对XX怎么规定", "中国版职务作品规则", "PRC fair use", "中国二创合法吗", "动画在中国的著作权归属", or any 著作权法 question.
---

# Chinese (PRC) copyright Q&A

Answer 著作权法 questions grounded in the actual 2020-revised statute. Be especially careful about three things where PRC differs sharply from Japan:

1. **Work types**: PRC renamed 电影作品 to 视听作品 (audiovisual works) in the 2020 amendment. Use the new term.
2. **Ownership defaults**: PRC has 职务作品 / 委托作品 / 法人作品 / 视听作品 ownership rules that look superficially like Japan's 職務著作 but operate differently.
3. **合理使用 is narrow**: PRC's exceptions are an exhaustive list (著作权法 第24条 plus 第25条 for textbook 法定许可). There is no general fair-use doctrine. Compare to Japan's 引用 (Art 32) which is also narrow but applied differently.

## Always read the statute first

Before answering, read `~~/references/cn_laws/著作权法.md`. It is the 2020 version (the major rewrite that added 视听作品, 广播权 modernization, and the 信息网络传播权 carveouts).

For adjacent questions:

- Contract / licensing: `~~/references/cn_laws/民法典.md` 合同编 (especially 技术合同 第18章 第三节 技术许可)
- Employee vs contractor: `~~/references/cn_laws/劳动合同法.md` + `民法典.md` 承揽 (第770条以下)
- Online infringement, platform liability: `~~/references/cn_laws/网络安全法.md` + 民法典 第1194-1197条 (网络侵权)
- Trademark overlap (角色名, 作品名): `~~/references/cn_laws/商标法.md` + `反不正当竞争法.md`

## Anime-industry concepts → PRC anchors

| Concept | Anchor article |
|---|---|
| Definition of 作品 — independent creation requirement | 著作权法 第3条 |
| 著作人身权 (署名权, 修改权, 保护作品完整权) | 著作权法 第10条第1-4项 |
| 著作财产权 (含 信息网络传播权 第10项, 改编权 第14项) | 著作权法 第10条第5-17项 |
| 视听作品 ownership default | 著作权法 第17条 (制作者享有著作权; 编剧, 导演, 作曲, 作词 享有署名权和报酬请求权) |
| 视听作品 中可单独使用的剧本/音乐 | 著作权法 第17条第3款 (作者可单独行使) |
| 职务作品 | 著作权法 第18条 (一般归作者; 特殊情形归单位 — 程序设计、工程设计、地图等) |
| 法人作品 | 著作权法 第11条 (法人主持创作并担责则视为作者) |
| 委托作品 | 著作权法 第19条 (默认归受托人; 合同另有约定从约定) |
| 保护期 | 著作权法 第22-23条 (一般50年, 视听作品自首发 50年) |
| 合理使用 — exhaustive list | 著作权法 第24条 |
| 侵权法定赔偿 | 著作权法 第54条 (500元-500万元) |
| 信息网络传播 — notice take-down | 民法典 第1195-1197条 (通知-删除规则) |

## Cross-border practical realities (this is where you earn your money)

- **职務著作 ≠ 职务作品**. A Japanese 制作会社 expecting employer-owned 著作权 in China should look at 著作权法 第18条 and the contract — default ownership stays with the employee for most works, opposite of what 日本法 第15条 produces.
- **PRC has no 私的複製 carveout** comparable to Japan's 第30条. Personal copying is technically infringement; in practice it is not enforced against individuals, but **anything corporate-scale is exposed**.
- **PRC's 合理使用 列表** is 12 categories. For animation, the most useful are:
  - 第24条第1项 个人学习、研究、欣赏 (narrow — corporate use doesn't qualify)
  - 第24条第2项 适当引用 (with attribution, in critique/comment)
  - 第24条第5项 报纸/广播/网络 timely 转载 (with very specific source rules)
- **二次创作 (同人) in China is structurally different from Japan**. There is no 二次創作文化 of tolerance. PRC rights-holders enforce more aggressively, and 抖音/B站 cooperation with takedown is faster than Japan's plat.

## House style for answers

1. **Lead with the article**, then the conclusion. "著作权法第17条规定[X]，所以……"
2. **Always say "2020 修正"** when the answer turns on a post-2020 provision (most 视听作品 questions do).
3. **Cross-reference Japan**. The user works at a Japanese studio. If the PRC answer diverges from the Japan answer, flag it explicitly: "**与日本法不同的地方**: ……"
4. **Identify regulator gaps**. If the practical answer needs 国家版权局/国家网信办 implementation rules or 司法解释, say so — those are not in this plugin.
5. **Recommend 中国律师** for anything involving litigation, customs IPR enforcement, or platform takedown disputes.

## What this skill cannot do

- **No 司法解释**. 最高人民法院《关于审理著作权民事纠纷案件适用法律若干问题的解释》is critical for practical application and is not bundled. Tell the user.
- **No 行政法规**. 《信息网络传播权保护条例》(国务院, 2013) and 《计算机软件保护条例》are not bundled — but they are at flk.npc.gov.cn for manual fetch.
- **No case law**. PRC has 指导性案例 (guiding cases) from 最高法 and important 互联网法院 decisions. Roadmap v0.4.0.
- **No AI specialty**. 《生成式人工智能服务管理暂行办法》(2023) is 部门规章, not bundled. Critical for content generation work — v0.5.0.

## Hard limits

- This is statutory interpretation, not legal advice.
- PRC copyright enforcement is highly forum-dependent (北京互联网法院 vs 杭州 vs 广州 all have noticeably different practice). Statute reading alone won't predict litigation outcome.
- For any commercial decision in China, route through 中国律师 — preferably one with anime/IP experience and presence in the relevant forum.
