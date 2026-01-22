#!/usr/bin/env python3
"""
doc_to_html.py

Utility to extract/produce HTML from inputs that are stored with a .doc extension.

Common case in this repo: a Confluence export saved as ".doc" that is actually a MIME message
with an embedded text/html part.

Behavior:
- If input is MIME/multipart and contains a text/html part -> extract it and save as .html
- Else if input looks like HTML text already -> save as .html
- Else (likely a real legacy binary .doc) -> optionally attempt LibreOffice conversion when --libreoffice is set
"""

from __future__ import annotations

import argparse
import subprocess
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Optional


def try_extract_html_from_mime_message(path: Path) -> Optional[str]:
    try:
        raw = path.read_bytes()
        msg = BytesParser(policy=policy.default).parsebytes(raw)
        if not msg.is_multipart():
            return None
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                html = part.get_content()  # handles charset + quoted-printable/base64
                if isinstance(html, str) and "<html" in html.lower():
                    return html
        return None
    except Exception:
        return None


def looks_like_html_text(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:4096].lower()
        return "<html" in head or "<!doctype html" in head
    except Exception:
        return False


def convert_with_libreoffice_to_html(source: Path, output_dir: Path, *, soffice: str = "soffice") -> bool:
    """
    Best-effort conversion for real Word docs using LibreOffice.
    """
    cmd = [soffice, "--headless", "--convert-to", "html", "--outdir", str(output_dir), str(source)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, check=False)
    if result.returncode != 0:
        print("LibreOffice conversion failed.")
        print("cmd:", " ".join(cmd))
        if result.stdout:
            print("stdout:", result.stdout.strip())
        if result.stderr:
            print("stderr:", result.stderr.strip())
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract HTML from .doc-like inputs (Confluence exports).")
    parser.add_argument("--input", required=True, help="Path to input file (often .doc)")
    parser.add_argument(
        "--output-dir",
        default="Policy_Adjustment/data/NewNow/html",
        help="Directory to write the extracted HTML file into",
    )
    parser.add_argument(
        "--libreoffice",
        action="store_true",
        help="If no HTML is extractable, try converting via LibreOffice (soffice) to HTML",
    )
    parser.add_argument("--soffice", default="soffice", help="Path/command for LibreOffice (default: soffice)")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise SystemExit(f"Input does not exist: {input_path}")

    html = try_extract_html_from_mime_message(input_path)
    if html is not None:
        out_path = output_dir / f"{input_path.stem}.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"Extracted MIME text/html -> {out_path}")
        return

    if looks_like_html_text(input_path):
        out_path = output_dir / f"{input_path.stem}.html"
        # Normalize encoding by re-writing as utf-8.
        text = input_path.read_text(encoding="utf-8", errors="ignore")
        out_path.write_text(text, encoding="utf-8")
        print(f"Input already looks like HTML -> {out_path}")
        return

    if args.libreoffice:
        ok = convert_with_libreoffice_to_html(input_path, output_dir, soffice=args.soffice)
        if ok:
            print(f"LibreOffice conversion produced HTML in: {output_dir}")
            return

    raise SystemExit(
        "Could not extract HTML from input. If this is a real Word .doc, re-run with --libreoffice "
        "(requires a working LibreOffice/soffice)."
    )


if __name__ == "__main__":
    main()

