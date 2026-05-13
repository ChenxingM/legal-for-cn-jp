# legal-for-cn-jp

面向动画／影像内容行业的日中双语法律助手。

为技术美术、流程 TD、制片人、以及动画工作室内部小型法务团队设计——任何需要快速、可靠地搞清楚"日本或中国法律对这件事究竟怎么规定"，又不想立刻去找外部律师的人。

**本插件不能替代持牌律师（弁護士／律师）。** 它能给你的是条文原文、结构化分析、以及该追问的问题。涉及金钱、诉讼、监管机关的事，请找律师。

## v0.2.1 包含的内容

七个 skill：

| Skill | 用途 |
|---|---|
| `oss-license-review` | AE / Blender / UE / 3ds Max 工具链的 OSS 依赖审查——许可证兼容性、GPL 传染、署名义务 |
| `jp-copyright-qa` | 基于著作権法实际条文的问答。映画の著作物、職務著作、二次利用都锚定到具体条款 |
| `jp-labor-contract-review` | 审查雇用／業務委託／派遣合同。识别偽装請負风险、违法加班、労契法第 16 条违反 |
| `jp-subcontract-review` | **新增**。下請取引 (B2B 外注) 的下請法合规审计：親-下請事業者 资本阈值判定、第3条 8 项书面必备事项、60 日支付上限、第4条 11 项禁止行为、14.6%/年遅延利息、2 年书类保存义务 |
| `jp-law-lookup` | 日本法条查询——内置 17 部核心法律 + 下請法系 4 部规则／政令，10,257 部全量靠 e-Gov API 补长尾 |
| `cn-copyright-qa` | 基于 2020 年修订版著作权法的问答。视听作品、职务作品、信息网络传播权都锚定到具体条款 |
| `cn-law-lookup` | 中国法条查询——内置 21 部核心法律。长尾暂未覆盖（计划由 LawRefBook 同步覆盖更多法律部门） |

## 内置内容

**日本侧**：17 部核心法律 + 下請法系 4 部規則／政令，清洗后的 Markdown（约 2.5 MB），存放在 `references/laws/`，外加 8,952 部精简索引（`references/law-index.csv`，2.4 MB）。下請法系 5 文件来自公正取引委員会官網（`下請代金支払遅延等防止法.md` / `下請法施行令.md` / `下請法書面規則.md` / `下請法遅延利息規則.md` / `下請法書類保存規則.md`）。

**中国侧**：21 部核心法律，清洗后的 Markdown（约 0.97 MB），存放在 `references/cn_laws/`。长尾（行政法规／司法解释／地方性法规等）当前版本不提供运行时查询，计划在后续版本中由 GitHub Actions 周缓存一批扩展集（详见 ROADMAP）。

**工具脚本**（Python，仅依赖标准库，运行时无第三方依赖）：
- `skills/jp-law-lookup/scripts/egov_client.py` —— e-Gov API v2 客户端
- `skills/cn-law-lookup/scripts/refresh_cn_corpus.py` —— 本地刷新脚本，用于从 .docx 维护中国核心法
- `tooling/cn-law-refresh/scraper.py` —— LawRefBook 同步器，由 GitHub Actions 调用

**插件总体积**：约 6 MB。

## 如何触发

Skill 会被常见说法自动触发（日文、英文、中文均可）：

- "Review this dependency list" → `oss-license-review`
- "著作権法第30条の中身は？" → `jp-copyright-qa` + `jp-law-lookup`
- "中国著作权法对XX怎么规定" → `cn-copyright-qa` + `cn-law-lookup`
- "この業務委託契約レビューして" → `jp-labor-contract-review`
- "民法典第533条" → `cn-law-lookup`

## 工具用法

### e-Gov 客户端（日本）

```bash
egov_client.py search "建築基準" --limit 5
egov_client.py keyword "ディープフェイク"
egov_client.py fetch 345AC0000000048
egov_client.py fetch 345AC0000000048 --asof 2020-04-01
egov_client.py revisions 345AC0000000048
```

### 刷新中国核心法语料

