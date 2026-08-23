from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.services.S3Service import upload_document


def generate_loan_receipt(
    loan,
):

    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4,
    )

    pdf.setTitle("Smart Library Loan Receipt")

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawString(
        50,
        800,
        "SMART LIBRARY",
    )

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        770,
        "BOOK LOAN RECEIPT",
    )

    pdf.line(
        50,
        755,
        545,
        755,
    )

    y = 720

    pdf.drawString(
        50,
        y,
        f"Receipt ID: {loan.id}",
    )

    y -= 30

    pdf.drawString(
        50,
        y,
        f"Member: {loan.member.name}",
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Email: {loan.member.email}",
    )

    y -= 40

    pdf.drawString(
        50,
        y,
        f"Book: {loan.book.title}",
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Book ID: {loan.book.id}",
    )

    y -= 40

    pdf.drawString(
        50,
        y,
        f"Issued At: {loan.issued_at}",
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Due Date: {loan.due_date}",
    )

    y -= 50

    pdf.drawString(
        50,
        y,
        "Please return the book before the due date.",
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        "Thank you for using Smart Library.",
    )

    pdf.save()

    buffer.seek(0)

    receipt_bytes = buffer.getvalue()

    file_name = f"receipts/loan_{loan.id}.pdf"

    receipt_url = upload_document(
        file_bytes=receipt_bytes,
        file_name=file_name,
        content_type="application/pdf",
    )

    return receipt_url, receipt_bytes