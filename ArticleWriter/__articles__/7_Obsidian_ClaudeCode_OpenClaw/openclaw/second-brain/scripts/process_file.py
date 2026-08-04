#!/usr/bin/env python3
"""Process an uploaded file (photo, PDF, doc) and return metadata for vault note creation."""

import json
import mimetypes
import os
import sys
from datetime import datetime


def classify_file(filepath: str) -> dict:
    """Determine file type and target subfolder."""
    mime, _ = mimetypes.guess_type(filepath)
    mime = mime or "application/octet-stream"
    name = os.path.basename(filepath)
    size_bytes = os.path.getsize(filepath) if os.path.isfile(filepath) else 0

    if mime.startswith("image/"):
        subfolder = "photos"
        file_type = "photo"
    elif mime == "application/pdf":
        subfolder = "docs"
        file_type = "pdf"
    elif mime in ("application/msword",
                  "application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
        subfolder = "docs"
        file_type = "document"
    elif mime.startswith("audio/"):
        subfolder = "voice"
        file_type = "audio"
    elif mime.startswith("video/"):
        subfolder = "video"
        file_type = "video"
    else:
        subfolder = "other"
        file_type = "file"

    return {
        "filename": name,
        "mime": mime,
        "file_type": file_type,
        "subfolder": subfolder,
        "size_bytes": size_bytes,
        "size_human": _human_size(size_bytes),
        "vault_path": f"50-Files/{subfolder}/{name}",
        "date": datetime.now().strftime("%Y-%m-%d"),
    }


def _human_size(nbytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if nbytes < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} TB"


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: process_file.py <filepath>"}))
        sys.exit(1)

    filepath = sys.argv[1].strip()
    if not os.path.isfile(filepath):
        print(json.dumps({"error": f"File not found: {filepath}"}))
        sys.exit(1)

    result = classify_file(filepath)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