两条路径：

**自动同步（推荐）**：`.github/workflows/refresh-cn-laws.yml` 每周一 03:00 UTC 在 GH-hosted runner 上跑 `scraper.py`，`git clone` LawRefBook/Laws 然后挑出我们要的 17 部最新版同步到 `references/cn_laws/`。有变化时自动开 PR。终端用户 `git pull` 拿更新。

**手动**（owner-maintained 那 4 部，或新加法律时）：

```bash
# 把新 .docx 放到任意目录（例如从 flk.npc.gov.cn 在能访问 .cn 的环境下载）：
refresh_cn_corpus.py /path/to/new/docx/
# 或针对单个文件：
refresh_cn_corpus.py /path/to/中华人民共和国反不正当竞争法_20250627.docx
# 把一部非核心法加进核心语料：
refresh_cn_corpus.py /path/to/file.docx --add
```

不需要重装插件——下次 Claude 会话自动加载新文本。

## 自动刷新（GitHub Actions）

本仓库部署了 `.github/workflows/refresh-cn-laws.yml`。每周一 03:00 UTC（12:00 JST）从 LawRefBook/Laws 同步最新中国核心法，有变化时自动开 PR。详见 `tooling/cn-law-refresh/README.md`。

## 时效性——使用前请阅读

**日本侧（内置）**：截至 2026-05-13 为当前版本。e-Gov API 客户端总是返回最新文本——任何对时效敏感的场景请优先用 API。

**日本侧（e-Gov API）**：始终最新。

**中国侧（21 部核心法律）**：截至 2026-05-13 为当前版本。17 部由 GitHub Actions 每周自动从 LawRefBook/Laws 同步，PR 合并后即生效。4 部 owner-maintained（民法典 / 反不正当竞争法 / 网络安全法 / 仲裁法）由维护者从权威 .docx 刷新——LawRefBook 跟上 2025 修正后可移回自动同步列表。

## v0.2.0 不包含的内容

详见 `ROADMAP.md`。要点：

- **v0.2.1 / v0.3.0**：中国法长尾查询——扩展 `LRB_SOURCED_LAWS` 覆盖更多法律部门／行政法规／司法解释；或换更全的上游
- **v0.3.0**：日中英三语法律术语对照表、动画行业合同模板
- **v0.4.0**：判例检索（先日本后中国——判例／裁判文书）
- **v0.5.0**：AI 立法专项（生成式AI暂行办法、広島AIプロセス、EU AI Act 对照）

## 硬性边界——务必阅读

1. **不构成法律意见。** 任何输出在被采纳前都需经持牌律师审核。
2. **只覆盖成文法，不覆盖判例。** 判例（日本）和裁判文书（中国）在 v0.4.0 之前不在范围内。
3. **中国 AI 部门规章未内置。** 《生成式人工智能服务管理暂行办法》（国家网信办，2023）对 AI 内容业务关键，目前未内置。计划在 v0.5.0 加入。
4. **下請代金支払遅延等防止法 + 4 部相关规则／政令已内置。** v0.2.1 起，主法 + 施行令 + 第3条书面规则 + 第4条の2 遅延利息规则 + 第5条书类保存规则 全部从公正取引委員会官網拉取后内置；用 `jp-subcontract-review` skill 审计 下請取引。e-Gov 中仍然没有 下請法，所以未来更新时需要重新从 jftc.go.jp 抓最新版（当前内置版反映到 平成21年改正/令和5年規則改正）。
5. **中国法长尾查询暂不可用。** 当前版本仅 21 部核心法可在运行时查询。长尾查询计划通过扩展 LawRefBook 同步列表逐步覆盖。

## 许可证

插件代码使用 MIT。内置法条为公有领域政府作品。

- 日本：政府著作物，e-Gov 法令数据——公开。
- 中国：依照著作权法第 5 条第 1 项，中国政府作品属公有领域。
- 中国核心法语料来源 [LawRefBook/Laws](https://github.com/LawRefBook/Laws)（致谢；该项目当前未声明 license）。
