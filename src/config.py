import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    telegram_bot_token: str
    google_service_account_json: str
    spreadsheet_id: str

    income_sheet_name: str = "Income"
    expenses_sheet_name: str = "Expenses"

    log_level: str = "INFO"


def _get_env(name: str, default: Optional[str] = None, required: bool = False) -> str:
    """
    Helper function to read environment variables.

    :param name: Name of the environment variable.
    :param default: Default value if the variable is not set.
    :param required: If True, raise an error when the variable is missing.
    :return: The environment variable value as a string.
    """
    value = os.getenv(name, default)

    if required and not value:
        raise RuntimeError(f"Environment variable '{name}' is required but not set.")

    if value is None:
        # Normalize None to empty string when not required
        return ""

    return value


def get_settings() -> Settings:
    """
    Create and return a Settings instance using environment variables.

    This function can be imported and reused across the project.
    """
    return Settings(
        telegram_bot_token=_get_env("TELEGRAM_BOT_TOKEN", required=True),
        google_service_account_json=_get_env("GOOGLE_SERVICE_ACCOUNT_JSON", required=True),
        spreadsheet_id=_get_env("SPREADSHEET_ID", required=True),
        income_sheet_name=_get_env("INCOME_SHEET_NAME", default="Income"),
        expenses_sheet_name=_get_env("EXPENSES_SHEET_NAME", default="Expenses"),
        log_level=_get_env("LOG_LEVEL", default="INFO"),
    )
