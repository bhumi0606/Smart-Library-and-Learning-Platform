from fastapi import HTTPException, status

from app.repository.CourseRepository import create_course, delete_course, get_course_by_id, get_courses, update_course
from app.schemas.course.CourseCreate import CreateCourse
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.course.CourseUpdate import UpdateCourse

async def create_course_service(
        course: CreateCourse,
        session: AsyncSession
):
    response = await create_course(
        course = course,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "Course is not added"
        )
    return response

async def get_course_by_id_service(
        id: int,
        session: AsyncSession
):
    response = await get_course_by_id(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"Course not found with id:{id}"
        )

    return response

async def get_courses_service(
        session: AsyncSession
):
    response = await get_courses(
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Course not found"
        )

    return response

async def update_course_service(
        id: int,
        course_update: UpdateCourse,
        session: AsyncSession
):
    response = await update_course(
        id = id,
        update_course = course_update,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"Course not found with id:{id}"
        )

    return response

async def delete_course_service(
        id: int,
        session: AsyncSession
):
    response = await delete_course(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"Course not found with id:{id}"
        )
        
    return response