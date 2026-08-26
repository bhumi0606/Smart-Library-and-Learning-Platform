from pydantic import BaseModel, EmailStr, Field

class MemberLogin(BaseModel):
    email: EmailStr = Field(
        description="The email address of the member"
    )
    password: str = Field(
        description="The password of the member"
    )