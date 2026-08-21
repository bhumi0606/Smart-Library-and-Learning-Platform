from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.schemas.bookAuthor.BookAuthorCreate import CreateBookAuthor
from app.services.BookAuthorService import create_book_author_service, get_book_author_by_id_service, get_book_authors_service, delete_book_author_service

@pytest.mark.asyncio
@patch("app.services.BookAuthorService.create_book_author")
async def test_create_book_author_service(mock_create_book_author):

    session = MagicMock()

    fake_book_author = MagicMock()
    fake_book_author.id = 1
    fake_book_author.book_id = 1
    fake_book_author.author_id = 1

    mock_create_book_author.return_value = fake_book_author

    book_author = CreateBookAuthor(
        book_id=1,
        author_id=1
    )

    result = await create_book_author_service(
        book_author=book_author,
        session=session
    )

    assert result == fake_book_author


@pytest.mark.asyncio
@patch("app.services.BookAuthorService.get_book_author_by_id")
async def test_get_book_author_by_id_service(mock_get_book_author_by_id):

    session = MagicMock()

    fake_book_author = MagicMock()
    fake_book_author.id = 1
    fake_book_author.book_id = 1
    fake_book_author.author_id = 1

    mock_get_book_author_by_id.return_value = fake_book_author

    result = await get_book_author_by_id_service(
        id=1,
        session=session
    )

    assert result == fake_book_author


@pytest.mark.asyncio
@patch("app.services.BookAuthorService.get_book_authors")
async def test_get_book_authors_service(mock_get_book_authors):

    session = MagicMock()

    fake_book_authors = [
        MagicMock(
            id=1,
            book_id=1,
            author_id=1
        ),
        MagicMock(
            id=2,
            book_id=2,
            author_id=2
        )
    ]

    mock_get_book_authors.return_value = fake_book_authors

    result = await get_book_authors_service(
        session=session
    )

    assert result == fake_book_authors


@pytest.mark.asyncio
@patch("app.services.BookAuthorService.delete_book_author")
async def test_delete_book_author_service(mock_delete_book_author):

    session = MagicMock()

    fake_book_author = MagicMock()
    fake_book_author.id = 1
    fake_book_author.book_id = 1
    fake_book_author.author_id = 1

    mock_delete_book_author.return_value = fake_book_author

    result = await delete_book_author_service(
        id=1,
        session=session
    )

    assert result == fake_book_author