from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.db.models import BookStatus, BookType
from datetime import datetime, date

class BookResponse(BaseModel):
    id: int = Field(
        description="Unique identifier for the book"
    )
    title: str = Field(
        description="Title of the book"
    )
    published_date: Optional[date] = Field(
        default=None,
        description="Published date of the book"
    )
    isbn: str = Field(
        description="ISBN of the book"
    )
    book_type: BookType = Field(
        description="Type of the book"
    )
    status: BookStatus = Field(
        description="Status of the book"
    )
    created_at: datetime = Field(
        description="Timestamp when the book was created"
    )

    model_config = ConfigDict(from_attributes=True)
