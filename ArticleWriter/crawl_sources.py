#!/usr/bin/env python3
"""
ArticleWriter - crawl sources into Markdown files.

Usage:
  python ArticleWriter/crawl_sources.py ArticleWriter/1_Arxio_NewOutlook.config
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, Optional

import json5

from model.firecrawl_source_crawler import FirecrawlSourceCrawler


def _sanitize_filename_component(value: str, max_len: int = 120) -> str:
    """
    Make a readable, filesystem-safe filename component.
    """
    value = (value or "").strip()
    value = re.sub(r"\s+", " ", value).strip()
    # Replace forbidden characters on Windows/macOS/Linux
    value = re.sub(r'[\/\\:\*\?"<>\|]+', "-", value)
    value = value.strip(" .-_")
    if not value:
        return "untitled"
    if len(value) > max_len:
        value = value[:max_len].rstrip(" .-_")
    return value or "untitled"


def _first_matching_file(output_dir: Path, prefix: str) -> Optional[Path]:
    """
    Return an existing file that indicates the prefix has already been crawled.
    """
    for p in output_dir.glob(f"{prefix}_*.md"):
        return p
    return None


def _iter_source_lines(sources_file: Path) -> Iterable[tuple[int, str]]:
    """
    Yield (line_no, url) for each non-empty line (line numbers are 1-based).
    """
    lines = sources_file.read_text(encoding="utf-8").splitlines()
    for i, raw in enumerate(lines, start=1):
        url = (raw or "").strip()
        if not url:
            continue
        if url.startswith("#") or url.startswith("//"):
            continue
        yield i, url


def load_config(config_path: Path) -> dict:
    try:
        with config_path.open("r", encoding="utf-8") as f:
            return json5.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found: {config_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to read config as JSON5: {config_path}\n{e}")
        sys.exit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Crawl URLs from sources.txt into Markdown files.")
    parser.add_argument("config", help="Path to JSON5 config file")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    config_path = Path(args.config).expanduser()
    if not config_path.is_absolute():
        config_path = (Path.cwd() / config_path).resolve()

    config = load_config(config_path)
    working_folder = (config.get("working_folder") or "").strip()
    if not working_folder:
        print('Error: config key "working_folder" is required.')
        return 2

    working_dir = (script_dir / working_folder).resolve()
    if not working_dir.exists() or not working_dir.is_dir():
        print(f"Error: working_folder does not exist or is not a directory: {working_dir}")
        return 2

    sources_file = working_dir / "sources.txt"
    if not sources_file.exists():
        print(f"Error: sources.txt not found in working folder: {sources_file}")
        return 2

    output_dir = working_dir / "Sources"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create crawler only when we actually need to crawl something.
    crawler: Optional[FirecrawlSourceCrawler] = None

    any_crawled = False
    for line_no, url in _iter_source_lines(sources_file):
        prefix = f"{line_no:02d}"
        existing = _first_matching_file(output_dir, prefix)
        if existing is not None:
            print(f"Skip {prefix}: already exists ({existing.name})")
            continue

        if crawler is None:
            crawler = FirecrawlSourceCrawler()

        print(f"Crawling {prefix}: {url}")
        try:
            result = crawler.scrape_markdown(url)
        except Exception as e:
            print(f"Error crawling {prefix}: {url}\n{e}")
            continue

        title = _sanitize_filename_component(result.title or url)
        filename_base = f"{prefix}_{title}"
        out_path = output_dir / f"{filename_base}.md"

        # Avoid collisions (e.g., very similar/truncated titles)
        if out_path.exists():
            n = 2
            while True:
                candidate = output_dir / f"{filename_base}_{n}.md"
                if not candidate.exists():
                    out_path = candidate
                    break
                n += 1

        content = f"<!-- Source: {url} -->\n\n{result.markdown.strip()}\n"
        out_path.write_text(content, encoding="utf-8")
        print(f"Wrote: {out_path}")
        any_crawled = True

    if not any_crawled:
        print("Nothing to crawl (all sources already have numbered markdown files).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

