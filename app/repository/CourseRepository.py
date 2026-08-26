from sqlalchemy import func, or_, select

from app.db.models import Course
from app.schemas.course.CourseCreate import CreateCourse
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.course.CourseUpdate import UpdateCourse

async def create_course(
        course: CreateCourse,
        session: AsyncSession
):
    course = Course(
        name = course.name,
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
    session: AsyncSession,
    name: str | None = None,
    description: str | None = None,
    page: int = 1,
    limit: int = 100,
):
    conditions = []

    if name:
        conditions.append(
            Course.name.ilike(f"%{name}%")
        )

    if description:
        conditions.append(
            Course.description.ilike(f"%{description}%")
        )

    # Total count
    count_query = select(
        func.count(Course.id)
    )

    if conditions:
        count_query = count_query.where(
            or_(*conditions)
        )

    count_result = await session.execute(
        count_query
    )

    total = count_result.scalar_one()

    # Course query
    query = select(Course)

    if conditions:
        query = query.where(
            or_(*conditions)
        )

    # Pagination safety
    page = max(page, 1)
    limit = min(max(limit, 1), 100)

    offset = (page - 1) * limit

    query = (
        query
        .offset(offset)
        .limit(limit)
        .order_by(Course.id)
    )

    result = await session.execute(query)

    courses = result.scalars().all()

    return courses, total

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