import pytest
from unittest.mock import MagicMock, AsyncMock

from app.db.models import BookAuthor
from app.repository.BookAuthorRepository import create_book_author, delete_book_author, get_book_author_by_id, get_book_authors

@pytest.mark.asyncio
async def test_create_book_author():
    session = AsyncMock()
    session.commit = AsyncMock()
    fake_book_author = MagicMock()

    result_mock = AsyncMock()
    result_mock.scalar_one_or_none.return_value = fake_book_author

    session.execute = AsyncMock(return_value=result_mock)
    session.add = MagicMock()
    session.commit = AsyncMock()

    result = await create_book_author(
        book_author = fake_book_author,
        session = session
    )

    assert isinstance(result, BookAuthor)

@pytest.mark.asyncio
async def test_get_book_author_by_id():
    session = AsyncMock()
    fake_book_author = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_book_author

    session.execute = AsyncMock(return_value = result_mock)
    result = await get_book_author_by_id(
        id = 1,
        session = session
    )

    assert result == fake_book_author

@pytest.mark.asyncio
async def test_get_book_authors():
    session = AsyncMock()
    fake_book_authors = MagicMock()

    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = [fake_book_authors]

    session.execute = AsyncMock(return_value = result_mock)

    result = await get_book_authors(
        session=session
    )

    assert result == [fake_book_authors]

@pytest.mark.asyncio
async def test_delete_book_author():
    session = AsyncMock()
    session.commit = AsyncMock()
    fake_book_author = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_book_author

    session.execute = AsyncMock(return_value=result_mock)
    
    result = await delete_book_author(
        id = 1,
        session = session
    )

    assert result == fake_book_author