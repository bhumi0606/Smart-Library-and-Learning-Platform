from typing import List

from app.core.config import settings
from app.core.openai_client import client
from app.rag.retrieval import retrieve_documents


DEFAULT_SYSTEM_PROMPT = """     
You are a Smart Library assistant.

Answer the user's question using ONLY the information provided
in the retrieved library documents.

Do not use outside knowledge.

If the provided documents do not contain enough information
to answer the question, say:

"I couldn't find this information in the library documents."

Always base your answer on the retrieved context.

When possible, mention the book or course used to answer
the question.
"""


def create_context(
    chunks: List[dict],
):

    context = []

    for chunk in chunks:

        metadata = chunk.get(
            "metadata",
            {},
        )

        content = chunk.get(
            "content",
            "",
        )

        book_title = metadata.get(
            "book_title",
            "Unknown",
        )

        book_id = metadata.get(
            "book_id",
            "Unknown",
        )

        book_type = metadata.get(
            "book_type",
            "Unknown",
        )

        page_number = metadata.get(
            "page_number",
            "Unknown",
        )

        heading = metadata.get(
            "heading",
            "Unknown",
        )

        context.append(
            f"""
[Book ID: {book_id}]
[Book: {book_title}]
[Book Type: {book_type}]
[Page: {page_number}]
[Heading: {heading}]

{content}
"""
        )

    return "\n\n".join(context)


def generate_answer(
    query: str,
    chunks: List[dict],
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    history: List[dict] | None = None,
):
    context = create_context(
        chunks=chunks,
    )

    user_prompt = f"""
Context:

{context}

User Question:
{query}
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    if history:
        messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    response = client.chat.completions.create(
        model=settings.OPENAI_CHAT_MODEL,
        messages=messages
    )

    return response.choices[0].message.content

def answer_query(
    query: str,
    top_k: int = 5,
    book_id: int | None = None,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    history: List[dict] | None = None,
):

    where = None

    if book_id is not None:
        where = {
            "book_id": book_id,
        }

    chunks = retrieve_documents(
        query=query,
        top_k=top_k,
        where=where,
    )

    if not chunks:
        return {
            "answer": (
                "I couldn't find relevant information "
                "in the library documents."
            ),
            "citations": [],
            "retrieved_chunks": [],
        }

    answer = generate_answer(
        query=query,
        chunks=chunks,
        system_prompt=system_prompt,
        history=history,
    )

    citations = []

    for chunk in chunks:

        metadata = chunk.get(
            "metadata",
            {},
        )

        citations.append(
            {
                "book_id": metadata.get(
                    "book_id"
                ),

                "book_title": metadata.get(
                    "book_title"
                ),

                "book_type": metadata.get(
                    "book_type"
                ),

                "file_name": metadata.get(
                    "file_name"
                ),

                "page_number": metadata.get(
                    "page_number"
                ),

                "heading": metadata.get(
                    "heading"
                ),

                "chunk_id": chunk.get(
                    "chunk_id"
                ),

                "distance": chunk.get(
                    "distance"
                ),
            }
        )

    return {
        "answer": answer,
        "citations": citations,
        "retrieved_chunks": chunks,
    }