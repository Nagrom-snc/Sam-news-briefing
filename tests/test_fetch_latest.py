#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError
from io import BytesIO

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fetcher.fetch_latest import (  # noqa: E402
    canonicalize_url,
    collect_latest,
    load_sources,
    parse_datetime,
    parse_rhg_research,
    parse_rss_or_atom,
    parse_secrss_listing,
    story_key,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class CanonicalizeTests(unittest.TestCase):
    def test_strips_ft_tracking_and_app_host(self) -> None:
        url = "https://app.ft.com/content/abc-123?syn-25a6b1a6=1&utm_source=rss"
        self.assertEqual(canonicalize_url(url), "https://www.ft.com/content/abc-123")

    def test_substack_open_url(self) -> None:
        url = "https://open.substack.com/pub/chinatalk/p/modeltalk-pacing-the-frontier?r=1dklgl&utm_medium=ios"
        self.assertEqual(
            canonicalize_url(url),
            "https://chinatalk.substack.com/p/modeltalk-pacing-the-frontier",
        )

    def test_story_key_ignores_www_and_tracking(self) -> None:
        a = "https://www.scmp.com/tech/article/3367605/deepseek?utm_source=rss_feed"
        b = "https://scmp.com/tech/article/3367605/deepseek/"
        self.assertEqual(story_key(a), story_key(b))


class DatetimeTests(unittest.TestCase):
    def test_rfc822(self) -> None:
        self.assertEqual(
            parse_datetime("Thu, 17 Sep 2026 04:00:31 GMT"),
            "2026-09-17T04:00:31+00:00",
        )

    def test_relative_chinese_hours(self) -> None:
        now = datetime(2026, 9, 17, 10, 0, tzinfo=timezone.utc)
        got = parse_datetime("1小时前", now=now)
        self.assertEqual(got, (now - timedelta(hours=1)).isoformat())


class FeedParseTests(unittest.TestCase):
    def test_rss_items_and_tracking_strip(self) -> None:
        stories = parse_rss_or_atom((FIXTURES / "ft_rss.xml").read_bytes())
        self.assertEqual(len(stories), 2)
        self.assertEqual(
            stories[0]["url"],
            "https://www.ft.com/content/fb8e1037-8c48-49d2-809e-950472bcbae5",
        )
        self.assertIn("China cuts US Treasury", stories[0]["title"])
        self.assertEqual(stories[0]["published"], "2026-09-17T04:00:31+00:00")

    def test_atom(self) -> None:
        stories = parse_rss_or_atom((FIXTURES / "atom.xml").read_bytes())
        self.assertEqual(len(stories), 1)
        self.assertEqual(stories[0]["title"], "ModelTalk: pacing the frontier")
        self.assertTrue(stories[0]["url"].endswith("/p/modeltalk-pacing-the-frontier"))

    def test_secrss_listing(self) -> None:
        html = (FIXTURES / "secrss_list.html").read_text(encoding="utf-8")
        stories = parse_secrss_listing(html, "https://www.secrss.com/articles")
        self.assertEqual(len(stories), 2)
        self.assertEqual(stories[0]["url"], "https://www.secrss.com/articles/94078")
        self.assertIn("油轮", stories[0]["title"])
        self.assertTrue(stories[0]["published"])

    def test_rhg_research_dedupes(self) -> None:
        html = (FIXTURES / "rhg_home.html").read_text(encoding="utf-8")
        stories = parse_rhg_research(html, "https://rhg.com/")
        self.assertEqual(len(stories), 2)
        urls = {item["url"] for item in stories}
        self.assertIn("https://rhg.com/research/the-banks-behind-the-china-shock", urls)


class IsolationTests(unittest.TestCase):
    def test_one_source_failure_does_not_stop_the_rest(self) -> None:
        catalog = {
            "sources": [
                {
                    "id": "OK",
                    "name": "Ok Source",
                    "homepage": "https://example.com",
                    "endpoints": [
                        {"kind": "rss", "label": "feed", "url": "https://ok.example/feed"}
                    ],
                },
                {
                    "id": "BAD",
                    "name": "Bad Source",
                    "homepage": "https://bad.example",
                    "endpoints": [
                        {"kind": "rss", "label": "feed", "url": "https://bad.example/feed"}
                    ],
                },
                {
                    "id": "WEIXIN",
                    "name": "WeChat",
                    "homepage": "https://mp.weixin.qq.com",
                    "notes": "No public RSS or article listing.",
                    "endpoints": [],
                },
            ]
        }
        rss = (FIXTURES / "ft_rss.xml").read_bytes()

        def fake_fetch(url: str, timeout: int) -> tuple[str, bytes, str]:
            if "bad.example" in url:
                raise HTTPError(url, 503, "Unavailable", hdrs=None, fp=BytesIO())
            return url, rss, "application/rss+xml"

        payload = collect_latest(
            catalog, timeout=5, workers=2, max_per_source=5, fetch_fn=fake_fetch
        )
        self.assertGreaterEqual(payload["story_count"], 1)
        self.assertIn("OK", payload["ok_sources"])
        self.assertIn("BAD", payload["failed_sources"])
        self.assertIn("WEIXIN", payload["failed_sources"])
        self.assertTrue(payload["stories"][0]["url"])


class CatalogTests(unittest.TestCase):
    def test_sources_json_covers_intake_hosts(self) -> None:
        catalog = load_sources(ROOT / "fetcher" / "sources.json")
        ids = {src["id"] for src in catalog["sources"]}
        for expected in {
            "FT",
            "SCMP",
            "POLITICO",
            "POLITICO_EU",
            "CNBC",
            "BLOOMBERG",
            "RHG",
            "GAZZETTA",
            "SECRSS",
            "CHINATALK",
            "NETASKARI",
            "MPY",
            "WEIXIN",
        }:
            self.assertIn(expected, ids)
        json.dumps(catalog)


if __name__ == "__main__":
    unittest.main()
