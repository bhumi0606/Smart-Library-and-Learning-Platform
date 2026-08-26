from datetime import datetime, timedelta, timezone
from typing import Any

from app.agents.tools.book_recommendation_tool import (
    book_recommendation_tool,
)

from app.agents.tools.book_tool import execute_book_tool

from app.graph.state import AssistantState

from app.repository.BookRepository import get_book_by_id, get_books

from app.schemas.loan.LoanCreate import CreateLoan

from app.services.BookService import check_book_availability_service

from app.services.LoanService import create_loan_service, get_loans_service, renew_loan_service, return_loan_service

from app.services.ReservationService import create_reservation_service
from app.repository.CourseRepository import get_courses

def get_task_arguments(
    state: AssistantState,
    task: str,
):
    arguments = state.get(
        "task_arguments",
        {},
    )

    if not isinstance(arguments, dict):
        return {}

    task_arguments = arguments.get(
        task,
        {},
    )

    if not isinstance(task_arguments, dict):
        return {}

    return task_arguments


def normalize_enum_value(
    value: Any,
):
    if hasattr(value, "value"):
        return str(value.value)

    return str(value)


def normalize_title(
    title: Any,
):
    if title is None:
        return None

    title = str(title).strip().lower()

    if not title:
        return None

    return title


def serialize_book(
    book,
):
    return {
        "id": book.id,
        "title": book.title,

        "published_date": (
            book.published_date.isoformat()
            if book.published_date
            else None
        ),

        "isbn": book.isbn,

        "book_type": normalize_enum_value(
            book.book_type
        ),

        "status": normalize_enum_value(
            book.status
        ),

        "authors": [
            author.name
            for author in getattr(
                book,
                "authors",
                [],
            )
        ],
    }


def is_active_loan(
    loan,
):

    return (
        getattr(
            loan,
            "return_date",
            None,
        )
        is None
    )


def serialize_loan(
    loan,
    book=None,
):
    return {
        "id": loan.id,
        "member_id": loan.member_id,
        "book_id": loan.book_id,

        "book_title": (
            book.title
            if book
            else None
        ),

        "issued_at": (
            loan.issued_at.isoformat()
            if getattr(
                loan,
                "issued_at",
                None,
            )
            else None
        ),

        "due_date": (
            loan.due_date.isoformat()
            if getattr(
                loan,
                "due_date",
                None,
            )
            else None
        ),

        "return_date": (
            loan.return_date.isoformat()
            if getattr(
                loan,
                "return_date",
                None,
            )
            else None
        ),
    }


async def get_book_for_loan(
    loan,
    session,
):

    book = getattr(
        loan,
        "book",
        None,
    )

    if book is not None:
        return book

    book_id = getattr(
        loan,
        "book_id",
        None,
    )

    if book_id is None:
        return None

    return await get_book_by_id(
        id=book_id,
        session=session,
    )


async def get_active_loans_with_books(
    state: AssistantState,
):
    session = state.get(
        "session"
    )

    current_user = state.get(
        "current_user"
    )

    if session is None or current_user is None:
        return []

    history = state.get(
        "member_history",
        [],
    )

    if not history:
        return []

    active_loans = [
        loan
        for loan in history
        if is_active_loan(loan)
    ]

    result = []

    for loan in active_loans:

        book = await get_book_for_loan(
            loan=loan,
            session=session,
        )

        result.append(
            (
                loan,
                book,
            )
        )

    return result


