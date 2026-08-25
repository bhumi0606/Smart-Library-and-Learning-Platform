from datetime import datetime, timedelta, timezone
import re

from app.agents.tools.book_recommendation_tool import book_recommendation_tool

from app.agents.tools.book_tool import execute_book_tool

from app.graph.state import AssistantState

from app.rag.retrieval import retrieve_documents
from app.repository.BookRepository import get_book_by_id, get_books

from app.repository.LoanRepository import get_loans

from app.schemas.loan.LoanCreate import CreateLoan

from app.services.BookService import check_book_availability_service
from app.services.LoanService import create_loan_service, get_loans_service, renew_loan_service, return_loan_service
from app.services.ReservationService import create_reservation_service

async def execute_tasks(
    state: AssistantState,
):

    tasks = state.get(
        "tasks",
        [],
    )

    for task in tasks:

        state = await execute_task(
            task=task,
            state=state,
        )

    return state

async def execute_task(
    task: str,
    state: AssistantState,
):

    if task == "answer_general":
        return await answer_general(state)

    if task == "search_book_content":
        return await search_book_content(state)

    if task == "search_books":
        return await search_books(state)

    if task == "get_book":
        return await get_book(state)

    if task == "recommend_book":
        return await recommend_book(state)

    if task == "get_member_history":
        return await get_member_history(state)

    if task == "check_book_availability":
        return await check_book_availability(state)

    if task == "borrow_book":
        return await borrow_book(state)

    if task == "return_book":
        return await return_book(state)

    if task == "renew_loan":
        return await renew_loan(state)

    if task == "reserve_book": 
        return await reserve_book(state)

    return state

async def answer_general(
    state: AssistantState,
):

    state["answer"] = "Hello! I'm your Smart Library assistant. " \
        "I can help you with books, loans, " \
        "courses and library information."

    return state

async def search_book_content(
    state: AssistantState,
):

    result = await execute_book_tool(
        query=state["question"],
        top_k=5,
    )

    state["answer"] = result.get(
        "answer",
        "",
    )

    state["citations"] = result.get(
        "citations",
        [],
    )

    state["retrieved_chunks"] = result.get(
        "retrieved_chunks",
        [],
    )

    return state


async def search_books(
    state: AssistantState,
):
    session = state.get("session")

    if session is None:
        state["book_candidates"] = []
        state["book_total"] = 0
        state["answer"] = (
            "I could not access the library catalog."
        )
        return state

    books, total = await get_books(
        session=session,
        page=1,
        limit=100,
    )

    candidates = []

    for book in books:

        book_status = (
            book.status.value
            if hasattr(book.status, "value")
            else str(book.status)
        )

        book_type = (
            book.book_type.value
            if hasattr(book.book_type, "value")
            else str(book.book_type)
        )

        candidates.append(
            {
                "id": book.id,
                "title": book.title,
                "published_date": (
                    book.published_date.isoformat()
                    if book.published_date
                    else None
                ),
                "isbn": book.isbn,
                "book_type": book_type,
                "status": book_status,
            }
        )

    state["book_candidates"] = candidates
    state["book_total"] = len(candidates)

    print("\n========== BOOK SEARCH ==========")
    print("TOTAL BOOKS:", len(candidates))

    for book in candidates:
        print(
            f"ID={book['id']} "
            f"TITLE={book['title']} "
            f"TYPE={book['book_type']} "
            f"STATUS={book['status']}"
        )

    print("=================================\n")

    # No books
    if not candidates:
        state["answer"] = (
            "I couldn't find any books in the library."
        )
        return state

    question = state.get(
        "question",
        "",
    ).lower()

    # --------------------------------
    # AVAILABLE BOOKS
    # --------------------------------

    if "available" in question:

        available_books = [
            book
            for book in candidates
            if book["status"].lower() == "available"
        ]

        if not available_books:
            state["answer"] = (
                "There are currently no available books."
            )
            return state

        lines = []

        for book in available_books:
            lines.append(
                f"- {book['title']} "
                f"(ID: {book['id']}, "
                f"type: {book['book_type']})"
            )

        state["answer"] = (
            f"I found {len(available_books)} available books:\n"
            + "\n".join(lines)
        )

        return state

    # --------------------------------
    # GENERIC BOOK SEARCH
    # --------------------------------

    lines = []

    for book in candidates:
        lines.append(
            f"- {book['title']} "
            f"(ID: {book['id']}, "
            f"type: {book['book_type']}, "
            f"status: {book['status']})"
        )

    state["answer"] = (
        f"I found {len(candidates)} books:\n"
        + "\n".join(lines)
    )

    return state

