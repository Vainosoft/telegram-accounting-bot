import logging
import re
from typing import List

from aiogram import Dispatcher, Router, types
from aiogram.filters import Command

from ..google_sheets_client import GoogleSheetsClient

logger = logging.getLogger(__name__)
router = Router()

_sheets_client: GoogleSheetsClient | None = None


class IncomeValidationError(Exception):
    """Custom exception used when /income message validation fails."""
    pass


@router.message(Command("income"))
async def handle_income(message: types.Message) -> None:
    """
    Handle the /income command.

    The message is expected to contain 10 or 11 lines after the command.
    If validation succeeds, a new row is appended to the Income worksheet.
    """
    if _sheets_client is None:
        logger.error("GoogleSheetsClient is not initialized in income_handler.")
        await message.answer(
            "Error: internal configuration problem. Please contact the administrator."
        )
        return

    text = message.text or ""
    try:
        values = parse_income_message(text)
    except IncomeValidationError as e:
        # Validation error – send a clear message to the user
        await message.answer(str(e))
        return
    except Exception:
        # Unexpected error while parsing
        logger.exception("Unexpected error while parsing /income message")
        await message.answer(
            "Error: something went wrong while processing your /income message. "
            "Please check the format or try again later."
        )
        return

    try:
        _sheets_client.append_income_row(values)
    except Exception:
        logger.exception("Failed to append income row to Google Sheets")
        await message.answer(
            "Error: failed to write data to the spreadsheet. "
            "Please try again later or contact the administrator."
        )
        return

    # Success
    await message.answer("Done")


def parse_income_message(full_text: str) -> List[str]:
    """
    Parse and validate the full /income message text.

    Expected structure:
    /income
    1) Payment date
    2) Amount with currency
    3) Payment purpose
    4) Client full name
    5) Client date of birth
    6) Phone number
    7) Email
    8) Client status
    9) Country
    10) Manager
    11) Comment (optional)

    Returns:
        List of 11 strings (comment may be an empty string).

    Raises:
        IncomeValidationError: if any validation rule is violated.
    """
    lines = full_text.splitlines()

    if not lines:
        raise IncomeValidationError(
            "Error: the message is empty. Please send /income followed by the template."
        )

    # First line contains the command (/income); all subsequent lines are data
    body_lines = [line.strip() for line in lines[1:]]

    line_count = len(body_lines)

    if line_count < 10:
        raise IncomeValidationError(
            "Error: not enough lines for /income. Expected 10–11 lines after the command."
        )

    if line_count > 11:
        raise IncomeValidationError(
            "Error: only one income record is allowed per message. "
            "Remove extra lines and send a new message."
        )

    # If there are exactly 10 lines, add an empty comment line at the end
    if line_count == 10:
        body_lines.append("")
        line_count = 11

    # Now we must have exactly 11 lines
    assert line_count == 11

    # Validate required fields (lines 1–10)
    for i in range(10):
        if body_lines[i] == "":
            # Lines are 1-based for the user
            line_number = i + 1
            raise IncomeValidationError(
                f"Error: line {line_number} is required but empty. "
                "Please check the /income template and send the message again."
            )

    payment_date = body_lines[0]
    amount_with_currency = body_lines[1]

    # --- Validate date (line 1) ---
    if not _is_valid_date_format(payment_date):
        raise IncomeValidationError(
            "Error in line 1: payment date must be in format DD.MM.YY or DD.MM.YYYY."
        )

    # --- Validate amount with currency (line 2) ---
    if not _starts_with_number(amount_with_currency):
        raise IncomeValidationError(
            "Error in line 2: unable to parse amount. "
            "Examples: 500 USD, 500 EUR, 500.00 USD."
        )

    # All other fields are required but we do not enforce any specific formats for them
    return body_lines


def _is_valid_date_format(value: str) -> bool:
    """
    Check that the date is in one of the accepted formats:
    DD.MM.YY or DD.MM.YYYY
    """
    pattern = r"^\d{2}\.\d{2}\.\d{2}(\d{2})?$"
    return re.match(pattern, value) is not None


def _starts_with_number(value: str) -> bool:
    """
    Check that the string starts with a number (integer or decimal),
    optionally followed by any currency text.
    """
    value = value.strip()
    if not value:
        return False

    # Match at the beginning: digits, optional decimal part
    match = re.match(r"^\d+(?:[.,]\d+)?", value)
    return match is not None


def register_income_handlers(dp: Dispatcher, sheets_client: GoogleSheetsClient) -> None:
    """
    Register /income handlers on the given Dispatcher and
    store a reference to the GoogleSheetsClient instance.
    """
    global _sheets_client
    _sheets_client = sheets_client
    dp.include_router(router)
