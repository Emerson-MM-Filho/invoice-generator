import datetime
import os
from pathlib import Path

import pdfkit
from google.auth.external_account_authorized_user import (
    Credentials as ExternalAccountCredentials,
)
from google.oauth2.credentials import Credentials
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

from google_drive import upload_file

# Path to the templates folder
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


class Receiver(BaseModel):
    name: str
    email: str
    address: str
    city: str
    state: str
    zip_code: str
    country: str
    folder_id: str


class BillTo(BaseModel):
    name: str
    address: str


class Invoice(BaseModel):
    number: str
    date: datetime.date
    due_date: datetime.date
    receiver: Receiver
    bill_to: BillTo
    description: str
    total: str
    template: str = "invoice_template.html"

    @property
    def file_name(self):
        return "{year}-{month}-{day}-invoice-{number}.pdf".format(
            year=self.date.year,
            month=self.date.month,
            day=self.date.day,
            number=self.number,
        )


def generate_invoice_pdf(invoice: Invoice):
    path = Path(invoice.file_name)
    # Set up Jinja2 environment to load the HTML template
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(invoice.template)

    # Render the HTML with the provided invoice data
    html_out = template.render(invoice=invoice.model_dump(mode="json"))

    # Define options to force A4 size
    options = {
        "dpi": 300,
        "grayscale": True,
        "title": "Invoice",
    }

    # Save the generated HTML to PDF using pdfkit
    pdfkit.from_string(html_out, path, options=options)

    return path


def upload_invoice(
    invoice: Invoice, credentials: ExternalAccountCredentials | Credentials
):
    path = Path(invoice.file_name)
    if not path.exists():
        raise FileNotFoundError(
            "PDF file not found. Please generate the PDF file first."
        )

    # Upload the file to Google Drive
    file = upload_file(
        credentials,
        invoice.receiver.folder_id,
        path,
        properties=invoice.model_dump(mode="json", include={"receiver", "bill_to"}),
    )

    return file
