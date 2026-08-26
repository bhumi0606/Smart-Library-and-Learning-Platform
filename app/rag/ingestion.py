from app.rag.embeddings import create_embedding
from app.rag.vector_store import add_document
from app.services.ChunkingService import create_chunks


def store_chunks(
    chunks: list[dict],
):

    if not chunks:                      
        return 0

    count = 0

    for chunk in chunks:

        content = chunk["content"]

        if not content.strip():
            continue

        embedding = create_embedding(
            text=content,
        )

        metadata = {
            "book_id": chunk["book_id"],
            "book_title": chunk["book_title"],
            "book_type": chunk["book_type"],
            "file_name": chunk["file_name"],
            "page_number": chunk["page_number"],
            "heading": chunk["heading"],
            "chunk_index": chunk["chunk_index"],
        }

        add_document(
            document_id=chunk["chunk_id"],
            text=content,
            embedding=embedding,
            metadata=metadata,
        )

        count += 1

    return count

def ingest_document( 
        pages: list[dict], 
        file_name: str, 
        book_id: int | None = None, 
        book_title: str | None = None, 
        book_type: str | None = None
    ): 
    chunks = create_chunks( 
        pages=pages, 
        file_name=file_name, 
        book_id=book_id, 
        book_title=book_title, 
        book_type=book_type
    )
    stored_count = store_chunks( 
        chunks=chunks
    ) 
    return { 
        "file_name": file_name, 
        "book_id": book_id, 
        "chunks_created": len(chunks), 
        "chunks_stored": stored_count
    }