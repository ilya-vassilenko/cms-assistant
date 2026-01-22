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
from model.openrouter_image_generator import OpenRouterImageGenerator, OpenRouterImageRequest
from model.thumbnail_prompt_builder import ThumbnailPromptBuilder, ThumbnailPromptRequest


def load_config(config_path: Path) -> dict:
    try:
        with config_path.open("r", encoding="utf-8") as f:
            return json5.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found: {config_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to read config as JSON5: {config_path}\n{e}")
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
        print('Error: config key "working_folder" is required.')
        return 2

    working_dir = (script_dir / working_folder).resolve()
    if not working_dir.exists() or not working_dir.is_dir():
        print(f"Error: working_folder does not exist or is not a directory: {working_dir}")
        return 2

    output_dir = working_dir / "Output"
    picker = LatestOutputPicker()
    pick = picker.pick_latest(output_dir)

    article_md = pick.path.read_text(encoding="utf-8")
    if not article_md.strip():
        print(f"Error: latest article is empty: {pick.path}")
        return 2

    openai_model = (config.get("openai_model_prompt") or "gpt-4o-mini").strip()

    prompt_builder = ThumbnailPromptBuilder()
    prompt = prompt_builder.build_prompt(
        ThumbnailPromptRequest(
            article_markdown=article_md,
            model=openai_model,
        )
    )

    thumbnails_dir = working_dir / "Thumbnails"
    thumbnails_dir.mkdir(parents=True, exist_ok=True)

    # Use seconds in output filenames to avoid overwrites on quick re-generations.
    run_prefix = datetime.now().strftime("%Y-%m-%d %H_%M_%S")

    thumbnail_models = config.get("thumbnail_models")
    enabled_models: list[str] = []

    if isinstance(thumbnail_models, dict) and thumbnail_models:
        for model_id, enabled in thumbnail_models.items():
            if bool(enabled):
                enabled_models.append(str(model_id))
    else:
        # Backward compatible fallback
        enabled_models.append((config.get("openrouter_model_image") or "google/gemini-2.5-flash-image").strip())

    generator = OpenRouterImageGenerator()
    wrote_any = False

    for model_id in enabled_models:
        model_id = (model_id or "").strip()
        if not model_id:
            continue

        model_tag = _model_slug(model_id)
        base_name = f"{run_prefix} Thumbnail {model_tag}"

        prompt_path = thumbnails_dir / f"{base_name}.prompt.txt"
        prompt_path.write_text(prompt.strip() + "\n", encoding="utf-8")

        image = generator.generate(
            OpenRouterImageRequest(
                prompt=prompt,
                model=model_id,
                aspect_ratio="16:9",
            )
        )

        out_path = thumbnails_dir / f"{base_name}.{image.extension}"
        out_path.write_bytes(image.image_bytes)
        print(f"Wrote thumbnail: {out_path}")
        print(f"Wrote prompt: {prompt_path}")
        wrote_any = True

    if not wrote_any:
        print("No thumbnails generated (no enabled models in config).")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

