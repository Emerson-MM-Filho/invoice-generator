import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List


def send_email(
    from_: str,
    password: str,
    to: List[str],
    cc: List[str],
    subject: str,
    body: str,
    attachments: List[Path],
):
    # Set up the email message
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_
    msg["To"] = ", ".join(to)
    msg["Cc"] = ", ".join(cc)

    msg.attach(MIMEText(body, "plain"))

    # Attach files to the email
    for attachment in attachments:
        with open(attachment, "rb") as f:
            part = MIMEApplication(f.read(), Name=attachment.name)
        # After the file is closed
        part["Content-Disposition"] = 'attachment; filename="%s"' % attachment.name
        msg.attach(part)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(from_, password)
    s.sendmail(from_, to + cc, msg.as_string().encode("utf-8"))
    s.quit()
