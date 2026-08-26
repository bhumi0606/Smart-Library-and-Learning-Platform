from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from app.schemas.book.BookCreate import CreateBook
from app.schemas.book.BookUpdate import UpdateBook
from app.services.BookService import create_book_service, get_books_service, get_book_by_id_service, update_book_service, delete_book_service


@pytest.mark.asyncio
@patch("app.services.BookService.create_book")
async def test_create_book_service(mock_create_book):
    session = MagicMock()
    fake_book = MagicMock()

    mock_create_book.return_value = fake_book

    book = CreateBook(
        title="Test Book",
        published_date="2022-04-05",
        isbn="TEST123456",
        book_type="physical",
        status="available"
    )

    result = await create_book_service(
        book=book,
        session=session
    )

    assert result == fake_book


@pytest.mark.asyncio
@patch("app.services.BookService.get_books")
async def test_get_books_service(mock_get_books):
    session = MagicMock()
    fake_book = MagicMock()

    mock_get_books.return_value = fake_book

    result = await get_books_service(
        session=session
    )

    assert result == fake_book


@pytest.mark.asyncio
@patch("app.services.BookService.get_book_by_id")
async def test_get_book_by_id_service(mock_get_book_by_id):
    session = MagicMock()
    fake_book = MagicMock()

    mock_get_book_by_id.return_value = fake_book

    result = await get_book_by_id_service(
        id=1,
        session=session
    )

    assert result == fake_book


@pytest.mark.asyncio
@patch("app.services.BookService.update_book")
async def test_update_book_service(mock_update_book):
    session = MagicMock()
    fake_book = MagicMock()

    mock_update_book.return_value = fake_book

    book_update = UpdateBook(
        title="Updated Book"
    )

    result = await update_book_service(
        id=1,
        book_update=book_update,
        session=session
    )

    assert result == fake_book


@pytest.mark.asyncio
@patch("app.services.BookService.delete_book")
async def test_delete_book_service(mock_delete_book):
    session = MagicMock()
    fake_book = MagicMock()

    mock_delete_book.return_value = fake_book

    result = await delete_book_service(
        id=1,
        session=session
    )

    assert result == fake_book