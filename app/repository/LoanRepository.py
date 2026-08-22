from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Loan
from app.schemas.loan.LoanCreate import CreateLoan
from app.schemas.loan.LoanUpdate import UpdateLoan


async def create_loan(
    loan: CreateLoan,
    session: AsyncSession,
):
    new_loan = Loan(
        member_id=loan.member_id,
        book_id=loan.book_id,
        issued_at=datetime.now(timezone.utc),
        due_date=loan.due_date,
        return_date=None,
    )

    session.add(new_loan)

    await session.commit()
    await session.refresh(new_loan)

    return new_loan


async def get_loan_by_id(
    id: int,
    session: AsyncSession,
):
    result = await session.execute(
        select(Loan).where(
            Loan.id == id
        )
    )

    return result.scalar_one_or_none()


async def get_loans(
    session: AsyncSession,
    member_id: int | None = None,
):
    query = select(Loan)

    if member_id is not None:
        query = query.where(
            Loan.member_id == member_id
        )

    result = await session.execute(query)

    return result.scalars().all()


async def get_overdue_loans(
    session: AsyncSession,
    member_id: int | None = None,
):
    now = datetime.now(timezone.utc)

    query = select(Loan).where(
        Loan.due_date < now,
        Loan.return_date.is_(None),
    )

    if member_id is not None:
        query = query.where(
            Loan.member_id == member_id
        )

    result = await session.execute(query)

    return result.scalars().all()


async def update_loan(
    id: int,
    loan_update: UpdateLoan,
    session: AsyncSession,
):
    loan = await get_loan_by_id(
        id=id,
        session=session,
    )

    if loan is None:
        return None

    if loan_update.due_date is not None:
        loan.due_date = loan_update.due_date

    if loan_update.return_date is not None:
        loan.return_date = loan_update.return_date

    await session.commit()
    await session.refresh(loan)

    return loan


async def return_loan(
    id: int,
    session: AsyncSession,
):
    loan = await get_loan_by_id(
        id=id,
        session=session,
    )

    if loan is None:
        return None

    loan.return_date = datetime.now(timezone.utc)

    await session.commit()
    await session.refresh(loan)

    return loan


async def delete_loan(
    id: int,
    session: AsyncSession,
):
    loan = await get_loan_by_id(
        id=id,
        session=session,
    )

    if loan is None:
        return None

    await session.delete(loan)

    await session.commit()

    return loan