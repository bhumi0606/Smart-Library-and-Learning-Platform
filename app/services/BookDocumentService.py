import os
import tempfile

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.BookRepository import get_book_by_id
from app.rag.ingestion import ingest_document
from app.services.BookExtractionService import extract_text


async def upload_book_document(
    book_id: int,
    file: UploadFile,
    session: AsyncSession,
):
    book = await get_book_by_id(
        id=book_id,
        session=session,
    )

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required",
        )

    allowed_extensions = (
        ".pdf",
        ".txt",
        ".docx",
    )

    if not file.filename.lower().endswith(
        allowed_extensions
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only PDF, TXT and DOCX files "
                "are supported"
            ),
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty",
        )

    temporary_path = None

    try:
        suffix = os.path.splitext(
            file.filename
        )[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temporary_file:

            temporary_file.write(
                file_bytes
            )

            temporary_path = (
                temporary_file.name
            )

        pages = extract_text(
            temporary_path
        )

        if not pages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "No text could be extracted "
                    "from the document"
                ),
            )

        result = ingest_document(
            pages=pages,
            file_name=file.filename,
            book_id=book.id,
            book_title=book.title,
            book_type=(
                book.book_type.value
                if hasattr(
                    book.book_type,
                    "value",
                )
                else str(book.book_type)
            ),
        )

        return {
            "message": (
                "Book document uploaded "
                "and indexed successfully"
            ),
            "book_id": book.id,
            "file_name": file.filename,
            "chunks_created": (
                result["chunks_created"]
            ),
            "chunks_stored": (
                result["chunks_stored"]
            ),
        }

    finally:
        if (
            temporary_path
            and os.path.exists(temporary_path)
        ):
            os.remove(temporary_path)