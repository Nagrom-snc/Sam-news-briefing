#!/usr/bin/env python3
"""
Firefox Article Scraper for Sam News Intelligence Agent

Uses your existing Firefox profile (with paywall bypass extensions) to scrape articles.

Usage:
    # Single URL
    python scripts/firefox_scraper.py <url>
    python scripts/firefox_scraper.py "https://www.ft.com/content/..."

    # Batch from file or stdin
    python scripts/firefox_scraper.py --url-list urls.txt
    python scripts/firefox_scraper.py --url-list -   # read URLs from stdin

    # Paywall-heavy: run with visible browser (uses profile cookies)
    python scripts/firefox_scraper.py --no-headless --url-list urls.txt

Output (default):
    Saves to data/raw/YYYY-MM-DD/{ARTICLE_ID}.md in raw format (title, author/date, URL, body).
"""

import sys
import os
import re
import argparse
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from dateutil import parser as date_parser

try:
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("Error: Selenium not installed. Run: pip install selenium")
    sys.exit(1)

try:
    from dateutil import parser as date_parser
except ImportError:
    print("Error: python-dateutil not installed. Run: pip install python-dateutil")
    sys.exit(1)

# Configuration
FIREFOX_PROFILE_PATH = os.path.expanduser(
    "~/Library/Application Support/Firefox/Profiles/f9cigfu0.default-release"
)
PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Outlet detection patterns
OUTLET_PATTERNS = {
    "ft.com": ("Financial Times", "FT"),
    "reuters.com": ("Reuters", "REUTERS"),
    "bloomberg.com": ("Bloomberg", "BLOOM"),
    "economist.com": ("The Economist", "ECON"),
    "wsj.com": ("Wall Street Journal", "WSJ"),
    "scmp.com": ("South China Morning Post", "SCMP"),
    "asia.nikkei.com": ("Nikkei Asia", "NIKKEI"),
    "nikkei.com": ("Nikkei Asia", "NIKKEI"),
    "apnews.com": ("AP News", "AP"),
    "politico.com": ("Politico", "POLITICO"),
    "politico.eu": ("Politico EU", "POLITICO"),
    "techcrunch.com": ("TechCrunch", "TC"),
    "theverge.com": ("The Verge", "VERGE"),
    "nytimes.com": ("The New York Times", "NYT"),
    "telegraph.co.uk": ("The Telegraph", "TELEGRAPH"),
    "economictimes.indiatimes.com": ("Economic Times", "ECT"),
}

# Site-specific selectors for article extraction
SITE_SELECTORS = {
    "ft.com": {
        "title": "h1.article-headline, h1[data-trackable='heading']",
        "author": ".article-author-name, [data-trackable='author']",
        "date": "time[data-trackable='publish-date'], .article-info time",
        "content": ".article-body, [data-component='article-body']",
    },
    "reuters.com": {
        "title": "h1[data-testid='Heading']",
        "author": "[data-testid='AuthorName']",
        "date": "time[data-testid='PublishDate']",
        "content": "[data-testid='ArticleBody']",
    },
    "bloomberg.com": {
        "title": "h1.headline, h1[data-component='headline']",
        "author": ".author-name, [rel='author']",
        "date": "time[data-type='published']",
        "content": ".body-content, article .body",
    },
    "nytimes.com": {
        "title": "h1[data-testid='headline'], h1",
        "author": "[data-testid='byline'], .byline-author",
        "date": "time[datetime], [data-testid='date-published']",
        "content": "section[data-testid='article-body'], article section",
    },
    "telegraph.co.uk": {
        "title": "h1",
        "author": ".author-name, [rel='author']",
        "date": "time[datetime], .date",
        "content": "article .article__body, .article-body, article",
    },
    "default": {
        "title": "h1, .headline, .article-title",
        "author": ".author, .byline, [rel='author']",
        "date": "time, .date, .published",
        "content": "article, .article-body, .story-body, main",
    },
}


def detect_outlet(url: str) -> tuple[str, str]:
    """Detect news outlet from URL."""
    for domain, (name, code) in OUTLET_PATTERNS.items():
        if domain in url:
            return name, code
    return "Unknown", "UNK"


def get_selectors(url: str) -> dict:
    """Get site-specific selectors."""
    for domain, selectors in SITE_SELECTORS.items():
        if domain in url:
            return selectors
    return SITE_SELECTORS["default"]


