from pydantic import BaseModel, EmailStr, Field

class MemberCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        description="The name of the member"
    )
    email: EmailStr = Field(
        description="The email address of the member"
    )
    password: str = Field(
        min_length=6,
        description="The password of the member"
    )
