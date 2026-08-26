from app.db.models import Author
from app.db.models.Book import Book
from app.schemas.book.BookCreate import CreateBook
from app.schemas.book.BookUpdate import UpdateBook

from app.enums.BookEnums import BookStatus, BookType

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

async def create_book(
    book: CreateBook,
    session: AsyncSession,
):
    new_book = Book(
        title=book.title,
        published_date=book.published_date,
        isbn=book.isbn,
        book_type=BookType(book.book_type),
        status=BookStatus(book.status),
    )

    session.add(new_book)

    await session.commit()
    await session.refresh(new_book)

    return new_book

def _normalize_status(status):
    if status is None:
        return None

    if hasattr(status, "value"):
        return str(status.value)

    return str(status)

async def get_books(
    session: AsyncSession,
    title: str | None = None,
    author: str | None = None,
    status=None,
    page: int = 1,
    limit: int = 10,
):
    page = max(page, 1)
    limit = max(min(limit, 100), 1)

    status_value = _normalize_status(status)

    query = (
        select(Book)
        .options(
            selectinload(Book.authors)
        )
    )

    if title:
        query = query.where(
            Book.title.ilike(
                f"%{title}%"
            )
        )

    if author:
        query = (
            query
            .join(Book.authors)
            .where(
                Author.name.ilike(
                    f"%{author}%"
                )
            )
        )

    if status_value:
        query = query.where(
            Book.status == status_value
        )

    count_query = select(
        func.count(
            func.distinct(Book.id)
        )
    )

    # Title filter
    if title:
        count_query = count_query.where(
            Book.title.ilike(
                f"%{title}%"
            )
        )

    # Author filter
    if author:
        count_query = (
            count_query
            .select_from(Book)
            .join(Book.authors)
            .where(
                Author.name.ilike(
                    f"%{author}%"
                )
            )
        )

    # Status filter
    if status_value:
        count_query = count_query.where(
            Book.status == status_value
        )

    total_result = await session.execute(
        count_query
    )

    total = total_result.scalar() or 0

    query = (
        query
        .distinct()
        .offset(
            (page - 1) * limit
        )
        .limit(limit)
    )

    result = await session.execute(
        query
    )

    books = (
        result
        .scalars()
        .unique()
        .all()
    )

    return books, total

async def get_book_by_id(
    id: int,
    session: AsyncSession,
):
    """
    Get one book by ID.

    Authors are eagerly loaded because the AI assistant
    serializes author information after retrieving a book.
    """

    result = await session.execute(
        select(Book)
        .options(
            selectinload(Book.authors)
        )
        .where(
            Book.id == id
        )
    )

    return result.scalar_one_or_none()

async def update_book(
    id: int,
    update_book: UpdateBook,
    session: AsyncSession,
):
    book = await get_book_by_id(
        id=id,
        session=session,
    )

    if book is None:
        return None
    
    if update_book.title is not None:
        book.title = update_book.title

    if update_book.published_date is not None:
        book.published_date = (
            update_book.published_date
        )

    if update_book.isbn is not None:
        book.isbn = update_book.isbn

    if update_book.book_type is not None:
        book.book_type = (
            BookType(update_book.book_type)
            if not isinstance(
                update_book.book_type,
                BookType,
            )
            else update_book.book_type
        )

    if update_book.status is not None:
        book.status = (
            BookStatus(update_book.status)
            if not isinstance(
                update_book.status,
                BookStatus,
            )
            else update_book.status
        )

    await session.commit()
    await session.refresh(book)

    return book

async def delete_book(
    id: int,
    session: AsyncSession,
):
    book = await get_book_by_id(
        id=id,
        session=session,
    )

    if book is None:
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
    
    status_value = _normalize_status(
        book.status
    )

    return {
        "book_id": book.id,
        "title": book.title,

        "available": (
            status_value
            == BookStatus.AVAILABLE.value
        ),

        "status": status_value,
    }