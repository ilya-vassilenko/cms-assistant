import base64
import json
import os
import re
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class OpenRouterImageRequest:
    prompt: str
    model: str = "google/gemini-2.5-flash-image"
    aspect_ratio: str = "16:9"


@dataclass(frozen=True)
class GeneratedImage:
    mime_type: str
    image_bytes: bytes

    @property
    def extension(self) -> str:
        m = (self.mime_type or "").lower().strip()
        return {
            "image/png": "png",
            "image/jpeg": "jpg",
            "image/jpg": "jpg",
            "image/webp": "webp",
        }.get(m, "png")


@dataclass(frozen=True)
class OpenRouterNoImageError(Exception):
    """
    Raised when OpenRouter returns a valid response but no image payload is present.
    Carries the parsed response for structured logging upstream.
    """

    message: str
    response: Dict[str, Any]

    def __str__(self) -> str:  # pragma: no cover
        return self.message


class OpenRouterImageGenerator:
    """
    Calls OpenRouter image generation via chat completions.

    Expects env var: OPENROUTER_API_KEY
    """

    def __init__(self, api_key_env: str = "OPENROUTER_API_KEY"):
        api_key = (os.getenv(api_key_env) or "").strip()
        if not api_key:
            raise ValueError(f"Missing OpenRouter API key. Please set environment variable {api_key_env}.")
        self._api_key = api_key
        self._endpoint = "https://openrouter.ai/api/v1/chat/completions"

    def generate(self, req: OpenRouterImageRequest) -> GeneratedImage:
        prompt = (req.prompt or "").strip()
        if not prompt:
            raise ValueError("prompt is empty")

        payload = {
            "model": req.model,
            "modalities": ["image", "text"],
            "image_config": {"aspect_ratio": req.aspect_ratio},
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Generate a single 16:9 thumbnail image.\n"
                        "No readable text, no logos, no brand names.\n\n"
                        f"{prompt}"
                    ),
                }
            ],
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
            with urllib.request.urlopen(request, timeout=300) as resp:
                body = resp.read()
        except Exception as e:
            raise RuntimeError(f"OpenRouter request failed: {e}") from e

        try:
            parsed: Dict[str, Any] = json.loads(body.decode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"OpenRouter returned non-JSON response: {body[:200]!r}") from e

        data_url = self._extract_first_image_data_url(parsed)
        if not data_url:
            raise OpenRouterNoImageError(
                message="OpenRouter response did not contain an image.",
                response=parsed,
            )

        mime_type, image_bytes = self._decode_data_url(data_url)
        return GeneratedImage(mime_type=mime_type, image_bytes=image_bytes)

    @staticmethod
    def extract_text_message(parsed: Dict[str, Any]) -> Optional[str]:
        """
        Best-effort extraction of assistant text content from a chat response.
        """
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

    @staticmethod
    def _extract_first_image_data_url(parsed: Dict[str, Any]) -> Optional[str]:
        """
        Extract base64 data URL from common OpenRouter response shapes.
        """
        try:
            choices = parsed.get("choices") or []
            if not choices:
                return None
            msg = (choices[0] or {}).get("message") or {}
            images = msg.get("images") or []
            if images:
                img0 = images[0] or {}
                # common: imageUrl: { url: "data:image/png;base64,..." }
                for key in ("imageUrl", "image_url"):
                    v = img0.get(key)
                    if isinstance(v, dict):
                        u = v.get("url")
                        if isinstance(u, str) and u.startswith("data:image/"):
                            return u
                # sometimes flattened: { url: "data:image/..." }
                u = img0.get("url")
                if isinstance(u, str) and u.startswith("data:image/"):
                    return u
        except Exception:
            return None
        return None

    @staticmethod
    def _decode_data_url(data_url: str) -> Tuple[str, bytes]:
        """
        Decode data:image/<type>;base64,<...>
        """
        m = re.match(r"^data:(image\/[a-zA-Z0-9.+-]+);base64,(.+)$", data_url)
        if not m:
            raise ValueError("Unsupported image data URL format")
        mime = m.group(1)
        b64 = m.group(2)
        try:
            raw = base64.b64decode(b64, validate=False)
        except Exception as e:
            raise ValueError("Failed to decode base64 image") from e
        return mime, raw

