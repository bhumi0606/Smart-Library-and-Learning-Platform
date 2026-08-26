from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CreateLoan(BaseModel):
    member_id: int = Field(
        description="The ID of the member who is borrowing the book"
    )
    book_id: int = Field(
        description="The ID of the book being borrowed"
    )
    due_date: datetime = Field(
        description="Timestamp when the loan is due"
    )
