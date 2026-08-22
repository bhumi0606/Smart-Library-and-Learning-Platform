from pydantic import BaseModel, Field
from typing import Optional

class CreateCourse(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255,
        description="Title of the course"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Description of the course"
    )