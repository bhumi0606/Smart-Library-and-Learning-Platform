from pydantic import BaseModel, Field

class MemberLoginResponse(BaseModel):
    access_token:  str = Field(
        description="The access token for the member"
    )
    token_type: str = Field(
        default="bearer",
        description="The type of the token"
    )