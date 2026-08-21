from fastapi import HTTPException, status

from app.repository.LoanRepository import create_loan, delete_loan, get_loan_by_id, get_loans, update_loan
from app.schemas.loan.LoanCreate import CreateLoan
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.loan.LoanUpdate import UpdateLoan

async def create_loan_service(
        loan: CreateLoan,
        session: AsyncSession
):
    response = await create_loan(
        loan = loan,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "Loan is not added"
        )
    return response

async def get_loan_by_id_service(
        id: int,
        session: AsyncSession
):
    response = await get_loan_by_id(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"Loan not found with id:{id}"
        )

    return response

async def get_loans_service(
        session: AsyncSession
):
    response = await get_loans(
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Loan not found"
        )

    return response

async def update_loan_service(
        id: int,
        loan_update: UpdateLoan,
        session: AsyncSession
):
    response = await update_loan(
        id = id,
        update_loan = loan_update,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"Loan not found with id:{id}"
        )

    return response

async def delete_loan_service(
        id: int,
        session: AsyncSession
):
    response = await delete_loan(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"Loan not found with id:{id}"
        )
        
    return response