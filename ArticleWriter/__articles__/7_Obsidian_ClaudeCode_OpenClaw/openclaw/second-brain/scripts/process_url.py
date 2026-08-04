#!/usr/bin/env python3
"""Fetch a URL, extract readable content, summarize via OpenAI, and return structured JSON."""

import json
import os
import re
import subprocess
import sys
from urllib.parse import urlparse

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
MODEL = "gpt-4o-mini"
MAX_CONTENT_CHARS = 12000


def fetch_page(url: str) -> dict:
    """Fetch page HTML and extract title + text via curl + simple parsing."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "15", "-A",
             "Mozilla/5.0 (compatible; SecondBrain/1.0)", url],
            capture_output=True, text=True, timeout=20,
        )
        html = result.stdout
    except (subprocess.TimeoutExpired, Exception) as exc:
        return {"error": str(exc), "html": ""}

    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else urlparse(url).netloc

    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return {"title": title, "text": text[:MAX_CONTENT_CHARS]}


def summarize(title: str, text: str, url: str) -> dict:
    """Call OpenAI API to generate summary and tags."""
    if not OPENAI_API_KEY:
        return {
            "title": title,
            "summary": "(auto-summary unavailable — no OPENAI_API_KEY)",
            "tags": ["link"],
            "source_domain": urlparse(url).netloc,
        }

    prompt = f"""Analyze this web page and return a JSON object with exactly these fields:
- "summary": a 2-3 sentence summary of the article/page
- "tags": an array of 2-5 lowercase single-word tags describing the topic

Page title: {title}
Page content (truncated):
{text[:8000]}"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a concise knowledge-base assistant. Return only valid JSON."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 300,
    }

    try:
        result = subprocess.run(
            ["curl", "-s", "https://api.openai.com/v1/chat/completions",
             "-H", f"Authorization: Bearer {OPENAI_API_KEY}",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(payload)],
            capture_output=True, text=True, timeout=30,
        )
        response = json.loads(result.stdout)
        content = response["choices"][0]["message"]["content"]
        content = re.sub(r"```json\s*", "", content)
        content = re.sub(r"```\s*$", "", content)
        data = json.loads(content)
    except Exception:
        data = {"summary": text[:200] + "...", "tags": ["link"]}

    return {
        "title": title,
        "summary": data.get("summary", ""),
        "tags": data.get("tags", ["link"]),
        "source_domain": urlparse(url).netloc,
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: process_url.py <url>"}))
        sys.exit(1)

    url = sys.argv[1].strip()
    page = fetch_page(url)

    if "error" in page:
        print(json.dumps({
            "title": urlparse(url).netloc,
            "summary": f"Failed to fetch: {page['error']}",
            "tags": ["link", "fetch-failed"],
            "source_domain": urlparse(url).netloc,
        }))
        sys.exit(0)

    result = summarize(page["title"], page["text"], url)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
