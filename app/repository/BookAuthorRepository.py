from sqlalchemy import select

from app.db.models.BookAuthor import BookAuthor
from app.schemas.bookAuthor import BookAuthorCreate
from sqlalchemy.ext.asyncio import AsyncSession

async def create_book_author(
        book_author: BookAuthorCreate,
        session: AsyncSession
):
    book_author = BookAuthor(
        book_id = book_author.book_id,
        author_id = book_author.author_id
    )

    await session.add(book_author)
    await session.commit()
    return book_author

async def get_book_author_by_id(
        id: int,
        session: AsyncSession
):
    book_author = await session.execute(
        select(BookAuthor).where(BookAuthor.id == id)
    )

    return book_author.scalar_one_or_none()

async def get_book_authors(
        session: AsyncSession
):
    book_authors = await session.execute(
        select(BookAuthor)
    )
    return book_authors.scalars().all()

async def delete_book_author(
        id: int,
        session: AsyncSession
):
    book_author = await get_book_author_by_id(
        id = id,
        session = session
    )
    if book_author == None:
        return None
    
    await session.delete(book_author)
    await session.commit()
    return book_author