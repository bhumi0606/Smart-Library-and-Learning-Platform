from typing import Any, TypedDict

from sqlalchemy.ext.asyncio import AsyncSession


class AssistantState(TypedDict, total=False):

    # User request
    question: str
    session_id: str
    member_id: int | None

    # Current user / DB session
    session: AsyncSession
    current_user: Any

    # Conversation
    messages: list[dict[str, Any]]

    # LLM planning
    intents: list[str]
    tasks: list[str]
    is_multi_step: bool
    task_arguments: dict[str, dict[str, Any]]

    # RAG / book content
    retrieved_chunks: list[dict[str, Any]]
    citations: list[dict[str, Any]]

    # Book
    book_id: int | None
    book_candidates: list[dict[str, Any]]
    book_total: int

    # Member history
    member_history: list[Any]

    # Recommendation
    recommendation_context: list[Any]
    recommended_book: dict[str, Any] | None
    recommendation_reason: str

    # Availability
    book_available: bool | None
    availability_message: str

    # Loan
    loan_result: dict[str, Any] | None

    # Reservation
    reservation: dict[str, Any] | None

    # Final response
    answer: str