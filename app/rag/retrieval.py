from app.rag.embeddings import create_embedding
from app.rag.vector_store import similarity_search


def retrieve_documents(
    query: str,
    top_k: int = 5,
    where: dict | None = None,
):
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    query_embedding = create_embedding(
        text=query,
    )

    results = similarity_search(
        query_embedding=query_embedding,
        top_k=top_k,
        where=where,
    )

    relevant_documents = []

    for result in results:

        relevant_documents.append(
            {
                "chunk_id": result.get("chunk_id"),
                "content": result.get("text", ""),
                "metadata": {
                    "book_id": result.get("book_id"),
                    "book_title": result.get("book_title"),
                    "book_type": result.get("book_type"),
                    "file_name": result.get("file_name"),
                    "page_number": result.get("page_number"),
                    "heading": result.get("heading"),
                    "chunk_index": result.get("chunk_index"),
                },
                "distance": result.get("distance"),
            }
        )

    return relevant_documents