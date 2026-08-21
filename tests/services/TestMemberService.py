from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.services.MemberService import get_member_by_id_service, get_members_service, update_member_service, delete_member_service
from app.schemas.member.MemberUpdate import MemberUpdate


@pytest.mark.asyncio
@patch("app.services.MemberService.get_member_by_id")
async def test_get_member_by_id_service(mock_get_member):
    session = MagicMock()

    fake_member = MagicMock()
    fake_member.id = 1
    fake_member.name = "Test"
    fake_member.email = "testing1@gmail.com"

    mock_get_member.return_value = fake_member

    result = await get_member_by_id_service(
        id=1,
        session=session
    )

    assert result == fake_member

@pytest.mark.asyncio
@patch("app.services.MemberService.get_members")
async def test_get_members_service(mock_get_members):
    session = MagicMock()

    fake_members = [
        MagicMock(id=1, name="Test"),
        MagicMock(id=2, name="Test2")
    ]

    mock_get_members.return_value = fake_members

    result = await get_members_service(
        session=session
    )

    assert result == fake_members


@pytest.mark.asyncio
@patch("app.services.MemberService.update_member", new_callable=AsyncMock)
async def test_update_member_service(mock_update_member):
    session = MagicMock()

    fake_member = MagicMock()
    fake_member.id = 1
    fake_member.name = "Updated Test"

    member_update = MemberUpdate(
        name = "Updated Test"
    )

    mock_update_member.return_value = fake_member

    result = await update_member_service(
        id=1,
        member_update=member_update,
        session=session
    )

    assert result == fake_member

@pytest.mark.asyncio
@patch("app.services.MemberService.delete_member", new_callable=AsyncMock)
async def test_delete_member_service(mock_delete_member):
    session = MagicMock()

    fake_member = MagicMock()
    fake_member.id = 1

    mock_delete_member.return_value = fake_member

    result = await delete_member_service(
        id=1,
        session=session
    )

    assert result == fake_member
