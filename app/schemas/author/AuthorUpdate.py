from pydantic import BaseModel, Field
from typing import Optional

class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="The updated name of the author"
    )