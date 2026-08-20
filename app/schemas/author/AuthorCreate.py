from pydantic import BaseModel, Field

class AuthorCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        description="The name of the author"
    )