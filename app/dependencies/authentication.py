from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt_token import decode_token
from app.db.database import get_db
from app.db.models import Member
from app.enums.RoleEnums import Role
from app.repository.AuthenticationRepository import get_member_by_email


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)


async def get_current_user(
    token = Depends(oauth2_scheme),
    session = Depends(get_db),
):
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )

    email = payload.get("email")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    user = await get_member_by_email(email,session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


async def require_member(
    current_user = Depends(get_current_user),
):
    if current_user.role not in (
        Role.MEMBER,
        Role.LIBRARIAN,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    return current_user


async def require_member_access(
    member_id: int,
    current_user = Depends(get_current_user),
):
    if (
        current_user.role != Role.LIBRARIAN
        and current_user.id != member_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own member record",
        )

    return current_user


async def require_librarian(
    current_user = Depends(get_current_user),
):
    if current_user.role != Role.LIBRARIAN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Librarian access required",
        )

    return current_user