async def find_loan_by_book(
    state: AssistantState,
    task_name: str,
    active_only: bool = True,
):
    session = state.get(
        "session"
    )

    if session is None:
        return None, None

    arguments = get_task_arguments(
        state,
        task_name,
    )

    requested_book_id = arguments.get(
        "book_id"
    )

    requested_title = arguments.get(
        "book_title"
    )

    normalized_requested_title = normalize_title(
        requested_title
    )

    history = state.get(
        "member_history",
        [],
    )

    if not history:

        current_user = state.get(
            "current_user"
        )

        if current_user is not None:

            history = await get_loans_service(
                current_user=current_user,
                session=session,
            )

            state["member_history"] = history

    loans = history

    if active_only:

        loans = [
            loan
            for loan in loans
            if is_active_loan(loan)
        ]

    if requested_book_id is not None:

        try:
            requested_book_id = int(
                requested_book_id
            )
        except (
            TypeError,
            ValueError,
        ):
            requested_book_id = None

    if requested_book_id is not None:

        for loan in loans:

            if loan.book_id == requested_book_id:

                book = await get_book_for_loan(
                    loan=loan,
                    session=session,
                )

                return loan, book

        return None, None

    if normalized_requested_title:

        for loan in loans:

            book = await get_book_for_loan(
                loan=loan,
                session=session,
            )

            if book is None:
                continue

            if (
                normalize_title(book.title)
                == normalized_requested_title
            ):
                return loan, book

        return None, None

    if len(loans) == 1:

        loan = loans[0]

        book = await get_book_for_loan(
            loan=loan,
            session=session,
        )

        return loan, book

    return None, None


def clear_book_selection(
    state: AssistantState,
):

    state.pop(
        "book_id",
        None,
    )

    state.pop(
        "recommended_book",
        None,
    )

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

        if state.get(
            "task_failed",
            False,
        ):
            break

    return state


async def execute_task(
    task: str,
    state: AssistantState,
):

    handlers = {
        "answer_general": answer_general,
        "search_book_content": search_book_content,
        "search_books": search_books,
        "get_book": get_book,
        "recommend_book": recommend_book,
        "get_member_history": get_member_history,
        "check_book_availability": check_book_availability,
        "borrow_book": borrow_book,
        "return_book": return_book,
        "renew_loan": renew_loan,
        "reserve_book": reserve_book,
        "search_courses": search_courses,
    }

    handler = handlers.get(
        task
    )

    if handler is None:

        state["task_failed"] = True

        state["answer"] = (
            f"I don't know how to execute task '{task}'."
        )

        return state

    return await handler(
        state
    )


async def answer_general(
    state: AssistantState,
):

    state["answer"] = (
        "Hello! I'm your Smart Library assistant. "
        "I can help you with books, loans, reservations, "
        "courses, recommendations and library information."
    )

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

    session = state.get(
        "session"
    )

    if session is None:

        state["book_candidates"] = []
        state["book_total"] = 0
        state["task_failed"] = True

        state["answer"] = (
            "I could not access the library catalog."
        )

        return state

    arguments = get_task_arguments(
        state,
        "search_books",
    )

    title = arguments.get(
        "title"
    )

    author = arguments.get(
        "author"
    )

    status = arguments.get(
        "status"
    )

    query = arguments.get(
        "query"
    )

    page = arguments.get(
        "page",
        1,
    )

    limit = arguments.get(
        "limit",
        100,
    )

    if query and not title:
        title = query

    books, total = await get_books(
        session=session,
        title=title,
        author=author,
        status=status,
        page=page,
        limit=limit,
    )

    candidates = [
        serialize_book(book)
        for book in books
    ]

    state["book_candidates"] = candidates
    state["book_total"] = total

    if not candidates:

        state["answer"] = (
            "I couldn't find any books matching your request."
        )

        return state

    if len(candidates) == 1:

        state["book_id"] = candidates[0]["id"]

        state["recommended_book"] = candidates[0]

    lines = []

    for book in candidates:

        author_text = ""

        if book.get("authors"):

            author_text = (
                " by "
                + ", ".join(
                    book["authors"]
                )
            )

        lines.append(
            f"- {book['title']}"
            f"{author_text} "
            f"(ID: {book['id']}, "
            f"type: {book['book_type']}, "
            f"status: {book['status']})"
        )

    if status == "available":

        state["answer"] = (
            f"I found {len(candidates)} available books:\n"
            + "\n".join(lines)
        )

    else:

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

    arguments = get_task_arguments(
        state,
        "get_book",
    )

    book_id = arguments.get(
        "book_id"
    )

    if book_id is None:
        book_id = state.get(
            "book_id"
        )

    if session is None or book_id is None:
        return state

    try:
        book_id = int(book_id)
    except (
        TypeError,
        ValueError,
    ):

        state["answer"] = (
            "The provided book ID is invalid."
        )

        return state

    book = await get_book_by_id(
        id=book_id,
        session=session,
    )

    if book is None:

        state["answer"] = (
            f"I could not find book with ID {book_id}."
        )

        return state

    state["book_id"] = book.id

    state["recommended_book"] = serialize_book(
        book
    )

    return state

