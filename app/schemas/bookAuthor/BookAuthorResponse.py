from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class BookAuthorResponse(BaseModel):
    id: int = Field(
        description="Unique identifier for the book-author relationship"
    )
    book_id: int = Field(
        description="The ID of the book associated with the author"
    )
    author_id: int = Field(
        description="The ID of the author associated with the book"
    )
    created_at: datetime = Field(
        description="Timestamp when the book-author relationship was created"
    )
    
    model_config = ConfigDict(from_attributes=True)