# Sam News Briefing

Public archive of daily China- and AI-related briefings (`briefings/`, GitHub Pages via `index.md`). Intake still arrives as dated URL lists (`YYMMDD_list.txt`); this repo now also has a **latest-news fetcher** that polls those publishers instead of waiting for a pasted list.

## Latest-news fetcher

`fetcher/fetch_latest.py` pulls current headlines, links, and timestamps from the outlets in `260917_list.txt` (17 Sep 2026 intake). It writes:

- `data/latest/latest.json` — stories plus per-source failures
- `data/latest/latest_urls.txt` — same URL-list shape as existing `YYMMDD_list.txt` files, ready to drop into the briefing pipeline

Python 3.10+ only. No pip packages.

```bash
python3 fetcher/fetch_latest.py
```

Useful flags:

```bash
# Inspect JSON on stdout as well as writing the default files
python3 fetcher/fetch_latest.py --stdout

# Fewer stories / tighter timeouts
python3 fetcher/fetch_latest.py --max-per-source 8 --timeout 15 --workers 6

# One or two publishers
python3 fetcher/fetch_latest.py --source SCMP --source FT

# Keyword search + filter (China/AI terms from the 17 Sep intake)
python3 fetcher/fetch_latest.py --keywords

# Ad-hoc terms: search publisher search pages where they exist, else filter feeds
python3 fetcher/fetch_latest.py --keyword DeepSeek --keyword Huawei

# Custom output (JSON + intake list)
python3 fetcher/fetch_latest.py \
  --out data/latest/2026-09-17.json \
  --list-out 260917_auto_list.txt
```

A source that 403s, times out, or has no public feed is recorded under `failures` / `warnings` and the run continues. WeChat (`mp.weixin.qq.com`) has no public listing, so it is always reported as failed and skipped.

### How the sources were mapped

Article URLs in `260917_list.txt` were grouped by publisher, then each publisher’s live feed or listing page was probed:

| Source | Intake pattern | Latest-news endpoint |
| --- | --- | --- |
| Financial Times | `/content/{uuid}` (`www` and `app`) | `/?format=rss` → `/rss/home/international`; section feeds `/{section}?format=rss` (china, AI, technology, world) |
| SCMP | `/{desk}/article/{id}/{slug}` | Official RSS, e.g. `/rss/36/feed` (tech), `/rss/4/feed` (China), `/rss/2/feed` (Hong Kong) |
| POLITICO US | `/news/YYYY/MM/DD/{slug}` | `https://rss.politico.com/politics-news.xml`, `technology.xml` |
| POLITICO Europe | `/article/…`, `/newsletter/…` | `/feed/`, `/section/technology/feed/`, `/tag/artificial-intelligence/feed/`, `/newsletter/feed/` |
| CNBC | `/YYYY/MM/DD/{slug}.html` | `/id/{channel}/device/rss/rss.html` (top, world, Asia, technology) |
| Bloomberg | `/news/articles/{date}/{slug}` | `/feeds/{desk}/news.rss` (technology, markets, politics, economics) |
| Rhodium Group | `/research/{slug}/` | Homepage + `/china/` listing links; WordPress `/feed/` for news posts |
| Gazzetta | `gazzetta.xyz/{slug}/` | `/rss/` |
| 安全内参 | `/articles/{id}` | HTML list at `/articles` (no RSS) |
| ChinaTalk / Netaskari | `open.substack.com/pub/{pub}/p/{slug}` | `{pub}.substack.com/feed` |
| Mark Parker Young | `/posts/{slug}` | Site RSS is often 403; Substack mirror `markparkeryoung.substack.com/feed` |
| WeChat | `mp.weixin.qq.com/s/…` | No public feed — skipped with an error |

Edit `fetcher/sources.json` to add or disable endpoints. Tracking query params (`utm_*`, `syn-*`, `module`, `pgtype`, …) are stripped so the intake list is stable.

### Keyword fetch

`--keywords` (or `--keyword TERM`) does two things:

1. **Search** native publisher endpoints that accept a query (POLITICO Europe `/search/{query}/feed/`, Rhodium `/?s={query}&feed=rss2`, 安全内参 `/search?keywords=`).
2. **Filter** every source’s RSS/listing hits so only headlines/summaries/URLs matching the terms are kept (word-boundary match; Chinese terms are substring). Default terms live in `fetcher/keywords.json`.

FT, SCMP, CNBC, Bloomberg, and POLITICO US do not expose a public keyword RSS we can poll, so those sources contribute matching stories from their latest section feeds. WeChat still has no public listing.

### Tests

```bash
python3 -m unittest discover -s tests -v
```

### Output JSON (shape)

```json
{
  "generated_at": "2026-09-17T10:30:00+00:00",
  "story_count": 80,
  "ok_sources": ["FT", "SCMP"],
  "failed_sources": ["WEIXIN"],
  "stories": [
    {
      "source_id": "SCMP",
      "source_name": "South China Morning Post",
      "title": "…",
      "url": "https://www.scmp.com/tech/article/…",
      "published": "2026-09-17T08:00:00+00:00",
      "author": "…",
      "summary": "…",
      "endpoint": "tech"
    }
  ],
  "failures": [{"source_id": "WEIXIN", "errors": [{"url": "…", "error": "…"}]}]
}
```

Use `latest_urls.txt` (or a renamed `YYMMDD_list.txt`) as the next briefing intake the same way as `260822_list.txt`.
