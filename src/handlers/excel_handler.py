import logging

from aiogram import Dispatcher, Router, types
from aiogram.filters import Command

from ..google_sheets_client import GoogleSheetsClient

logger = logging.getLogger(__name__)
router = Router()

_sheets_client: GoogleSheetsClient | None = None


@router.message(Command("excel"))
async def handle_excel(message: types.Message) -> None:
    """
    Handle the /excel command.

    For the MVP we simply send a link to the Google Sheets document.
    If needed, this can later be extended to generate and send
    an exported file (e.g. XLSX or CSV).
    """
    if _sheets_client is None:
        logger.error("GoogleSheetsClient is not initialized in excel_handler.")
        await message.answer(
            "Error: internal configuration problem. Please contact the administrator."
        )
        return

    try:
        url = _sheets_client.get_spreadsheet_url()
    except Exception:
        logger.exception("Failed to get spreadsheet URL from Google Sheets client")
        await message.answer(
            "Error: unable to access the spreadsheet. "
            "Please contact the administrator."
        )
        return

    text = (
        "Here is the link to the accounting spreadsheet:\n"
        f"{url}"
    )
    await message.answer(text)


def register_excel_handlers(dp: Dispatcher, sheets_client: GoogleSheetsClient) -> None:
    """
    Register /excel handlers on the given Dispatcher and
    store a reference to the GoogleSheetsClient instance.
    """
    global _sheets_client
    _sheets_client = sheets_client
    dp.include_router(router)
