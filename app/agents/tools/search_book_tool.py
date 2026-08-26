from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.BookRepository import get_books


async def search_books(
    session: AsyncSession,
    title: str | None = None,
    author: str | None = None,
    status=None,
    page: int = 1,
    limit: int = 10,
):

    books, total = await get_books(
        session=session,
        title=title,
        author=author,
        status=status,
        page=page,
        limit=limit,
    )

    results = []

    for book in books:

        results.append(
            {
                "id": book.id,
                "title": book.title,
                "published_date": (
                    book.published_date.isoformat()
                    if book.published_date
                    else None
                ),
                "isbn": book.isbn,
                "book_type": (
                    book.book_type.value
                    if hasattr(
                        book.book_type,
                        "value",
                    )
                    else str(book.book_type)
                ),
                "status": (
                    book.status.value
                    if hasattr(
                        book.status,
                        "value",
                    )
                    else str(book.status)
                ),
                "created_at": (
                    book.created_at.isoformat()
                    if book.created_at
                    else None
                ),
            }
        )

    return {
        "books": results,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (
            (total + limit - 1) // limit
            if limit > 0
            else 0
        ),
    }
