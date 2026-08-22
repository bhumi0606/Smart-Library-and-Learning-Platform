from unittest.mock import AsyncMock, patch


@patch("app.api.enrollments.create_enrollment_service")
def test_create_enrollment(
    mock_create_enrollment,
    member_client,
):

    fake_enrollment = {
        "id": 1,
        "member_id": 2,
        "course_id": 1,
    }

    mock_create_enrollment.return_value = fake_enrollment

    response = member_client.post(
        "/api/enrollments",
        json={
            "member_id": 2,
            "course_id": 1,
        },
    )

    assert response.status_code == 201
    assert response.json() == fake_enrollment


@patch("app.api.enrollments.get_enrollments_service")
def test_get_enrollments(
    mock_get_enrollments,
    member_client,
):

    fake_enrollments = [
        {
            "id": 1,
            "member_id": 2,
            "course_id": 1,
        }
    ]

    mock_get_enrollments.return_value = fake_enrollments

    response = member_client.get("/api/enrollments")

    assert response.status_code == 200
    assert response.json() == fake_enrollments


@patch("app.api.enrollments.get_enrollment_by_id_service")
def test_get_enrollment(
    mock_get_enrollment,
    member_client,
):

    fake_enrollment = {
        "id": 1,
        "member_id": 2,
        "course_id": 1,
    }

    mock_get_enrollment.return_value = fake_enrollment

    response = member_client.get("/api/enrollments/1")

    assert response.status_code == 200
    assert response.json() == fake_enrollment


@patch("app.api.enrollments.update_enrollment_service")
def test_update_enrollment(
    mock_update_enrollment,
    member_client,
):

    fake_enrollment = {
        "id": 1,
        "member_id": 2,
        "course_id": 1,
        "status": "completed",
    }

    mock_update_enrollment.return_value = fake_enrollment

    response = member_client.patch(
        "/api/enrollments/1",
        json={
            "status": "completed",
        },
    )

    assert response.status_code == 200
    assert response.json() == fake_enrollment


@patch("app.api.enrollments.delete_enrollment_service")
def test_delete_enrollment(
    mock_delete_enrollment,
    member_client,
):

    mock_delete_enrollment.return_value = None

    response = member_client.delete("/api/enrollments/1")

    assert response.status_code == 204