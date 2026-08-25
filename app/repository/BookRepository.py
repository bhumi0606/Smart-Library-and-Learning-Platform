from app.db.models import Author
from app.db.models.Book import Book
from app.schemas.book.BookCreate import CreateBook
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.schemas.book.BookUpdate import UpdateBook
from app.enums.BookEnums import BookStatus, BookType
from sqlalchemy.orm import selectinload


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
    session: AsyncSession,
    title: str | None = None,
    author: str | None = None,
    status=None,
    page: int = 1,
    limit: int = 10,
):
    query = (
        select(Book)
        .options(
            selectinload(Book.authors)
        )
    )

    if title:
        query = query.where(
            Book.title.ilike(f"%{title}%")
        )

    if author:
        query = query.join(
            Book.authors
        ).where(
            Author.name.ilike(f"%{author}%")
        )

    if status:
        query = query.where(
            Book.status == status
        )

    count_query = select(
        func.count(func.distinct(Book.id))
    )

    if title:
        count_query = count_query.where(
            Book.title.ilike(f"%{title}%")
        )

    if author:
        count_query = (
            count_query
            .select_from(Book)
            .join(Book.authors)
            .where(
                Author.name.ilike(f"%{author}%")
            )
        )

    if status:
        count_query = count_query.where(
            Book.status == status
        )

    total_result = await session.execute(
        count_query
    )

    total = total_result.scalar() or 0

    query = (
        query
        .distinct()
        .offset((page - 1) * limit)
        .limit(limit)
    )

    result = await session.execute(query)

    books = result.scalars().unique().all()

    return books, total

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

async def check_book_availability(
    book_id: int,
    session: AsyncSession,
):
    book = await get_book_by_id(
        id=book_id,
        session=session,
    )

    if book is None:
        return None

    return {
        "book_id": book.id,
        "title": book.title,
        "available": book.status == BookStatus.AVAILABLE,
        "status": (
            book.status.value
            if hasattr(book.status, "value")
            else str(book.status)
        ),
    }