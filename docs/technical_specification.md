# Telegram Accounting Bot – Technical Specification

**Project name:** Telegram Accounting Bot  
**Purpose:** Track income and expense operations in a Telegram group and store them in Google Sheets.  
**Language:** All code, documentation, field names, and bot messages are in English.

---

## 1. Purpose & Scope

The Telegram Accounting Bot is a simple backend-only Telegram bot that allows users to record **income** and **expense** operations in a shared **Google Sheets** document.

Each correctly formatted message in a Telegram group is converted into exactly **one row** in a corresponding worksheet:

- `/income` → worksheet `Income`
- `/expense` → worksheet `Expenses`

The bot:

- Receives messages in a **vertical template** format (one field per line).
- Validates the structure and basic formats (dates, required fields, amounts).
- Appends rows to Google Sheets via a Google service account.
- Replies to the user in English with clear success or error messages.

The bot **does not**:

- Perform any currency conversion.
- Calculate totals or statistics.
- Modify or delete existing rows in the spreadsheet.
- Provide analytics or dashboards.

---

## 2. Main Features

- Track income operations with a strict multi-line template.
- Track expense operations with a strict multi-line template.
- Validate incoming messages and reject invalid data.
- Append rows to two worksheets: `Income` and `Expenses`.
- Provide an `/excel` command to share or export the spreadsheet (link or file).
- Basic logging and error handling for troubleshooting.
- Clean and predictable integration with Google Sheets using a service account.

---

## 3. Commands

All commands, responses, and field names are in English.

### 3.1 `/start`

- **Scope:** Private chat and group chat.
- **Purpose:** Show a short introduction and list of commands.
- **Behavior:**
  - Sends a welcome message explaining that this bot tracks income and expenses in Google Sheets.
  - Lists the main commands: `/income`, `/expense`, `/excel`, `/help`.

Example reply:

> Welcome!  
> This bot helps you track income and expenses in a shared Google Sheets document.  
>  
> Available commands:  
> • `/income` – add a new income record  
> • `/expense` – add a new expense record  
> • `/excel` – get access to the spreadsheet  
> • `/help` – show message formats and instructions

---

### 3.2 `/help`

- **Scope:** Private chat and group chat.
- **Purpose:** Show message formats and basic rules.
- **Behavior:**
  - Explains that:
    - `/income` uses a vertical template with **10–11 lines**.
    - `/expense` uses a vertical template with **6–7 lines**.
  - Reminds that **one message = one record**.
  - Explains that the bot only appends rows and does not recalculate anything.

Example reply (shortened):

> Use `/income` for income records and `/expense` for expenses.  
> Each command expects a vertical text template (one field per line).  
> One message always creates exactly one row in the spreadsheet.  
> The bot does not perform any currency conversion or calculations.

---

### 3.3 `/income` – Income record

- **Scope:** Group chat.
- **Target worksheet:** `Income`
- **Purpose:** Insert a single income transaction.

#### 3.3.1 Message format

After the `/income` command, the bot expects **10 or 11 lines**:

- Minimum: 10 lines (no comment).
- Maximum: 11 lines (with optional comment).

The lines map to fields as follows:

| Line | Field key             | Field label (English)            | Required | Type                       |
|------|-----------------------|----------------------------------|---------:|----------------------------|
| 1    | `payment_date`        | Payment date                     | Yes      | Date                       |
| 2    | `amount_with_currency`| Amount with currency             | Yes      | Amount with currency       |
| 3    | `payment_purpose`     | Payment purpose                  | Yes      | Non-empty string           |
| 4    | `client_full_name`    | Client full name                 | Yes      | Non-empty string           |
| 5    | `client_birth_date`   | Client date of birth             | Yes      | Non-empty string           |
| 6    | `phone_number`        | Phone number                     | Yes      | Non-empty string           |
| 7    | `email`               | Email                            | Yes      | Non-empty string           |
| 8    | `client_status`       | Client status                    | Yes      | Non-empty string           |
| 9    | `country`             | Country                          | Yes      | Non-empty string           |
| 10   | `manager`             | Manager                          | Yes      | Non-empty string           |
| 11   | `comment`             | Comment                          | No       | Optional string            |

Example message:

```text
/income
24.12.2024
500 USD
Full payment for Vietnam program
John Doe
14.06.1986
+1 555 123 456
john.doe@example.com
Returning client
USA
Kate
Client asked for invoice copy
