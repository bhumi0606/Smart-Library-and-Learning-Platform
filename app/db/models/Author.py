
# AUTHOR
from datetime import datetime

from sqlalchemy import DateTime, String, func

from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    books: Mapped[list["Book"]] = relationship(
        "Book",
        secondary="book_authors",
        back_populates="authors",
    )