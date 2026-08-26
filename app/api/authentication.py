from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.member.MemberLoginResponse import MemberLoginResponse
from app.schemas.member.MemberResponse import MemberResponse
from app.schemas.member.MemberCreate import MemberCreate
from app.services.AuthenticationService import register_member_service, login_member_service
from app.core.rate_limiter import limiter

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=MemberResponse
)
@limiter.limit("5/minute")
async def register_member(
    request: Request,
    member: MemberCreate,
    session: AsyncSession = Depends(get_db),
):
    return await register_member_service(
        member=member,
        session=session,
    )

@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=MemberLoginResponse
)
@limiter.limit("5/minute")
async def login_member(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    return await login_member_service(
        member=form_data,
        session=session,
    )