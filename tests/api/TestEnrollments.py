from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch("app.api.enrollments.create_enrollment_service")
def test_create_enrollment(mock_create_enrollment):

    fake_enrollment = {
        "id": 1,
        "member_id": 1,
        "course_id": 1,
    }

    mock_create_enrollment.return_value = fake_enrollment

    response = client.post(
        "/api/enrollments",
        json={
            "member_id": 1,
            "course_id": 1,
        }
    )

    assert response.status_code == 201
    assert response.json() == fake_enrollment


@patch("app.api.enrollments.get_enrollments_service")
def test_get_enrollments(mock_get_enrollments):

    fake_enrollments = [
        {
            "id": 1,
            "member_id": 1,
            "course_id": 1,
        },
        {
            "id": 2,
            "member_id": 2,
            "course_id": 2,
        },
    ]

    mock_get_enrollments.return_value = fake_enrollments

    response = client.get("/api/enrollments")

    assert response.status_code == 200
    assert response.json() == fake_enrollments


@patch("app.api.enrollments.get_enrollment_by_id_service")
def test_get_enrollment(mock_get_enrollment):

    fake_enrollment = {
        "id": 1,
        "member_id": 1,
        "course_id": 1,
    }

    mock_get_enrollment.return_value = fake_enrollment

    response = client.get("/api/enrollments/1")

    assert response.status_code == 200
    assert response.json() == fake_enrollment


@patch("app.api.enrollments.update_enrollment_service")
def test_update_enrollment(mock_update_enrollment):

    fake_enrollment = {
        "id": 1,
        "member_id": 1,
        "course_id": 1,
        "status": "completed",
    }

    mock_update_enrollment.return_value = fake_enrollment

    response = client.patch(
        "/api/enrollments/1",
        json={
            "status": "completed"
        }
    )

    assert response.status_code == 200
    assert response.json() == fake_enrollment


@patch("app.api.enrollments.delete_enrollment_service")
def test_delete_enrollment(mock_delete_enrollment):

    mock_delete_enrollment.return_value = None

    response = client.delete("/api/enrollments/1")

    assert response.status_code == 204