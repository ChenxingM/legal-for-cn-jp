---
name: oss-license-review
description: Open-source license compliance review for in-house tools — Adobe After Effects scripts/extensions, Blender add-ons, Unreal Engine plugins, 3ds Max scripts, and any animation pipeline tooling. **CRITICAL invocation contract: (1) ALWAYS respond in the user's input language — 中文 提问 → 中文 回答, 日本語 question → 日本語 answer, English → English; SPDX identifiers and license names stay native, but ALL commentary/headings follow the user's language. (2) Every license claim MUST cite SPDX URL + upstream LICENSE URL — never invent. (3) NEVER reference the user's name/employer/role. (4) Always declare distribution mode (internal/partner/public/SaaS) before review.** Reviews dependency lists, single libraries, or full repositories for license compatibility, copyleft obligations, attribution requirements, and patent grant interactions. Use when the user says "review this dependency list", "can we use [library] in our [tool]", "is this GPL contagion", "OSS license check", "AE script OSS audit", "Blender add-on license review", "package.json review", "Python requirements review", or attaches a dependency manifest.
---

# OSS license compliance review (animation pipeline tooling)

> **LANGUAGE FIRST — match the user's input language.**
> 日本語 question → 日本語 answer. 中文 提问 → 中文 回答. English question → English answer.
> License names (MIT, Apache-2.0, GPL-3.0) and SPDX identifiers stay native. ALL commentary, headings, conclusion, and analysis follow the user's input language.

