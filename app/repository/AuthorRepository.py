from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.Author import Author
from app.schemas.author.AuthorCreate import AuthorCreate
from app.schemas.author.AuthorUpdate import AuthorUpdate

async def create_author(
        author: AuthorCreate,
        session: AsyncSession
):
    author = Author(
        name = author.name
    )

    session.add(author)
    await session.commit()
    return author

async def get_author_by_id(
        id: int,
        session: AsyncSession
):
    author = await session.execute(
        select(Author).where(Author.id == id)
    )

    return author.scalar_one_or_none()

async def get_authors(
        session: AsyncSession
):
    authors = await session.execute(
        select(Author)
    )
    return authors.scalars().all()

async def update_author(
        id: int,
        update_author: AuthorUpdate,
        session: AsyncSession
):
    author = await get_author_by_id(
        id = id,
        session = session
    )
    if author == None:
        return None
    else:
        if update_author.name:
            author.name = update_author.name

    await session.commit()
    return author

async def delete_author(
        id:int,
        session: AsyncSession
):
    author = await get_author_by_id(
        id = id,
        session = session
    )
    if author == None:
        return None

    await session.delete(author)
    await session.commit()

    return author
    