def get_next_sequence(date_dir: Path, outlet_code: str) -> int:
    """Get next sequence number for this outlet (matches any case, e.g. Reuters or REUTERS)."""
    max_seq = 0
    if date_dir.exists():
        prefix = outlet_code.upper()
        for f in date_dir.iterdir():
            # Match 20260225_REUTERS_001.md or 20260225_Reuters_004.md
            m = re.match(r"(\d{8})_(\w+)_(\d{3})\.md$", f.name, re.IGNORECASE)
            if m and m.group(2).upper() == prefix:
                max_seq = max(max_seq, int(m.group(3)))
    return max_seq + 1


def parse_date_to_iso(date_text: str) -> str:
    """Parse various date formats and return ISO format (YYYY-MM-DD)."""
    if not date_text:
        return datetime.now().strftime("%Y-%m-%d")
    
    # Clean up common prefixes
    date_text = re.sub(r'^(Published|Updated|Posted)\s*', '', date_text, flags=re.IGNORECASE)
    date_text = date_text.strip()
    
    try:
        parsed = date_parser.parse(date_text, fuzzy=True)
        return parsed.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        # If parsing fails, return today's date
        return datetime.now().strftime("%Y-%m-%d")


def create_driver(headless: bool = True) -> webdriver.Firefox:
    """Create Firefox driver with existing profile (with paywall bypass)."""
    options = Options()
    options.profile = FIREFOX_PROFILE_PATH
    if headless:
        options.add_argument("--headless")
    
    print(f"Using Firefox profile: {FIREFOX_PROFILE_PATH}" + (" (headless)" if headless else " (visible)"))
    
    try:
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        print(f"Error creating Firefox driver: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Firefox is installed")
        print("2. Install geckodriver: brew install geckodriver")
        print("3. Close any existing Firefox windows using this profile")
        print("4. For paywalls try: --no-headless")
        sys.exit(1)


def extract_text(driver, selector: str) -> str:
    """Extract text using CSS selector, trying multiple selectors."""
    for sel in selector.split(", "):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, sel.strip())
            if elements:
                return elements[0].text.strip()
        except:
            pass
    return ""


def extract_content(driver, selector: str) -> str:
    """Extract article content, preserving paragraphs."""
    for sel in selector.split(", "):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, sel.strip())
            if elements:
                # Get all paragraph text
                paragraphs = elements[0].find_elements(By.TAG_NAME, "p")
                if paragraphs:
                    return "\n\n".join(p.text.strip() for p in paragraphs if p.text.strip())
                return elements[0].text.strip()
        except:
            pass
    return ""


def scrape_article(url: str, driver=None, headless: bool = True) -> dict:
    """Scrape article from URL using Firefox. If driver is provided, reuse it (caller must quit)."""
    print(f"\nScraping: {url}")
    
    outlet_name, outlet_code = detect_outlet(url)
    selectors = get_selectors(url)
    
    own_driver = driver is None
    if driver is None:
        driver = create_driver(headless=headless)
    
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
        time.sleep(3)
        
        title = extract_text(driver, selectors["title"])
        author = extract_text(driver, selectors["author"])
        date_text_raw = extract_text(driver, selectors["date"])
        content = extract_content(driver, selectors["content"])
        
        date_iso = parse_date_to_iso(date_text_raw)
        if not title:
            title = driver.title.split("|")[0].strip()
        
        return {
            "url": url,
            "outlet_name": outlet_name,
            "outlet_code": outlet_code,
            "title": title,
            "author": author or "Unknown",
            "date": date_iso,
            "date_raw": date_text_raw,
            "content": content,
            "scraped_at": datetime.now().isoformat(),
        }
    finally:
        if own_driver:
            driver.quit()


def _url_to_raw_line(url: str) -> str:
    """Format URL as raw file line: ' www.domain.com /path'."""
    p = urlparse(url)
    netloc = p.netloc or ""
    path = p.path or ""
    if path.startswith("/"):
        path = path[1:]
    return f" {netloc} /{path}" if path else f" {netloc} "


def _date_iso_to_dd_mm_yyyy(iso: str) -> str:
    """Convert YYYY-MM-DD to DD/MM/YYYY for raw header."""
    if not iso or len(iso) < 10:
        return ""
    try:
        parts = iso.split("-")
        if len(parts) == 3:
            return f"{parts[2]}/{parts[1]}/{parts[0]}"
    except Exception:
        pass
    return iso


