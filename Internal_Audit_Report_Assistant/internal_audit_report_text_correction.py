#!/usr/bin/env python3
"""
Internal Audit Report Text Correction
Reads config, connects to a Google Sheet, processes rows where filter column is 'x',
sends input column content to OpenRouter (prompt + input), writes LLM response to output column.
"""

import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

import gspread
from google.oauth2.service_account import Credentials

try:
    from colorama import Fore, Style, init as colorama_init
except ImportError:
    Fore = type("Fore", (), {"GREEN": "", "RED": "", "YELLOW": "", "CYAN": ""})()
    Style = type("Style", (), {"RESET_ALL": ""})()
    def colorama_init(*_args, **_kwargs):
        pass

colorama_init(autoreset=True)

REQUIRED_CONFIG_KEYS = [
    "iso_table_url",
    "iso_table_tab",
    "filter_column",
    "control_id_column",
    "control_title_column",
    "input_column",
    "output_column",
    "starting_row",
    "llm_model",
    "prompt",
]

COLUMN_TITLE_KEYS = [
    "filter_column",
    "control_id_column",
    "control_title_column",
    "input_column",
    "output_column",
]


def _success(msg: str) -> str:
    return f"{Fore.GREEN}{msg}{Style.RESET_ALL}"


def _error(msg: str) -> str:
    return f"{Fore.RED}{msg}{Style.RESET_ALL}"


def _info(msg: str) -> str:
    return f"{Fore.CYAN}{msg}{Style.RESET_ALL}"


def load_config(config_path: str) -> dict:
    """Load and validate config from JSON file."""
    path = Path(config_path)
    if not path.is_file():
        print(_error(f"Config file not found: {config_path}"))
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
    missing = [k for k in REQUIRED_CONFIG_KEYS if k not in config]
    if missing:
        print(_error(f"Config missing required keys: {missing}"))
        sys.exit(1)
    for key in COLUMN_TITLE_KEYS:
        if not isinstance(config.get(key), str):
            print(_error(f"Config key '{key}' must be a string (column title)."))
            sys.exit(1)
    if not isinstance(config.get("starting_row"), int) or config["starting_row"] < 1:
        print(_error("Config 'starting_row' must be a positive integer."))
        sys.exit(1)
    return config


def _setup_google_credentials():
    """Setup Google Sheets credentials (same pattern as Invoice_Generator)."""
    credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
    if not credentials_path:
        script_dir = Path(__file__).resolve().parent
        parent = script_dir.parent
        possible_paths = [
            parent / ".vscode" / "client_secret_1049835516666-5v9s988evv40904gof6p0i7l93f57go7.apps.googleusercontent.com.json",
            script_dir / "credentials.json",
            script_dir / "client_secret.json",
            Path.home() / ".config" / "gspread" / "credentials.json",
        ]
        for p in possible_paths:
            if p.exists():
                credentials_path = str(p)
                break
    if credentials_path and os.path.exists(credentials_path):
        try:
            script_dir = Path(__file__).resolve().parent
            parent = script_dir.parent
            authorized_user_paths = [
                parent / ".vscode" / "authorized_user.json",
                script_dir / "authorized_user.json",
                Path.home() / ".config" / "gspread" / "authorized_user.json",
            ]
            authorized_user_path = None
            for p in authorized_user_paths:
                if p.exists():
                    authorized_user_path = str(p)
                    break
            return gspread.oauth(
                credentials_filename=credentials_path,
                authorized_user_filename=authorized_user_path,
            )
        except Exception:
            try:
                scope = [
                    "https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive",
                ]
                creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
                return gspread.authorize(creds)
            except Exception:
                pass
    return gspread.oauth()


def _extract_spreadsheet_id(url: str) -> Optional[str]:
    pattern = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def resolve_column_indices(header_row: List[str], config: dict) -> Dict[str, int]:
    """Map config column titles to 0-based column indices. Fails if any title is missing."""
    header_stripped = [str(c).strip() for c in header_row]
    indices = {}
    for key in COLUMN_TITLE_KEYS:
        title = (config.get(key) or "").strip()
        try:
            idx = header_stripped.index(title)
        except ValueError:
            idx = -1
        if idx < 0:
            raise ValueError(f"Column title not found in header: {title!r}")
        indices[key] = idx
    return indices