async def get_book(
    state: AssistantState,
):

    session = state.get(
        "session"
    )

    book_id = state.get(
        "book_id"
    )

    if (
        session is None
        or book_id is None
    ):
        return state

    book = await get_book_by_id(
        id=book_id,
        session=session,
    )

    if book:

        state["recommended_book"] = {
            "id": book.id,
            "title": book.title,
            "isbn": book.isbn,
            "book_type": (
                book.book_type.value
                if hasattr(
                    book.book_type,
                    "value",
                )
                else str(book.book_type)
            ),
            "status": (
                book.status.value
                if hasattr(
                    book.status,
                    "value",
                )
                else str(book.status)
            ),
        }

    return state

async def get_member_history(
    state: AssistantState,
):
    session = state.get(
        "session"
    )

    current_user = state.get(
        "current_user"
    )

    if session is None or current_user is None:
        return state

    loans = await get_loans_service(
        current_user=current_user,
        session=session,
    )

    state["member_history"] = loans

    return state

async def recommend_book(
    state: AssistantState,
):
    candidates = state.get(
        "book_candidates",
        [],
    )

    if not candidates:
        state["recommended_book"] = None
        state["book_available"] = False
        state["answer"] = (
            "I couldn't find any books to recommend."
        )
        return state

    history = state.get(
        "member_history",
        [],
    )

    result = await book_recommendation_tool.execute(
        question=state["question"],
        member_history=history,
        candidates=candidates,
    )

    recommended_book = result.get(
        "recommended_book"
    )

    state["recommended_book"] = recommended_book

    state["recommendation_reason"] = result.get(
        "reason",
        "",
    )

    if recommended_book:

        state["book_available"] = (
            str(
                recommended_book.get(
                    "status",
                    "",
                )
            ).lower()
            == "available"
        )

        state["answer"] = (
            f"I recommend "
            f"'{recommended_book['title']}'. "
            f"{result.get('reason', '')}"
        )

    else:

        state["book_available"] = False

        state["answer"] = result.get(
            "reason",
            "I couldn't find a suitable book.",
        )

    return state

async def check_book_availability(
    state: AssistantState,
):
    session = state.get("session")

    if session is None:
        state["book_available"] = False
        state["answer"] = (
            "I could not access the library catalog."
        )
        return state

    question = state.get(
        "question",
        "",
    ).strip()

    # ---------------------------------------------------------
    # 1. Try book ID first
    # ---------------------------------------------------------
    book_id = state.get("book_id")

    if book_id is None:
        match = re.search(
            r"\bbook\s*(?:id\s*)?(\d+)\b",
            question.lower(),
        )

        if match:
            book_id = int(match.group(1))
            state["book_id"] = book_id

    book = None

    # ---------------------------------------------------------
    # 2. If book ID exists, get book directly
    # ---------------------------------------------------------
    if book_id is not None:

        book = await get_book_by_id(
            id=book_id,
            session=session,
        )

    # ---------------------------------------------------------
    # 3. Otherwise search catalog by title
    # ---------------------------------------------------------
    if book is None:

        books, _ = await get_books(
            session=session,
            page=1,
            limit=100,
        )

        normalized_question = question.lower()

        for candidate in books:

            title = candidate.title.lower()

            if title in normalized_question:
                book = candidate
                break

    # ---------------------------------------------------------
    # 4. Book not found
    # ---------------------------------------------------------
    if book is None:

        state["book_available"] = False
        state["answer"] = (
            "I could not find that book in the library catalog."
        )

        return state

    # ---------------------------------------------------------
    # 5. Store book information
    # ---------------------------------------------------------
    state["book_id"] = book.id

    state["recommended_book"] = {
        "id": book.id,
        "title": book.title,
        "isbn": book.isbn,
        "book_type": (
            book.book_type.value
            if hasattr(book.book_type, "value")
            else str(book.book_type)
        ),
        "status": (
            book.status.value
            if hasattr(book.status, "value")
            else str(book.status)
        ),
    }

    # ---------------------------------------------------------
    # 6. Check availability
    # ---------------------------------------------------------
    result = await check_book_availability_service(
        book_id=book.id,
        session=session,
    )

    state["book_available"] = result["available"]

    if result["available"]:

        state["answer"] = (
            f"Yes, '{result['title']}' is currently available."
        )

    else:

        state["answer"] = (
            f"No, '{result['title']}' is currently "
            f"{result['status']}."
        )

    state["availability_message"] = state["answer"]

    return state

