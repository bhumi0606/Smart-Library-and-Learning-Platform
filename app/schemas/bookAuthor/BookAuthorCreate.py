from pydantic import BaseModel, Field

class CreateBookAuthor(BaseModel):
    book_id: int = Field(
        description="The ID of the book associated with the author."
    )
    author_id: int = Field(
        description="The ID of the author associated with the book."
    )