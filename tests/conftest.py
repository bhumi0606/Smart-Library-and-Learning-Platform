import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies.authentication import get_current_user
from app.db.models import Member
from app.enums.RoleEnums import Role


@pytest.fixture
def member_client():

    fake_member = Member(
        id=1,
        name="Test Member",
        email="member@gmail.com",
        role=Role.MEMBER,
    )

    async def override_get_current_user():
        return fake_member

    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()


@pytest.fixture
def librarian_client():

    fake_librarian = Member(
        id=99,
        name="Test Librarian",
        email="librarian@gmail.com",
        role=Role.LIBRARIAN,
    )

    async def override_get_current_user():
        return fake_librarian

    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()