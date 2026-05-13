# legal-for-cn-jp

面向动画／影像内容行业的日中双语法律助手的 Claude 插件。

为动画师，技术美术、流程 TD、制片人、以及动画工作室内部小型法务团队设计——任何需要快速、可靠地搞清楚"日本或中国法律对这件事究竟怎么规定"，又不想立刻去找外部律师的人。

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

## 安装

在 Claude Code 会话内执行下列操作。

### 方式一：GitHub marketplace（推荐）

```
/plugin marketplace add ChenxingM/legal-for-cn-jp
/plugin install legal-for-cn-jp@legal-for-cn-jp
/reload-plugins
```

`/plugin list` 应能看到 `legal-for-cn-jp` 与 7 个 skill。

### 方式二：本地目录（已克隆仓库时）

```
/plugin marketplace add path\to\legal-for-cn-jp
/plugin install legal-for-cn-jp@legal-for-cn-jp
/reload-plugins
```

或一次性测试（不安装到 cache）：

```bash
claude --plugin-dir path\to\legal-for-cn-jp
```

### 升级

Claude Code 不会自动 `git pull`。本地拉新后再让 marketplace 重新读：

```bash
cd path\to\legal-for-cn-jp
git pull
```

在 Claude Code 会话里：

```
/plugin marketplace update legal-for-cn-jp
/reload-plugins
```

### 卸载

```
/plugin uninstall legal-for-cn-jp@legal-for-cn-jp
```

## 用例

### 用例 1：業務委託契約 を 偽装請負 + 下請法 ダブル監査

**场景**：工作室（資本金 2 億円）給 個人作画師（個人事業主）发外注合同，担心 偽装請負 + 下請法 都中。

**输入**：
```
レビューお願いします:
業務委託契約書 (アタッチ済み)
当方は資本金 2 億円のアニメ制作スタジオ、相手は個人事業主の作画作家です。
```

**激活的 skill**：`jp-labor-contract-review` + `jp-subcontract-review`

**输出**：労働者性判断基準 八要素チェック → 偽装請負 リスク判定／下請法 適用判定（資本金 > 1000 万円 + 個人 = 適用）→ 第3条 8 項書面チェック + 60日支払上限 + 11 禁止行為 + 改訂提案文

### 用例 2：中国信息网络传播权 解释

**场景**：制片人需要解释中国电视台播放与网络视频平台二次利用的法律差异。

**输入**：
```
中国《著作权法》对信息网络传播权（第10条第12项）和广播权（第11项）怎么区分？
对动画视听作品授权来说，这两个权利能分别授权吗？
```

**激活的 skill**：`cn-copyright-qa` + `cn-law-lookup`

**输出**：第10条 各权利逐条引用 + 信息网络传播权 vs 广播权 区分 + 视听作品下两权可分别授权的实务建议

### 用例 3：下請法 60 日支払期日 自检

**场景**：工作室"納品から放送後支払"的现金流惯例可能触发下請法。

**输入**：
```
当社（資本金 1500 万円）が個人原画スタッフに作画委託している。
納品から TV 放送後 (3〜4ヶ月後) 支払の慣行があるが、下請法 上どこまでセーフか？
```

**激活的 skill**：`jp-subcontract-review`

**输出**：下請法 適用判定 (情報成果物作成委託) → 法 第2条の2 60日支払期日 違反 → 第4条の2 14.6%/年 遅延利息 発生 → 第7条 公取委 勧告 + 公表 リスク → 改善案

### 用例 4：AE プラグインの OSS 依存审查

**场景**：TA 内部分发 AE plugin，依赖几个 npm 包，担心 license 兼容。

**输入**：
```
このAEプラグインの dependencies チェックして:
- lodash@4.17.21
- axios@1.6.2
- sharp@0.32.6
社内のみ配布、商用利用なし。
```

**激活的 skill**：`oss-license-review`

**输出**：各依赖 license 识别 + GPL 传染分析（sharp の依存にも注意）+ 兼容性矩阵 + 内部分発時の署名義務

### 用例 5：日中職務著作 対比

**场景**：中日合拍合同里"工作成果归属"条款，需要明确两侧法律差异。

**输入**：
```
日本の職務著作 (著作権法第15条) と 中国の职务作品 (著作权法第18条) の差を、
著作者人格権 と 著作財産権 の帰属で整理してほしい。
```

**激活的 skill**：`jp-copyright-qa` + `cn-copyright-qa` + `jp-law-lookup` + `cn-law-lookup`

**输出**：両法条文対比 + 法人著作物の要件差 + 著作者人格権 vs 著作者人格的權利 の取扱い差 + 跨境合同で明確化すべき事項

## 内置内容

**日本侧**：21 个文件——其中 17 部核心法律 + 下請法主法（共 17 部"法律"）+ 下請法施行令（政令）+ 下請法 3 部公正取引委員会規則，清洗后的 Markdown（约 2.5 MB），存放在 `references/laws/`，外加 8,952 部精简索引（`references/law-index.csv`，2.4 MB）。下請法系 5 文件来自公正取引委員会官網（`下請代金支払遅延等防止法.md` / `下請法施行令.md` / `下請法書面規則.md` / `下請法遅延利息規則.md` / `下請法書類保存規則.md`）。

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

## 未包含的内容

详见 `ROADMAP.md`。要点：

- **v0.2.2 / v0.3.0**：中国法长尾查询——扩展 `LRB_SOURCED_LAWS` 覆盖更多法律部门／行政法规／司法解释；或换更全的上游
- **v0.3.0**：日中英三语法律术语对照表、动画行业合同模板
- **v0.4.0**：判例检索（先日本后中国——判例／裁判文书）
- **v0.5.0**：AI 立法专项（生成式AI暂行办法、広島AIプロセス、EU AI Act 对照）

## 硬性边界——务必阅读

1. **不构成法律意见。** 任何输出在被采纳前都需经持牌律师审核。
2. **只覆盖成文法，不覆盖判例。** 判例（日本）和裁判文书（中国）在 v0.4.0 之前不在范围内。
3. **中国 AI 部门规章未内置。** 《生成式人工智能服务管理暂行办法》（国家网信办，2023）对 AI 内容业务关键，目前未内置。计划在 v0.5.0 加入。
4. **下請法 不在 e-Gov 中，未来更新需手动从 JFTC 抓。** v0.2.1 起内置了 下請法 主法 + 施行令 + 3 部公正取引委員会規則，但 e-Gov 批量数据不含 下請法，所以下次修正后没有自动同步——需要手工从 jftc.go.jp 重新抓取后覆盖本地文件。当前内置版反映到 平成21年改正（主法）/令和5年改正（書面規則）。
5. **中国法长尾查询暂不可用。** 当前版本仅 21 部核心法可在运行时查询。长尾查询计划通过扩展 LawRefBook 同步列表逐步覆盖。

## 许可证

插件代码使用 MIT。内置法条为公有领域政府作品。

- 日本：政府著作物，e-Gov 法令数据——公开。
- 中国：依照著作权法第 5 条第 1 项，中国政府作品属公有领域。
- 中国核心法语料来源 [LawRefBook/Laws](https://github.com/LawRefBook/Laws)（致谢；该项目当前未声明 license）。
