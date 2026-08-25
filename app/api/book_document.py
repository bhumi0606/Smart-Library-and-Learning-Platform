from fastapi import APIRouter, Depends, File, Request, UploadFile, status   
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.authentication import require_librarian
from app.services.BookDocumentService import upload_book_document
from app.core.rate_limiter import limiter

book_document_router = APIRouter(
    prefix="/books",
    tags=["Book Documents"],
    dependencies=[Depends(require_librarian)],
)


@book_document_router.post(
    "/{book_id}/document",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("20/minute")
async def upload_document(
    request: Request,
    book_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
):
    return await upload_book_document(
        book_id=book_id,
        file=file,
        session=session,
    )
