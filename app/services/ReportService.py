from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.services.S3Service import upload_document


def generate_monthly_report(
    report_data,
    year: int,
    month: int,
):
    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4,
    )

    pdf.setTitle(
        f"Smart Library Monthly Report - {year}-{month:02d}"
    )

    pdf.setFont(
        "Helvetica-Bold",
        20,
    )

    pdf.drawString(
        50,
        800,
        "SMART LIBRARY",
    )

    pdf.setFont(
        "Helvetica-Bold",
        15,
    )

    pdf.drawString(
        50,
        770,
        f"Monthly Usage Report - {year}-{month:02d}",
    )

    pdf.line(
        50,
        750,
        545,
        750,
    )

    y = 710

    total_issued = report_data["total_issued"]
    overdue_loans = report_data["overdue_loans"]

    if total_issued > 0:
        overdue_rate = (
            overdue_loans / total_issued
        ) * 100
    else:
        overdue_rate = 0

    pdf.setFont(
        "Helvetica",
        12,
    )

    pdf.drawString(
        50,
        y,
        f"Total Books Issued: {total_issued}",
    )

    y -= 30

    pdf.drawString(
        50,
        y,
        f"Total Overdue Loans: {overdue_loans}",
    )

    y -= 30

    pdf.drawString(
        50,
        y,
        f"Overdue Rate: {overdue_rate:.2f}%",
    )

    y -= 50

    pdf.setFont(
        "Helvetica-Bold",
        14,
    )

    pdf.drawString(
        50,
        y,
        "Popular Titles",
    )

    y -= 30

    pdf.setFont(
        "Helvetica",
        11,
    )

    for index, row in enumerate(
        report_data["popular_titles"],
        start=1,
    ):
        title = row[0]
        loan_count = row[1]

        pdf.drawString(
            60,
            y,
            f"{index}. {title} - {loan_count} loans",
        )

        y -= 25

        if y < 80:
            pdf.showPage()

            y = 800

            pdf.setFont(
                "Helvetica",
                11,
            )

    pdf.save()

    buffer.seek(0)

    report_bytes = buffer.getvalue()

    file_name = (
        f"reports/{year}/{month:02d}/"
        f"monthly_report_{year}_{month:02d}.pdf"
    )

    report_url = upload_document(
        file_bytes=report_bytes,
        file_name=file_name,
        content_type="application/pdf",
    )

    return report_url, report_bytes