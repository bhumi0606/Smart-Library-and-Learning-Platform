import chromadb

from app.core.config import settings


client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH,
)


collection = client.get_or_create_collection(
    name="library",
)


def add_document(
    document_id: str,
    text: str,
    embedding: list[float],
    metadata: dict,
):
    collection.upsert(
        ids=[document_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
    )


def similarity_search(
    query_embedding: list[float],
    top_k: int = 5,
    where: dict | None = None,
):

    query_params = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
    }

    if where:
        query_params["where"] = where

    results = collection.query(
        **query_params
    )

    ids = results.get(
        "ids",
        [[]],
    )[0]

    documents = results.get(
        "documents",
        [[]],
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]],
    )[0]

    distances = results.get(
        "distances",
        [[]],
    )[0]

    matches = []

    for i in range(len(ids)):

        metadata = metadatas[i] or {}

        distance = distances[i]

        matches.append(
            {
                "chunk_id": ids[i],

                "text": documents[i] or "",

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

                "chunk_index": metadata.get(
                    "chunk_index"
                ),

                "distance": distance,

            }
        )

    return matches