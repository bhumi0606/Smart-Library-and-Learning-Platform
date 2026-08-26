from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.jwt_token import create_access_token
from app.db.models.Member import Member
from app.schemas.member.MemberCreate import MemberCreate
from app.services.AuthenticationService import login_member_service, register_member_service

@pytest.mark.asyncio
async def test_register_member_service():
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    fake_member = MemberCreate(
        name="Test",
        email="testing1@gmail.com",
        password="test123456",
        role="member"
    )

    result = await register_member_service(
        member=fake_member,
        session=session
    )

    assert isinstance(result, Member)

@pytest.mark.asyncio
@patch("app.services.AuthenticationService.create_access_token")
@patch("app.services.AuthenticationService.verify_password")
@patch("app.services.AuthenticationService.get_member_by_email")
async def test_login_user_service(mock_get_user,mock_verify_password,mock_create_token):
    session = MagicMock()
    fake_member = MagicMock()
    fake_member.email = "testing1@gmail.com"
    fake_member.password = "$2b$12$oDiZxg./N.5NDTcVTm5FdOluMTIx1GvhEhvSjGqWvxo8ErOHVuXRq"
    fake_member.role = "user"

    mock_get_user.return_value = fake_member
    mock_verify_password.return_value = True
    mock_create_token.return_value = 500

    login_data = MagicMock()
    login_data.username = "testing1@gmail.com"
    login_data.password = "test1"

    token = await login_member_service(
        member=login_data,
        session=session
    )
    assert token == {
        "access_token": 500,
        "token_type": "bearer"
    }