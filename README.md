# MailCLI

A lightweight Python command-line tool for building and sending emails through an SMTP server.

## Features

- Send plain-text and HTML emails.
- Send to one or multiple recipients.
- Attach files to outgoing messages.
- Configure SMTP credentials through environment variables.
- Preview message details with a dry run without connecting to the SMTP server.
- Handle configuration, message-building, and delivery errors with custom exceptions.

## Requirements

- Python 3.11 or later
- Access to an SMTP server and valid credentials for sending real emails

## Installation

Clone the repository and move into the project directory:

```bash
git clone https://github.com/MESLIMOHAMEDM22005188/mailcli-email-sender.git
cd mailcli-email-sender
```

Create and activate a virtual environment.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the package and its development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Configuration

MailCLI reads its SMTP configuration from environment variables:

| Variable | Description | Example |
| --- | --- | --- |
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USERNAME` | SMTP account username | `your-address@gmail.com` |
| `SMTP_PASSWORD` | SMTP authentication password | App password or provider-supported credential |
| `SMTP_USE_TLS` | Whether to use STARTTLS | `true` |

### Example: Gmail

For Gmail, use `smtp.gmail.com` on port `587` with STARTTLS enabled. Depending on your account, you may need a Google app password; app passwords require two-step verification and are not available for every account.

In Windows PowerShell, set the variables for the current terminal session:

```powershell
$env:SMTP_HOST = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SMTP_USE_TLS = "true"
$env:SMTP_USERNAME = Read-Host "Your Gmail address"

$securePassword = Read-Host "Google app password" -AsSecureString
$env:SMTP_PASSWORD = [System.Net.NetworkCredential]::new("", $securePassword).Password.Replace(" ", "")
Remove-Variable securePassword
```

These variables are session-specific and must be set again in a new terminal session. Never commit real credentials or app passwords to the repository.

## Usage

If you are running the source tree without installing the package, set `PYTHONPATH` from the project root:

**Windows PowerShell:**

```powershell
$env:PYTHONPATH = "src"
```

### Show help

```bash
python -m mailcli --help
```

### Show the version

```bash
python -m mailcli --version
```

### Send a plain-text email

```bash
python -m mailcli --from "sender@example.com" --to "recipient@example.com" --subject "Hello" --body "Hello from MailCLI!"
```

### Send to multiple recipients

Provide all recipient addresses after `--to`:

```bash
python -m mailcli --from "sender@example.com" --to "first@example.com" "second@example.com" --subject "Team update" --body "Hello everyone."
```

### Send an HTML email

Add the `--html` flag when the body contains HTML:

```bash
python -m mailcli --from "sender@example.com" --to "recipient@example.com" --subject "HTML message" --body "<h1>Hello</h1><p>Sent with MailCLI.</p>" --html
```

### Attach a file

Use `--attachment` for each file you want to attach:

```bash
python -m mailcli --from "sender@example.com" --to "recipient@example.com" --subject "Report" --body "Please find the report attached." --attachment "report.pdf"
```

Multiple attachments are supported:

```bash
python -m mailcli --from "sender@example.com" --to "recipient@example.com" --subject "Documents" --body "Please find the attached files." --attachment "report.pdf" --attachment "summary.txt"
```

### Dry run

Use `--dry-run` to build the email and display its main details without sending it:

```bash
python -m mailcli --from "sender@example.com" --to "recipient@example.com" --subject "Test" --body "Testing MailCLI" --dry-run
```

A successful dry run does not verify SMTP credentials or confirm email delivery.

## Running tests

Install the development dependencies, then run:

```bash
python -m pytest
```

For verbose output:

```bash
python -m pytest -v
```

## Error handling

MailCLI defines custom exceptions for common failure categories:

- `ConfigurationError`: missing or invalid SMTP configuration.
- `MessageError`: invalid message data or an attachment that cannot be accessed.
- `EmailSendError`: an SMTP connection or sending failure.

The command-line interface reports these errors and exits with a non-zero status code.

## Project structure

```text
mailcli-email-sender/
├── src/
│   └── mailcli/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── config.py
│       ├── exceptions.py
│       ├── mailer.py
│       ├── message_builder.py
│       └── models.py
├── tests/
├── .env.example
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

## Security notes

- Do not hard-code SMTP credentials in source files.
- Do not commit `.env` files or real passwords.
- Use provider-supported authentication and follow your SMTP provider's security requirements.

## License

See the [LICENSE](LICENSE) file for license details.
