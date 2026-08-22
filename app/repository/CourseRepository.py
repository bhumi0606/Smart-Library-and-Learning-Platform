from sqlalchemy import select

from app.db.models import Course
from app.schemas.course.CourseCreate import CreateCourse
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.course.CourseUpdate import UpdateCourse

async def create_course(
        course: CreateCourse,
        session: AsyncSession
):
    course = Course(
        title = course.title,
        description = course.description
    )

    session.add(course)
    await session.commit()
    await session.refresh(course)
    return course

async def get_course_by_id(
        id: int,
        session: AsyncSession
):
    course = await session.execute(
        select(Course).where(Course.id == id)
    )

    return course.scalar_one_or_none()

async def get_courses(
        session: AsyncSession
):
    courses = await session.execute(
        select(Course)
    )

    return courses.scalars().all()

async def update_course(
        id: int,
        update_course: UpdateCourse,
        session: AsyncSession
):
    course = await get_course_by_id(
        id=id,
        session = session
    )
    if course == None:
        return None
    else:
        if update_course.title:
            course.title = update_course.title
        if update_course.description:
            course.description = update_course.description
    await session.commit()
    await session.refresh(course)
    return course

async def delete_course(
        id: int,
        session: AsyncSession
):
    course = await get_course_by_id(
        id=id,
        session = session
    )
    if course == None:
        return None

    await session.delete(course)
    await session.commit()

    return course