#!/usr/bin/env python3
"""
ArticleWriter - generate an article using OpenAI from crawled sources.

Usage:
  python ArticleWriter/write_article.py ArticleWriter/1_Arxio_NewOutlook.config
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import List

import json5

from model.openai_article_writer import ArticleWriteRequest, OpenAIArticleWriter


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


def _read_text(path: Path, label: str) -> str:
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def _load_sources(sources_dir: Path) -> List[str]:
    if not sources_dir.exists() or not sources_dir.is_dir():
        raise FileNotFoundError(f"Sources folder not found: {sources_dir}")

    md_files = sorted([p for p in sources_dir.glob("*.md") if p.is_file()])
    if not md_files:
        raise FileNotFoundError(f"No .md files found in Sources folder: {sources_dir}")

    sources: List[str] = []
    for p in md_files:
        text = p.read_text(encoding="utf-8").strip()
        if not text:
            continue
        sources.append(f"## {p.name}\n\n{text}")
    if not sources:
        raise ValueError(f"All source files were empty in: {sources_dir}")
    return sources


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an article from Sources/*.md using OpenAI.")
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

    system_prompt_path = working_dir / "system_prompt.txt"
    instructions_path = working_dir / "instructions.txt"
    sources_dir = working_dir / "Sources"

    try:
        system_prompt = _read_text(system_prompt_path, "system_prompt.txt")
        instructions = _read_text(instructions_path, "instructions.txt")
        sources_markdown = _load_sources(sources_dir)
    except Exception as e:
        print(f"Error preparing inputs:\n{e}")
        return 2

    model = (config.get("openai_model") or "gpt-4o-mini").strip()
    temperature = float(config.get("openai_temperature", 0.2))

    writer = OpenAIArticleWriter()
    article_md = writer.write_article(
        ArticleWriteRequest(
            system_prompt=system_prompt,
            sources_markdown=sources_markdown,
            instructions=instructions,
            model=model,
            temperature=temperature,
        )
    )

    output_dir = working_dir / "Output"
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = datetime.now().strftime("%Y-%m-%d %H_%M Article.md")
    out_path = output_dir / filename
    out_path.write_text(article_md.strip() + "\n", encoding="utf-8")

    print(f"Wrote article: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

