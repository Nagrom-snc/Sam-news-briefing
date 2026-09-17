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
    expand_endpoints,
    interpolate_url,
    load_sources,
    parse_datetime,
    parse_rhg_research,
    parse_rss_or_atom,
    parse_secrss_listing,
    story_key,
    story_matches,
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


class KeywordTests(unittest.TestCase):
    def test_word_boundary_does_not_match_air(self) -> None:
        story = {"title": "Hot air balloon over Thailand", "summary": "", "url": "", "author": ""}
        self.assertFalse(story_matches(story, ["AI"]))
        self.assertTrue(story_matches({"title": "China AI chips", "summary": "", "url": "", "author": ""}, ["AI"]))

    def test_chinese_substring(self) -> None:
        story = {"title": "浅析美国空军人工智能训练战略", "summary": "", "url": "", "author": ""}
        self.assertTrue(story_matches(story, ["人工智能"]))

    def test_match_all_requires_every_term(self) -> None:
        story = {"title": "China tariff talks", "summary": "", "url": "", "author": ""}
        self.assertTrue(story_matches(story, ["China", "AI"], mode="any"))
        self.assertFalse(story_matches(story, ["China", "AI"], mode="all"))

    def test_search_url_interpolation(self) -> None:
        self.assertEqual(
            interpolate_url("https://www.politico.eu/search/{query}/feed/", "Hong Kong"),
            "https://www.politico.eu/search/Hong%20Kong/feed/",
        )

    def test_expand_search_endpoints(self) -> None:
        source = {
            "endpoints": [{"kind": "rss", "label": "home", "url": "https://rhg.com/feed/"}],
            "search_endpoints": [
                {"kind": "rss", "label": "search", "url": "https://rhg.com/?s={query}&feed=rss2"}
            ],
        }
        expanded = expand_endpoints(source, ["China", "AI"])
        self.assertEqual(len(expanded), 3)
        self.assertTrue(any("s=China" in item["url"] for item in expanded))

    def test_keyword_filter_keeps_matching_feed_items(self) -> None:
        catalog = {
            "sources": [
                {
                    "id": "FT",
                    "name": "Financial Times",
                    "homepage": "https://www.ft.com",
                    "endpoints": [{"kind": "rss", "label": "home", "url": "https://ok.example/feed"}],
                }
            ]
        }
        rss = (FIXTURES / "ft_rss.xml").read_bytes()

        def fake_fetch(url: str, timeout: int) -> tuple[str, bytes, str]:
            return url, rss, "application/rss+xml"

        payload = collect_latest(
            catalog,
            timeout=5,
            workers=1,
            max_per_source=5,
            fetch_fn=fake_fetch,
            keywords=["China"],
        )
        self.assertEqual(payload["story_count"], 1)
        self.assertIn("China", payload["stories"][0]["title"])
        self.assertIn("China", payload["stories"][0]["matched_keywords"])

        empty = collect_latest(
            catalog,
            timeout=5,
            workers=1,
            max_per_source=5,
            fetch_fn=fake_fetch,
            keywords=["DeepSeek"],
        )
        self.assertEqual(empty["story_count"], 0)
        self.assertIn("FT", empty["ok_sources"])


class SortTests(unittest.TestCase):
    def test_undated_stories_sort_last(self) -> None:
        from fetcher.fetch_latest import story_sort_tuple

        items = [
            {"title": "old", "published": "2026-09-16T00:00:00+00:00", "url": "https://a/1"},
            {"title": "undated", "published": "", "url": "https://a/2"},
            {"title": "new", "published": "2026-09-17T00:00:00+00:00", "url": "https://a/3"},
        ]
        items.sort(key=story_sort_tuple, reverse=True)
        self.assertEqual([item["title"] for item in items], ["new", "old", "undated"])


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
