from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.authentication import get_current_user, require_librarian
from app.schemas.author.AuthorCreate import AuthorCreate
from app.schemas.author.AuthorUpdate import AuthorUpdate
from app.services.AuthorService import create_author_service, get_author_by_id_service, get_authors_service, update_author_service, delete_author_service

author_router = APIRouter(
    dependencies=[Depends(get_current_user)],
    prefix="/authors",
    tags=["Authors"],
)


@author_router.post(
    "",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_201_CREATED,
)
async def create_author(
    author: AuthorCreate,
    session: AsyncSession = Depends(get_db),
):
    return await create_author_service(
        author=author,
        session=session,
    )


@author_router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_authors(
    session: AsyncSession = Depends(get_db),
):
    return await get_authors_service(
        session=session,
    )


@author_router.get(
    "/{author_id}",
    status_code=status.HTTP_200_OK,
)
async def get_author(
    author_id: int,
    session: AsyncSession = Depends(get_db),
):
    return await get_author_by_id_service(
        id=author_id,
        session=session,
    )


@author_router.patch(
    "/{author_id}",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_200_OK,
)
async def update_author(
    author_id: int,
    author_update: AuthorUpdate,
    session: AsyncSession = Depends(get_db),
):
    return await update_author_service(
        id=author_id,
        author_update=author_update,
        session=session,
    )


@author_router.delete(
    "/{author_id}",
    dependencies=[Depends(require_librarian)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_author(
    author_id: int,
    session: AsyncSession = Depends(get_db),
):
    await delete_author_service(
        id=author_id,
        session=session,
    )