from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch("app.api.courses.create_course_service")
def test_create_course(mock_create_course):

    fake_course = {
        "id": 1,
        "title": "Python Course",
    }

    mock_create_course.return_value = fake_course

    response = client.post(
        "/api/courses",
        json={
            "title": "Python Course"
        }
    )

    assert response.status_code == 201
    assert response.json() == fake_course


@patch("app.api.courses.get_courses_service")
def test_get_courses(mock_get_courses):

    fake_courses = [
        {
            "id": 1,
            "title": "Python Course",
        },
        {
            "id": 2,
            "title": "FastAPI Course",
        },
    ]

    mock_get_courses.return_value = fake_courses

    response = client.get("/api/courses")

    assert response.status_code == 200
    assert response.json() == fake_courses

@patch("app.api.courses.get_course_by_id_service")
def test_get_course(mock_get_course):

    fake_course = {
        "id": 1,
        "title": "Python Course",
    }

    mock_get_course.return_value = fake_course

    response = client.get("/api/courses/1")

    assert response.status_code == 200
    assert response.json() == fake_course


@patch("app.api.courses.update_course_service")
def test_update_course(mock_update_course):

    fake_course = {
        "id": 1,
        "title": "Advanced Python Course",
    }

    mock_update_course.return_value = fake_course

    response = client.patch(
        "/api/courses/1",
        json={
            "title": "Advanced Python Course"
        }
    )

    assert response.status_code == 200
    assert response.json() == fake_course


@patch("app.api.courses.delete_course_service")
def test_delete_course(mock_delete_course):

    mock_delete_course.return_value = None

    response = client.delete("/api/courses/1")

    assert response.status_code == 204