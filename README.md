# legal-for-cn-jp

A Japan + China bilingual law assistant for the animation / visual-content industry.

Built for technical artists, pipeline TDs, producers, and small in-house legal teams at animation studios — anyone who needs a fast, grounded answer to "what does Japanese or Chinese law actually say about this" without an immediate trip to outside counsel.

**This plugin is not a substitute for a licensed attorney (bengoshi / 律师).** It gives you the statutory text, structured analysis, and the questions to ask. For anything that involves money, litigation, or a regulator, get a lawyer.

## What's in v0.2.0

Six skills:

| Skill | What it does |
|---|---|
| `oss-license-review` | OSS dependency review for AE / Blender / UE / 3ds Max tools — license compatibility, GPL contagion, attribution duties |
| `jp-copyright-qa` | 著作権法 Q&A grounded in the actual statute. Anchors 映画の著作物, 職務著作, 二次利用 to specific articles |
| `jp-labor-contract-review` | Reviews 雇用 / 業務委託 / 派遣 contracts. Flags 偽装請負 risk, illegal overtime, 労契法 第16条 violations |
| `jp-law-lookup` | Japanese statute lookup — 16 core laws bundled, 10,257-law e-Gov API for the long tail |
| `cn-copyright-qa` | 著作权法 Q&A grounded in the 2020-revised statute. Anchors 视听作品, 职务作品, 信息网络传播权 |
| `cn-law-lookup` | PRC statute lookup — 21 core laws bundled, 22,552-law HuggingFace index for the long tail |

## Network architecture (important for corporate environments)

| Service | Used for | Reachable when .cn is blocked? |
|---|---|---|
| e-Gov 法令API v2 (laws.e-gov.go.jp) | Japan long-tail lookup | ✅ .jp domain, generally allowed |
| HuggingFace datasets (huggingface.co + cas-bridge.xethub.hf.co) | PRC long-tail lookup | ✅ no .cn dependency |
| flk.npc.gov.cn | NOT used at runtime | ⚠️ only used by the user for manual core-statute refresh |

The PRC long-tail lookup deliberately uses HuggingFace's mirror of the 国家法律法规数据库 instead of flk.npc.gov.cn so the plugin works even on networks that block .cn domains.

## What's bundled

**Japan side**: 16 core statutes as cleaned Markdown (~2.5 MB) in `references/laws/`, plus 8,952-law slim index (`references/law-index.csv`, 2.4 MB).

**China side**: 21 core statutes as cleaned Markdown (~0.97 MB) in `references/cn_laws/`, plus 22,552-law HuggingFace index covering 法律 / 宪法 / 行政法规 / 司法解释 / 地方性法规 / 监察法规 (`references/cn-law-index.csv`, 3.5 MB).

**Tooling** (Python, stdlib only — no third-party deps required at runtime):
- `skills/jp-law-lookup/scripts/egov_client.py` — e-Gov API v2 client
- `skills/cn-law-lookup/scripts/hf_client.py` — HuggingFace dataset client
- `skills/cn-law-lookup/scripts/refresh_cn_corpus.py` — local refresh script for keeping PRC core laws current

**Total plugin size**: ~10 MB.

## How to invoke

The skills auto-trigger on common phrasings (Japanese, English, or Chinese):

- "Review this dependency list" → `oss-license-review`
- "著作権法第30条の中身は？" → `jp-copyright-qa` + `jp-law-lookup`
- "中国著作权法对XX怎么规定" → `cn-copyright-qa` + `cn-law-lookup`
- "この業務委託契約レビューして" → `jp-labor-contract-review`
- "民法典第533条" → `cn-law-lookup`

## Tooling usage

### e-Gov client (JP)

```bash
egov_client.py search "建築基準" --limit 5
egov_client.py keyword "ディープフェイク"
egov_client.py fetch 345AC0000000048
egov_client.py fetch 345AC0000000048 --asof 2020-04-01
egov_client.py revisions 345AC0000000048
```

### HuggingFace client (CN)

```bash
hf_client.py search "信息网络传播权"
hf_client.py search "著作权" --law-type "司法解释"
hf_client.py fetch 934
hf_client.py fetch-title "信息网络传播权保护条例"
```

### Refresh PRC core corpus

When a PRC core law gets amended:

```bash
# Drop the new .docx (downloaded from flk.npc.gov.cn) in any directory, then:
refresh_cn_corpus.py /path/to/new/docx/
# Or a single file:
refresh_cn_corpus.py /path/to/中华人民共和国反不正当竞争法_20250627.docx
# Add a non-core law to the corpus:
refresh_cn_corpus.py /path/to/file.docx --add
```

No plugin reinstall required — next Claude session picks up the new text.

## Freshness — read before relying on output

**Japan side (Bundled)**: current as of 2026-05-13. The e-Gov API client always returns current text — prefer the API for anything where staleness matters.

**Japan side (e-Gov API)**: always current.

**China side (21 core statutes)**: current as of 2026-05-13, rebuilt from the user's batch download.

**China side (HuggingFace index, 22,552 laws)**: 2023-09 snapshot. **The bundled core 21 supersede HF text for those 21 laws.** For non-core laws amended after 2023-09 (e.g., 反不正当竞争法 2025-06, 网络安全法 2025-10), pull the latest docx and run `refresh_cn_corpus.py --add` to bring it into the core set.

## What's not in v0.2.0

See `ROADMAP.md`. Highlights:

- **v0.3.0**: Trilingual JP/CN/EN legal terminology table, anime-industry contract templates
- **v0.4.0**: Case law search (Japan first, then China — 判例 / 裁判文书)
- **v0.5.0**: AI legislation specialty (生成式AI暂行办法, 広島AIプロセス, EU AI Act mapping)

## Hard limits — read these

1. **Not legal advice.** Every output is for review by a qualified attorney before being relied on.
2. **Statutes only, no case law.** 判例 (Japan) and 裁判文书 (China) are out of scope until v0.4.0.
3. **PRC AI 部门规章 not bundled.** 《生成式人工智能服务管理暂行办法》(国家网信办, 2023) is critical for AI content work and is not in the HuggingFace index. v0.5.0.
4. **下請代金支払遅延等防止法 not in e-Gov.** Japan's Subcontract Act is missing from the e-Gov bulk feed for unknown reasons. Use the 公正取引委員会 site for now.
5. **HuggingFace data is 2023-09**. For laws amended after that date, use `refresh_cn_corpus.py` to bring in the latest docx.

## License

MIT for the plugin code. The bundled statutes are public-domain government works.

- Japan: 政府著作物, e-Gov 法令データ — public.
- China: PRC government works in the public domain per 著作权法 第5条第1项.
- HuggingFace dataset `twang2218/chinese-law-and-regulations` is Apache 2.0 — attribution to the maintainer (`twang2218`) is included in this README.
