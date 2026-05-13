# CN law auto-refresh via GitHub Actions

Keep the bundled PRC core statutes current — without needing access to `.cn` domains from your corporate network.

## How it works

```
LawRefBook/Laws  ─────►  GitHub Actions runner  ─────►  PR opened
(GitHub corpus,         (runs scraper.py once a              │
 maintained by           week, git clones + picks            ▼
 community,              the latest-dated version       Reviewer merges
 handles flk.npc          of each core law)                   │
 dirty work for                                               ▼
 us)                                                    `git pull`
```

`scraper.py` does a `git clone --depth 1` of [LawRefBook/Laws](https://github.com/LawRefBook/Laws), then for each law in `LRB_SOURCED_LAWS` it picks the file matching `{stem}(YYYY-MM-DD).md` with the largest date and copies it into `references/cn_laws/{stem}.md`. Pure stdlib — no `requests`, no `playwright`.

## Why not scrape flk.npc.gov.cn directly?

`flk.npc.gov.cn` rebuilt as a SPA in 2026. The unofficial JSON API documented by [twang2218/law-datasets](https://github.com/twang2218/law-datasets) (the `?type=flsearch` / `?type=detail` endpoints) no longer exists — `/api/?type=flsearch` is now caught by the SPA's frontend router and returns the index.html shell. LawRefBook handles the new API for us; we just consume their curated output.

## Owner-maintained laws (scraper does not touch these)

| File | Why owner-maintained |
|---|---|
| `民法典.md` | Owner has authoritative .docx (1260 articles); use `refresh_cn_corpus.py` |
| `反不正当竞争法.md` | 2025-06-27 第二次修订; LawRefBook stuck at 2019-04-23 |
| `网络安全法.md` | 2025-10-28 修正; LawRefBook stuck at 2016-11-07 |
| `仲裁法.md` | 2025-09-12 修订; LawRefBook stuck at 2017-09-01 |

Move a name out of `OWNER_MAINTAINED_LAWS` in `scraper.py` once LawRefBook catches up (and you've verified their version matches the latest amendment).

## One-time setup

1. Fork or copy this plugin to your GitHub repo (private is fine).

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

Edit the `cron` line in `.github/workflows/refresh-cn-laws.yml` to change. Cron is in UTC.

## Output

If anything changed, a **pull request** is opened with the diff. Reviewer should:

1. Spot-check a few changed files — does the version header in the new file match a known recent amendment in LawRefBook's commits?
2. If a law you care about appears in the diff and a 2025+ amendment exists upstream of LawRefBook (but they haven't picked it up), move that law into `OWNER_MAINTAINED_LAWS` and `refresh_cn_corpus.py` from the authoritative .docx instead.
3. Merge if it looks right.

## Format note — LawRefBook vs owner-curated

LawRefBook outputs flat markdown:

```
# 中华人民共和国某法

(amendment lines, blank-separated)

<!-- INFO END -->

第一条 ...内容...

第二条 ...
```

`refresh_cn_corpus.py` (owner-curated for 民法典 etc.) outputs richer markdown:

```
# 中华人民共和国某法

(amendment lines, parenthesized)
目　　录

## 第一章　总则
### 第一节　...
#### 第一条
...内容...
```

Both work with `cn-law-lookup` (which hands the full file to Claude rather than navigating headings). The richer format is nicer to read but is regenerated every time `refresh_cn_corpus.py` runs.

## Extending — adding a new core law

Edit `LRB_SOURCED_LAWS` in `scraper.py`:

```python
LRB_SOURCED_LAWS = [
    # ... existing ...
    "新加的法名",  # bare title, no 中华人民共和国 prefix, no extension
]
```

The scraper will search the standard top-level dirs in LawRefBook (民法商法, 经济法, 行政法, 社会法, 刑法, 诉讼与非诉讼程序法, 宪法, 宪法相关法, 司法解释, 行政法规, 部门规章, 其他). If LawRefBook doesn't have the law, the run fails with `not found in LawRefBook`. Either wait for upstream to add it, or add the law to `OWNER_MAINTAINED_LAWS` and refresh from .docx locally.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `git clone failed` | GitHub rate limit / outage | Re-run; usually transient |
| `not found in LawRefBook` for a law you expect | LawRefBook doesn't have it under the searched dirs, or filename pattern differs | Verify on github.com/LawRefBook/Laws; widen SEARCH_DIRS if needed |
| LawRefBook's latest is older than a known amendment | LawRefBook lags upstream (their own scraper has the same flk problem we hit) | Move that law to OWNER_MAINTAINED_LAWS, use refresh_cn_corpus.py |
| Workflow opens PR but content is identical (whitespace-only diff) | LawRefBook formatting drift | Merge anyway, or close PR |

## Attribution

Statute corpus sourced from [LawRefBook/Laws](https://github.com/LawRefBook/Laws). PRC statutes are public-domain government works per 著作权法 第5条第1项; LawRefBook's curation (organization, naming, formatting) is their work — at the time of writing they have no declared license, so this consumption is on a best-effort attribution basis.
