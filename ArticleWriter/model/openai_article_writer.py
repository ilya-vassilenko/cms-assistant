import os
from dataclasses import dataclass
from typing import List, Optional

_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


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

    When the requested model name contains "/" (e.g. "anthropic/claude-opus-4.6"),
    the request is routed through OpenRouter using OPENROUTER_API_KEY.
    Otherwise the standard OPENAI_API_KEY is used.
    """

    def __init__(self, api_key_env: str = "OPENAI_API_KEY"):
        self._default_api_key_env = api_key_env

    def _get_client(self, model: str):
        from openai import OpenAI  # type: ignore

        if "/" in model:
            api_key = (os.getenv("OPENROUTER_API_KEY") or "").strip()
            if not api_key:
                raise ValueError(
                    "Missing OpenRouter API key. Please set environment variable OPENROUTER_API_KEY."
                )
            return OpenAI(api_key=api_key, base_url=_OPENROUTER_BASE_URL)

        api_key = (os.getenv(self._default_api_key_env) or "").strip()
        if not api_key:
            raise ValueError(
                f"Missing OpenAI API key. Please set environment variable {self._default_api_key_env}."
            )
        return OpenAI(api_key=api_key)

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

        resp = self._get_client(req.model).chat.completions.create(
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