def save_article(article: dict, output_dir: Path, raw_format: bool = True) -> Path:
    """Save article to markdown file. raw_format=True writes to data/raw style (title, author/date, URL, body)."""
    today = datetime.now().strftime("%Y-%m-%d")
    date_str = datetime.now().strftime("%Y%m%d")
    
    date_dir = output_dir / today
    date_dir.mkdir(parents=True, exist_ok=True)
    
    seq = get_next_sequence(date_dir, article["outlet_code"])
    article_id = f"{date_str}_{article['outlet_code']}_{seq:03d}"
    
    if raw_format:
        author_date = article["author"]
        if article.get("date_raw"):
            author_date += " " + article["date_raw"]
        else:
            author_date += " " + _date_iso_to_dd_mm_yyyy(article["date"])
        md_content = (
            f"{article['title']}\n"
            f"{author_date}\n"
            f"{_url_to_raw_line(article['url'])}\n\n"
            f"{article['content'] or '(No content extracted - try --no-headless)'}\n"
        )
    else:
        import hashlib
        content_hash = hashlib.md5(article["content"].encode()).hexdigest()[:16]
        word_count = len(article["content"].split())
        md_content = f"""---
id: "{article_id}"
source: "{article['outlet_name']}"
title: "{article['title']}"
url: "{article['url']}"
date: "{article['date']}"
author: "{article['author']}"
content_hash: "{content_hash}"
word_count: {word_count}
processed_at: {article['scraped_at']}
---

# {article['title']}

**Article ID:** {article_id}  
**Source:** {article['outlet_name']}  
**URL:** {article['url']}  
**Date:** {article['date']}  
**Author:** {article['author']}

---

{article['content']}

---

*Scraped: {article['scraped_at']}*
"""
    
    output_path = date_dir / f"{article_id}.md"
    output_path.write_text(md_content)
    
    word_count = len((article["content"] or "").split())
    title_preview = article['title'][:60] + "..." if len(article['title']) > 60 else article['title']
    print(f"\n✓ Saved: {output_path}")
    print(f"  Article ID: {article_id}")
    print(f"  Title: {title_preview}")
    print(f"  Words: {word_count}")
    
    return output_path


def load_urls(url_list_arg) -> list[str]:
    """Load URLs from file path or stdin (-)."""
    urls = []
    if url_list_arg == "-":
        for line in sys.stdin:
            line = line.strip()
            if line and not line.startswith("#") and line.startswith("http"):
                urls.append(line)
    else:
        path = Path(url_list_arg)
        if not path.exists():
            print(f"Error: File not found: {path}")
            sys.exit(1)
        for line in path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and line.startswith("http"):
                urls.append(line)
    return urls


def main():
    parser = argparse.ArgumentParser(
        description="Scrape articles with Firefox (paywall bypass via profile). Saves to data/raw by default."
    )
    parser.add_argument("url", nargs="?", help="Single article URL")
    parser.add_argument(
        "--url-list",
        metavar="FILE",
        help="Batch: file of URLs (one per line) or '-' for stdin",
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Show browser window (recommended for paywalled sites; uses profile cookies)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_RAW_DIR,
        help=f"Output directory (default: data/raw)",
    )
    parser.add_argument(
        "--processed",
        action="store_true",
        help="Save to data/processed with YAML frontmatter instead of raw format",
    )
    args = parser.parse_args()
    
    if args.url_list:
        urls = load_urls(args.url_list)
        if not urls:
            print("No valid URLs found.")
            sys.exit(1)
        print(f"Batch mode: {len(urls)} URL(s). Output: {args.output_dir}")
        if args.processed:
            args.output_dir = PROJECT_ROOT / "data" / "processed"
        raw_format = not args.processed
        
        driver = create_driver(headless=not args.no_headless)
        saved = []
        try:
            for i, url in enumerate(urls):
                try:
                    article = scrape_article(url, driver=driver, headless=not args.no_headless)
                    if not article["content"]:
                        print(f"  ⚠ No content: {url[:60]}...")
                    path = save_article(article, args.output_dir, raw_format=raw_format)
                    saved.append(path)
                except Exception as e:
                    print(f"  ✗ Failed: {url[:60]}... — {e}")
            print(f"\n✓ Done. Saved {len(saved)}/{len(urls)} to {args.output_dir}")
        finally:
            driver.quit()
        return
    
    if not args.url:
        parser.print_help()
        print("\nExample: python firefox_scraper.py 'https://www.ft.com/content/...'")
        print("         python firefox_scraper.py --url-list urls.txt --no-headless")
        sys.exit(1)
    
    url = args.url
    if not url.startswith("http"):
        print(f"Error: Invalid URL: {url}")
        sys.exit(1)
    
    raw_format = not args.processed
    if args.processed:
        args.output_dir = PROJECT_ROOT / "data" / "processed"
    
    article = scrape_article(url, headless=not args.no_headless)
    if not article["content"]:
        print("\n⚠ Warning: No content extracted. Try --no-headless for paywalled sites.")
    
    output_path = save_article(article, args.output_dir, raw_format=raw_format)
    print(f"\n✓ Next: Run Sam news on {output_path.parent.name}/")


if __name__ == "__main__":
    main()
