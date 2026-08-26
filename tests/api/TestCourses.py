from unittest.mock import AsyncMock, patch


@patch("app.api.courses.create_course_service")
def test_create_course(
    mock_create_course,
    librarian_client,
):

    fake_course = {
        "id": 1,
        "name": "Python Programming",
        "description": "Learn Python",
    }

    mock_create_course.return_value = fake_course

    response = librarian_client.post(
        "/api/courses",
        json={
            "name": "Python Programming",
            "description": "Learn Python",
        },
    )

    assert response.status_code == 201
    assert response.json() == fake_course


@patch("app.api.courses.get_courses_service")
def test_get_courses(
    mock_get_courses,
    member_client,
):

    fake_courses = [
        {
            "id": 1,
            "name": "Python Programming",
            "description": "Learn Python",
        }
    ]

    mock_get_courses.return_value = fake_courses

    response = member_client.get("/api/courses")

    assert response.status_code == 200
    assert response.json() == fake_courses


@patch("app.api.courses.get_course_by_id_service")
def test_get_course(
    mock_get_course,
    member_client,
):

    fake_course = {
        "id": 1,
        "name": "Python Programming",
        "description": "Learn Python",
    }

    mock_get_course.return_value = fake_course

    response = member_client.get("/api/courses/1")

    assert response.status_code == 200
    assert response.json() == fake_course


@patch("app.api.courses.update_course_service")
def test_update_course(
    mock_update_course,
    librarian_client,
):

    fake_course = {
        "id": 1,
        "name": "Advanced Python",
        "description": "Advanced Python",
    }

    mock_update_course.return_value = fake_course

    response = librarian_client.patch(
        "/api/courses/1",
        json={
            "name": "Advanced Python",
        },
    )

    assert response.status_code == 200
    assert response.json() == fake_course


@patch("app.api.courses.delete_course_service")
def test_delete_course(
    mock_delete_course,
    librarian_client,
):

    mock_delete_course.return_value = None

    response = librarian_client.delete("/api/courses/1")

    assert response.status_code == 204