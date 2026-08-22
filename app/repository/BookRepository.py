from app.db.models.Book import Book
from app.schemas.book.BookCreate import CreateBook
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.book.BookUpdate import UpdateBook
from app.enums.BookEnums import BookStatus, BookType


async def create_book(
    book: CreateBook,
    session: AsyncSession
):
    book = Book(
        title = book.title,
        published_date = book.published_date,
        isbn = book.isbn,
        book_type = BookType(book.book_type),
        status = BookStatus(book.status)
    )

    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book

async def get_books(
        session: AsyncSession
):
    books = await session.execute(
        select(Book)
    )
    return books.scalars().all()

async def get_book_by_id(
        id: int,
        session: AsyncSession
):
    book = await session.execute(
        select(Book).where(Book.id == id)
    )
    return book.scalar_one_or_none()

async def update_book(
        id: int,
        update_book: UpdateBook,
        session: AsyncSession
):
    book = await get_book_by_id(
        id = id,
        session = session
    )

    if book == None:
        return None
    else:
        if update_book.title:
            book.title = update_book.title
        if update_book.published_date:
            book.published_date = update_book.published_date
        if update_book.isbn:
            book.isbn = update_book.isbn
        if update_book.book_type:
            book.book_type = update_book.book_type
        if update_book.status:
            book.status = update_book.status

    await session.commit()
    await session.refresh(book)
    return book

async def delete_book(
        id: int,
        session: AsyncSession
):
    book = await get_book_by_id(
        id = id,
        session = session
    )
    if book == None:
        return None

    await session.delete(book)
    await session.commit()

    return book