from dataclasses import dataclass
from typing import List

import gspread
from google.oauth2.service_account import Credentials

from .config import Settings, get_settings


# Scopes required to access Google Sheets and (optionally) Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@dataclass
class GoogleSheetsClient:
    """
    Simple wrapper around the Google Sheets API for this project.

    Responsibilities:
    - Authenticate using a service account JSON file.
    - Open the target spreadsheet by its ID.
    - Append rows to the Income and Expenses worksheets.
    """

    settings: Settings
    client: gspread.Client
    spreadsheet: gspread.Spreadsheet

    @classmethod
    def from_settings(cls, settings: Settings) -> "GoogleSheetsClient":
        """
        Factory method that creates a GoogleSheetsClient instance
        from a Settings object.
        """
        credentials = Credentials.from_service_account_file(
            settings.google_service_account_json,
            scopes=SCOPES,
        )
        gc = gspread.authorize(credentials)
        spreadsheet = gc.open_by_key(settings.spreadsheet_id)

        return cls(
            settings=settings,
            client=gc,
            spreadsheet=spreadsheet,
        )

    @classmethod
    def default(cls) -> "GoogleSheetsClient":
        """
        Factory method that loads settings from environment variables
        and creates a GoogleSheetsClient instance.
        """
        settings = get_settings()
        return cls.from_settings(settings)

    # --- Public methods for appending rows ---

    def append_income_row(self, values: List[str]) -> None:
        """
        Append a new row to the Income worksheet.

        :param values: List of cell values as strings, in the expected column order.
        """
        self._append_row(self.settings.income_sheet_name, values)

    def append_expense_row(self, values: List[str]) -> None:
        """
        Append a new row to the Expenses worksheet.

        :param values: List of cell values as strings, in the expected column order.
        """
        self._append_row(self.settings.expenses_sheet_name, values)

    # --- Optional helpers ---

    def get_spreadsheet_url(self) -> str:
        """
        Return the public URL of the spreadsheet.

        This is useful for the /excel command when we just want to
        send a link to the users instead of exporting a file.
        """
        return self.spreadsheet.url

    # --- Internal helpers ---

    def _append_row(self, sheet_name: str, values: List[str]) -> None:
        """
        Append a row of values to the given worksheet.

        :param sheet_name: Name of the worksheet (tab) in the spreadsheet.
        :param values: List of cell values as strings.
        """
        worksheet = self.spreadsheet.worksheet(sheet_name)
        # USER_ENTERED makes Google Sheets interpret numbers and dates naturally
        worksheet.append_row(values, value_input_option="USER_ENTERED")