async def get_member_history(
    state: AssistantState,
):
    session = state.get("session")
    current_user = state.get("current_user")

    if session is None or current_user is None:
        state["member_history"] = []
        state["current_loans"] = []
        state["task_failed"] = True
        state["answer"] = (
            "I could not identify the current library member."
        )
        return state

    try:
        loans = await get_loans_service(
            current_user=current_user,
            session=session,
        )

        state["member_history"] = loans

        active_loans = [
            loan
            for loan in loans
            if getattr(loan, "return_date", None) is None
        ]

        if not active_loans:
            state["current_loans"] = []

            state["answer"] = (
                "You currently do not have any borrowed books."
            )

            return state

        current_loans = []

        for loan in active_loans:

            book = getattr(
                loan,
                "book",
                None,
            )

            if book is not None:

                title = book.title
                book_id = book.id

            else:

                title = f"Book #{loan.book_id}"
                book_id = loan.book_id

            current_loans.append({
                "loan_id": loan.id,
                "book_id": book_id,
                "title": title,
                "due_date": (
                    loan.due_date.isoformat()
                    if loan.due_date
                    else None
                ),
            })

        state["current_loans"] = current_loans

        lines = []

        for item in current_loans:

            if item["due_date"]:

                lines.append(
                    f"- '{item['title']}' "
                    f"(due {item['due_date']})"
                )

            else:

                lines.append(
                    f"- '{item['title']}'"
                )

        count = len(current_loans)

        if count == 1:

            state["answer"] = (
                "You currently have 1 borrowed book:\n"
                + "\n".join(lines)
            )

        else:

            state["answer"] = (
                f"You currently have {count} borrowed books:\n"
                + "\n".join(lines)
            )

        return state

    except Exception as exc:

        state["member_history"] = []
        state["current_loans"] = []
        state["task_failed"] = True

        state["answer"] = (
            "I could not retrieve your current borrowed books."
        )

        return state

async def recommend_book(
    state: AssistantState,
):

    candidates = state.get(
        "book_candidates",
        [],
    )

    history = state.get(
        "member_history",
        [],
    )

    if not candidates:

        state["recommended_book"] = None
        state["book_available"] = False

        state["answer"] = (
            "I couldn't find any books to recommend."
        )

        return state

    result = await book_recommendation_tool.execute(
        question=state["question"],
        member_history=history,
        candidates=candidates,
    )

    recommended_book = result.get(
        "recommended_book"
    )

    state["recommended_book"] = (
        recommended_book
    )

    state["recommendation_reason"] = result.get(
        "reason",
        "",
    )

    if recommended_book:

        state["book_id"] = (
            recommended_book.get("id")
        )

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

