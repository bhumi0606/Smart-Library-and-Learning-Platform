from pydantic import BaseModel, Field
from typing import Optional
from app.enums.BookEnums import BookStatus, BookType
from datetime import date

class UpdateBook(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Title of the book"
    )
    published_date: Optional[date] = Field(
        default=None,
        description="Published date of the book"
    )
    isbn: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=13,
        description="ISBN of the book"
    )
    book_type: Optional[BookType] = Field(
        default=None,
        description="Type of the book"
    )
    status: Optional[BookStatus] = Field(
        default=None,
        description="Status of the book"
    )