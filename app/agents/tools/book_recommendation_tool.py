from typing import Any

from app.core.config import settings
from app.core.openai_client import client


class BookRecommendationTool:
    name = "recommend_book"

    description = """
    Recommend a library book based on the member's
    previous borrowing history and available book candidates.
    """

    async def execute(
        self,
        question: str,
        member_history: list[dict[str, Any]],
        candidates: list[dict[str, Any]],
    ):

        if not candidates:
            return {
                "recommended_book": None,
                "reason": "No suitable books were found in the library."
            }

        history_text = self._format_history(
            member_history
        )

        candidates_text = self._format_candidates(
            candidates
        )

        prompt = f"""
You are a Smart Library recommendation assistant.

Recommend exactly ONE book from the candidate list.

Rules:

1. You MUST select a book from the candidate list.
2. NEVER invent a book.
3. Consider the user's request.
4. Consider the member's borrowing history.
5. Prefer books that are currently available.
6. If there are no suitable candidates, return BOOK_ID: NONE.

Member borrowing history:
{history_text}

User request:
{question}

Candidate books:
{candidates_text}

Return EXACTLY:

BOOK_ID: <id>
REASON: <short explanation>

Or:

BOOK_ID: NONE
REASON: <short explanation>
"""

        response = client.chat.completions.create(
            model=settings.OPENAI_CHAT_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

        content = (
            response.choices[0]
            .message
            .content
            .strip()
        )

        return self._parse_response(
            content=content,
            candidates=candidates,
        )

    @staticmethod
    def _format_history(                            
        history: list[dict[str, Any]],
    ):

        if not history:
            return "No previous borrowing history."

        result = []

        for loan in history:

            book = getattr(
                loan,
                "book",
                None,
            )

            if book is not None:

                result.append(
                    f"- Book ID: {book.id}, "
                    f"Title: {book.title}"
                )

        return "\n".join(result)

    @staticmethod
    def _format_candidates(
        candidates: list[dict[str, Any]],
    ):

        result = []

        for book in candidates:

            result.append(
                f"- ID: {book['id']}, "
                f"Title: {book['title']}, "
                f"ISBN: {book.get('isbn')}, "
                f"Type: {book.get('book_type')}, "
                f"Status: {book.get('status')}, "
                f"Published: {book.get('published_date')}"
            )

        return "\n".join(result)

    @staticmethod
    def _parse_response(
        content: str,
        candidates: list[dict[str, Any]],
    ):

        book_id = None
        reason = ""

        for line in content.splitlines():

            line = line.strip()

            if line.startswith("BOOK_ID:"):

                value = line.split(
                    ":",
                    1,
                )[1].strip()

                if value.upper() != "NONE":

                    try:
                        book_id = int(value)

                    except ValueError:
                        book_id = None

            elif line.startswith("REASON:"):

                reason = line.split(
                    ":",
                    1,
                )[1].strip()

        if book_id is None:

            return {
                "recommended_book": None,
                "reason": reason
                or "No suitable book found.",
            }

        for book in candidates:

            if book["id"] == book_id:

                return {
                    "recommended_book": book,
                    "reason": reason,
                }

        return {
            "recommended_book": None,
            "reason": (
                "The recommended book was not "
                "found in the candidate list."
            ),
        }


book_recommendation_tool = BookRecommendationTool()
