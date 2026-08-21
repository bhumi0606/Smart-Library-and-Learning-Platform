from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.MemberRepository import delete_member, get_member_by_id, get_members, update_member
from app.schemas.member.MemberUpdate import MemberUpdate

async def get_member_by_id_service(
        id: int,
        session: AsyncSession
):
    response = await get_member_by_id(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"member not found with id:{id}"
        )
    return response

async def get_members_service(
        session: AsyncSession
):
    response = await get_members(
        session= session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "member not found"
        )
    return response

async def update_member_service(
        id: int,
        member_update: MemberUpdate,
        session: AsyncSession
):
    response = await update_member(
        id = id,
        update_member = member_update,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="member not found"
        )
    return response

async def delete_member_service(
        id: int,
        session: AsyncSession
):
    response = await delete_member(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "member not found"
        )
    return response