from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.authentication import get_current_user, require_librarian
from app.schemas.bookAuthor.BookAuthorCreate import CreateBookAuthor
from app.services.BookAuthorService import create_book_author_service, get_book_author_by_id_service, get_book_authors_service, delete_book_author_service

book_author_router = APIRouter(
    dependencies=[Depends(get_current_user)],
    prefix="/book-authors",
    tags=["Book Authors"],
)


@book_author_router.post(
    "",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_201_CREATED,
)
async def create_book_author(
    book_author: CreateBookAuthor,
    session: AsyncSession = Depends(get_db),
):
    return await create_book_author_service(
        book_author=book_author,
        session=session,
    )


@book_author_router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_book_authors(
    session: AsyncSession = Depends(get_db),
):
    return await get_book_authors_service(
        session=session,
    )


@book_author_router.get(
    "/{book_author_id}",
    status_code=status.HTTP_200_OK,
)
async def get_book_author(
    book_author_id: int,
    session: AsyncSession = Depends(get_db),
):
    return await get_book_author_by_id_service(
        id=book_author_id,
        session=session,
    )


@book_author_router.delete(
    "/{book_author_id}",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book_author(
    book_author_id: int,
    session: AsyncSession = Depends(get_db),
):
    await delete_book_author_service(
        id=book_author_id,
        session=session,
    )