from unittest.mock import AsyncMock, patch


@patch("app.api.book_authors.create_book_author_service")
def test_create_book_author(
    mock_create_book_author,
    librarian_client,
):

    fake_book_author = {
        "id": 1,
        "book_id": 1,
        "author_id": 1,
    }

    mock_create_book_author.return_value = fake_book_author

    response = librarian_client.post(
        "/api/book-authors",
        json={
            "book_id": 1,
            "author_id": 1,
        },
    )

    assert response.status_code == 201
    assert response.json() == fake_book_author


@patch("app.api.book_authors.get_book_authors_service")
def test_get_book_authors(
    mock_get_book_authors,
    member_client,
):

    fake_book_authors = [
        {
            "id": 1,
            "book_id": 1,
            "author_id": 1,
        },
        {
            "id": 2,
            "book_id": 2,
            "author_id": 2,
        },
    ]

    mock_get_book_authors.return_value = fake_book_authors

    response = member_client.get("/api/book-authors")

    assert response.status_code == 200
    assert response.json() == fake_book_authors


@patch("app.api.book_authors.get_book_author_by_id_service")
def test_get_book_author(
    mock_get_book_author,
    member_client,
):

    fake_book_author = {
        "id": 1,
        "book_id": 1,
        "author_id": 1,
    }

    mock_get_book_author.return_value = fake_book_author

    response = member_client.get("/api/book-authors/1")

    assert response.status_code == 200
    assert response.json() == fake_book_author


@patch("app.api.book_authors.delete_book_author_service")
def test_delete_book_author(
    mock_delete_book_author,
    librarian_client,
):

    mock_delete_book_author.return_value = None

    response = librarian_client.delete(
        "/api/book-authors/1"
    )

    assert response.status_code == 204