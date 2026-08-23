from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Book, Loan


async def get_monthly_report_data(
    session: AsyncSession,
    start_date: datetime,
    end_date: datetime,
):
    total_issued_result = await session.execute(
        select(func.count(Loan.id)).where(
            Loan.issued_at >= start_date,
            Loan.issued_at < end_date,
        )
    )

    total_issued = total_issued_result.scalar() or 0

    overdue_result = await session.execute(
        select(func.count(Loan.id)).where(
            Loan.issued_at >= start_date,
            Loan.issued_at < end_date,
            Loan.due_date < datetime.now(timezone.utc),
            Loan.return_date.is_(None),
        )
    )

    overdue_loans = overdue_result.scalar() or 0

    popular_result = await session.execute(
        select(
            Book.title,
            func.count(Loan.id).label("loan_count"),
        )
        .join(Loan, Loan.book_id == Book.id)
        .where(
            Loan.issued_at >= start_date,
            Loan.issued_at < end_date,
        )
        .group_by(Book.id, Book.title)
        .order_by(
            func.count(Loan.id).desc()
        )
        .limit(10)
    )

    popular_titles = popular_result.all()

    return {
        "total_issued": total_issued,
        "overdue_loans": overdue_loans,
        "popular_titles": popular_titles,
    }