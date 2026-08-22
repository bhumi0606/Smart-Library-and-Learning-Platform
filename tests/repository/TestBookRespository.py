import pytest
from unittest.mock import MagicMock, AsyncMock

from app.db.models.Book import Book
from app.repository.BookRepository import create_book, delete_book, get_book_by_id, get_books, update_book
from app.schemas.book.BookUpdate import UpdateBook

@pytest.mark.asyncio
async def test_create_book():
    session = AsyncMock()
    session.commit = AsyncMock()
    fake_book = MagicMock()
    fake_book.title = "Test"
    fake_book.published_date = "20/08/2026"
    fake_book.isbn = "TEST123"
    fake_book.book_type = "physical"
    fake_book.status = "available"

    result_mock = AsyncMock()
    result_mock.scalar_one_or_none.return_value = fake_book

    session.execute = AsyncMock(return_value=result_mock)
    session.add = MagicMock()
    session.commit = AsyncMock()

    result = await create_book(
        book = fake_book,
        session = session
    )

    assert isinstance(result, Book)

@pytest.mark.asyncio
async def test_get_books():
    session = AsyncMock()
    books = MagicMock()

    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = [books]

    session.execute = AsyncMock(return_value=result_mock)

    result = await get_books(
        session = session
    )

    assert result == [books]

@pytest.mark.asyncio
async def test_get_book_by_id():
    session = AsyncMock()
    book = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = book

    session.execute = AsyncMock(return_value=result_mock)

    result = await get_book_by_id(
        id = 1,
        session = session
    )

    assert result == book

@pytest.mark.asyncio
async def test_update_book():
    session = AsyncMock()
    fake_book = MagicMock()
    fake_book.title = "Test"

    fake_book_update = UpdateBook(
        title="Testing"
    )

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_book

    session.execute = AsyncMock(return_value=result_mock)
    session.commit = AsyncMock()

    result = await update_book(
        id = 1,
        update_book = fake_book_update,
        session = session
    )

    assert result == fake_book

@pytest.mark.asyncio
async def test_delete_book():
    fake_book = MagicMock()
    fake_book.id = 1
    session = AsyncMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_book

    session.execute = AsyncMock(return_value=result_mock)
    session.commit = AsyncMock()

    result = await delete_book(
        id = 1,
        session = session
    )

    assert result == fake_book