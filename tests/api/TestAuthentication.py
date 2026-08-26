from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch("app.api.authentication.register_member_service")
def test_register_member(mock_register_member):

    fake_member = {
        "id": 1,
        "name": "Test Member",
        "email": "test@gmail.com",
        "created_at": "2026-08-22T09:47:00.104350"
    }

    mock_register_member.return_value = fake_member

    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test Member",
            "email": "test@gmail.com",
            "password": "test123456",
            "role": "member",
        }
    )

    assert response.status_code == 201
    assert response.json() == fake_member


@patch("app.api.authentication.login_member_service")
def test_login_member(mock_login_member):

    mock_login_member.return_value = {
        "access_token": "test_access_token",
        "token_type": "bearer"
    }

    response = client.post(
        "/api/auth/login",
        data={
            "username": "test@gmail.com",
            "password": "test123456",
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "access_token": "test_access_token",
        "token_type": "bearer"
    }