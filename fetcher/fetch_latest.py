#!/usr/bin/env python3
"""Fetch latest headlines from Sam News sources and write a briefing intake payload.

Uses only the Python standard library. One source failing does not stop the rest.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCES = HERE / "sources.json"
DEFAULT_JSON_OUT = HERE.parent / "data" / "latest" / "latest.json"
DEFAULT_LIST_OUT = HERE.parent / "data" / "latest" / "latest_urls.txt"
USER_AGENT = (
    "Mozilla/5.0 (compatible; SamNewsBriefing/1.0; "
    "+https://github.com/nagrom-snc/sam-news-briefing) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
TRACKING_QUERY_KEYS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "utm_id",
    "syn-25a6b1a6",
    "module",
    "pgtype",
    "srnd",
    "r",
    "hide_intro_popup",
}
DROP_QUERY_PREFIXES = ("utm_", "syn-")
TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")
SECRSS_ITEM_RE = re.compile(r'<li class="list-item">(.*?)</li>', re.S | re.I)
SECRSS_HREF_RE = re.compile(
    r'<h2 class="title">\s*<a[^>]+href="([^"]+)"[^>]*>\s*(.*?)\s*</a>',
    re.S | re.I,
)
SECRSS_TIME_RE = re.compile(r'<span class="time">([^<]+)</span>', re.I)
SECRSS_AUTHOR_RE = re.compile(
    r'<span class="author">.*?<a[^>]*>([^<]+)</a>', re.S | re.I
)
SECRSS_INTRO_RE = re.compile(
    r'<p class="intro[^"]*">\s*<a[^>]*>\s*(.*?)\s*</a>', re.S | re.I
)
RELATIVE_TIME_PATTERNS = (
    (re.compile(r"^刚刚$|^just now$", re.I), lambda _m: timedelta(0)),
    (re.compile(r"^(\d+)\s*秒前$"), lambda m: timedelta(seconds=int(m.group(1)))),
    (re.compile(r"^(\d+)\s*分钟前$"), lambda m: timedelta(minutes=int(m.group(1)))),
    (re.compile(r"^(\d+)\s*小時前$|^(\d+)\s*小时前$"), lambda m: timedelta(hours=int(m.group(1) or m.group(2)))),
    (re.compile(r"^(\d+)\s*天前$"), lambda m: timedelta(days=int(m.group(1)))),
    (re.compile(r"^昨天$"), lambda _m: timedelta(days=1)),
    (re.compile(r"^(\d+)\s*hours?\s+ago$", re.I), lambda m: timedelta(hours=int(m.group(1)))),
    (re.compile(r"^(\d+)\s*minutes?\s+ago$", re.I), lambda m: timedelta(minutes=int(m.group(1)))),
    (re.compile(r"^(\d+)\s*days?\s+ago$", re.I), lambda m: timedelta(days=int(m.group(1)))),
)
FetchFn = Callable[[str, int], tuple[str, bytes, str]]


class Story(dict):
    """JSON-serializable story record."""


def local_tag(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def strip_html(text: str | None) -> str:
    if not text:
        return ""
    text = unescape(TAG_RE.sub(" ", text))
    return WHITESPACE_RE.sub(" ", text).strip()


def canonicalize_url(url: str) -> str:
    if not url:
        return ""
    url = unescape(url.strip())
    parsed = urlparse(url)
    scheme = parsed.scheme or "https"
    host = parsed.netloc.lower()
    path = parsed.path or "/"

    if host in {"app.ft.com", "www.ft.com"}:
        host = "www.ft.com"
    if host == "open.substack.com":
        match = re.match(r"^/pub/([^/]+)/p/([^/?#]+)", path)
        if match:
            host = f"{match.group(1)}.substack.com"
            path = f"/p/{match.group(2)}"

    kept: list[tuple[str, str]] = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered in TRACKING_QUERY_KEYS:
            continue
        if any(lowered.startswith(prefix) for prefix in DROP_QUERY_PREFIXES):
            continue
        kept.append((key, value))
    query = urlencode(kept)
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return urlunparse((scheme, host, path, "", query, ""))


def story_key(url: str) -> str:
    parsed = urlparse(canonicalize_url(url))
    host = parsed.netloc[4:] if parsed.netloc.startswith("www.") else parsed.netloc
    return f"{host}{parsed.path}".lower()


def parse_datetime(value: str | None, now: datetime | None = None) -> str | None:
    if not value:
        return None
    raw = unescape(value).strip()
    if not raw:
        return None
    now = now or datetime.now(timezone.utc)
    for pattern, delta_fn in RELATIVE_TIME_PATTERNS:
        match = pattern.match(raw)
        if match:
            return (now - delta_fn(match)).replace(microsecond=0).isoformat()
    try:
        parsed = parsedate_to_datetime(raw)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).replace(microsecond=0).isoformat()
    except (TypeError, ValueError, OverflowError):
        pass
    iso = raw.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(iso)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).replace(microsecond=0).isoformat()
    except ValueError:
        return None


def first_child_text(node: ET.Element, names: Iterable[str]) -> str:
    wanted = set(names)
    for child in node:
        if local_tag(child.tag) in wanted:
            href = child.attrib.get("href") or child.attrib.get("url")
            if href and local_tag(child.tag) == "link" and not (child.text or "").strip():
                return href.strip()
            text = "".join(child.itertext()).strip()
            if text:
                return text
            if href:
                return href.strip()
    return ""


def parse_rss_or_atom(payload: bytes | str) -> list[dict[str, str]]:
    text = payload.decode("utf-8", "replace") if isinstance(payload, bytes) else payload
    text = text.lstrip("\ufeff")
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return []
    stories: list[dict[str, str]] = []
    root_name = local_tag(root.tag)
    if root_name == "feed":
        nodes = [el for el in root.iter() if local_tag(el.tag) == "entry"]
        for entry in nodes:
            title = first_child_text(entry, {"title"})
            link = ""
            for child in entry:
                if local_tag(child.tag) == "link":
                    rel = child.attrib.get("rel", "alternate")
                    href = child.attrib.get("href", "")
                    if href and rel in {"alternate", ""}:
                        link = href
                        break
            if not link:
                link = first_child_text(entry, {"link", "id"})
            stories.append(
                {
                    "title": strip_html(title),
                    "url": canonicalize_url(link),
                    "published": parse_datetime(
                        first_child_text(entry, {"published", "updated", "date"})
                    )
                    or "",
                    "author": strip_html(first_child_text(entry, {"author", "name", "creator"})),
                    "summary": strip_html(first_child_text(entry, {"summary", "content"}))[:400],
                }
            )
        return [s for s in stories if s["title"] and s["url"]]

    items = [el for el in root.iter() if local_tag(el.tag) == "item"]
    for item in items:
        title = first_child_text(item, {"title"})
        link = first_child_text(item, {"link"})
        if not link:
            link = first_child_text(item, {"guid"})
        stories.append(
            {
                "title": strip_html(title),
                "url": canonicalize_url(link),
                "published": parse_datetime(
                    first_child_text(item, {"pubDate", "date", "published", "updated"})
                )
                or "",
                "author": strip_html(first_child_text(item, {"creator", "author"})),
                "summary": strip_html(first_child_text(item, {"description", "encoded", "summary"}))[
                    :400
                ],
            }
        )
    return [s for s in stories if s["title"] and s["url"]]


def parse_secrss_listing(html: str, base_url: str) -> list[dict[str, str]]:
    stories: list[dict[str, str]] = []
    for block in SECRSS_ITEM_RE.findall(html):
        href_match = SECRSS_HREF_RE.search(block)
        if not href_match:
            continue
        href = urljoin(base_url, href_match.group(1).strip())
        if "/articles/" not in href or "?" in href:
            continue
        time_match = SECRSS_TIME_RE.search(block)
        author_match = SECRSS_AUTHOR_RE.search(block)
        intro_match = SECRSS_INTRO_RE.search(block)
        stories.append(
            {
                "title": strip_html(href_match.group(2)),
                "url": canonicalize_url(href),
                "published": parse_datetime(time_match.group(1) if time_match else "") or "",
                "author": strip_html(author_match.group(1) if author_match else ""),
                "summary": strip_html(intro_match.group(1) if intro_match else "")[:400],
            }
        )
    return [s for s in stories if s["title"] and s["url"]]


class _AnchorCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self._href = href
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href is not None:
            self.anchors.append((self._href, "".join(self._text)))
            self._href = None
            self._text = []


def parse_rhg_research(html: str, base_url: str) -> list[dict[str, str]] :
    parser = _AnchorCollector()
    try:
        parser.feed(html)
    except Exception:
        return []
    seen: set[str] = set()
    stories: list[dict[str, str]] = []
    for href, text in parser.anchors:
        abs_url = urljoin(base_url, href.strip())
        parsed = urlparse(abs_url)
        if parsed.netloc.lower() not in {"rhg.com", "www.rhg.com"}:
            continue
        path = parsed.path.rstrip("/")
        parts = [p for p in path.split("/") if p]
        if len(parts) != 2 or parts[0] != "research":
            continue
        title = strip_html(text)
        if len(title) < 8:
            continue
        key = story_key(abs_url)
        if key in seen:
            continue
        seen.add(key)
        stories.append(
            {
                "title": title,
                "url": canonicalize_url(abs_url),
                "published": "",
                "author": "",
                "summary": "",
            }
        )
    return stories


HTML_PARSERS = {
    "secrss_listing": parse_secrss_listing,
    "rhg_research": parse_rhg_research,
}


def default_fetch(url: str, timeout: int) -> tuple[str, bytes, str]:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, text/html;q=0.9, */*;q=0.5",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        return response.geturl(), response.read(), content_type


def fetch_endpoint(
    source: dict[str, Any],
    endpoint: dict[str, Any],
    timeout: int,
    fetch_fn: FetchFn,
) -> tuple[list[dict[str, str]], dict[str, Any] | None]:
    url = endpoint["url"]
    try:
        final_url, body, _content_type = fetch_fn(url, timeout)
    except HTTPError as exc:
        return [], {"url": url, "error": f"HTTP {exc.code} {exc.reason}"}
    except URLError as exc:
        return [], {"url": url, "error": f"URL error: {exc.reason}"}
    except TimeoutError:
        return [], {"url": url, "error": f"timed out after {timeout}s"}
    except Exception as exc:  # noqa: BLE001 — isolate source failures
        return [], {"url": url, "error": f"{type(exc).__name__}: {exc}"}

    kind = endpoint.get("kind", "rss")
    parser_name = endpoint.get("parser")
    try:
        if kind == "html_listing":
            parser = HTML_PARSERS.get(parser_name)
            if parser is None:
                return [], {"url": url, "error": f"unknown HTML parser {parser_name!r}"}
            stories = parser(body.decode("utf-8", "replace"), final_url)
        elif kind == "rss":
            stories = parse_rss_or_atom(body)
            if not stories and b"<html" in body[:400].lower():
                return [], {"url": url, "error": "expected RSS/Atom, got an HTML page"}
        else:
            return [], {"url": url, "error": f"unknown endpoint kind {kind!r}"}
    except Exception as exc:  # noqa: BLE001
        return [], {"url": url, "error": f"parse error: {type(exc).__name__}: {exc}"}

    for story in stories:
        story["source_id"] = source["id"]
        story["source_name"] = source["name"]
        story["endpoint"] = endpoint.get("label", "")
    return stories, None


def fetch_source(
    source: dict[str, Any],
    timeout: int,
    fetch_fn: FetchFn,
    max_per_source: int,
) -> dict[str, Any]:
    endpoints = source.get("endpoints") or []
    if not endpoints:
        return {
            "id": source["id"],
            "ok": False,
            "stories": [],
            "errors": [
                {
                    "url": source.get("homepage", ""),
                    "error": source.get("notes") or "no public listing or feed",
                }
            ],
        }

    stories: list[dict[str, str]] = []
    errors: list[dict[str, Any]] = []
    for endpoint in endpoints:
        batch, error = fetch_endpoint(source, endpoint, timeout, fetch_fn)
        if error:
            errors.append(error)
        stories.extend(batch)

    deduped: list[dict[str, str]] = []
    seen: set[str] = set()
    for story in stories:
        key = story_key(story["url"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(story)

    def sort_key(item: dict[str, str]) -> tuple[int, str]:
        published = item.get("published") or ""
        return (0 if published else 1, published)

    deduped.sort(key=sort_key, reverse=True)
    if max_per_source > 0:
        deduped = deduped[:max_per_source]
    return {
        "id": source["id"],
        "ok": bool(deduped),
        "stories": deduped,
        "errors": errors,
    }


def load_sources(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def collect_latest(
    catalog: dict[str, Any],
    *,
    timeout: int = 20,
    workers: int = 8,
    max_per_source: int = 12,
    only: set[str] | None = None,
    fetch_fn: FetchFn = default_fetch,
) -> dict[str, Any]:
    sources = catalog["sources"]
    if only:
        wanted = {item.upper() for item in only}
        sources = [src for src in sources if src["id"].upper() in wanted]
        missing = wanted - {src["id"].upper() for src in sources}
        if missing:
            raise SystemExit(f"unknown source id(s): {', '.join(sorted(missing))}")

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {
            pool.submit(fetch_source, source, timeout, fetch_fn, max_per_source): source["id"]
            for source in sources
        }
        for future in as_completed(futures):
            source_id = futures[future]
            try:
                results.append(future.result())
            except Exception as exc:  # noqa: BLE001
                results.append(
                    {
                        "id": source_id,
                        "ok": False,
                        "stories": [],
                        "errors": [{"url": "", "error": f"{type(exc).__name__}: {exc}"}],
                    }
                )

    order = {src["id"]: index for index, src in enumerate(sources)}
    results.sort(key=lambda item: order.get(item["id"], 999))

    stories: list[dict[str, str]] = []
    seen: set[str] = set()
    for result in results:
        for story in result["stories"]:
            key = story_key(story["url"])
            if key in seen:
                continue
            seen.add(key)
            stories.append(story)

    stories.sort(
        key=lambda item: (0 if item.get("published") else 1, item.get("published") or ""),
        reverse=True,
    )
    failures = [
        {
            "source_id": result["id"],
            "errors": result["errors"],
        }
        for result in results
        if not result["ok"]
    ]
    warnings = [
        {
            "source_id": result["id"],
            "errors": result["errors"],
        }
        for result in results
        if result["ok"] and result["errors"]
    ]
    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_count": len(sources),
        "ok_sources": [result["id"] for result in results if result["ok"]],
        "failed_sources": [result["id"] for result in results if not result["ok"]],
        "story_count": len(stories),
        "stories": stories,
        "failures": failures,
        "warnings": warnings,
    }


def write_outputs(payload: dict[str, Any], json_out: Path, list_out: Path) -> None:
    json_out.parent.mkdir(parents=True, exist_ok=True)
    list_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    date_stamp = payload["generated_at"][:10]
    lines = [f"# Sam intake {date_stamp} (auto-fetched latest news)", ""]
    for story in payload["stories"]:
        lines.append(story["url"])
    list_out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch latest headlines/links/timestamps from Sam News sources."
    )
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES, help="Source catalog JSON")
    parser.add_argument("--out", type=Path, default=DEFAULT_JSON_OUT, help="JSON output path")
    parser.add_argument(
        "--list-out",
        type=Path,
        default=DEFAULT_LIST_OUT,
        help="URL-list output path (same shape as YYMMDD_list.txt)",
    )
    parser.add_argument("--max-per-source", type=int, default=12)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--source",
        action="append",
        dest="only",
        help="Limit to one source id (repeatable), e.g. --source SCMP --source FT",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Also print the JSON payload to stdout",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    catalog = load_sources(args.sources)
    payload = collect_latest(
        catalog,
        timeout=args.timeout,
        workers=args.workers,
        max_per_source=args.max_per_source,
        only=set(args.only) if args.only else None,
    )
    write_outputs(payload, args.out, args.list_out)
    summary = (
        f"fetched {payload['story_count']} stories from "
        f"{len(payload['ok_sources'])}/{payload['source_count']} sources; "
        f"wrote {args.out} and {args.list_out}"
    )
    if payload["failed_sources"]:
        summary += f"; failed: {', '.join(payload['failed_sources'])}"
    print(summary, file=sys.stderr)
    if args.stdout:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    return 0 if payload["story_count"] else 1


if __name__ == "__main__":
    sys.exit(main())
