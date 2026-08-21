from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.schemas.enrollment.EnrollmentCreate import CreateEnrollment
from app.schemas.enrollment.EnrollmentUpdate import UpdateEnrollment
from app.services.EnrollmentService import create_enrollment_service, get_enrollment_by_id_service, get_enrollments_service, update_enrollment_service, delete_enrollment_service


@pytest.mark.asyncio
@patch("app.services.EnrollmentService.create_enrollment")
async def test_create_enrollment_service(mock_create_enrollment):
    session = MagicMock()

    enrollment = CreateEnrollment(
        member_id=1,
        course_id=1
    )

    fake_enrollment = MagicMock()
    fake_enrollment.id = 1
    fake_enrollment.member_id = 1
    fake_enrollment.course_id = 1

    mock_create_enrollment.return_value = fake_enrollment

    result = await create_enrollment_service(
        enrollment=enrollment,
        session=session
    )

    assert result == fake_enrollment


@pytest.mark.asyncio
@patch("app.services.EnrollmentService.get_enrollment_by_id")
async def test_get_enrollment_by_id_service(mock_get_enrollment_by_id):
    session = MagicMock()

    fake_enrollment = MagicMock()
    fake_enrollment.id = 1
    fake_enrollment.member_id = 1
    fake_enrollment.course_id = 1

    mock_get_enrollment_by_id.return_value = fake_enrollment

    result = await get_enrollment_by_id_service(
        id=1,
        session=session
    )

    assert result == fake_enrollment


@pytest.mark.asyncio
@patch("app.services.EnrollmentService.get_enrollments")
async def test_get_enrollments_service(mock_get_enrollments):
    session = MagicMock()

    fake_enrollments = [
        MagicMock(
            id=1,
            member_id=1,
            course_id=1
        ),
        MagicMock(
            id=2,
            member_id=2,
            course_id=2
        )
    ]

    mock_get_enrollments.return_value = fake_enrollments

    result = await get_enrollments_service(
        session=session
    )

    assert result == fake_enrollments


@pytest.mark.asyncio
@patch("app.services.EnrollmentService.update_enrollment")
async def test_update_enrollment_service(mock_update_enrollment):
    session = MagicMock() 

    enrollment_update = UpdateEnrollment(
        status="completed"
    )

    fake_enrollment = MagicMock()
    fake_enrollment.id = 1
    fake_enrollment.status = "completed"

    mock_update_enrollment.return_value = fake_enrollment

    result = await update_enrollment_service(
        id=1,
        enrollment_update=enrollment_update,
        session=session
    )

    assert result == fake_enrollment


@pytest.mark.asyncio
@patch("app.services.EnrollmentService.delete_enrollment")
async def test_delete_enrollment_service(mock_delete_enrollment):
    session = MagicMock()

    fake_enrollment = MagicMock()
    fake_enrollment.id = 1

    mock_delete_enrollment.return_value = fake_enrollment

    result = await delete_enrollment_service(
        id=1,
        session=session
    )

    assert result == fake_enrollment