import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from .config import get_settings, Settings
from .google_sheets_client import GoogleSheetsClient


logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Application entry point.

    - Load settings from environment variables.
    - Configure logging.
    - Initialize the Telegram bot and dispatcher.
    - Initialize the Google Sheets client.
    - Register all handlers.
    - Start polling for updates.
    """
    settings: Settings = get_settings()

    # Configure root logger
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    logger.info("Starting Telegram Accounting Bot")

    # Initialize bot and dispatcher
    bot = Bot(token=settings.telegram_bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # Initialize Google Sheets client (shared for all handlers)
    sheets_client = GoogleSheetsClient.from_settings(settings)

    # Register handlers (will be implemented step by step)
    from .handlers import service_commands, income_handler, expense_handler, excel_handler

    service_commands.register_service_commands(dp)
    income_handler.register_income_handlers(dp, sheets_client)
    expense_handler.register_expense_handlers(dp, sheets_client)
    excel_handler.register_excel_handlers(dp, sheets_client)

    logger.info("Bot is running. Waiting for updates...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
