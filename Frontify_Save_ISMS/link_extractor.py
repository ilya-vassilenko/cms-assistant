"""
Link extraction logic for Frontify ISMS documents.

Extracts top-level document links from HTML, filtering out subpages.
"""

from __future__ import annotations

from urllib.parse import urljoin, urlparse

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 not installed. Install with: pip install beautifulsoup4")
    raise


def extract_document_links_from_html(html_content: str, base_url: str = "https://weare.frontify.com") -> list[str]:
    """
    Extract top-level document links from HTML content.
    
    Args:
        html_content: HTML content as string
        base_url: Base URL for constructing absolute URLs
        
    Returns:
        List of absolute URLs for top-level pages (subpages are filtered out)
    """
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Find all <aside> elements
    aside_elements = soup.find_all("aside")
    
    # Collect all hrefs from links in <aside> that match the pattern
    hrefs = []
    for aside in aside_elements:
        links = aside.find_all("a", href=True)
        for link in links:
            href = link.get("href", "")
            if href and "/document/2354#/-/" in href:
                hrefs.append(href)
    
    # Filter to only top-level pages
    return filter_top_level_links(hrefs, base_url)


def filter_top_level_links(hrefs: list[str], base_url: str = "https://weare.frontify.com") -> list[str]:
    """
    Filter a list of hrefs to only include top-level document links.
    
    This is the core filtering logic that can be reused.
    
    Args:
        hrefs: List of href strings (can be relative or absolute)
        base_url: Base URL for constructing absolute URLs
        
    Returns:
        List of canonical absolute URLs for top-level pages only
    """
    seen = set()
    unique_links = []
    
    for href in hrefs:
        if not href:
            continue
        
        # Ensure absolute URL
        absolute_url = urljoin(base_url, href)
        parsed = urlparse(absolute_url)
        
        # Must match /document/2354#/-/ pattern
        if "/document/2354#" not in absolute_url:
            continue
        
        # Extract hash fragment (urlparse returns fragment without #)
        # For URL like "https://weare.frontify.com/document/2354#/-/test"
        # fragment will be "/-/test"
        if not parsed.fragment:
            continue
        
        fragment = parsed.fragment
        
        # Must start with /-/ (fragment from urlparse doesn't include #)
        if not fragment.startswith("/-/"):
            continue
        
        # Remove the /-/ prefix to get the path part
        # Note: Links don't have trailing slashes, e.g., "/-/fisms-005-asset-management-policy"
        path_part = fragment[3:]  # Remove "/-/"
        
        # Split by / to count segments (filter out empty strings)
        segments = [s for s in path_part.split("/") if s]
        
        # Top-level pages have exactly 1 segment (no additional path components)
        # Subpages have more segments (additional path components after the page name)
        if len(segments) != 1:
            # This is a subpage, skip it
            continue
        
        # Construct the canonical URL: https://weare.frontify.com/document/2354#/-/<page>
        # Note: fragment from urlparse doesn't include #, so we add it back
        canonical_url = f"{base_url}/document/2354#{fragment}"
        
        if canonical_url not in seen:
            seen.add(canonical_url)
            unique_links.append(canonical_url)
    
    return unique_links
