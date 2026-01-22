import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class ArticleWriteRequest:
    system_prompt: str
    sources_markdown: List[str]
    instructions: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.2


class OpenAIArticleWriter:
    """
    Thin wrapper around the OpenAI Chat Completions API.

    Expects the API key in env var: OPENAI_API_KEY
    """

    def __init__(self, api_key_env: str = "OPENAI_API_KEY"):
        api_key = (os.getenv(api_key_env) or "").strip()
        if not api_key:
            raise ValueError(f"Missing OpenAI API key. Please set environment variable {api_key_env}.")

        # Lazy import so module can be imported without dependency installed.
        from openai import OpenAI  # type: ignore

        self._client = OpenAI(api_key=api_key)

    def write_article(self, req: ArticleWriteRequest) -> str:
        system_prompt = (req.system_prompt or "").strip()
        if not system_prompt:
            raise ValueError("system_prompt is empty")

        instructions = (req.instructions or "").strip()
        if not instructions:
            raise ValueError("instructions is empty")

        sources_blob = "\n\n---\n\n".join([s.strip() for s in req.sources_markdown if (s or "").strip()])
        if not sources_blob:
            raise ValueError("No sources_markdown provided (or all were empty)")

        # Keep structure simple and robust.
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    "Here are the sources (Markdown). Use them as factual grounding.\n\n"
                    f"{sources_blob}"
                ),
            },
            {
                "role": "user",
                "content": (
                    "Now follow these instructions. Return ONLY the final article in Markdown format.\n\n"
                    f"{instructions}"
                ),
            },
        ]

        resp = self._client.chat.completions.create(
            model=req.model,
            messages=messages,
            temperature=req.temperature,
        )

        content: Optional[str] = None
        if resp and getattr(resp, "choices", None):
            choice0 = resp.choices[0]
            msg = getattr(choice0, "message", None)
            content = getattr(msg, "content", None)

        if not content or not content.strip():
            raise RuntimeError("OpenAI returned empty content")

        return content.strip()

