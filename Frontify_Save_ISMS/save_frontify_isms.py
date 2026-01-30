#!/usr/bin/env python3
"""
Frontify ISMS Document Exporter

Scrapes Frontify guideline documents from weare.frontify.com:
- Opens browser and waits for manual login + 2FA
- Collects links from <aside> navigation matching /document/2354#/
- Exports each document's <main> content and full page HTML
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
import time
from urllib.parse import urljoin, urlparse

try:
    from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
except ImportError:
    print("Error: playwright not installed. Run: pip install playwright && python3 -m playwright install chromium")
    sys.exit(1)

# Import link extraction logic
try:
    from link_extractor import filter_top_level_links
except ImportError:
    # Fallback if module not found (shouldn't happen in normal usage)
    filter_top_level_links = None

try:
    from colorama import Fore, Style, init as colorama_init
except ImportError:
    # Fallback when colorama isn't installed
    class _NoColor:
        CYAN = GREEN = YELLOW = RED = LIGHTMAGENTA_EX = RESET = ""

    class _NoStyle:
        RESET_ALL = ""

    Fore = _NoColor()  # type: ignore
    Style = _NoStyle()  # type: ignore

    def colorama_init(*_args, **_kwargs) -> None:  # type: ignore
        return None

colorama_init(autoreset=True)

# Output directories
SCRIPT_DIR = Path(__file__).parent
OUTPUT_MAIN = SCRIPT_DIR / "2_Output_MainOnly"
OUTPUT_FULL = SCRIPT_DIR / "3_Output_Full"

# Target URL
FRONTIFY_URL = "https://weare.frontify.com"


def c_info(msg: str) -> str:
    return f"{Fore.CYAN}{msg}{Style.RESET_ALL}"


def c_success(msg: str) -> str:
    return f"{Fore.GREEN}{msg}{Style.RESET_ALL}"


def c_warn(msg: str) -> str:
    return f"{Fore.YELLOW}{msg}{Style.RESET_ALL}"


def c_error(msg: str) -> str:
    return f"{Fore.RED}{msg}{Style.RESET_ALL}"


def c_prompt(msg: str) -> str:
    return f"{Fore.LIGHTMAGENTA_EX}{msg}{Style.RESET_ALL}"


def sanitize_filename(title: str, max_length: int = 200) -> str:
    """
    Sanitize a title to be a valid filename on macOS/Unix.
    Removes/replaces illegal characters and trims length.
    """
    # Remove/replace illegal characters for macOS filesystem
    # Illegal: / : < > | \ " ? * and control characters
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', title)
    # Replace multiple underscores/spaces with single underscore
    sanitized = re.sub(r'[_\s]+', '_', sanitized)
    # Trim leading/trailing underscores and whitespace
    sanitized = sanitized.strip('_').strip()
    # Cap length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip('_')
    # Ensure not empty
    if not sanitized:
        sanitized = "untitled"
    return sanitized


def get_unique_filename(base_dir: Path, base_name: str, extension: str = ".html") -> Path:
    """
    Get a unique filename by appending (2), (3), etc. if needed.
    """
    filename = base_name + extension
    filepath = base_dir / filename
    
    if not filepath.exists():
        return filepath
    
    counter = 2
    while True:
        new_filename = f"{base_name} ({counter}){extension}"
        new_filepath = base_dir / new_filename
        if not new_filepath.exists():
            return new_filepath
        counter += 1


def setup_browser(playwright) -> tuple[Browser, BrowserContext, Page]:
    """
    Launch a headful browser with realistic Chrome headers.
    """
    print(c_info("Launching browser..."))
    
    # Try to use installed Chrome, fallback to Chromium
    try:
        browser = playwright.chromium.launch(
            channel="chrome",
            headless=False,
        )
        print(c_success("Using Google Chrome"))
    except Exception:
        browser = playwright.chromium.launch(headless=False)
        print(c_info("Using Chromium"))
    
    # Create context with realistic Chrome headers for proper localization
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
        locale="en-US",
        timezone_id="America/New_York",
        extra_http_headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "DNT": "1",
            "Cache-Control": "max-age=0",
        },
    )
    
    page = context.new_page()
    return browser, context, page


def collect_document_links(page: Page) -> list[str]:
    """
    Collect all links from <aside> that match /document/2354#/-/ pattern.
    Only includes top-level pages (not subpages).
    Returns list of absolute URLs, deduplicated while preserving order.
    """
    print(c_info("Waiting for navigation sidebar..."))
    
    try:
        page.wait_for_selector("aside a", timeout=10000)
    except Exception as e:
        print(c_error(f"Error: Could not find <aside> navigation: {e}"))
        return []
    
    print(c_info("Collecting document links..."))
    
    # Get all links from aside that match the pattern /document/2354#/-/
    links = page.locator('aside a[href*="/document/2354#/-/"]').evaluate_all(
        """elements => elements.map(el => el.href)"""
    )
    
    # Use the extracted link filtering logic
    if filter_top_level_links:
        base_domain = "https://weare.frontify.com"
        unique_links = filter_top_level_links(links, base_domain)
    else:
        # Fallback to inline logic (shouldn't happen)
        print(c_warn("Warning: Using fallback link filtering logic"))
        unique_links = _filter_links_fallback(links)
    
    print(c_success(f"Found {len(unique_links)} document links (top-level pages only)"))
    return unique_links


def _filter_links_fallback(hrefs: list[str]) -> list[str]:
    """
    Fallback link filtering logic (used if link_extractor module not available).
    """
    seen = set()
    unique_links = []
    base_domain = "https://weare.frontify.com"
    
    for href in hrefs:
        if not href:
            continue
        
        absolute_url = urljoin(base_domain, href)
        parsed = urlparse(absolute_url)
        
        # Fragment from urlparse doesn't include #, so it will be "/-/..." not "#/-/..."
        if not parsed.fragment or not parsed.fragment.startswith("/-/"):
            continue
        
        fragment = parsed.fragment
        path_part = fragment[3:]  # Remove "/-/"
        segments = [s for s in path_part.split("/") if s]
        
        if len(segments) != 1:
            continue
        
        canonical_url = f"{base_domain}/document/2354#{fragment}"
        if canonical_url not in seen:
            seen.add(canonical_url)
            unique_links.append(canonical_url)
    
    return unique_links


def extract_and_save_document(page: Page, url: str, doc_index: int, total: int) -> bool:
    """
    Navigate to a document URL, extract title and content, save files.
    Returns True on success, False on error.
    """
    print(c_info(f"\n[{doc_index}/{total}] Processing: {url}"))
    
    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
    except Exception as e:
        print(c_error(f"Error navigating to {url}: {e}"))
        return False
    
    # Give the page a bit of extra time to fully render
    time.sleep(3)
    
    # Wait for main content and title
    try:
        page.wait_for_selector("main h1", timeout=10000)
    except Exception as e:
        print(c_error(f"Error: Could not find <main><h1> on page: {e}"))
        return False
    
    # Extract title
    try:
        title_text = page.locator("main h1").first.inner_text().strip()
        if not title_text:
            print(c_warn("Warning: Title is empty, using fallback"))
            title_text = f"Document_{doc_index}"
    except Exception as e:
        print(c_warn(f"Warning: Could not extract title: {e}, using fallback"))
        title_text = f"Document_{doc_index}"
    
    print(c_info(f"Title: {title_text}"))
    
    # Sanitize filename
    safe_filename = sanitize_filename(title_text)
    
    # Extract main content
    try:
        main_html = page.locator("main").first.evaluate("el => el.outerHTML")
    except Exception as e:
        print(c_error(f"Error extracting <main> content: {e}"))
        return False
    
    # Get full page HTML
    try:
        full_html = page.content()
    except Exception as e:
        print(c_error(f"Error getting full page HTML: {e}"))
        return False
    
    # Save main-only HTML
    main_filepath = get_unique_filename(OUTPUT_MAIN, safe_filename, ".html")
    try:
        main_filepath.write_text(main_html, encoding="utf-8")
        print(c_success(f"Saved main content: {main_filepath.name}"))
    except Exception as e:
        print(c_error(f"Error saving main content: {e}"))
        return False
    
    # Save full page HTML
    full_filepath = get_unique_filename(OUTPUT_FULL, safe_filename, ".html")
    try:
        full_filepath.write_text(full_html, encoding="utf-8")
        print(c_success(f"Saved full page: {full_filepath.name}"))
    except Exception as e:
        print(c_error(f"Error saving full page: {e}"))
        return False
    
    return True


def main() -> None:
    """
    Main execution flow.
    """
    print(c_info("=" * 60))
    print(c_info("Frontify ISMS Document Exporter"))
    print(c_info("=" * 60))
    
    # Ensure output directories exist
    OUTPUT_MAIN.mkdir(parents=True, exist_ok=True)
    OUTPUT_FULL.mkdir(parents=True, exist_ok=True)
    print(c_success(f"Output directories ready: {OUTPUT_MAIN.name}, {OUTPUT_FULL.name}"))
    
    with sync_playwright() as playwright:
        browser, context, page = setup_browser(playwright)
        
        try:
            # Navigate to Frontify
            print(c_info(f"\nOpening {FRONTIFY_URL}..."))
            page.goto(FRONTIFY_URL, wait_until="domcontentloaded", timeout=30000)
            
            # Wait for manual login + 2FA
            print(c_prompt("\n" + "=" * 60))
            print(c_prompt("Please complete login and 2FA authentication in the browser."))
            print(c_prompt("=" * 60))
            input(c_prompt("\nAfter login+2FA, press Enter to continue..."))
            
            # Collect document links from the first page
            links = collect_document_links(page)
            
            if not links:
                print(c_error("No document links found. Exiting."))
                return
            
            # Print all found links for user confirmation
            print(c_info("\n" + "=" * 60))
            print(c_info(f"Found {len(links)} document links:"))
            print(c_info("=" * 60))
            for idx, link in enumerate(links, start=1):
                print(c_info(f"{idx}. {link}"))
            print(c_info("=" * 60))
            
            # Wait for user confirmation
            print(c_prompt("\nPlease review the links above."))
            input(c_prompt("Press Enter to confirm and proceed with scraping, or Ctrl+C to cancel..."))
            
            # Process all documents (no per-document keystroke pauses)
            for idx, link in enumerate(links, start=1):
                success = extract_and_save_document(page, link, idx, len(links))
                if not success:
                    print(c_error(f"Failed to process document {idx}/{len(links)}. Continuing..."))
                    continue
            
            print(c_success("\n" + "=" * 60))
            print(c_success("All documents processed successfully!"))
            print(c_success("=" * 60))
            
        except KeyboardInterrupt:
            print(c_warn("\n\nInterrupted by user. Exiting..."))
        except Exception as e:
            print(c_error(f"\nUnexpected error: {e}"))
            import traceback
            traceback.print_exc()
        finally:
            print(c_info("\nClosing browser..."))
            browser.close()


if __name__ == "__main__":
    main()
