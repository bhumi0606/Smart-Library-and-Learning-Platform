import pytest
from unittest.mock import MagicMock, AsyncMock

from app.db.models import Enrollment
from app.repository.EnrollmentRepository import create_enrollment, delete_enrollment, get_enrollment_by_id, get_enrollments, update_enrollment
from app.schemas.enrollment.EnrollmentUpdate import UpdateEnrollment
from app.schemas.member.MemberUpdate import MemberUpdate

@pytest.mark.asyncio
async def test_create_enrollment():
    session = AsyncMock()
    fake_enrollment = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_enrollment

    session.execute = AsyncMock(return_value=result_mock)
    session.add = MagicMock()
    session.commit = AsyncMock()

    result = await create_enrollment(
        enrollment = fake_enrollment,
        session = session
    )

    assert isinstance(result, Enrollment)

@pytest.mark.asyncio
async def test_get_enrollment_by_id():
    session = AsyncMock()
    fake_enrollment = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_enrollment

    session.execute = AsyncMock(return_value = result_mock)

    result = await get_enrollment_by_id(
        id = 1,
        session = session
    )

    assert result == fake_enrollment

@pytest.mark.asyncio
async def test_get_enrollments():
    session = AsyncMock()
    fake_enrollment = MagicMock()

    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = [fake_enrollment]

    session.execute = AsyncMock(return_value = result_mock)

    result = await get_enrollments(
        session = session
    )

    assert result == [fake_enrollment]

@pytest.mark.asyncio
async def test_update_enrollment():
    session = AsyncMock()
    fake_enrollment = MagicMock()
    fake_enrollment.member_id = 1

    fake_enrollment_update = UpdateEnrollment(
        member_id = 1
    )

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_enrollment

    session.execute = AsyncMock(return_value = result_mock)
    session.commit = AsyncMock()

    result = await update_enrollment(
        id = 1,
        update_enrollment = fake_enrollment_update,
        session = session
    )

    assert result == fake_enrollment

@pytest.mark.asyncio
async def test_delete_enrollment():
    session = AsyncMock()
    fake_enrollment = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_enrollment

    session.execute = AsyncMock(return_value = result_mock)
    session.commit = AsyncMock()

    result = await delete_enrollment(
        id = 1,
        session = session
    )

    assert result == fake_enrollment