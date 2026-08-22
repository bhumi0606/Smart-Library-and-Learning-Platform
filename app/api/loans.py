from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db

from app.dependencies.authentication import get_current_user, require_librarian

from app.schemas.loan.LoanCreate import CreateLoan
from app.schemas.loan.LoanUpdate import UpdateLoan

from app.services.LoanService import create_loan_service, get_loan_by_id_service, get_loans_service, update_loan_service, return_loan_service, get_overdue_loans_service

loan_router = APIRouter(
    dependencies=[Depends(get_current_user)],
    prefix="/loans",
    tags=["Loans"],
)


@loan_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_loan(
    loan: CreateLoan,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await create_loan_service(
        loan=loan,
        current_user=current_user,
        session=session,
    )


@loan_router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_loans(
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await get_loans_service(
        current_user=current_user,
        session=session,
    )


@loan_router.get(
    "/overdue",
    status_code=status.HTTP_200_OK,
)
async def get_overdue_loans(
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await get_overdue_loans_service(
        current_user=current_user,
        session=session,
    )


@loan_router.get(
    "/{loan_id}",
    status_code=status.HTTP_200_OK,
)
async def get_loan(
    loan_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await get_loan_by_id_service(
        id=loan_id,
        current_user=current_user,
        session=session,
    )


@loan_router.post(
    "/{loan_id}/return",
    status_code=status.HTTP_200_OK,
)
async def return_loan(
    loan_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await return_loan_service(
        id=loan_id,
        current_user=current_user,
        session=session,
    )


@loan_router.patch(
    "/{loan_id}",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_200_OK,
)
async def update_loan(
    loan_id: int,
    loan_update: UpdateLoan,
    session: AsyncSession = Depends(get_db),
):
    return await update_loan_service(
        id=loan_id,
        loan_update=loan_update,
        session=session,
    )