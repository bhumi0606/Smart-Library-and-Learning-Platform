from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class UpdateLoan(BaseModel):
    due_date: Optional[date] = Field(
        default=None,
        description="Date when the loan is due"
    )
    return_date: Optional[date] = Field(
        default=None,
        description="Date when the loan was returned"
    )