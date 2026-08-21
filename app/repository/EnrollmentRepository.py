
from sqlalchemy import select

from app.db.models import Enrollment
from app.schemas.enrollment.EnrollmentCreate import CreateEnrollment
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.enrollment.EnrollmentUpdate import UpdateEnrollment

async def create_enrollment(
    enrollment: CreateEnrollment,
    session: AsyncSession
):
    enrollment = Enrollment(
        member_id = enrollment.member_id,
        course_id = enrollment.course_id
    )

    await session.add(enrollment)
    await session.commit()
    return enrollment

async def get_enrollment_by_id(
    id: int,
    session: AsyncSession
):
    enrollment = await session.execute(
        select(Enrollment).where(Enrollment.id == id)
    )

    return enrollment.scalar_one_or_none()

async def get_enrollments(
    session: AsyncSession
):
    enrollments = await session.execute(
        select(Enrollment)
    )

    return enrollments.scalars().all()

async def update_enrollment(
    id: int,
    update_enrollment: UpdateEnrollment,
    session: AsyncSession
):
    enrollment = await get_enrollment_by_id(
        id = id,
        session = session
    )

    if enrollment == None:
        return None
    else:
        if update_enrollment.member_id:
            enrollment.member_id = update_enrollment.member_id
        if update_enrollment.course_id:
            enrollment.course_id = update_enrollment.course_id

    await session.commit()
    return enrollment

async def delete_enrollment(
    id: int,
    session: AsyncSession
):
    enrollment = await get_enrollment_by_id(
        id = id,
        session = session
    )

    if enrollment == None:
        return None

    await session.delete(enrollment)
    await session.commit()
    return enrollment