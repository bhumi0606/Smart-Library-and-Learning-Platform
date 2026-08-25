from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.graph.assistant_graph import assistant_graph


async def chat(
        question: str,
        current_user: Any,
        session: AsyncSession,
        session_id: str | None = None,
    ):

        if not question or not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        state = {
            "question": question.strip(),

            "session_id": (
                session_id
                or str(current_user.id)
            ),

            "member_id": current_user.id,

            "session": session,

            "current_user": current_user,

            "messages": [
                {
                    "role": "user",
                    "content": question.strip(),
                }
            ],

            "intents": [],

            "tasks": [],

            "retrieved_chunks": [],

            "citations": [],

            "book_candidates": [],

            "member_history": [],

            "recommended_book": None,

            "book_available": None,

            "reservation": None,

            "answer": "",
        }

        result = await assistant_graph.ainvoke(
            state
        )

        return {
            "answer": result.get(
                "answer",
                "",
            ),
            "citations": result.get(
                "citations",
                [],
            ),
            "recommended_book": result.get(
                "recommended_book",
            ),
            "book_available": result.get(
                "book_available",
            ),
            "loan_result": result.get(
                "loan_result",
            ),
            "reservation": result.get(
                "reservation",
            ),
        }
