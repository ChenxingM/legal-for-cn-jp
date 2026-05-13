# legal-for-cn-jp

面向动画／影像内容行业的日中双语法律助手。

为技术美术、流程 TD、制片人、以及动画工作室内部小型法务团队设计——任何需要快速、可靠地搞清楚"日本或中国法律对这件事究竟怎么规定"，又不想立刻去找外部律师的人。

**本插件不能替代持牌律师（弁護士／律师）。** 它能给你的是条文原文、结构化分析、以及该追问的问题。涉及金钱、诉讼、监管机关的事，请找律师。

## v0.2.0 包含的内容

六个 skill：

| Skill | 用途 |
|---|---|
| `oss-license-review` | AE / Blender / UE / 3ds Max 工具链的 OSS 依赖审查——许可证兼容性、GPL 传染、署名义务 |
| `jp-copyright-qa` | 基于著作権法实际条文的问答。映画の著作物、職務著作、二次利用都锚定到具体条款 |
| `jp-labor-contract-review` | 审查雇用／業務委託／派遣合同。识别偽装請負风险、违法加班、労契法第 16 条违反 |
| `jp-law-lookup` | 日本法条查询——内置 16 部核心法律，10,257 部全量靠 e-Gov API 补长尾 |
| `cn-copyright-qa` | 基于 2020 年修订版著作权法的问答。视听作品、职务作品、信息网络传播权都锚定到具体条款 |
| `cn-law-lookup` | 中国法条查询——内置 21 部核心法律。长尾暂未覆盖（计划由 GitHub Actions 缓存 flk.npc.gov.cn） |

## 网络架构（公司网络下重要）

| 服务 | 用途 | .cn 被屏蔽时能访问吗？ |
|---|---|---|
| e-Gov 法令API v2 (laws.e-gov.go.jp) | 日本长尾查询 | ✅ .jp 域名，一般放行 |
| flk.npc.gov.cn | 仅由 GitHub Actions 周抓取，**不**在用户端运行时使用 | ⚠️ 用户端不需要访问，由 GH 服务器（美国／欧洲）抓取后回写到本仓库 |

中国侧核心 21 部由 GitHub Actions 每周一在 GH-hosted runner 上从 flk.npc.gov.cn 抓最新文本、有变化时自动开 PR。这样维护者和最终用户都不需要直接访问 .cn 域名。

## 内置内容

**日本侧**：16 部核心法律，清洗后的 Markdown（约 2.5 MB），存放在 `references/laws/`，外加 8,952 部精简索引（`references/law-index.csv`，2.4 MB）。

**中国侧**：21 部核心法律，清洗后的 Markdown（约 0.97 MB），存放在 `references/cn_laws/`。长尾（行政法规／司法解释／地方性法规等）当前版本不提供运行时查询，计划在后续版本中由 GitHub Actions 周缓存一批扩展集（详见 ROADMAP）。

**工具脚本**（Python，仅依赖标准库，运行时无第三方依赖）：
- `skills/jp-law-lookup/scripts/egov_client.py` —— e-Gov API v2 客户端
- `skills/cn-law-lookup/scripts/refresh_cn_corpus.py` —— 本地刷新脚本，用于保持中国核心法最新
- `tooling/cn-law-refresh/scraper.py` —— flk.npc.gov.cn 抓取器，由 GitHub Actions 调用

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

**自动（推荐）**：`.github/workflows/refresh-cn-laws.yml` 每周一 03:00 UTC 在 GH-hosted runner 上跑，从 flk.npc.gov.cn 拉最新文本，有变化时自动开 PR。终端用户 `git pull` 拿更新。

**手动**（仅当本地能直连 .cn 时）：

```bash
# 把新 .docx（从 flk.npc.gov.cn 下载）放到任意目录，然后：
refresh_cn_corpus.py /path/to/new/docx/
# 或针对单个文件：
refresh_cn_corpus.py /path/to/中华人民共和国反不正当竞争法_20250627.docx
# 把一部非核心法加进核心语料：
refresh_cn_corpus.py /path/to/file.docx --add
```

不需要重装插件——下次 Claude 会话自动加载新文本。

## 自动刷新（GitHub Actions）

本仓库部署了 `.github/workflows/refresh-cn-laws.yml`。每周一 03:00 UTC（12:00 JST）从 flk.npc.gov.cn 抓最新中国核心法，有变化时自动开 PR。

之所以放在 GitHub：公司网络通常屏蔽 .cn 域名，但 GitHub-hosted runner 在美国／欧洲可以直连 flk.npc.gov.cn。详见 `tooling/cn-law-refresh/README.md`。

## 时效性——使用前请阅读

**日本侧（内置）**：截至 2026-05-13 为当前版本。e-Gov API 客户端总是返回最新文本——任何对时效敏感的场景请优先用 API。

**日本侧（e-Gov API）**：始终最新。

**中国侧（21 部核心法律）**：截至 2026-05-13 为当前版本。由 GitHub Actions 每周自动从 flk.npc.gov.cn 刷新，PR 合并后即生效。

## v0.2.0 不包含的内容

详见 `ROADMAP.md`。要点：

- **v0.2.1 / v0.3.0**：中国法长尾查询——由 GitHub Actions 周缓存 flk.npc.gov.cn 的扩展集到本仓库（待维护者在能访问 .cn 的环境完成具体方案）
- **v0.3.0**：日中英三语法律术语对照表、动画行业合同模板
- **v0.4.0**：判例检索（先日本后中国——判例／裁判文书）
- **v0.5.0**：AI 立法专项（生成式AI暂行办法、広島AIプロセス、EU AI Act 对照）

## 硬性边界——务必阅读

1. **不构成法律意见。** 任何输出在被采纳前都需经持牌律师审核。
2. **只覆盖成文法，不覆盖判例。** 判例（日本）和裁判文书（中国）在 v0.4.0 之前不在范围内。
3. **中国 AI 部门规章未内置。** 《生成式人工智能服务管理暂行办法》（国家网信办，2023）对 AI 内容业务关键，目前未内置。计划在 v0.5.0 加入。
4. **下請代金支払遅延等防止法 不在 e-Gov 中。** 日本《下請法》因不明原因未纳入 e-Gov 批量数据。目前请使用公正取引委員会官网。
5. **中国法长尾查询暂不可用。** 当前版本仅 21 部核心法可在运行时查询。长尾查询由后续版本通过 GitHub Actions 周缓存 flk.npc.gov.cn 实现。

## 许可证

插件代码使用 MIT。内置法条为公有领域政府作品。

- 日本：政府著作物，e-Gov 法令数据——公开。
- 中国：依照著作权法第 5 条第 1 项，中国政府作品属公有领域。
- flk.npc.gov.cn 抓取器的反向工程参考了 `github.com/twang2218/law-datasets`（致谢）。
