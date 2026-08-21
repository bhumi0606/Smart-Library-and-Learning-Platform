from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.schemas.loan.LoanCreate import CreateLoan
from app.schemas.loan.LoanUpdate import UpdateLoan
from app.services.LoanService import create_loan_service, get_loan_by_id_service, get_loans_service, update_loan_service, delete_loan_service

@pytest.mark.asyncio
@patch("app.services.LoanService.create_loan")
async def test_create_loan_service(mock_create_loan):
    session = MagicMock()

    loan = CreateLoan(
        member_id=1,
        book_id=1,
        issued_at=datetime.now(),
        due_date=datetime.now() + timedelta(days=14),
        return_date=datetime.now() + timedelta(days=14)
    )

    fake_loan = MagicMock()
    fake_loan.id = 1
    fake_loan.member_id = 1
    fake_loan.book_id = 1

    mock_create_loan.return_value = fake_loan

    result = await create_loan_service(
        loan=loan,
        session=session
    )

    assert result == fake_loan


@pytest.mark.asyncio
@patch("app.services.LoanService.get_loan_by_id")
async def test_get_loan_by_id_service(mock_get_loan_by_id):
    session = MagicMock()

    fake_loan = MagicMock()
    fake_loan.id = 1
    fake_loan.member_id = 1
    fake_loan.book_id = 1

    mock_get_loan_by_id.return_value = fake_loan

    result = await get_loan_by_id_service(
        id=1,
        session=session
    )

    assert result == fake_loan


@pytest.mark.asyncio
@patch("app.services.LoanService.get_loans")
async def test_get_loans_service(mock_get_loans):
    session = MagicMock()

    fake_loans = [
        MagicMock(
            id=1,
            member_id=1,
            book_id=1
        ),
        MagicMock(
            id=2,
            member_id=2,
            book_id=2
        )
    ]

    mock_get_loans.return_value = fake_loans

    result = await get_loans_service(
        session=session
    )

    assert result == fake_loans


@pytest.mark.asyncio
@patch("app.services.LoanService.update_loan")
async def test_update_loan_service(mock_update_loan):
    session = MagicMock()

    loan_update = UpdateLoan(
        status="returned"
    )

    fake_loan = MagicMock()
    fake_loan.id = 1
    fake_loan.status = "returned"

    mock_update_loan.return_value = fake_loan

    result = await update_loan_service(
        id=1,
        loan_update=loan_update,
        session=session
    )

    assert result == fake_loan


@pytest.mark.asyncio
@patch("app.services.LoanService.delete_loan")
async def test_delete_loan_service(mock_delete_loan):
    session = MagicMock()

    fake_loan = MagicMock()
    fake_loan.id = 1

    mock_delete_loan.return_value = fake_loan

    result = await delete_loan_service(
        id=1,
        session=session
    )

    assert result == fake_loan