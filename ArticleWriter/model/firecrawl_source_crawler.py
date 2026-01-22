import os
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class FirecrawlScrapeResult:
    title: str
    markdown: str
    metadata: Dict[str, Any]


class FirecrawlSourceCrawler:
    """
    Small wrapper around Firecrawl SDK to keep the main script readable.

    Expects the API key in env var: FIRECRAWL_API_KEY
    """

    def __init__(self, timeout_ms: int = 600_000, only_main_content: bool = True):
        self.timeout_ms = timeout_ms
        self.only_main_content = only_main_content

        api_key = (os.getenv("FIRECRAWL_API_KEY") or "").strip()
        if not api_key:
            raise ValueError(
                "Missing Firecrawl API key. Please set environment variable FIRECRAWL_API_KEY."
            )

        # Lazy import so the script can still load/validate config without Firecrawl installed.
        from firecrawl import Firecrawl  # type: ignore

        self._client = Firecrawl(api_key=api_key)

    def scrape_markdown(self, url: str) -> FirecrawlScrapeResult:
        """
        Scrape a single URL and return (title, markdown, metadata).
        """
        url = (url or "").strip()
        if not url:
            raise ValueError("URL is empty")

        # Firecrawl SDK has evolved; handle common response shapes defensively.
        result: Any
        if hasattr(self._client, "scrape"):
            result = self._client.scrape(
                url=url,
                formats=["markdown"],
                only_main_content=self.only_main_content,
                timeout=self.timeout_ms,
            )
        elif hasattr(self._client, "scrape_url"):
            # Older SDK naming
            result = self._client.scrape_url(
                url,
                formats=["markdown"],
                only_main_content=self.only_main_content,
                timeout=self.timeout_ms,
            )
        else:
            raise RuntimeError("Firecrawl client does not expose a scrape method")

        data = self._unwrap_data(result)
        metadata = self._unwrap_metadata(data)

        title = (metadata.get("title") or data.get("title") or "").strip()
        markdown = (data.get("markdown") or "").strip()

        if not markdown:
            raise RuntimeError(f"Firecrawl returned empty markdown for URL: {url}")

        return FirecrawlScrapeResult(title=title, markdown=markdown, metadata=metadata)

    @staticmethod
    def _unwrap_data(result: Any) -> Dict[str, Any]:
        """
        Normalize Firecrawl responses into a plain dict `data`.
        Supports dict-style responses and simple objects.
        """
        if result is None:
            return {}

        # dict response: { success, data: {...} } or already data-like
        if isinstance(result, dict):
            if "data" in result and isinstance(result.get("data"), dict):
                return result["data"]
            return result

        # object response with `.data`
        if hasattr(result, "data"):
            data = getattr(result, "data")
            if isinstance(data, dict):
                return data

        # fallback: try to treat as mapping
        try:
            return dict(result)  # type: ignore[arg-type]
        except Exception:
            return {}

    @staticmethod
    def _unwrap_metadata(data: Dict[str, Any]) -> Dict[str, Any]:
        md = data.get("metadata")
        if isinstance(md, dict):
            return md
        return {}

