from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class MemberUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="The name of the member"
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="The email address of the member"
    )
    password: Optional[str] = Field(
        default=None,
        min_length=6,
        description="The password of the member"
    )