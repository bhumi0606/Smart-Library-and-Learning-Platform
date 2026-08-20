from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime

class MemberResponse(BaseModel):
    id: int = Field(
        description="The unique identifier of the member"
    )
    name: str = Field(
        description="The name of the member"
    )
    email: EmailStr = Field(
        description="The email address of the member"
    )
    created_at: datetime = Field(
        description="The timestamp when the member was created"
    )

    model_config = ConfigDict(from_attributes=True)