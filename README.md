# Telegram Accounting Bot

Telegram Accounting Bot is a minimal implementation of a Telegram bot that records **income** and **expense** operations into a shared **Google Sheets** document.

Each correctly formatted message in a Telegram group is converted into a single row in one of two worksheets:

* `Income` – for income records (command `/income`)
* `Expenses` – for expense records (command `/expense`)

The project focuses on clear structure, validation, and integration with Google Sheets.

---

## Overview

The bot is designed as a small, self-contained backend service that:

* Listens to messages in a Telegram chat.
* Supports commands for working with income, expenses, and the spreadsheet.
* Validates incoming messages using strict multi-line text templates.
* Appends rows to Google Sheets using a Google service account.

All code, documentation, identifiers, and bot messages in this repository are in English.

For detailed behavior, see the technical specification:

* `docs/technical_specification.md`

---

## Features

* `/income` – add a new income record using a 10–11 line template.
* `/expense` – add a new expense record using a 6–7 line template.
* `/excel` – get a link to the Google Sheets document.
* `/start` – introduction and command list.
* `/help` – explanation of message formats and basic rules.

Validation includes:

* Number of lines in the message after the command.
* Presence of all required fields.
* Date format (`DD.MM.YY` or `DD.MM.YYYY`).
* Amount format (must start with a number).
* For `/expense`: at least one amount field must be provided (USD/EUR/other).

On success, the bot writes a new row to Google Sheets and replies with:

```text
Done
```

---

## Commands

### `/start`

Shows a short introduction and the list of available commands.

### `/help`

Explains the general rules and shows the expected templates for `/income` and `/expense`.

### `/income`

Adds a new income record to the `Income` worksheet.

Expected message after the command:

```text
/income
1) Payment date (DD.MM.YY or DD.MM.YYYY)
2) Amount with currency (e.g. 500 USD)
3) Payment purpose
4) Client full name
5) Client date of birth
6) Phone number
7) Email
8) Client status
9) Country
10) Manager
11) Comment (optional)
```

### `/expense`

Adds a new expense record to the `Expenses` worksheet.

Expected message after the command:

```text
/expense
1) Date (DD.MM.YY or DD.MM.YYYY)
2) Amount in USD (optional)
3) Amount in EUR (optional)
4) Amount in other currency (optional)
5) Expense name
6) Manager
7) Comment (optional)
```

At least one of lines 2–4 must contain a valid amount.

### `/excel`

Returns a link to the Google Sheets document used for accounting.

---

## Data Model

The bot writes data to a single Google Sheets document with two worksheets:

* `Income` – one row per `/income` message.
* `Expenses` – one row per `/expense` message.

Columns for each sheet and detailed validation rules are described in:

* `docs/technical_specification.md`

---

## Technology Stack

* **Language:** Python 3.x
* **Telegram framework:** `aiogram`
* **Google Sheets integration:** `gspread` + `google-auth` (service account)
* **Configuration:** environment variables (optionally via `.env` and `python-dotenv`)
* **Runtime:** any environment that can run Python (local machine, server, NAS, Docker, etc.)

---

## Project Structure

```text
telegram-accounting-bot/
  README.md
  .gitignore
  .env.example
  requirements.txt
  LICENSE

  src/
    __init__.py
    bot.py
    config.py
    google_sheets_client.py

    handlers/
      __init__.py
      service_commands.py   # /start and /help
      income_handler.py     # /income
      expense_handler.py    # /expense
      excel_handler.py      # /excel

  docs/
    technical_specification.md
    project_chats.md
```

* `src/bot.py` – application entry point: settings, logging, bot initialization, handler registration.
* `src/config.py` – loading configuration from environment variables.
* `src/google_sheets_client.py` – wrapper around Google Sheets API (append rows, get spreadsheet URL).
* `src/handlers/` – Telegram message handlers for each command.
* `docs/technical_specification.md` – detailed technical specification in English.
* `docs/project_chats.md` – description of the original project chat structure.

---

## Configuration

Configuration is provided through environment variables.
An example file `.env.example` is included:

```env
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE
GOOGLE_SERVICE_ACCOUNT_JSON=./service_account.json
SPREADSHEET_ID=YOUR_SPREADSHEET_ID_HERE
INCOME_SHEET_NAME=Income
EXPENSES_SHEET_NAME=Expenses
LOG_LEVEL=INFO
```

Typical variables:

* `TELEGRAM_BOT_TOKEN` – Telegram bot token from BotFather.
* `GOOGLE_SERVICE_ACCOUNT_JSON` – path to the Google service account JSON file.
* `SPREADSHEET_ID` – ID of the target Google Sheets document.
* `INCOME_SHEET_NAME` – name of the income worksheet (default: `Income`).
* `EXPENSES_SHEET_NAME` – name of the expenses worksheet (default: `Expenses`).
* `LOG_LEVEL` – logging level (e.g. `INFO`, `DEBUG`).

---

## Usage (conceptual)

To run the bot in a real environment, you would typically:

1. Create a `.env` file based on `.env.example` and fill in:

   * `TELEGRAM_BOT_TOKEN`
   * `GOOGLE_SERVICE_ACCOUNT_JSON`
   * `SPREADSHEET_ID`
2. Create or configure the Google Sheets document with `Income` and `Expenses` worksheets.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Start the bot, for example:

   ```bash
   python -m src.bot
   ```

Exact steps may vary depending on the hosting and deployment setup.

---

## Status

This repository contains a minimal implementation of a Telegram bot that integrates with Google Sheets:

* Command handlers for `/start`, `/help`, `/income`, `/expense` and `/excel` are implemented.
* Google Sheets integration using a service account is implemented.
* The code is structured as a small, clear example of combining a Telegram bot with Google Sheets.

Additional configuration, testing and deployment work may be required before using this bot in a real production environment.

---

## License

This project is intended to be used under the MIT License.
The `LICENSE` file can contain the full MIT license text.
