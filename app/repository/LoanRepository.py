
from sqlalchemy import select

from app.db.models import Loan
from app.schemas.loan.LoanCreate import CreateLoan
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.loan.LoanUpdate import UpdateLoan

async def create_loan(
    loan: CreateLoan,
    session: AsyncSession
):
    loan = Loan(
        member_id = loan.member_id,
        book_id = loan.book_id,
        issued_at = loan.issued_at,
        due_date = loan.due_date,
        return_date = loan.return_date
    )

    session.add(loan)
    await session.commit()
    return loan

async def get_loan_by_id(
        id: int,
        session: AsyncSession
):
    loan = await session.execute(
        select(Loan).where(Loan.id == id)
    )
    
    return loan.scalar_one_or_none()

async def get_loans(
        session: AsyncSession
):
    loans = await session.execute(
        select(Loan)
    )
    
    return loans.scalars().all()

async def update_loan(
        id: int,
        update_loan: UpdateLoan,
        session: AsyncSession
):
    loan = await get_loan_by_id(
        id = id,
        session = session
    )
    if loan == None:
        return None
    else:
        if update_loan.due_date:
            loan.due_date = update_loan.due_date
        if update_loan.return_date:
            loan.return_date = update_loan.return_date

    await session.commit()
    return loan

async def delete_loan(
        id: int,
        session: AsyncSession
):
    loan = await get_loan_by_id(
        id = id,
        session = session
    )
    if loan == None:
        return None

    await session.delete(loan)
    await session.commit()

    return loan