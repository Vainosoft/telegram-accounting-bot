# Project Chats Overview

This project was originally designed and discussed using several separate “project chats”, each with a clear role and scope.  
This document summarizes those chats and their purpose in English.

---

## 00_director – Project director

- **Chat ID:** `00_director`
- **Role:** Project director / coordinator
- **Scope:**
  - Define the overall vision and goals of the Telegram Accounting Bot.
  - Choose the technology stack and key tools.
  - Decide on the structure of all project chats.
  - Approve important business and architecture decisions.
- **Notes:**
  - This chat keeps the “big picture” of the project.
  - All other chats are more technical and focused.

---

## 01_requirements_and_ux – Requirements & UX

- **Chat ID:** `01_requirements_and_ux`
- **Role:** Requirements, UX, and message formats
- **Scope:**
  - Define commands: `/income`, `/expense`, `/excel`, `/start`, `/help`.
  - Design message templates (vertical format, one field per line).
  - Define validation rules and error messages.
  - Decide how the bot should respond to success and failure.
- **Notes:**
  - This chat produced the main functional requirements and the technical specification.
  - The English version of the specification is stored in `docs/technical_specification.md`.

---

## 02_google_sheets_structure – Google Sheets structure

- **Chat ID:** `02_google_sheets_structure`
- **Role:** Data model and spreadsheet structure
- **Scope:**
  - Define the structure of the Google Sheets document.
  - Decide which worksheets are needed (`Income` and `Expenses`).
  - Define the columns for each worksheet.
  - Decide how the Google service account will access the spreadsheet.
- **Notes:**
  - The visible columns are business fields only (no internal technical columns are required in the UI).
  - Technical behavior is described in the technical specification.

---

## 03_telegram_bot_setup – Telegram bot setup

- **Chat ID:** `03_telegram_bot_setup`
- **Role:** Bot infrastructure
- **Scope:**
  - Create the bot in Telegram via BotFather.
  - Obtain and store the bot token (environment variable).
  - Choose the Telegram bot framework (for example, `aiogram`).
  - Decide on the update delivery method (long polling or webhook).
  - Connect the bot to the target Telegram group.
- **Notes:**
  - This chat focuses on the basic “skeleton” of the bot application.

---

## 04_income_command_handler – Income handler

- **Chat ID:** `04_income_command_handler`
- **Role:** `/income` command handler
- **Scope:**
  - Read messages that start with `/income`.
  - Split the message into lines and validate the format.
  - Map lines to the `Income` worksheet columns.
  - Call the Google Sheets client to append a row.
  - Return clear success or error messages to the user.
- **Notes:**
  - Uses the validation and field definitions from the requirements chat.
  - Strict rule: one message always creates exactly one `Income` row.

---

## 05_expense_command_handler – Expense handler

- **Chat ID:** `05_expense_command_handler`
- **Role:** `/expense` command handler
- **Scope:**
  - Read messages that start with `/expense`.
  - Validate the number of lines and required fields.
  - Ensure that at least one amount (USD/EUR/other) is provided.
  - Map lines to the `Expenses` worksheet columns.
  - Call the Google Sheets client to append a row.
  - Return clear success or error messages to the user.
- **Notes:**
  - Similar to the income handler but with three possible amount fields.
  - Enforces the “at least one amount” rule.

---

## 06_excel_and_service_commands – `/excel` and service commands

- **Chat ID:** `06_excel_and_service_commands`
- **Role:** `/excel`, `/start`, `/help`, and other service commands
- **Scope:**
  - Define the behavior of `/excel` (send spreadsheet link or export a file).
  - Implement service commands:
    - `/start` – introduction and list of commands
    - `/help` – message formats and basic instructions
  - Decide if `/excel` is available to everyone or only to specific users.
- **Notes:**
  - This chat ensures that non-technical users can conveniently access the spreadsheet.
  - Also defines how the bot explains itself to new users.

---

## 07_errors_logging_testing_deploy – Errors, logging, testing, deployment

- **Chat ID:** `07_errors_logging_testing_deploy`
- **Role:** Quality, reliability, and deployment strategy
- **Scope:**
  - Define minimal but useful logging:
    - Bot startup and shutdown
    - Successful writes to Google Sheets
    - Validation errors
    - Exceptions and API failures
  - Define error handling strategy:
    - What users see
    - What is written to logs
  - Prepare a basic test checklist for all commands.
  - Decide how the bot is deployed and updated (e.g. server, NAS, Docker).
- **Notes:**
  - This chat is about making the bot stable, testable, and maintainable in production.

---

## Summary

The original project used separate chats to keep discussions focused and organized.  
In this repository, the same structure is reflected as:

- Documentation in `docs/` (technical specification and this overview).
- Source code in `src/` grouped by responsibility (configuration, Google Sheets client, handlers).

All new code, comments, and documentation are written in English to make the project easier to share and maintain.
