from fastapi import HTTPException, status

from app.repository.EnrollmentRepository import create_enrollment, delete_enrollment, get_enrollment_by_id, get_enrollments, update_enrollment
from app.schemas.enrollment import EnrollmentUpdate
from app.schemas.enrollment.EnrollmentCreate import CreateEnrollment
from sqlalchemy.ext.asyncio import AsyncSession

async def create_enrollment_service(
        enrollment: CreateEnrollment,
        session: AsyncSession
):
    response = await create_enrollment(
        enrollment = enrollment,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "Enrollment is not added"
        )
    
    return response

async def get_enrollment_by_id_service(
        id: int,
        session: AsyncSession
):
    response = await get_enrollment_by_id(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"Enrollment not found with id:{id}"
        )

    return response

async def get_enrollments_service(
        session: AsyncSession
):
    response = await get_enrollments(
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Enrollment not found"
        )

    return response

async def update_enrollment_service(
        id: int,
        enrollment_update: EnrollmentUpdate,
        session: AsyncSession
):
    response = await update_enrollment(
        id = id,
        update_enrollment = enrollment_update,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"Enrollment not found with id:{id}"
        )

    return response

async def delete_enrollment_service(
        id: int,
        session: AsyncSession
):
    response = await delete_enrollment(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"Enrollment not found with id:{id}"
        )
        
    return response