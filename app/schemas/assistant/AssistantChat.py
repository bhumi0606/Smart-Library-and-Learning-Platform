from typing import Any

from pydantic import BaseModel, Field


class AssistantChatRequest(BaseModel):

    question: str = Field(
        min_length=1,
        max_length=2000,
    )

    session_id: str | None = None


class AssistantChatResponse(BaseModel):

    answer: str

    citations: list[dict] = []

    recommended_book: dict | None = None

    book_available: bool | None = None

    loan_result: dict | None = None

    reservation: dict[str, Any] | None = None
