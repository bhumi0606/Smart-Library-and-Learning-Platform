from fastapi import APIRouter, Depends, Request

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.authentication import get_current_user

from app.schemas.Reservation.ReservationCreate import ReservationCreate
from app.schemas.Reservation.ReservationResponse import ReservationResponse

from app.services.ReservationService import create_reservation_service, get_reservation_service, get_my_reservations_service, get_book_reservations_service, cancel_reservation_service
from app.core.rate_limiter import limiter

reservation_router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"],
)

@reservation_router.post(
    "",
    response_model=ReservationResponse,
)
@limiter.limit("20/minute")
async def create_reservation(
    request: Request,
    reservation: ReservationCreate,
    current_user=Depends(
        get_current_user
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    return await create_reservation_service(
        member_id=current_user.id,
        book_id=reservation.book_id,
        expires_at=reservation.expires_at,
        session=session,
    )

@reservation_router.get(
    "/my",
    response_model=list[ReservationResponse],
)
@limiter.limit("20/minute")
async def get_my_reservations(
    request: Request,
    current_user=Depends(
        get_current_user
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    return await get_my_reservations_service(
        current_user=current_user,
        session=session,
    )

@reservation_router.get(
    "/{id}",
    response_model=ReservationResponse,
)
@limiter.limit("20/minute")
async def get_reservation(
    request: Request,
    id: int,
    current_user=Depends(
        get_current_user
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    return await get_reservation_service(
        id=id,
        current_user=current_user,
        session=session,
    )

@reservation_router.get(
    "/book/{book_id}",
    response_model=list[ReservationResponse],
)
@limiter.limit("20/minute")
async def get_book_reservations(
    request: Request,
    book_id: int,
    session: AsyncSession = Depends(
        get_db
    ),
):

    return await get_book_reservations_service(
        book_id=book_id,
        session=session,
    )

@reservation_router.delete(
    "/{id}",
    response_model=ReservationResponse,
)
@limiter.limit("20/minute")
async def cancel_reservation(
    request: Request,
    id: int,
    current_user=Depends(
        get_current_user
    ),
    session: AsyncSession = Depends(
        get_db
    ),
):

    return await cancel_reservation_service(
        id=id,
        current_user=current_user,
        session=session,
    )