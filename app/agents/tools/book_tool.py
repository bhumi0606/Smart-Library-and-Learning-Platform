from app.services.RAGService import answer_query


async def execute_book_tool(
    query: str,
    top_k: int = 5,
    book_id: int | None = None,
):
    if not query or not query.strip():
        raise ValueError(
            "Query cannot be empty"
        )

    result = answer_query(
        query=query,
        top_k=top_k,
        book_id=book_id,
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

        "retrieved_chunks": result.get(
            "retrieved_chunks",
            [],
        ),
    }