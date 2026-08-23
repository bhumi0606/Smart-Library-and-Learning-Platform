from email.message import EmailMessage

import aiosmtplib

from app.core.config import SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM
from app.db.models import Loan

async def send_overdue_email(
    email: str,
    member_name: str,
    book_title: str,
    due_date,
):
    message = EmailMessage()

    message["From"] = EMAIL_FROM
    message["To"] = email
    message["Subject"] = "Overdue Book Reminder"

    message.set_content(
        f"""
            Hello {member_name},

            The following book is overdue:

            Book: {book_title}
            Due date: {due_date}

            Please return the book as soon as possible.

            Regards,
            Smart Library
            """
                )

    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
        start_tls=True,
    )

async def send_loan_receipt_email(
    email: str,
    member_name: str,
    book_title: str,
    due_date,
    receipt_bytes: bytes,
):
    message = EmailMessage()

    message["From"] = EMAIL_FROM
    message["To"] = email
    message["Subject"] = "Smart Library - Book Checkout Receipt"

    message.set_content(
        f"""
Hello {member_name},

Your book has been successfully checked out.

Book: {book_title}
Due date: {due_date}

Your loan receipt is attached to this email.

Regards,
Smart Library
"""
    )

    message.add_attachment(
        receipt_bytes,
        maintype="application",
        subtype="pdf",
        filename=f"loan_receipt.pdf",
    )

    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
        start_tls=True,
    )