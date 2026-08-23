import asyncio

from app.core.celery_app import celery_app
from app.db.database import Session
from app.repository.LoanRepository import get_overdue_loans
from app.services.NotificationService import send_overdue_email


async def process_overdue_loans():

    async with Session() as session:

        overdue_loans = await get_overdue_loans(
            session=session,
        )

        for loan in overdue_loans:

            member = loan.member
            book = loan.book

            await send_overdue_email(
                email=member.email,
                member_name=member.name,
                book_title=book.title,
                due_date=loan.due_date,
            )


@celery_app.task(
    name="send_overdue_notifications"
)
def send_overdue_notifications():

    asyncio.run(
        process_overdue_loans()
    )
    