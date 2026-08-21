from fastapi import HTTPException, status

from app.repository.BookAuthorRepository import create_book_author, delete_book_author, get_book_author_by_id, get_book_authors
from app.schemas.bookAuthor import BookAuthorCreate
from sqlalchemy.ext.asyncio import AsyncSession

async def create_book_author_service(
        book_author: BookAuthorCreate,
        session: AsyncSession
):
    response = await create_book_author(
        book_author = book_author,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "book author not added"
        )
    return response

async def get_book_author_by_id_service(
        id: int,
        session: AsyncSession
):
    response = await get_book_author_by_id(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"book author not found with id:{id}"
        )
    return response

async def get_book_authors_service(
        session: AsyncSession
):
    response = await get_book_authors(
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"book author not found"
        )
    return response

async def delete_book_author_service(
        id: int,
        session: AsyncSession
):
    response = await delete_book_author(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"book author not found with id:{id}"
        )
    return response
