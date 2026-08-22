from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch("app.api.members.get_members_service")
def test_get_members(mock_get_members):

    fake_members = [
        {
            "id": 1,
            "name": "Test Member",
            "email": "test1@gmail.com",
            "role": "member",
        },
        {
            "id": 2,
            "name": "Test Member 2",
            "email": "test2@gmail.com",
            "role": "member",
        },
    ]

    mock_get_members.return_value = fake_members

    response = client.get("/api/members")

    assert response.status_code == 200
    assert response.json() == fake_members


@patch("app.api.members.get_member_by_id_service")
def test_get_member(mock_get_member):

    fake_member = {
        "id": 1,
        "name": "Test Member",
        "email": "test@gmail.com",
        "role": "member",
    }
    
    mock_get_member.return_value = fake_member

    response = client.get("/api/members/1")

    assert response.status_code == 200
    assert response.json() == fake_member


@patch("app.api.members.update_member_service")
def test_update_member(mock_update_member):

    fake_member = {
        "id": 1,
        "name": "Updated Member",
        "email": "test@gmail.com",
        "role": "member",
    }

    mock_update_member.return_value = fake_member

    response = client.patch(
        "/api/members/1",
        json={
            "name": "Updated Member"
        }
    )

    assert response.status_code == 200
    assert response.json() == fake_member


@patch("app.api.members.delete_member_service")
def test_delete_member(mock_delete_member):

    mock_delete_member.return_value = None

    response = client.delete("/api/members/1")

    assert response.status_code == 204