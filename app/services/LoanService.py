from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.BookEnums import BookStatus, BookType
from app.enums.RoleEnums import Role

from app.repository.BookRepository import get_book_by_id
from app.repository.LoanRepository import (
    create_loan,
    delete_loan,
    get_loan_by_id,
    get_loans,
    get_overdue_loans,
    return_loan,
    update_loan,
)
from app.repository.MemberRepository import get_member_by_id


async def create_loan_service(
    loan,
    current_user,
    session: AsyncSession,
):
    # Members can only create loans for themselves
    if current_user.role == Role.MEMBER:
        loan.member_id = current_user.id

    # Check member exists
    member = await get_member_by_id(
        id=loan.member_id,
        session=session,
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )

    # Check book exists
    book = await get_book_by_id(
        id=loan.book_id,
        session=session,
    )

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    # Physical books can only be borrowed when available
    if (
        book.book_type == BookType.PHYSICAL
        and book.status != BookStatus.AVAILABLE
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is not available",
        )

    # Create loan
    response = await create_loan(
        loan=loan,
        session=session,
    )

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan is not created",
        )

    # Physical book becomes borrowed
    if book.book_type == BookType.PHYSICAL:
        book.status = BookStatus.BORROWED

        await session.commit()
        await session.refresh(book)

    return response


async def get_loans_service(
    current_user,
    session: AsyncSession,
):
    # Librarian can see all loans
    if current_user.role == Role.LIBRARIAN:
        return await get_loans(
            session=session,
        )

    # Member can see only their own loans
    return await get_loans(
        session=session,
        member_id=current_user.id,
    )


async def get_loan_by_id_service(
    id: int,
    current_user,
    session: AsyncSession,
):
    loan = await get_loan_by_id(
        id=id,
        session=session,
    )

    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan not found with id: {id}",
        )

    # Members can only access their own loans
    if (
        current_user.role != Role.LIBRARIAN
        and loan.member_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own loan",
        )

    return loan


async def get_overdue_loans_service(
    current_user,
    session: AsyncSession,
):
    # Librarian can see all overdue loans
    if current_user.role == Role.LIBRARIAN:
        return await get_overdue_loans(
            session=session,
        )

    # Member can see only their overdue loans
    return await get_overdue_loans(
        session=session,
        member_id=current_user.id,
    )


async def return_loan_service(
    id: int,
    current_user,
    session: AsyncSession,
):
    loan = await get_loan_by_id(
        id=id,
        session=session,
    )

    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan not found with id: {id}",
        )

    # Members can only return their own loans
    if (
        current_user.role != Role.LIBRARIAN
        and loan.member_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only return your own loan",
        )

    # Prevent duplicate return
    if loan.return_date is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan has already been returned",
        )

    # Get book
    book = await get_book_by_id(
        id=loan.book_id,
        session=session,
    )

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    # Set return date
    response = await return_loan(
        id=id,
        session=session,
    )

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book could not be returned",
        )

    # Physical book becomes available again
    if book.book_type == BookType.PHYSICAL:
        book.status = BookStatus.AVAILABLE

        await session.commit()
        await session.refresh(book)

    return response


async def update_loan_service(
    id: int,
    loan_update,
    session: AsyncSession,
):
    response = await update_loan(
        id=id,
        loan_update=loan_update,
        session=session,
    )

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan not found with id: {id}",
        )

    return response


async def delete_loan_service(
    id: int,
    session: AsyncSession,
):
    response = await delete_loan(
        id=id,
        session=session,
    )

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan not found with id: {id}",
        )

    return response