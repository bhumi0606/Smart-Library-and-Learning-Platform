from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.Reservation import Reservation


async def create_reservation(
    member_id: int,
    book_id: int,
    expires_at,
    session: AsyncSession,
):

    reservation = Reservation(
        member_id=member_id,
        book_id=book_id,
        expires_at=expires_at,
        status="active",
    )

    session.add(reservation)

    await session.commit()

    result = await session.execute(
        select(Reservation)
        .options(
            selectinload(Reservation.member),
            selectinload(Reservation.book),
        )
        .where(
            Reservation.id == reservation.id
        )
    )

    return result.scalar_one()


async def get_reservation_by_id(
    id: int,
    session: AsyncSession,
):

    result = await session.execute(
        select(Reservation)
        .options(
            selectinload(Reservation.member),
            selectinload(Reservation.book),
        )
        .where(
            Reservation.id == id
        )
    )

    return result.scalar_one_or_none()


async def get_member_reservations(
    member_id: int,
    session: AsyncSession,
):

    result = await session.execute(
        select(Reservation)
        .options(
            selectinload(Reservation.book),
        )
        .where(
            Reservation.member_id == member_id
        )
        .order_by(
            Reservation.reserved_at.desc()
        )
    )

    return result.scalars().all()


async def get_active_reservation(
    member_id: int,
    book_id: int,
    session: AsyncSession,
):

    result = await session.execute(
        select(Reservation)
        .where(
            Reservation.member_id == member_id,
            Reservation.book_id == book_id,
            Reservation.status == "active",
        )
    )

    return result.scalar_one_or_none()


async def get_book_reservations(
    book_id: int,
    session: AsyncSession,
):

    result = await session.execute(
        select(Reservation)
        .options(
            selectinload(Reservation.member),
        )
        .where(
            Reservation.book_id == book_id,
            Reservation.status == "active",
        )
        .order_by(
            Reservation.reserved_at.asc()
        )
    )

    return result.scalars().all()


async def cancel_reservation(
    id: int,
    session: AsyncSession,
):

    reservation = await get_reservation_by_id(
        id=id,
        session=session,
    )

    if reservation is None:
        return None

    reservation.status = "cancelled"

    await session.commit()

    await session.refresh(reservation)

    return reservation