async def borrow_book(
    state: AssistantState,
):

    session = state.get(
        "session"
    )

    current_user = state.get(
        "current_user"
    )

    recommended_book = state.get(
        "recommended_book"
    )

    book_available = state.get(
        "book_available",
        False,
    )

    if not book_available:

        state["loan_result"] = {
            "success": False,
            "message": (
                "The recommended book "
                "is not available."
            ),
        }

        return state

    if session is None or current_user is None or recommended_book is None:
        return state

    due_date = datetime.now(timezone.utc) + timedelta(days=14)

    loan = CreateLoan(
        member_id=current_user.id,
        book_id=recommended_book["id"],
        due_date=due_date,
    )

    result = await create_loan_service(
        loan=loan,
        current_user=current_user,
        session=session,
    )

    state["loan_result"] = {
        "success": True,
        "loan": result,
    }

    state["answer"] = f"I recommended '{recommended_book['title']}' and successfully created the loan."

    return state

async def return_book(
    state: AssistantState,
):
    session = state.get("session")
    current_user = state.get("current_user")

    if session is None or current_user is None:
        state["answer"] = (
            "I could not identify the current library member."
        )
        return state

    history = state.get(
        "member_history",
        [],
    )

    if not history:
        state["answer"] = (
            "You do not have any borrowed books to return."
        )
        return state

    # ---------------------------------------------------------
    # Find active loans
    # ---------------------------------------------------------
    active_loans = [
        loan
        for loan in history
        if getattr(
            loan,
            "return_date",
            None,
        ) is None
    ]

    if not active_loans:
        state["answer"] = (
            "You do not have any active borrowed books to return."
        )
        return state

    # ---------------------------------------------------------
    # Try to identify the requested book from the question
    # ---------------------------------------------------------
    question = state.get(
        "question",
        "",
    ).lower()

    selected_loan = None

    for loan in active_loans:

        book = getattr(
            loan,
            "book",
            None,
        )

        if book is None:
            continue

        book_title = book.title.lower()

        if book_title in question:
            selected_loan = loan
            break

    # ---------------------------------------------------------
    # If exactly one active loan exists,
    # return it automatically
    # ---------------------------------------------------------
    if selected_loan is None and len(active_loans) == 1:
        selected_loan = active_loans[0]

    # ---------------------------------------------------------
    # Multiple active loans and book not identified
    # ---------------------------------------------------------
    if selected_loan is None:

        active_books = []

        for loan in active_loans:

            book = getattr(
                loan,
                "book",
                None,
            )

            if book is not None:
                active_books.append(
                    f"'{book.title}'"
                )
            else:
                active_books.append(
                    f"Loan #{loan.id}"
                )

        state["answer"] = (
            "You currently have multiple borrowed books: "
            + ", ".join(active_books)
            + ".\nPlease specify which book you want to return."
        )

        return state

    # ---------------------------------------------------------
    # Return selected loan
    # ---------------------------------------------------------
    result = await return_loan_service(
        id=selected_loan.id,
        current_user=current_user,
        session=session,
    )

    book = getattr(
        selected_loan,
        "book",
        None,
    )

    if book is not None:
        book_title = book.title
    else:
        book_title = f"book #{selected_loan.book_id}"

    state["loan_result"] = {
        "success": True,
        "action": "returned",
        "loan_id": result.id,
        "book_id": result.book_id,
        "return_date": result.return_date,
    }

    state["book_available"] = True

    state["answer"] = (
        f"Successfully returned '{book_title}'. "
        "The book is now available."
    )

    return state

