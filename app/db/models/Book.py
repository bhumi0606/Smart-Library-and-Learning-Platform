

# BOOK
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, String, func

from app.enums.BookEnums import BookStatus, BookType
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    published_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    isbn: Mapped[str] = mapped_column(
        String(17),
        unique=True,
        nullable=False,
        index=True,
    )

    book_type: Mapped[BookType] = mapped_column(
        Enum(
            BookType,
            name="book_type",
            values_callable=lambda enum_class: [
                member.value for member in enum_class
            ],
        ),
        nullable=False,
    )

    status: Mapped[BookStatus] = mapped_column(
        Enum(
            BookStatus,
            name="book_status",
            values_callable=lambda enum_class: [
                member.value for member in enum_class
            ],
        ),
        default=BookStatus.AVAILABLE,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    loans: Mapped[list["Loan"]] = relationship(
        "Loan",
        back_populates="book",
    )

    authors: Mapped[list["Author"]] = relationship(
        "Author",
        secondary="book_authors",
        back_populates="books",
    )
