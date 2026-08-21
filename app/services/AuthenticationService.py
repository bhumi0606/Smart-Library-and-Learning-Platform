from fastapi import HTTPException, status

from app.repository.AuthenticationRepository import get_member_by_email, register_member
from app.schemas.member.TokenData import TokenData
from app.schemas.member.MemberCreate import MemberCreate
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.hashing import hash_password, verify_password
from app.core.jwt_token import create_access_token

async def register_member_service(
        member: MemberCreate,
        session: AsyncSession
):
    member.password = hash_password(member.password)
    response = await register_member(
        member = member,
        session = session
    )
    return response

async def login_member_service(member,session):
    email = member.username
    password = member.password
    member = await get_member_by_email(email,session)
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    if not verify_password(password, member.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    data = TokenData(
        email = member.email,
        role = member.role
    )
    token = create_access_token(data)
    return token
