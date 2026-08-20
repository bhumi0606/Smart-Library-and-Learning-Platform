from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class AuthorResponse(BaseModel):
    id: int = Field(
        description="The unique identifier of the author"
    )
    name: str = Field(
        description="The name of the author"
    )
    created_at: datetime = Field(
        description="The timestamp when the author was created"
    )
    
    model_config = ConfigDict(from_attributes=True)