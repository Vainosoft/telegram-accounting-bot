from aiogram import Dispatcher, Router, types
from aiogram.filters import CommandStart, Command

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    """
    Handle the /start command.

    Sends a short introduction and a list of available commands.
    """
    text = (
        "Welcome!\n"
        "This bot helps you track income and expenses in a shared Google Sheets document.\n\n"
        "Available commands:\n"
        "• /income – add a new income record\n"
        "• /expense – add a new expense record\n"
        "• /excel – get access to the spreadsheet\n"
        "• /help – show message formats and instructions"
    )
    await message.answer(text)


@router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    """
    Handle the /help command.

    Explains how to use /income and /expense commands and shows the expected templates.
    """
    text = (
        "Here is how to use the bot.\n\n"
        "<b>General rules</b>\n"
        "• One message always creates exactly one record in the spreadsheet.\n"
        "• The bot only appends rows and does not perform any calculations or currency conversion.\n\n"
        "<b>/income</b> – add a new income record\n"
        "The message after /income must contain 10 or 11 lines:\n"
        "1) Payment date (DD.MM.YY or DD.MM.YYYY)\n"
        "2) Amount with currency (e.g. 500 USD)\n"
        "3) Payment purpose\n"
        "4) Client full name\n"
        "5) Client date of birth\n"
        "6) Phone number\n"
        "7) Email\n"
        "8) Client status\n"
        "9) Country\n"
        "10) Manager\n"
        "11) Comment (optional)\n\n"
        "Example:\n"
        "<pre>/income\n"
        "24.12.2024\n"
        "500 USD\n"
        "Full payment for Vietnam program\n"
        "John Doe\n"
        "14.06.1986\n"
        "+1 555 123 456\n"
        "john.doe@example.com\n"
        "Returning client\n"
        "USA\n"
        "Kate\n"
        "Client asked for invoice copy</pre>\n\n"
        "<b>/expense</b> – add a new expense record\n"
        "The message after /expense must contain 6 or 7 lines:\n"
        "1) Date (DD.MM.YY or DD.MM.YYYY)\n"
        "2) Amount in USD (optional)\n"
        "3) Amount in EUR (optional)\n"
        "4) Amount in other currency (optional)\n"
        "5) Expense name\n"
        "6) Manager\n"
        "7) Comment (optional)\n\n"
        "At least one of lines 2–4 must contain a valid amount.\n\n"
        "Example:\n"
        "<pre>/expense\n"
        "24.12.2024\n"
        "319 USD\n"
        "276 EUR\n"
        "120000 KZT\n"
        "Salary payment for SMM specialist\n"
        "Kate\n"
        "Remaining amount will be paid next week</pre>"
    )

    await message.answer(text)


def register_service_commands(dp: Dispatcher) -> None:
    """
    Register service command handlers (such as /start and /help)
    on the given Dispatcher instance.
    """
    dp.include_router(router)
