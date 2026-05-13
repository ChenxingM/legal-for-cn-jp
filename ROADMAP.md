# Roadmap

The vision is a Japan-China bilingual legal assistant for the animation industry. v0.1.0 ships the Japan side. Subsequent versions widen the geographic and content scope.

## v0.1.0 — shipped

- 4 skills: oss-license-review, jp-copyright-qa, jp-labor-contract-review, jp-law-lookup
- 16 core Japanese statutes bundled offline
- e-Gov 法令API v2 client for the long tail
- ~5 MB total

## v0.2.0 — shipped (Chinese statutory law)

- 21 core PRC statutes bundled from user's 2026-05 docx batch download
- `cn-law-lookup` skill against the bundled 21 (no .cn dependency at runtime)
- `cn-copyright-qa` skill with cross-references to Japan-side concepts
- `refresh_cn_corpus.py` for local corpus updates without plugin reinstall
- GitHub Actions workflow `.github/workflows/refresh-cn-laws.yml` — weekly sync of 17 of the 21 core statutes from `github.com/LawRefBook/Laws` (a community-maintained GitHub corpus that handles flk.npc.gov.cn's 2026 SPA migration for us). The remaining 4 (民法典, 反不正当竞争法, 网络安全法, 仲裁法) are owner-maintained via `refresh_cn_corpus.py` from authoritative .docx because LawRefBook hasn't picked up their 2025 amendments yet.
- Total plugin size ~6 MB

Deferred from original v0.2.0 plan:
- `cn-labor-contract-review` skill — folded into the JP version's logic; can be split out later if user demand justifies it
- Long-tail PRC law lookup beyond the bundled 21 — the v0.2.0 build originally shipped a HuggingFace index for this, which has been removed. Direct scraping of flk.npc.gov.cn (the originally planned replacement) was abandoned after their 2026 SPA migration broke the unofficial JSON API. Current plan: extend `LRB_SOURCED_LAWS` in `scraper.py` to cover more 法律部门 / 行政法规 / 司法解释 from LawRefBook in v0.3.0.

(下請法 was also deferred from v0.2.0 — shipped in v0.2.1 below.)

## v0.2.1 — shipped (incremental refinements)

- **下請代金支払遅延等防止法 (下請法) + 4 implementing rules** fetched from 公正取引委員会 (jftc.go.jp) and bundled in `references/laws/`. Includes 主法 (12 articles + 附則), 施行令 (cabinet order on 情報成果物/役務 definitions and electronic consent), 書面規則 (8 mandatory written-contract items under 第3条), 遅延利息規則 (14.6%/year rate under 第4条の2), and 書類保存規則 (12 record-items + 2-year retention under 第5条). Reflects amendments through 平成21年法律第51号 (act) and 令和5年公正取引委員会規則第3号 (書面規則).
- **`jp-subcontract-review` skill** — new dedicated audit skill for 下請法 compliance: 親-下請事業者 capital-threshold decision tree, the 8 mandatory items, 60-day payment ceiling, 11 prohibited 親事業者 acts, late-interest computation, records retention, anime-industry mappings, house-style audit output. Distinct from `jp-labor-contract-review` (which handles worker-classification / 偽装請負).

Still deferred to later (v0.2.2 or v0.3.0):

- `cn-labor-contract-review` as standalone skill (currently the JP-side skill does double duty for Chinese contracts)
- 部门规章 bundle for the most cited rules in anime work:
  - 《生成式人工智能服务管理暂行办法》(国家网信办, 2023)
  - 《互联网信息服务深度合成管理规定》(国家网信办, 2023)
  - 《信息网络传播权保护条例》(国务院, 2013)
  - 《计算机软件保护条例》(国务院, 2013)
  - 《广告语言文字管理暂行规定》

## v0.3.0 — trilingual terminology + contract templates

Goal: bridge the JP / CN / EN legal vocabulary so cross-border contracts stop suffering from translation drift.

- Trilingual legal glossary, ~500 entries — populated initially from 著作権法 / 著作权法 article-by-article term comparison
- Skill: `legal-terminology` — looks up a term in any of three languages, returns the others plus the controlling statute
- Anime-industry contract template corpus in `references/templates/`:
  - 製作委員会契約 / Production committee agreement
  - 原画外注契約 / Drawing commission agreement
  - 声優出演契約 / Voice talent agreement
  - 海外配信ライセンス / Overseas distribution license
  - キャラクター利用許諾 / Character licensing
  - 共同制作契約 (中日合作) / China-Japan co-production
- Skill: `anime-contract-review` — reviews against the templates

This phase needs **the user to provide actual templates** from their studio practice (sanitized). Public-domain templates from JIBA (Japan Branding Association) or JCAA can also be used, with attribution.

## v0.4.0 — case law

The big one. Statutes tell you what the law says; cases tell you how courts actually apply it.

- Japanese case law corpus, starting with the 50-100 most-cited animation industry decisions:
  - 鋼の錬金術師同人事件 (2007 東京地裁)
  - ときめきメモリアル事件 (2001 最判)
  - ファイアーエムブレム事件 (1999 東京地裁)
  - ライブドア「ニュース女子」事件
  - キャラクターポンキッキ事件
  - キン肉マン事件 (1976)
  - And more — full list curated by relevance
- Sources: 裁判所Web (公開判例), 判例タイムズ, 判例時報, D1-Law (if budget)
- Skill: `jp-case-lookup` — search and retrieve
- Chinese case law:
  - 中国裁判文书网 (where accessible)
  - 最高人民法院指导性案例 (free, mandatory persuasive)
  - 北京互联网法院 AI 系列判决 (重要先例)
  - Skill: `cn-case-lookup`
- Cases get stored as searchable text + structured metadata (court, date, parties, holding, key articles cited). Probably SQLite or a small FTS index rather than raw Markdown for scale.

## v0.5.0 — AI law specialty

AI law is moving faster than any other area and is not well covered by general statute lookup.

- 生成式人工智能服务管理暂行办法 (PRC, 2023) — full text + analysis
- 広島AIプロセス国際指針 / AI事業者ガイドライン (Japan, soft law) — summarized with cross-references
- EU AI Act — relevant provisions for content generators
- 文化庁 AI 著作権 guidance — collected from announcements
- Skill: `ai-content-compliance` — answers "can we use this AI-generated content under [jurisdiction]" questions

## v1.0.0 — production release

Polish, internal testing at one studio, documentation pass, governance:

- Update cadence: weekly CN sync from LawRefBook (already in place); monthly JP statute refresh from e-Gov
- Case law additions: quarterly
- Versioned releases with changelog
- Internal review process for new skill contributions