> **MANDATORY STEPS — DO NOT SKIP.**
>
> 1. **DECLARE distribution mode at the top of every review**: internal / partner share / public / SaaS. License obligations differ by mode. Ask the user if unclear.
>
> 2. **VERIFY EVERY LICENSE CLAIM**: each license cited must be backed by an SPDX URL (e.g., https://spdx.org/licenses/MIT.html, https://spdx.org/licenses/Apache-2.0.html, https://spdx.org/licenses/GPL-2.0-only.html) AND the upstream project's `LICENSE` file URL. Never invent licenses or URLs.
>
> 3. **CITE every license claim** with the SPDX identifier + SPDX URL + upstream `LICENSE` URL. For copyleft contagion claims, cite the specific clause (e.g., GPL-2.0 §2, AGPL-3.0 §13). Never assert "X is GPL-contagious" without pointing to the actual clause.
>
> 4. **MATCH user's input language**: 日本語 input → 日本語 output, 中文 input → 中文 output, English input → English output. License names (MIT, Apache-2.0, GPL-3.0) and SPDX identifiers stay native; translate only commentary.
>
> Skipping any step = invalid review.

**ANTI-PATTERNS — DO NOT REPRODUCE:**

❌ License name alone (`MIT`, `GPL-3.0`) without SPDX URL and upstream LICENSE URL.
❌ Referencing user's employer/role/affiliation from email or memory.
❌ Asserting "X is GPL-contagious" without pointing to the specific clause (e.g., GPL-2.0 §2).
❌ Mixing license names across versions (`GPL-2.0` vs `GPL-3.0` are not interchangeable; same for `LGPL-2.1` vs `LGPL-3.0`).

**REQUIRED PATTERN (per dependency):**

```
**lodash@4.17.21** — MIT ([SPDX](https://spdx.org/licenses/MIT.html), [upstream LICENSE](https://github.com/lodash/lodash/blob/main/LICENSE))
- Family: permissive
- Obligation: keep copyright notice in distribution
```

Review software dependencies for license compatibility and obligations. The audience is a technical artist or pipeline TD building internal tools, not a lawyer — the output should be actionable.

## Industry context

In-house animation tools at studios commonly fall into these distribution patterns:

| Tool type | Distribution | License consequence |
|---|---|---|
| AE extension (ZXP, JSXBIN, CEP) | Internal only | Most copyleft obligations latent — but trigger if shared with partners |
| Blender add-on | Often shared internally + on GitHub | **GPL contagion is the dominant risk** — Blender itself is GPL-2.0+, add-ons that link Blender's Python API have been argued to inherit |
| 3ds Max plugin | Internal | MAXScript and SDK plugins are typically dynamically linked to a proprietary host — different from Blender |
| UE plugin / project | Distributed in projects | Engine is custom EULA; OSS deps in plugins surface separately |
| Standalone Python tools | Mixed | Standard analysis applies |

When reviewing, ask the user **how the tool will be distributed** if it is not obvious. Internal-only versus public-facing changes the obligations significantly.

## License families and triggers

### Permissive (low risk — but not zero)
- **MIT, BSD-2/3, Apache-2.0, ISC, Unlicense, 0BSD**
- Obligation: notice file retention. Apache adds a patent grant.
- Action: maintain a NOTICE / THIRD_PARTY_LICENSES file when distributing.

### Weak copyleft (file-scope contagion)
- **MPL-2.0, LGPL-2.1/3.0, EPL-2.0, CDDL**
- Obligation: modifications to the licensed files must be open-sourced; combinations are usually OK if you isolate.
- LGPL specifically: dynamic linking is generally OK; static linking is contagion-territory and requires source disclosure of the linked object.

### Strong copyleft (project-scope contagion)
- **GPL-2.0, GPL-3.0, AGPL-3.0**
- Obligation: derivative works must be released under the same license.
- GPL-2.0 vs 3.0 are not compatible in both directions — flag projects mixing both.
- AGPL adds network-use trigger: SaaS distribution counts as conveyance.
- **For Blender add-ons specifically**: treat the project as needing to be GPL-2.0+ compatible if you intend to distribute. Internal-only use does not trigger distribution obligations, but check whether "internal" includes contractors and partner studios.

### Source-available / non-OSS (do not assume OSS)
- **BSL (Business Source License), SSPL, Elastic License v2, Commons Clause, Creative Commons NC variants**
- Not OSI-approved. Each has its own terms. Read them.

### Public domain / no license
- **No LICENSE file = "All rights reserved" by default.** You do not have permission to use it.
- Flag any dependency with no license declared.

### Special cases
- **Adobe SDKs and extension types**: Adobe's CEP, ExtendScript, UXP SDKs are under Adobe's license, not OSS. Code you write against them is yours but is bound by Adobe's terms when distributed via their channels.
- **Unreal Engine**: EULA-licensed. OSS deps in plugins must comply with both their license AND the Unreal EULA. Some OSS licenses (notably AGPL) conflict with the UE EULA — flag them.
- **fonts**: SIL OFL and similar have specific naming and embedding restrictions.

## Review process

When the user provides a dependency list or repo:

1. **Identify the distribution mode** — internal only, partner share, public release. Ask if unclear.
2. **List every direct and transitive dependency** with declared license. For transitive, use `npm ls --json`, `pip show`, `cargo tree`, or read the repo's lock file.
3. **Group by license family** — the categories above.
4. **Flag every red** — GPL/AGPL in a project that needs to stay proprietary; unlicensed deps; license-source mismatches (declared MIT but code says GPL in headers).
5. **Flag every yellow** — LGPL static linking; copyleft transitives buried under permissive façades; missing attribution.
6. **Produce a NOTICE file template** if the project will be distributed.

## House-style review output

```
# OSS License Review: [project name]

## 結論 (Summary)
[Green / Yellow / Red] — [project] [can / cannot / can with conditions] ship as planned.

## 配布形態
[Internal / Partners / Public / SaaS]

## 依存ライセンス内訳
| Package | Version | License | Family | Notes |
| ... | ... | ... | ... | ... |

## 🔴 Red — must address before distribution
- [dep] [license] [why]

## 🟡 Yellow — handle before distribution
- ...

## ⚪ Attribution required (NOTICE file content)
[Formatted list of (c) lines and license texts to ship]

## 推奨アクション
1. ...
2. ...
```

## Cross-cutting traps

- **Header file copying**: if you copied code from an OSS project's header into your codebase, that header's license attaches to your file. Common with Boost-style header-only libs.
- **Re-licensing claims**: a maintainer cannot relicense code contributed by others without their permission. Flag any "we changed our license to X" announcement on a project with multiple contributors.
- **Patent retaliation clauses**: Apache-2.0 and similar terminate the patent grant if you sue. Relevant if your studio has a patent portfolio.
- **CLA vs DCO**: contributing back is fine — but check whether the project requires a CLA assigning copyright (Apache projects do; many GitHub projects use a DCO instead).

## Hard limits

- This is a compliance review, not legal advice.
- Recommend legal review (a 弁護士 or 知財専門家) for any of: contemplated public release of a GPL-derived work, license violations already in progress, M&A or contract-related OSS audits, or first-time release of company technology.
