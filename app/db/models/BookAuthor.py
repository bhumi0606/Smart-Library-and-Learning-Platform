# BOOK - AUTHOR
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func

from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class BookAuthor(Base):
    __tablename__ = "book_authors"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
