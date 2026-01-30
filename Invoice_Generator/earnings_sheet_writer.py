#!/usr/bin/env python3
"""
Earnings Sheet Writer
Prompts the user (Y/n) to append one row to the overall earnings Google Sheet.
"""

import os
import re
from typing import Optional

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


def _success(msg: str) -> str:
    return f"{Fore.GREEN}{msg}{Style.RESET_ALL}"


def _error(msg: str) -> str:
    return f"{Fore.RED}{msg}{Style.RESET_ALL}"


def _prompt(msg: str) -> str:
    return f"{Fore.CYAN}{msg}{Style.RESET_ALL}"


class EarningsSheetWriter:
    """
    Appends one earnings row to a Google Sheet after prompting the user (Y/n).
    Uses GOOGLE_DOC_EARNINGS_LINK (spreadsheet URL with optional gid) and
    same auth pattern as GoogleDocReader.
    """

    def __init__(
        self,
        config: dict,
        last_month_str: str,
        money_no_vat: float,
        vat_amount: float,
        money_total: float,
        currency: str,
        today_yyyymmdd: str,
        pay_by_yyyymmdd: str,
    ):
        self.config = config
        self.last_month_str = last_month_str
        self.money_no_vat = money_no_vat
        self.vat_amount = vat_amount
        self.money_total = money_total
        self.currency = currency
        self.today_yyyymmdd = today_yyyymmdd
        self.pay_by_yyyymmdd = pay_by_yyyymmdd
        self._gc = None

    def _setup_credentials(self) -> bool:
        """Setup Google Sheets credentials (same pattern as GoogleDocReader)."""
        try:
            credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
            if not credentials_path:
                possible_paths = [
                    os.path.join(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        ".vscode",
                        "client_secret_1049835516666-5v9s988evv40904gof6p0i7l93f57go7.apps.googleusercontent.com.json",
                    ),
                    "credentials.json",
                    "client_secret.json",
                    os.path.expanduser("~/.config/gspread/credentials.json"),
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        credentials_path = path
                        break

            if credentials_path and os.path.exists(credentials_path):
                try:
                    authorized_user_paths = [
                        ".vscode/authorized_user.json",
                        "authorized_user.json",
                        os.path.expanduser("~/.config/gspread/authorized_user.json"),
                    ]
                    authorized_user_path = None
                    for path in authorized_user_paths:
                        if os.path.exists(path):
                            authorized_user_path = path
                            break
                    self._gc = gspread.oauth(
                        credentials_filename=credentials_path,
                        authorized_user_filename=authorized_user_path,
                    )
                    return True
                except Exception:
                    try:
                        scope = [
                            "https://spreadsheets.google.com/feeds",
                            "https://www.googleapis.com/auth/drive",
                        ]
                        creds = Credentials.from_service_account_file(
                            credentials_path, scopes=scope
                        )
                        self._gc = gspread.authorize(creds)
                        return True
                    except Exception:
                        pass

            self._gc = gspread.oauth()
            return True
        except Exception:
            self._gc = None
            return False

    @staticmethod
    def _extract_spreadsheet_id(url: str) -> Optional[str]:
        """Extract spreadsheet ID from Google Sheets URL."""
        pattern = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"
        match = re.search(pattern, url)
        return match.group(1) if match else None

    @staticmethod
    def _extract_worksheet_gid(url: str) -> Optional[int]:
        """Extract worksheet gid from URL (e.g. gid=1398966721 or #gid=1398966721)."""
        # Try gid=... first (query string), then #gid=... (fragment)
        for pattern in [r"[?&]gid=(\d+)", r"#gid=(\d+)"]:
            match = re.search(pattern, url)
            if match:
                return int(match.group(1))
        return None

    def _get_worksheet(self, url: str):
        """Open spreadsheet by key and return worksheet by gid, or first sheet if no gid."""
        if not self._gc:
            return None
        sheet_id = self._extract_spreadsheet_id(url)
        if not sheet_id:
            return None
        spreadsheet = self._gc.open_by_key(sheet_id)
        gid = self._extract_worksheet_gid(url)
        if gid is not None:
            for ws in spreadsheet.worksheets():
                if ws.id == gid:
                    return ws
            return None
        return spreadsheet.sheet1

    def _find_next_free_row(self, sheet) -> int:
        """Return 1-based row number of first empty cell in column A."""
        try:
            col_a = sheet.col_values(1)
            for i, cell in enumerate(col_a):
                if not (cell and str(cell).strip()):
                    return i + 1
            return len(col_a) + 1
        except Exception:
            return 1

    def run(self) -> None:
        """
        Prompt user (Y/n); if yes, append one row to the earnings sheet.
        Does not exit the process on missing URL or write errors.
        """
        try:
            response = input(
                _prompt("Add row to overall list of earnings? (Y/n): ")
            ).strip().lower()
            if response in ("n", "no"):
                return

            url = os.getenv("GOOGLE_DOC_EARNINGS_LINK")
            if not url:
                print(_error("GOOGLE_DOC_EARNINGS_LINK is not set. Skipping earnings row."))
                return

            if not self._gc and not self._setup_credentials():
                print(_error("Could not authenticate with Google Sheets. Skipping earnings row."))
                return

            sheet = self._get_worksheet(url)
            if not sheet:
                print(_error("Could not open earnings sheet (check URL and gid). Skipping."))
                return

            row_index = self._find_next_free_row(sheet)
            gsheet_name = self.config.get("GSheet", "")
            row_values = [
                gsheet_name,
                f"{self.last_month_str} - Varia",
                self.money_no_vat,
                self.vat_amount,
                self.money_total,
                self.currency,
                self.today_yyyymmdd,
                self.pay_by_yyyymmdd,
            ]
            range_a1 = f"A{row_index}:H{row_index}"
            sheet.update(range_a1, [row_values], value_input_option="USER_ENTERED")
            print(_success("Earnings row added successfully."))
        except Exception as e:
            print(_error(f"Failed to add earnings row: {e}"))
