# e-Gov 法令API v2 — Usage Notes

Detailed reference for the API client at `../scripts/egov_client.py`. The official API is hosted by 総務省行政管理局 and the spec is at https://laws.e-gov.go.jp/api/2/swagger-ui.

## No authentication required

The API is open. No API key, no OAuth, no rate-limit headers in the public spec. Be polite — don't fire 1000+ requests in a tight loop.

## Endpoints in use

### `GET /laws` — search by title

Returns law metadata for laws whose title matches `law_title` (partial match) and other filters. Use this to discover the `law_id` you need for `fetch`.

```bash
egov_client.py search "個人情報" --law-type Act --limit 5
```

Returns up to `--limit` records, each with `law_id`, `law_num`, `title`, `law_type`, `promulgation_date`.

### `GET /keyword` — full-text search

Searches the body text of every law in the database. Supports AND, OR, NOT, and wildcards.

```bash
# Single keyword
egov_client.py keyword "アニメーション"

# AND search (space-separated in URL; pass as one quoted arg)
egov_client.py keyword "著作権 二次的"

# OR
egov_client.py keyword "アニメ OR 動画"

# NOT
egov_client.py keyword "著作権 NOT 隣接"

# Wildcard
egov_client.py keyword "著作*"
```

Returns hit count and per-law snippets showing where the keyword appears. Use these snippets to decide which law to `fetch` for the full text.

Filter by law type to narrow noise:
- `--law-type Act` — statutes only (most common)
- `--law-type CabinetOrder` — 政令
- `--law-type MinisterialOrdinance` — 省令
- `--law-type Rule` — 規則

Multiple types: `--law-type "Act,CabinetOrder"`.

### `GET /law_data/{law_id}` — fetch full text

Returns the entire current text of one law. The client converts the XML response into readable plain text preserving article structure.

```bash
egov_client.py fetch 345AC0000000048
```

Get historical text (as it stood on a given date):

```bash
egov_client.py fetch 345AC0000000048 --asof 2020-04-01
```

### `GET /law_revisions/{law_id}` — revision history

Lists every amendment to a law with dates.

```bash
egov_client.py revisions 345AC0000000048
```

Useful for "when did this rule change" questions.

## Law ID format

e-Gov law IDs follow the pattern `[era_year][type_code][serial]_[date]_[amendment_id]`. The short form `[era_year][type_code][serial]` (the first segment) is enough for API calls.

Common type codes:
- `AC` — 法律 (Act)
- `CO` — 政令 (Cabinet Order)
- `M` — 省令 (Ministerial Ordinance)
- `R` — 規則 (Rule)
- `DF` — 太政官布告 (historical)

Era year: 3-digit. `345` = 昭和45 (1970). `129` = 明治29 (1896). `405` = 平成5 (1993). `506` = 令和6 (2024).

## Practical patterns

### Finding the right law when the user only knows the topic

```bash
# Step 1: keyword search to find candidate laws
egov_client.py keyword "ステマ" --limit 5

# Step 2: from the hits, pick the law_id
# (e.g. 景品表示法 — 337AC0000000134)

# Step 3: fetch the full text
egov_client.py fetch 337AC0000000134
```

### Comparing current text to a specific date

```bash
egov_client.py fetch 345AC0000000048                    # current
egov_client.py fetch 345AC0000000048 --asof 2018-01-01  # pre-TPP-11
```

### Finding which laws mention a specific keyword

```bash
egov_client.py keyword "ディープフェイク" --limit 20 --sentences-limit 2
```

Returns the laws that contain the term plus context snippets. As of 2025, "ディープフェイク" is not yet in statute — useful for confirming that.

## Failure modes

- `404 / "取得結果が０件です"` — no hits. Try a broader keyword or different filter.
- Network timeouts — the API is generally fast but occasional 502/503. Retry once before falling back.
- HTML in snippets — by default the API wraps keyword hits in HTML tags. The client strips `<mark>` tags it sets itself; if you change `highlight_tag`, update the strip regex.

## What this API does NOT provide

- 判例 (case law). Use D1-Law, 判例検索 on 裁判所Web, LEX/DB, etc.
- 通達 / ガイドライン (ministerial guidance). Some are in the database; many are not. For 文化庁 著作権 guidance, check bunka.go.jp directly.
- 旧法 (laws no longer in force). Some are in the index for historical reference but most are excluded.
- 国際条約 (treaties). Separate database.
