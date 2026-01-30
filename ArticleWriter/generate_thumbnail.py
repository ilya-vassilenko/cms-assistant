#!/usr/bin/env python3
"""
ArticleWriter - generate a thumbnail for the latest article in Output/.

Usage:
  python ArticleWriter/generate_thumbnail.py ArticleWriter/1_Arxio_NewOutlook.config
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import json5

from model.latest_output_picker import LatestOutputPicker
from model.logging_utils import dim, error, info, prompt_pink, success, warning
from model.openrouter_image_generator import (
    OpenRouterImageGenerator,
    OpenRouterImageRequest,
    OpenRouterNoImageError,
)
from model.thumbnail_prompt_builder import ThumbnailPromptBuilder, ThumbnailPromptRequest


def load_config(config_path: Path) -> dict:
    try:
        with config_path.open("r", encoding="utf-8") as f:
            return json5.load(f)
    except FileNotFoundError:
        error(f"Config file not found: {config_path}")
        sys.exit(1)
    except Exception as e:
        error(f"Failed to read config as JSON5: {config_path}\n{e}")
        sys.exit(1)

def _model_slug(model_id: str) -> str:
    return (
        (model_id or "")
        .strip()
        .replace("/", "_")
        .replace(":", "_")
        .replace(" ", "_")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a 16:9 thumbnail for the latest Output/*.md article.")
    parser.add_argument("config", help="Path to JSON5 config file")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    config_path = Path(args.config).expanduser()
    if not config_path.is_absolute():
        config_path = (Path.cwd() / config_path).resolve()

    config = load_config(config_path)
    working_folder = (config.get("working_folder") or "").strip()
    if not working_folder:
        error('Config key "working_folder" is required.')
        return 2

    working_dir = (script_dir / working_folder).resolve()
    if not working_dir.exists() or not working_dir.is_dir():
        error(f"working_folder does not exist or is not a directory: {working_dir}")
        return 2

    output_dir = working_dir / "Output"
    picker = LatestOutputPicker()
    pick = picker.pick_latest(output_dir)
    info(f"Using latest article: {pick.path.name}")
    dim(f"Article prefix: {pick.prefix}")

    article_md = pick.path.read_text(encoding="utf-8")
    if not article_md.strip():
        error(f"Latest article is empty: {pick.path}")
        return 2

    thumbnails_dir = working_dir / "Thumbnails"
    thumbnails_dir.mkdir(parents=True, exist_ok=True)

    # Use seconds in output filenames to avoid overwrites on quick re-generations.
    run_prefix = datetime.now().strftime("%Y-%m-%d %H_%M_%S")
    dim(f"Run prefix: {run_prefix}")

    # Attempts-based config: each attempt defines prompt model + thumbnail model.
    # Also supports legacy config keys for backward compatibility.
    attempts = config.get("thumbnail_attempts")
    normalized_attempts: list[dict] = []
    if isinstance(attempts, list) and attempts:
        for a in attempts:
            if isinstance(a, dict):
                normalized_attempts.append(a)

    if not normalized_attempts:
        # Backward compatible fallback:
        # - prompt model from openai_model_prompt (or default)
        # - enabled thumbnail models from thumbnail_models dict (or openrouter_model_image)
        prompt_model = (config.get("openai_model_prompt") or "openai/gpt-5-mini").strip()
        thumbnail_models = config.get("thumbnail_models")
        enabled_models: list[str] = []
        if isinstance(thumbnail_models, dict) and thumbnail_models:
            for model_id, enabled in thumbnail_models.items():
                if bool(enabled):
                    enabled_models.append(str(model_id))
        else:
            enabled_models.append((config.get("openrouter_model_image") or "google/gemini-2.5-flash-image").strip())
        for model_id in enabled_models:
            normalized_attempts.append(
                {
                    "enabled": True,
                    "prompt_model": prompt_model,
                    "thumbnail_model": model_id,
                }
            )

    prompt_builder = ThumbnailPromptBuilder()
    generator = OpenRouterImageGenerator()

    # Cache prompts per prompt model within this run.
    prompt_cache: dict[str, str] = {}

    wrote_any = False
    info(f"Attempts to run: {len(normalized_attempts)}")
    for idx, attempt in enumerate(normalized_attempts, start=1):
        if attempt.get("enabled") is False:
            dim(f"[{idx}/{len(normalized_attempts)}] Skipping disabled attempt")
            continue

        prompt_model = str(attempt.get("prompt_model") or "").strip()
        thumb_model = str(attempt.get("thumbnail_model") or "").strip()
        if not prompt_model or not thumb_model:
            warning(f"[{idx}/{len(normalized_attempts)}] Skipping attempt with missing model(s)")
            continue

        # Prompt caching: only generate once per prompt_model.
        prompt = prompt_cache.get(prompt_model)
        if prompt is None:
            info(f"[{idx}/{len(normalized_attempts)}] Generating prompt with: {prompt_model}")
            prompt = prompt_builder.build_prompt(
                ThumbnailPromptRequest(
                    article_markdown=article_md,
                    model=prompt_model,
                )
            )
            prompt_cache[prompt_model] = prompt
            prompt_pink("---- Nano Banana prompt (generated) ----")
            prompt_pink(prompt.strip())
            prompt_pink("---- end prompt ----")
        else:
            info(f"[{idx}/{len(normalized_attempts)}] Reusing cached prompt for: {prompt_model}")

        prompt_tag = _model_slug(prompt_model)
        thumb_tag = _model_slug(thumb_model)
        # Filename requirement: prompt model, then "--", then thumbnail model
        base_name = f"{run_prefix} {prompt_tag}--{thumb_tag} Thumbnail"

        prompt_path = thumbnails_dir / f"{base_name}.prompt.txt"
        prompt_path.write_text(prompt.strip() + "\n", encoding="utf-8")
        dim(f"[{idx}/{len(normalized_attempts)}] Prompt saved: {prompt_path.name}")

        info(f"[{idx}/{len(normalized_attempts)}] Generating thumbnail with: {thumb_model}")
        try:
            image = generator.generate(
                OpenRouterImageRequest(
                    prompt=prompt,
                    model=thumb_model,
                    aspect_ratio="16:9",
                )
            )
        except OpenRouterNoImageError as e:
            # Structured red error output, but keep running further attempts.
            resp = e.response or {}
            resp_id = resp.get("id")
            provider = resp.get("provider")
            model = resp.get("model")
            usage = resp.get("usage")
            text_msg = OpenRouterImageGenerator.extract_text_message(resp)

            error("=== THUMBNAIL GENERATION FAILED (no image returned) ===")
            error(f"Attempt: {idx}/{len(normalized_attempts)}")
            error(f"Prompt model: {prompt_model}")
            error(f"Thumbnail model: {thumb_model}")
            error(f"Run prefix: {run_prefix}")
            error(f"OpenRouter id: {resp_id}")
            error(f"Provider: {provider}")
            error(f"Model (echo): {model}")
            if usage is not None:
                error(f"Usage: {usage}")
            if text_msg:
                error("--- assistant message (text) ---")
                error(text_msg.strip())
            error("=== END FAILURE ===")
            continue
        except Exception as e:
            # Any other error: log and continue.
            error("=== THUMBNAIL GENERATION FAILED (exception) ===")
            error(f"Attempt: {idx}/{len(normalized_attempts)}")
            error(f"Prompt model: {prompt_model}")
            error(f"Thumbnail model: {thumb_model}")
            error(f"Run prefix: {run_prefix}")
            error(str(e))
            error("=== END FAILURE ===")
            continue

        out_path = thumbnails_dir / f"{base_name}.{image.extension}"
        out_path.write_bytes(image.image_bytes)
        success(f"[{idx}/{len(normalized_attempts)}] Wrote thumbnail: {out_path.name}")
        wrote_any = True

    if not wrote_any:
        warning("No thumbnails generated (no enabled models in config).")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

