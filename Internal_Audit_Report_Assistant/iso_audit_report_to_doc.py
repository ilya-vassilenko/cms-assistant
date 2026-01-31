#!/usr/bin/env python3
"""
ISO 27001 Audit Report to Google Doc
Reads main requirements and controls tabs from a Google Sheet (columns by title, filter = 'x'),
then writes two bullet lists to a Google Doc with "ID Title:" in bold and observation after.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

try:
    from colorama import Fore, Style, init as colorama_init
except ImportError:
    Fore = type("Fore", (), {"GREEN": "", "RED": "", "YELLOW": "", "CYAN": ""})()
    Style = type("Style", (), {"RESET_ALL": ""})()
    def colorama_init(*_args, **_kwargs):
        pass

colorama_init(autoreset=True)

# OAuth scopes: Sheets + Drive + Docs (for writing to Google Doc)
OAUTH_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

SECTION_COLUMN_KEYS = ["id_column", "title_column", "observation_column", "filter_column"]


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
    required_top = ["google_sheet_url", "google_doc_url", "main_requirements", "controls"]
    missing = [k for k in required_top if k not in config]
    if missing:
        print(_error(f"Config missing required keys: {missing}"))
        sys.exit(1)
    for section_key in ["main_requirements", "controls"]:
        section = config[section_key]
        if not isinstance(section, dict):
            print(_error(f"Config '{section_key}' must be an object."))
            sys.exit(1)
        for col_key in SECTION_COLUMN_KEYS + ["tab"]:
            if col_key not in section:
                print(_error(f"Config '{section_key}.{col_key}' is required."))
                sys.exit(1)
            if col_key != "tab" and (not isinstance(section.get(col_key), str) or not section[col_key].strip()):
                print(_error(f"Config '{section_key}.{col_key}' must be a non-empty string (column title)."))
                sys.exit(1)
    return config


def _setup_credentials():
    """Setup Google credentials with Sheets + Docs scope; returns (gspread_client, credentials)."""
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
            gc = gspread.oauth(
                credentials_filename=credentials_path,
                authorized_user_filename=authorized_user_path,
                scopes=OAUTH_SCOPES,
            )
            return gc, gc.auth
        except Exception:
            try:
                scope = [
                    "https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive",
                    "https://www.googleapis.com/auth/documents",
                ]
                creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
                gc = gspread.authorize(creds)
                return gc, creds
            except Exception:
                pass
    gc = gspread.oauth(scopes=OAUTH_SCOPES)
    return gc, gc.auth


def _extract_spreadsheet_id(url: str) -> Optional[str]:
    pattern = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def _extract_document_id(url: str) -> Optional[str]:
    pattern = r"/document/d/([a-zA-Z0-9-_]+)"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def resolve_section_columns(header_row: List[str], section: dict) -> Dict[str, int]:
    """Map section column titles to 0-based indices. Fails if any title is missing."""
    header_stripped = [str(c).strip() for c in header_row]
    indices = {}
    for key in SECTION_COLUMN_KEYS:
        title = (section.get(key) or "").strip()
        try:
            idx = header_stripped.index(title)
        except ValueError:
            idx = -1
        if idx < 0:
            raise ValueError(f"Column title not found in header: {title!r}")
        indices[key] = idx
    return indices


def collect_filtered_rows(
    all_values: List[List[Any]],
    section: dict,
    col: Dict[str, int],
) -> List[Tuple[str, str, str]]:
    """From row 2 onward, filter where filter_column == 'x'; return list of (id, title, observation)."""
    result = []
    for row in all_values[1:]:
        raw = row[col["filter_column"]] if col["filter_column"] < len(row) else ""
        filter_val = str(raw).strip() if raw is not None else ""
        if filter_val.lower() != "x":
            continue
        id_val = (row[col["id_column"]] if col["id_column"] < len(row) else "").strip()
        title_val = (row[col["title_column"]] if col["title_column"] < len(row) else "").strip()
        obs_val = (row[col["observation_column"]] if col["observation_column"] < len(row) else "").strip()
        result.append((id_val, title_val, obs_val))
    return result


# Control ID prefix -> section title (order: A.5, A.6, A.7, A.8)
CONTROL_SECTIONS = [
    ("A.5", "Organizational controls:"),
    ("A.6", "People-related controls:"),
    ("A.7", "Physical controls:"),
    ("A.8", "Technological controls:"),
]


def _group_controls_by_prefix(
    control_items: List[Tuple[str, str, str]],
) -> List[Tuple[str, List[Tuple[str, str, str]]]]:
    """Group (id, title, obs) by A.5, A.6, A.7, A.8; then append 'Other' for non-matching."""
    groups: Dict[str, List[Tuple[str, str, str]]] = {prefix: [] for prefix, _ in CONTROL_SECTIONS}
    groups["_other"] = []
    for item in control_items:
        id_val = (item[0] or "").strip()
        placed = False
        for prefix, _ in CONTROL_SECTIONS:
            if id_val.startswith(prefix):
                groups[prefix].append(item)
                placed = True
                break
        if not placed:
            groups["_other"].append(item)
    result: List[Tuple[str, List[Tuple[str, str, str]]]] = []
    for prefix, title in CONTROL_SECTIONS:
        if groups[prefix]:
            result.append((title, groups[prefix]))
    if groups["_other"]:
        result.append(("Other controls:", groups["_other"]))
    return result


def _write_doc_content(
    docs_service: Any,
    document_id: str,
    main_items: List[Tuple[str, str, str]],
    control_items: List[Tuple[str, str, str]],
) -> None:
    """Replace document body: main requirements with heading, then control sections by A.5/A.6/A.7/A.8; 'ID Title:' in bold."""
    main_heading = "Main requirements of the ISO 27001:2022:\n\n"
    control_sections = _group_controls_by_prefix(control_items)

    parts: List[str] = [main_heading]
    for (id_val, title_val, obs_val) in main_items:
        parts.append(f"{id_val} {title_val}: {obs_val}\n")
    for section_title, items in control_sections:
        parts.append(f"\n{section_title}\n\n")
        for (id_val, title_val, obs_val) in items:
            parts.append(f"{id_val} {title_val}: {obs_val}\n")
    text = "".join(parts)

    doc = docs_service.documents().get(documentId=document_id).execute()
    body = doc.get("body", {})
    content = body.get("content", [])
    if not content:
        body_end = 1
    else:
        body_end = content[-1].get("endIndex", 1)

    requests: List[Dict[str, Any]] = []
    if body_end > 2:
        requests.append({"deleteContentRange": {"range": {"startIndex": 1, "endIndex": body_end - 1}}})
    requests.append({"insertText": {"location": {"index": 1}, "text": text}})

    pos = 1
    bullet_ranges: List[Tuple[int, int]] = []
    bold_ranges: List[Tuple[int, int]] = []

    pos += len(main_heading)
    for (id_val, title_val, obs_val) in main_items:
        line = f"{id_val} {title_val}: {obs_val}\n"
        start = pos
        end = pos + len(line)
        bullet_ranges.append((start, end))
        bold_end = start + len(id_val) + 1 + len(title_val) + 2
        bold_ranges.append((start, bold_end))
        pos = end
    for section_title, items in control_sections:
        pos += len(f"\n{section_title}\n\n")
        for (id_val, title_val, obs_val) in items:
            line = f"{id_val} {title_val}: {obs_val}\n"
            start = pos
            end = pos + len(line)
            bullet_ranges.append((start, end))
            bold_end = start + len(id_val) + 1 + len(title_val) + 2
            bold_ranges.append((start, bold_end))
            pos = end

    for start, end in bullet_ranges:
        requests.append({
            "createParagraphBullets": {
                "range": {"startIndex": start, "endIndex": end},
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
            }
        })
    for start, end in bold_ranges:
        requests.append({
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "textStyle": {"bold": True},
                "fields": "bold",
            }
        })

    docs_service.documents().batchUpdate(documentId=document_id, body={"requests": requests}).execute()


def run(config_path: str) -> None:
    config = load_config(config_path)
    print(_info("Connecting to Google Sheets..."))
    try:
        gc, creds = _setup_credentials()
    except Exception as e:
        print(_error(f"Google authentication failed: {e}"))
        sys.exit(1)

    sheet_id = _extract_spreadsheet_id(config["google_sheet_url"])
    if not sheet_id:
        print(_error(f"Could not extract spreadsheet ID from: {config['google_sheet_url']}"))
        sys.exit(1)

    try:
        spreadsheet = gc.open_by_key(sheet_id)
    except Exception as e:
        print(_error(f"Failed to open spreadsheet: {e}"))
        sys.exit(1)

    main_section = config["main_requirements"]
    control_section = config["controls"]

    print(_info("Reading main requirements tab..."))
    try:
        ws_main = spreadsheet.worksheet(main_section["tab"])
    except Exception as e:
        print(_error(f"Failed to open worksheet {main_section['tab']!r}: {e}"))
        sys.exit(1)
    all_main = ws_main.get_all_values()
    if not all_main:
        print(_error("Main requirements sheet is empty."))
        sys.exit(1)
    try:
        col_main = resolve_section_columns(all_main[0], main_section)
    except ValueError as e:
        print(_error(str(e)))
        sys.exit(1)
    main_items = collect_filtered_rows(all_main, main_section, col_main)
    print(_success(f"Main requirements: {len(main_items)} filtered rows."))

    print(_info("Reading controls tab..."))
    try:
        ws_control = spreadsheet.worksheet(control_section["tab"])
    except Exception as e:
        print(_error(f"Failed to open worksheet {control_section['tab']!r}: {e}"))
        sys.exit(1)
    all_control = ws_control.get_all_values()
    if not all_control:
        print(_error("Controls sheet is empty."))
        sys.exit(1)
    try:
        col_control = resolve_section_columns(all_control[0], control_section)
    except ValueError as e:
        print(_error(str(e)))
        sys.exit(1)
    control_items = collect_filtered_rows(all_control, control_section, col_control)
    print(_success(f"Controls: {len(control_items)} filtered rows."))

    doc_id = _extract_document_id(config["google_doc_url"])
    if not doc_id:
        print(_error(f"Could not extract document ID from: {config['google_doc_url']}"))
        sys.exit(1)

    print(_info("Writing to Google Doc..."))
    try:
        docs_service = build("docs", "v1", credentials=creds)
        _write_doc_content(docs_service, doc_id, main_items, control_items)
    except Exception as e:
        print(_error(f"Failed to update Google Doc: {e}"))
        sys.exit(1)
    print(_success("Google Doc updated."))


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="ISO 27001 audit report: Sheet to Google Doc bullet lists")
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parent / "config_iso_audit.json"),
        help="Path to JSON config (default: config_iso_audit.json in script directory)",
    )
    args = parser.parse_args()
    run(args.config)


if __name__ == "__main__":
    main()
