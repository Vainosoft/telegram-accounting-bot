import logging
import re
from typing import List

from aiogram import Dispatcher, Router, types
from aiogram.filters import Command

from ..google_sheets_client import GoogleSheetsClient

logger = logging.getLogger(__name__)
router = Router()

_sheets_client: GoogleSheetsClient | None = None


class ExpenseValidationError(Exception):
    """Custom exception used when /expense message validation fails."""
    pass


@router.message(Command("expense"))
async def handle_expense(message: types.Message) -> None:
    """
    Handle the /expense command.

    The message is expected to contain 6 or 7 lines after the command.
    If validation succeeds, a new row is appended to the Expenses worksheet.
    """
    if _sheets_client is None:
        logger.error("GoogleSheetsClient is not initialized in expense_handler.")
        await message.answer(
            "Error: internal configuration problem. Please contact the administrator."
        )
        return

    text = message.text or ""
    try:
        values = parse_expense_message(text)
    except ExpenseValidationError as e:
        # Validation error – send a clear message to the user
        await message.answer(str(e))
        return
    except Exception:
        # Unexpected error while parsing
        logger.exception("Unexpected error while parsing /expense message")
        await message.answer(
            "Error: something went wrong while processing your /expense message. "
            "Please check the format or try again later."
        )
        return

    try:
        _sheets_client.append_expense_row(values)
    except Exception:
        logger.exception("Failed to append expense row to Google Sheets")
        await message.answer(
            "Error: failed to write data to the spreadsheet. "
            "Please try again later or contact the administrator."
        )
        return

    # Success
    await message.answer("Done")


def parse_expense_message(full_text: str) -> List[str]:
    """
    Parse and validate the full /expense message text.

    Expected structure:
    /expense
    1) Date
    2) Amount in USD (optional)
    3) Amount in EUR (optional)
    4) Amount in other currency (optional)
    5) Expense name
    6) Manager
    7) Comment (optional)

    Returns:
        List of 7 strings (comment may be an empty string).

    Raises:
        ExpenseValidationError: if any validation rule is violated.
    """
    lines = full_text.splitlines()

    if not lines:
        raise ExpenseValidationError(
            "Error: the message is empty. Please send /expense followed by the template."
        )

    # First line contains the command (/expense); all subsequent lines are data
    body_lines = [line.strip() for line in lines[1:]]

    line_count = len(body_lines)

    if line_count < 6:
        raise ExpenseValidationError(
            "Error: not enough lines for /expense. Expected 6–7 lines after the command."
        )

    if line_count > 7:
        raise ExpenseValidationError(
            "Error: only one expense record is allowed per message. "
            "Remove extra lines and send a new message."
        )

    # If there are exactly 6 lines, add an empty comment line at the end
    if line_count == 6:
        body_lines.append("")
        line_count = 7

    # Now we must have exactly 7 lines
    assert line_count == 7

    # Validate required fields:
    # line 1 (date), line 5 (expense name), line 6 (manager)
    required_indices = [0, 4, 5]
    for i in required_indices:
        if body_lines[i] == "":
            line_number = i + 1
            raise ExpenseValidationError(
                f"Error: line {line_number} is required but empty. "
                "Please check the /expense template and send the message again."
            )

    date_value = body_lines[0]
    amount_usd = body_lines[1]
    amount_eur = body_lines[2]
    amount_other = body_lines[3]

    # --- Validate date (line 1) ---
    if not _is_valid_date_format(date_value):
        raise ExpenseValidationError(
            "Error in line 1: date must be in format DD.MM.YY or DD.MM.YYYY."
        )

    # --- Validate amounts (lines 2–4) ---
    amount_lines = [amount_usd, amount_eur, amount_other]

    # Check that at least one of lines 2–4 contains a valid amount
    has_any_amount = any(
        line and _starts_with_number(line) for line in amount_lines
    )

    if not has_any_amount:
        raise ExpenseValidationError(
            "Error: no expense amount specified. Please fill at least one of lines 2–4."
        )

    # If a line is not empty but does not start with a number, it is invalid
    for index, value in enumerate(amount_lines, start=2):
        if value and not _starts_with_number(value):
            raise ExpenseValidationError(
                f"Error in line {index}: unable to parse amount. "
                "Examples: 319 USD, 276 EUR, 120000 KZT."
            )

    # All checks passed – return all 7 lines in order
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


def register_expense_handlers(dp: Dispatcher, sheets_client: GoogleSheetsClient) -> None:
    """
    Register /expense handlers on the given Dispatcher and
    store a reference to the GoogleSheetsClient instance.
    """
    global _sheets_client
    _sheets_client = sheets_client
    dp.include_router(router)