async def resolve_book(
    state: AssistantState,
    task_name: str,
):

    session = state.get(
        "session"
    )

    if session is None:
        return None

    arguments = get_task_arguments(
        state,
        task_name,
    )

    explicit_book_id = arguments.get(
        "book_id"
    )

    explicit_book_title = arguments.get(
        "book_title"
    )

    if explicit_book_id is not None:

        try:
            book_id = int(
                explicit_book_id
            )
        except (
            TypeError,
            ValueError,
        ):
            book_id = None

        if book_id is not None:

            book = await get_book_by_id(
                id=book_id,
                session=session,
            )

            if book:

                state["book_id"] = book.id

                state["recommended_book"] = (
                    serialize_book(book)
                )

                return book

    if explicit_book_title:

        books, _ = await get_books(
            session=session,
            title=explicit_book_title,
            page=1,
            limit=10,
        )

        normalized_title = normalize_title(
            explicit_book_title
        )

        for book in books:

            if (
                normalize_title(book.title)
                == normalized_title
            ):

                state["book_id"] = book.id

                state["recommended_book"] = (
                    serialize_book(book)
                )

                return book

        if len(books) == 1:

            book = books[0]

            state["book_id"] = book.id

            state["recommended_book"] = (
                serialize_book(book)
            )

            return book

        return None

    candidates = state.get(
        "book_candidates",
        [],
    )

    if len(candidates) == 1:

        candidate = candidates[0]

        book = await get_book_by_id(
            id=candidate["id"],
            session=session,
        )

        if book:

            state["book_id"] = book.id

            state["recommended_book"] = (
                serialize_book(book)
            )

            return book
        
    existing_book_id = state.get(
        "book_id"
    )

    if existing_book_id is not None:

        try:
            existing_book_id = int(
                existing_book_id
            )
        except (
            TypeError,
            ValueError,
        ):
            existing_book_id = None

    if existing_book_id is not None:

        book = await get_book_by_id(
            id=existing_book_id,
            session=session,
        )

        if book:

            state["book_id"] = book.id

            state["recommended_book"] = (
                serialize_book(book)
            )

            return book

    return None

async def check_book_availability(
    state: AssistantState,
):

    session = state.get(
        "session"
    )

    if session is None:

        state["book_available"] = False

        state["answer"] = (
            "I could not access the library catalog."
        )

        return state

    book = await resolve_book(
        state,
        "check_book_availability",
    )

    if book is None:

        state["book_available"] = False

        state["answer"] = (
            "I could not identify the book you are asking about."
        )

        return state

    result = await check_book_availability_service(
        book_id=book.id,
        session=session,
    )

    state["book_available"] = result[
        "available"
    ]

    if result["available"]:

        state["answer"] = (
            f"Yes, '{result['title']}' is currently available."
        )

    else:

        state["answer"] = (
            f"No, '{result['title']}' is currently "
            f"{result['status']}."
        )

    state["availability_message"] = (
        state["answer"]
    )

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

    if session is None or current_user is None:

        state["loan_result"] = {
            "success": False,
            "message": (
                "I could not identify the current member."
            ),
        }

        state["answer"] = (
            "I could not identify the current member."
        )

        return state

    book = await resolve_book(
        state,
        "borrow_book",
    )

    if book is None:

        state["loan_result"] = {
            "success": False,
            "message": (
                "I could not identify which book you want to borrow."
            ),
        }

        state["answer"] = (
            "I could not identify which book you want to borrow."
        )

        return state

    availability = await check_book_availability_service(
        book_id=book.id,
        session=session,
    )

    if not availability["available"]:

        state["book_available"] = False

        state["loan_result"] = {
            "success": False,
            "message": (
                f"'{book.title}' is currently "
                f"{availability['status']}."
            ),
        }

        state["answer"] = (
            f"I cannot borrow '{book.title}' because it is "
            f"currently {availability['status']}."
        )

        return state

    state["book_available"] = True

    due_date = (
        datetime.now(timezone.utc)
        + timedelta(days=14)
    )

    loan = CreateLoan(
        member_id=current_user.id,
        book_id=book.id,
        due_date=due_date,
    )

    result = await create_loan_service(
        loan=loan,
        current_user=current_user,
        session=session,
    )

    state["loan_result"] = {
        "success": True,
        "action": "borrowed",
        "loan": result,
    }

    state["answer"] = (
        f"Successfully borrowed '{book.title}'. "
        f"Your due date is {result["due_date"].isoformat()}."
    )

    return state

