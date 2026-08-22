from unittest.mock import AsyncMock, patch


@patch("app.api.books.create_book_service")
def test_create_book(
    mock_create_book,
    librarian_client,
):
    fake_book = {
        "id": 1,
        "title": "Machine Learning",
        "published_date": "2026-01-01",
        "isbn": "9781234567890",
        "book_type": "physical",
        "status": "available",
        "created_at": "2026-08-22T10:00:00",
    }

    mock_create_book.return_value = fake_book

    response = librarian_client.post(
        "/api/books",
        json={
            "title": "Machine Learning",
            "published_date": "2026-01-01",
            "isbn": "9781234567890",
            "book_type": "physical",
            "status": "available",
        },
    )

    assert response.status_code == 201
    assert response.json() == fake_book


@patch("app.api.books.get_books_service")
def test_get_books(
    mock_get_books,
    member_client,
):
    fake_books = [
        {
            "id": 1,
            "title": "Python Basics",
            "published_date": "2026-01-01",
            "isbn": "9781234567890",
            "book_type": "physical",
            "status": "available",
            "created_at": "2026-08-22T10:00:00",
        },
        {
            "id": 2,
            "title": "Machine Learning",
            "published_date": "2026-02-01",
            "isbn": "9781234567891",
            "book_type": "digital",
            "status": "available",
            "created_at": "2026-08-22T10:00:00",
        },
    ]

    mock_get_books.return_value = fake_books

    response = member_client.get("/api/books")

    assert response.status_code == 200
    assert response.json() == fake_books


@patch("app.api.books.get_book_by_id_service")
def test_get_book_by_id(
    mock_get_book,
    member_client,
):
    fake_book = {
        "id": 1,
        "title": "Machine Learning",
        "published_date": "2026-01-01",
        "isbn": "9781234567890",
        "book_type": "physical",
        "status": "available",
        "created_at": "2026-08-22T10:00:00",
    }

    mock_get_book.return_value = fake_book

    response = member_client.get("/api/books/1")

    assert response.status_code == 200
    assert response.json() == fake_book


@patch("app.api.books.update_book_service")
def test_update_book(
    mock_update_book,
    librarian_client,
):
    fake_book = {
        "id": 1,
        "title": "Updated Book",
        "published_date": "2026-01-01",
        "isbn": "9781234567890",
        "book_type": "physical",
        "status": "available",
        "created_at": "2026-08-22T10:00:00",
    }

    mock_update_book.return_value = fake_book

    response = librarian_client.patch(
        "/api/books/1",
        json={
            "title": "Updated Book",
        },
    )

    assert response.status_code == 200
    assert response.json() == fake_book


@patch("app.api.books.delete_book_service")
def test_delete_book(
    mock_delete_book,
    librarian_client,
):
    mock_delete_book.return_value = None

    response = librarian_client.delete("/api/books/1")

    assert response.status_code == 204