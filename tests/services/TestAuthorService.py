from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.schemas.author.AuthorCreate import AuthorCreate
from app.schemas.author.AuthorUpdate import AuthorUpdate
from app.services.AuthorService import create_author_service, get_author_by_id_service, get_authors_service, update_author_service, delete_author_service


@pytest.mark.asyncio
@patch("app.services.AuthorService.create_author")
async def test_create_author_service(mock_create_author):

    session = MagicMock()

    fake_author = MagicMock()
    fake_author.id = 1
    fake_author.name = "Test Author"

    mock_create_author.return_value = fake_author

    author = AuthorCreate(
        name = "Test Author"
    )

    result = await create_author_service(
        author=author,
        session=session
    )

    assert result == fake_author


@pytest.mark.asyncio
@patch("app.services.AuthorService.get_author_by_id")
async def test_get_author_by_id_service(mock_get_author_by_id):

    session = MagicMock()

    fake_author = MagicMock()
    fake_author.id = 1
    fake_author.name = "Test Author"

    mock_get_author_by_id.return_value = fake_author

    result = await get_author_by_id_service(
        id=1,
        session=session
    )

    assert result == fake_author


@pytest.mark.asyncio
@patch("app.services.AuthorService.get_authors")
async def test_get_authors_service(mock_get_authors):

    session = MagicMock()

    fake_authors = [
        MagicMock(id=1, name="Author 1"),
        MagicMock(id=2, name="Author 2")
    ]

    mock_get_authors.return_value = fake_authors

    result = await get_authors_service(
        session=session
    )

    assert result == fake_authors


@pytest.mark.asyncio
@patch(
"app.services.AuthorService.update_author")
async def test_update_author_service(mock_update_author):

    session = MagicMock()

    fake_author = MagicMock()
    fake_author.id = 1
    fake_author.name = "Updated Author"

    mock_update_author.return_value = fake_author

    author_update = AuthorUpdate(
        name = "Updated Author"
    )

    result = await update_author_service(
        id=1,
        author_update=author_update,
        session=session
    )

    assert result == fake_author


@pytest.mark.asyncio
@patch("app.services.AuthorService.delete_author")
async def test_delete_author_service(mock_delete_author):

    session = MagicMock()

    fake_author = MagicMock()
    fake_author.id = 1
    fake_author.name = "Test Author"

    mock_delete_author.return_value = fake_author

    result = await delete_author_service(
        id=1,
        session=session
    )

    assert result == fake_author