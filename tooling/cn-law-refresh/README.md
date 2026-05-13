# CN law auto-refresh via GitHub Actions

Keep the bundled PRC core statutes current — without needing access to `.cn` domains from your corporate network. GitHub-hosted runners are in the US/EU and can reach `flk.npc.gov.cn` directly.

## How it works

```
flk.npc.gov.cn  ─────►  GitHub Actions runner  ─────►  PR opened
(reachable from         (runs scraper.py once a              │
 US/EU IPs)              week, converts docx→md)             ▼
                                                       Reviewer merges
                                                             │
                                                             ▼
                                                       New plugin version
                                                       (or just git pull)
```

## One-time setup

1. Fork or copy this plugin to your GitHub repo (private is fine — GH Actions runs there too).

2. Move the workflow file into the GitHub-required location:

   ```bash
   mkdir -p .github/workflows/
   cp tooling/cn-law-refresh/workflow.yml .github/workflows/refresh-cn-laws.yml
   git add .github/workflows/refresh-cn-laws.yml
   git commit -m 'chore: add weekly PRC law refresh'
   git push
   ```

3. In GitHub repo settings → Actions → General → "Workflow permissions" → choose **"Read and write permissions"** AND check **"Allow GitHub Actions to create and approve pull requests"**.

4. Go to **Actions** tab → "Refresh PRC core statutes" → **Run workflow** button to test.

## Scheduled cadence

Default: **Monday 03:00 UTC** (Monday 12:00 JST).

To change, edit the `cron` line in `.github/workflows/refresh-cn-laws.yml`. Cron is in UTC.

## What the scraper does

Reads `CORE_LAWS` dict in `scraper.py` (21 laws by default). For each:

1. Query `flk.npc.gov.cn/api/?type=flsearch` with the exact title
2. Find the latest record with status=1 (有效) and type=法律
3. Get detail page to find the WORD download link
4. Download docx from `wb.flk.npc.gov.cn`
5. Convert to Markdown using the same logic as `refresh_cn_corpus.py`
6. Write to `references/cn_laws/{stem}.md`

If any law fails to fetch, the workflow exits with status 1 — but already-fetched laws are written. Failures usually mean a network blip or a title change; check the run log.

## Output

If anything changed, a **pull request** is opened with the diff. Reviewer should:

1. Spot-check 2-3 changed files (especially short ones like 电子签名法 where a sole-clause change is detectable)
2. Look at the publish_date in the new file's header — does it match a known recent amendment?
3. Merge if it looks right.

Once merged, anyone using the plugin can `git pull` (if they cloned) or wait for the next `.plugin` release to get the updates.

## Extending — add new laws

Edit `CORE_LAWS` in `scraper.py`:

```python
CORE_LAWS = {
    # ... existing 21 ...
    "中华人民共和国某新法": "某新法",
    "信息网络传播权保护条例": "信息网络传播权保护条例",  # 行政法规, not 法律 — see note below
}
```

Then update `search_law()` in `scraper.py` if you want non-法律 types (行政法规, 司法解释). The current filter is `status == "1" and type == "法律"` — relax it for other tiers.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| HTTP 403 on flk.npc.gov.cn | Site changed bot detection | Update UA string in scraper.py, or wait for the unofficial API to stabilize |
| Empty docx | Site CDN serving placeholder | Retry the workflow manually; some files are slow to land |
| Wrong title returned | Exact-match search picked wrong revision | Adjust `search_law()` filter or add 法令番号 disambiguation |
| GH Actions blocked from .cn | Rare but possible | Move to self-hosted runner outside corporate firewall |

## Reading the unofficial API (for future maintainers)

The flk.npc.gov.cn frontend uses an undocumented JSON API. github.com/twang2218/law-datasets reverse-engineered it. Key endpoints:

- `GET /api/?type=flsearch&searchType=title;vague&title=X&page=1&size=10&sortTr=f_bbrq_s;desc` — search
- `GET /api/?type=detail&id=Y` — detail page with file links
- Detail response includes `body[]` with `type=WORD`/`HTML`/`PDF` and a `path` (prepend `https://wb.flk.npc.gov.cn`)

The API is unofficial — it may change without notice. If the workflow starts failing, check both:
1. github.com/twang2218/law-datasets for crawler updates
2. flk.npc.gov.cn's frontend Network tab for current API shape

## License consideration

Scraping flk.npc.gov.cn is legally fine — PRC statutes are public-domain government works per 著作权法 第5条第1项. But the site does not formally publish API contracts; respect their rate limits (the scraper sleeps 1 sec between requests).
