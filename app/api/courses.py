from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.authentication import get_current_user, require_librarian
from app.schemas.course.CourseCreate import CreateCourse
from app.schemas.course.CourseUpdate import UpdateCourse
from app.services.CourseService import create_course_service, get_course_by_id_service, get_courses_service, update_course_service, delete_course_service

course_router = APIRouter(
    dependencies=[Depends(get_current_user)],
    prefix="/courses",
    tags=["Courses"],
)


@course_router.post(
    "",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_201_CREATED,
)
async def create_course(
    course: CreateCourse,
    session: AsyncSession = Depends(get_db),
):
    return await create_course_service(
        course=course,
        session=session,
    )


@course_router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_courses(
    session: AsyncSession = Depends(get_db),
):
    return await get_courses_service(
        session=session,
    )


@course_router.get(
    "/{course_id}",
    status_code=status.HTTP_200_OK,
)
async def get_course(
    course_id: int,
    session: AsyncSession = Depends(get_db),
):
    return await get_course_by_id_service(
        id=course_id,
        session=session,
    )


@course_router.patch(
    "/{course_id}",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_200_OK,
)
async def update_course(
    course_id: int,
    course_update: UpdateCourse,
    session: AsyncSession = Depends(get_db),
):
    return await update_course_service(
        id=course_id,
        course_update=course_update,
        session=session,
    )


@course_router.delete(
    "/{course_id}",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_course(
    course_id: int,
    session: AsyncSession = Depends(get_db),
):
    await delete_course_service(
        id=course_id,
        session=session,
    )