async def return_book(
    state: AssistantState,
):

    session = state.get(
        "session"
    )

    current_user = state.get(
        "current_user"
    )

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

    active_loans = [
        loan
        for loan in history
        if is_active_loan(loan)
    ]

    if not active_loans:

        state["answer"] = (
            "You do not have any active borrowed books to return."
        )

        return state

    arguments = get_task_arguments(
        state,
        "return_book",
    )

    requested_title = arguments.get(
        "book_title"
    )

    requested_book_id = arguments.get(
        "book_id"
    )

    selected_loan = None
    selected_book = None

    if requested_book_id is not None:

        try:
            requested_book_id = int(
                requested_book_id
            )
        except (
            TypeError,
            ValueError,
        ):
            requested_book_id = None

        if requested_book_id is not None:

            for loan in active_loans:

                if loan.book_id == requested_book_id:

                    selected_loan = loan

                    selected_book = (
                        await get_book_for_loan(
                            loan=loan,
                            session=session,
                        )
                    )

                    break

    if (
        selected_loan is None
        and requested_title
    ):

        normalized_title = normalize_title(
            requested_title
        )

        for loan in active_loans:

            book = await get_book_for_loan(
                loan=loan,
                session=session,
            )

            if book is None:
                continue

            if (
                normalize_title(book.title)
                == normalized_title
            ):

                selected_loan = loan
                selected_book = book

                break

    has_explicit_book = (
        requested_title is not None
        or requested_book_id is not None
    )

    if (
        selected_loan is None
        and has_explicit_book
    ):

        requested_display = (
            requested_title
            if requested_title
            else f"book ID {requested_book_id}"
        )

        state["answer"] = (
            f"You do not currently have "
            f"'{requested_display}' borrowed."
        )

        state["loan_result"] = {
            "success": False,
            "message": (
                f"The requested book is not an active loan "
                f"for the current member."
            ),
        }

        return state

    if selected_loan is None:

        if len(active_loans) == 1:

            selected_loan = active_loans[0]

            selected_book = (
                await get_book_for_loan(
                    loan=selected_loan,
                    session=session,
                )
            )

        else:

            active_books = []

            for loan in active_loans:

                book = await get_book_for_loan(
                    loan=loan,
                    session=session,
                )

                if book:

                    active_books.append(
                        f"'{book.title}'"
                    )

            state["answer"] = (
                "You currently have multiple borrowed books: "
                + ", ".join(active_books)
                + ".\nPlease specify which book you want to return."
            )

            return state

    result = await return_loan_service(
        id=selected_loan.id,
        current_user=current_user,
        session=session,
    )

    title = (
        selected_book.title
        if selected_book
        else f"book #{selected_loan.book_id}"
    )

    state["loan_result"] = {
        "success": True,
        "action": "returned",
        "loan_id": result.id,
        "book_id": result.book_id,
        "return_date": (
            result.return_date.isoformat()
            if result.return_date
            else None
        ),
    }

    state["book_available"] = True

    state["answer"] = (
        f"Successfully returned '{title}'. "
        "The book is now available."
    )

    return state

