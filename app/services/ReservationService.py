from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.BookEnums import BookStatus
from app.repository.BookRepository import get_book_by_id

from app.repository.ReservationRepository import (
    cancel_reservation,
    create_reservation,
    get_active_reservation,
    get_book_reservations,
    get_member_reservations,
    get_reservation_by_id,
)


async def create_reservation_service(
    member_id: int,
    book_id: int,
    expires_at,
    session: AsyncSession,
):

    book = await get_book_by_id(
        id=book_id,
        session=session,
    )

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    # If book is available, there is no reason to reserve it.
    if book.status == BookStatus.AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is currently available. You can borrow it directly.",
        )

    existing = await get_active_reservation(
        member_id=member_id,
        book_id=book_id,
        session=session,
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active reservation for this book.",
        )

    reservation = await create_reservation(
        member_id=member_id,
        book_id=book_id,
        expires_at=expires_at,
        session=session,
    )

    return reservation


async def get_reservation_service(
    id: int,
    current_user,
    session: AsyncSession,
):

    reservation = await get_reservation_by_id(
        id=id,
        session=session,
    )

    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation not found with id: {id}",
        )

    if (
        reservation.member_id != current_user.id
        and current_user.role.value != "librarian"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own reservation.",
        )

    return reservation


async def get_my_reservations_service(
    current_user,
    session: AsyncSession,
):

    return await get_member_reservations(
        member_id=current_user.id,
        session=session,
    )


async def get_book_reservations_service(
    book_id: int,
    session: AsyncSession,
):

    return await get_book_reservations(
        book_id=book_id,
        session=session,
    )


async def cancel_reservation_service(
    id: int,
    current_user,
    session: AsyncSession,
):

    reservation = await get_reservation_by_id(
        id=id,
        session=session,
    )

    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation not found with id: {id}",
        )

    if (
        reservation.member_id != current_user.id
        and current_user.role.value != "librarian"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only cancel your own reservation.",
        )

    if reservation.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reservation is not active.",
        )

    return await cancel_reservation(
        id=id,
        session=session,
    )