def call_openrouter(api_key: str, model: str, user_content: str, timeout: int = 120) -> str:
    """Send user message to OpenRouter chat completions; return assistant content."""
    endpoint = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": user_content}],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read()
    parsed: Dict[str, Any] = json.loads(body.decode("utf-8"))
    choices = parsed.get("choices") or []
    if not choices:
        raise RuntimeError("OpenRouter returned no choices")
    msg = (choices[0] or {}).get("message") or {}
    content = msg.get("content")
    if not isinstance(content, str):
        raise RuntimeError("OpenRouter response had no text content")
    return content.strip()


def run(config_path: str) -> None:
    config = load_config(config_path)
    api_key = (os.getenv("OPENROUTER_API_KEY") or "").strip()
    if not api_key:
        print(_error("OPENROUTER_API_KEY is not set."))
        sys.exit(1)

    print(_info("Connecting to Google Sheets..."))
    try:
        gc = _setup_google_credentials()
    except Exception as e:
        print(_error(f"Google Sheets authentication failed: {e}"))
        sys.exit(1)

    sheet_id = _extract_spreadsheet_id(config["iso_table_url"])
    if not sheet_id:
        print(_error(f"Could not extract spreadsheet ID from: {config['iso_table_url']}"))
        sys.exit(1)

    try:
        spreadsheet = gc.open_by_key(sheet_id)
        worksheet = spreadsheet.worksheet(config["iso_table_tab"])
    except Exception as e:
        print(_error(f"Failed to open sheet/tab: {e}"))
        sys.exit(1)

    print(_info("Reading sheet data..."))
    all_values = worksheet.get_all_values()
    if not all_values:
        print(_error("Sheet is empty."))
        sys.exit(1)

    header_row = all_values[0]
    try:
        col = resolve_column_indices(header_row, config)
    except ValueError as e:
        print(_error(str(e)))
        sys.exit(1)

    start_row = config["starting_row"]
    if start_row < 1 or start_row > len(all_values):
        print(_error(f"starting_row {start_row} is out of range (1..{len(all_values)})."))
        sys.exit(1)

    data_rows = all_values[start_row - 1 :]
    processed = 0
    skipped = 0
    errors = 0

    for i, row in enumerate(data_rows):
        gspread_row = start_row + i
        filter_val = (row[col["filter_column"]] if col["filter_column"] < len(row) else "").strip()
        if filter_val != "x":
            skipped += 1
            continue
        input_val = (row[col["input_column"]] if col["input_column"] < len(row) else "").strip()
        if not input_val:
            print(_info(f"Row {gspread_row}: empty input, skipping."))
            skipped += 1
            continue

        control_id = row[col["control_id_column"]] if col["control_id_column"] < len(row) else ""
        control_title = row[col["control_title_column"]] if col["control_title_column"] < len(row) else ""
        title_preview = (control_title[:30] + "…") if len(control_title) > 30 else control_title
        print(_info(f"Row {gspread_row} (Control: {control_id} / {title_preview}): calling LLM..."))

        user_content = (config["prompt"] or "") + "\n\n" + input_val
        try:
            result = call_openrouter(api_key, config["llm_model"], user_content)
        except Exception as e:
            print(_error(f"Row {gspread_row}: LLM failed: {e}"))
            errors += 1
            try:
                worksheet.update_cell(gspread_row, col["output_column"] + 1, f"[Error: {e}]")
            except Exception:
                pass
            continue

        try:
            worksheet.update_cell(gspread_row, col["output_column"] + 1, result)
            print(_success(f"Row {gspread_row}: written."))
            processed += 1
        except Exception as e:
            print(_error(f"Row {gspread_row}: write failed: {e}"))
            errors += 1

        time.sleep(1)

    print(_info(f"Done. Processed: {processed}, skipped: {skipped}, errors: {errors}."))


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Internal audit report text correction via OpenRouter")
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parent / "config.json"),
        help="Path to JSON config (default: config.json in script directory)",
    )
    args = parser.parse_args()
    run(args.config)


if __name__ == "__main__":
    main()
