import pytest
from unittest.mock import MagicMock, AsyncMock

from app.db.models import Loan
from app.repository.LoanRepository import create_loan, get_loan_by_id, get_loans, update_loan
from app.schemas.loan.LoanUpdate import UpdateLoan

@pytest.mark.asyncio
async def test_create_loan():
    session = AsyncMock()
    fake_loan = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_loan

    session.execute = AsyncMock(return_value = result_mock)
    session.add = MagicMock()
    session.commit = AsyncMock()

    result = await create_loan(
        loan = fake_loan,
        session = session
    )

    assert isinstance(result, Loan)

@pytest.mark.asyncio
async def test_get_loan_by_id():
    session = AsyncMock()
    fake_loan = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_loan

    session.execute = AsyncMock(return_value = result_mock)

    result = await get_loan_by_id(
        id = 1,
        session = session
    )

    assert result == fake_loan

@pytest.mark.asyncio
async def test_get_loans():
    session = AsyncMock()
    fake_loan = MagicMock()

    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = [fake_loan]

    session.execute = AsyncMock(return_value = result_mock)

    result = await get_loans(
        session = session
    )

    assert result == [fake_loan]

@pytest.mark.asyncio
async def test_update_loan():
    session = AsyncMock()
    fake_loan = MagicMock()
    fake_loan.due_date = "2024-06-22"

    fake_loan_update = UpdateLoan(
        due_date = "2024-06-26"
    )

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_loan

    session.execute = AsyncMock(return_value = result_mock)
    session.commit = AsyncMock()

    result = await update_loan(
        id = 1,
        loan_update = fake_loan_update,
        session = session
    )

    assert result == fake_loan
