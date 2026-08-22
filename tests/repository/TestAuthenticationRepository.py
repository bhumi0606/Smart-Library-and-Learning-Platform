from unittest.mock import MagicMock, AsyncMock
import pytest

from app.repository.AuthenticationRepository import get_member_by_email, register_member
from app.db.models import Member

@pytest.mark.asyncio
async def test_register_member():
    session = AsyncMock()
    session.commit = AsyncMock()
    fake_member = MagicMock()

    fake_member.name = "Test"
    fake_member.email = "testing1@gmail.com"
    fake_member.password = "Test@123"

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_member
        
    session.execute = AsyncMock(return_value=result_mock)
    session.add = MagicMock()
    session.commit = AsyncMock()

    result = await register_member(
        member = fake_member,
        session = session
    )

    assert isinstance(result, Member)

@pytest.mark.asyncio
async def test_get_member_by_email():
    session = AsyncMock()
    fake_member = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_member

    session.execute = AsyncMock(return_value=result_mock)

    member = await get_member_by_email(
        email="testing1@gmail.com",
        session = session
    )

    assert member == fake_member