from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch("app.api.authors.create_author_service")
def test_create_author(mock_create_author):

    fake_author = {
        "id": 1,
        "name": "Test Author",
    }

    mock_create_author.return_value = fake_author

    response = client.post(
        "/api/authors",
        json={
            "name": "Test Author"
        }
    )

    assert response.status_code == 201
    assert response.json() == fake_author


@patch("app.api.authors.get_authors_service")
def test_get_authors(mock_get_authors):

    fake_authors = [
        {
            "id": 1,
            "name": "Author 1",
        },
        {
            "id": 2,
            "name": "Author 2",
        },
    ]

    mock_get_authors.return_value = fake_authors

    response = client.get("/api/authors")

    assert response.status_code == 200
    assert response.json() == fake_authors


@patch("app.api.authors.get_author_by_id_service")
def test_get_author(mock_get_author):

    fake_author = {
        "id": 1,
        "name": "Test Author",
    }

    mock_get_author.return_value = fake_author

    response = client.get("/api/authors/1")

    assert response.status_code == 200
    assert response.json() == fake_author


@patch("app.api.authors.update_author_service")
def test_update_author(mock_update_author):

    fake_author = {
        "id": 1,
        "name": "Updated Author",
    }

    mock_update_author.return_value = fake_author

    response = client.patch(
        "/api/authors/1",
        json={
            "name": "Updated Author"
        }
    )

    assert response.status_code == 200
    assert response.json() == fake_author

@patch("app.api.authors.delete_author_service")
def test_delete_author(mock_delete_author):

    mock_delete_author.return_value = None

    response = client.delete("/api/authors/1")

    assert response.status_code == 204