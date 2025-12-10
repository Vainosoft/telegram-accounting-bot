# Telegram Accounting Bot

Telegram Accounting Bot is a simple Telegram bot that allows users to record **income** and **expense** operations into a shared **Google Sheets** document.

Each correctly formatted message in a Telegram group is converted into a single row in the corresponding Google Sheets worksheet (for example: `Income` and `Expenses`).

The project is intentionally minimal and focused on integration and data quality rather than analytics or automation.

---

## Features

- Record income using a dedicated text template (one message = one income record).
- Record expenses using a dedicated text template (one message = one expense record).
- Append rows to Google Sheets using a service account.
- Optional `/excel` command to share or export the spreadsheet.
- Basic validation of:
  - Number of lines in the message.
  - Required fields.
  - Date format.
  - At least one expense amount (for expenses).
- Clear success and error replies in chat.

> Note: All business logic, handlers, and examples are written in English in this repository to make the project easier to understand and reuse.

---

## Technology Stack

- **Language:** Python 3.x  
- **Telegram framework:** `aiogram` (or a similar Telegram bot library)  
- **Google Sheets integration:** Google Sheets API via `google-api-python-client` or `gspread`  
- **Runtime:** Any environment that can run Python (local machine, server, NAS, Docker)

---

## Repository Structure

```text
telegram-accounting-bot/
  README.md
  .gitignore
  requirements.txt

  src/
    __init__.py
    bot.py
    config.py
    google_sheets_client.py

    handlers/
      __init__.py
      income_handler.py
      expense_handler.py
      excel_handler.py
      service_commands.py

  docs/
    technical_specification.md
    project_chats.md

---

## Status

This repository contains a minimal implementation of a Telegram bot for tracking income and expenses in Google Sheets.

Current state:
- Command handlers for `/start`, `/help`, `/income`, `/expense` and `/excel` are implemented.
- Integration with Google Sheets via a service account is implemented in `google_sheets_client.py`.
- The code is structured as a small, clean example of how to combine Telegram bot logic with Google Sheets.

Additional testing, configuration and deployment steps may be required before using this bot in a real production environment.

