
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch("app.api.loans.create_loan_service")
def test_create_loan(mock_create_loan):

    fake_loan = {
        "id": 1,
        "member_id": 1,
        "book_id": 1,
        "issued_at": "2026-08-22T10:00:00",
        "due_date": "2026-09-05T10:00:00",
        "return_date": None,
    }

    mock_create_loan.return_value = fake_loan

    response = client.post(
        "/api/loans",
        json={
            "member_id": 1,
            "book_id": 1,
            "issued_at": "2026-08-22T10:00:00",
            "due_date": "2026-09-05T10:00:00",
            "return_date": None,
        }
    )

    assert response.status_code == 201
    assert response.json() == fake_loan



@patch("app.api.loans.get_loans_service")
def test_get_loans(mock_get_loans):

    fake_loans = [
        {
            "id": 1,
            "member_id": 1,
            "book_id": 1,
            "issued_at": "2026-08-22T10:00:00",
            "due_date": "2026-09-05T10:00:00",
            "return_date": None,
        },
        {
            "id": 2,
            "member_id": 2,
            "book_id": 2,
            "issued_at": "2026-08-20T10:00:00",
            "due_date": "2026-09-03T10:00:00",
            "return_date": None,
        },
    ]

    mock_get_loans.return_value = fake_loans

    response = client.get("/api/loans")

    assert response.status_code == 200
    assert response.json() == fake_loans


@patch("app.api.loans.get_loan_by_id_service")
def test_get_loan(mock_get_loan):

    fake_loan = {
        "id": 1,
        "member_id": 1,
        "book_id": 1,
        "issued_at": "2026-08-22T10:00:00",
        "due_date": "2026-09-05T10:00:00",
        "return_date": None,
    }

    mock_get_loan.return_value = fake_loan

    response = client.get("/api/loans/1")

    assert response.status_code == 200
    assert response.json() == fake_loan


@patch("app.api.loans.update_loan_service")
def test_update_loan(mock_update_loan):

    fake_loan = {
        "id": 1,
        "member_id": 1,
        "book_id": 1,
        "issued_at": "2026-08-22T10:00:00",
        "due_date": "2026-09-05T00:00:00",
        "return_date": "2026-08-25T00:00:00",
    }

    mock_update_loan.return_value = fake_loan

    response = client.patch(
        "/api/loans/1",
        json={
            "return_date": "2026-08-25"
        }
    )

    assert response.status_code == 200
    assert response.json() == fake_loan

@patch("app.api.loans.delete_loan_service")
def test_delete_loan(mock_delete_loan):

    mock_delete_loan.return_value = None

    response = client.delete("/api/loans/1")

    assert response.status_code == 204