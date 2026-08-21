from app.repository.MemberRepository import delete_member, get_member_by_id, get_members, update_member
from unittest.mock import MagicMock, AsyncMock
import pytest

from app.schemas.member.MemberUpdate import MemberUpdate

@pytest.mark.asyncio
async def test_get_member_by_id():
    session = AsyncMock()
    fake_member = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_member

    session.execute = AsyncMock(return_value=result_mock)

    member = await get_member_by_id(1, session)

    assert member == fake_member

@pytest.mark.asyncio
async def test_get_members():
    session = AsyncMock()
    fake_member = MagicMock()

    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = [fake_member]

    session.execute = AsyncMock(return_value=result_mock)

    members = await get_members(session)

    assert members == [fake_member]

@pytest.mark.asyncio
async def test_update_member():
    session = AsyncMock()
    fake_member = MagicMock()
    fake_member.name = "Test"

    fake_member_update = MemberUpdate(
        name = "Testing"
    )

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_member

    session.execute = AsyncMock(return_value=result_mock)
    session.commit = AsyncMock()

    result = await update_member(
        id=1,
        update_member=fake_member_update,
        session = session
    )

    assert result == fake_member

@pytest.mark.asyncio
async def test_delete_member():
    session = AsyncMock()
    fake_member = MagicMock()
    fake_member.id = 1

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_member

    session.execute = AsyncMock(return_value=result_mock)
    session.commit = AsyncMock()

    result = await delete_member(
        id = 1,
        session = session
    )

    assert result == fake_member