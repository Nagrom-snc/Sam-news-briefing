#!/bin/bash
# Sam News Scraper - Firefox Article Scraper (paywall bypass via profile)
# Usage:
#   ./scripts/scrape.sh <url>                    # single URL → data/raw/YYYY-MM-DD/
#   ./scripts/scrape.sh --url-list urls.txt      # batch from file
#   ./scripts/scrape.sh --url-list -             # batch from stdin
#   ./scripts/scrape.sh --no-headless --url-list urls.txt   # visible browser (paywalls)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SAM_NEWS_VENV:-$HOME/.sam_news_venv}"

if [ -d "$VENV_DIR/bin" ]; then
  source "$VENV_DIR/bin/activate"
fi

python "$SCRIPT_DIR/firefox_scraper.py" "$@"
