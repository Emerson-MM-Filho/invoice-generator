# Invoice Automation Project

This project automatically generates invoices, sends them via email, stores them on Google Drive, and fill Notion database with the invoice details.

## Features

- Generate PDF invoices automatically.
- Send invoices via email.
- Store invoices in Google Drive.
- Fill Notion database with invoice details.

## Requirements

- Python 3.8+
- [Poetry](https://python-poetry.org/) for dependency management.
- [Ruff](https://beta.ruff.rs/docs/) for linting and formatting.
- [pre-commit](https://pre-commit.com/) for automatic linting and formatting on commit.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/invoice-automation.git
cd invoice-automation
```

2. Install the dependencies using Poetry:
```bash
poetry install
```

3. Set up the configuration file:
```bash
poetry run pre-commit install
```

## Usage

To generate an invoice:
```bash
poetry run python generate_invoice.py
```

The script will:

- Generate the invoice PDF.
- Send it via email.
- Upload it to Google Drive.
- Fill the Notion database with the invoice details.

## Development

### Linting and Formatting
We use Ruff for linting and formatting. The pre-commit hooks are set up to automatically run Ruff before each commit. You can also run it manually:

```bash
poetry run ruff .
```

License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
