from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.BookEnums import BookStatus, BookType
from app.enums.RoleEnums import Role

from app.repository.BookRepository import get_book_by_id
from app.repository.LoanRepository import create_loan, delete_loan, get_loan_by_id, get_loans, get_overdue_loans, renew_loan, return_loan, update_loan
from app.services.DocumentService import generate_loan_receipt
from app.services.NotificationService import send_loan_receipt_email


async def create_loan_service(
    loan,
    current_user,
    session: AsyncSession,
):
    if current_user.role == Role.MEMBER:
        loan.member_id = current_user.id

    book = await get_book_by_id(
        id=loan.book_id,
        session=session,
    )

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    if (
        book.book_type == BookType.PHYSICAL
        and book.status != BookStatus.AVAILABLE
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is not available",
        )

    response = await create_loan(
        loan=loan,
        session=session,
    )

    if not response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan is not created",
        )

    if book.book_type == BookType.PHYSICAL:
        book.status = BookStatus.BORROWED

        await session.commit()
        await session.refresh(book)

    receipt_url, receipt_bytes = generate_loan_receipt(
        loan=response,
    )
    await send_loan_receipt_email(
        email=response.member.email,
        member_name=response.member.name,
        book_title=response.book.title,
        due_date=response.due_date,
        receipt_bytes=receipt_bytes,
    )
    return {
        "id": response.id,
        "member_id": response.member_id,
        "book_id": response.book_id,
        "issued_at": response.issued_at,
        "due_date": response.due_date,
        "return_date": response.return_date,
        "receipt_url": receipt_url,
    }

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

async def renew_loan_service(
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

    if (
        current_user.role != Role.LIBRARIAN
        and loan.member_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only renew your own loan.",
        )

    if loan.return_date is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This loan has already been returned.",
        )

    result = await renew_loan(
        id=id,
        session=session,
        days=14,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan could not be renewed.",
        )

    return result