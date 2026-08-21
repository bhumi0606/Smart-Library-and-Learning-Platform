import pytest
from unittest.mock import MagicMock, AsyncMock

from app.db.models.Author import Author
from app.schemas.author.AuthorUpdate import AuthorUpdate
from app.repository.AuthorRepository import create_author, delete_author, get_author_by_id, get_authors, update_author

@pytest.mark.asyncio
async def test_create_author():
    session = AsyncMock()
    session.commit = AsyncMock()
    fake_author = MagicMock()

    result_mock = AsyncMock()
    result_mock.scalar_one_or_none.return_value = fake_author

    session.execute = AsyncMock(return_value=result_mock)
    session.commit = AsyncMock()

    result = await create_author(
        author = fake_author,
        session = session
    )

    assert isinstance(result, Author)

@pytest.mark.asyncio
async def test_get_authors():
    session = AsyncMock()
    authors = MagicMock()

    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = [authors]

    session.execute = AsyncMock(return_value=result_mock)

    result = await get_authors(
        session = session
    )

    assert result == [authors]

@pytest.mark.asyncio
async def test_get_author_by_id():
    session = AsyncMock()
    author = MagicMock()

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = author

    session.execute = AsyncMock(return_value=result_mock)

    result = await get_author_by_id(
        id = 1,
        session = session
    )

    assert result == author

@pytest.mark.asyncio
async def test_update_author():
    session = AsyncMock()
    fake_author = MagicMock()
    fake_author.title = "Test"

    fake_author_update = AuthorUpdate(
        title = "Testing"
    )

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_author

    session.execute = AsyncMock(return_value=result_mock)
    session.commit = AsyncMock()

    result = await update_author(
        id = 1,
        update_author = fake_author_update,
        session = session
    )

    assert result == fake_author

@pytest.mark.asyncio
async def test_delete_author():
    session = AsyncMock()
    fake_author = MagicMock()
    fake_author.id = 1

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = fake_author

    session.execute = AsyncMock(return_value=result_mock)
    session.commit = AsyncMock()

    result = await delete_author(
        id = 1,
        session = session
    )

    assert result == fake_author