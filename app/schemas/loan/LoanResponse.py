from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class LoanResponse(BaseModel):
    id: int = Field(
        description="Unique identifier for the loan"
    )
    member_id: int = Field(
        description="The ID of the member who is borrowing the book"
    )
    book_id: int = Field(
        description="The ID of the book being borrowed"
    )
    issued_at: datetime = Field(
        description="Timestamp when the loan was issued"
    )
    due_date: datetime = Field(
        description="Timestamp when the loan is due"
    )
    return_date: Optional[datetime] = Field(
        description="Timestamp when the loan was returned"
    )
    receipt_url: str = Field(
        description="URL of the loan receipt stored in S3"
    )
    
    model_config = ConfigDict(from_attributes=True)