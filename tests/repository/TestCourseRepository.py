import pytest
from unittest.mock import AsyncMock, MagicMock

from app.db.models import Course
from app.repository.CourseRepository import create_course, delete_course, get_course_by_id, get_courses, update_course
from app.schemas.course.CourseUpdate import UpdateCourse

@pytest.mark.asyncio
async def test_create_course():
    session = AsyncMock()
    fake_course = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_course

    session.execute = AsyncMock(return_value=fake_course)
    session.commit = AsyncMock()

    result = await create_course(
        course = fake_course,
        session = session
    )

    assert isinstance(result, Course)

@pytest.mark.asyncio
async def test_get_course_by_id():
    session = AsyncMock()
    fake_course = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_course

    session.execute = AsyncMock(return_value = result_mock)

    result = await get_course_by_id(
        id = 1,
        session = session
    )

    assert result == fake_course

@pytest.mark.asyncio
async def test_get_courses():
    session = AsyncMock()
    fake_courses = MagicMock()

    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = [fake_courses]

    session.execute = AsyncMock(return_value = result_mock)

    result = await get_courses(
        session = session
    )

    assert result == [fake_courses]

@pytest.mark.asyncio
async def test_update_course():
    session = AsyncMock()
    fake_course = MagicMock()
    fake_course.title = "Test"

    fake_update_course = UpdateCourse(
        title = "Testing"
    )

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_course

    session.execute = AsyncMock(return_value=result_mock)
    session.commit = AsyncMock()

    result = await update_course(
        id = 1,
        update_course = fake_update_course,
        session = session
    )

    assert result == fake_course

@pytest.mark.asyncio
async def test_delete_course():
    session = AsyncMock()
    fake_course = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_course

    session.execute = AsyncMock(return_value = result_mock)
    session.commit = AsyncMock()

    result = await delete_course(
        id = 1,
        session = session
    )

    assert result == fake_course