from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.authentication import get_current_user, require_librarian, require_member_access
from app.schemas.member.MemberUpdate import MemberUpdate
from app.services.MemberService import get_member_by_id_service, get_members_service, update_member_service, delete_member_service

member_router = APIRouter(
    dependencies=[Depends(get_current_user)],
    prefix="/members",
    tags=["Members"],
)


@member_router.get(
    "",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_200_OK,
)
async def get_members(
    session: AsyncSession = Depends(get_db),
):
    return await get_members_service(
        session=session,
    )


@member_router.get(
    "/{member_id}",
    dependencies=[Depends(require_member_access)],
    status_code=status.HTTP_200_OK,
)
async def get_member(
    member_id: int,
    session: AsyncSession = Depends(get_db),
):
    return await get_member_by_id_service(
        id=member_id,
        session=session,
    )


@member_router.patch(
    "/{member_id}",
    dependencies=[Depends(require_member_access)],
    status_code=status.HTTP_200_OK,
)
async def update_member(
    member_id: int,
    member_update: MemberUpdate,
    session: AsyncSession = Depends(get_db),
):
    return await update_member_service(
        id=member_id,
        member_update=member_update,
        session=session,
    )


@member_router.delete(
    "/{member_id}",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_member(
    member_id: int,
    session: AsyncSession = Depends(get_db),
):
    await delete_member_service(
        id=member_id,
        session=session,
    )