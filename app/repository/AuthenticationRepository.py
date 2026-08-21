from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Member
from app.schemas.member.MemberCreate import MemberCreate

async def register_member(
        member: MemberCreate,
        session: AsyncSession
):
    member = Member(
        name = member.name,
        email = member.email,
        password = member.password,
        role = member.role
    )

    session.add(member)
    await session.commit()
    return member

async def get_member_by_email(
        email: str,
        session: AsyncSession
):
    member = await session.execute(
        select(Member).where(Member.email == email)
    )
    return member.scalar_one_or_none()