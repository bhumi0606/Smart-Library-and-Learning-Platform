import math

from fastapi import HTTPException, status

from app.enums.BookEnums import BookStatus
from app.repository.BookRepository import create_book, delete_book, get_book_by_id, get_books, update_book
from app.schemas.book.BookCreate import CreateBook
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.book.BookUpdate import UpdateBook

async def create_book_service(
        book: CreateBook,
        session: AsyncSession
):
    response = await create_book(
        book = book,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "Book is not added"
        )
    return response

async def get_books_service(
    session: AsyncSession,
    title: str | None = None,
    author: str | None = None,
    book_status: BookStatus | None = None,
    page: int = 1,
    limit: int = 10,        
):

    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be greater than 0",
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100",
        )

    books, total = await get_books(
        session=session,
        title=title,
        author=author,
        status=book_status,
        page=page,
        limit=limit,
    )

    pages = math.ceil(total / limit) if total else 0

    return {
        "books": books,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages,
    }

async def get_book_by_id_service(
        id: int,
        session: AsyncSession
):
    response = await get_book_by_id(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"Books not found with id:{id}"
        )

    return response

async def update_book_service(
        id: int,
        book_update: UpdateBook,
        session: AsyncSession
):
    response = await update_book(
        id = id,
        update_book = book_update,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"Books not found with id:{id}"
        )

    return response

async def delete_book_service(
        id: int,
        session: AsyncSession
):
    response = await delete_book(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"Books not found with id:{id}"
        )
        
    return response