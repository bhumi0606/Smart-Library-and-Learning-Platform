from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.authentication import get_current_user, require_librarian
from app.enums.BookEnums import BookStatus
from app.schemas.book.BookResponse import BookListResponse, BookResponse
from app.schemas.book.BookCreate import CreateBook
from app.schemas.book.BookUpdate import UpdateBook
from app.services.BookService import create_book_service, get_books_service, get_book_by_id_service, update_book_service, delete_book_service

book_router = APIRouter(
    dependencies=[Depends(get_current_user)],
    prefix="/books",
    tags=["Books"],     
)


@book_router.post(
    "",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    book: CreateBook,
    session: AsyncSession = Depends(get_db),
):
    return await create_book_service(
        book=book,
        session=session,
    )


@book_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=BookListResponse
)
async def get_books_api(
    title: str | None = None,
    author: str | None = None,
    book_status: BookStatus | None = None,
    page: int = 1,
    limit: int = 10,
    session: AsyncSession = Depends(get_db),
):

    return await get_books_service(
        session=session,
        title=title,
        author=author,
        book_status=book_status,
        page=page,
        limit=limit,
    )


@book_router.get(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model= BookResponse
)
async def get_book(
    book_id: int,
    session: AsyncSession = Depends(get_db),
):
    return await get_book_by_id_service(
        id=book_id,
        session=session,
    )


@book_router.patch(
    "/{book_id}",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_200_OK,
)
async def update_book(
    book_id: int,
    book_update: UpdateBook,
    session: AsyncSession = Depends(get_db),
):
    return await update_book_service(
        id=book_id,
        book_update=book_update,
        session=session,
    )


@book_router.delete(
    "/{book_id}",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(get_db),
):
    await delete_book_service(
        id=book_id,
        session=session,
    )