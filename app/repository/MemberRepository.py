from app.db.models.Member import Member
from app.schemas.member.MemberUpdate import MemberUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_member_by_id(
        id:int,
        session: AsyncSession
    ):
    member = await session.execute(
        select(Member).where(Member.id == id)
    )
    return member.scalar_one_or_none()

async def get_members(
        session: AsyncSession
    ):
    members = await session.execute(
        select(Member)
    )
    return members.scalars().all()

async def update_member(
        id: int,
        update_member: MemberUpdate,
        session: AsyncSession
    ):
    old_member = await get_member_by_id(id,session)
    if old_member == None:
        return None
    else:
        if update_member.name:
            old_member.name = update_member.name
        if update_member.email:
            old_member.email = update_member.email

    await session.commit()
    await session.refresh(old_member)
    return old_member

async def delete_member(
        id: int,
        session: AsyncSession
    ):
    member = await get_member_by_id(id,session)
    if member == None:
        return None
    
    await session.delete(member)
    await session.commit()
    return member
