#!/usr/bin/env python3
"""
Test script for link extraction logic.

Tests the link filtering logic with both:
1. Sample HTML file (may not have navigation if loaded dynamically)
2. Mock data to verify filtering logic works correctly
"""

from __future__ import annotations

from pathlib import Path

from link_extractor import extract_document_links_from_html, filter_top_level_links

# Path to sample HTML file
SAMPLE_HTML = Path(__file__).parent / "1_Sample" / "FISMS-006 Leadership and Commitment - The FISMS 2024 - Information Security Home.html"


def test_with_mock_data() -> None:
    """Test filtering logic with mock link data."""
    print("\n" + "=" * 60)
    print("Testing with Mock Data")
    print("=" * 60)
    
    # Mock links: mix of top-level pages and subpages
    mock_links = [
        "https://weare.frontify.com/document/2354#/-/fisms-006-leadership-and-commitment",
        "https://weare.frontify.com/document/2354#/-/fisms-005-asset-management-policy",
        "https://weare.frontify.com/document/2354#/-/fisms-006-leadership-and-commitment/document-version-control",  # Subpage - should be filtered
        "https://weare.frontify.com/document/2354#/-/fisms-007-risk-management",
        "https://weare.frontify.com/document/2354#/-/fisms-005-asset-management-policy/some-subpage",  # Subpage - should be filtered
        "/document/2354#/-/fisms-008-incident-response",  # Relative URL
        "https://weare.frontify.com/document/2354#/-/fisms-009-business-continuity",
    ]
    
    print(f"\nInput: {len(mock_links)} links (including subpages)")
    print("Mock links:")
    for link in mock_links:
        print(f"  - {link}")
    
    # Filter links
    filtered = filter_top_level_links(mock_links)
    
    print(f"\nOutput: {len(filtered)} top-level links (subpages filtered out)")
    print("Filtered links:")
    for link in filtered:
        print(f"  ✓ {link}")
    
    # Verify
    expected_count = 5  # Should have 5 top-level pages
    assert len(filtered) == expected_count, f"Expected {expected_count} links, got {len(filtered)}"
    
    # Verify subpages are excluded
    subpages = [link for link in filtered if "/" in link.split("#/-/")[-1] if "#/-/" in link]
    assert len(subpages) == 0, f"Found subpages in filtered results: {subpages}"
    
    print("\n✓ All tests passed!")


def test_with_html_file() -> None:
    """Test link extraction from sample HTML file."""
    print("\n" + "=" * 60)
    print("Testing with Sample HTML File")
    print("=" * 60)
    
    # Load sample HTML
    if not SAMPLE_HTML.exists():
        print(f"Error: Sample HTML file not found: {SAMPLE_HTML}")
        return
    
    print(f"\nLoading HTML from: {SAMPLE_HTML.name}")
    html_content = SAMPLE_HTML.read_text(encoding="utf-8")
    print(f"HTML size: {len(html_content):,} characters")
    
    # Extract links
    print("\nExtracting document links...")
    links = extract_document_links_from_html(html_content)
    
    # Display results
    print(f"\n{'=' * 60}")
    print(f"Found {len(links)} top-level document links:")
    print(f"{'=' * 60}")
    
    if links:
        for idx, link in enumerate(links, start=1):
            print(f"{idx}. {link}")
    else:
        print("No links found!")
        print("\nNote: This is expected if navigation is loaded dynamically via JavaScript.")
        print("The saved HTML file may not contain the full navigation structure.")
    
    print(f"\n{'=' * 60}")


def main() -> None:
    """Run all tests."""
    print("=" * 60)
    print("Link Extractor Test Suite")
    print("=" * 60)
    
    # Test with mock data (verifies filtering logic)
    test_with_mock_data()
    
    # Test with HTML file (may not find links if loaded dynamically)
    test_with_html_file()
    
    print("\n" + "=" * 60)
    print("Test Suite Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
