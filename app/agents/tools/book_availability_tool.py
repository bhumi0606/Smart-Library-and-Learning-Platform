from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.BookEnums import BookStatus, BookType
from app.repository.BookRepository import get_book_by_id


async def check_book_availability(
    book_id: int,
    session: AsyncSession,
):

    book = await get_book_by_id(
        id=book_id,
        session=session,
    )

    if book is None:
        return {
            "available": False,
            "book": None,
            "message": "Book not found.",
        }

    if book.book_type == BookType.DIGITAL:

        return {
            "available": True,
            "book": {
                "id": book.id,
                "title": book.title,
                "isbn": book.isbn,
                "book_type": book.book_type.value,
                "status": book.status.value,
            },
            "message": (
                f"'{book.title}' is available digitally."
            ),
        }

    if book.status == BookStatus.AVAILABLE:

        return {
            "available": True,
            "book": {
                "id": book.id,
                "title": book.title,
                "isbn": book.isbn,
                "book_type": book.book_type.value,
                "status": book.status.value,
            },
            "message": (
                f"'{book.title}' is currently available."
            ),
        }

    return {
        "available": False,
        "book": {
            "id": book.id,
            "title": book.title,
            "isbn": book.isbn,
            "book_type": book.book_type.value,
            "status": book.status.value,
        },
        "message": (
            f"'{book.title}' is currently unavailable."
        ),
    }
