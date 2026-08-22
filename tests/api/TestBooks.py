from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

@patch("app.api.books.create_book_service")
def test_create_book(mock_create_book):

    fake_book = {
        "id": 1,
        "title": "Test Book",
        "published_date": "2022-04-05",
        "isbn": "TEST123456",
        "book_type": "physical",
        "status": "available",
    }

    mock_create_book.return_value = fake_book

    response = client.post(
        "/api/books",
        json={
            "title": "Test Book",
            "published_date": "2022-04-05",
            "isbn": "TEST123456",
            "book_type": "physical",
            "status": "available",
        },
    )

    assert response.status_code == 201
    assert response.json() == fake_book

@patch("app.api.books.get_books_service")
def test_get_books(mock_get_books):

    fake_books = [
        {
            "id": 1,
            "title": "Book 1",
            "published_date": "2023-06-04",
            "isbn":"TEST123456",
            "book_type":"physical",
            "status":"available",
            "created_at":"2026-08-22T10:30:00Z"
        },
        {
            "id": 2,
            "title": "Book 2",
            "published_date": "2023-06-04",
            "isbn":"TEST123456",
            "book_type":"physical",
            "status":"available",
            "created_at":"2026-08-22T10:30:00Z"
        },
    ]

    mock_get_books.return_value = fake_books

    response = client.get("/api/books")

    assert response.status_code == 200
    assert response.json() == fake_books

@patch("app.api.books.get_book_by_id_service")
def test_get_book_by_id(mock_get_book):

    fake_book = {
        "id": 1,
        "title": "Book 1",
        "published_date": "2023-06-04",
        "isbn":"TEST123456",
        "book_type":"physical",
        "status":"available",
        "created_at":"2026-08-22T10:30:00Z"
    }

    mock_get_book.return_value = fake_book

    response = client.get("/api/books/1")

    assert response.status_code == 200
    assert response.json() == fake_book

@patch("app.api.books.update_book_service")
def test_update_book(mock_update_book):

    fake_book = {
        "id": 1,
        "title": "Book 1",
        "published_date": "2023-06-04",
        "isbn":"TEST123456",
        "book_type":"physical",
        "status":"available",
        "created_at":"2026-08-22T10:30:00Z"
    }

    mock_update_book.return_value = fake_book

    response = client.patch(
        "/api/books/1",
        json={
            "title": "Updated Book",
        },
    )

    assert response.status_code == 200
    assert response.json() == fake_book

@patch("app.api.books.delete_book_service")
def test_delete_book(mock_delete_book):

    mock_delete_book.return_value = None

    response = client.delete("/api/books/1")

    assert response.status_code == 204