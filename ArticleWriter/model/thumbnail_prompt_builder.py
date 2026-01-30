import json
import os
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ThumbnailPromptRequest:
    article_markdown: str
    model: str = "openai/gpt-5-mini"
    temperature: float = 0.4


class ThumbnailPromptBuilder:
    """
    Builds a single image-generation prompt from article markdown using OpenRouter
    so that different text models can be tested.

    Expects the API key in env var: OPENROUTER_API_KEY
    """

    def __init__(self, api_key_env: str = "OPENROUTER_API_KEY"):
        api_key = (os.getenv(api_key_env) or "").strip()
        if not api_key:
            raise ValueError(f"Missing OpenRouter API key. Please set environment variable {api_key_env}.")
        self._api_key = api_key
        self._endpoint = "https://openrouter.ai/api/v1/chat/completions"

    def build_prompt(self, req: ThumbnailPromptRequest) -> str:
        article_md = (req.article_markdown or "").strip()
        if not article_md:
            raise ValueError("article_markdown is empty")

        system = (
            "You create prompts for text-to-image thumbnail generation.\n"
            "Output must be a SINGLE prompt only, no preface, no quotes, no markdown.\n"
            "Style: professional, clean, modern, editorial illustration suitable for an infosec article.\n"
            "Constraints: no logos, no brand names, no copyrighted characters, no readable text in the image.\n"
            "Include composition guidance for a 16:9 thumbnail."
        )

        user = (
            "Based on this article, write one strong image prompt for a thumbnail.\n"
            "Avoid mainstream symbols like lock for security topics.\n\n"
            "ARTICLE (markdown):\n"
            f"{article_md}"
        )

        payload = {
            "model": req.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": req.temperature,
        }

        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self._endpoint,
            data=data,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=120) as resp:
                body = resp.read()
        except Exception as e:
            raise RuntimeError(f"OpenRouter request failed: {e}") from e

        try:
            parsed: Dict[str, Any] = json.loads(body.decode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"OpenRouter returned non-JSON response: {body[:200]!r}") from e

        content = self._extract_content(parsed)

        if not content or not content.strip():
            raise RuntimeError("OpenRouter returned empty thumbnail prompt")

        # Ensure single-line-ish prompt output
        return content.strip()

    @staticmethod
    def _extract_content(parsed: Dict[str, Any]) -> Optional[str]:
        try:
            choices = parsed.get("choices") or []
            if not choices:
                return None
            msg = (choices[0] or {}).get("message") or {}
            content = msg.get("content")
            if isinstance(content, str):
                return content
        except Exception:
            return None
        return None