async def renew_loan(
    state: AssistantState,
):
    session = state.get("session")
    current_user = state.get("current_user")

    if session is None or current_user is None:
        state["answer"] = (
            "I could not identify the current library member."
        )
        return state

    history = state.get(
        "member_history",
        [],
    )

    active_loans = [
        loan
        for loan in history
        if getattr(loan, "return_date", None) is None
    ]

    if not active_loans:
        state["answer"] = (
            "You do not have any active loans to renew."
        )
        return state

    question = state.get(
        "question",
        "",
    ).lower()

    selected_loan = None

    # Try to identify the requested book
    for loan in active_loans:

        book = getattr(
            loan,
            "book",
            None,
        )

        if book is None:
            continue

        title = book.title.lower()

        if title in question:
            selected_loan = loan
            break

    # If only one active loan exists,
    # renew it automatically.
    if selected_loan is None and len(active_loans) == 1:
        selected_loan = active_loans[0]

    # Multiple loans and no book identified
    if selected_loan is None:

        active_books = []

        for loan in active_loans:

            book = getattr(
                loan,
                "book",
                None,
            )

            if book is not None:
                active_books.append(
                    f"'{book.title}'"
                )
            else:
                active_books.append(
                    f"Loan #{loan.id}"
                )

        state["answer"] = (
            "You have multiple active loans: "
            + ", ".join(active_books)
            + ".\nPlease specify which book you want to renew."
        )

        return state

    result = await renew_loan_service(
        id=selected_loan.id,
        current_user=current_user,
        session=session,
    )

    book = getattr(
        result,
        "book",
        None,
    )

    book_title = (
        book.title
        if book is not None
        else f"loan #{result.id}"
    )

    state["loan_result"] = {
        "success": True,
        "action": "renewed",
        "loan_id": result.id,
        "book_id": result.book_id,
        "due_date": result.due_date,
    }

    state["answer"] = (
        f"Successfully renewed '{book_title}'. "
        f"Your new due date is "
        f"{result.due_date.isoformat()}."
    )

    return state

async def reserve_book(
    state: AssistantState,
):
    session = state.get("session")
    current_user = state.get("current_user")

    if session is None or current_user is None:
        state["reservation"] = {
            "success": False,
            "message": "I could not identify the current member.",
        }

        state["answer"] = (
            "I could not identify the current member."
        )

        return state

    book_id = state.get("book_id")

    if book_id is None:

        question = state.get(
            "question",
            "",
        ).lower()

        match = re.search(
            r"\bbook\s*(?:id\s*)?(\d+)\b",
            question,
        )

        if match:
            book_id = int(
                match.group(1)
            )

            state["book_id"] = book_id

    if book_id is None:
        state["reservation"] = {
            "success": False,
            "message": "I could not identify which book to reserve.",
        }

        state["answer"] = (
            "I could not identify which book you want to reserve."
        )

        return state

    try:

        book = await get_book_by_id(
            id=book_id,
            session=session,
        )

        if book is None:

            state["reservation"] = {
                "success": False,
                "message": (
                    f"Book with ID {book_id} was not found."
                ),
            }

            state["answer"] = (
                f"I could not find book with ID {book_id}."
            )

            return state

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        result = await create_reservation_service(
            member_id=current_user.id,
            book_id=book_id,
            expires_at=expires_at,
            session=session,
        )

        state["reservation"] = {
            "success": True,
            "id": result.id,
            "member_id": result.member_id,
            "book_id": result.book_id,
            "reserved_at": result.reserved_at,
            "status": (
                result.status.value
                if hasattr(
                    result.status,
                    "value",
                )
                else str(result.status)
            ),
        }

        state["answer"] = (
            f"Successfully reserved '{book.title}'."
        )

        return state

    except Exception as exc:

        state["reservation"] = {
            "success": False,
            "message": str(exc),
        }

        state["answer"] = (
            f"I could not reserve '{book.title}'. "
            f"{str(exc)}"
        )

        return state