from typing import Any, TypedDict

from sqlalchemy.ext.asyncio import AsyncSession


class AssistantState(TypedDict, total=False):

    # user request
    question: str
    session_id: str
    member_id: int | None

    # session and current user
    session: AsyncSession
    current_user: Any

    # conversation
    messages: list[dict[str, Any]]

    # intent
    intents: list[str]
    tasks: list[str]
    is_multi_step: bool

    # rag
    retrieved_chunks: list[dict[str, Any]]
    citations: list[dict[str, Any]]
    

    # Book / recommendation
    book_id: int | None
    book_candidates: list[dict[str, Any]]
    book_total: int
    member_history: list[Any]
    recommendation_context: list[Any]
    recommended_book: dict[str, Any] | None
    recommendation_reason: str
    book_available: bool | None
    availability_message: str

    # loan
    loan_result: dict[str, Any] | None
    # reservation
    reservation: dict[str, Any] | None
    # final response
    answer: str