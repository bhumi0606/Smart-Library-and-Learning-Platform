from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.authentication import get_current_user
from app.schemas.enrollment.EnrollmentCreate import CreateEnrollment
from app.schemas.enrollment.EnrollmentUpdate import UpdateEnrollment
from app.services.EnrollmentService import create_enrollment_service, get_enrollment_by_id_service, get_enrollments_service, update_enrollment_service, delete_enrollment_service
from app.core.rate_limiter import limiter

enrollment_router = APIRouter(
    dependencies=[Depends(get_current_user)],
    prefix="/enrollments",
    tags=["Enrollments"],
)

@enrollment_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("20/minute")
async def create_enrollment(
    request: Request,
    enrollment: CreateEnrollment,
    session: AsyncSession = Depends(get_db),
):
    return await create_enrollment_service(
        enrollment=enrollment,
        session=session,
    )

@enrollment_router.get(
    "",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("20/minute")
async def get_enrollments(
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    return await get_enrollments_service(
        session=session,
    )

@enrollment_router.get(
    "/{enrollment_id}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("20/minute")
async def get_enrollment(
    request: Request,
    enrollment_id: int,
    session: AsyncSession = Depends(get_db),
):
    return await get_enrollment_by_id_service(
        id=enrollment_id,
        session=session,
    )

@enrollment_router.patch(
    "/{enrollment_id}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("20/minute")
async def update_enrollment(
    request: Request,
    enrollment_id: int,
    enrollment_update: UpdateEnrollment,
    session: AsyncSession = Depends(get_db),
):
    return await update_enrollment_service(
        id=enrollment_id,
        enrollment_update=enrollment_update,
        session=session,
    )

@enrollment_router.delete(
    "/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("20/minute")
async def delete_enrollment(
    request: Request,
    enrollment_id: int,
    session: AsyncSession = Depends(get_db),
):
    await delete_enrollment_service(
        id=enrollment_id,
        session=session,
    )