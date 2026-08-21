from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.schemas.course.CourseCreate import CreateCourse
from app.schemas.course.CourseUpdate import UpdateCourse
from app.services.CourseService import create_course_service, get_course_by_id_service, get_courses_service, update_course_service, delete_course_service

@pytest.mark.asyncio
@patch("app.services.CourseService.create_course")
async def test_create_course_service(mock_create_course):
    session = MagicMock()

    course = CreateCourse(
        title="Python Course"
    )

    fake_course = MagicMock()
    fake_course.id = 1
    fake_course.name = "Python Course"

    mock_create_course.return_value = fake_course

    result = await create_course_service(
        course=course,
        session=session
    )

    assert result == fake_course


@pytest.mark.asyncio
@patch("app.services.CourseService.get_course_by_id")
async def test_get_course_by_id_service(mock_get_course_by_id):
    session = MagicMock()

    fake_course = MagicMock()
    fake_course.id = 1
    fake_course.name = "Python Course"

    mock_get_course_by_id.return_value = fake_course

    result = await get_course_by_id_service(
        id=1,
        session=session
    )

    assert result == fake_course


@pytest.mark.asyncio
@patch("app.services.CourseService.get_courses")
async def test_get_courses_service(mock_get_courses):
    session = MagicMock()

    fake_courses = [
        MagicMock(
            id=1,
            name="Python Course"
        ),
        MagicMock(
            id=2,
            name="FastAPI Course"
        )
    ]

    mock_get_courses.return_value = fake_courses

    result = await get_courses_service(
        session=session
    )

    assert result == fake_courses


@pytest.mark.asyncio
@patch("app.services.CourseService.update_course")
async def test_update_course_service(mock_update_course):
    session = MagicMock()

    course_update = UpdateCourse(
        name="Advanced Python Course"
    )

    fake_course = MagicMock()
    fake_course.id = 1
    fake_course.name = "Advanced Python Course"

    mock_update_course.return_value = fake_course

    result = await update_course_service(
        id=1,
        course_update=course_update,
        session=session
    )

    assert result == fake_course


@pytest.mark.asyncio
@patch("app.services.CourseService.delete_course")
async def test_delete_course_service(mock_delete_course):
    session = MagicMock()

    fake_course = MagicMock()
    fake_course.id = 1
    fake_course.name = "Python Course"

    mock_delete_course.return_value = fake_course

    result = await delete_course_service(
        id=1,
        session=session
    )

    assert result == fake_course