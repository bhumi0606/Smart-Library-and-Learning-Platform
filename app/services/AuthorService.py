from fastapi import HTTPException, status

from app.repository.AuthorRepository import create_author, delete_author, get_author_by_id, get_authors, update_author
from app.schemas.author.AuthorCreate import AuthorCreate
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.author.AuthorUpdate import AuthorUpdate


async def create_author_service(
        author: AuthorCreate,
        session: AsyncSession
):
    response = await create_author(
        author = author,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "author not added"
        )
    return response

async def get_author_by_id_service(
        id: int,
        session: AsyncSession
):
    response = await get_author_by_id(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"author not found with id:{id}"
        )
    return response

async def get_authors_service(
        session: AsyncSession
):
    response = await get_authors(
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"author not found"
        )
    return response

async def update_author_service(
        id: int,
        author_update: AuthorUpdate,
        session: AsyncSession
):
    response = await update_author(
        id = id,
        update_author = author_update,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"author not found with id:{id}"
        )
    return response

async def delete_author_service(
        id: int,
        session: AsyncSession
):
    response = await delete_author(
        id = id,
        session = session
    )
    if not response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"author not found with id:{id}"
        )
    return response 