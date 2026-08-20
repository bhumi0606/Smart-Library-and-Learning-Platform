from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UpdateLoan(BaseModel):
    due_date: Optional[datetime] = Field(
        description="Timestamp when the loan is due"
    )
    return_date: Optional[datetime] = Field(
        description="Timestamp when the loan was returned"
    )