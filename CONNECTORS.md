# Connectors

This plugin is distribution-generic: it does not assume any particular studio's internal tools or storage system.

## External dependencies

Only one external service: **e-Gov 法令API v2** (`https://laws.e-gov.go.jp/api/2/`). It is:

- Operated by 総務省行政管理局 (Ministry of Internal Affairs and Communications, Japan)
- Public, open, no authentication, no API key
- Stable URL since 2024 (v1 was deprecated)
- Spec: https://laws.e-gov.go.jp/api/2/swagger-ui

The plugin does not need any user-side connector configuration.

## Studio-specific customization (optional)

If you fork this plugin for a specific studio, the places to customize are:

| Location | What to customize | Why |
|---|---|---|
| `skills/jp-labor-contract-review/SKILL.md` | House-style review output template | Match your team's existing memo format |
| `skills/jp-copyright-qa/SKILL.md` | Escalation triggers — which contacts to recommend | Specific to your legal department |
| `references/laws/` | Add studio-specific reference docs | Internal IP licensing playbooks, partner-specific positions |
| `plugin.json` | author, homepage | Identify the fork |

Forks intended for distribution beyond one studio should keep the generic shape and add studio-specific content under a separate `references/internal/` subdirectory that is gitignored.

## Future connector hooks

Versions v0.2.0+ will introduce optional connectors. None are required:

- **flk.npc.gov.cn** (国家法律法规数据库) — Chinese statute API, free, registration required
- **Chinese case law sources** — may require commercial subscription (北大法宝, 威科先行)

The plugin will continue to work with zero external connectors for the bundled corpus; connectors will only be needed for the long-tail queries beyond bundled content.
