import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ThumbnailPromptRequest:
    article_markdown: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.4


class ThumbnailPromptBuilder:
    """
    Builds a single image-generation prompt from article markdown using OpenAI.

    Expects the API key in env var: OPENAI_API_KEY
    """

    def __init__(self, api_key_env: str = "OPENAI_API_KEY"):
        api_key = (os.getenv(api_key_env) or "").strip()
        if not api_key:
            raise ValueError(f"Missing OpenAI API key. Please set environment variable {api_key_env}.")

        from openai import OpenAI  # type: ignore

        self._client = OpenAI(api_key=api_key)

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
            "Prefer symbolic/abstract visuals (e.g., privacy, email, cloud, compliance, risk).\n\n"
            "ARTICLE (markdown):\n"
            f"{article_md}"
        )

        resp = self._client.chat.completions.create(
            model=req.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=req.temperature,
        )

        content: Optional[str] = None
        if resp and getattr(resp, "choices", None):
            msg = getattr(resp.choices[0], "message", None)
            content = getattr(msg, "content", None)

        if not content or not content.strip():
            raise RuntimeError("OpenAI returned empty thumbnail prompt")

        # Ensure single-line-ish prompt output
        return content.strip()