async def renew_loan(
    state: AssistantState,
):

    session = state.get(
        "session"
    )

    current_user = state.get(
        "current_user"
    )

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

        history = await get_loans_service(
            current_user=current_user,
            session=session,
        )

        state["member_history"] = history

    active_loans = [
        loan
        for loan in history
        if is_active_loan(loan)
    ]

    if not active_loans:

        state["answer"] = (
            "You do not have any active loans to renew."
        )

        return state

    arguments = get_task_arguments(
        state,
        "renew_loan",
    )

    requested_title = arguments.get(
        "book_title"
    )

    requested_book_id = arguments.get(
        "book_id"
    )

    selected_loan = None
    selected_book = None

    if requested_book_id is not None:

        try:
            requested_book_id = int(
                requested_book_id
            )
        except (
            TypeError,
            ValueError,
        ):
            requested_book_id = None

        if requested_book_id is not None:

            for loan in active_loans:

                if loan.book_id == requested_book_id:

                    selected_loan = loan

                    selected_book = (
                        await get_book_for_loan(
                            loan=loan,
                            session=session,
                        )
                    )

                    break

    if (
        selected_loan is None
        and requested_title
    ):

        normalized_title = normalize_title(
            requested_title
        )

        for loan in active_loans:

            book = await get_book_for_loan(
                loan=loan,
                session=session,
            )

            if book is None:
                continue

            if (
                normalize_title(book.title)
                == normalized_title
            ):

                selected_loan = loan
                selected_book = book

                break

    
    has_explicit_book = (
        requested_title is not None
        or requested_book_id is not None
    )

    if (
        selected_loan is None
        and has_explicit_book
    ):

        requested_display = (
            f"'{requested_title}'"
            if requested_title
            else f"book ID {requested_book_id}"
        )

        state["loan_result"] = {
            "success": False,
            "message": (
                f"{requested_display} is not currently "
                "borrowed by you."
            ),
        }

        state["answer"] = (
            f"You do not currently have "
            f"{requested_display} borrowed, "
            "so it cannot be renewed."
        )

        return state

    if selected_loan is None:

        if len(active_loans) == 1:

            selected_loan = active_loans[0]

            selected_book = (
                await get_book_for_loan(
                    loan=selected_loan,
                    session=session,
                )
            )

        else:

            active_books = []

            for loan in active_loans:

                book = await get_book_for_loan(
                    loan=loan,
                    session=session,
                )

                if book:

                    active_books.append(
                        f"'{book.title}'"
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

    title = (
        selected_book.title
        if selected_book
        else f"book #{result.book_id}"
    )

    state["loan_result"] = {
        "success": True,
        "action": "renewed",
        "loan_id": result.id,
        "book_id": result.book_id,
        "due_date": (
            result.due_date.isoformat()
            if result.due_date
            else None
        ),
    }

    state["answer"] = (
        f"Successfully renewed '{title}'. "
        f"Your new due date is "
        f"{result.due_date.isoformat()}."
    )

    return state

async def reserve_book(
    state: AssistantState,
):

    session = state.get(
        "session"
    )

    current_user = state.get(
        "current_user"
    )

    if session is None or current_user is None:

        state["reservation"] = {
            "success": False,
            "message": (
                "I could not identify the current member."
            ),
        }

        state["answer"] = (
            "I could not identify the current member."
        )

        return state

    book = await resolve_book(
        state,
        "reserve_book",
    )

    if book is None:

        state["reservation"] = {
            "success": False,
            "message": (
                "I could not identify which book to reserve."
            ),
        }

        state["answer"] = (
            "I could not identify which book you want to reserve."
        )

        return state

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(days=7)
    )

    try:

        result = await create_reservation_service(
            member_id=current_user.id,
            book_id=book.id,
            expires_at=expires_at,
            session=session,
        )

        state["reservation"] = {
            "success": True,
            "id": result.id,
            "member_id": result.member_id,
            "book_id": result.book_id,
            "reserved_at": (
                result.reserved_at.isoformat()
                if result.reserved_at
                else None
            ),
            "status": normalize_enum_value(
                result.status
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

async def search_courses(
    state: AssistantState,
):
    session = state.get("session")

    if session is None:
        state["course_candidates"] = []
        state["course_total"] = 0
        state["task_failed"] = True
        state["answer"] = (
            "I could not access the course catalog."
        )
        return state

    arguments = get_task_arguments(
        state,
        "search_courses",
    )

    title = arguments.get("title")
    query = arguments.get("query")

    if query and not title:
        title = query

    courses, total = await get_courses(
        session=session,
        name=title,
    )

    candidates = []

    for course in courses:
        candidates.append({
            "id": course.id,
            "title": course.name,
            "description": getattr(
                course,                 
                "description",
                None,
            ),
        })

    state["course_candidates"] = candidates
    state["course_total"] = total

    if not candidates:
        state["answer"] = (
            "I couldn't find any courses matching your request."
        )
        return state

    lines = []

    for course in candidates:
        description = course.get("description")

        if description:
            lines.append(
                f"- {course['title']} "
                f"(ID: {course['id']}): "
                f"{description}"
            )
        else:
            lines.append(
                f"- {course['title']} "
                f"(ID: {course['id']})"
            )

    state["answer"] = (
        f"I found {len(candidates)} relevant courses:\n"
        + "\n".join(lines)
    )

    state["citations"] = [
        {
            "type": "course",
            "course_id": course["id"],
            "title": course["title"],
        }
        for course in candidates
    ]

    return state