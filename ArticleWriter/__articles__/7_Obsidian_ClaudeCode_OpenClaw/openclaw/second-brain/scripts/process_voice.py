#!/usr/bin/env python3
"""Transcribe an audio file via OpenAI Whisper API, then summarize and tag."""

import json
import os
import subprocess
import sys

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
MODEL_WHISPER = "whisper-1"
MODEL_CHAT = "gpt-4o-mini"


def transcribe(audio_path: str) -> str:
    """Send audio to OpenAI Whisper API and return transcription text."""
    if not OPENAI_API_KEY:
        return "(transcription unavailable — no OPENAI_API_KEY)"

    try:
        result = subprocess.run(
            ["curl", "-s", "https://api.openai.com/v1/audio/transcriptions",
             "-H", f"Authorization: Bearer {OPENAI_API_KEY}",
             "-F", f"file=@{audio_path}",
             "-F", f"model={MODEL_WHISPER}",
             "-F", "response_format=json"],
            capture_output=True, text=True, timeout=120,
        )
        response = json.loads(result.stdout)
        return response.get("text", "(empty transcription)")
    except Exception as exc:
        return f"(transcription failed: {exc})"


def summarize_transcription(text: str) -> dict:
    """Summarize and tag the transcription via ChatGPT."""
    if not OPENAI_API_KEY or text.startswith("("):
        return {"summary": text[:200], "tags": ["voice"]}

    prompt = f"""Analyze this voice note transcription and return JSON with:
- "summary": a 1-2 sentence summary
- "tags": 2-5 lowercase single-word topic tags

Transcription:
{text[:6000]}"""

    payload = {
        "model": MODEL_CHAT,
        "messages": [
            {"role": "system", "content": "You are a concise knowledge-base assistant. Return only valid JSON."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 200,
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
        import re
        content = response["choices"][0]["message"]["content"]
        content = re.sub(r"```json\s*", "", content)
        content = re.sub(r"```\s*$", "", content)
        return json.loads(content)
    except Exception:
        return {"summary": text[:200] + "...", "tags": ["voice"]}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: process_voice.py <audio_file_path>"}))
        sys.exit(1)

    audio_path = sys.argv[1].strip()
    if not os.path.isfile(audio_path):
        print(json.dumps({"error": f"File not found: {audio_path}"}))
        sys.exit(1)

    transcription = transcribe(audio_path)
    analysis = summarize_transcription(transcription)

    result = {
        "transcription": transcription,
        "summary": analysis.get("summary", ""),
        "tags": analysis.get("tags", ["voice"]),
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
