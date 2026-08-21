from pydantic import BaseModel, Field
from typing import Optional
from app.enums.BookEnums import BookStatus, BookType
from datetime import date

class CreateBook(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
        description="Title of the book"
    )
    published_date: Optional[date] = Field(
        default=None,
        description="Published date of the book"
    )
    isbn: str = Field(
        min_length=10,
        max_length=13,
        description="ISBN of the book"
    )
    book_type: BookType = Field(
        default=BookType.PHYSICAL,
        description="Type of the book"
    )
    status: Optional[BookStatus] = Field(
        default=BookStatus.AVAILABLE,
        description="Status of the book"
    )